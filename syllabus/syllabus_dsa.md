# Syllabus: Data Structures & Algorithms
## Faculty Weight: 25% | 12h/week | Target: LC Hard Fluency + Competitive Speed

> **Reference Resources:**
> - *Striver's A2Z DSA Sheet* (Take U Forward)
> - *Competitive Programmer's Handbook* — Antti Laaksonen
> - cp-algorithms.com (advanced topics reference)
> - LeetCode, Codeforces (practice platforms)
>
> **Weekly Cadence:** 2h theory + 8h problem solving + 2h contest/upsolving
> **Target:** 400+ LeetCode problems (150 Easy, 175 Medium, 75+ Hard)

---

## Phase 1: Foundation (Weeks 1–13)

### Week 1 — Complexity Analysis & Arrays
- [x] Big-O, Big-Ω, Big-Θ — formal definitions with proofs
- [x] Amortized analysis (aggregate, accounting, potential methods)
- [x] Array problems: Two Sum, Kadane's algorithm, Dutch National Flag
- **Problems:** 10 Easy (arrays), 5 Medium (arrays)
- **LC Focus:** #1, #53, #75, #238, #41

### Week 2 — Strings & Hashing
- [x] String manipulation, substring problems
- [x] Hash maps, frequency counting, anagram grouping
- [x] Rolling hash (Rabin-Karp) introduction
- **Problems:** 8 Easy, 7 Medium
- **LC Focus:** #49, #3, #76, #242, #438

### Week 3 — Two Pointers & Sliding Window
- [ ] Two pointer patterns: converging, same direction, fast-slow
- [ ] Fixed-size sliding window, variable-size sliding window
- [ ] Minimum window substring pattern
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #15, #11, #42, #76, #239

### Week 4 — Linked Lists
- [ ] Singly linked list: reversal, cycle detection (Floyd's)
- [ ] Doubly linked list, LRU cache implementation
- [ ] Merge sorted lists, intersection detection
- **Problems:** 8 Easy, 7 Medium
- **LC Focus:** #206, #141, #142, #21, #146, #23

### Week 5 — Stacks & Queues
- [ ] Stack applications: valid parentheses, min stack
- [ ] Monotonic stack pattern (next greater element)
- [ ] Queue from stacks, circular queue
- [ ] Deque applications: sliding window maximum
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #20, #155, #496, #739, #84, #85

### Week 6 — Binary Search Mastery
- [ ] Standard binary search, search in rotated array
- [ ] Binary search on answer (capacity, speed, distance problems)
- [ ] Upper bound, lower bound patterns
- [ ] Median of two sorted arrays
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #33, #34, #875, #1011, #4

### Week 7 — Sorting & Searching Deep Dive
- [ ] Merge sort (and its applications: inversion count)
- [ ] Quick sort, quickselect (Kth largest)
- [ ] Counting sort, radix sort (non-comparison sorts)
- [ ] Custom comparators for complex sorting
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #215, #347, #179, #56, #315

### Week 8 — Recursion & Backtracking
- [ ] Recursion tree visualization, stack depth analysis
- [ ] Subsets, permutations, combinations (the 3 backtracking templates)
- [ ] N-Queens, Sudoku Solver
- [ ] Pruning strategies for optimization
- **Problems:** 3 Easy, 8 Medium, 4 Hard
- **LC Focus:** #78, #46, #39, #51, #37, #131

### Week 9 — Binary Trees I
- [ ] Traversals: inorder, preorder, postorder, level order
- [ ] Height, diameter, balanced tree check
- [ ] Lowest Common Ancestor (LCA)
- [ ] Serialize/deserialize binary tree
- **Problems:** 8 Easy, 7 Medium
- **LC Focus:** #104, #543, #236, #102, #297

### Week 10 — Binary Trees II & BST
- [ ] BST property, search, insert, delete
- [ ] Validate BST, Kth smallest in BST
- [ ] BST from preorder, inorder + preorder reconstruction
- [ ] AVL tree / Red-Black tree concepts (no implementation needed)
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #98, #230, #1008, #105, #124

### Week 11 — Heaps & Priority Queues
- [ ] Min-heap, max-heap implementation from array
- [ ] Heap operations: insert, extract, heapify
- [ ] Top-K problems, merge K sorted lists
- [ ] Median from data stream (two-heap technique)
- **Problems:** 3 Easy, 7 Medium, 3 Hard
- **LC Focus:** #215, #347, #23, #295, #373

### Week 12 — Tries & Advanced Hashing
- [ ] Trie (prefix tree) implementation
- [ ] Autocomplete, word search, word dictionary
- [ ] Bloom filters (concept), consistent hashing (concept)
- **Problems:** 3 Easy, 7 Medium, 2 Hard
- **LC Focus:** #208, #211, #212, #336, #745

### Week 13 — Phase 1 Review & Contest Prep
- [ ] Solve 15 mixed problems (timed, 45 min each)
- [ ] Participate in 2 LeetCode weekly contests
- [ ] Review all incorrect/slow solutions from Weeks 1-12
- **Target:** 150+ problems completed by end of Phase 1

---

## Phase 2: Deepening (Weeks 14–26)

### Week 14 — Graphs I: Representation & Traversal
- [ ] Adjacency list vs adjacency matrix
- [ ] BFS: shortest path in unweighted graph, multi-source BFS
- [ ] DFS: connected components, grid traversal
- [ ] Bipartite check, flood fill
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #200, #695, #994, #785, #127

### Week 15 — Graphs II: Cycle Detection & Topological Sort
- [ ] Cycle detection: directed (DFS coloring) and undirected (union-find)
- [ ] Topological sort: Kahn's BFS + DFS-based
- [ ] Course schedule problems, alien dictionary
- **Problems:** 2 Easy, 8 Medium, 2 Hard
- **LC Focus:** #207, #210, #269, #802, #1462

### Week 16 — Graphs III: Shortest Paths
- [ ] Dijkstra's algorithm (min-heap implementation)
- [ ] Bellman-Ford (negative weights)
- [ ] Floyd-Warshall (all-pairs shortest path)
- [ ] 0-1 BFS (deque-based)
- **Problems:** 0 Easy, 8 Medium, 4 Hard
- **LC Focus:** #743, #787, #1514, #1334, #882

### Week 17 — Graphs IV: MST & Advanced
- [ ] Kruskal's algorithm (with Union-Find)
- [ ] Prim's algorithm (min-heap)
- [ ] Union-Find: path compression + union by rank
- [ ] Applications: number of islands (union-find), redundant connection
- **Problems:** 0 Easy, 8 Medium, 3 Hard
- **LC Focus:** #684, #1584, #1135, #778, #1168

### Week 18 — Graphs V: Advanced Graph Algorithms
- [ ] Strongly Connected Components (Tarjan's, Kosaraju's)
- [ ] Articulation points and bridges
- [ ] Euler paths and circuits
- [ ] Network flow concepts (Ford-Fulkerson, max-flow min-cut)
- **Problems:** 0 Easy, 5 Medium, 3 Hard
- **LC Focus:** #1192, #1568, #332, #1489

### Week 19 — Dynamic Programming I: Fundamentals
- [ ] Memoization vs tabulation
- [ ] 1D DP: climbing stairs, house robber, decode ways
- [ ] Fibonacci variants, coin change
- [ ] State definition methodology (what changes between subproblems?)
- **Problems:** 5 Easy, 8 Medium, 2 Hard
- **LC Focus:** #70, #198, #91, #322, #139

### Week 20 — Dynamic Programming II: 2D & Grid DP
- [ ] Grid DP: unique paths, minimum path sum
- [ ] 0/1 Knapsack, unbounded knapsack
- [ ] Longest Common Subsequence (LCS), Edit Distance
- [ ] DP space optimization (rolling array)
- **Problems:** 2 Easy, 8 Medium, 3 Hard
- **LC Focus:** #62, #64, #1143, #72, #312

### Week 21 — Dynamic Programming III: String DP
- [ ] Longest Palindromic Subsequence/Substring
- [ ] Wildcard matching, regex matching
- [ ] Interleaving strings, distinct subsequences
- **Problems:** 0 Easy, 5 Medium, 5 Hard
- **LC Focus:** #5, #516, #10, #44, #115

### Week 22 — Dynamic Programming IV: Interval & State Machine DP
- [ ] Matrix chain multiplication pattern
- [ ] Burst balloons, strange printer
- [ ] Stock buying/selling (state machine DP approach)
- [ ] Palindrome partitioning
- **Problems:** 0 Easy, 5 Medium, 5 Hard
- **LC Focus:** #312, #664, #188, #123, #132

### Week 23 — Greedy Algorithms
- [ ] Activity selection, interval scheduling
- [ ] Jump game variants
- [ ] Huffman coding concept
- [ ] When greedy works vs when you need DP (exchange argument proofs)
- **Problems:** 3 Easy, 8 Medium, 2 Hard
- **LC Focus:** #55, #45, #134, #435, #621

### Week 24 — Bit Manipulation
- [ ] Bitwise operations review, XOR tricks
- [ ] Counting bits, power of two, single number variants
- [ ] Bitmask enumeration for subsets
- [ ] Brian Kernighan's algorithm
- **Problems:** 5 Easy, 7 Medium, 2 Hard
- **LC Focus:** #136, #137, #260, #338, #1863

### Week 25 — Math & Number Theory
- [ ] GCD (Euclidean), LCM, modular arithmetic
- [ ] Sieve of Eratosthenes, prime factorization
- [ ] Fast exponentiation (binary exponentiation)
- [ ] Combinatorics: nCr with modular inverse
- **Problems:** 5 Easy, 7 Medium, 2 Hard
- **LC Focus:** #204, #50, #372, #343, #829

### Week 26 — Phase 2 Review & Contest Push
- [ ] Solve 20 mixed Medium/Hard problems (timed)
- [ ] Participate in 3 Codeforces rounds (Div 2)
- [ ] Upsolve all unsolved contest problems
- **Target:** 300+ problems completed by end of Phase 2

---

## Phase 3: Specialization (Weeks 27–39)

### Week 27 — Segment Trees I
- [ ] Segment tree: build, point update, range query
- [ ] Range sum queries, range minimum queries
- [ ] Implementation: array-based (2*N space)
- **Problems:** 0 Easy, 5 Medium, 3 Hard
- **LC Focus:** #307, #315, #327, #493

### Week 28 — Segment Trees II: Lazy Propagation
- [ ] Range updates with lazy propagation
- [ ] Range add + range sum query
- [ ] Range set + range min query
- [ ] Persistent segment tree concepts
- **Problems:** 0 Easy, 3 Medium, 4 Hard

### Week 29 — Fenwick Tree (BIT) & Square Root Decomposition
- [ ] Binary Indexed Tree: point update, prefix sum
- [ ] 2D BIT for matrix problems
- [ ] Square root decomposition: Mo's algorithm
- **Problems:** 0 Easy, 5 Medium, 3 Hard
- **LC Focus:** #307 (BIT version), #308, #1649

### Week 30 — Advanced DP: DP on Trees
- [ ] Tree DP: diameter, max path sum
- [ ] Rerooting technique
- [ ] Tree coloring, independent set on trees
- **Problems:** 0 Easy, 5 Medium, 4 Hard
- **LC Focus:** #124, #337, #968, #1372

### Week 31 — Advanced DP: Bitmask DP
- [ ] Subset DP: Travelling Salesman (Held-Karp)
- [ ] Assignment problem with bitmask
- [ ] Profile DP (broken profile)
- **Problems:** 0 Easy, 3 Medium, 4 Hard
- **LC Focus:** #1125, #943, #691, #1494

### Week 32 — Advanced DP: Digit DP & Probability DP
- [ ] Digit DP: count numbers with certain properties in range
- [ ] Probability DP, expected value problems
- **Problems:** 0 Easy, 3 Medium, 4 Hard

### Week 33 — String Algorithms
- [ ] KMP (Knuth-Morris-Pratt) pattern matching
- [ ] Z-algorithm
- [ ] Rabin-Karp (rolling hash)
- [ ] Suffix arrays introduction
- **Problems:** 0 Easy, 5 Medium, 3 Hard
- **LC Focus:** #28, #214, #1392, #459

### Week 34 — Advanced Graph: Shortest Paths & Special Graphs
- [ ] Dijkstra with modifications (K shortest paths)
- [ ] A* search algorithm
- [ ] Directed acyclic graph (DAG) shortest/longest path
- [ ] Centroid decomposition introduction
- **Problems:** 0 Easy, 4 Medium, 4 Hard

### Week 35 — Game Theory & Miscellaneous
- [ ] Sprague-Grundy theorem, Nim game
- [ ] Minimax algorithm with alpha-beta pruning
- [ ] Geometry basics: convex hull, line intersection
- **Problems:** 0 Easy, 5 Medium, 3 Hard
- **LC Focus:** #292, #877, #464, #1140

### Weeks 36–39 — Intensive Problem Solving Sprint
- [ ] **Week 36:** 15 Hard graph/DP problems
- [ ] **Week 37:** 15 Hard segment tree/string problems
- [ ] **Week 38:** 10 Codeforces Div 1 problems (upsolving)
- [ ] **Week 39:** Company-tagged problems (Tower Research, Goldman, Morgan Stanley on LC)
- **Target:** 380+ problems completed by end of Phase 3

---

## Phase 4: Peak & Place (Weeks 40–52)

### Weeks 40–43 — Interview Pattern Mastery
- [ ] **Week 40:** Top 30 most-asked LC problems across target companies
- [ ] **Week 41:** Timed practice — 2 Medium + 1 Hard in 90 min
- [ ] **Week 42:** System design + DSA combo rounds (mock)
- [ ] **Week 43:** Revisit all problems where solution took >30 min

### Weeks 44–47 — Mock Interviews & Contests
- [ ] 2 mock interviews per week (peer or platform)
- [ ] Weekly Codeforces + LeetCode contests
- [ ] Upsolve every problem not solved in contest
- [ ] Track contest rating progression

### Weeks 48–50 — Weak Area Blitz
- [ ] Identify bottom 3 topic areas from failure analysis
- [ ] 10 focused problems per weak area
- [ ] Re-test with timed problems in those areas

### Weeks 51–52 — Final Review
- [ ] Review spaced repetition queue — clear all overdue items
- [ ] Speed run: solve 5 Medium problems in 60 min
- [ ] Confidence check: solve 2 Hard problems cold
- **Target:** 400+ problems completed, contest rating 1600+ (Codeforces)
