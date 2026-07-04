# Syllabus: Edge AI / Machine Learning
## Faculty Weight: 15% | 7h/week | Target: Deploy ML Models on Edge Hardware in C++

> **Reference Resources:**
> - NVIDIA TensorRT Developer Guide
> - ONNX Runtime Documentation
> - PyTorch Documentation (torch.onnx)
> - *Deep Learning* — Ian Goodfellow (foundations reference)
>
> **Hardware:** RTX 3050 (6GB VRAM) — all work must be feasible on this GPU and also there are
 other onile platforms like kaggle that can be used when work preceeds the capability of these GPU
> **Weekly Cadence:** 2h theory + 4h hands-on + 1h reading/research

---

## Phase 1: Foundation (Weeks 1–13) — ML & Deep Learning Basics

### Week 1 — Python ML Ecosystem Setup
- [ ] Python environment: `venv`, `pip`, `conda` basics
- [ ] NumPy fundamentals: arrays, broadcasting, vectorized operations
- [ ] Matplotlib/Seaborn for visualization
- **Deliverable:** NumPy-only implementation of linear regression with gradient descent

### Week 2 — ML Fundamentals
- [ ] Supervised vs unsupervised learning
- [ ] Linear regression, logistic regression (math + implementation)
- [ ] Loss functions: MSE, cross-entropy
- [ ] Gradient descent variants: batch, mini-batch, SGD
- **Deliverable:** Logistic regression classifier from scratch (NumPy only)

### Week 3 — Neural Network Foundations
- [ ] Perceptron, multi-layer perceptron (MLP)
- [ ] Backpropagation derivation (chain rule)
- [ ] Activation functions: ReLU, sigmoid, tanh, softmax
- [ ] Weight initialization strategies
- **Deliverable:** 2-layer MLP from scratch (NumPy) on MNIST

### Week 4 — PyTorch Fundamentals
- [ ] Tensors, autograd, computational graphs
- [ ] `nn.Module`, `nn.Linear`, `nn.Sequential`
- [ ] `DataLoader`, `Dataset`, transforms
- [ ] Training loop: forward → loss → backward → step
- **Deliverable:** MNIST classifier in PyTorch (>98% accuracy)

### Week 5 — Convolutional Neural Networks
- [ ] Convolution operation, kernel/filter, stride, padding
- [ ] Pooling layers (max, average)
- [ ] Classic architectures: LeNet, AlexNet (concepts)
- [ ] Modern architectures: ResNet (skip connections), MobileNet (depthwise separable convolutions)
- **Deliverable:** CIFAR-10 classifier using ResNet-18 (transfer learning)

### Week 6 — Training Best Practices
- [ ] Regularization: dropout, weight decay, data augmentation
- [ ] Learning rate scheduling: step, cosine annealing, warm-up
- [ ] Batch normalization, layer normalization
- [ ] Overfitting diagnosis, train/val/test splits
- **Deliverable:** Train a model with all regularization techniques, compare results

### Week 7 — Object Detection Foundations
- [ ] Region-based methods: R-CNN family (concepts)
- [ ] Single-shot detectors: YOLO architecture, SSD
- [ ] Anchor boxes, IoU, Non-Maximum Suppression (NMS)
- [ ] mAP (mean Average Precision) metric
- **Deliverable:** Fine-tune YOLOv8-nano on a custom 3-class dataset

### Week 8 — Sequence Models
- [ ] RNN fundamentals, vanishing gradient problem
- [ ] LSTM, GRU architectures
- [ ] Attention mechanism (Bahdanau attention)
- [ ] Transformer architecture: self-attention, multi-head attention, positional encoding
- **Deliverable:** Sentiment classifier using a small transformer

### Weeks 9–10 — Model Optimization Theory
- [ ] **Week 9:** Quantization fundamentals (FP32 → FP16 → INT8)
  - Post-training quantization (PTQ) vs quantization-aware training (QAT)
  - Calibration datasets, accuracy/speed tradeoffs
- [ ] **Week 10:** Model compression techniques
  - Pruning: structured vs unstructured
  - Knowledge distillation: teacher-student framework
  - Neural Architecture Search (NAS) concepts
- **Deliverable:** Quantize a ResNet model (FP32 → INT8), measure accuracy drop + speedup

### Weeks 11–13 — ONNX Fundamentals
- [ ] **Week 11:** ONNX format: operators, graph structure, opset versions
  - Export PyTorch model to ONNX (`torch.onnx.export`)
  - Verify with ONNX checker, visualize with Netron
- [ ] **Week 12:** ONNX Runtime: Python API
  - InferenceSession, input/output binding
  - Execution providers: CPU, CUDA
  - Benchmark: PyTorch vs ONNX Runtime inference
- [ ] **Week 13:** ONNX graph optimization
  - ONNX Simplifier (onnx-simplifier)
  - Operator fusion, constant folding
- **Deliverable:** Full pipeline: train in PyTorch → export ONNX → optimize → benchmark

---

## Phase 2: Deepening (Weeks 14–26) — Inference Optimization

### Weeks 14–16 — TensorRT Fundamentals
- [ ] **Week 14:** TensorRT architecture: builder, engine, runtime
  - `trtexec` CLI tool for quick profiling
  - Build TRT engine from ONNX model
- [ ] **Week 15:** TensorRT optimizations
  - Layer fusion, kernel auto-tuning
  - FP16 inference on RTX 3050
  - INT8 calibration with calibration dataset
- [ ] **Week 16:** TensorRT C++ API
  - `IBuilder`, `INetworkDefinition`, `ICudaEngine`
  - Memory management: device buffers, host-device transfers
  - Synchronous vs asynchronous inference
- **Deliverable:** C++ application loading TRT engine and running inference

### Weeks 17–18 — CUDA Programming Basics
- [ ] **Week 17:** CUDA programming model
  - Threads, blocks, grids, warps
  - Kernel launch syntax, `__global__`, `__device__`, `__host__`
  - Thread indexing: `threadIdx`, `blockIdx`, `blockDim`
- [ ] **Week 18:** CUDA memory model
  - Global, shared, constant, register memory
  - Memory coalescing, bank conflicts
  - `cudaMalloc`, `cudaMemcpy`, `cudaFree`
- **Deliverable:** Custom CUDA kernel for matrix multiplication, benchmark vs cuBLAS

### Weeks 19–20 — Advanced Inference Patterns
- [ ] **Week 19:** Batched inference, dynamic batching
  - Throughput vs latency tradeoffs
  - Input shape optimization (fixed vs dynamic shapes in TRT)
- [ ] **Week 20:** Multi-stream inference
  - CUDA streams for concurrent execution
  - Pipeline: preprocess → infer → postprocess (overlapping)
- **Deliverable:** Multi-stream inference pipeline with preprocessing overlap

### Weeks 21–22 — Real-Time Video Inference
- [ ] **Week 21:** OpenCV + CUDA integration
  - Video capture, frame preprocessing on GPU
  - GStreamer pipeline concepts
- [ ] **Week 22:** End-to-end video inference pipeline
  - Camera → decode → preprocess → infer → postprocess → display
  - FPS measurement, frame dropping strategies
- **Deliverable:** Real-time object detection on webcam feed using TensorRT

### Weeks 23–26 — Edge Deployment Patterns
- [ ] **Week 23:** Model serving architectures
  - NVIDIA Triton Inference Server concepts
  - REST vs gRPC for model serving
- [ ] **Week 24:** Cross-platform inference
  - ONNX Runtime vs TensorRT vs OpenVINO (comparison)
  - When to use which runtime
- [ ] **Week 25:** Profiling & debugging inference
  - NVIDIA Nsight Systems for profiling
  - Identifying bottlenecks: CPU-bound vs GPU-bound
- [ ] **Week 26:** Edge MLOps concepts
  - Model versioning, A/B testing at edge
  - OTA model updates pattern
- **Deliverable:** Documented comparison: ONNX Runtime vs TensorRT for same model on RTX 3050

---

## Phase 3: Specialization (Weeks 27–39) — Inference Engine Project

### Weeks 27–29 — Project: ONNX Model Loader
- [ ] C++ ONNX model parser (using onnxruntime C++ API)
- [ ] Custom memory allocator for tensor buffers
- [ ] Model validation and error handling
- **Deliverable:** C++ library that loads and validates any ONNX model

### Weeks 30–32 — Project: TensorRT Backend
- [ ] TensorRT engine builder from ONNX
- [ ] FP16 + INT8 quantization pipeline
- [ ] Engine serialization/deserialization (plan files)
- **Deliverable:** Automated ONNX → TensorRT conversion with quantization options

### Weeks 33–35 — Project: Inference Server
- [ ] HTTP API for model inference (simple REST endpoint)
- [ ] Multithreaded request handling
- [ ] Batching scheduler for throughput optimization
- [ ] Health checks, metrics endpoint (latency p50/p99/p999)
- **Deliverable:** C++ inference server handling 100+ req/s for image classification

### Weeks 36–39 — Project: Polish & Benchmark
- [ ] Comprehensive benchmark suite: latency, throughput, memory usage
- [ ] Support for multiple model architectures (classification, detection)
- [ ] Docker container for deployment
- [ ] README with architecture diagram, performance results
- **Deliverable:** Published repo: Edge AI Inference Engine

---

## Phase 4: Peak & Place (Weeks 40–52) — Advanced Topics & Interview Prep

### Weeks 40–43 — Emerging AI Topics
- [ ] Vision Transformers (ViT) — inference optimization challenges
- [ ] Large Language Model inference: KV-cache, speculative decoding (concepts)
- [ ] Diffusion models at the edge (concepts)
- [ ] On-device training concepts (federated learning intro)

### Weeks 44–48 — NVIDIA-Specific Interview Prep
- [ ] CUDA interview questions: memory hierarchy, warp divergence, occupancy
- [ ] GPU architecture: SMs, tensor cores, memory bandwidth
- [ ] Common ML system design: "Design a real-time video analytics pipeline"
- **Deliverable:** 5 ML system design mock answers

### Weeks 49–52 — Portfolio & Review
- [ ] Inference engine project final polish
- [ ] Prepare demo: live inference on webcam with FPS overlay
- [ ] Write technical blog post explaining the architecture
- **Deliverable:** Demo-ready inference engine + blog post draft
