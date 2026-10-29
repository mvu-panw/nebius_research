# Higgsfield AI: Training a large-scale diffusion model at speed with Nebius AI Cloud

Source: https://nebius.com/customer-stories/higgsfield-ai

Skip to main content

## Impact deliveredImpact delivered

- 

Scaled from zero to $200M in run rate in just nine months, with infrastructure reliability from Nebius as the foundation

- 

Expanded to 15M+ users while maintaining consistent performance

- 

Sustaining 4.5M+ (both video and image) generations per day without service disruption

- 

Enabled hypergrowth by pairing lightning-fast iteration with infrastructure designed for stability at scale

- 

Time to first training run: < 1 hour

- 

100% self-service infrastructure setup

“Multi-billion-parameter diffusion models expose every weakness in a system. At Higgsfield, we design for resilience, throughput, and rapid iteration from day one. Nebius’s Blackwell-powered infrastructure reinforced that approach, allowing us to move quickly, scale confidently, and keep our attention on building differentiated creative intelligence, not managing infrastructure complexity.”

— Alex Mashrabov, Founder and CEO, Higgsfield AI

## ContentsContents

Scaleup speed with enterprise-grade training

The challenge: Scaling diffusion training without losing momentum

Finding a cloud provider and co-engineer in Nebius

Accelerated computing resources: NVIDIA HGX B200 changed the equation

Higgsfield AI’s data strategy kept GPUs busy and training stable

Solving the “taste problem” with human preference

The result: Training stability unlocked product velocity

Higgsfield AI, a fast scaling genAI company with $130M in Series A funding, trained a multi-billion-parameter diffusion model for image editing and keyframe generation by solving some of the hardest problems in distributed training, memory optimization and data scaling. With Nebius as a co-engineering collaborator leveraging NVIDIA Blackwell GPUs, the team built a training pipeline that stayed stable under sustained load and supported one of the fastest scale-ups ever seen in the application layer of generative AI.

# Scaleup speed with enterprise-grade trainingScaleup speed with enterprise-grade training

With more than 15 million users globally and customers already spending $300,000+ annually, Higgsfield AI’s ambition is simple but demanding: make high-quality visual creation effortless. The company is building a generative image and video platform that transforms text and reference images into coherent, animated visuals in seconds without forcing creators to become technologists or prompt engineers.

Under the hood, that experience depends on serious model training. Higgsfield AI’s product, which some position as the Cursor for video, is powered by a custom diffusion model that understands both language and vision and can generate visuals that evolve naturally over time. The latest architecture combines image editing and keyframe generation into a single diffusion framework, enabling temporal coherence rather than isolated frames.

For Higgsfield AI, as it moves toward powering over half of all social media content in 5 years, training is about enabling rapid iteration, improving output quality and supporting continuous product evolution as usage scales.

## The challenge: Scaling diffusion training without losing momentum

Building a diffusion model that spans image editing and temporal keyframes introduces complexity across every layer of the stack. The model must handle large parameter counts, long diffusion sequences and high-resolution data, while running reliably across multi-node GPU clusters for extended training cycles.

At this scale, long-running jobs are vulnerable to hardware interruptions, node failures, networking instability and I/O bottlenecks, any of which can terminate a run and erase days of progress. These are the realities of large-scale training.

At the same time, Higgsfield AI’s broader mission gained momentum. The company is moving towards making creativity accessible for both professional social media creators and the largest advertising agencies and global brands. That means the training pipeline must support rapid iteration, consistent quality and predictable delivery.

## Finding a cloud provider and co-engineer in Nebius

To meet these demands, Higgsfield AI collaborated with Nebius as a hands-on infrastructure collaborator deeply involved in solving the challenges of large-scale training. From day one, the joint work focused on removing the systemic risks that derail long training runs like unreliable capacity.

As Alex Mashrabov, Founder and CEO of Higgsfield AI, explains: “From day one, Nebius felt like a co-engineer, not just a cloud provider. Their infrastructure, paired with the new Blackwell GPUs, gave us the confidence to push the boundaries of generative AI — enabling faster iterations, stable scaling and exceptional reliability across model development, training and inference.”

This co-engineering mindset proved critical as Higgsfield AI scaled model complexity and business demand.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Accelerated computing resources: NVIDIA HGX B200 changed the equation

The computational demands of Higgsfield AI’s training pipeline required state-of-the-art compute resources. The team deployed NVIDIA HGX B200 systems, with a total GPU memory of 180 GB to support large model parameters and high-resolution batches. This allowed Higgsfield to achieve high performance without worrying about memory constraints.

Higher memory bandwidth and strong FLOPS performance further reduced pressure points common in diffusion workloads, allowing the team to design the training stack around predictable hardware behavior.

The team designed the training stack optimized for the NVIDIA Blackwell architecture.

## Memory optimization beat recomputationMemory optimization beat recomputation

To manage GPU memory demands, Higgsfield AI evaluated two primary strategies: activation checkpointing and distributed optimizers. Activation checkpointing reduced memory usage but introduced significant recomputation overhead during the backward pass, slowing training to an unacceptable degree.

The team observed that while checkpointing saved memory, it increased per-iteration time enough to negate its benefits. Distributed optimizers, by contrast, effectively managed memory without imposing the same performance penalty. Higgsfield AI opted to rely solely on distributed optimizers for the full training run.

The takeaway: in large diffusion models, conserving memory is important — but not at the expense of iteration speed.

## FlashAttention-based optimizations improved throughputFlashAttention-based optimizations improved throughput

The team benchmarked multiple implementations, including FlashAttention variants (designed for Hopper) and cuDNN fused attention (built for Blackwell). Empirical testing revealed that a hybrid configuration maximized throughput for Higgsfield AI’s diffusion workload. This tuning step was essential for sustaining performance across long training runs.

## Kernel fusion compounded at scaleKernel fusion compounded at scale

To extract additional efficiency, Higgsfield AI leveraged torch.compile() to JIT-compile graph-friendly sections of the model. This enabled kernel fusion, reducing memory access overhead by combining multiple operations into single GPU instructions.

While the gains per iteration were modest in isolation, they compounded across longer runs, saving thousands of GPU hours over the full training lifecycle.

## Higgsfield AI’s data strategy kept GPUs busy and training stable

Training stability wasn’t just a problem of accessing enough compute at the right time. Higgsfield AI designed a multi-stage data curriculum that progressed along two dimensions: resolution and data quality.

Early training focused on mid-resolution imagery (around 720p) to teach the model basic structure. As training advanced, resolution increased beyond 2K, allowing the model to learn fine-grained detail and texture. In parallel, the dataset evolved from massive, broadly sourced data to increasingly curated, high-quality samples. For an audience of fast-moving creatives, this reliability and aesthetic focus is the difference between frustration and execution.

Nebius played a critical role by enabling high-throughput data distribution and storage architectures tuned for streaming large datasets. Higgsfield AI decoupled data preprocessing from training: raw image-caption pairs were filtered, encoded into latents and cached by resolution in a shared, location-aware store. Training nodes then pulled pre-processed batches asynchronously, ensuring GPUs were never idle waiting for data.

## Solving the “taste problem” with human preference

Once the training pipeline stabilized, Higgsfield AI turned to alignment. High-quality outputs need to be more than technically correct. They had to reflect human aesthetic judgment with expression and visual appeal.

The team used Direct Preference Optimization (DPO), generating multiple candidate outputs per prompt and ranking them with human evaluators. This process required reliable access to large GPU clusters to support repeated generation and retraining cycles.

Nebius’ stable multi-node clusters made it possible to run these preference-driven training loops continuously.

## The result: Training stability unlocked product velocity

By solving the hardest training problems first, Higgsfield AI built a foundation that scaled with the business. Training runs completed reliably. Iteration cycles shortened. Engineering effort shifted from firefighting to refinement.

That stability translated directly into speed. Higgsfield AI moved from zero to $100M in seven months, then crossed a $200M run rate faster than any other gen AI company — in just two months, soon after without re-architecting its training stack or slowing development.

As Mashrabov puts it: “Training a multi-billion-parameter diffusion model isn’t just about compute — it’s about stability, bandwidth and trust. Nebius delivered all three.”

For Higgsfield AI, the collaboration with Nebius delivered more than infrastructure. It was a nimble co-engineering collaborator that enabled the company to push the boundaries of generative AI while keeping creators at the center of the experience.

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
