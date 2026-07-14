# Syllabus: C++ / Systems Programming
## Faculty Weight: 35% | 17h/week | Target: HFT-Ready Systems Engineer

> **Reference Books:**
> - *Effective Modern C++* — Scott Meyers
> - *C++ Concurrency in Action* — Anthony Williams
> - *Operating Systems: Three Easy Pieces* (OSTEP)
> - *Computer Systems: A Programmer's Perspective* (CS:APP)
>
> **Reference Talks:** CppCon (Fedor Pikus, Chandler Carruth, Patrice Roy)
> **Tools:** Godbolt Compiler Explorer, Google Benchmark, perf, Valgrind

---

## Phase 1: Foundation (Weeks 1–13)

### Week 1 — C++ Build Systems & Environment
- [x] CMake fundamentals: targets, libraries, compiler flags
- [x] GCC/Clang compilation pipeline: preprocessor → compiler → assembler → linker
- [x] Debug vs Release builds, `-O2` vs `-O3` vs `-Os`
- [x] Setting up Google Benchmark & Google Test
- **Deliverable:** CMake project template with benchmark + test targets
- **Resources:**
  - 🎥 [How the C++ Compiler Works — The Cherno (17 min)](https://www.youtube.com/watch?v=3tIqpEmWMLI)
  - 🎥 [How the C++ Linker Works — The Cherno (16 min)](https://www.youtube.com/watch?v=H4s55GgAg0I)
  - 📄 [CMake Tutorial Step 1: Building an Executable](https://cmake.org/cmake/help/latest/guide/tutorial/A%20Basic%20Starting%20Point.html) — Start here, read only Step 1
  - 📖 CS:APP Chapter 7 — Linking (explains why build systems exist)
  - ⏱️ Study time: ~1 hour (watch both Cherno videos + read CMake Step 1)

### Week 2 — Memory Model: Stack, Heap, Static
- [ ] Stack frame layout, calling conventions (cdecl, System V AMD64)
- [ ] Heap allocation internals: `malloc`/`free`, `brk`/`mmap`
- [ ] Static vs dynamic storage duration
- [ ] `sizeof`, alignment, padding rules (`alignof`, `alignas`)
- **Deliverable:** Program that visualizes memory layout of structs with different padding
- **Resources:**
  - 🎥 [Stack vs Heap Memory — The Cherno](https://www.youtube.com/watch?v=wJ1L2nSIV1s)
  - 📖 CS:APP Chapter 3.4 — Stack frames and calling conventions
  - 📖 CS:APP Chapter 9 — Virtual Memory
  - 📄 [Memory Layout of C Programs — GeeksforGeeks](https://www.geeksforgeeks.org/memory-layout-of-c-program/)

### Week 3 — RAII & Ownership
- [ ] Construction/destruction sequences (base → derived, member init order)
- [ ] Rule of Zero, Rule of Five
- [ ] `std::unique_ptr` deep dive — implement from scratch
- [ ] `std::shared_ptr` + `std::weak_ptr` — reference counting internals
- **Deliverable:** Custom `UniquePtr<T>` with deleter support, full test suite
- **Resources:**
  - 🎥 [RAII in C++ — The Cherno](https://www.youtube.com/watch?v=AmjoMSEXfmI)
  - 🎥 [Smart Pointers — The Cherno](https://www.youtube.com/watch?v=UOB7-B2MfwA)
  - 📖 *Effective Modern C++* — Items 18-22 (Smart Pointers)
  - 📄 [cppreference: std::unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)

### Week 4 — Move Semantics & Value Categories
- [ ] Lvalues, rvalues, xvalues, prvalues, glvalues
- [ ] Rvalue references, `std::move`, `std::forward`
- [ ] Perfect forwarding, reference collapsing rules
- [ ] `noexcept` and its impact on STL container performance
- **Deliverable:** Custom `Vector<T>` with move constructor/assignment, benchmark vs copy
- **Resources:**
  - 🎥 [Move Semantics — The Cherno](https://www.youtube.com/watch?v=ehMg6zvXuMY)
  - 🎥 [CppCon: Back to Basics Move Semantics — Klaus Iglberger](https://www.youtube.com/watch?v=knEaMpytRMA)
  - 📖 *Effective Modern C++* — Items 23-30 (Rvalue References & Move Semantics)
  - 📄 [cppreference: Value categories](https://en.cppreference.com/w/cpp/language/value_category)

### Week 5 — STL Internals
- [ ] `std::vector` — growth strategy, iterator invalidation
- [ ] `std::unordered_map` — hash table layout, load factor, rehashing
- [ ] `std::string` — SSO (Small String Optimization)
- [ ] `std::array`, `std::span` (C++20) for zero-cost views
- **Deliverable:** Implement `std::vector<T>` from raw memory (`placement new`, manual destructor calls)
- **Resources:**
  - 🎥 [How std::vector Works — The Cherno](https://www.youtube.com/watch?v=PocJ_JoM7bg)
  - 🎥 [CppCon: std::unordered_map — Matt Kulukundis](https://www.youtube.com/watch?v=ncHmEUmJZf4)
  - 📖 *Effective Modern C++* — Item 42 (Emplacement)
  - 📄 [cppreference: std::vector](https://en.cppreference.com/w/cpp/container/vector)

### Week 6 — Pointers, References & `const` Correctness
- [ ] Pointer arithmetic, array decay
- [ ] `const` correctness: `const T*` vs `T* const` vs `const T&`
- [ ] `mutable`, `const_cast` (and why you almost never use it)
- [ ] Function pointers, `std::function`, lambdas (capture semantics)
- **Deliverable:** Refactor a 200-line codebase for strict const correctness
- **Resources:**
  - 🎥 [Pointers in C++ — The Cherno](https://www.youtube.com/watch?v=DTxHyVn0ODg)
  - 🎥 [Const in C++ — The Cherno](https://www.youtube.com/watch?v=4fJBrditnJU)
  - 🎥 [Lambdas in C++ — The Cherno](https://www.youtube.com/watch?v=mWgmBBz0y8c)
  - 📖 *Effective Modern C++* — Items 31-33 (Lambda Expressions)

### Week 7 — Virtual Dispatch & Polymorphism Internals
- [ ] vtable layout, vptr, dynamic dispatch cost
- [ ] Virtual destructor necessity, pure virtual functions
- [ ] CRTP (Curiously Recurring Template Pattern) as static polymorphism
- [ ] Devirtualization by the compiler (`-O2` + `final`)
- **Deliverable:** Benchmark: virtual dispatch vs CRTP vs `std::variant` + `std::visit`

### Week 8 — Templates Fundamentals
- [ ] Function templates, class templates, template specialization
- [ ] Template argument deduction, CTAD (C++17)
- [ ] `constexpr` functions and variables
- [ ] `static_assert` for compile-time contracts
- **Deliverable:** Compile-time matrix multiplication using `constexpr`

### Week 9 — Error Handling Strategies
- [ ] Exceptions vs error codes vs `std::optional` vs `std::expected` (C++23)
- [ ] Exception safety guarantees (basic, strong, nothrow)
- [ ] Cost of exceptions (zero-cost when not thrown, table-based unwinding)
- [ ] When HFT systems disable exceptions entirely (`-fno-exceptions`)
- **Deliverable:** Implement a parser with 3 error handling strategies, benchmark all three

### Week 10 — Linux Process Model
- [ ] Process creation: `fork`, `exec`, `wait`
- [ ] Virtual memory: pages, page tables, TLB
- [ ] Signals, `mmap`, shared memory (`shm_open`)
- [ ] `/proc` filesystem, `strace` for syscall tracing
- **Deliverable:** Multi-process IPC system using shared memory + semaphores

### Week 11 — Linux I/O & File Systems
- [ ] File descriptors, `open`/`read`/`write`/`close`
- [ ] Buffered vs unbuffered I/O, `stdio` vs `syscall`
- [ ] `select`, `poll`, `epoll` — evolution of I/O multiplexing
- [ ] `io_uring` fundamentals (submission/completion queues)
- **Deliverable:** Echo server using `epoll`, then rewrite with `io_uring`, benchmark both

### Week 12 — CPU Architecture & Cache Hierarchy
- [ ] CPU pipeline: fetch, decode, execute, memory, writeback
- [ ] Branch prediction, speculative execution
- [ ] Cache hierarchy: L1/L2/L3, cache line size (64 bytes)
- [ ] Cache-friendly programming: SoA vs AoS, loop tiling
- **Deliverable:** Benchmark demonstrating cache miss penalty (random vs sequential access)

### Week 13 — Phase 1 Review & Memory Allocator Project Kickoff
- [ ] Comprehensive review: implement a mini-project using ALL Phase 1 concepts
- [ ] Memory Allocator project: design document & architecture
- [ ] Pool allocator skeleton code
- **Deliverable:** Memory Allocator design doc + initial implementation

---

## Phase 2: Deepening (Weeks 14–26)

### Week 14 — Advanced Templates & SFINAE
- [ ] SFINAE (Substitution Failure Is Not An Error)
- [ ] `std::enable_if`, `if constexpr` (C++17)
- [ ] C++20 Concepts: `requires` clause, concept definitions
- [ ] Variadic templates, fold expressions
- **Deliverable:** Type-safe serialization library using concepts

### Week 15 — Template Metaprogramming
- [ ] Type traits (`std::is_same`, `std::is_integral`, etc.)
- [ ] `consteval` (C++20), `constinit`
- [ ] Compile-time type lists, tuple implementation
- [ ] Policy-based design (Andrei Alexandrescu style)
- **Deliverable:** Compile-time state machine using TMP

### Week 16 — Threading Fundamentals
- [ ] `std::thread`, `std::jthread` (C++20)
- [ ] Thread lifecycle, joining, detaching
- [ ] `std::mutex`, `std::lock_guard`, `std::unique_lock`
- [ ] `std::condition_variable`, producer-consumer pattern
- **Deliverable:** Thread pool implementation (fixed-size, task queue)

### Week 17 — Advanced Concurrency
- [ ] `std::shared_mutex` (reader-writer locks)
- [ ] `std::future`, `std::promise`, `std::async`
- [ ] Deadlock prevention: lock ordering, `std::scoped_lock`
- [ ] Thread-safe singleton (Meyer's singleton, `std::call_once`)
- **Deliverable:** Concurrent hash map with reader-writer locking

### Week 18 — Atomics & Memory Ordering
- [ ] `std::atomic<T>`, atomic operations on integers and pointers
- [ ] Memory ordering: `relaxed`, `acquire`, `release`, `acq_rel`, `seq_cst`
- [ ] Compiler barriers vs hardware barriers
- [ ] Why `seq_cst` is the default (and when it's too expensive)
- **Deliverable:** Lock-free counter with all 5 memory orderings, benchmark each

### Week 19 — Lock-Free Data Structures
- [ ] CAS loops (`compare_exchange_weak` vs `strong`)
- [ ] Lock-free SPSC queue (single producer, single consumer)
- [ ] The ABA problem, hazard pointers, epoch-based reclamation
- [ ] Lock-free MPMC queue (Dmitry Vyukov's bounded queue)
- **Deliverable:** Lock-free SPSC ring buffer with benchmark vs `std::queue` + mutex

### Week 20 — Networking: Sockets & TCP/IP
- [ ] BSD socket API: `socket`, `bind`, `listen`, `accept`, `connect`
- [ ] TCP vs UDP tradeoffs, `TCP_NODELAY` (Nagle's algorithm)
- [ ] Non-blocking sockets, `O_NONBLOCK`
- [ ] Multicast UDP for market data feeds
- **Deliverable:** TCP echo server handling 1000 concurrent connections (epoll-based)

### Week 21 — Networking: Performance & Kernel Bypass
- [ ] Zero-copy techniques: `sendfile`, `splice`
- [ ] DPDK fundamentals (poll-mode drivers, hugepages)
- [ ] Solarflare/Onload (kernel bypass for trading)
- [ ] `SO_BUSY_POLL` and other socket tuning options
- **Deliverable:** Benchmark: kernel networking vs user-space (simulated DPDK path)

### Week 22 — Performance Profiling & Optimization
- [ ] `perf stat`, `perf record`, `perf report`
- [ ] Flamegraphs with Brendan Gregg's tools
- [ ] `cachegrind`, `callgrind` (Valgrind suite)
- [ ] Google Benchmark: microbenchmarking best practices
- **Deliverable:** Profile & optimize a deliberately slow program (target: 10x speedup)

### Week 23 — Memory Allocator Project: Pool & Slab
- [ ] Complete pool allocator with fixed-size blocks
- [ ] Slab allocator for variable-size objects
- [ ] Free list management, fragmentation analysis
- **Deliverable:** Working pool + slab allocator with unit tests

### Week 24 — Memory Allocator Project: Benchmarking
- [ ] Benchmark suite: allocator vs `malloc` vs `jemalloc` vs `tcmalloc`
- [ ] Multithreaded allocation benchmark (contention analysis)
- [ ] Memory usage profiling, fragmentation metrics
- **Deliverable:** Complete benchmark report with graphs, README, repo published

### Week 25 — Order Book Project Kickoff: Market Data Parsing
- [ ] Exchange binary protocol formats (simplified L3 feed)
- [ ] Parsing binary data in C++ (endianness, packed structs)
- [ ] Ring buffer for incoming market data
- **Deliverable:** Market data parser reading from a simulated binary feed

### Week 26 — Order Book Project: Matching Engine Core
- [ ] Price-time priority matching algorithm
- [ ] Order types: limit, market, cancel, modify
- [ ] Data structure choice: `std::map` vs custom sorted structure
- [ ] Lock-free order queue for submission
- **Deliverable:** Basic matching engine handling limit orders with price-time priority

---

## Phase 3: Specialization (Weeks 27–39)

### Week 27 — Order Book Project: Optimization Pass
- [ ] Profile the matching engine, identify hot paths
- [ ] Cache-friendly order book layout
- [ ] Pre-allocated memory pools for orders
- [ ] Latency measurement: tick-to-trade
- **Deliverable:** Optimized matching engine with latency benchmarks (target: <1μs per match)

### Week 28 — Order Book Project: Complete & Publish
- [ ] Full L3 order book with add/modify/cancel/trade events
- [ ] Load test: 1M+ orders per second
- [ ] Comprehensive README with architecture diagram
- **Deliverable:** Published repo with benchmarks, architecture doc, and build instructions

### Week 29 — Advanced C++20/23 Features
- [ ] Ranges library (`std::views`, lazy evaluation)
- [ ] Coroutines (`co_await`, `co_yield`, `co_return`)
- [ ] Modules (replacing headers)
- [ ] `std::expected` (C++23), `std::mdspan`
- **Deliverable:** Refactor a previous project to use ranges + coroutines

### Week 30 — Design Patterns for Systems Code
- [ ] LMAX Disruptor pattern (ring buffer + sequence barriers)
- [ ] Actor model (message passing between threads)
- [ ] Event-driven architecture, reactor pattern
- [ ] Object pool pattern for zero-allocation hot paths
- **Deliverable:** Event-driven message processing system using Disruptor pattern

### Week 31 — OS Internals: Scheduling & Memory Management
- [ ] Linux process scheduler: CFS, `SCHED_FIFO`, `SCHED_RR`
- [ ] CPU affinity, thread pinning (`pthread_setaffinity_np`)
- [ ] `mlockall` to prevent page faults, hugepages (`mmap` with `MAP_HUGETLB`)
- [ ] NUMA awareness for multi-socket systems
- **Deliverable:** Benchmark showing latency impact of thread pinning + hugepages

### Week 32 — Compiler Optimization & Assembly Reading
- [ ] Reading x86-64 assembly (Godbolt Compiler Explorer)
- [ ] Common compiler optimizations: inlining, loop unrolling, vectorization (SSE/AVX)
- [ ] `__builtin_expect`, `[[likely]]`/`[[unlikely]]` (C++20)
- [ ] Link-Time Optimization (LTO), Profile-Guided Optimization (PGO)
- **Deliverable:** Optimize a hot loop by guiding compiler with intrinsics, verify on Godbolt

### Weeks 33–35 — Edge AI Inference Engine (C++ Component)
- [ ] ONNX model loading in C++ (onnxruntime C++ API)
- [ ] Custom memory management for tensor buffers
- [ ] Multithreaded inference pipeline
- **Deliverable:** C++ inference server for ONNX models (connects to AI faculty project)

### Weeks 36–39 — Advanced Systems Topics
- [ ] **Week 36:** Shared libraries, dynamic linking, `dlopen`/`dlsym`, plugin architectures
- [ ] **Week 37:** IPC deep dive: Unix domain sockets, named pipes, eventfd, signal handling
- [ ] **Week 38:** Linux namespaces & cgroups (how Docker works under the hood)
- [ ] **Week 39:** Building a minimal container runtime from scratch (namespace + cgroups + chroot)
- **Deliverable:** Minimal container runtime that can isolate a process

---

## Phase 4: Peak & Place (Weeks 40–52)

### Weeks 40–42 — Distributed KV Store (C++ Component)
- [ ] Raft consensus protocol implementation in C++
- [ ] Persistent log storage, state machine replication
- [ ] Client library with linearizable reads
- **Deliverable:** C++ Raft node (connects to Data & Scale faculty project)

### Weeks 43–45 — HFT Interview Preparation (C++ Focus)
- [ ] Implement `std::vector`, `std::string`, `std::shared_ptr` from scratch
- [ ] Implement a thread-safe concurrent queue (multiple approaches)
- [ ] Common HFT C++ interview questions:
  - Virtual dispatch cost, vtable layout
  - Move semantics edge cases
  - Memory ordering scenarios
  - Cache optimization problems
- **Deliverable:** Portfolio of "implement from scratch" solutions with tests

### Weeks 46–48 — Mock Technical Rounds
- [ ] Timed implementation problems (45-min mock sessions)
- [ ] System design: "Design a trading system's hot path"
- [ ] Code review exercises: find bugs in concurrency code
- **Deliverable:** 6 mock interview sessions completed, scored

### Weeks 49–52 — Final Review & Portfolio Polish
- [ ] Review all 4 portfolio projects, update READMEs
- [ ] Ensure all projects build cleanly on fresh Ubuntu install
- [ ] Prepare project deep-dive talking points for interviews
- [ ] Final gap analysis against target company JDs
- **Deliverable:** All repos polished, talking points documented
