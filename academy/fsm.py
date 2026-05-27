"""Academy Finite State Machine.

The core orchestration engine. Implements the ReAct loop as a
deterministic state machine with explicit transitions.

States:
    IDLE → READ_JOURNAL → PROCESS_INTEL → ASSESS_POSITION →
    CHECK_SR → GENERATE_SPRINT → WRITE_OUTPUT → ARCHIVE → IDLE

Error handling: Any state can transition to ERROR, which logs
the failure and transitions back to IDLE.
"""

import logging
import re
from datetime import date, timedelta
from pathlib import Path

from academy.utils import (
    load_config,
    resolve_path,
    read_file,
    write_file,
    parse_frontmatter,
    is_file_empty_or_placeholder,
    archive_file,
    extract_syllabus_progress,
    extract_week_resources,
    today_str,
    now_str,
    get_day_of_week,
    get_week_number,
)
from academy.sm2 import SpacedRepetitionEngine
from academy.ollama import OllamaClient, OllamaError
from academy.report import generate_weekly_report, collect_week_journals, compute_faculty_hours, get_current_week_range

logger = logging.getLogger("academy")


class AcademyFSM:
    """
    Finite State Machine for the Academy orchestrator.

    Each state is a method that returns the next state name.
    The run() method drives the machine until it reaches IDLE.
    """

    STATES = [
        "IDLE",
        "READ_JOURNAL",
        "PROCESS_INTEL",
        "ASSESS_POSITION",
        "CHECK_SR",
        "GENERATE_SPRINT",
        "WRITE_OUTPUT",
        "ARCHIVE",
        "ERROR",
    ]

    def __init__(self, config_path: Path = None, mode: str = "sprint"):
        """
        Args:
            config_path: Path to config.yaml (defaults to project root).
            mode: 'sprint' for daily sprint generation, 'review' for weekly review.
        """
        self.config = load_config(config_path)
        self.mode = mode
        self.state = "IDLE"

        # Resolve paths
        self.state_dir = resolve_path(self.config["paths"]["state_dir"])
        self.archive_dir = resolve_path(self.config["paths"]["archive_dir"])
        self.syllabus_dir = resolve_path(self.config["paths"]["syllabus_dir"])
        self.prompts_dir = resolve_path(self.config["paths"]["prompts_dir"])
        self.logs_dir = resolve_path(self.config["paths"]["logs_dir"])

        # State file paths
        self.journal_path = self.state_dir / "user_journal.md"
        self.sprint_path = self.state_dir / "active_sprint.md"
        self.intel_drop_path = self.state_dir / "intel_drop.md"
        self.intel_analysis_path = self.state_dir / "intel_analysis.md"
        self.competency_path = self.state_dir / "competency_matrix.md"
        self.weekly_report_path = self.state_dir / "weekly_report.md"

        # Context accumulated across states (fed to LLM)
        self.context = {
            "journal_fm": {},
            "journal_body": "",
            "intel_content": None,
            "syllabus_progress": {},
            "weekly_hours": {},
            "sr_due_items": "",
            "competency_snapshot": "",
            "underweight_faculties": "",
        }

        # Components
        self.sr_engine = SpacedRepetitionEngine(
            self.state_dir / "spaced_repetition.md", self.config
        )
        self.ollama = OllamaClient(self.config)

        # Output buffer
        self.output = ""
        self.error_message = ""

    def run(self) -> bool:
        """
        Execute one full cycle of the state machine.

        Returns:
            True if cycle completed successfully, False on error.
        """
        logger.info(f"=== Academy FSM Start (mode={self.mode}) ===")
        logger.info(f"Date: {today_str()}, Day: {get_day_of_week()}")

        # Check rest day
        if self._is_rest_day() and self.mode == "sprint":
            logger.info("Today is a rest day. Processing intel only (if any).")
            # On rest days, only process intel drops — no sprint
            if not is_file_empty_or_placeholder(self.intel_drop_path):
                self.state = "PROCESS_INTEL"
                self._run_state("PROCESS_INTEL")
            else:
                logger.info("No intel to process. Enjoy your day off!")
            return True

        # Check for weekly review mode
        if self.mode == "review":
            return self._run_weekly_review()

        # Normal sprint generation cycle
        transitions = {
            "IDLE": self._state_idle,
            "READ_JOURNAL": self._state_read_journal,
            "PROCESS_INTEL": self._state_process_intel,
            "ASSESS_POSITION": self._state_assess_position,
            "CHECK_SR": self._state_check_sr,
            "GENERATE_SPRINT": self._state_generate_sprint,
            "WRITE_OUTPUT": self._state_write_output,
            "ARCHIVE": self._state_archive,
            "ERROR": self._state_error,
        }

        self.state = "IDLE"
        max_transitions = 20  # Safety net against infinite loops

        for _ in range(max_transitions):
            handler = transitions.get(self.state)
            if handler is None:
                logger.error(f"Unknown state: {self.state}")
                break

            next_state = handler()
            logger.info(f"Transition: {self.state} → {next_state}")
            self.state = next_state

            if self.state == "IDLE":
                logger.info("=== Academy FSM Complete ===")
                return True

        logger.error("FSM exceeded max transitions — possible infinite loop")
        return False

    def _run_state(self, state_name: str) -> None:
        """Run a single state by name."""
        handlers = {
            "PROCESS_INTEL": self._state_process_intel,
        }
        handler = handlers.get(state_name)
        if handler:
            handler()

    # ──────────────────────────────────────────────────────────
    # FSM States
    # ──────────────────────────────────────────────────────────

    def _state_idle(self) -> str:
        """Check preconditions and decide whether to start a cycle."""
        # Pre-flight: check Ollama
        if not self.ollama.health_check():
            self.error_message = (
                "Ollama is not running. Start it with: ollama serve\n"
                f"Expected at: {self.config['ollama_url']}"
            )
            return "ERROR"

        if not self.ollama.is_model_available():
            self.error_message = (
                f"Model '{self.config['model']}' not found. Pull it with:\n"
                f"ollama pull {self.config['model']}"
            )
            return "ERROR"

        # Pre-flight: check for CUDA conflicts
        cuda_warning = self.ollama.check_cuda_conflict()
        if cuda_warning:
            logger.warning(cuda_warning)

        # Check if journal has content to process
        has_journal = not is_file_empty_or_placeholder(self.journal_path)

        if has_journal:
            return "READ_JOURNAL"
        else:
            logger.info("No journal entry found. Skipping to position assessment.")
            # Even without a journal, we can still generate a sprint
            return "ASSESS_POSITION"

    def _state_read_journal(self) -> str:
        """Parse the user journal and extract structured data."""
        content = read_file(self.journal_path)
        fm, body = parse_frontmatter(content)

        if not fm and not body:
            logger.warning("Journal exists but is empty/unparseable.")
            return "ASSESS_POSITION"

        self.context["journal_fm"] = fm
        self.context["journal_body"] = body

        # Process SR grades from the journal
        sr_grades = fm.get("sr_grades", [])
        if sr_grades and isinstance(sr_grades, list):
            self.sr_engine.process_journal_grades(sr_grades)
            logger.info(f"Processed {len(sr_grades)} SR grades from journal")

        logger.info(
            f"Journal parsed: faculty={fm.get('faculty')}, "
            f"status={fm.get('status')}, hours={fm.get('hours_spent')}"
        )

        # Check for intel before assessing position
        if not is_file_empty_or_placeholder(self.intel_drop_path):
            return "PROCESS_INTEL"

        return "ASSESS_POSITION"

    def _state_process_intel(self) -> str:
        """Analyze intel drops using the LLM."""
        content = read_file(self.intel_drop_path)
        fm, body = parse_frontmatter(content)

        if not body or body.startswith(">"):
            logger.info("Intel drop is empty or placeholder. Skipping.")
            return "ASSESS_POSITION"

        logger.info("Processing intel drop...")

        # Load prompt template
        template = read_file(self.prompts_dir / "intel_analysis.md")
        system_prompt = read_file(self.prompts_dir / "system_prompt.md")
        competency = read_file(self.competency_path)

        # Build syllabus summary
        syllabus_summary = self._build_syllabus_summary()

        # Fill template
        prompt = template.format(
            intel_content=body,
            intel_type=fm.get("type", "unknown"),
            intel_source=fm.get("source", "unknown"),
            intel_date=fm.get("date", today_str()),
            competency_matrix=competency,
            syllabus_summary=syllabus_summary,
        )

        try:
            analysis = self.ollama.generate(prompt, system_prompt)
            write_file(
                self.intel_analysis_path,
                f"# Intel Analysis — {today_str()}\n\n"
                f"**Source:** {fm.get('source', 'unknown')}\n\n"
                f"{analysis}\n",
            )

            # Archive the intel drop
            archive_file(
                self.intel_drop_path,
                self.archive_dir / "intel",
                prefix="intel_",
            )

            # Reset intel drop to empty
            write_file(
                self.intel_drop_path,
                "# Intel Drop\n\n"
                "> Paste job descriptions, tech trends, or skill alerts below.\n"
                "> Add a YAML frontmatter with date, type, and source.\n"
                "> The orchestrator will process this on the next run.\n",
            )

            logger.info("Intel analysis complete and archived.")

        except OllamaError as e:
            logger.error(f"Intel analysis failed: {e}")
            # Non-fatal — continue to sprint generation

        return "ASSESS_POSITION"

    def _state_assess_position(self) -> str:
        """Cross-reference journal with syllabi to determine position."""
        # Load all syllabus progress
        faculty_config = self.config["faculties"]
        progress = {}

        for key, fconf in faculty_config.items():
            syllabus_path = resolve_path(fconf["syllabus"])
            syllabus_text = read_file(syllabus_path)
            if syllabus_text:
                progress[key] = extract_syllabus_progress(syllabus_text)
                progress[key]["name"] = fconf["name"]
            else:
                progress[key] = {
                    "name": fconf["name"],
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "progress_pct": 0,
                    "current_week": "Not started",
                    "current_topics": [],
                }

        self.context["syllabus_progress"] = progress

        # Compute this week's faculty hours from archives
        monday, sunday = get_current_week_range()
        journal_archive = self.archive_dir / "journal"
        week_journals = collect_week_journals(journal_archive, monday, sunday)
        self.context["weekly_hours"] = compute_faculty_hours(week_journals)

        # Determine underweight faculties
        total_hours = sum(self.context["weekly_hours"].values()) or 0.01
        underweight = []
        for key, fconf in faculty_config.items():
            target_pct = fconf["weight"]
            actual_hours = self.context["weekly_hours"].get(key, 0)
            actual_pct = actual_hours / total_hours if total_hours > 0 else 0
            deficit = target_pct - actual_pct
            if deficit > 0.05:  # More than 5% below target
                underweight.append(
                    f"- {fconf['name']}: {actual_pct*100:.0f}% actual vs "
                    f"{target_pct*100:.0f}% target (deficit: {deficit*100:.0f}%)"
                )

        self.context["underweight_faculties"] = (
            "\n".join(underweight) if underweight else "All faculties on track."
        )

        logger.info(
            f"Position assessed: {len(progress)} faculties, "
            f"weekly hours so far: {total_hours:.1f}h"
        )

        return "CHECK_SR"

    def _state_check_sr(self) -> str:
        """Check spaced repetition queue for due items."""
        self.context["sr_due_items"] = self.sr_engine.format_due_items_for_prompt()
        due_count = len(self.sr_engine.get_due_items())
        logger.info(f"SR check: {due_count} items due")
        return "GENERATE_SPRINT"

    def _state_generate_sprint(self) -> str:
        """Build the full prompt and call Ollama to generate the sprint."""
        system_prompt = read_file(self.prompts_dir / "system_prompt.md")
        template = read_file(self.prompts_dir / "sprint_gen.md")
        competency = read_file(self.competency_path)

        # Build syllabus progress summary
        syllabus_summary = self._build_syllabus_summary()

        # Build weekly hours summary
        weekly_summary = self._build_weekly_hours_summary()

        # Extract journal metadata
        fm = self.context.get("journal_fm", {})

        # Fill the template
        prompt = template.format(
            today_date=today_str(),
            day_of_week=get_day_of_week().capitalize(),
            week_number=get_week_number(),
            journal_body=self.context.get("journal_body", "No journal entry today."),
            journal_faculty=fm.get("faculty", "N/A"),
            journal_status=fm.get("status", "N/A"),
            journal_hours=fm.get("hours_spent", "N/A"),
            journal_difficulty=fm.get("difficulty_rating", "N/A"),
            journal_blocker=fm.get("blocker", "None"),
            syllabus_progress=syllabus_summary,
            weekly_hours_summary=weekly_summary,
            underweight_faculties=self.context["underweight_faculties"],
            sr_due_items=self.context["sr_due_items"],
            competency_snapshot=competency[:2000],  # Truncate for context window
        )

        try:
            self.output = self.ollama.generate(prompt, system_prompt)
            logger.info(f"Sprint generated: {len(self.output)} chars")

            # Quality gate: validate output before writing
            quality_ok, quality_msg = self._validate_sprint_quality(self.output)
            if not quality_ok:
                logger.warning(f"Sprint quality check failed: {quality_msg}")
                logger.info("Retrying sprint generation (attempt 2/2)...")
                try:
                    self.output = self.ollama.generate(prompt, system_prompt)
                    quality_ok, quality_msg = self._validate_sprint_quality(
                        self.output
                    )
                    if not quality_ok:
                        logger.warning(
                            f"Retry also failed quality check: {quality_msg}. "
                            f"Writing output with warning header."
                        )
                        self.output = (
                            f"> ⚠️ **Quality Warning:** {quality_msg}\n\n"
                            + self.output
                        )
                except OllamaError as retry_err:
                    logger.error(f"Retry failed: {retry_err}")
                    # Use the first attempt's output with a warning
                    self.output = (
                        f"> ⚠️ **Quality Warning:** {quality_msg} "
                        f"(retry also failed)\n\n" + self.output
                    )

            return "WRITE_OUTPUT"
        except OllamaError as e:
            self.error_message = f"Sprint generation failed: {e}"
            return "ERROR"

    def _state_write_output(self) -> str:
        """Write the generated sprint to active_sprint.md."""
        # Strip any LLM-hallucinated resource sections from output
        cleaned_output = self._strip_llm_resources(self.output)

        # Build the sprint file content
        content_parts = [
            f"# Active Sprint — {today_str()}\n",
            f"*Generated at {now_str()}*\n\n",
            cleaned_output,
        ]

        # Inject verified resources from the syllabus
        verified_resources = self._get_verified_resources()
        if verified_resources:
            content_parts.append(f"\n{verified_resources}")
        else:
            logger.info("No curated resources found for current week in syllabus.")

        # Append Friday intel reminder if applicable
        if get_day_of_week() == self.config.get("intel_reminder_day", "friday"):
            content_parts.append(self._build_intel_reminder())

        write_file(self.sprint_path, "\n".join(content_parts))
        logger.info("Sprint written to active_sprint.md")

        return "ARCHIVE"

    def _state_archive(self) -> str:
        """Archive the journal (never delete) and clean up."""
        if not is_file_empty_or_placeholder(self.journal_path):
            archive_file(
                self.journal_path,
                self.archive_dir / "journal",
            )

            # Reset journal to empty template
            template = (
                "---\n"
                "date:\n"
                "faculty:\n"
                "task_id:\n"
                "status:\n"
                "difficulty_rating:\n"
                "sr_grades: []\n"
                "blocker: null\n"
                "hours_spent:\n"
                "sleep_hours:\n"
                "workout:\n"
                "---\n\n"
                "## What I Built\n\n\n"
                "## Where I Struggled\n\n"
            )
            write_file(self.journal_path, template)
            logger.info("Journal archived and reset.")

        # Also archive the previous sprint
        if not is_file_empty_or_placeholder(self.sprint_path):
            # The sprint was just written, so we archive it as a backup
            pass  # Current sprint stays active; it gets archived next cycle

        return "IDLE"

    def _state_error(self) -> str:
        """Handle errors gracefully."""
        logger.error(f"FSM Error: {self.error_message}")

        # Write error to log file
        error_log = self.logs_dir / "error.log"
        error_log.parent.mkdir(parents=True, exist_ok=True)
        with open(error_log, "a", encoding="utf-8") as f:
            f.write(f"[{now_str()}] {self.error_message}\n")

        return "IDLE"

    # ──────────────────────────────────────────────────────────
    # Weekly Review Mode
    # ──────────────────────────────────────────────────────────

    def _run_weekly_review(self) -> bool:
        """Execute the weekly review cycle."""
        logger.info("Running weekly review...")

        # Pre-flight
        if not self.ollama.health_check():
            logger.error("Ollama not available for weekly review.")
            return False

        # Generate velocity report from archives
        report = generate_weekly_report(
            archive_dir=self.archive_dir / "journal",
            faculty_config=self.config["faculties"],
            weekly_hour_cap=self.config["daily_hour_cap"] * 6,  # 6 working days
        )

        # Load context for LLM
        competency = read_file(self.competency_path)
        syllabus_summary = self._build_syllabus_summary()
        due_items = self.sr_engine.get_due_items()

        # Calculate SR stats
        all_items = self.sr_engine.items
        sr_total = len(all_items)
        sr_due_count = len(due_items)
        sr_avg_ef = (
            sum(i.ef for i in all_items) / sr_total if sr_total > 0 else 2.5
        )

        # Load weekly review prompt
        template = read_file(self.prompts_dir / "weekly_review.md")
        system_prompt = read_file(self.prompts_dir / "system_prompt.md")

        prompt = template.format(
            today_date=today_str(),
            week_number=get_week_number(),
            weekly_report=report,
            competency_matrix=competency[:2000],
            all_syllabus_progress=syllabus_summary,
            sr_total=sr_total,
            sr_due_count=sr_due_count,
            sr_avg_ef=f"{sr_avg_ef:.2f}",
        )

        try:
            review_output = self.ollama.generate(prompt, system_prompt)

            # Write the combined report
            full_report = (
                f"# Weekly Review — {today_str()}\n\n"
                f"*Generated at {now_str()}*\n\n"
                f"{report}\n\n"
                f"---\n\n"
                f"## AI Analysis\n\n"
                f"{review_output}\n"
            )

            write_file(self.weekly_report_path, full_report)

            # Archive the report
            archive_file(
                self.weekly_report_path,
                self.archive_dir / "sprints",
                prefix="review_",
            )

            # Process SR recommendations from the review
            self._extract_sr_recommendations(review_output)

            logger.info("Weekly review complete.")
            return True

        except OllamaError as e:
            logger.error(f"Weekly review failed: {e}")
            # Still write the data-only report
            write_file(self.weekly_report_path, f"# Weekly Report\n\n{report}\n")
            return False

    # ──────────────────────────────────────────────────────────
    # Helper Methods
    # ──────────────────────────────────────────────────────────

    def _is_rest_day(self) -> bool:
        """Check if today is a configured rest day."""
        return get_day_of_week() == self.config.get("rest_day", "sunday")

    def _strip_llm_resources(self, output: str) -> str:
        """
        Strip LLM-hallucinated resource sections from sprint output.

        The LLM often generates fake URLs in 'Resources' sections.
        We remove these and replace with verified resources from the syllabus.
        """
        lines = output.splitlines()
        cleaned = []
        skip = False

        for line in lines:
            stripped = line.strip()
            # Detect resource section headers (various formats the LLM uses)
            if any(
                marker in stripped.lower()
                for marker in [
                    "### resources",
                    "### 📚 resources",
                    "### 📖 resources",
                    "resources (study these first)",
                ]
            ):
                skip = True
                continue

            # Stop skipping when we hit the next section
            if skip and stripped.startswith("### "):
                skip = False

            if not skip:
                cleaned.append(line)

        return "\n".join(cleaned)

    def _get_verified_resources(self) -> str:
        """
        Extract curated resources from the current week's syllabus.

        Determines which faculty is being assigned and pulls the
        resource links from that syllabus's current week.
        """
        faculties = self.config.get("faculties", {})

        # Strategy 1: From journal faculty
        target_faculty = self.context.get("journal_fm", {}).get("faculty")

        # Strategy 2: Detect from sprint output text
        if not target_faculty and self.output:
            output_lower = self.output.lower()
            for key, fconf in faculties.items():
                # Check both key ("cpp") and name ("C++ / Systems")
                if key in output_lower or fconf["name"].lower() in output_lower:
                    target_faculty = key
                    break

        # Strategy 3: Try all faculties and return first one with resources
        if not target_faculty:
            for key in faculties:
                resources = self._try_extract_resources(key)
                if resources:
                    return resources
            return ""

        return self._try_extract_resources(target_faculty)

    def _try_extract_resources(self, faculty_key: str) -> str:
        """Try to extract resources for a given faculty key."""
        faculty_config = self.config.get("faculties", {}).get(faculty_key)
        if not faculty_config:
            return ""

        syllabus_path = resolve_path(faculty_config["syllabus"])
        syllabus_text = read_file(syllabus_path)
        if not syllabus_text:
            return ""

        progress = extract_syllabus_progress(syllabus_text)
        current_week = progress.get("current_week", "")

        if not current_week or current_week == "Not started":
            return ""

        resources = extract_week_resources(syllabus_text, current_week)
        if resources:
            logger.info(f"Injected verified resources from {faculty_key}: {current_week}")
        return resources

    def _validate_sprint_quality(self, output: str) -> tuple[bool, str]:
        """
        Validate that the LLM output is a usable sprint.

        Checks for:
        - Minimum length (not empty or trivially short)
        - No refusal/apology patterns (model declining to respond)
        - Contains some structure (headers, lists, or code blocks)

        Returns:
            (is_valid, message) tuple.
        """
        # Check 1: Minimum length
        if len(output.strip()) < 100:
            return False, f"Output too short ({len(output.strip())} chars, need 100+)"

        output_lower = output.lower()

        # Check 2: Refusal/apology patterns
        refusal_patterns = [
            "i cannot",
            "i can't",
            "i'm sorry",
            "i apologize",
            "as an ai",
            "i'm unable",
            "i don't have enough",
            "i need more context",
        ]
        for pattern in refusal_patterns:
            if pattern in output_lower and len(output.strip()) < 300:
                return False, f"Model appears to have refused (detected: '{pattern}')"

        # Check 3: Has some structure (at least one header, list item, or code block)
        has_header = "#" in output
        has_list = "- " in output or "1." in output
        has_code = "```" in output
        if not (has_header or has_list or has_code):
            return False, "Output lacks structure (no headers, lists, or code blocks)"

        return True, "OK"

    def _build_syllabus_summary(self) -> str:
        """Build a compact syllabus progress summary for the prompt."""
        lines = []
        faculty_config = self.config["faculties"]

        for key, fconf in faculty_config.items():
            syllabus_path = resolve_path(fconf["syllabus"])
            syllabus_text = read_file(syllabus_path)
            if not syllabus_text:
                lines.append(f"- **{fconf['name']}**: No syllabus found")
                continue

            prog = extract_syllabus_progress(syllabus_text)
            lines.append(
                f"- **{fconf['name']}**: {prog['progress_pct']}% complete "
                f"({prog['completed_tasks']}/{prog['total_tasks']} tasks)"
            )
            if prog["current_week"] != "Not started":
                lines.append(f"  Current: {prog['current_week']}")
                for topic in prog["current_topics"][:3]:
                    lines.append(f"    - {topic}")

        return "\n".join(lines)

    def _build_weekly_hours_summary(self) -> str:
        """Build a weekly hours summary showing actual vs target per faculty."""
        weekly_hours = self.context.get("weekly_hours", {})
        total_hours = sum(weekly_hours.values()) or 0
        faculty_config = self.config["faculties"]
        weekly_cap = self.config["daily_hour_cap"] * 6

        lines = [f"**Total this week: {total_hours:.1f}h / {weekly_cap}h cap**\n"]

        for key, fconf in faculty_config.items():
            target_hours = fconf["weight"] * weekly_cap
            actual = weekly_hours.get(key, 0)
            status = "✅" if actual >= target_hours * 0.8 else "⚠️"
            lines.append(
                f"- {fconf['name']}: {actual:.1f}h / {target_hours:.1f}h target {status}"
            )

        return "\n".join(lines)

    def _build_intel_reminder(self) -> str:
        """Build the Friday intel session reminder block."""
        companies = self.config.get("target_companies", [])
        company_links = "\n".join(
            f"{i+1}. [{c['name']}]({c['careers_url']})"
            for i, c in enumerate(companies[:5])
        )

        return (
            "\n\n---\n\n"
            "## 🔍 Weekly Intel Session (15 min)\n\n"
            "It's Friday. Spend 15 minutes scanning these pages and paste "
            "anything relevant into `state/intel_drop.md`:\n\n"
            f"{company_links}\n\n"
            "**Format:** Just paste the raw JD text. Add a YAML header with "
            "`type:` and `source:`. The orchestrator handles the rest.\n"
        )

    def _extract_sr_recommendations(self, review_text: str) -> None:
        """Extract SR recommendations from the weekly review and add them."""
        # Look for lines matching: - concept_name (faculty_key)
        pattern = re.compile(r"^-\s+(.+?)\s+\((\w+)\)\s*$", re.MULTILINE)
        in_sr_section = False

        for line in review_text.splitlines():
            if "SR_RECOMMENDATIONS" in line or "sr_recommendations" in line.lower():
                in_sr_section = True
                continue
            if in_sr_section and line.startswith("#"):
                break  # Hit next section
            if in_sr_section:
                match = pattern.match(line.strip())
                if match:
                    concept = match.group(1).strip()
                    faculty = match.group(2).strip()
                    self.sr_engine.add_item(concept, faculty)
