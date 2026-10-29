# Post-training by Nebius Token Factory: The missing layer between a minimum viable product and production

Source: https://nebius.com/blog/posts/post-training-in-token-factory

Skip to main content

Train large open-source models across multi-node clusters, distill them into fast students, enforce structured outputs and deploy instantly to dedicated, zero-retention endpoints.

This is how modern teams turn usage data into better models, without building an ML infra team.

“Post-training with Nebius Token Factory let us match the SWE performance of closed-source giants — in a fully private environment”

— Cosine

Now, let’s look at why post-training has become the critical layer between a minimum viable product and production, and how Nebius Token Factory makes it simple, scalable and practical for real applications.

# The shift to customized modelsThe shift to customized models

Since the start of the generative AI wave, application teams have been shipping products on top of base foundation models, without significant optimizations. That made sense in POCs and demos. In the real world, at scale, unit economics and latency matter.

Now, at the end of 2025, the gap between base models and production workloads is widening. Every user interaction generates data that encodes product-specific intelligence — how your users write, search, code or talk. That data is a latent optimization signal, and ignoring it means leaving performance, efficiency and differentiation on the table.

We’ve seen this shift firsthand. The most performant GenAI apps today, from code assistants serving 1,000 tokens per second to enterprise copilots, are not powered by off-the-shelf models. They’re powered by post-trained ones: distilled, spec-decoded and quantized to real user behavior. Post-training is becoming an essential deployment step.

The challenge is that post-training isn’t simple. Each technique — LoRA, quantization, RFT, speculative decoding — carries its own orchestration logic, deep domain expertise and hardware quirks. Doing it well used to mean hiring a team of senior ML engineers and running idle GPU clusters.

The post-training roadmap by Nebius Token Factory changes that.

Today, we’re introducing our roadmap for a new service that lets teams move from raw production data to optimized, deployed models in a single, integrated workflow — without building their own training infrastructure.

### Data ingestion and curationData ingestion and curation

Post-training enables you to utilize Token Factory production data–chat transcripts, logs and feedback streams for training. This turns every user interaction into a continuous optimization signal for your model.

### Multi-node supervised fine-tuningMulti-node supervised fine-tuning

Post-training lets users launch multi-node supervised fine-tuning (SFT) jobs powered by Nebius Papyrax. Sharding, parallelism, scheduling and checkpointing are automatically handled, ensuring maximum throughput, stability and reproducibility without effort.

### Reinforcement fine-tuning (Co-design)Reinforcement fine-tuning (Co-design)

Post-training also supports reinforcement fine-tuning (RFT), aligning model behavior with product-specific goals such as helpfulness, tone and safety. Explicit and implicit user feedback is converted into reward models that drive policy optimization on the same cluster.

Request private beta access

### Speculative decodingSpeculative decoding

After fine-tuning, models can be optimized for inference speed through speculative decoding and other performance-enhancing techniques. Post-training provides API access to the same speculative decoding pipeline that powers our DeepSeek v3 and other high-performance endpoints — consistently ranking among the fastest non-ASIC inference endpoints in production.

Request private beta access

### Deployment and continuous optimizationDeployment and continuous optimization

Built on Nebius Papyrax, our multi-node distributed training framework, post-training unifies compression, fine-tuning and deployment into a single composable system. It gives teams a push-button path to transform any foundation model into a lean, customized, production-ready asset — in hours, not weeks.

This is the infrastructure for the next phase of generative AI, where efficiency, personalization and speed are not trade-offs but standard practice.

# Nebius PapyraxNebius Papyrax

The rapid growth of large-scale language models has placed increasing demands on training infrastructure: more GPUs, higher network bandwidth, more efficient sharding strategies and resilient orchestration. At Nebius Token Factory, our in-house AI R&D team has designed and engineered large-scale training systems to address exactly these challenges. It includes JAX/XLA-based model code, fully deterministic execution, GPU-first metrics, a modular architecture with sharding-agnostic tensor axis labelling, out-of-the-box support for data, tensor, context and expert parallelism, custom kernels for I/O-aware attention and mixture of experts, and robust checkpointing and cluster monitoring.

Building on that foundation, we now introduce Nebius Papyrax, a multi-node training framework designed to push LLM training throughput, resilience and flexibility further. Papyrax is built for organizations that must scale beyond a single node, mix sharding strategies, tolerate hardware failures and optimize resource usage across a heterogeneous cluster. It emphasizes:

Scalability across nodes — Enables system growth from tens to thousands of GPUs (and beyond), without rewriting model code.

Sharding flexibility — Decouples model logic from physical mapping: tensor axes carry logical labels and the framework maps those logical axes to device-mesh dimensions via configuration.

Resilience and efficiency — Checkpointing, job scheduling, monitoring and self-healing minimize wasted GPU hours.

Modular, hardware-aware kernels — Optimized routines for attention, matrix operations and token routing that exploit modern GPU features and interconnects.

Platform-agnostic execution — While leveraging high-end interconnects and storage back-ends, the framework exposes abstractions so model developers remain focused on architecture, not plumbing.

Nebius Papyrax empowers ML research and production teams to focus on model design and training strategy, while the framework handles the distributed systems complexity underneath.

Our modular parallelism and asynchronous scheduling architecture allow it to maintain linear scaling and predictable latency in scenarios where other frameworks break or stall. These results establish Papyrax as a state-of-the-art distributed post-training framework for LLMs at production scale.

We will follow up with the comprehensive benchmark in the coming weeks.

# Discussion and design implicationsDiscussion and design implications

Internal benchmark data demonstrates clear, consistent performance advantages of Nebius Papyrax against other open-source frameworks, particularly in distributed LoRA fine-tuning workloads. These improvements are not incidental — they arise from deliberate architectural choices aimed at minimizing communication overhead, maximizing hardware utilization and decoupling model logic from topology-specific configurations.

### Logical sharding abstractionLogical sharding abstraction

At the core of Papyrax lies its sharding-agnostic tensor labeling system. Instead of hard-coding data, tensor or pipeline parallel axes, Papyrax associates logical names with tensor dimensions. The runtime then dynamically maps these logical axes onto the physical device mesh based on cluster topology and configuration.

This design achieves Zero-rewrite scaling: models can be trained on 8 or 1024 GPUs, without modifying code.

This abstraction is the foundation of Papyrax’s flexible scaling, allowing throughput to scale almost linearly while keeping memory use predictable.

### Communication–computation overlapCommunication–computation overlap

Papyrax’s scheduler employs fine-grained overlapping of computation, communication and checkpointing. Instead of treating all-reduce and pipeline synchronization as blocking barriers, it partitions and streams gradients and activations asynchronously.

The result:

- 

Higher effective GPU utilization: The framework minimizes idle GPU cycles during synchronization.

- 

Predictable scaling: Synchronization overhead grows sub-linearly with node count.

### Resilient multi-node executionResilient multi-node execution

Papyrax supports an asynchronous checkpointing mechanism that avoids I/O blocking on the critical path. This architecture preserves training momentum and significantly reduces Mean Time to Recovery (MTTR) during node outages. Our lightning-fast storage allows us to restart quickly in case of failed runs.

This improves:

- 

Training uptime and resource efficiency, especially in multi-day LLM runs.

- 

Cost-per-token trained, since partial progress is preserved.

### Hardware-aware kernels and I/O optimizationHardware-aware kernels and I/O optimization

Papyrax integrates custom fused kernels for attention and matrix ops tuned for Tensor Cores, combined with I/O-aware scheduling that pre-fetches data batches into GPU memory while compute kernels run. This design minimizes PCIe bottlenecks and achieves the 40–50 GB lower memory footprint observed in benchmarks.

### Unified multi-precision and quantization supportUnified multi-precision and quantization support

While competitors rely on ad hoc 4-bit quantization for large contexts, Papyrax’s internal pipeline supports mixed-precision computation (BF16 and FP32) with automatic scaling, ensuring higher numerical stability and eliminating the need for manual configuration.

Key takeaways

- 

Throughput leadership: 1.5–2.5× faster than open-source frameworks across workloads.

- 

Scalable reliability: Zero OOM, or job restarts with up to 131k context on multi-node clusters.

- 

Future extensibility: Low precision (FP8, NVFP4), quantization-aware training (QAT), pipeline parallelism.

### Customer spotlight: How Cosine delivers enterprise-grade security with state-of-the-art performanceCustomer spotlight: How Cosine delivers enterprise-grade security with state-of-the-art performance

Cosine is an autonomous AI coding agent built for real-world engineering: complex codebases, multi-step tasks and full end-to-end execution.

As demand for AI coding agents surges, Cosine faced a critical hurdle: large enterprises required on-premise deployments for security, but traditional open-source models couldn’t match the reasoning capabilities of closed-source giants.

By leveraging Nebius Token Factory, Cosine successfully bridged the gap between strict data privacy and high-performance model reasoning.

The challenge: The closed-source wall

Global financial institutions and large enterprises needed Cosine’s coding agents, but deemed closed-source foundational LLMs off-limits due to data sovereignty and security risks. Cosine needed a way to elevate open-source models to meet these rigorous standards.

The solution: Targeted post-training

Using the Nebius platform, Cosine executed large-scale post-training workflows on Llama 3.3 70B, GPT-OSS-120B. This involved a rigorous combination of:

- 

Supervised fine-tuning to adapt the model to specific coding environments.

- 

Reinforcement learning from code execution to improve the model’s logic and reliability dramatically.

The impact: Parity with proprietary models

The results of this post-training were transformative. Cosine successfully deployed their agent to one of Europe’s largest financial institutions, achieving performance on software engineering tasks equivalent to OpenAI’s o3 model, all within a secure, private environment.

“We have been able to service this need by post-training the latest open-source LLMs with Nebius Token Factory… allowing us to improve the SWE ability of open-source models to a level where they drive significant value to enterprise customers.”

— Cosine

### Custom speculator training API in private betaCustom speculator training API in private beta

As part of the Papyrax post-training platform release, we’re opening access to our Custom Speculator Training API, which lets teams train and integrate their own speculative decoding models.

This unlocks low-latency inference pipelines tailored to your specific workloads, giving you fine-grained control over speed, accuracy and cost. Whether you’re optimizing a code assistant, search engine or enterprise copilot, the API provides a programmable interface to build custom draft models that push throughput even further.

We’re inviting a limited number of teams to join the private beta. If you want early access to build state of the art draft models.

Apply for the beta

### White-glove reinforcement fine-tuning programWhite-glove reinforcement fine-tuning program

We are pleased to announce a white-glove reinforcement fine-tuning program, designed for teams that need more than standard alignment. This is a hands-on, researcher-led partnership where Nebius AI researchers work directly with your product and engineering teams to build custom reward models, architect RFT pipelines and drive end-to-end behavioral tuning on dedicated Papyrax infrastructure.

This limited program is built for organizations aiming to push beyond generic copilots. Companies that need systems that reflect their workflows, their safety constraints and their distinct product voice. If your north star is a model that behaves like it was trained in-house from day one, this is the fastest way to get there.

Participation is intentionally limited to ensure deep collaboration and measurable outcomes.

Apply for the beta

# ClosingClosing

Post-training by Nebius Token Factory is designed for teams that are done playing with demos and ready to run real systems: models that are faster, more aligned, cheaper to serve and deeply adapted to their domain.

If you’re building AI products on open-source LLMs and want to own both the model and the outcome, now is the time to move beyond base checkpoints.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Nebius team

## See also

### 

NVIDIA Nemotron Nano 2 VL in Nebius AI Studio: powering agentic multimodal AI

We’re pleased to announce that Nebius AI Studio now hosts NVIDIA Nemotron Nano 2 VL, a compact, production-ready multimodal reasoning model engineered for real-world document intelligence and video understanding.

October 28, 2025
3 mins to read

### 

Build a multi-agent AI customer support system

This guide walks you through building a production-ready, multi-agent AI system by using the Google ADK and A2A, powered by Nebius AI Studio models. With sentiment detection, RAG-powered answers and escalation handling, you can automate customer queries end-to-end.

September 24, 2025
13 mins to read

### 

Leveraging high-speed, rack-scale GPU interconnect with NVIDIA GB200 NVL72

Let’s explore one of the key features that makes the new NVIDIA GB200 NVL72 stand out: the fifth generation NVIDIA NVLink™ scale-up fabric. We’ll discuss how it redefines infrastructure by moving beyond the traditional 8-GPU NVLink. You’ll see a practical example of how to take advantage of this capability. Finally, we’ll examine a real-world use case: pre-training the Nemotron-4 340B LLM.

October 23, 2025
10 mins to read

Sign in to save this post
Sign In
