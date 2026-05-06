# Syllabus: Data & Scale (System Design + DevOps)
## Faculty Weight: 12% | 6h/week | Target: Design Scalable Systems, Containerize Everything

> **Reference Resources:**
> - *Designing Data-Intensive Applications* (DDIA) — Martin Kleppmann
> - ByteByteGo (visual system design)
> - Docker Documentation, PostgreSQL Documentation
> - *Database Internals* — Alex Petrov (advanced reference)
>
> **Weekly Cadence:** 2h theory/reading + 2h hands-on + 2h design practice

---

## Phase 1: Foundation (Weeks 1–13) — Databases & Linux

### Week 1 — SQL Fundamentals
- [ ] Relational model: tables, rows, columns, keys
- [ ] SQL: SELECT, JOIN (inner, left, right, full), GROUP BY, HAVING
- [ ] Subqueries, CTEs (Common Table Expressions)
- [ ] Aggregate functions, window functions (ROW_NUMBER, RANK, LAG/LEAD)
- **Deliverable:** Solve 20 SQL problems on LeetCode Database section

### Week 2 — PostgreSQL Deep Dive
- [ ] Installation (Docker-based), `psql` CLI
- [ ] Data types, constraints, indexes (B-Tree, Hash, GIN)
- [ ] EXPLAIN ANALYZE: reading query plans
- [ ] Transactions, ACID properties, isolation levels
- **Deliverable:** Design schema for a trading order management system

### Week 3 — Database Design & Normalization
- [ ] Normal forms: 1NF, 2NF, 3NF, BCNF
- [ ] Denormalization for read performance
- [ ] Schema design patterns: star schema, snowflake
- [ ] Index design strategy: composite indexes, partial indexes
- **Deliverable:** Schema for a social media platform (users, posts, followers, likes)

### Week 4 — Linux Administration Essentials
- [ ] File system hierarchy, permissions, ownership
- [ ] Process management: `ps`, `top`, `htop`, `kill`, `nice`
- [ ] Networking: `ip`, `netstat`, `ss`, `curl`, `dig`, `nslookup`
- [ ] Shell scripting: variables, loops, conditionals, `awk`, `sed`, `grep`
- **Deliverable:** Bash script that monitors system resources and logs to file

### Week 5 — Docker Fundamentals
- [ ] Containerization concepts: images, containers, layers
- [ ] Dockerfile: FROM, RUN, COPY, CMD, ENTRYPOINT
- [ ] Image optimization: multi-stage builds, `.dockerignore`
- [ ] `docker run`, `docker exec`, `docker logs`, volumes, port mapping
- **Deliverable:** Dockerize a Python FastAPI application with PostgreSQL

### Week 6 — Docker Compose & Multi-Container Apps
- [ ] `docker-compose.yml`: services, networks, volumes
- [ ] Environment variables, secrets management
- [ ] Health checks, depends_on, restart policies
- [ ] Building development vs production configurations
- **Deliverable:** Docker Compose stack: App + PostgreSQL + Redis + nginx

### Week 7 — Redis Fundamentals
- [ ] In-memory data store concepts, use cases
- [ ] Data structures: Strings, Hashes, Lists, Sets, Sorted Sets
- [ ] Commands: GET, SET, EXPIRE, TTL, HSET, ZADD
- [ ] Pub/Sub messaging pattern
- **Deliverable:** Implement a rate limiter using Redis (sliding window)

### Week 8 — Caching Strategies
- [ ] Cache-aside (lazy loading), write-through, write-behind
- [ ] Cache invalidation strategies (TTL, event-based)
- [ ] Cache stampede prevention (locking, probabilistic early expiration)
- [ ] Redis as session store, leaderboard, real-time analytics
- **Deliverable:** Add Redis caching to the Docker Compose app from Week 6

### Weeks 9–10 — Networking & HTTP
- [ ] **Week 9:** TCP/IP stack, DNS resolution, HTTP/1.1 vs HTTP/2 vs HTTP/3
  - TLS/SSL handshake, certificates
  - RESTful API design principles
- [ ] **Week 10:** Load balancing strategies
  - Round-robin, least connections, IP hash, consistent hashing
  - Reverse proxy: nginx configuration
  - Health checks, circuit breakers
- **Deliverable:** nginx reverse proxy configuration with load balancing across 3 app instances

### Weeks 11–13 — System Design Fundamentals
- [ ] **Week 11:** Horizontal vs vertical scaling
  - Stateless vs stateful services
  - Database replication: primary-replica, multi-primary
  - Database sharding strategies
- [ ] **Week 12:** Message queues & async processing
  - Kafka concepts: topics, partitions, consumer groups
  - RabbitMQ concepts: exchanges, queues, bindings
  - Event-driven architecture patterns
- [ ] **Week 13:** CAP theorem, consistency models
  - Strong consistency, eventual consistency, causal consistency
  - PACELC theorem
  - Consensus algorithms overview (Paxos, Raft)
- **Deliverable:** Write-up comparing Kafka vs RabbitMQ for an order processing system

---

## Phase 2: Deepening (Weeks 14–26) — System Design Practice

### Weeks 14–15 — System Design: Core Problems I
- [ ] **Week 14:** Design a URL Shortener
  - Hashing strategy, collision handling, analytics
  - Scale estimation: QPS, storage, bandwidth
- [ ] **Week 15:** Design a Rate Limiter
  - Token bucket, leaking bucket, sliding window
  - Distributed rate limiting with Redis
- **Deliverable:** Full written solution for each (framework format from DDIA)

### Weeks 16–17 — System Design: Core Problems II
- [ ] **Week 16:** Design a Chat System (WhatsApp-like)
  - WebSocket connections, message delivery, presence
  - Group chat architecture, message persistence
- [ ] **Week 17:** Design a News Feed / Timeline
  - Fan-out on write vs fan-out on read
  - Ranking algorithms, caching strategies
- **Deliverable:** Full written solution for each

### Weeks 18–19 — System Design: Core Problems III
- [ ] **Week 18:** Design a Notification System
  - Push vs pull, priority queues, template engine
  - Rate limiting notifications per user
- [ ] **Week 19:** Design a Distributed Cache
  - Consistent hashing ring, virtual nodes
  - Cache coherence, replication strategies
- **Deliverable:** Full written solution for each

### Weeks 20–22 — Database Internals
- [ ] **Week 20:** Storage engines: B-Tree vs LSM-Tree
  - Write-Ahead Log (WAL), checkpointing
  - MVCC (Multi-Version Concurrency Control)
- [ ] **Week 21:** Distributed databases
  - Partitioning: hash, range, directory-based
  - Replication: synchronous vs asynchronous
  - Conflict resolution strategies
- [ ] **Week 22:** Time-series databases, column stores
  - InfluxDB, TimescaleDB concepts
  - Columnar storage for analytics (Parquet, ClickHouse concepts)
- **Deliverable:** Comparison document: when to use SQL vs NoSQL vs time-series

### Weeks 23–26 — Advanced Infrastructure
- [ ] **Week 23:** Kubernetes concepts
  - Pods, Services, Deployments, ConfigMaps, Secrets
  - Container orchestration vs Docker Compose
- [ ] **Week 24:** CI/CD fundamentals
  - GitHub Actions pipeline: build → test → deploy
  - Container registry, image tagging strategy
- [ ] **Week 25:** Monitoring & observability
  - Metrics (Prometheus concepts), logging (ELK concepts), tracing
  - SLIs, SLOs, SLAs, error budgets
- [ ] **Week 26:** Infrastructure as Code
  - Terraform concepts (declarative infra)
  - Environment parity: dev = staging ≈ prod
- **Deliverable:** GitHub Actions pipeline that builds, tests, and pushes Docker image

---

## Phase 3: Specialization (Weeks 27–39) — Distributed KV Store Project

### Weeks 27–29 — Raft Consensus Implementation
- [ ] Raft paper reading and understanding
- [ ] Leader election, log replication, safety properties
- [ ] Implementation in Python or C++ (connects to C++ faculty)
- **Deliverable:** Working Raft implementation passing basic consensus tests

### Weeks 30–32 — KV Store Layer
- [ ] Key-value API: GET, PUT, DELETE
- [ ] Persistent storage with WAL
- [ ] Client library with retry logic
- [ ] Linearizable reads (read index / lease-based reads)
- **Deliverable:** Single-node KV store with persistence

### Weeks 33–35 — Distribution & Sharding
- [ ] Consistent hashing for key distribution
- [ ] Multi-shard architecture with shard router
- [ ] Cross-shard transactions (2PC concept)
- **Deliverable:** Multi-shard KV store with automatic key routing

### Weeks 36–39 — Production Readiness
- [ ] Docker Compose cluster (3-node Raft per shard)
- [ ] Failure injection testing: leader crash, network partition (simulated)
- [ ] Performance benchmarks: throughput, latency under load
- [ ] README with architecture diagram, deployment guide
- **Deliverable:** Published repo: Distributed KV Store

---

## Phase 4: Peak & Place (Weeks 40–52) — Interview Prep

### Weeks 40–43 — HFT System Design
- [ ] Design a low-latency trading system
- [ ] Design a market data distribution system
- [ ] Design an order management system
- [ ] Design a risk management system (real-time position tracking)
- **Deliverable:** Written solutions for all 4 HFT design problems

### Weeks 44–48 — Mock System Design Interviews
- [ ] 2 mock system design interviews per week
- [ ] Practice: 5-min requirements → 5-min estimation → 25-min design → 5-min tradeoffs
- [ ] Record and review each session for improvement
- **Deliverable:** 8 mock interviews completed, scored

### Weeks 49–52 — Final Review
- [ ] Review all 12 system design solutions written
- [ ] Update KV store project with any improvements
- [ ] Prepare 3-minute "elevator pitch" for each portfolio project
- **Deliverable:** All design docs polished, project talking points ready
