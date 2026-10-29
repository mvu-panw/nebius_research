# Nebius demonstrates industry-leading AI training performance in latest MLPerf® results

Source: https://nebius.com/blog/posts/industry-leading-ai-training-performance-in-mlperf

Skip to main content

Today, we’re thrilled to announce our first submission of MLPerf® Training v5.0 results. As a peer-reviewed industry benchmark suite, MLPerf® Training by MLCommons® is one of the most trustworthy sources of data about AI cloud performance in the industry.

We achieved impressive results by training a Llama 3.1 405B model on 512 and 1,024 NVIDIA Hopper GPU clusters interconnected with NVIDIA Quantum-2 InfiniBand networking, which demonstrates our capabilities to deliver predictable training performance at large scale.

# About MLPerf Training benchmarksAbout MLPerf Training benchmarks

For many AI and ML professionals today, AI cloud is an obvious and inseparable part of their production pipelines. At the same time, it remains a very complex and sophisticated system, where performance and reliability are hard to measure and compare. This creates a big challenge for potential customers of AI clouds when it comes to comparing options and making decisions about where to invest millions of dollars.

The MLPerf® benchmarks address this problem perfectly. Developed by industry and academic engineers, and open to community reviews, MLPerf® benchmarks create a credible measurement system that reveals ML model performance in realistic deployment scenarios across various workloads.

“We appreciate how MLCommons serves as a reliable compass for our industry, offering a clear framework to measure AI infrastructure performance. It helps us demonstrate our capabilities as a cloud provider, while also underscoring the rapid pace required to remain competitive in today’s AI landscape.”

— Narek Tatevosyan, Director of Product Management at Nebius

# Large-scale training of the 405B modelLarge-scale training of the 405B model

We submitted results for training the Llama 3.1 405B model, one of the largest and most challenging-to-train models from the latest MLPerf® Training benchmark suite. We ran this benchmark on two multi-host clusters, built on the NVIDIA Hopper architecture and interconnected with NVIDIA Quantum-2 InfiniBand networking:

- 

64-node cluster with 512 NVIDIA H200 GPUs

- 

128-node cluster with 1,024 NVIDIA H200 GPUs

Even on the verge of proliferation of NVIDIA Blackwell platforms, NVIDIA HGX™ H200 platforms are an excellent choice for distributed model training — they deliver robust performance and exceptional cost-effectiveness at scale.

“We are thrilled to welcome Nebius as a first-time MLPerf Training submitter. We are particularly impressed by their achievement of training Llama 3.1 405B — the largest open-weight model in our benchmark suite — on substantial clusters of 512 and 1,024 GPUs.”

— David Kanter, Founder and Head of MLPerf at MLCommons

Nebius serves GPU clusters, accelerated by NVIDIA, to industry-leading AI labs and continuously improves our expertise in delivering compute capacity for massive ML training. This made us confident that we would be able to demonstrate solid performance results on clusters of this scale.

# Achieving top-tier training performanceAchieving top-tier training performance

MLPerf® Training benchmarks measure training step time — the amount of time it takes to complete one training step — from loading a batch of data to updating the model’s weights. Shorter step time means more optimized compute infrastructure, which results in faster and less expensive training.

We achieved training step times of 124.5 min and 244.6 min for Llama 3.1 405B on the 128-node cluster and 64-node cluster, respectively¹.

Figure 1. Training step time decreases by 1.97x when doubling from 512 to 1,024 GPUs

These numbers demonstrate near-linear scaling of Nebius infrastructure: 1.97x increase in speed when doubling from 512 to 1,024 GPUs. Beyond excellent performance and cost-efficiency potential, this result also shows how efficiently we can scale GPU capacity when training requirements grow.

# Purpose-built AI cloudPurpose-built AI cloud

At Nebius, we know that there is no accidental success in our industry, either on the customer or vendor side. Each achievement or milestone is backed by months of rigorous research, testing and investigation.

Providing AI cloud infrastructure means that every piece of software and hardware should be optimized and precisely validated before being deployed to production clusters. Following this principle, we ensure full control over the cloud stack — from proprietary firmware and custom-designed servers to optimized compute engine and unique orchestration software.

In particular, we launched these benchmarks by using Soperator, our in-house Kubernetes operator for Slurm. This software enables AI clusters to run with a high level of resiliency and availability, while providing exceptional simplicity for ML operational teams.

As an NVIDIA Cloud Partner (NCP), we’re aligned with the latest NVIDIA technologies and reference architectures, to advance our product offering and maximize NVIDIA GPU utilization.

# Innovating for better resultsInnovating for better results

These MLPerf® Training results prove our capability to deliver a predictable training experience for large foundational models, at scale.

However, having promising benchmark numbers today is not enough. Since the AI landscape evolves rapidly, we have no choice but to stay committed to the continuous improvement of every piece of our cloud infrastructure.

Feel free to contact us if you need reliable, high-performance infrastructure for large-scale, distributed training.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- About MLPerf Training benchmarks

- Large-scale training of the 405B model

- Achieving top-tier training performance

- Purpose-built AI cloud

- Innovating for better results

## See also

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

We’re introducing the 300 MW New Jersey region and expanding to Iceland

We’re thrilled to announce a major upgrade to our US-based compute capacity. To bring it to life, we’ve joined forces with DataOne, an AI hosting infrastructure company, to ensure that the first phase of the New Jersey facility goes live this summer. We’re also launching a colocation facility in Iceland with Verne, a provider of sustainably powered data centers across the Nordics, and expect it to go live this month.

March 5, 2025
2 mins to read

### 

SWE-rebench: A continuously updated benchmark for SWE LLMs

Our AI R&D team presents SWE-rebench, a new benchmark for evaluating agentic LLMs on a continuously updated and decontaminated set of real-world software engineering tasks mined from real GitHub repositories. Our goal with this benchmark is to make evaluation of software engineering LLMs more transparent, reproducible and focused on core model capabilities.

May 14, 2025
1 min to read

¹ Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information.

Sign in to save this post
Sign In
