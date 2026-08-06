"""SM-2 Spaced Repetition Engine.

Implements the SuperMemo 2 algorithm for scheduling concept reviews.
All state is persisted in state/spaced_repetition.md as a markdown table.
"""

import logging
from datetime import date, timedelta
from pathlib import Path

from academy.utils import (
    read_file,
    write_file,
    parse_markdown_table,
    build_markdown_table,
    today_str,
)

logger = logging.getLogger("academy")

# Table column headers (must match the markdown file)
SR_HEADERS = ["Concept", "Faculty", "Sprint", "Last Review", "Interval (days)", "EF", "Next Due"]


class SR_Item:
    """A single spaced repetition item."""

    def __init__(
        self,
        concept: str,
        faculty: str,
        sprint: str,
        last_review: str,
        interval: int,
        ef: float,
        next_due: str,
    ):
        self.concept = concept
        self.faculty = faculty
        self.sprint = sprint
        self.last_review = last_review
        self.interval = interval
        self.ef = ef
        self.next_due = next_due

    def to_row(self) -> dict:
        return {
            "Concept": self.concept,
            "Faculty": self.faculty,
            "Sprint": self.sprint,
            "Last Review": self.last_review,
            "Interval (days)": str(self.interval),
            "EF": f"{self.ef:.2f}",
            "Next Due": self.next_due,
        }

    @classmethod
    def from_row(cls, row: dict) -> "SR_Item":
        return cls(
            concept=row.get("Concept", ""),
            faculty=row.get("Faculty", ""),
            sprint=row.get("Sprint", ""),
            last_review=row.get("Last Review", today_str()),
            interval=int(row.get("Interval (days)", "1")),
            ef=float(row.get("EF", "2.5")),
            next_due=row.get("Next Due", today_str()),
        )


class SpacedRepetitionEngine:
    """Manages the SM-2 spaced repetition queue."""

    def __init__(self, sr_path: Path, config: dict):
        self.sr_path = sr_path
        self.min_ef = config.get("sr_minimum_ef", 1.3)
        self.initial_ef = config.get("sr_initial_ef", 2.5)
        self.initial_interval = config.get("sr_initial_interval", 1)
        self.second_interval = config.get("sr_second_interval", 6)
        self.items: list[SR_Item] = []
        self._load()

    def _load(self) -> None:
        """Load SR items from the markdown table."""
        content = read_file(self.sr_path)
        if not content.strip():
            self.items = []
            return

        rows = parse_markdown_table(content)
        self.items = [SR_Item.from_row(r) for r in rows]
        logger.info(f"Loaded {len(self.items)} SR items")

    def _save(self) -> None:
        """Save SR items back to the markdown table."""
        rows = [item.to_row() for item in self.items]
        table = build_markdown_table(SR_HEADERS, rows)
        content = f"# Spaced Repetition Queue (SM-2)\n\n{table}\n"
        write_file(self.sr_path, content)

    def get_due_items(self, as_of: str = None) -> list[SR_Item]:
        """Return items that are due for review on or before the given date."""
        check_date = date.fromisoformat(as_of) if as_of else date.today()
        due = []
        for item in self.items:
            try:
                due_date = date.fromisoformat(item.next_due)
                if due_date <= check_date:
                    due.append(item)
            except ValueError:
                # If date can't be parsed, consider it due
                due.append(item)
        return due

    def add_item(self, concept: str, faculty: str, sprint: str = "") -> None:
        """Add a new concept to the SR queue."""
        # Check for duplicates
        for item in self.items:
            if item.concept.lower() == concept.lower():
                logger.info(f"SR item already exists: {concept}")
                return

        new_item = SR_Item(
            concept=concept,
            faculty=faculty,
            sprint=sprint,
            last_review=today_str(),
            interval=self.initial_interval,
            ef=self.initial_ef,
            next_due=today_str(),
        )
        self.items.append(new_item)
        self._save()
        logger.info(f"Added SR item: {concept} ({faculty}, sprint={sprint})")

    def review_item(self, concept: str, grade: int) -> None:
        """
        Process a review for a concept with the given grade (0-5).

        SM-2 Algorithm:
        - grade < 3: reset interval to 1, keep EF
        - grade >= 3: update interval and EF

        EF formula:
            EF' = EF + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
            EF = max(EF', min_ef)

        Interval:
            n=1: interval = 1
            n=2: interval = 6
            n>2: interval = round(prev_interval * EF)
        """
        grade = max(0, min(5, grade))  # Clamp to 0-5

        for item in self.items:
            if item.concept.lower() == concept.lower():
                # Update EF
                new_ef = item.ef + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
                item.ef = max(new_ef, self.min_ef)

                if grade < 3:
                    # Failed review — reset to beginning
                    item.interval = self.initial_interval
                else:
                    # Successful review — advance interval
                    if item.interval == self.initial_interval:
                        item.interval = self.second_interval
                    else:
                        item.interval = round(item.interval * item.ef)

                item.last_review = today_str()
                item.next_due = (
                    date.today() + timedelta(days=item.interval)
                ).isoformat()

                self._save()
                logger.info(
                    f"Reviewed '{concept}': grade={grade}, "
                    f"EF={item.ef:.2f}, next_interval={item.interval}d, "
                    f"next_due={item.next_due}"
                )
                return

        logger.warning(f"SR item not found for review: {concept}")

    def process_journal_grades(self, sr_grades: list[dict]) -> None:
        """
        Process SR grades from a journal entry.

        Expects list of dicts: [{"concept": "...", "grade": N}, ...]
        """
        if not sr_grades:
            return

        for entry in sr_grades:
            concept = entry.get("concept", "")
            grade = entry.get("grade", 0)
            if concept:
                self.review_item(concept, grade)

    def format_due_items_for_prompt(self, max_items: int = 5) -> str:
        """Format due items as a markdown snippet for the LLM prompt."""
        due = self.get_due_items()
        if not due:
            return "No spaced repetition items due today."

        lines = ["**Spaced Repetition Items Due Today:**"]
        for item in due[:max_items]:
            overdue = (date.today() - date.fromisoformat(item.next_due)).days
            status = f" (overdue by {overdue}d)" if overdue > 0 else ""
            lines.append(f"- [{item.faculty}] {item.concept}{status} (EF: {item.ef:.1f})")

        if len(due) > max_items:
            lines.append(f"- ...and {len(due) - max_items} more items")

        return "\n".join(lines)
