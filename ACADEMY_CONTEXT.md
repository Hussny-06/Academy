# ACADEMY_CONTEXT.md — Antigravity Context File

> **Purpose:** Attach this file when starting a new Antigravity conversation about Project Academy. It gives full context so I can pick up exactly where we left off without hallucinating or asking redundant questions.
>
> **Last updated:** 2026-07-01

---

## 1. What Is This Project?

**Project Academy** is a self-study orchestration engine that generates daily coding assignments for a 6th-semester Computer Engineering student (Hussain) preparing for placement at HFT firms and top tech companies. Graduation deadline: June 2027.

**How it works:**
1. Student writes a journal entry about yesterday's progress
2. `python orchestrator.py` runs an FSM that reads the journal, checks syllabus position, calls a local LLM (Ollama), and generates today's assignment
3. Student reads the sprint, studies resources, writes code in `work/` directory
4. Weekly deep review happens with Antigravity (me), not the local LLM

**The split:** 7B local model handles daily sprint generation (structured, template-following). Antigravity handles weekly reviews, code review, strategy, and anything requiring real reasoning.

---

## 2. Hardware & Environment

| Component | Detail |
|---|---|
| **OS** | Windows 11 |
| **GPU** | NVIDIA RTX 3050 Laptop, **6 GB VRAM** |
| **RAM** | 16 GB DDR4 |
| **LLM** | `qwen2.5-coder:7b` via Ollama (4.7 GB, fits in VRAM) |
| **Python** | 3.11.9 |
| **Project Path** | `D:\Dev\Projects\AI Academy` |
| **Workspace** | `d:\Dev\Projects\Biomechanics_MiniProject_SemVI` (for running commands) |

> **Why 7B not 14B:** The 14B model (9 GB) requires ~10 GB total memory. With 16 GB RAM at ~50% usage, there's not enough headroom for CPU memory spill. The 7B fits entirely in 6 GB VRAM — no spill, no crashes, 4x faster (12-14 tok/s vs 2.7 tok/s).

---

## 3. Project Architecture

```
AI Academy/
├── orchestrator.py          # CLI entry point (--status, --check, --warmup, --add-sr, -v)
├── config.yaml              # Model, faculties, weights, paths, target companies
├── test_e2e.py              # End-to-end integration test
├── requirements.txt         # pyyaml, httpx
│
├── academy/                 # Core engine
│   ├── fsm.py               # Finite State Machine (the brain)
│   ├── ollama.py            # Ollama HTTP client (generate, warmup, CUDA check)
│   ├── sm2.py               # Spaced repetition engine (SM-2 algorithm)
│   ├── utils.py             # File I/O, markdown parsing, syllabus progress
│   └── report.py            # Weekly report generation
│
├── prompts/                 # LLM prompt templates
│   ├── system_prompt.md     # Academy persona + output format
│   ├── sprint_gen.md        # Sprint generation context injection
│   └── intel_analysis.md    # Job posting analysis prompt
│
├── syllabus/                # 52-week curricula (one per faculty)
│   ├── syllabus_cpp.md      # C++ / Systems (35% weight)
│   ├── syllabus_dsa.md      # DSA (25% weight)
│   ├── syllabus_ai.md       # Edge AI / ML (15% weight)
│   ├── syllabus_scale.md    # Data & Scale (12% weight)
│   └── syllabus_interview.md # Interview Prep (13% weight)
│
├── state/                   # Live state files (read/written each cycle)
│   ├── active_sprint.md     # Today's assignment
│   ├── user_journal.md      # Student's daily log (archived after each run)
│   ├── intel_drop.md        # Job postings pasted on Fridays
│   ├── intel_analysis.md    # LLM analysis of job postings
│   ├── competency_matrix.md # Skill tracking (🔴→🟡→🟢)
│   ├── spaced_repetition.md # SM-2 review queue
│   ├── project_tracker.md   # Portfolio project progress
│   └── weekly_report.md     # Weekly metrics
│
├── work/                    # Student's assignment code
│   ├── cpp/                 # C++ assignments (w01_cmake/, w02_memory/, etc.)
│   ├── dsa/                 # DSA solutions
│   ├── ai/                  # ML work
│   ├── scale/               # System design work
│   └── interview/           # Interview prep materials
│
├── archive/                 # Historical data
│   ├── journal/             # Daily journal entries (YYYY-MM-DD.md)
│   ├── sprints/             # Past sprints
│   └── intel/               # Past job posting analyses
│
└── ME.md                    # Student's personal scratchbook (gitignored)
```

---

## 4. FSM States (the Core Loop)

```
IDLE → READ_JOURNAL → PROCESS_INTEL → ASSESS_POSITION → CHECK_SR → GENERATE_SPRINT → WRITE_OUTPUT → ARCHIVE → IDLE
```

- **IDLE:** Checks if Ollama is running, rest day, CUDA conflicts
- **READ_JOURNAL:** Parses `state/user_journal.md` frontmatter (faculty, status, hours, blocker)
- **PROCESS_INTEL:** If `intel_drop.md` has content, sends to LLM for analysis
- **ASSESS_POSITION:** Reads all 5 syllabi, computes progress %, identifies underweight faculties
- **CHECK_SR:** Queries SM-2 engine for due items
- **GENERATE_SPRINT:** Calls Ollama with context → gets assignment
- **WRITE_OUTPUT:** Strips hallucinated resources, injects verified resources from syllabus, adds work directory note, writes `active_sprint.md`
- **ARCHIVE:** Archives journal to `archive/journal/YYYY-MM-DD.md`, resets journal

---

## 5. Key Design Decisions (and WHY)

| Decision | Why |
|---|---|
| **7B model, not 14B** | 14B requires ~10 GB, exceeds 6 GB VRAM + available RAM. 7B fits entirely in VRAM. |
| **Resources injected by code, not LLM** | The 7B model hallucinated fake URLs (2/3 links were dead). FSM now strips LLM resource sections and injects verified links from syllabus. |
| **Sprint includes "What You Need to Know"** | Student encountered topics they'd never seen (e.g., CMake). Original prompt assumed prior knowledge. |
| **Sprint includes "Where to Write Code"** | Student didn't know where to put assignment code. FSM now appends `work/{faculty}/{week}_{topic}/` guidance. |
| **Weekly reviews done by Antigravity, not 7B** | 7B can follow templates but can't reason about code quality, learning patterns, or strategy. |
| **Sunday rest day** | Configured in config.yaml. No sprint generated on Sundays. |
| **300s timeout** | Cold-loading the model can take 30-60s on first run. 300s gives ample headroom. |
| **CUDA conflict detection** | If student has `ollama run` open interactively, it hogs VRAM. FSM warns before attempting generation. |
| **Sprint quality gate** | FSM validates LLM output has headers, lists, code blocks. Auto-retries once if output is empty/refusal. |

---

## 6. CLI Commands

| Command | LLM Call? | Purpose |
|---|---|---|
| `python orchestrator.py` | ✅ Yes | Generate daily sprint |
| `python orchestrator.py --status` | ❌ No | System health dashboard |
| `python orchestrator.py --check` | ❌ No | Validate student's code against sprint |
| `python orchestrator.py --warmup` | ✅ Minimal | Pre-load model into VRAM |
| `python orchestrator.py --add-sr "X" --faculty Y` | ❌ No | Add concept to spaced repetition |
| `python orchestrator.py -v` | ✅ Yes | Verbose debug mode |
| `python orchestrator.py --mode=review` | ✅ Yes | Auto metrics (rarely used — Antigravity does reviews) |

---

## 7. Faculties & Target Companies

**5 Faculties:**
- **C++ / Systems** (35%) — Build systems, memory, RAII, move semantics, threading, lock-free, kernel bypass
- **DSA** (25%) — 400+ LeetCode problems, segment trees, DP, graphs, competitive programming
- **Edge AI / ML** (15%) — PyTorch → ONNX → TensorRT → CUDA → C++ inference server
- **Data & Scale** (12%) — SQL, Docker, Redis, system design, Raft KV store project
- **Interview Prep** (13%) — Resume, behavioral, mocks, company research, negotiation

**Target Companies (Tier 1):** Tower Research, iRage, IMC, Graviton, WorldQuant
**Target Companies (Tier 2):** Morgan Stanley, Goldman Sachs, Bloomberg
**Target Companies (Tier 3):** Google, NVIDIA

---

## 8. Known Issues & Workarounds

| Issue | Workaround |
|---|---|
| Ollama not running | Run `ollama serve` in a terminal before using orchestrator |
| CUDA conflict (another ollama session) | Close any `ollama run` sessions (type `/bye`) |
| LLM hallucinated URLs in sprint | Fixed: FSM strips LLM resources, injects verified ones from syllabus |
| CMake tutorial link too broad | Fixed: Changed to specific Step 1 page |
| `--mode=review` is low quality | Don't use it. Do weekly reviews with Antigravity instead. |
| Windows terminal encoding | Fixed: orchestrator.py wraps stdout/stderr with utf-8 |

---

## 9. What Antigravity (I) Do for This Project

1. **Weekly reviews** — Read journals, review code, analyze progress, adjust strategy
2. **Code review** — Deep feedback on assignment code in `work/` directory
3. **System improvements** — Add features to the orchestrator, fix prompts, update syllabi
4. **Resource curation** — Find and verify YouTube/doc links for syllabus weeks
5. **Curriculum analysis** — Identify gaps, adjust faculty weights, reorder topics
6. **Debugging** — Fix orchestrator issues, Ollama connectivity, FSM bugs

---

## 10. How to Use This File

**Starting a new chat:**
> "I'm working on Project Academy. Here's the context file: [attach ACADEMY_CONTEXT.md]. I need help with [specific request]."

**Updating this file:** After significant changes (new features, architecture shifts, resolved issues), ask Antigravity to update this file.

**What NOT to put here:** Daily progress, journal entries, specific sprint content — those belong in `archive/` and `state/`. This file is about the *system*, not the *content*.
