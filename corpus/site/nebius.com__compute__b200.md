# NVIDIA HGX B200 on Nebius AI Cloud — Blackwell GPU Infrastructure

Source: https://nebius.com/compute/b200

Skip to main content

## What makes HGX B200 on Nebius different

### GPU performance, optimized in-house

Our GPU clusters are optimized across every layer of the stack — from in-house designed servers to a software layer validated against NVIDIA benchmarks — so your AI workloads run at the highest achievable performance.

### AI without operational overhead

We take care of the infrastructure, at any scale. Run containerized experiments with Serverless Jobs or deploy large-scale training clusters on Slurm, without touching drivers, networking, or cluster configuration.

### Security and reliability by design

Every Nebius cluster comes with auto-healing that detects and recovers from hardware failures with minimum possible interruption. Our platform is also built on industry security and compliance standards, so your data and workloads always stay secure.

## Introducing Live GPU Spot Prices

Access GPU capacity for interruptible workloads at live market-driven prices by comparing available models and regions. Set your maximum price or follow the market.
Get startedAbout Preemptible VMs

## What teams run on NVIDIA HGX B200

## Large-scale LLM training

Train frontier language models on a platform designed for the demands of large-scale, memory-intensive workloads. HGX B200 combines 1.4 TB of HBM3e memory per node with fifth-generation NVIDIA NVLink™, making it a capable platform for dense model training at scale.

## MoE model training and inference

Build and train Mixture-of-Experts models efficiently, where the combination of high memory capacity and fast intra-node interconnect directly improves utilization across expert layers. HGX B200 handles both the training and serving stages of MoE architectures without memory constraints.

## High-throughput inference

Serve production AI workloads at scale with the throughput that modern inference demands. HGX B200’s FP4 Tensor Cores and large memory footprint allow teams to run large models at full precision with room for long context lengths and high request concurrency.

## NVIDIA HGX B200 specifications

Specification

HGX B200

Form factor

8× NVIDIA Blackwell GPUs

FP4 Tensor Core (sparse | dense)

144 PFLOPS | 72 PFLOPS

FP8/FP6 Tensor Core (sparse)

72 PFLOPS

INT8 Tensor Core (sparse)

72 POPS

FP16/BF16 Tensor Core (sparse)

36 PFLOPS

TF32 Tensor Core (sparse)

18 PFLOPS

FP32

600 TFLOPS

FP64/FP64 Tensor Core

296 TFLOPS

Total memory

1.4 TB HBM3e

NVIDIA NVLink

Fifth generation

NVIDIA NVLink Switch

NVLink 5 Switch

NVLink GPU-to-GPU bandwidth

1.8 TB/s

Total NVLink bandwidth

14.4 TB/s

Networking bandwidth

0.8 Tb/s

Source: nvidia.com/en-us/data-center/hgx — NVIDIA Blackwell tab.

## Supercomputer-class performance for your workloads

NVIDIA HGX B200 systems on Nebius are connected via NVIDIA Quantum-2 InfiniBand at 400 Gb/s per GPU. Having this high-speed interconnect enables massive parallel computation across thousands of GPUs, utilizing the full potential of NVIDIA accelerated compute, so your distributed workloads scale without becoming bottlenecked by the network fabric.

## 

NVIDIA Exemplar Cloud Validation

Nebius is a Reference Platform NVIDIA Cloud Partner and holds NVIDIA Exemplar Cloud validation across multiple GPU generations — from NVIDIA H200 to NVIDIA GB300 NVL72. Exemplar Cloud is awarded to providers that demonstrate real-world training performance against NVIDIA’s benchmarking standards, not just peak specifications.
Read the blog

## Frequently Asked Questions

What is the NVIDIA HGX B200?

The NVIDIA HGX B200 is an 8-GPU server platform built on NVIDIA Blackwell architecture. It delivers 1.4 TB of HBM3e memory per node, fifth-generation NVLink interconnects, and FP4 Tensor Core support, designed for large-scale AI training and high-throughput inference workloads.

What is the key difference between HGX B200 and NVIDIA HGX H200?

HGX B200 introduces the Blackwell architecture with second-generation Transformer Engine and FP4 precision support, delivering significantly higher AI compute throughput than H200. It also nearly doubles the per-node memory capacity, making it the stronger platform for teams running large-scale training or serving workloads that benefit from Blackwell’s compute and memory improvements.

What is the key difference between HGX B200 and HGX B300?

HGX B200 is built on the Blackwell architecture and is a well-balanced platform for large-scale training and inference across dense and MoE model architectures. For teams whose workloads fit within its memory and compute profile, it delivers strong performance at a more accessible entry point than Blackwell Ultra systems.

Is HGX B200 available in self-service?

Yes. HGX B200 is available as self-service GPU instances and you can get started without speaking to sales.

What orchestration options are available?

Nebius provides a managed Kubernetes environment as the default. You can also deploy Slurm clusters through Managed Soperator without any manual cluster setup. Ray / Anyscale, SkyPilot, and other scheduling frameworks that run over Kubernetes are all supported.

How do I get access to NVIDIA HGX B200 on Nebius?

You can get started directly through self-service: launch GPU instances, run containerized workloads via Serverless, or deploy a managed Slurm cluster, all without contacting sales. If you need large-scale reserved capacity or want to discuss your specific requirements, fill in the contact form and our team will get back to you.

## Get started with NVIDIA HGX B200 on Nebius

Launch your first instance in minutes or talk to our team to find the right setup for your workload.
Get startedContact sales
