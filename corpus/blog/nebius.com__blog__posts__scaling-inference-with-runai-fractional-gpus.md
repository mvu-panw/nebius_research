# Scaling efficient production-grade inference with NVIDIA Run:ai on Nebius

Source: https://nebius.com/blog/posts/scaling-inference-with-runai-fractional-gpus

Skip to main content

As AI moves into production, inference is becoming more and more a defining operational challenge. Training is finite; inference runs continuously, scales with real user demand and directly determines both cost and user experience. NVIDIA has emphasized this shift, highlighting how throughput, latency and cost per token are now core business metrics for production AI — not just technical considerations.

At the same time, inference workloads have fundamentally changed. Production environments rarely serve a single model in isolation. They combine large language models, embedding models and smaller task-specific models, often under bursty and highly concurrent demand. Traditional deployment patterns — dedicating full GPUs to individual models — lead to idle capacity, rising costs and unpredictable performance as workloads diversify.

## What the benchmarks showWhat the benchmarks show

To evaluate a more efficient approach, NVIDIA and Nebius ran joint benchmarks using NVIDIA Run:ai, the AI workload orchestration and optimization software platform in Nebius AI Cloud. The goal was simple: test whether fractional GPU allocation could improve efficiency and scalability for real-world inference workloads — without compromising performance.

The results validate that it can. Across full GPUs and fractional slices down to 0.125 GPU, the benchmarks demonstrated:

- 

Consistent throughput scaling across single-node and multi-GPU clusters

- 

Improved GPU utilization with minimal idle capacity

- 

Stable latency, including Time-to-First-Token (TTFT), under mixed workloads and high concurrency

- 

Reliable elastic autoscaling behavior during scale-out events

Embedding models, in particular, performed well under high-density fractionalization, making them strong candidates for cost-sensitive and high-concurrency inference environments.

## NVIDIA Run:ai on NebiusNVIDIA Run:ai on Nebius

Nebius AI Cloud is the foundation for production inference, delivering full-stack, scalable NVIDIA compute, networking and storage designed for predictable performance under real-world concurrency and mixed workloads. NVIDIA Run:ai layers intelligent GPU orchestration on top, using fractional GPU allocation and dynamic workload scheduling to maximize utilization while maintaining stable latency and throughput. Unlike static GPU partitioning, fractional GPUs are allocated and scheduled dynamically based on workload demand.

Together, Nebius and NVIDIA Run:ai deliver a more efficient model for scaling inference in production across fractional GPUs bringing improved utilization with minimal idle capacity, stable latency under high concurrency and reliable autoscaling behavior across multi-model workloads.

For a deeper technical breakdown of the benchmarking methodology and performance results, read the full analysis on the NVIDIA Developer Blog. Or check out the NVIDIA GTC 2026 session S82234, “Scale Inference Using Open Models: How Nebius Token Factory Delivers Control and Efficiency,” presented by Nebius.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

The energy behind AI: Why power efficiency matters

As AI adoption accelerates, energy use increasingly sets the boundaries of how far the systems can scale. Power availability, efficiency and infrastructure design are becoming practical constraints. This shift is prompting to think of concrete ways to manage the energy footprint of AI systems by optimizing energy use and creating measurable efficiency gains. In our latest whitepaper, we explain how Nebius improves efficiency across the stack, from software engineering to hardware design and data center operations.

January 26, 2026
4 mins to read

Sign in to save this post
Sign In
