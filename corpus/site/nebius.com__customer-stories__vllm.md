# vLLM: Advancing open-source LLM inference

Source: https://nebius.com/customer-stories/vllm

Skip to main content

## Long story shortLong story short

For organisations leveraging AI in their day-to-day operations, optimizing LLM inference is crucial to enhancing efficiency, scalability, and accessibility. Using Nebius’ infrastructure, vLLM — a leading open-source LLM inference framework — leveraged cutting-edge compute accelerators and clusters to test and optimize their inference capabilities in different conditions, enabling high-performance, low-cost model serving in production environments.

vLLM is an open-source framework under the Linux Foundation, designed to optimize LLM inference at scale. It enables organizations to deploy and serve large language models with greater efficiency, reducing infrastructure costs and enhancing performance. With regular contributions from UC Berkeley, Anyscale, Meta, Red Hat, Hugging Face, NVIDIA, AMD, Google, AWS, Intel, and others, vLLM fosters innovation through a collaborative, community-driven approach.

## ContentsContents

Scaling up and optimising LLM inference performance

Benchmarking LLM inference

The competitive edge

Infrastructure and data handling

Key takeaways from collaborating with Nebius

Future roadmap and next steps

vLLM is a pioneering open-source framework dedicated to advancing LLM inference. As LLM technology evolves rapidly, achieving cost-effective inference at scale requires continuous optimization, hardware experimentation, and collaboration across industry and academia.

The framework is designed to support a wide range of model architectures and other LLM related processes, including:

- 

Transformer-based decoder models for text generation

- 

Multi-modal models with vision and language capabilities

- 

Reinforcement learning (RLHF) pipelines for LLM fine-tuning

By leveraging Nebius’ high-performance compute clusters, vLLM has successfully accelerated inference across all these applications. This includes deploying RLHF workloads for synthetic data generation, reward modeling, and real-time inference evaluation, helping organisations in ensuring that models are continuously optimized for efficiency and responsiveness.

One of the key challenges in inference development is access to cutting-edge accelerated compute hardware for rigorous testing and benchmarking.

Through our collaboration, vLLM has overcome these barriers, leveraging high-performance compute clusters and network infra to accelerate development and testing cycles. This access has been instrumental in refining vLLM’s inference capabilities, ensuring that organizations using the framework benefit from reduced costs and improved performance.

## Scaling up and optimising LLM inference performance

Nebius’ infrastructure played a key role in helping vLLM optimize inference for transformer-based models, including large-scale architectures such as DeepSeek R1. While tests on smaller models can be performed on a single node with accelerated compute instances, the requirements fundamentally shift for models like DeepSeek R1.

By utilizing compute clusters, vLLM successfully scaled up inference experiments, integrating cutting-edge optimizations like multi-latent attention and multi-token prediction from the DeepSeek research paper into vLLM. Having reliable, high-performance machines made it possible to rigorously test and refine these cutting-edge features before releasing them for broader community use.

Nebius’ infra enabled vLLM to run large-scale LLM inference with seamless scaling, allowing it to handle increased workloads efficiently. It also provided a reliable environment for benchmarking models across multiple types of accelerated compute, ensuring consistent and accurate performance evaluations. Additionally, the infrastructure supported the optimization of multi-token prediction, leading to improved response latency and a smoother user experience.

vLLM’s mission is to make high-performance LLM inference accessible to a broad range of organizations. To achieve this, it was also critical to balance cost-efficiency, performance, and speed when running large-scale models.

With Nebius’ compute, vLLM was able to optimize inference throughput by maximizing tokens per second, significantly enhancing cost-effectiveness. Nebius also ensured reliable accelerated compute availability by seamlessly scaling resources on demand, eliminating any delays. Additionally, access to Nebius’ latest accelerated compute removed hardware constraints, enabling uninterrupted testing and benchmarking.

This seamless integration allowed vLLM to refine and scale inference workloads without disruptions, ensuring high availability and consistent model performance.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Benchmarking LLM inference

To ensure the highest performance standards, vLLM employs rigorous benchmarking methods, using both standard inference benchmarks and internal performance metrics.

Key success indicators include throughput, which focuses on maximizing tokens per second to enhance inference speed. Another important metric is queries per second, which aims to optimize the number of concurrent requests the system can handle. Lastly, latency is carefully monitored to reduce both time-to-first-token and inter-token delays.

These benchmarks help vLLM continuously refine its inference performance, ensuring that users experience highly efficient, low-latency model serving.

## The competitive edge

vLLM operates in a competitive landscape alongside frameworks like TensorRT-LLM, but it stands out through several key differentiators. As a fully open-source project governed under the Linux Foundation, it promotes transparency and fosters community collaboration. Its hardware-agnostic design allows it to support a wide variety of accelerated compute and cloud environments, enabling flexible and scalable deployments. Additionally, vLLM integrates a variety of advanced inference optimizations that enhance throughput and response times, ultimately delivering best-in-class cost efficiency.

This combination of community-driven innovation and cutting-edge optimizations positions vLLM as a leader in LLM inference frameworks.

## Infrastructure and data handling

For efficient inference, vLLM required a high throughput storage solution to handle model weights. With Nebius’ non-replicated disks (NRD), vLLM could store large-scale model weights while maintaining high data throughput without incurring unnecessary redundancy costs.

NRD allowed vLLM to quickly load large model weights without bottlenecks, ensuring smooth and efficient initialization. It also optimized data access for inference workflows by leveraging fast local storage, which significantly improved performance. At the same time, it maintained cost-effective storage solutions by minimizing unnecessary overhead, striking a balance between speed and efficiency.

The simplicity of storing large model weights locally on fast disks met vLLM’s performance needs and allowed them to focus on inference optimization rather than storage management.

## Key takeaways from collaborating with Nebius

- 

Stable infrastructure: vLLM never encountered hardware-related issues.

- 

Reliable metrics: vLLM can trust the performance metrics gathered on Nebius machines.

- 

Enhanced productivity: This level of reliability and consistency allows vLLM to focus on developing new features and optimizations rather than troubleshooting resource constraints.

By working with Nebius, vLLM has successfully accelerated its open-source framework development, enabling organizations to serve large-scale language models with greater efficiency, reliability, and scalability.

## Future roadmap and next steps

vLLM’s next phase of development focuses on:

- 

Expanding support for very large models through distributed inference.

- 

Implementing advanced parallelism strategies — including context, model, tensor, pipeline, and sequence parallelism to handle increasingly large model architectures.

- 

Enhancing training workflows and RLHF use cases to ensure high-throughput performance.

- 

Keeping vLLM modular and extensible to allow users to integrate their own plugins or additional components to suit specialized needs.

Looking ahead, vLLM will continue leveraging Nebius’ cutting-edge infrastructure to push the boundaries of LLM inference, ensuring that the broader open-source community benefits from highly optimized and cost-effective AI model serving.

## More exciting stories

## 

Simulacra AI

Simulacra AI is combining ab initio quantum chemistry with deep learning to build a scalable large wavefunction model (LWM) to generate high-accuracy datasets for drug and material discovery pipelines.
Read the story

## 

SynthLabs

Synthlabs significantly simplified their training infrastructure setup using TractoAI serverless platform. Synthlabs research engineers leveraged TractoAI distributed offline inference capability to accelerate the release of the first open source reasoning dataset.
Read the story

## 

Unum

In our field, effective partnerships that harness complementary strengths can drive significant breakthroughs. Such is the case with the collaboration between Nebius and Unum, an AI research lab known for developing compact and efficient AI models.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
