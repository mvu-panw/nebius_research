# Built with Nebius

Source: https://nebius.com/customer-stories

Skip to main content

# Built with Nebius37 stories

Industry

Industry
Workload type

Workload type
Segment

Segment
Region

Region

## 

Wildflow

Wildflow builds multimodal foundation models for biodiversity, starting with coral reefs. Using Nebius AI Cloud, the team processes terabytes of underwater footage and environmental data into high-fidelity 3D digital twins for ecosystem monitoring and restoration. Their scalable reconstruction pipeline works with data from more than 20 research organizations worldwide and produces 3D reconstructions and renders in hours rather than days.

## 

NormaCore

NormaCore is building the infrastructure layer for physical AI, with an open-source runtime and high-fidelity telemetry database that standardize data capture across heterogeneous robot fleets. With Nebius, teams can move from on-robot data collection to S3-compatible storage and GPU training through a single integration, helping NormaCore go from initial evaluation to full production in under three hours.

## 

Antioch

Antioch is building a cloud simulation platform for physical AI, letting robotics teams replace hardware-in-the-loop testing with thousands of scenarios run in parallel. On Nebius, teams spin up a GPU-backed simulation environment in under five minutes, stream scenes at 100+ frames per second, and run end-to-end simulation cycles up to 50% faster.

## 

Voxel51

Voxel51 develops FiftyOne, an open-source platform that helps physical AI teams understand, curate, and evaluate multimodal datasets. Together with Nebius and NVIDIA, the company built a production synthetic data pipeline that enables teams to generate synthetic scene variations at scale and review them in FiftyOne.

## 

Ultimate Bots

Ultimate Bots is building a robot sports league and software for humanoid robots. Its browser-based Studio makes humanoid robotics accessible to creators by turning recorded movement into deployable robot motion in minutes. Powered by Nebius Serverless and NVIDIA’s SONIC foundation model, Studio now supports more than 500 creative workflows each month.

## 

Prima Mente

Prima Mente is building foundation models to uncover what’s happening in the brain without directly accessing it. With a 32-GPU reserved cluster in Nebius, Prima Mente amped up pre-training throughput by 12%, processing 1.19 million tokens/s on 16 nodes, a critical step in their goal toward scaling model size from 7B up beyond 100B parameters.

## 

RoboForce

RoboForce builds Robo-Labor for dirty, dangerous and repetitive industrial work across solar, data centers, shipping, mining, manufacturing and logistics. With Nebius AI Cloud, NVIDIA Blackwell infrastructure, scalable storage and expert support, RoboForce reduced AI setup pipeline time by 70% and cut iteration cycles from months to days.

## 

Jua

Jua is building a foundation AI model for weather simulation, creating a real-time digital twin of the Earth. Using Nebius AI Cloud, the team trains large-scale physics-based models to deliver fast, high-resolution forecasts, enabling energy traders to make better decisions in highly volatile, weather-driven markets.

## 

Sword Health

Sword Health built Dawn, a direct-to-consumer AI wellbeing specialist, to scale mental health support beyond clinician-led care. Using Nebius AI Cloud, MindGuard guardrails and the MindEval framework, the team enabled safe, long-form conversations in production.

## 

Revolut

Revolut rebuilt core operations around AI to scale fast in a regulated environment, using Nebius AI Cloud and Token Factory to power fraud prevention, customer support, and large-scale model training across more than 200 NVIDIA H100 GPUs.

## 

Recraft V4

To train its latest model, Recraft collaborated with Nebius and deployed NVIDIA HGX B200, achieving a seamless transition from the NVIDIA Hopper architecture with minimal code changes. Through early access testing and hands-on engineering support, the company validated Blackwell’s capabilities for large-scale workloads.

## 

Stanford

CRISPR-GPT is an LLM-powered agent system developed by scientists from Stanford, Princeton and Google DeepMind, which automates gene-editing experiments, from CRISPR system selection to decision making when designing gene-editing RNA to data analysis.

## Learn quickly about workload types and outcomes

## vLLM: Advancing open-source LLM inference

vLLM is an open-source framework under the Linux Foundation, designed to optimize LLM inference at scale. It enables organizations to deploy and serve large language models with greater efficiency, reducing infrastructure costs and enhancing performance.

Goal: To develop and continuously optimize vLLM framework for efficient LLM inference, enabling organizations to serve large language models at lower costs while ensuring scalability and performance optimization.

Solution: The Nebius team provided vLLM with reliable access to cutting-edge compute accelerators and compute clusters for large-scale inference experiments.

Result: With Nebius, vLLM has successfully optimized inference performance for transformer-based models, including DeepSeek R1. The project has achieved high-throughput inference, seamless scalability, and integration of advanced features like multi-latent attention and multi-token prediction.
- 
Inference
- 
Open-source

Zero
hardware-related issues

Consistently
accurate hardware performance metrics

Compute clusters to run
DeepSeek R1

## Enhancing AI-powered search

Brave Software, with over 80 million users, develops a fast, privacy-focused browser and Brave Search, an independent search engine. Its AI-powered feature, Answer with AI, provides real-time, privacy-centric summaries for user queries.

Goal: To generate AI-driven search responses with modern compute infrastructure.

Solution: Brave uses Terraform for provisioning and HAProxy for load balancing, ensuring efficient AI inference, real-time response generation and seamless traffic scaling.

Result: With Nebius, Brave runs large AI models with nearly 100% compute utilization, delivering real-time AI summaries for over 11 million queries daily. The scalable infra allows Brave Search to provide faster, more relevant answers while maintaining strict privacy standards.
- 
Inference
- 
Web search
- 
AI summaries

10–70B
LLM parameters

1.3B
search queries per month

11M+
AI-generated answers daily

## Cost-efficient AI deployment platform

The CentML Platform powers open-source model deployment with automated compute optimizations and flexible configurations. CentML delivers state-of-the art inference at reduced costs, without vendor lock-in.

Goal: Give customers access to a highly performant, cost-optimized full stack solution for AI deployment.

Solution: CentML uses Nebius compute alongside ML techniques to optimize their inference platform, delivering flexible scaling, streamlined deployments and enhanced hardware utilization for AI models.

Result: Significant cost savings, improved reliability and scalability, and enhanced EU-based compute capabilities. Customers can reduce infrastructure complexity and securely deploy open-source LLMs.
- 
Inference
- 
Open-source

x5
lower costs compared to other major providers

Enhanced
compliance with EU compute requirements

1 week
to get cluster online

## Stable diffusion inference

TheStage AI builds inference simulators and DNN optimization tools for a wide range of hardware, significantly reducing GPU costs.

Goal: To enhance the capabilities of TheStage AI platform with a focus on stable diffusion architecture.

Solution: To run tests on TheStage AI acceleration framework, particularly on the computationally intensive UNet component, using the open-source Stable Diffusion v1-5 model by RunwayML.

Result: Two acceleration methods — quantization and structured sparsification — were implemented using NVIDIA H100 Tensor Core GPUs for efficient INT8 and sparse computation. The project resulted in a significant reduction in the number of GPUs needed for inference.
- 
H100
- 
Inference
- 
Stable diffusion

4x leap
in speed over the early version of the framework running on A100

~500 ms
to process one image during inference

1B parameters
of the model

## Training gen AI foundational model

Recraft is an AI design tool that lets users create and edit digital illustrations, vector art, icons and 3D graphics in a uniform brand style.

Goal: To train the first generative AI model for designers from scratch.

Solution: To utilize all the key parts of Nebius AI and implement PyTorch + Kubeflow, with NCCL used for the hardware setup.

Result: Thanks to the contributions from the Nebius support and architect teams, Recraft overcame hardware configuration challenges and achieved remarkable system stability.
- 
GenAI
- 
Training

20B
model parameters

Comparable
to DALL·E 3 with 49% preference on PartiPrompts benchmark

54%
preference over Midjourney v6 on the same benchmark

## Streamlining music creation through AI

Wubble is a cutting-edge AI platform designed to empower businesses to generate high-quality, royalty-free music instantly, streamlining creative processes and unlocking limitless possibilities for marketing, advertising, podcasts, games, stores and more.

Goal: To optimize AI operations and model deployment for scalable, efficient and low-latency music generation.

Solution: Leveraging Nebius’ infrastructure and Kubernetes, Wubble built a scalable system for managing workloads and deployments.

Result: The company achieved high-capacity inference, QLoRA adaptation and faster audio analysis pipelines. These advancements reduced the time to first token and ensured reliable performance, while integration with GCP enabled robust scalability and efficient resource utilization.
- 
Media
- 
Inference
- 
LoRA

3B+
model parameters

100+ genres
the model is conversant in

1.8 seconds
Reduced time to first token generation

## Quantum Chemistry for drug and material discovery

Simulacra AI is transforming the quantum chemistry field by automatically generating high-precision datasets for molecular dynamics models at scale.

Goal: Build a scalable foundational wave-function model for molecular systems that can generate high-accuracy datasets for pipelines of drug and material discovery.

Solution: Simulacra AI used Nebius infrastructure to overcome scalability and efficiency challenges.

Result: Simulacra AI delivers next-generation molecular data, enabling any company to refine in silico pipelines without relying on broad internal infrastructure to train models.
- 
Training
- 
Research
- 
Quantum tech

100M+
model parameters

90% faster
Thanks to Nebius infrastructure, our largest models take 10–20 minutes to compile for pre-training, compared to over 2 hours previously

H100 + H200
NVIDIA Tensor core GPU fleet

## Advancing molecular generation

Quantori is the end-to-end data, technology and digital services partner of choice for leading biopharma and healthcare organizations worldwide.

Goal: To develop an AI framework that generates molecules with precise 3D shapes, enhancing drug discovery and material design.

Solution: Quantori employs a pipeline based on Equivariant Diffusion Model and Structure Seer model trained on 1.6M molecules from the ChEMBL database. The pipeline generates molecular structures using shape descriptors.

Result: After 1,500 training epochs, the model successfully generated chemically sound molecules that closely resemble real molecules in shape. The approach enables rapid molecular ideation, predicting valid 3D conformations with optimized properties.
- 
Training
- 
Drug discovery

1.6M
molecules from ChEMBL — dataset size

1,500 epochs
Training duration

High similarity
to reference geometries

## Start your journey today
Make it my experience

## Explore the platform

Pricing​
Docs​
