<div align="center">

# 🎓 Project Academy

**A fully local, autonomous AI agent that plans your engineering career — one sprint at a time.**

It reads your daily progress, identifies weak areas, schedules what to learn next, and generates tailored assignments — all powered by a locally-run LLM with zero cloud dependencies or API costs.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-000000?logo=ollama&logoColor=white)](https://ollama.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 💡 What Is This?

Most study planners are static checklists. This one **thinks**.

Project Academy is a **headless AI agent** that runs entirely on your machine. You tell it what you did today by writing a short journal entry, and it:

1. **Parses** your structured journal (YAML frontmatter + freeform notes)
2. **Cross-references** five 52-week curricula to find where you stand
3. **Checks** your spaced repetition queue for overdue concepts
4. **Detects** which subject areas you've been neglecting this week
5. **Calls** a local LLM to generate tomorrow's personalized assignment
6. **Archives** your journal entry (data is never deleted — only archived)

All of this happens in a single command:

```bash
python orchestrator.py
```

No cloud. No subscription. No internet required after setup.

---

## ⚙️ How It Works

The orchestrator is a **finite state machine** that transitions through 8 deterministic states on every run:

```
                    ┌──────────────────────────────────────────────────┐
                    │              ORCHESTRATOR FSM                    │
                    │                                                  │
  orchestrator.py ──┤  IDLE                                           │
       (CLI)        │   │                                             │
                    │   ▼                                             │
                    │  READ_JOURNAL ── parse YAML frontmatter         │
                    │   │                                             │
                    │   ▼                                             │
                    │  PROCESS_INTEL ── analyze JDs via LLM           │
                    │   │                                             │
                    │   ▼                                             │
                    │  ASSESS_POSITION ── cross-ref syllabi & hours   │
                    │   │                                             │
                    │   ▼                                             │
                    │  CHECK_SR ── SM-2 spaced repetition queue       │
                    │   │                                             │
                    │   ▼                                             │
                    │  GENERATE_SPRINT ── prompt LLM → assignment     │
                    │   │                                             │
                    │   ▼                                             │
                    │  WRITE_OUTPUT ── write active_sprint.md         │
                    │   │                                             │
                    │   ▼                                             │
                    │  ARCHIVE ── archive journal → reset → IDLE      │
                    │                                                  │
                    └──────────────────────────────────────────────────┘
```

**State is just files.** There is no database — the entire system runs on markdown files with YAML frontmatter. This makes every piece of state human-readable, git-trackable, and trivially debuggable.

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Why |
|---|---|
| Python 3.11+ | Orchestrator runtime |
| [Ollama](https://ollama.ai) | Local LLM inference |
| ~9 GB disk | Model weights (`qwen2.5-coder:14b`) |
| GPU with 6 GB+ VRAM | Recommended for usable speed (CPU works but slow) |

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/Hussny-06/AI-Academy.git
cd AI-Academy

# 2. Install dependencies (just 2 packages)
pip install -r requirements.txt

# 3. Pull the model (~9 GB download)
ollama pull qwen2.5-coder:14b

# 4. Verify everything works
python orchestrator.py --status
```

You should see:

```
============================================================
  PROJECT ACADEMY — System Status
============================================================

  Ollama: ✅ Running
  Model:  ✅ Available
  SR Queue: 0 total, 0 due today

  Faculty              Progress     Current Week
  --------------------------------------------------------
  C++ / Systems          0.0%      Week 1 — C++ Build Systems
  DSA                    0.0%      Week 1 — Complexity Analysis
  ...
```

---

## 📋 Daily Workflow

The system is designed around a **journal → sprint → journal** loop:

### 1. Do your assignment
Open `state/active_sprint.md` and work through today's tasks.

### 2. Write your journal
Fill in `state/user_journal.md` after your study session:

```yaml
---
date: 2026-05-07
faculty: cpp
task_id: CPP-W01-D1
status: completed        # completed | blocked | partial
difficulty_rating: 3     # 1-5 scale
sr_grades:
  - concept: "RAII pattern"
    grade: 4             # 0-5 (SM-2 scale)
blocker: null
hours_spent: 2.5
---

## What I Built
Implemented a custom UniquePtr with move semantics and deleter support.

## Where I Struggled
Reference collapsing rules are still confusing — need to revisit.
```

### 3. Generate next sprint

```bash
python orchestrator.py
```

The orchestrator reads your journal, checks your position across all 5 syllabi, reviews the SR queue, calls the LLM, and writes your next assignment.

---

## 🧰 Commands

| Command | What It Does |
|---|---|
| `python orchestrator.py` | Generate daily sprint (reads journal, calls LLM) |
| `python orchestrator.py --mode=review` | Weekly performance review with velocity metrics |
| `python orchestrator.py --status` | System dashboard — no LLM call |
| `python orchestrator.py --add-sr "concept" --faculty cpp` | Manually add a concept to spaced repetition |
| `python orchestrator.py -v` | Verbose debug logging |

---

## 🏗️ Features

### 📚 5-Faculty Curriculum System

Five handcrafted 52-week syllabi, each broken into 4 phases with weekly granularity:

| Faculty | Weight | Weekly Hours | Focus |
|---|---|---|---|
| **C++ / Systems** | 35% | ~17h | Memory models → lock-free DS → kernel bypass → order book engine |
| **DSA** | 25% | ~12h | Arrays → segment trees → 400+ LeetCode, CF 1600+ target |
| **Edge AI / ML** | 15% | ~7h | PyTorch → ONNX → TensorRT → C++ inference server |
| **Data & Scale** | 12% | ~6h | SQL → Docker → Redis → system design → distributed KV store |
| **Interview Prep** | 13% | ~6h | Resume → STAR behavioral → mock rounds → negotiation |

Each syllabus has **checkboxes per topic** — the orchestrator parses these to know exactly where you are.

### 🧠 SM-2 Spaced Repetition

Every concept you learn gets tracked with the [SuperMemo 2](https://en.wikipedia.org/wiki/SuperMemo#Description_of_SM-2_algorithm) algorithm:

- Grade yourself **0–5** in your journal
- Grade < 3 → interval resets to 1 day (you need to re-learn it)
- Grade ≥ 3 → interval grows: 1d → 6d → `n * EF` (spaced out over weeks)
- Due items are automatically embedded into your next sprint

### 📊 Faculty Weight Enforcement

The orchestrator tracks hours per faculty each week. If you're spending too much time on DSA and neglecting C++, it **forces** a C++ sprint to rebalance.

### 🔍 Intel Drop System

Paste a raw job description into `state/intel_drop.md`. On the next run, the LLM:
- Identifies skill gaps vs your competency matrix
- Suggests priority shifts and syllabus additions
- Rates urgency (low → critical)
- Archives the intel after processing

### 📈 Weekly Reports

Run `--mode=review` for an automated report:
- Task completion velocity (assigned / completed / blocked)
- Faculty hour distribution vs targets (with ✅/⚠️/🔴 indicators)
- Failure analysis (what you got stuck on and why)
- AI-generated performance grade (A/B/C/D/F) with recommendations

### ⏰ Scheduled Execution

Optional Task Scheduler setup (Windows):

```powershell
# Run as Administrator
.\setup_scheduler.ps1
```

Creates two tasks:
- **Academy_Morning** (7:00 AM) — generates your daily sprint
- **Academy_Evening** (10:00 PM) — runs the weekly review

---

## 📁 Project Structure

```
AI Academy/
├── orchestrator.py              # CLI entry point (4 modes)
├── config.yaml                  # System configuration
├── requirements.txt             # pyyaml, requests
│
├── academy/                     # Core engine
│   ├── fsm.py                   # Finite state machine (8 states)
│   ├── sm2.py                   # SM-2 spaced repetition engine
│   ├── ollama.py                # Ollama HTTP client
│   ├── report.py                # Weekly report generator
│   └── utils.py                 # YAML, markdown, file I/O
│
├── prompts/                     # LLM prompt templates
│   ├── system_prompt.md         # Academy persona & output format
│   ├── sprint_gen.md            # Daily sprint generation
│   ├── intel_analysis.md        # JD gap analysis
│   └── weekly_review.md         # Performance review
│
├── syllabus/                    # 52-week curricula
│   ├── syllabus_cpp.md          # C++ / Systems (288 lines)
│   ├── syllabus_dsa.md          # DSA (316 lines)
│   ├── syllabus_ai.md           # Edge AI / ML (207 lines)
│   ├── syllabus_scale.md        # Data & Scale (207 lines)
│   └── syllabus_interview.md    # Interview Prep (190 lines)
│
├── state/                       # Runtime state (⚠️ gitignored)
│   ├── user_journal.md          # Today's journal entry
│   ├── active_sprint.md         # Current assignment
│   ├── spaced_repetition.md     # SM-2 queue
│   ├── competency_matrix.md     # Skill levels per topic
│   ├── intel_drop.md            # Raw JD input
│   └── ...
│
├── archive/                     # Historical data (⚠️ gitignored)
├── logs/                        # Execution logs (⚠️ gitignored)
│
├── test_e2e.py                  # Integration test suite
└── setup_scheduler.ps1          # Windows Task Scheduler setup
```

> **Why is `state/` gitignored?** It contains personal data — journal entries, skill assessments, and job descriptions you're analyzing. The code is public; the data stays local.

---

## ⚡ Tech Stack

| Layer | Choice | Why |
|---|---|---|
| **Runtime** | Python 3.11 | Simple, ubiquitous, fast enough for orchestration |
| **LLM** | Ollama + `qwen2.5-coder:14b` | Free, local, code-specialized, fits in 6 GB VRAM |
| **State** | Markdown + YAML frontmatter | Human-readable, git-friendly, zero setup |
| **Dependencies** | `pyyaml` + `requests` | Intentionally minimal — 2 packages total |
| **Scheduling** | Windows Task Scheduler | Native, reliable, no extra dependencies |

**Design philosophy:** No database. No Docker. No framework. Just Python reading and writing markdown files, with one HTTP call to a local LLM. The entire system is understandable in an afternoon.

---

## 🖥️ Hardware

Designed for edge computation on consumer hardware:

| Spec | Minimum | Recommended |
|---|---|---|
| GPU VRAM | 4 GB (CPU fallback) | 6 GB+ |
| System RAM | 8 GB | 16 GB |
| Disk | 10 GB free | 15 GB free |
| Speed | ~3 tok/s (CPU) | ~10-15 tok/s (GPU) |

Tested on RTX 3050 6GB — model uses ~5.5 GB VRAM, remainder spills to system RAM.

---

## 🔧 Configuration

All settings in [`config.yaml`](config.yaml):

```yaml
# LLM
ollama_url: "http://localhost:11434"
model: "qwen2.5-coder:14b"
temperature: 0.3

# Schedule
daily_hour_cap: 8
rest_day: "sunday"
intel_reminder_day: "friday"

# Faculty weights (must sum to 1.0)
faculties:
  cpp:   { weight: 0.35 }
  dsa:   { weight: 0.25 }
  ai:    { weight: 0.15 }
  scale: { weight: 0.12 }
  interview: { weight: 0.13 }
```

---

## 🧪 Testing

```bash
# Dry run — tests parsing, SM-2, and structure (no LLM needed)
python test_e2e.py --dry

# Full E2E — tests everything including LLM generation
python test_e2e.py
```

---

## 📄 License

MIT — See [LICENSE](LICENSE) for details.
