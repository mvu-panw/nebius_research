# Nebius and PyTorch partner to accelerate frontier MoE training on NVIDIA Blackwell

Source: https://nebius.com/blog/posts/nebius-and-pytorch-partner-to-accelerate-frontier-moe-training-on-nvidia-blackwell

Skip to main content

In collaboration with PyTorch, Nebius helped demonstrate up to 41% faster pre-training of DeepSeek-V3 models on NVIDIA Blackwell GPUs.

As model sizes and architectures evolve, training infrastructure must keep pace. Mixture-of-Experts (MoE) models in particular introduce new challenges: large-scale distributed communication, dynamic routing across GPUs and ever-increasing compute demands.

To explore how the latest hardware and software innovations can address these challenges, Nebius and PyTorch collaborated on a set of experiments training DeepSeek-V3 models using TorchTitan on a 256-GPU NVIDIA HGX B200 cluster running in Nebius Cloud.

The results demonstrate how advances in both numerical formats and distributed communication can significantly improve large-scale model training performance.

## Up to 41% faster trainingUp to 41% faster training

The joint experiments evaluated two optimizations on top of a BF16 baseline:

- MXFP8 training via TorchAO, leveraging NVIDIA Blackwell FP8 tensor cores to accelerate performance;

- DeepEP communication, a GPU-initiated expert-parallel communication backend designed for MoE workloads.

Running on 32 nodes (256 NVIDIA HGX B200 GPUs) in Nebius Cloud, the team observed:

- +32% training throughput using DeepEP alone;

- +41% total throughput improvement when combining DeepEP with MXFP8 for grouped GEMMs.

For the DeepSeek-V3 671B model, throughput increased from 651 tokens/sec to 918 tokens/sec.

The experiments also verified that MXFP8 maintains equivalent convergence behavior to BF16, based on loss-curve validation using the 16B MoE variant.

## Infrastructure built for frontier trainingInfrastructure built for frontier training

All experiments ran on a Nebius Cloud cluster optimized for large-scale AI workloads:

- 256 NVIDIA HGX B200 GPUs across 32 nodes;

- NVIDIA NVLink / NVSwitch for high-bandwidth intra-node communication;

- NVIDIA Quantum InfiniBand networking for inter-node scale;

- Soperator, Nebius’ scheduling system combining Slurm-style semantics with Kubernetes.

Soperator continuously monitors GPU and interconnect health and automatically replaces underperforming nodes. Combined with built-in observability and automated cluster scaling, this allowed the team to focus on training optimization rather than cluster operations.

## Open and reproducibleOpen and reproducible

All experiments were performed using open-source, PyTorch-native tooling, including:

- TorchTitan for pre-training;

- TorchAO for MXFP8 mixed-precision training;

- DeepEP for expert-parallel communication.

The full training configurations and scripts are available in the Nebius ML-Cookbook repository, enabling others to reproduce the experiments on Blackwell-based clusters.

## A joint step toward faster AI trainingA joint step toward faster AI training

This collaboration highlights how hardware capabilities, open-source frameworks, AI software and optimized infrastructure must evolve together to unlock the next generation of large-scale frontier AI models.

By combining NVIDIA Blackwell GPUs, PyTorch tooling and Nebius’ AI-optimized cloud infrastructure powered by NVIDIA Blackwell GPUs, the work demonstrates a practical path to significantly improving the performance and cost-efficiency of MoE training.

For the full technical deep dive, read the PyTorch blog and check out our GitHub page.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Hooman Ramezani
Solutions Architect

Contents

- Up to 41% faster training

- Infrastructure built for frontier training

- Open and reproducible

- A joint step toward faster AI training

## See also

### 

Nebius and Eigen AI partner to accelerate frontier open-source AI inference

Nebius and Eigen AI are partnering to bring optimized frontier open-source models to Nebius Token Factory. As part of the collaboration, optimized implementations of models such as DeepSeek, GLM, GPT-OSS, Kimi, Llama, MiniMax and Qwen will be published on the platform, giving developers direct access to high-performance inference through production-ready endpoints and APIs.

March 17, 2026
8 mins to read

### 

From fragmented data to production-grade agents: Nebius, Nexla and Tripadvisor at NVIDIA GTC

Nexla and Nebius are partnering to deliver a production-ready data and agent stack that connects governed enterprise data with infrastructure built for sustained inference. In this post, we outline how this architecture enables multi-agent systems to move from fragmented data pipelines to reliable production workflows, and show it in action through a live “Inspiration to Trip” demo presented with Tripadvisor at NVIDIA GTC.

March 17, 2026
5 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
