# 🎓 Project Academy

A fully local AI-powered study planner that acts as your personal mentor. It reads your daily progress, identifies weak areas, schedules what to learn next, and generates tailored assignments — all using a locally-run LLM (Ollama) with zero cloud or API costs.

Built for engineering students preparing for top-tier tech placements.

---

## Architecture

```
orchestrator.py (CLI)
       │
       ▼
  AcademyFSM (academy/fsm.py)
       │
       ├── READ_JOURNAL ──► Parse YAML frontmatter from user_journal.md
       ├── PROCESS_INTEL ──► Analyze pasted JDs via LLM
       ├── ASSESS_POSITION ──► Cross-reference syllabi & weekly hours
       ├── CHECK_SR ──► SM-2 spaced repetition due items
       ├── GENERATE_SPRINT ──► Build prompt → call Ollama → get assignment
       ├── WRITE_OUTPUT ──► Write active_sprint.md
       └── ARCHIVE ──► Archive journal (never delete) → IDLE
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Orchestrator | Python 3.11+ (native `os`, `re`, `pathlib`) |
| Inference | [Ollama](https://ollama.ai) (local, WSL) |
| Model | `qwen2.5-coder:14b` (4-bit quantized) |
| State | Markdown files with YAML frontmatter |
| Dependencies | `pyyaml`, `requests` (2 packages total) |

## Quick Start

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.ai) installed and running
- ~9GB disk space for the model

### Setup
```bash
# Clone
git clone https://github.com/YOUR_USERNAME/AI-Academy.git
cd AI-Academy

# Install dependencies
pip install -r requirements.txt

# Pull the model
ollama pull qwen2.5-coder:14b

# Check system status
python orchestrator.py --status
```

### Daily Workflow

**1. Complete your assignment** from `state/active_sprint.md`

**2. Write your journal** in `state/user_journal.md`:
```yaml
---
date: 2026-05-07
faculty: cpp
task_id: CPP-W01-D1
status: completed    # completed | blocked | partial
difficulty_rating: 3
sr_grades:
  - concept: "RAII pattern"
    grade: 4          # 0-5 (SM-2 scale)
blocker: null
hours_spent: 2.5
---

## What I Built
Implemented a custom UniquePtr with move semantics.

## Where I Struggled
Reference collapsing rules are still confusing.
```

**3. Generate your next sprint:**
```bash
python orchestrator.py
```

The orchestrator reads your journal, checks your syllabus position, reviews spaced repetition items, calls the LLM, and writes your next assignment to `state/active_sprint.md`.

### Commands

```bash
python orchestrator.py                  # Generate daily sprint
python orchestrator.py --mode=review    # Weekly performance review
python orchestrator.py --status         # System dashboard (no LLM)
python orchestrator.py --add-sr "concept" --faculty cpp  # Add SR item
python orchestrator.py -v               # Verbose logging
```

## Features

### 📚 5-Faculty Curriculum System
52-week syllabi with week-by-week breakdown:
- **C++ / Systems** (35%) — Memory models, concurrency, lock-free DS, networking
- **DSA** (25%) — Arrays to segment trees, 400+ LeetCode target
- **Edge AI / ML** (15%) — PyTorch, ONNX, TensorRT, C++ inference
- **Data & Scale** (12%) — SQL, Docker, Redis, system design
- **Interview Prep** (13%) — Resume, behavioral, mocks, negotiation

### 🧠 SM-2 Spaced Repetition
Concepts you learn are tracked using the SuperMemo 2 algorithm. Grade yourself 0-5 in your journal, and the system schedules reviews at optimal intervals.

### 📊 Faculty Weight Enforcement
The orchestrator tracks hours per faculty each week. If you're under-spending on C++ and over-spending on DSA, it forces a C++ sprint.

### 🔍 Intel Drop System
Paste job descriptions into `state/intel_drop.md`. The LLM analyzes skill gaps against your competency matrix and proposes syllabus changes.

### 📈 Weekly Reports
Automated velocity tracking, faculty distribution analysis, and failure pattern detection.

### ⏰ Scheduled Execution
Runs via Windows Task Scheduler — morning sprint (7 AM) and evening review (10 PM).

## Project Structure

```
AI Academy/
├── orchestrator.py          # CLI entry point
├── config.yaml              # All system configuration
├── academy/
│   ├── fsm.py               # Finite state machine (8 states)
│   ├── sm2.py               # SM-2 spaced repetition engine
│   ├── ollama.py            # Ollama HTTP client
│   ├── report.py            # Weekly report generator
│   └── utils.py             # File I/O, YAML, markdown parsing
├── prompts/                 # LLM prompt templates
├── syllabus/                # 52-week curricula (5 files)
├── state/                   # Runtime state (gitignored)
├── archive/                 # Journal history (gitignored)
└── logs/                    # Execution logs (gitignored)
```

## Configuration

All settings live in `config.yaml`:
- Ollama endpoint and model selection
- Faculty weights and daily hour cap
- SM-2 parameters (EF floor, initial intervals)
- Rest day and intel reminder schedule
- Target company career page URLs

## Hardware Requirements

Designed for edge computation:
- **GPU:** RTX 3050 (6GB VRAM) or equivalent
- **RAM:** 16GB system RAM
- **Trade-off:** ~5.5GB model on GPU, ~3.5GB spills to RAM. Expect 10-15 tok/s.

## License

MIT — See [LICENSE](LICENSE) for details.
