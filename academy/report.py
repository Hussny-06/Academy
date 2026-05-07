"""Weekly Report Generator.

Parses journal archives to produce velocity metrics, faculty distribution,
and failure analysis for weekly review.
"""

import logging
from datetime import date, timedelta
from pathlib import Path

from academy.utils import (
    read_file,
    write_file,
    parse_frontmatter,
    today_str,
    get_week_number,
)

logger = logging.getLogger("academy")


def get_current_week_range() -> tuple[date, date]:
    """Return (monday, sunday) of the current ISO week."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def collect_week_journals(archive_dir: Path, start: date, end: date) -> list[dict]:
    """
    Collect all archived journal entries for the given date range.
    Returns list of parsed frontmatter dicts.
    """
    journals = []

    for md_file in sorted(archive_dir.glob("*.md")):
        content = read_file(md_file)
        fm, body = parse_frontmatter(content)
        if not fm:
            continue

        entry_date_str = fm.get("date")
        if not entry_date_str:
            continue

        try:
            entry_date = date.fromisoformat(str(entry_date_str))
        except (ValueError, TypeError):
            continue

        if start <= entry_date <= end:
            fm["_body"] = body
            fm["_filename"] = md_file.name
            journals.append(fm)

    return journals


def compute_faculty_hours(journals: list[dict]) -> dict[str, float]:
    """Sum hours spent per faculty from journal entries."""
    hours = {}
    for entry in journals:
        faculty = entry.get("faculty", "unknown")
        spent = entry.get("hours_spent")
        if spent is not None:
            try:
                hours[faculty] = hours.get(faculty, 0) + float(spent)
            except (ValueError, TypeError):
                pass
    return hours


def compute_velocity(journals: list[dict]) -> dict:
    """Compute task completion velocity from journal entries."""
    total = len(journals)
    completed = sum(1 for j in journals if j.get("status") == "completed")
    blocked = sum(1 for j in journals if j.get("status") == "blocked")
    partial = sum(1 for j in journals if j.get("status") == "partial")
    total_hours = sum(
        float(j.get("hours_spent", 0))
        for j in journals
        if j.get("hours_spent") is not None
    )

    return {
        "tasks_assigned": total,
        "tasks_completed": completed,
        "tasks_blocked": blocked,
        "tasks_partial": partial,
        "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
        "total_hours": round(total_hours, 1),
    }


def extract_failures(journals: list[dict]) -> list[dict]:
    """Extract blocked/partial entries with their struggle notes."""
    failures = []
    for entry in journals:
        status = entry.get("status", "")
        if status in ("blocked", "partial"):
            failures.append({
                "date": str(entry.get("date", "?")),
                "faculty": entry.get("faculty", "?"),
                "task_id": entry.get("task_id", "?"),
                "status": status.upper(),
                "body": entry.get("_body", "")[:200],  # Truncate for report
            })
    return failures


def generate_weekly_report(
    archive_dir: Path,
    faculty_config: dict,
    weekly_hour_cap: float = 48.0,
) -> str:
    """
    Generate a full weekly report in markdown format.

    Args:
        archive_dir: Path to archive/journal/
        faculty_config: Faculty config dict from config.yaml
        weekly_hour_cap: Total weekly hour cap

    Returns:
        Markdown string for the weekly report.
    """
    monday, sunday = get_current_week_range()
    week_num = get_week_number()

    journals = collect_week_journals(archive_dir, monday, sunday)

    if not journals:
        return (
            f"## Weekly Report — W{week_num:02d} "
            f"({monday.isoformat()} to {sunday.isoformat()})\n\n"
            "No journal entries found for this week.\n"
        )

    velocity = compute_velocity(journals)
    faculty_hours = compute_faculty_hours(journals)
    failures = extract_failures(journals)

    # Build the report
    lines = [
        f"## Weekly Report — W{week_num:02d} "
        f"({monday.isoformat()} to {sunday.isoformat()})",
        "",
        "### Velocity",
        f"- Tasks assigned: {velocity['tasks_assigned']}",
        f"- Tasks completed: {velocity['tasks_completed']}",
        f"- Completion rate: {velocity['completion_rate']}%",
        f"- Hours logged: {velocity['total_hours']}h / {weekly_hour_cap}h cap",
        "",
        "### Faculty Distribution",
    ]

    for key, fconf in faculty_config.items():
        name = fconf["name"]
        target_pct = fconf["weight"] * 100
        actual_hours = faculty_hours.get(key, 0)
        actual_pct = (
            round(actual_hours / velocity["total_hours"] * 100, 1)
            if velocity["total_hours"] > 0
            else 0
        )
        diff = actual_pct - target_pct
        emoji = "✅" if abs(diff) <= 3 else ("⚠️" if abs(diff) <= 7 else "🔴")
        diff_str = f" ({diff:+.0f}%)" if abs(diff) > 1 else ""
        lines.append(
            f"- {name}: {actual_hours}h ({actual_pct}%) {emoji}{diff_str}"
        )

    if failures:
        lines.extend(["", "### Failure Analysis"])
        for f in failures:
            lines.append(
                f"- {f['status']}: [{f['faculty']}] {f['task_id']} "
                f"({f['date']})"
            )
            if f["body"]:
                # Extract first meaningful line of the body
                for bline in f["body"].splitlines():
                    bline = bline.strip()
                    if bline and not bline.startswith("#"):
                        lines.append(f"  → {bline[:120]}")
                        break

    lines.append("")
    return "\n".join(lines)
