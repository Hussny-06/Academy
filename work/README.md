# Work Directory

This is where you write code for Academy assignments.

## Structure

```
work/
├── cpp/           ← C++ / Systems assignments
│   ├── w01_cmake/
│   ├── w02_memory/
│   └── ...
├── dsa/           ← DSA problem solutions
│   ├── w01_arrays/
│   └── ...
├── ai/            ← Edge AI / ML work
├── scale/         ← Data & Scale projects
└── interview/     ← Interview prep materials
```

## Naming Convention

Use `w{NN}_{topic}/` format:
- `w01_cmake/` — Week 1, CMake assignment
- `w03_raii/` — Week 3, RAII assignment
- `w14_graphs/` — Week 14, Graph problems

## How It Works

1. **Read** your sprint in `state/active_sprint.md`
2. **Create** a folder in the matching faculty directory (e.g., `work/cpp/w01_cmake/`)
3. **Write** your code there
4. **Run** `python orchestrator.py --check` to validate your work
5. **Journal** your progress in `state/user_journal.md`
