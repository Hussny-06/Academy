# Syllabus: Systems-Grade AI & Autonomous Agent Orchestration
## Faculty Weight: 15% | 7h/week | Target: Architect & Orchestrate Autonomous Multi-Agent Systems

> **Reference Resources:**
> - *Language Models: An Information Retrieval Perspective* / Anthropic Research Papers
> - Model Context Protocol (MCP) Specification (Anthropic)
> - LangGraph & FSM-driven Agent Design Documentation
> - *Quantization & Efficient LLM Serving* — Tim Dettmers / llama.cpp
> - *Deep Learning* — Ian Goodfellow (foundations reference)
>
> **Hardware & Execution Environment:**
> - **Local:** RTX 3050 (6GB VRAM) — low-latency local agent serving using quantized models (`Qwen 2.5 Coder 7B`, `Llama 3.1 8B` via Ollama / llama.cpp / vLLM with 4k–8k context budgeting).
> - **Cloud:** Free Cloud Tiers (Kaggle 2x T4 16GB GPUs, Colab, Hugging Face Spaces) — utilized for bulky multi-agent setups, large parallel swarm evaluation, long-context retrieval, and multi-model consensus testing.
>
> **Weekly Cadence:** 2h theory/papers + 4h hands-on implementation + 1h agent benchmarking & testing

---

## Phase 1: Foundation (Weeks 1–13) — LLM Internals, Local Inference & Tool Execution

### Week 1 — PyTorch & Tensor Computing Foundations
- [ ] Tensor mechanics: striding, memory layout, contiguous vs non-contiguous views
- [ ] Autograd engine: computational graphs, backward pass, gradient accumulation
- [ ] PyTorch module abstractions: `nn.Module`, custom forward passes, parameter management
- [ ] GPU memory management: device allocation, CUDA streams, VRAM tracking with `torch.cuda`
- **Deliverable:** NumPy vs PyTorch benchmark measuring GPU acceleration across matrix operations

### Week 2 — The Transformer Architecture & Attention Mechanics
- [ ] Scaled dot-product attention: mathematical derivation, query-key-value interaction
- [ ] Multi-Head Attention (MHA) vs Multi-Query Attention (MQA) vs Grouped-Query Attention (GQA)
- [ ] Position encodings: Sinusoidal vs Rotary Position Embeddings (RoPE)
- [ ] Transformer Decoder block: layer norm, SwiGLU activation, residual connections
- **Deliverable:** Minimal GPT decoder block implemented from scratch in pure PyTorch

### Week 3 — Inference Dynamics & The KV-Cache
- [ ] Prefill phase vs Auto-regressive decode phase: compute-bound vs memory-bandwidth-bound
- [ ] KV-Cache internals: mechanics, memory footprint calculation, cache eviction strategies
- [ ] Sampling mechanics: greedy decoding, temperature, top-k, top-p (nucleus), repetition penalties
- [ ] Stop sequences and streaming response handling
- **Deliverable:** Minimal text generation loop implementing an explicit KV-cache from scratch

### Weeks 4–5 — Local LLM Serving & Quantization on RTX 3050
- [ ] **Week 4:** Quantization fundamentals: FP16 → INT8 → INT4
  - Weight-only vs weight-and-activation quantization
  - Quantization formats: GGUF, AWQ, EXL2
  - Serving local models via Ollama and `llama.cpp` server
- [ ] **Week 5:** Hardware benchmarking on RTX 3050 (6GB VRAM)
  - VRAM profiling: model weights vs context buffer vs KV-cache allocation
  - GPU layer offloading tuning (`ngl` / gpu-layers)
  - Measuring TTFT (Time to First Token) and generation tokens/second
- **Deliverable:** Benchmark report comparing `Qwen 2.5 Coder 7B` vs `Llama 3.1 8B` on RTX 3050 across varying context lengths

### Week 6 — Cloud Scaling for Heavy Models (Kaggle / Colab)
- [ ] Setting up 16GB–32GB VRAM environments on Kaggle (2x T4 GPUs)
- [ ] Serving unquantized FP16 models and large 14B/32B parameter models via vLLM
- [ ] PagedAttention & continuous batching concepts in vLLM
- [ ] Exposing cloud inference endpoints securely to local orchestrators via ngrok / cloudflared
- **Deliverable:** Script deploying a vLLM server on Kaggle and querying it from your local development environment

### Weeks 7–8 — The ReAct Pattern & Function Calling From Scratch
- [ ] **Week 7:** The ReAct (Reasoning + Acting) loop
  - Thought → Action → Observation → Reflection cycle
  - Implementing the loop in pure Python without external frameworks
  - Parsing agent actions and stop sequences reliably
- [ ] **Week 8:** Deterministic Function Calling
  - JSON Schema generation from Pydantic models
  - Injecting tool signatures into system prompts
  - Execution sandbox: handling tool runtime errors, timeout fallbacks, and retry loops
- **Deliverable:** Zero-framework CLI agent with 3 tools (File System Reader, Shell Executor, Math Evaluator)

### Weeks 9–10 — Structured Outputs & Constrained Decoding
- [ ] **Week 9:** The structured output problem in production agents
  - Why standard JSON prompting fails under edge cases
  - JSON Mode vs schema enforcement
  - Pydantic validation loops with automatic re-prompting on validation errors
- [ ] **Week 10:** Grammar-Constrained Decoding
  - Context-free grammars (CFGs) and GBNF grammars in `llama.cpp`
  - Constrained decoding engines (Outlines, guidance)
  - Enforcing 100% syntactically valid JSON and code blocks without hallucinations
- **Deliverable:** Structured data extraction pipeline guaranteed to adhere 100% to a complex Pydantic schema

### Weeks 11–13 — Prompt Engineering Patterns & Single-Agent Loops
- [ ] **Week 11:** Chain-of-Thought (CoT) and Self-Consistency sampling
- [ ] **Week 12:** Reflexion: Self-critique, error analysis, and iterative refinement
- [ ] **Week 13:** Plan-and-Solve: Decomposing high-level goals into DAGs (Directed Acyclic Graphs) of subtasks
- **Deliverable:** Self-healing Python code generator that writes code, runs pytest, detects failures, and patches bugs autonomously

---

## Phase 2: Deepening (Weeks 14–26) — Cognitive Architectures, Memory & Context Systems

### Weeks 14–16 — Context Window Engineering & Compaction
- [ ] **Week 14:** Context window anatomy & budgeting
  - Allocating token quotas: system instructions, tool definitions, working scratchpad, conversation history
  - Managing the 6GB VRAM context boundary (staying within 4k–8k tokens locally)
- [ ] **Week 15:** Dynamic Context Compaction
  - Sliding window summarization and token truncation strategies
  - Semantic message compaction: pruning redundant tool observation payloads
- [ ] **Week 16:** Prompt Caching & Reuse
  - How prompt caching works at the KV-cache level
  - Structuring prefixes for maximum cache hits
- **Deliverable:** Context manager class that maintains conversation coherence over 50+ tool-calling turns without context overflow

### Weeks 17–19 — Agentic Memory Hierarchy
- [ ] **Week 17:** Memory Taxonomy
  - Short-Term Memory: Active task scratchpad and working variables
  - Episodic Memory: Recording past execution trajectories, mistakes, and outcomes
  - Semantic Memory: Factual knowledge retrieval
- [ ] **Week 18:** Vector Embeddings & Vector Stores
  - Embedding models for code and text (`bge-small`, `nomic-embed-text`)
  - Local vector stores: Chroma, Qdrant
  - Similarity metrics: Cosine, Dot Product, Euclidean distance
- [ ] **Week 19:** Hybrid Retrieval
  - Why pure dense vector search fails for code symbols and exact matches
  - BM25 sparse keyword search + dense vector retrieval
  - Reciprocal Rank Fusion (RRF) and Cross-Encoder rerankers
- **Deliverable:** Local Code Search Agent that indexes a Git repository using hybrid retrieval and answers architectural queries

### Weeks 20–22 — GraphRAG & Complex Knowledge Systems
- [ ] **Week 20:** Knowledge Graphs for Agents
  - Nodes, edges, entities, and relationship extraction from code and documentation
  - Building lightweight graph representations using NetworkX / SQLite
- [ ] **Week 21:** Multi-Hop Reasoning with GraphRAG
  - Combining vector search with graph traversal (e.g., finding all callers of a function across files)
  - Graph-guided sub-agent exploration
- [ ] **Week 22:** Distributed Memory Testing on Cloud
  - Deploying a large vector index and embedding cluster on Kaggle / Colab
  - Stress testing retrieval latency under heavy document volume
- **Deliverable:** Codebase Dependency Navigator agent using GraphRAG to trace cross-file function calls and imports

### Weeks 23–26 — Tool Ecosystems, Sandboxing & Model Context Protocol (MCP)
- [ ] **Week 23:** Security & Sandboxing
  - Security risks of autonomous execution: prompt injection, unauthorized commands
  - Docker containerization for agent tool execution
  - Isolated file system mounts and execution resource limits (CPU/RAM/Timeout)
- [ ] **Week 24:** Anthropic's Model Context Protocol (MCP) Architecture
  - MCP client-server architecture: transports (STDIO, SSE), protocol lifecycle
  - Exposing tools, resources, and prompts via standardized MCP interfaces
- [ ] **Week 25:** Building Custom MCP Servers
  - Implementing an MCP server in Python for local Git operations
  - Implementing an MCP server for SQLite database queries
- [ ] **Week 26:** Agent MCP Integration
  - Connecting your local ReAct agent to multiple MCP servers concurrently
- **Deliverable:** Secure Docker-sandboxed MCP execution server with interactive tool authorization

---

## Phase 3: Specialization (Weeks 27–39) — Multi-Agent Systems & Orchestration Project

### Weeks 27–29 — Multi-Agent Topologies & Communication Patterns
- [ ] **Week 27:** When to use Multi-Agent Systems
  - Single-agent limitations: context dilution, role confusion, cognitive overload
  - Inter-agent communication protocols: shared state vs message passing
- [ ] **Week 28:** Core Topologies
  - **Supervisor / Router Pattern:** Central orchestrator decomposing goals and delegating to specialist agents
  - **Sequential Pipeline / Assembly Line:** Output of Agent A becomes input to Agent B
  - **Debate & Consensus Pattern:** Independent agents proposing solutions and critiquing edge cases
- [ ] **Week 29:** Large Swarm Prototyping on Cloud
  - Running a 6-agent swarm simultaneously on Kaggle (utilizing dual T4s / vLLM high-throughput batching)
  - Analyzing agent communication overhead, message serialization, and latency
- **Deliverable:** Multi-Agent Research Swarm (Planner → Searcher → Technical Writer → Reviewer) running locally and on cloud

### Weeks 30–32 — Deterministic State-Machine Orchestration (FSMs & Graphs)
- [ ] **Week 30:** Why Pure LLM Loops Fail in Production
  - The illusion of autonomy: non-determinism, infinite loops, compounding error rates
  - Deterministic state machines as structural guardrails
- [ ] **Week 31:** Graph-Based Orchestration
  - Nodes, edges, conditional branches, parallel execution paths
  - State persistence, checkpointing, and time-travel debugging (rewinding to prior states)
  - Framework analysis: LangGraph architecture vs custom FSM engines
- [ ] **Week 32:** Integrating with Project Academy's FSM
  - Connecting agent orchestration to `Project Academy`'s 8-state career OS (`academy/fsm.py`)
  - State transition validation, logging, and crash-resilient state recovery
- **Deliverable:** Deterministic FSM-driven agent workflow with checkpointing and resume-from-failure capabilities

### Weeks 33–35 — Human-in-the-Loop (HITL) & Safety Guardrails
- [ ] **Week 33:** Human-in-the-Loop Architecture
  - Breakpoints, interrupt gates, and manual approval workflows
  - Risk categorization: read-only actions vs destructive filesystem/network actions
- [ ] **Week 34:** State Diffing & Inspection
  - Generating human-readable change summaries before tool execution
  - Interactive terminal approval prompts and rollback mechanics
- [ ] **Week 35:** Error Recovery & Graceful Degradation
  - Fallback models, exponential backoff, circuit breakers on agent loops
  - Detecting and breaking infinite agent ping-pong loops
- **Deliverable:** Autonomous Git PR Creator agent with an interactive human approval gate before pushing commits

### Weeks 36–39 — Capstone Project: Autonomous Software Engineering Swarm
- [ ] **Week 36:** Architecture & Design
  - Multi-agent architecture:
    - *Architect Agent:* Analyzes GitHub issues, maps repo dependencies, drafts implementation plan
    - *Coder Agent:* Writes targeted code changes using precise file editing tools
    - *Reviewer Agent:* Performs static analysis, security checks, and code reviews
    - *QA Runner Agent:* Executes test suites in an isolated Docker container and reports results
- [ ] **Week 37:** Tool Integration & Local / Cloud Execution
  - Local mode on RTX 3050 for single-agent tasks
  - Cloud deployment script on Kaggle / Colab for heavy swarm batch execution
- [ ] **Week 38:** Testing & Benchmarking
  - Testing the swarm against 10 real GitHub issues from open-source repositories
  - Measuring resolution rate, token cost, and execution time
- [ ] **Week 39:** Production Polish & Documentation
  - Architecture diagrams, complete README, live execution screen recording
- **Deliverable:** Published GitHub repository: Autonomous Software Engineering Swarm with full test suite and documentation

---

## Phase 4: Peak & Place (Weeks 40–52) — Production Ops, Evals & System Design Interviews

### Weeks 40–43 — Agent Evaluation, Benchmarks & Observability
- [ ] **Week 40:** Evaluation Methodologies
  - Why traditional BLEU/ROUGE metrics fail for agents
  - Task completion metrics: success rate, step count efficiency, tool call accuracy
  - SWE-bench methodology overview
- [ ] **Week 41:** Synthetic Evaluation Harnesses
  - Building automated test harnesses to benchmark agent reliability
  - Regression testing prompts against model updates
- [ ] **Week 42:** Observability & Tracing
  - Instrumenting agents with OpenTelemetry, Langfuse, or Arize Phoenix
  - Tracing latency per step, token spend per sub-agent, and failure root-cause analysis
- [ ] **Week 43:** Stress Testing on Cloud
  - Executing 50-task batch evals on Kaggle / Colab to compute statistical success rates
- **Deliverable:** Automated Evaluation Suite reporting pass rates and latency metrics across 20 synthetic coding challenges

### Weeks 44–48 — Agent System Design Interviews (30–100 LPA Tier)
- [ ] **Week 44:** "Design an AI Coding Assistant like Cursor / GitHub Copilot"
  - Indexing codebases, real-time context retrieval, low-latency speculative completion, multi-file editing
- [ ] **Week 45:** "Design a Scalable Multi-Agent Customer Support & Workflow Automation System"
  - Hierarchical routing, stateful sessions, tool security, human escalation gates
- [ ] **Week 46:** "Design a Real-Time Agentic Search Engine with Hybrid RAG"
  - Query decomposition, parallel web scraping, citation verification, hallucination checks
- [ ] **Week 47:** "Design an Enterprise Knowledge Graph & Document Ingestion Pipeline"
  - Asynchronous OCR/parsing, entity resolution, graph updates, access control
- [ ] **Week 48:** Mock Interviews
  - Timed 45-minute whiteboarding sessions covering agent architecture tradeoffs
- **Deliverable:** 4 complete, production-grade system design architectural documents

### Weeks 49–52 — Portfolio Polish, Technical Blog & Final Review
- [ ] **Week 49:** Polish the Capstone Autonomous SWE Swarm repository
- [ ] **Week 50:** Write and publish a comprehensive technical deep-dive:
  - *"Building a Deterministic Multi-Agent Engineering Swarm with Local LLMs and FSMs"*
- [ ] **Week 51:** Integrate the Swarm demo, architecture diagram, and blog link into your Personal Portfolio Website (`hussny-06.github.io`)
- [ ] **Week 52:** Full academy review: Align all 5 faculties (C++ Systems, DSA, Data & Scale, Agentic AI, Interview Prep) for final placement drives
- **Deliverable:** Demo-ready Capstone featured on portfolio website + polished resume bullet points
