# Prime Intellect: Distributed training and RL with NVIDIA GB200 NVL72

Source: https://nebius.com/customer-stories/prime-intellect

Skip to main content

## Long story shortLong story short

Prime Intellect partners with every major cloud provider to supply GPUs, but Nebius is their go-to cloud for flexible on-demand utilization and access to frontier hardware. Their latest PoC on NVIDIA GB200 NVL72 from Nebius delivered out-of-the-box, advanced performance.

Prime Intellect is building AI infrastructure for globally distributed pre-training and reinforcement learning. Their open-source protocol makes multi-cluster training attainable for teams ready to scale.

## ContentsContents

Infra for distributed pre-training and reinforcement learning

Nebius and Prime Intellect

Industry-leading reliability and GPU utilization

PoC with NVIDIA Grace Blackwell architecture

Upgrading to NVIDIA GB200 NVL72

Choosing the optimal training precision

New opportunities powered by frontier hardware

## Infra for distributed pre-training and reinforcement learning

Complex AI workloads demand exceptional GPU performance and compute power — resources that non-enterprise teams struggle to obtain. Prime Intellect aggregates cloud GPUs from around the world on a unified platform, enabling small teams and startups to access more compute than they could otherwise obtain from individual providers. Their compute marketplace is designed for tasks beyond model inference, with a full training and evaluation stack to support pre-training, agent learning and reinforcement learning at scale.

Primarily a research lab, Prime Intellect is building the infrastructure for distributed pre-training and reinforcement learning for agents and large models like DeepSeek R1, using hundreds to thousands of GPUs. The Prime Intellect protocol enables distributed training via a peer-to-peer network, dynamically grouping GPUs with similar throughput and geography to maximize utilization.

Their latest distributed training initiatives deploy model instances across every onboarded cluster to run rollouts and experiments, then aggregate the rollouts for centralized training. This approach enables Prime Intellect to leverage non-reserved instances and heterogeneous, non-co-located compute — they’ve successfully coordinated resources from Nebius data centers in Europe and the US on training runs.

One of the company’s goals is to empower AI labs and researchers to build open source models by giving them on-demand access to distributed training and frontier hardware. Nebius is a key partner in reaching this goal.

## Nebius and Prime Intellect

Prime Intellect works with every major cloud provider to aggregate the world’s compute power, but Nebius is their go-to cloud for flexible on-demand compute and access to frontier hardware.

The company has partnered with Nebius from the start, training their Synthetic 2 and Intellect 2 models and scaling their research faster with elastic GPU provisioning. The culmination of their latest research is INTELLECT-3, a state-of-the-art Mixture-of-Experts model trained with 100B+ parameters on their reinforcement learning stack and fully open-sourced. They train their models on the same software and infrastructure offered to customers for post-training models on the Prime Intellect platform.

Prime Intellect can quickly scale up to thousands of GPUs to meet demand — part of the “magic” supported by the Nebius platform — with confidence in data transfer speeds and hardware reliability based on thorough stress testing of NVIDIA GPUs in Nebius AI Cloud. The team has taken advantage of SkyPilot integration to easily manage AI workloads across cloud platforms, using Nebius as a testing ground. Prime Intellect customers can also leverage NVIDIA HGX B200 systems in Nebius.

Alex Ferguson, head of Growth at Prime Intellect, explains how Nebius has become a preferred partner: “Nebius offers one of the highest capacities of on-demand utilization — much larger than most vendors. From a distributed training standpoint, one of the beautiful things is we can always find supply when we need it. We also get faster spinup times and better utilization rates compared to other vendors.”

## Industry-leading reliability and GPU utilization

At-scale reliability is critical for multi-host clusters like the Prime Intellect environment, where every disruption has wider repercussions. Each time a single node fails, training stops and resets to the last checkpoint on all the nodes, losing progress and wasting compute time.

To deliver a stable training environment, Nebius relies on purpose-built hardware and software designed to detect failures early and recover quickly in long training runs and demanding conditions. Automated mechanisms include multi-stage acceptance tests, health checks and end-to-end automation of recovery after node failure, with an average MTTR (mean time to recovery) of 12 minutes for multi-host training.

Prime Intellect uses Managed Soperator from Nebius to benefit from automations, along with smart scheduling and topology-aware job placement that boost efficiency for maximum GPU utilization.

High GPU utilization rates are critical to Prime Intellect to eliminate waste and get the best return on their AI infrastructure. With variable demand for compute, they leverage Nebius flexibility to achieve consistent 100% utilization during training runs, without booking GPUs.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## PoC with NVIDIA Grace Blackwell architecture

Beyond standard provisioning, the Nebius proof-of-concept (PoC) program gives Prime Intellect the unique opportunity to test drive the latest hardware before public release and explore advanced GPU capabilities. Prime Intellect tested the NVIDIA GB200 NVL72 for training and inference, using a four-node cluster with a total of 16 Blackwell GPUs to run real workloads and prepare to hit the ground running.

The NVIDIA GB200 NVL72 is designed for demanding AI tasks that require high bandwidth and low latency, well-aligned with Prime Intellect’s need for consistently high throughput in distributed AI training. A single NVIDIA GB200 NVL72 rack consists of 72 Blackwell GPUs and 36 Grace CPUs, interconnected by NVIDIA NVLink™, which allows the system to operate as one GPU.

Notably, the GPU calculation differs from NVIDIA Hopper: each NVIDIA GB200 NVL72 tray has four Blackwell GPUs. This difference translates to a larger number of interconnected nodes to handle AI workloads, resulting in a “new math” that requires a shift in thinking for AI architects, MLOps engineers and business leaders.

## Upgrading to NVIDIA GB200 NVL72

Prime Intellect took advantage of the Nebius PoC to optimize their workloads on the NVIDIA Blackwell rack-scale architecture.

In terms of compatibility, the upgrade didn’t require any code changes in their setup based on TorchTune, a PyTorch-native library, other than updating dependencies for the Arm-based Grace CPU. The team noted that the switch from Hopper to Blackwell went smoothly, with an optimized software stack at Nebius ensuring zero issues out of the box.

Experiments with reinforcement learning and pre-training on the GB200 NVL72 cluster led to downstream releases of the INTELLECT-3 model and the Trinity Large model, trained in partnership with Arcee AI. After experimentation, pre-training was performed on the HGX B300 systems.

## Choosing the optimal training precision

NVIDIA Blackwell features new, highly-efficient FP4 and enhanced FP8 floating-point data formats to boost performance for LLM inference and training. These low-precision formats represent data with fewer bits than the standard FP16 format for deep learning, allowing models to run faster and use less memory, though there is a tradeoff in output quality.

Prime Intellect’s experience with a wide range of AI workloads has helped them gain insights into choosing the right training precision. Here’s how they decide which precision to use for each project:

- 

BF16 (Bfloat16) precision is their trusted standard for training workloads, particularly for distributed training of large models.

- 

FP8 precision makes sense for most inference tasks.

- 

FP8 can be implemented successfully in some specific training scenarios as well. Since RL training includes a significant amount of inference, they use it for those tasks that are suited to low precision.

- 

FP4 adoption is currently more challenging due to the loss of quality. It can already be applied in some inference workloads and will start consuming more of the industry’s share in coming months.

## New opportunities powered by frontier hardware

Building on insights from their NVIDIA GB200 NVL72 proof-of-concept, Prime Intellect sees several strategic opportunities for future development.

Open source acceleration. The company plans to offer NVIDIA GB200 NVL72 compute access through their platform. They believe that easier access to cutting-edge hardware will accelerate improvements across the open-source ecosystem, from foundation models to reinforcement learning algorithms — benefitting the entire AI industry.

Overcoming scaling limitations. The GB200 NVL72 increased memory bandwidth improves parallelization for reinforcement learning workloads, potentially removing current limits to sequence length and chain-of-thought reasoning for faster RL scaling.

Software optimization for larger workloads. The company’s engineers have optimized their software stack for the GB200 NVL72 architecture and run larger, more scalable workloads. Their new Inference API provides direct access to more than 56 language models for large-scale evaluation of agents in the Environments Hub, a community platform for sharing RL environments. Looking ahead, they plan to run efficient reinforcement learning at scale and distributed training for giant models.

## More exciting stories

## 

vLLM

Using Nebius’ infrastructure, vLLM — a leading open-source LLM inference framework — is testing and optimizing their inference capabilities in different conditions, enabling high-performance, low-cost model serving in production environments.
Read the story

## 

SGLang

SGLang, a pioneering LLM inference framework, teamed up with Nebius AI Cloud to supercharge DeepSeek R1’s performance for real-world use. The SGLang team achieved a 2× boost in throughput and markedly lower latency on one node.
Read the story

## 

London Institute for Mathematical Sciences

How well can LLMs abstract problem-solving rules and how to test such ability? Research by the London Institute for Mathematical Sciences, conducted using our infrastructure, helps to understand the causes of LLM imperfections.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
