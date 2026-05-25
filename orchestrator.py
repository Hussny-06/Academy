#!/usr/bin/env python3
"""
Project Academy — Autonomous AI Training Agent
===============================================

CLI entry point for the Academy orchestrator.

Usage:
    python orchestrator.py                  # Morning sprint generation
    python orchestrator.py --mode=review    # Evening/weekly review
    python orchestrator.py --status         # Show current state (no LLM call)
    python orchestrator.py --warmup         # Pre-load model into VRAM
    python orchestrator.py --add-sr "concept" --faculty cpp  # Manually add SR item

Examples:
    # Generate today's sprint (reads journal, calls Ollama, writes sprint):
    python orchestrator.py

    # Pre-load model before first run (avoids cold-start timeout):
    python orchestrator.py --warmup

    # Run weekly review (Sunday evening):
    python orchestrator.py --mode=review

    # Check system status without calling the LLM:
    python orchestrator.py --status

    # Add a concept to spaced repetition manually:
    python orchestrator.py --add-sr "virtual dispatch cost" --faculty cpp
"""

import argparse
import logging
import sys
import io
from pathlib import Path

# Fix Windows terminal encoding for Unicode/emoji output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from academy.fsm import AcademyFSM
from academy.sm2 import SpacedRepetitionEngine
from academy.ollama import OllamaClient
from academy.utils import (
    load_config,
    resolve_path,
    read_file,
    extract_syllabus_progress,
    today_str,
    get_day_of_week,
    get_week_number,
    is_file_empty_or_placeholder,
)


def setup_logging(logs_dir: Path, verbose: bool = False) -> None:
    """Configure logging to both console and file."""
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_level = logging.DEBUG if verbose else logging.INFO

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_fmt)

    # File handler
    file_handler = logging.FileHandler(
        logs_dir / "orchestrator.log", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    # Root logger
    root_logger = logging.getLogger("academy")
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def show_status(config: dict) -> None:
    """Show current system status without calling the LLM."""
    print("\n" + "=" * 60)
    print("  PROJECT ACADEMY — System Status")
    print("=" * 60)
    print(f"\n  Date: {today_str()} ({get_day_of_week().capitalize()})")
    print(f"  Week: {get_week_number()}")
    print(f"  Model: {config['model']}")

    # Ollama status
    client = OllamaClient(config)
    ollama_ok = client.health_check()
    model_ok = client.is_model_available() if ollama_ok else False
    print(f"\n  Ollama: {'✅ Running' if ollama_ok else '❌ Not running'}")
    print(f"  Model:  {'✅ Available' if model_ok else '❌ Not pulled'}")

    # CUDA conflict check
    if ollama_ok:
        cuda_warning = client.check_cuda_conflict()
        if cuda_warning:
            print(f"  GPU:    ⚠️  Conflict detected (close 'ollama run' sessions)")
        else:
            print(f"  GPU:    ✅ Available")

    # Journal status
    state_dir = resolve_path(config["paths"]["state_dir"])
    journal_path = state_dir / "user_journal.md"
    journal_empty = is_file_empty_or_placeholder(journal_path)
    print(f"\n  Journal: {'📝 Has entry' if not journal_empty else '📭 Empty'}")

    # Intel status
    intel_path = state_dir / "intel_drop.md"
    intel_empty = is_file_empty_or_placeholder(intel_path)
    print(f"  Intel Drop: {'📥 Has content' if not intel_empty else '📭 Empty'}")

    # SR status
    sr_engine = SpacedRepetitionEngine(
        state_dir / "spaced_repetition.md", config
    )
    due = sr_engine.get_due_items()
    print(f"  SR Queue: {len(sr_engine.items)} total, {len(due)} due today")

    # Syllabus progress
    print(f"\n  {'Faculty':<20} {'Progress':<12} {'Current Week'}")
    print("  " + "-" * 56)
    for key, fconf in config["faculties"].items():
        syllabus_path = resolve_path(fconf["syllabus"])
        syllabus_text = read_file(syllabus_path)
        if syllabus_text:
            prog = extract_syllabus_progress(syllabus_text)
            print(
                f"  {fconf['name']:<20} "
                f"{prog['progress_pct']:>5.1f}%      "
                f"{prog['current_week'][:30]}"
            )
        else:
            print(f"  {fconf['name']:<20} {'N/A':>5}       No syllabus")

    # Rest day check
    rest_day = config.get("rest_day", "sunday")
    if get_day_of_week() == rest_day:
        print(f"\n  ⚡ Today is your rest day ({rest_day.capitalize()}).")
        print("     No sprint will be generated.")

    # Friday intel reminder
    if get_day_of_week() == config.get("intel_reminder_day", "friday"):
        print("\n  🔍 It's Friday — Intel Session day!")
        print("     Don't forget to paste JDs into state/intel_drop.md")

    print("\n" + "=" * 60 + "\n")


def add_sr_item(config: dict, concept: str, faculty: str) -> None:
    """Manually add a concept to the spaced repetition queue."""
    state_dir = resolve_path(config["paths"]["state_dir"])
    sr_engine = SpacedRepetitionEngine(
        state_dir / "spaced_repetition.md", config
    )
    sr_engine.add_item(concept, faculty)
    print(f"✅ Added to SR queue: '{concept}' ({faculty})")
    print(f"   Next review: {today_str()} (today)")


def main():
    parser = argparse.ArgumentParser(
        description="Project Academy — Autonomous AI Training Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--mode",
        choices=["sprint", "review"],
        default="sprint",
        help="Execution mode: 'sprint' (default) or 'review'",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show system status without calling the LLM",
    )
    parser.add_argument(
        "--add-sr",
        metavar="CONCEPT",
        help="Add a concept to the spaced repetition queue",
    )
    parser.add_argument(
        "--faculty",
        help="Faculty for --add-sr (e.g., cpp, dsa, ai, scale, interview)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config.yaml (default: auto-detect)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose (debug) logging",
    )
    parser.add_argument(
        "--warmup",
        action="store_true",
        help="Pre-load model into VRAM (avoids cold-start delay)",
    )

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    logs_dir = resolve_path(config["paths"]["logs_dir"])

    # Handle status check (no logging setup needed)
    if args.status:
        show_status(config)
        return

    # Handle manual SR addition
    if args.add_sr:
        if not args.faculty:
            print("Error: --faculty is required when using --add-sr")
            print("Valid faculties: cpp, dsa, ai, scale, interview")
            sys.exit(1)
        add_sr_item(config, args.add_sr, args.faculty)
        return

    # Handle model warmup
    if args.warmup:
        print("\n🔥 Warming up model (loading into VRAM)...")
        print("   This may take 2-3 minutes on first load.\n")
        client = OllamaClient(config)
        if not client.health_check():
            print("❌ Ollama is not running. Start it first.")
            sys.exit(1)
        cuda_warning = client.check_cuda_conflict()
        if cuda_warning:
            print(f"   {cuda_warning}\n")
        success = client.warmup()
        if success:
            print("✅ Model is warm and ready. Run 'python orchestrator.py' to generate a sprint.")
        else:
            print("❌ Warmup failed. Check if Ollama is running and the model is pulled.")
            sys.exit(1)
        return

    # Setup logging for main execution
    setup_logging(logs_dir, args.verbose)
    logger = logging.getLogger("academy")

    # Print banner
    print("\n" + "=" * 50)
    print("  🎓 PROJECT ACADEMY")
    print(f"  Mode: {args.mode.upper()}")
    print(f"  Date: {today_str()} ({get_day_of_week().capitalize()})")
    print("=" * 50 + "\n")

    # Run the FSM
    fsm = AcademyFSM(config_path=args.config, mode=args.mode)
    success = fsm.run()

    if success:
        print("\n✅ Academy cycle complete.")
        if args.mode == "sprint":
            sprint_path = resolve_path(config["paths"]["state_dir"]) / "active_sprint.md"
            print(f"📋 Your sprint is ready: {sprint_path}")
        elif args.mode == "review":
            report_path = resolve_path(config["paths"]["state_dir"]) / "weekly_report.md"
            print(f"📊 Weekly review written: {report_path}")
    else:
        print("\n❌ Academy cycle failed. Check logs/error.log for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
