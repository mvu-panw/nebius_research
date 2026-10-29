# Delivering a validated AI Factory stack for agent workloads on Nebius AI Cloud with DataRobot

Source: https://nebius.com/blog/posts/datarobot-validated-ai-factory-stack

Skip to main content

AI agents are increasingly being deployed into live business workflows, where sustained inference performance, runtime governance and unit economics matter as much as model quality. Systems must handle continuous token generation, maintain low latency under load and enforce governance controls while keeping inference costs predictable.

At NVIDIA GTC 2026, Nebius and DataRobot, with NVIDIA, announced a validated AI Factory stack designed for production-grade agent workloads.

The DataRobot Agent Workforce Platform, co-engineered with NVIDIA, is now supported on Nebius AI Cloud through a validated configuration optimized for running agent workloads in production environments. This brings together comprehensive agent lifecycle management and a validated AI Factory stack purpose-built for sustained token throughput, ultra-low latency, workload isolation and production grade elasticity with end-to-end governance.

This end-to-end agent lifecycle management platform provides a production-ready path for enterprises deploying AI agents into live workflows where governance, sustained inference and cost control matter as much as model capability.

## A validated AI Factory stack for agent workloadsA validated AI Factory stack for agent workloads

Nebius AI Cloud provides the infrastructure foundation for running agent workloads. Nebius Token Factory provides serverless access to models for generating tokens. DataRobot sits above these layers, providing the platform used to build, govern, and operate AI agents that rely on those models. Together, these components form the validated AI Factory stack used in this configuration:

- 

DataRobot’s Agent Workforce Platform provides the enterprise layer for building, governing, deploying, and operating AI agents.

- 

NVIDIA AI infrastructure and AI software — including NVIDIA NIM microservices and NVIDIA NeMo Guardrails integrated into DataRobot’s platform — provide the validated AI software components used to support agent execution, policy enforcement, and enterprise controls.

- 

Nebius AI Cloud provides the purpose-built infrastructure layer for running agent workloads. This includes serverless experimentation through Nebius Token Factory, as well as dedicated clusters supporting NVIDIA NIM-based deployments for sustained production inference.

## Benchmarking the stackBenchmarking the stack

To validate the performance of the solution, recent benchmarking of NVIDIA Dynamo on NVIDIA HGX B200 systems using gpt-oss-12b and the Mooncake Traces dataset on Nebius AI Cloud validates the performance characteristics of this stack:

- Up to 245,000 tokens per second total throughput on 8× HGX B200 systems;

- Time-to-first-token measured in hundreds of milliseconds under load;

- Zero-error operation in validated aggregated configurations;

- KV-aware routing improving throughput by up to 17% and reducing latency by up to 47%;

- Token processing costs as low as the order of pennies per million tokens on a single HGX B200 node.

This benchmarking exercise demonstrated that deployments integrating the NVIDIA NVLink scale up fabric deliver leading, production-ready throughput, while other configurations introduce transport-layer bottlenecks. These findings reinforce the importance of validated infrastructure design for sustained agent workloads.

These findings reinforce the importance of validated infrastructure design for sustained agent workloads. Nebius AI Cloud provides the high-performance GPU infrastructure, while Nebius Token Factory exposes optimized model endpoints with transparent token-level usage, autoscaling, and built-in access controls. DataRobot extends this foundation with the agent control layer — governance, policy enforcement, lifecycle management, and agent-level observability — required to operate AI agents safely and reliably in production environments.

For a full breakdown of benchmarking, including methodology, configuration details, and architectural analysis, see the technical blog published by DataRobot.

## Learn moreLearn more

Nebius and DataRobot will be showcasing this validated agentic AI factory stack at NVIDIA GTC 2026, taking place March 16-19 in San Jose, California.

- 

Read the press release and full technical benchmark analysis from DataRobot.

- 

Connect with Nebius (booth #713) and DataRobot (booth #104) at GTC 2026.

- 

See our sessions at GTC: Enterprise AI at Speed: Simplifying AI Factory Deployments at Scale [S81852] (Presented by DataRobot), Scale Inference Using Open Models: How Nebius Token Factory Delivers Control and Efficiency (Presented by Nebius) [S82234]

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- A validated AI Factory stack for agent workloads

- Benchmarking the stack

- Learn more

## See also

### 

From fragmented data to production-grade agents: Nebius, Nexla and Tripadvisor at NVIDIA GTC

Nexla and Nebius are partnering to deliver a production-ready data and agent stack that connects governed enterprise data with infrastructure built for sustained inference. In this post, we outline how this architecture enables multi-agent systems to move from fragmented data pipelines to reliable production workflows, and show it in action through a live “Inspiration to Trip” demo presented with Tripadvisor at NVIDIA GTC.

March 17, 2026
5 mins to read

### 

Nebius and Eigen AI partner to accelerate frontier open-source AI inference

Nebius and Eigen AI are partnering to bring optimized frontier open-source models to Nebius Token Factory. As part of the collaboration, optimized implementations of models such as DeepSeek, GLM, GPT-OSS, Kimi, Llama, MiniMax and Qwen will be published on the platform, giving developers direct access to high-performance inference through production-ready endpoints and APIs.

March 17, 2026
8 mins to read

### 

Elevating the craft: Introducing the Inference Frontier Program

Today we’re introducing the Inference Frontier Program, a new builder-to-builder initiative dedicated to production inference systems. The program surfaces real architectures, optimizations and engineering tradeoffs from teams running large-scale inference in production.

March 15, 2026
6 mins to read

Sign in to save this post
Sign In
