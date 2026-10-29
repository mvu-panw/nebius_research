# Recraft V4: Scaling image gen with the NVIDIA HGX B200 cluster in Nebius AI Cloud

Source: https://nebius.com/customer-stories/recraft-v4

Skip to main content

## A model developed with designersA model developed with designers

Today, Recraft unveiled Recraft V4, bringing true visual taste to AI generation, built for brand systems, campaigns, and production-ready design. It provides not just accurate prompt interpretation, but true design vision in composition, lighting, textures, and overall feel.

To train Recraft V4, the company collaborated with Nebius and deployed NVIDIA HGX B200, achieving a seamless transition from the NVIDIA Hopper architecture with minimal code changes. Through early access testing and hands-on engineering support, Recraft validated Blackwell’s capabilities for large-scale visual AI workloads.

## ContentsContents

About Recraft V4

Nebius and Recraft

Smooth migration to the newest architecture

Engineering support and robust infrastructure

Recraft’s training precision strategy

Key takeaways from Recraft’s experience upgrading to NVIDIA Blackwell GPUs

Learn more about NVFP4 and NVIDIA Quantum-2 InfiniBand

Most leading image models today are optimized for broad, general preference. While that works well for mass appeal, it often falls short of the standards required for brand systems, campaigns, and production-ready design work. Recraft V4 was developed in close collaboration with designers and tuned around professional aesthetics and real creative expectations. As a result, Recraft V4 brings true visual taste to AI image generation.

Recraft V4 is available in two versions: V4 and V4 Pro. Both share the same creative capabilities and design sensibility, producing art-directed, professional-quality visuals. The difference lies in resolution and scale. V4 is faster and more cost-efficient, while V4 Pro generates higher-resolution images for print-ready assets and large-scale use. The team believes Recraft V4 fills a meaningful niche: generative imagery tuned for professional design aesthetics rather than general internet preferences.

Recraft develops image models that enable designers and marketers to produce high-quality visual content. Built from the ground up on Nebius, Recraft V4 is a foundation model shaped by professional design standards to generate images with strong visual judgment and brand-level quality. Since the company developed the first text-to-image model made specifically for design teams, enterprise users and consumers have generated more than 350 million images on the Recraft platform.

The company is an early adopter of NVIDIA Blackwell GPUs, partnering with Nebius to test the latest chips before they became publicly available. NVIDIA Blackwell architecture is designed to support large-scale AI training, giving Recraft the computational capacity required to scale their foundation model.

Collaboration with Nebius helped the team transition seamlessly to the new architecture and run training and inference on an NVIDIA HGX B200 cluster in Nebius AI Cloud.

## Nebius and Recraft

Recraft has an extensive history with Nebius that spans successful deployments of NVIDIA Ampere, Hopper and Blackwell platforms. They were one of the first customers on the Nebius AI Cloud platform and early adopters of NVIDIA Blackwell GPUs at Nebius. After successfully adopting NVIDIA HGX B200, they have moved on to testing NVIDIA HGX B300 instances on their workloads.

They emphasize model quality through scale, building large foundation models for creating high-quality visual content. “For image generation, the bigger the model, the better the quality, ” explains Pavel Ostyakov, Head of AI at Recraft. “When we talk about model size, we mean more than just the number of parameters. In our experience, the most important factor is the quantity of operations, or the number of FLOPS the model uses internally in order to generate the output. With NVIDIA Blackwell GPUs, we were able to scale the model significantly in both operations and parameters — in this case, we’re talking about dozens of billions of parameters.”

## Smooth migration to the newest architecture

This new architecture offers enhanced training performance and inference capabilities, with LLM training up to four times faster than on previous generation. To power Recraft’s model training, Nebius provided a cluster with NVIDIA Blackwell GPUs, interconnected via NVIDIA Quantum-2 InfiniBand.

The transition from NVIDIA Hopper to NVIDIA Blackwell was straightforward for Recraft. Their PyTorch-based software stack was compatible with NVIDIA containers, which provide precompiled libraries that work out of the box. Distributed training workloads didn’t require any changes to the GPU communication software stack, with the InfiniBand network providing the same reliable performance as on previous generations of GPUs.

The Recraft team made a few customizations to their training setup to improve production performance on the new architecture, such as rewriting a portion of code to switch from compiling networks with TensorRT to using torch.compile directly.

“If you have simple code, you can switch to the new GPUs without doing anything special, ” Ostyakov noted.

## Engineering support and robust infrastructure

Nebius infrastructure facilitates hardware upgrades with an optimized software stack and preventative maintenance. The Nebius AI Cloud platform provides improved cluster observability through robust monitoring services and detailed logs, enabling Recraft to quickly identify and resolve performance issues.

Recraft engineers experienced minimal training interruptions due to efficient checkpoint and restart procedures. This can be attributed to Nebius’s automated maintenance systems and fault detection. When an InfiniBand link or GPU goes offline, the system automatically replaces the node and restarts training from the last checkpoint, minimizing disruption to multi-day training runs.

Recraft also collaborated with the in-house engineering team at Nebius throughout the transition to NVIDIA Blackwell GPUs, relying on their experience with hardware upgrades and deep expertise in this newest architecture to help solve issues that came up during early access testing.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Recraft’s training precision strategy

This latest generation of GPUs presents new alternatives for training precision, with support for both FP8 and FP4 quantization potentially enabling faster performance.

Recraft selects training precision formats based on workload-specific quality requirements. They primarily use bfloat16 for model training, where precision is critical for image generation quality. However, they deploy FP8 for running the text encoder component in their model pipeline — since these weights remain frozen during pre-training, the lower precision enables faster processing of samples without compromising output quality.

For LLM inference workloads, Recraft deploys FP8 precision, consistent with their NVIDIA Hopper implementation. The team is now experimenting with NVFP4, NVIDIA Blackwell’s native 4-bit format, to optimize inference speed.

## Key takeaways from Recraft’s experience upgrading to NVIDIA Blackwell GPUs

- 

Easy upgrade to frontier chips: Migrated from NVIDIA Hopper to Blackwell with minimal code changes, running distributed training out of the box.

- 

Scaling image generation: Successfully deployed NVIDIA Blackwell GPUs for scaling their model, validating this hardware for large-scale training of image generation models.

- 

Training precision optimization: Deployed workload-specific precision formats on NVIDIA Blackwell GPUs — BF16 for the majority of training, FP8 to accelerate training the text encoder and experiments with NVFP4 for faster inference.

- 

Reliable infrastructure and hands-on support: Minimized training interruptions through automated fault detection and checkpoint recovery in the Nebius AI Cloud. Nebius engineers were on hand to solve technical challenges for faster onboarding to the new generation.

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
