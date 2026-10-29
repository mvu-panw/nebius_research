# NVIDIA HGX H200 on Nebius AI Cloud — High-Memory Hopper GPU Infrastructure

Source: https://nebius.com/compute/h200

Skip to main content

## What makes HGX H200 on Nebius different

### GPU performance, optimized in-house

Our GPU clusters are optimized across every layer of the stack — from in-house designed servers to a software layer validated against NVIDIA benchmarks — so your AI workloads run at the highest achievable performance.

### AI without operational overhead

We take care of the infrastructure, at any scale. Run containerized experiments with Serverless Jobs or deploy large-scale inference clusters on Slurm, without touching drivers, networking, or cluster configuration.

### Security and reliability by design

Every Nebius cluster comes with auto-healing that detects and recovers from hardware failures with minimum possible interruption. Our platform is also built on industry security and compliance standards, so your data and workloads always stay secure.

## Introducing Live GPU Spot Prices

Access GPU capacity for interruptible workloads at live market-driven prices by comparing available models and regions. Set your maximum price or follow the market.
Get startedAbout Preemptible VMs

## What teams run on NVIDIA HGX H200

## Large model inference

Serve large language models at full precision without quantization trade-offs. With 141 GB of HBM3e memory per GPU, HGX H200 fits 70B to 405B parameter models in a single node, enabling high-concurrency inference with long context windows.

## LLM training and fine-tuning

Train and fine-tune large language models without the memory constraints that force teams into reduced-precision workflows. HGX H200 memory capacity handles larger models and longer sequences in both pre-training and fine-tuning jobs, making it a reliable platform across the full training lifecycle.

## Offline and batch inference

Process large volumes of AI requests in batch mode, where latency per request matters less than total throughput and cost. With 141 GB of memory per GPU, HGX H200 runs full-precision 70B–405B models on batch workloads without quantization, making it a strong fit for academic research, drug discovery, and life sciences applications that process large datasets offline.

## NVIDIA HGX H200 specifications

Specification

HGX H200

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

141 GB | 1.1 TB HBM3e

Memory bandwidth

4.8 TB/s per GPU

NVIDIA NVLink

Fourth generation

NVLink GPU-to-GPU bandwidth

900 GB/s

Total NVLink bandwidth

7.2 TB/s

Networking bandwidth

0.4 Tb/s

Source: nvidia.com/en-us/data-center/h200.

## Supercomputer-class performance for your workloads

NVIDIA HGX H200 systems on Nebius are connected via NVIDIA Quantum-2 InfiniBand at 400 Gb/s per GPU. Having this high-speed interconnect enables massive parallel computation across thousands of GPUs, utilizing the full potential of NVIDIA accelerated compute, so your distributed workloads scale without becoming bottlenecked by the network fabric.

## 

NVIDIA Exemplar Cloud Validation

Nebius is a Reference Platform NVIDIA Cloud Partner and holds NVIDIA Exemplar Cloud status across multiple GPU generations — from NVIDIA H200 to NVIDIA GB300 NVL72. For the HGX H200 specifically, Nebius achieved NVIDIA Exemplar Cloud validation for training workloads, demonstrating real-world performance against NVIDIA’s benchmarking standards on this platform.
Read the blog

## Frequently Asked Questions

What is the NVIDIA HGX H200?

The NVIDIA HGX H200 is an 8-GPU server platform built on NVIDIA’s Hopper architecture. It is the first GPU platform with HBM3e memory, delivering 141 GB per GPU and 4.8 TB/s of memory bandwidth, designed for large model inference and memory-intensive AI workloads.

What is the key difference between HGX H200 and HGX H100?

HGX H200 is built on the same Hopper compute die as H100 but introduces HBM3e memory, increasing per-GPU memory from 80 GB to 141 GB and memory bandwidth from 3.35 TB/s to 4.8 TB/s. This makes H200 significantly better suited for workloads where memory capacity and bandwidth are the primary constraint, such as large model inference and long-context workloads.

What is the key difference between HGX H200 and HGX B200?

HGX H200 is a Hopper-generation platform with 141 GB of HBM3e memory per GPU, optimized for memory-bound inference and large model serving. HGX B200 introduces the Blackwell architecture with FP4 Tensor Cores, second-generation Transformer Engine, and nearly double the per-node memory, making it the stronger platform for teams looking to move to the latest generation for training or high-throughput inference at scale.

Is HGX H200 available in self-service?

Yes. HGX H200 is available as self-service GPU instances and you can get started without speaking to sales.

What orchestration options are available?

Nebius provides a managed Kubernetes environment as the default. You can also deploy Slurm clusters through Managed Soperator without any manual cluster setup. Ray / Anyscale, SkyPilot, and other scheduling frameworks that run over Kubernetes are all supported.

How do I get access to NVIDIA HGX H200 on Nebius?

You can get started directly through self-service: launch GPU instances, run containerized workloads via Serverless, or deploy a managed Slurm cluster, all without contacting sales. If you need large-scale reserved capacity or want to discuss your specific requirements, fill in the contact form and our team will get back to you.

## Get started with NVIDIA HGX H200 on Nebius

Launch your first instance in minutes or talk to our team to find the right setup for your workload.
Get startedContact sales
