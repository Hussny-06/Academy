"""
End-to-End Integration Test for Project Academy.

Tests the full pipeline with a mock journal entry.
Requires Ollama to be running with the configured model.

Usage:
    python test_e2e.py          # Run full E2E test
    python test_e2e.py --dry    # Dry run (skip LLM call, test parsing only)
"""

import sys
import io
import os
from pathlib import Path

# Fix Windows terminal encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from academy.utils import (
    load_config,
    resolve_path,
    read_file,
    write_file,
    parse_frontmatter,
    parse_markdown_table,
    extract_syllabus_progress,
    today_str,
    is_file_empty_or_placeholder,
)
from academy.sm2 import SpacedRepetitionEngine
from academy.ollama import OllamaClient
from academy.report import generate_weekly_report
from academy.fsm import AcademyFSM


def test_utils():
    """Test utility functions."""
    print("\n--- Testing Utils ---")

    # Test frontmatter parsing
    sample = """---
date: 2026-05-07
faculty: cpp
status: completed
hours_spent: 3.5
sr_grades:
  - concept: "RAII pattern"
    grade: 4
---

## What I Built
Implemented a custom UniquePtr with move semantics.

## Where I Struggled
Reference collapsing rules are still confusing.
"""
    fm, body = parse_frontmatter(sample)
    assert str(fm["date"]) == "2026-05-07", f"Date mismatch: {fm['date']}"
    assert fm["faculty"] == "cpp", f"Faculty mismatch: {fm['faculty']}"
    assert fm["hours_spent"] == 3.5, f"Hours mismatch: {fm['hours_spent']}"
    assert len(fm["sr_grades"]) == 1, f"SR grades count: {len(fm['sr_grades'])}"
    assert "UniquePtr" in body, f"Body content missing"
    print("  [PASS] Frontmatter parsing")

    # Test markdown table parsing
    table = """| Concept | Faculty | EF |
|---|---|---|
| RAII | cpp | 2.50 |
| Move semantics | cpp | 2.30 |
"""
    rows = parse_markdown_table(table)
    assert len(rows) == 2, f"Row count: {len(rows)}"
    assert rows[0]["Concept"] == "RAII", f"First concept: {rows[0]['Concept']}"
    print("  [PASS] Markdown table parsing")

    # Test syllabus progress
    config = load_config()
    cpp_path = resolve_path(config["faculties"]["cpp"]["syllabus"])
    cpp_text = read_file(cpp_path)
    prog = extract_syllabus_progress(cpp_text)
    assert prog["total_tasks"] > 0, f"No tasks found in C++ syllabus"
    assert prog["current_week"] is not None, "Current week not detected"
    print(f"  [PASS] Syllabus progress: {prog['total_tasks']} tasks, "
          f"current: {prog['current_week']}")

    print("  All utils tests passed!")


def test_sm2():
    """Test SM-2 spaced repetition engine."""
    print("\n--- Testing SM-2 Engine ---")

    config = load_config()
    state_dir = resolve_path(config["paths"]["state_dir"])
    sr_path = state_dir / "spaced_repetition.md"

    engine = SpacedRepetitionEngine(sr_path, config)

    # Test adding items
    engine.add_item("test_concept_e2e", "dsa")
    assert any(i.concept == "test_concept_e2e" for i in engine.items), "Item not added"
    print("  [PASS] Add item")

    # Test duplicate detection
    count_before = len(engine.items)
    engine.add_item("test_concept_e2e", "dsa")
    assert len(engine.items) == count_before, "Duplicate not detected"
    print("  [PASS] Duplicate detection")

    # Test grade processing
    engine.review_item("test_concept_e2e", 4)
    item = next(i for i in engine.items if i.concept == "test_concept_e2e")
    assert item.interval == 6, f"Interval after grade 4: {item.interval} (expected 6)"
    print(f"  [PASS] Grade processing (interval={item.interval}, EF={item.ef:.2f})")

    # Test failed review
    engine.review_item("test_concept_e2e", 1)
    item = next(i for i in engine.items if i.concept == "test_concept_e2e")
    assert item.interval == 1, f"Interval after grade 1: {item.interval} (expected 1)"
    print(f"  [PASS] Failed review reset (interval={item.interval})")

    # Test due items
    due = engine.get_due_items()
    print(f"  [PASS] Due items check: {len(due)} items due")

    # Clean up test item
    engine.items = [i for i in engine.items if i.concept != "test_concept_e2e"]
    engine._save()
    print("  [PASS] Cleanup")

    print("  All SM-2 tests passed!")


def test_ollama():
    """Test Ollama connectivity."""
    print("\n--- Testing Ollama ---")

    config = load_config()
    client = OllamaClient(config)

    health = client.health_check()
    print(f"  Ollama health: {'PASS' if health else 'FAIL (not running)'}")

    if health:
        model_ok = client.is_model_available()
        print(f"  Model available: {'PASS' if model_ok else 'FAIL (not pulled)'}")
        return health and model_ok

    return False


def test_full_cycle(dry_run: bool = False):
    """Test a full sprint generation cycle."""
    print("\n--- Testing Full Sprint Cycle ---")

    config = load_config()
    state_dir = resolve_path(config["paths"]["state_dir"])
    journal_path = state_dir / "user_journal.md"

    # Write a test journal entry
    test_journal = f"""---
date: {today_str()}
faculty: cpp
task_id: CPP-W01-D1
status: completed
difficulty_rating: 3
sr_grades:
  - concept: "RAII pattern"
    grade: 4
blocker: null
hours_spent: 2.5
sleep_hours: 7
workout: true
---

## What I Built
Set up CMake project with Google Benchmark and Google Test targets.
Created a basic build system with Debug and Release configurations.

## Where I Struggled
Had some trouble understanding the difference between -O2 and -O3 flags
and when each is appropriate.
"""
    write_file(journal_path, test_journal)
    print("  [PASS] Test journal written")

    if dry_run:
        # Just test parsing, don't call LLM
        from academy.utils import parse_frontmatter
        fm, body = parse_frontmatter(test_journal)
        print(f"  [DRY] Parsed journal: faculty={fm['faculty']}, "
              f"status={fm['status']}, hours={fm['hours_spent']}")
        print(f"  [DRY] Body length: {len(body)} chars")
        print("  [DRY] Skipping LLM call. Use without --dry for full test.")

        # Reset journal
        reset_journal(journal_path)
        return True

    # Run full FSM cycle
    fsm = AcademyFSM(mode="sprint")
    success = fsm.run()

    if success:
        sprint_content = read_file(state_dir / "active_sprint.md")
        print(f"  [PASS] Sprint generated: {len(sprint_content)} chars")
        print(f"  Sprint preview (first 200 chars):")
        print(f"  {sprint_content[:200]}...")
    else:
        print("  [FAIL] Sprint generation failed")

    return success


def reset_journal(journal_path: Path):
    """Reset journal to empty template."""
    template = """---
date:
faculty:
task_id:
status:
difficulty_rating:
sr_grades: []
blocker: null
hours_spent:
sleep_hours:
workout:
---

## What I Built


## Where I Struggled

"""
    write_file(journal_path, template)


def main():
    dry_run = "--dry" in sys.argv

    print("=" * 50)
    print("  PROJECT ACADEMY — E2E Test Suite")
    print("=" * 50)

    # Unit tests (always run)
    test_utils()
    test_sm2()

    # Ollama connectivity
    ollama_ok = test_ollama()

    # Full cycle
    if dry_run:
        test_full_cycle(dry_run=True)
        print("\n✅ Dry run complete. All parsing tests passed.")
    elif ollama_ok:
        success = test_full_cycle(dry_run=False)
        if success:
            print("\n✅ Full E2E test passed! The Academy is operational.")
        else:
            print("\n❌ Full E2E test failed.")
            sys.exit(1)
    else:
        print("\n⚠️  Ollama not available. Run with --dry for parsing tests only.")
        print("    To fix: ensure Ollama is running and model is pulled.")
        sys.exit(1)


if __name__ == "__main__":
    main()
