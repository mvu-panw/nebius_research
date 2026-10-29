# NVIDIA HGX H100 on Nebius AI Cloud — Cost-Efficient Hopper GPU Infrastructure

Source: https://nebius.com/compute/h100

Skip to main content

## What makes HGX H100 on Nebius different

### GPU performance, optimized in-house

Our GPU clusters are optimized across every layer of the stack — from in-house designed servers to a software layer validated against NVIDIA benchmarks — so your AI workloads run at the highest achievable performance.

### AI without operational overhead

We take care of the infrastructure, at any scale. Run containerized experiments with Serverless Jobs or deploy large-scale training clusters on Slurm, without touching drivers, networking, or cluster configuration.

### Security and reliability by design

Every Nebius cluster comes with auto-healing that detects and recovers from hardware failures with minimum possible interruption. Our platform is also built on industry security and compliance standards, so your data and workloads always stay secure.

## Introducing Live GPU Spot Prices

Access GPU capacity for interruptible workloads at live market-driven prices by comparing available models and regions. Set your maximum price or follow the market.
Get startedAbout Preemptible VMs

## What teams run on NVIDIA HGX H100

## Cost-efficient LLM inference

Serve large language models at scale without overpaying for compute. HGX H100 delivers strong FP8 inference throughput at a lower cost per GPU-hour than newer generations, making it the practical choice for teams where cost efficiency is a priority alongside performance.

## LLM training for dense models

Train dense language models up to 70B parameters on a platform with a proven track record at cluster scale. HGX H100 is a reliable choice for non-MoE architectures, with years of optimized training recipes and well-understood behavior across large multi-node configurations.

## Offline and batch inference

Run high-volume AI inference in batch mode where per-request latency is less critical than overall throughput and cost per result. HGX H100 cost efficiency makes it well-suited for offline workloads in academic research, life sciences, and drug discovery, where large datasets are processed in scheduled jobs rather than real-time pipelines.

## NVIDIA HGX H100 specifications

Specification

HGX H100

Form factor

8× NVIDIA Hopper GPUs

FP8 Tensor Core (sparse)

32 PFLOPS

FP16/BF16 Tensor Core (sparse)

16 PFLOPS

TF32 Tensor Core (sparse)

8 PFLOPS

FP32

67 TFLOPS

FP64/FP64 Tensor Core

67 TFLOPS

INT8 Tensor Core (sparse)

32 POPS

GPU Memory (per GPU | total)

80 GB | 640 GB HBM3

Memory bandwidth

3.35 TB/s per GPU

NVIDIA NVLink™

Fourth generation

NVLink GPU-to-GPU bandwidth

900 GB/s

Total NVLink bandwidth

7.2 TB/s

Networking bandwidth

0.4 Tb/s

Source: nvidia.com/en-us/data-center/h100.

## Supercomputer-class performance for your workloads

NVIDIA HGX H100 systems on Nebius are connected via NVIDIA Quantum-2 InfiniBand at 400 Gb/s per GPU. Having this high-speed interconnect enables massive parallel computation across thousands of GPUs, utilizing the full potential of NVIDIA accelerated compute, so your distributed workloads scale without becoming bottlenecked by the network fabric.

## 

NVIDIA Exemplar Cloud Validation

Nebius is a Reference Platform NVIDIA Cloud Partner and holds NVIDIA Exemplar Cloud validation across multiple GPU generations — from NVIDIA H200 to NVIDIA GB300 NVL72. Exemplar Cloud is awarded to providers that demonstrate real-world training performance against NVIDIA’s benchmarking standards, not just peak specifications.
Read the blog

## Frequently Asked Questions

What is the NVIDIA HGX H100?

The NVIDIA HGX H100 is an 8-GPU server platform built on NVIDIA’s Hopper architecture. It delivers 80 GB of HBM3 memory per GPU, fourth-generation NVLink, and FP8 Tensor Core support, a proven and widely adopted platform for AI training, fine-tuning, and inference workloads.

What is the key difference between HGX H100 and HGX H200?

HGX H100 and H200 share the same Hopper compute die, so their AI compute throughput is identical. The key difference is memory: H200 doubles per-GPU memory to 141 GB using HBM3e, with higher memory bandwidth. For workloads that fit within 80 GB per GPU, H100 delivers the same compute performance at a lower cost per GPU.

What is the key difference between HGX H100 and HGX B200?

HGX H100 is the cost-efficient Hopper-generation platform with a mature and deeply optimized software ecosystem. HGX B200 introduces the Blackwell architecture with FP4 Tensor Cores, second-generation Transformer Engine, and significantly higher memory capacity and compute throughput. B200 is the right choice for teams pushing the limits of model scale or throughput; H100 is the right choice for teams prioritizing cost efficiency and ecosystem maturity.

Is HGX H100 available in self-service?

Yes. HGX H100 is available as self-service GPU instances and you can get started without speaking to sales.

What orchestration options are available?

Nebius provides a managed Kubernetes environment as the default. You can also deploy Slurm clusters through Managed Soperator without any manual cluster setup. Ray / Anyscale, SkyPilot, and other scheduling frameworks that run over Kubernetes are all supported.

How do I get access to NVIDIA HGX H100 on Nebius?

You can get started directly through self-service: launch GPU instances, run containerized workloads via Serverless, or deploy a managed Slurm cluster, all without contacting sales. If you need large-scale reserved capacity or want to discuss your specific requirements, fill in the contact form and our team will get back to you.

## Get started with NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

Launch your first instance in minutes or talk to our team to find the right setup for your workload.
Get startedContact sales
