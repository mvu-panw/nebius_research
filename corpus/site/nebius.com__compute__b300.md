# NVIDIA HGX B300 on Nebius AI Cloud — Blackwell Ultra GPU Infrastructure

Source: https://nebius.com/compute/b300

Skip to main content

## What makes HGX B300 on Nebius different

### GPU performance, optimized in-house

Our GPU clusters are optimized across every layer of the stack, from in-house designed servers to a software layer validated against NVIDIA benchmarks, so your AI workloads run at the highest achievable performance.

### AI without operational overhead

We take care of the infrastructure, at any scale. Run containerized experiments with Serverless Jobs or deploy large-scale training clusters on Slurm, without touching drivers, networking, or cluster configuration.

### Security and reliability by design

Every Nebius cluster comes with auto-healing that detects and recovers from hardware failures with minimum possible interruption. Our platform is also built on industry security and compliance standards, so your data and workloads always stay secure.

## Introducing Live GPU Spot Prices

Access GPU capacity for interruptible workloads at live market-driven prices by comparing available models and regions. Set your maximum price or follow the market.
Get startedAbout Preemptible VMs

## What teams run on NVIDIA HGX B300

## Large-scale LLM workloads

Train, fine-tune, and serve frontier language models on a platform built for memory-intensive workloads. HGX B300 carries significantly more memory per GPU than its predecessor, enabling larger models, longer context windows, and higher concurrency at production scale.

## Multimodal AI

Build and deploy AI systems that combine text, images, audio, or video. HGX B300 architecture efficiently balances compute and memory bandwidth, making it a practical platform for developing and running next-generation multimodal models.

## AI reasoning and agentic AI

Develop and scale reasoning models and agentic systems that generate significantly more tokens per request. HGX B300 memory capacity and compute profile sustain the throughput these workloads require, without the constraints that limit smaller-memory platforms.

## NVIDIA HGX B300 specifications

Specification

HGX B300

Form factor

8× NVIDIA Blackwell Ultra GPUs

FP4 Tensor Core (sparse | dense)

144 PFLOPS | 108 PFLOPS

FP8/FP6 Tensor Core (sparse)

72 PFLOPS

INT8 Tensor Core (sparse)

307 TOPS *

FP16/BF16 Tensor Core (sparse)

36 PFLOPS

TF32 Tensor Core (sparse)

18 PFLOPS

FP32

600 TFLOPS

FP64/FP64 Tensor Core

10 TFLOPS

Total memory

2.1 TB HBM3e

Total memory bandwidth

62 TB/s

NVIDIA NVLink

Fifth generation

NVIDIA NVLink Switch

NVIDIA NVLink™ 5 Switch

NVLink GPU-to-GPU bandwidth

1.8 TB/s

Total NVLink bandwidth

14.4 TB/s

Networking bandwidth

1.6 Tb/s

Source: nvidia.com/en-us/data-center/hgx and NVIDIA Blackwell Ultra datasheet. Projected performance subject to change.

## Supercomputer-class performance for your workloads

NVIDIA HGX B300 systems on Nebius are connected via NVIDIA Quantum-X800 InfiniBand at 800 Gb/s per GPU. Having this high-speed interconnect enables massive parallel computation across thousands of GPUs, utilizing the full potential of NVIDIA accelerated compute, so your distributed workloads scale without becoming bottlenecked by the network fabric.

## 

NVIDIA Exemplar Cloud Validation

Nebius is a Reference Platform NVIDIA Cloud Partner and holds NVIDIA Exemplar Cloud validation across multiple GPU generations — from NVIDIA H200 to NVIDIA GB300 NVL72. Exemplar Cloud is awarded to providers that demonstrate real-world training performance against NVIDIA’s benchmarking standards, not just peak specifications.
Read the blog

## Frequently Asked Questions

What is the NVIDIA HGX B300?

The NVIDIA HGX B300 is an 8-GPU server platform built on NVIDIA Blackwell Ultra architecture. Each GPU carries 270 GB of HBM3e memory and fifth-generation NVLink interconnects, designed for large-scale AI training and high-throughput inference workloads.

What is the key difference between HGX B300 and HGX B200?

HGX B300 offers 60% more memory per GPU (270 GB vs 180 GB), 1.5× more dense FP4 compute, and 2× higher attention-layer performance compared to HGX B200. In practice, this means the ability to run larger models at full precision, handle longer context lengths, and serve more concurrent users without running into memory constraints.

What is the key difference between HGX B300 and GB300 NVL72?

They serve different deployment models. HGX B300 is an air-cooled 8-GPU server node that scales horizontally across multiple machines via NVIDIA Quantum-X800 InfiniBand, flexible, multi-tenant, and straightforward to deploy. GB300 NVL72 is a liquid-cooled rack-scale system that integrates 72 Blackwell Ultra GPUs and 36 NVIDIA Grace CPUs in a single enclosure, connected by NVLink 5. That tight integration makes it better suited for workloads that require the highest possible per-rack throughput and unified memory access at rack scale.

Is HGX B300 available in self-service?

Yes. HGX B300 is available as self-service GPU instances and you can get started without speaking to sales. (Note: GB300 NVL72 is currently available through the sales team only.)

What orchestration options are available?

Nebius provides a managed Kubernetes environment as the default. You can also deploy Slurm clusters through Managed Soperator without any manual cluster setup. Ray / Anyscale, SkyPilot, and other scheduling frameworks that run over Kubernetes are all supported.

How do I get access to NVIDIA HGX B300 on Nebius?

You can get started directly through self-service: launch GPU instances, run containerized workloads via Serverless, or deploy a managed Slurm cluster, all without contacting sales. If you need large-scale reserved capacity or want to discuss your specific requirements, fill in the contact form and our team will get back to you.

## Get started with NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

Launch your first instance in minutes or talk to our team to find the right setup for your workload.
Get startedContact sales
