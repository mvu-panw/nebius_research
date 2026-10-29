# NVIDIA GB300 NVL72 on Nebius AI Cloud — Rack-Scale AI Reasoning Infrastructure

Source: https://nebius.com/compute/gb300

Skip to main content

## What makes GB300 NVL72 on Nebius different

## GPU performance, optimized in-house

Our GPU clusters are optimized across every layer of the stack — from in-house designed servers to a software layer validated against NVIDIA benchmarks — so your AI workloads run at the highest achievable performance.

## AI without operational overhead

We take care of the infrastructure, at any scale. Deploy large-scale training clusters or high-throughput inference systems on Slurm or Kubernetes, without managing rack-level hardware, cooling, or network configuration.

## Security and reliability by design

Every Nebius cluster comes with auto-healing that detects and recovers from hardware failures with minimum possible interruption. Our platform is also built on industry security and compliance standards, so your data and workloads always stay secure.

## What teams run on NVIDIA GB300 NVL72

## Frontier model training

Train the largest and most complex AI models, including MoE models at frontier scale, on a platform with 37 TB of fast memory and 1,440 PFLOPS of FP4 compute per rack. GB300 NVL72 provides the memory capacity and interconnect bandwidth for model sizes and training configurations that go beyond the limits of node-level platforms.

## AI reasoning and agentic AI

Run AI reasoning and agentic workloads that require test-time scaling, where models evaluate multiple candidate responses before producing an output, demanding up to 100× more compute than traditional inference. GB300 NVL72 is purpose-built for this class of workload, with an attention engine delivering 2.5× faster attention performance compared to NVIDIA Hopper.

## Real-time inference at scale

Serve AI models at maximum throughput and efficiency. The GB300 NVL72 rack-scale architecture is optimized for high token-per-second output, with the memory capacity to hold large models and long KV caches entirely in GPU memory, enabling low-latency responses at scale without offloading.

## NVIDIA GB300 NVL72 specifications

Specification

GB300 NVL72

Form factor

Fully liquid-cooled, rack-scale system

Blackwell Ultra GPUs | NVIDIA Grace CPUs

72 | 36

CPU cores

2,592 Arm Neoverse V2 cores

Total FP4 Tensor Core (sparse | dense)

1,440 PFLOPS | 1,080 PFLOPS

Total FP8/FP6 Tensor Core (sparse)

720 PFLOPS

Total fast memory

37 TB

Total memory bandwidth

576 TB/s

Total NVLink Switch bandwidth

130 TB/s

Individual Blackwell Ultra GPU Specifications

FP4 Tensor Core per GPU (sparse | dense)

20 PFLOPS | 15 PFLOPS

FP8/FP6 Tensor Core per GPU (sparse)

10 PFLOPS

INT8 Tensor Core per GPU (sparse)

330 TOPS

FP16/BF16 Tensor Core per GPU (sparse)

5 PFLOPS

TF32 Tensor Core per GPU (sparse)

2.5 PFLOPS

FP32 per GPU

80 TFLOPS

FP64/FP64 Tensor Core per GPU

1.3 TFLOPS

GPU Memory per GPU | bandwidth

279 GB HBM3e | 8 TB/s

Interconnect

Fifth-generation NVIDIA NVLink™: 1.8 TB/s

Source: NVIDIA Blackwell Ultra datasheet. Specifications in sparse unless noted. Projected performance subject to change.

## Rack-scale architecture with a unified NVLink domain

The NVIDIA GB300 NVL72 integrates 72 Blackwell Ultra GPUs and 36 NVIDIA Grace CPUs into a single, fully liquid-cooled rack, connected by a 72-GPU unified NVIDIA NVLink domain delivering 130 TB/s of low-latency GPU communication. This architecture eliminates the inter-node communication overhead typical of multi-server clusters, enabling the entire rack to operate as a single high-bandwidth compute platform.

For workloads that span beyond a single rack, GB300 NVL72 systems on Nebius connect via NVIDIA Quantum-X800 InfiniBand at 800 Gb/s per GPU, scaling output across multiple racks while maintaining the high-speed fabric that large-scale reasoning and training workloads require.

## 

NVIDIA Exemplar Cloud Achievement

Nebius is a Reference Platform NVIDIA Cloud Partner and has achieved NVIDIA Exemplar Cloud across multiple GPU generations, from NVIDIA H200 to NVIDIA GB300 NVL72. For the GB300 NVL72 specifically, Nebius achieved NVIDIA Exemplar Cloud status for training workloads, demonstrating real-world performance against NVIDIA’s benchmarking standards on this platform.
Read the blog

## Frequently Asked Questions

What is NVIDIA GB300 NVL72?

The NVIDIA GB300 NVL72 is a fully liquid-cooled, rack-scale system built on NVIDIA Blackwell Ultra architecture. It integrates 72 Blackwell Ultra GPUs and 36 NVIDIA Grace CPUs into a single platform, connected by a 72-GPU unified NVLink domain, purpose-built for AI reasoning, frontier model training, and large-scale inference.

What is the key difference between NVIDIA GB300 NVL72 and NVIDIA HGX™ B300?

GB300 NVL72 is a rack-scale system where 72 GPUs are unified in a single NVLink domain delivering 130 TB/s of intra-rack bandwidth, enabling the entire rack to operate as one high-bandwidth compute platform. HGX B300 is an 8-GPU node that scales horizontally across servers via NVIDIA Quantum-X800 InfiniBand. GB300 NVL72 is the right choice for workloads that benefit from the tightest possible GPU integration and maximum per-rack throughput; HGX B300 is the right choice for flexible, horizontally scalable deployments.

What is the key difference between NVIDIA GB300 NVL72 and NVIDIA GB200 NVL72?

GB300 NVL72 is built on Blackwell Ultra, the next generation after Blackwell. Each Blackwell Ultra GPU offers 1.5× more HBM3e memory, 1.5× more dense FP4 compute, and 2× higher attention-layer performance compared to the Blackwell GPU in GB200 NVL72. GB300 NVL72 is purpose-built for AI reasoning workloads and delivers higher throughput per rack for the same power envelope.

Is GB300 NVL72 available in self-service?

GB300 NVL72 is available through the Nebius sales team. Given the rack-scale nature of the system, deployments are configured to your workload requirements. Contact sales to discuss capacity, configuration, and availability.

What orchestration options are available?

Nebius provides a managed Kubernetes environment as the default. You can also deploy Slurm clusters through Managed Soperator without any manual cluster setup. Ray / Anyscale, SkyPilot, and other scheduling frameworks that run over Kubernetes are all supported.

How do I get access to NVIDIA GB300 NVL72 on Nebius?

Contact the Nebius sales team to discuss your workload requirements, cluster sizing, and availability. Our team will work with you to configure the right deployment for your use case.

## Get started with NVIDIA GB300 NVL72 on Nebius

Launch your first instance in minutes or talk to our team to find the right setup for your workload.
Get startedContact sales
