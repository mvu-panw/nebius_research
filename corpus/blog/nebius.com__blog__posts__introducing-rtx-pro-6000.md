# Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

Source: https://nebius.com/blog/posts/introducing-rtx-pro-6000

Skip to main content

Over the past few years, AI infrastructure has largely been defined by the rise of generative AI. Large language models and multimodal foundation models rely heavily on low-precision, tensor arithmetic and large-scale multi-host compute environments. This has pushed the market toward accelerators optimized for distributed performance and transformer-heavy workloads.

But the AI wave has not been limited to foundation models and LLM-powered chatbots. It has also accelerated growth in applied domains such as scientific simulations, robotics, digital twins and synthetic data generation. These workloads often require a different balance of capabilities, like strong performance for single-precision calculations, optimized single-host inference, or visual computing.

Today, we are introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on our global cloud infrastructure — expanding our GPU lineup to address this growing class of simulation workloads and multimodal AI.

## RTX and the rise of spatial AIRTX and the rise of spatial AI

RTX technology has long been associated with ray tracing in video games. In the data center context, RTX represents a combination of AI acceleration and dedicated RT Cores for spatial computation.

RT Cores accelerate geometric intersection and ray tracing operations, which are essential for visual computing, real-time rendering and high-fidelity simulations. As AI increasingly interacts with the physical world, spatial computing becomes foundational.

This makes RTX PRO 6000 Blackwell particularly well suited for emerging workloads such as Vision-Language-Action models, embodied reasoning in robotics, synthetic data generation and digital twin environments powered by NVIDIA Omniverse. These scenarios require tight integration between simulation, rendering and AI inference — a combination that RTX architecture is designed to support.

## Robust performance for scientific simulationsRobust performance for scientific simulations

Scientific computing has also been reshaped by AI. In drug discovery, for example, molecular dynamics and docking simulations increasingly work side by side with machine learning models that help identify the most promising molecules and estimate how well they interact with a target protein. Researchers may simulate protein behavior, use AI models to rank and refine results and visualize outcomes — all within a connected workflow.

A similar pattern appears in physics-based simulations and engineering research. Teams run large-scale simulations, analyze the results with AI models, adjust parameters and repeat. These iterative cycles demand not only visualization and AI inference, but also strong numerical performance for the underlying calculations.

NVIDIA RTX PRO 6000 Blackwell is well suited for these scenarios. It delivers robust single-precision compute for selected scientific workloads, while also supporting AI models and advanced visualization within the same architecture.

## Cost-efficient inference with 96GB GPU memoryCost-efficient inference with 96GB GPU memory

With 96GB of GDDR7 memory, RTX PRO 6000 Blackwell enables teams to serve substantial models without splitting them across multiple GPUs. For throughput-sensitive deployments, the GPU’s 5th Generation Tensor Cores support FP4 precision, further reducing memory footprint and increasing request concurrency for models where that trade-off is acceptable. Optimized 70B-parameter models can run on a single card, while 30–40B models can operate comfortably in 16-bit (BF16) precision. This simplifies system design and eliminates cross-GPU communication overhead, resulting in more consistent inference latency. Larger memory also enables higher request concurrency and supports longer context windows, both critical for production AI applications.

The GPU supports Multi-Instance GPU (MIG) technology, allowing a single card to be partitioned into up to four isolated 24GB instances. This makes it possible to serve multiple workloads on one GPU, for example, combining embeddings, reranking and language models, or to allocate resources efficiently across different users.

With up to 6X the performance of NVIDIA L40S systems and more than 2x better price-performance than the NVIDIA HGX H100 for LLM inference, the RTX PRO 6000 Blackwell offers an attractive balance of capacity and efficiency for production inference.

## Built on the evolution of NVIDIA L40S GPUBuilt on the evolution of NVIDIA L40S GPU

RTX PRO 6000 Blackwell Server Edition continues the evolution of NVIDIA RTX GPUs for data centers and can be seen as a successor to the widely used L40S. The new generation targets the same class of workloads such as visual computing, simulation-driven research and AI inference, while bringing important improvements in memory capacity, RT Core performance and single-precision compute.

These upgrades allow many workloads previously deployed on L40S to run faster and more efficiently, while also enabling larger models and more flexible inference configurations on a single GPU.

## Get startedGet started

Applied AI is a rapidly evolving domain. By introducing NVIDIA RTX PRO 6000 Blackwell Server Edition to Nebius, we aim to support practitioners in this field by providing more flexible access to compute designed for their specific needs.

On the Nebius platform, RTX PRO 6000 Blackwell instances are ready for production use, including deployments in regulated industries such as biotech and healthcare. Our cloud infrastructure provides strong data protection and secure environments designed to support HIPAA-compliant customer deployments.

Contact us to discuss your workload requirements and use case, and explore how RTX PRO 6000 Blackwell can support your next stage of innovation.

Please contact your account manager to check availability; self-service access will be available at a later stage.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- RTX and the rise of spatial AI

- Robust performance for scientific simulations

- Cost-efficient inference with 96GB GPU memory

- Built on the evolution of NVIDIA L40S GPU

- Get started

## See also

### 

Nebius AI Cloud “Aether 3.5”: Frictionless compute for real world AI

This release introduces new serverless capabilities, the NVIDIA RTX PRO™ 6000 Blackwell Server Edition GPU for applied AI use cases, improved cluster configuration tools, streamlined data operations and platform-level enhancements that reduce routine complexity while preserving full control.

March 26, 2026
8 mins to read

### 

Introducing DevPods, Jobs and Endpoints: Easy compute access with serverless AI

The serverless services at Nebius are a natural extension of how an AI infrastructure cloud evolves over time, building on a mature and well-established underlying platform. As the platform develops, it becomes possible to expose compute in more flexible and elastic forms that better match how AI workloads are consumed.

March 26, 2026
12 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
