"""Utility functions for file I/O, date handling, and markdown parsing."""

import os
import re
import shutil
import logging
from datetime import datetime, date
from pathlib import Path

import yaml

logger = logging.getLogger("academy")


def get_base_dir() -> Path:
    """Return the base directory of the Academy project."""
    return Path(__file__).resolve().parent.parent


def load_config(config_path: Path = None) -> dict:
    """Load and return the config.yaml as a dictionary."""
    if config_path is None:
        config_path = get_base_dir() / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(relative_path: str) -> Path:
    """Resolve a relative path against the Academy base directory."""
    return get_base_dir() / relative_path


def read_file(path: Path) -> str:
    """Read and return the full contents of a file. Returns empty string if missing."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def write_file(path: Path, content: str) -> None:
    """Write content to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Wrote {len(content)} bytes to {path}")


def append_file(path: Path, content: str) -> None:
    """Append content to a file, creating it if it doesn't exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from a markdown file.

    Returns:
        (frontmatter_dict, body_text)

    If no frontmatter is found, returns ({}, full_text).
    """
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)"
    match = re.match(pattern, text, re.DOTALL)
    if not match:
        return {}, text

    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse YAML frontmatter: {e}")
        frontmatter = {}

    body = match.group(2).strip()
    return frontmatter, body


def build_frontmatter(data: dict, body: str = "") -> str:
    """Build a markdown file with YAML frontmatter."""
    fm = yaml.dump(data, default_flow_style=False, allow_unicode=True).strip()
    result = f"---\n{fm}\n---\n"
    if body:
        result += f"\n{body}\n"
    return result


def today_str() -> str:
    """Return today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def now_str() -> str:
    """Return current datetime as ISO string."""
    return datetime.now().isoformat(timespec="seconds")


def get_day_of_week() -> str:
    """Return lowercase day of the week (e.g., 'monday', 'friday')."""
    return datetime.now().strftime("%A").lower()


def get_week_number() -> int:
    """Return ISO week number of the current date."""
    return date.today().isocalendar()[1]


def is_file_empty_or_placeholder(path: Path) -> bool:
    """Check if a file is empty or contains only placeholder content."""
    content = read_file(path).strip()
    if not content:
        return True
    # Check for common placeholder patterns
    if content.startswith(">") and len(content.splitlines()) <= 3:
        return True
    # Check if frontmatter values are all empty
    fm, body = parse_frontmatter(content)
    if fm and not body:
        # All frontmatter values are None/empty
        if all(v is None or v == [] or v == "" for v in fm.values()):
            return True
    return False


def archive_file(source: Path, archive_dir: Path, prefix: str = "") -> Path:
    """
    Move a file to the archive directory with a date-stamped name.
    Returns the path to the archived file.
    """
    date_stamp = today_str()
    suffix = source.suffix
    name = f"{prefix}{date_stamp}{suffix}" if prefix else f"{date_stamp}{suffix}"
    dest = archive_dir / name

    # Handle duplicate names (multiple entries per day)
    counter = 1
    while dest.exists():
        name = f"{prefix}{date_stamp}_{counter}{suffix}"
        dest = archive_dir / name
        counter += 1

    archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    logger.info(f"Archived {source.name} -> {dest}")
    return dest


def parse_markdown_table(text: str) -> list[dict]:
    """
    Parse a markdown table into a list of dictionaries.
    Handles tables with | delimiters.
    """
    lines = text.strip().splitlines()
    rows = []
    headers = None

    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue

        cells = [c.strip() for c in line.strip("|").split("|")]

        if headers is None:
            headers = cells
            continue

        # Skip separator row (|---|---|---|)
        if all(re.match(r"^[-:]+$", c) for c in cells):
            continue

        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))

    return rows


def build_markdown_table(headers: list[str], rows: list[dict]) -> str:
    """Build a markdown table string from headers and row dicts."""
    if not headers:
        return ""

    lines = []
    # Header row
    lines.append("| " + " | ".join(headers) + " |")
    # Separator
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    # Data rows
    for row in rows:
        cells = [str(row.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def extract_syllabus_progress(syllabus_text: str) -> dict:
    """
    Parse a syllabus file and extract progress info.

    Returns dict with:
        - total_tasks: int
        - completed_tasks: int
        - current_week: str (title of first incomplete week)
        - current_topics: list[str] (unchecked items in current week)
    """
    total = 0
    completed = 0
    current_week = None
    current_topics = []
    found_current = False

    week_pattern = re.compile(r"^###\s+(Week\s+\d+.*)", re.IGNORECASE)
    task_pattern = re.compile(r"^- \[([ xX])\]\s+(.*)")

    current_week_title = None

    for line in syllabus_text.splitlines():
        week_match = week_pattern.match(line.strip())
        if week_match:
            current_week_title = week_match.group(1)

        task_match = task_pattern.match(line.strip())
        if task_match:
            total += 1
            is_done = task_match.group(1).lower() == "x"
            if is_done:
                completed += 1
            elif not found_current:
                found_current = True
                current_week = current_week_title
                current_topics.append(task_match.group(2))
            elif current_week_title == current_week:
                current_topics.append(task_match.group(2))

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "progress_pct": round(completed / total * 100, 1) if total > 0 else 0,
        "current_week": current_week or "Not started",
        "current_topics": current_topics[:5],  # Limit to 5 for context window
    }
