# Scaling videogen with Baseten Inference Stack on Nebius

Source: https://nebius.com/blog/posts/scaling-videogen-with-baseten-inference-stack-on-nebius

Skip to main content

Turning a prompt into a video might feel easy for users, but behind the scenes, generative video workloads are notoriously demanding. They run longer than other types of data, stress GPU memory, and magnify the impact of latency. In this post, we’ll explain why generating videos at scale is a systems engineering challenge and walk you through the infrastructure and runtime optimizations that make production-grade text-to-video possible on Nebius AI Cloud, powered by the Baseten Inference Stack.

Since September 2025, Baseten has been running on Nebius across our cloud regions in the US, Finland and France. We’ll cover how Baseten’s optimized runtime (including topology-aware parallelism) and orchestration features operate on our GPU clusters, and how our elastic provisioning and intelligent autoscaling keep even the most demanding workloads running smoothly. We’ll also share the metrics that matter, from p90/p99 latency to utilization, and close with how you can test it yourself on cutting-edge accelerators.

# Why video generation pushes infrastructure to the limitWhy video generation pushes infrastructure to the limit

Text-to-video isn’t just “one more modality” of Generative AI. It runs longer, consumes more memory, and demands higher stability than text or image generation. A single request can take up an entire node. Latency shifts are visible in output quality, and scaling becomes difficult when workloads spike unexpectedly.

The only way to meet these requirements in production is to treat performance, reliability, and cost as a single system. That’s exactly what Nebius and Baseten deliver together: Nebius provides the AI cloud foundation with dedicated GPU clusters and elastic scale, and Baseten layers on an inference stack that makes that power predictable and efficient for day-to-day workloads.

# Optimizing performance at the model runtime layerOptimizing performance at the model runtime layer

Video generation efficiency depends heavily on the model runtime. Baseten’s stack includes:

- Modality-specific kernels that understand image and video execution patterns.

- Kernel fusion to collapse smaller operations into faster execution paths.

- Attention kernels tuned for balancing quantization with video output quality.

- Asynchronous compute to keep GPUs busy instead of idle between launches.

This runtime also prioritizes requests intelligently. Long-running generations don’t block shorter, latency-sensitive jobs. When models span multiple devices, topology-aware parallelism ensures scale-out across nodes with minimal communication overhead. These techniques lead to steady step times and higher effective frames per GPU second.

# Baseten Cloud on Nebius infrastructure: The backbone of scalable text-to-videoBaseten Cloud on Nebius infrastructure: The backbone of scalable text-to-video

Running the Baseten Inference Stack on Nebius AI clusters gives generative video workloads an AI-first foundation tuned for production. It integrates cleanly into existing pipelines with minimal rewiring, supported by:

- Dedicated GPU clusters that deliver supercomputer-class performance with the flexibility of cloud, purpose-built for AI-native workloads.

- Multi-zone availability across Europe and the US, enabling global scalability without hitting resource limits.

- Reliable networking with high-bandwidth and low-latency design, preventing infrastructure bottlenecks.

- Elastic provisioning to dynamically match GPU resources to real-time demand, optimizing for both cost-efficiency and performance.

- Deep AI expertise from in-house server design to 24/7 solution architects, continuously enhancing every aspect of compute.

At every step, Nebius’ vertically-integrated infrastructure — from non-virtualized GPUs to InfiniBand networking — ensures that compute is not just available, but consistently performant.

# Where Nebius and Baseten meet: ensuring production-grade video generationWhere Nebius and Baseten meet: ensuring production-grade video generation

Raw speed isn’t enough — performance has to be consistent. Baseten contributes the orchestration logic: routing requests to model replicas with cached elements to reduce time-to-output, balancing traffic across regions, and supporting synchronous, asynchronous, and streaming predictions over HTTPS, WebSocket, and gRPC. That flexibility lets engineers choose the right protocol for the job: batching large runs, streaming updates from long-running generations and others.

Equally important is how performance gets measured. Teams track end-to-end latency against p90/p99 targets to ensure a consistent user experience, per-step denoising times to spot performance regressions early, and GPU utilization to balance throughput with cost. Baseten surfaces these signals in real time, while Nebius provides the stable infrastructure baseline — dedicated, interconnected GPU clusters and multi-zone availability, so engineers can trust the numbers reflect workload behavior.

Together, Baseten and Nebius enable:

- SLA-aware autoscaling with fast cold starts to ensure that even when demand spikes, new replicas serve traffic quickly and contribute within SLOs.

- Independent component scaling to prevent multi-stage pipelines from bottlenecking on a single step.

- Continuous reliability via active-active region deployments and cross-cloud resilience.

For teams running production-grade video generation, this means infrastructure that scales and adapts dynamically, keeping performance consistent even when demand surges.

### Why this pairing worksWhy this pairing works

Nebius and Baseten are built for different layers of the same challenge. Nebius provides the AI cloud foundation — GPU clusters with the performance, networking, and elasticity to handle demanding generative video workloads. Baseten adds the inference stack that turns that infrastructure into a service: optimized runtimes, intelligent orchestration, and the ability to observe and adapt in real time.

Together, they solve what holds teams back: unpredictable latency, poor utilization, and operational overhead.

# Getting startedGetting started

Run a free PoC on Nebius powered by modern AI clusters — a strong fit for generative video workloads that demand long runtimes, large memory, and consistent throughput. If you’re moving from a hyperscaler, you can save 15% while gaining predictable performance at scale.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- 

Why video generation pushes infrastructure to the limit

- 

Optimizing performance at the model runtime layer

- 

Baseten Cloud on Nebius infrastructure: The backbone of scalable text-to-video

- 

Where Nebius and Baseten meet: ensuring production-grade video generation

- Why this pairing works

- 

Getting started

## See also

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

Watch the talks: Videos from Nebius AI Cloud Unveiled meetup

We wrapped up our first series of technical meetups with stops in Paris, London and San Francisco — each time providing a deep dive into our cloud. Here, you can watch all the talks from the first event in the series.

April 8, 2025
4 mins to read

### 

From genome analysis to quantum chemistry: Nebius powers the next generation of biotech research with NVIDIA

As part of NVIDIA GTC Paris at VivaTech, Nebius has announced deeper integration of the NVIDIA AI Enterprise software suite. This includes NVIDIA BioNeMo, a collection of tools, applications, generative AI solutions, and pre-trained microservices (NVIDIA NIM) designed squarely for the biopharma sector.

June 25, 2025
5 mins to read

Sign in to save this post
Sign In
