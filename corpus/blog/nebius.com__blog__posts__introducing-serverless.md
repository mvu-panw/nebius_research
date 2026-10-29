# Introducing DevPods, Jobs and Endpoints: Easy compute access with serverless AI

Source: https://nebius.com/blog/posts/introducing-serverless

Skip to main content

If you work with AI infrastructure, you know how much effort it can take to get production-ready compute up and running. Modern AI stacks span multiple layers — servers, accelerators, drivers, libraries, virtualization, orchestration, networking — and aligning all of them into a stable environment often requires weeks of work from an experienced DevOps team.

At the same time, many AI use cases don’t need a permanently provisioned cluster. Data scientists want to run experiments, ML engineers want to test training scripts and validate model inference behind real endpoints — all without waiting for long-lived infrastructure to be designed, provisioned and validated.

At Nebius, we’re focused on making advanced AI compute accessible and practical for a broad range of users. As part of this direction, we’re introducing DevPods, Jobs and Endpoints — new services that represent our first steps toward container-based serverless compute for AI workloads.

These services are designed to hide most of the underlying infrastructure complexity, allowing ML engineers and data scientists to focus on model development, experimentation and evaluation. Compute resources are provisioned on demand, while cluster management, GPU drivers and networking are handled by the platform.

## How serverless benefits AI practitionersHow serverless benefits AI practitioners

Originally, the serverless concept referred to Function-as-a-Service (FaaS) platforms such as AWS Lambda or Google Cloud Functions, where users execute short-lived functions on demand without provisioning or managing servers, virtual machines or clusters. Over time, this model evolved to support containerized applications, expanding serverless to a broader range of workloads.

Despite differences in implementation, most serverless platforms share several common characteristics:

- 

On-demand workload lifecycle — Compute resources are provisioned in response to triggers and released when the workload completes.

- 

Pay-per-use pricing — Users only pay for the time during which compute resources are actively allocated, thereby reducing costs associated with idle capacity.

- 

Infrastructure invisible for users — The cloud provider is responsible for provisioning, scaling and maintaining the underlying infrastructure.

In the world of AI, container-based serverless platforms have become a practical middle ground, enabling teams to accelerate different stages of the model development pipeline — from faster experimentation to scalable and cost-conscious model inference.

With this approach, data scientists and ML engineers can access AI compute almost immediately, without waiting for a DevOps team to provision clusters, install GPU drivers or configure networking for public endpoints.

Figure 1. Serverless compute compared to other models of AI compute

To get started, practitioners package their training code or model artifacts into a container and submit it to the serverless platform. The infrastructure below that layer is already provisioned, tested and managed by the provider, allowing teams to focus on running and evaluating their workloads rather than on environment setup (Figure 1).

In an environment where accelerators are scarce and expensive, this allows ML teams to run AI workloads without reserving large GPU clusters in advance and carrying out the overheads of idle resources.

## DevPods, Jobs and Endpoints: Develop, run and serve with zero hassleDevPods, Jobs and Endpoints: Develop, run and serve with zero hassle

DevPods, Jobs and Endpoints are three new services in Nebius AI Cloud that implement a container-based serverless approach to AI compute. Each of them is fully managed on our side and are designed to give users a simple way to run AI and ML workloads without provisioning or maintaining long-lived infrastructure.

To start working with either service, users can provide their own container image or specify the path to a public image and define basic configuration parameters. This includes selecting the available GPU type in the region and, if needed, mounting an object storage bucket or file system for datasets and artifacts. The rest of the infrastructure lifecycle is handled by the platform.

Jobs and Endpoints are currently available in public preview through the Nebius web console and CLI. DevPods are in private preview and are expected to become generally available in the next three months.

### DevPodsDevPods

DevPods are interactive development environments powered by GPU or CPU, designed for coding, debugging and exploratory work. The service serves as a developer playground for interactive coding in Jupyter or VS Code, exploratory data analysis and visualization, prototyping model ideas, and debugging running jobs or inference tasks.

The primary use case for DevPods is to quickly provision an interactive environment for human-in-the-loop development. These environments are not production-facing and therefore do not require production-grade stability or security, but they do require fast startup and rapid shutdown once work is complete.

An alternative approach would be to spin up a VM and install a development stack each time you need compute for prototyping. This process is tedious, requires infrastructure engineering effort and can incur unnecessary costs when GPUs remain idle during setup (see Figure 2).

Figure 2. Comparison of VM-based and serverless workflows: serverless reduces setup overhead and idle GPU utilization

### JobsJobs

Jobs provide a simple orchestration mechanism for running finite workloads on allocated GPU or CPU-only resources. The service is well-suited for use cases such as batch data processing, model training experiments or scientific simulations.

In its current form, Jobs are optimized for single-node workloads and simplified execution flows. As a result, the service is not intended for large-scale or highly complex distributed training scenarios.

### EndpointsEndpoints

Endpoints provide a serverless compute engine with pre-configured web endpoints, enabling users to deploy custom models and make them accessible via HTTP within minutes. In the current version, the service is particularly well-suited for pre-production deployments and testing scenarios, where teams want to evaluate model behavior under realistic conditions.

The longer-term roadmap for Endpoints focuses on enabling auto-scaling capabilities for a full-fledged model that combines simplicity with greater control over the inference runtime and configuration.

These serverless tools expand the variety of options for seamless ML development available on the Nebius cloud platform, enabling ML engineers to progress in their pipelines without halts and extra costs. They can start prototyping quickly with DevPods and Jobs, scaling the training with orchestrators like Managed Soperator and evaluating production models with Endpoints.

## Current limitations and upcoming changesCurrent limitations and upcoming changes

The Jobs and Endpoints services are being launched in public preview to give users early access to a container-based serverless experience for AI workloads. DevPods are expected to become publicly accessible in mid-April. At the same time, we recognize that the current functionality represents an initial stage, and that several core capabilities typically associated with mature serverless platforms are still under development.

The table below outlines the functionality available today, along with a set of core capabilities that are planned as part of the general availability (GA) roadmap. These timelines reflect our current plans and may evolve as development progresses.

 | 
 | Q1 2026
 | Q2–Q3 2026
 | Q4+ 2026

 | Startup latency
 | Slow
 | Moderate
 | Optimized

 | Observability
 | Logging, Basic monitoring
 | Logging, Advanced monitoring
 | Logging, Advanced monitoring

 | Monitoring
 | Basic
 | Improved
 | Improved

 | Health checks
 | Basic
 | Advanced
 | Advanced

 | Serverless for reserved capacity
 | —
 | Yes
 | Yes

 | Single-node cluster support
 | Yes
 | Yes
 | Yes

 | Multi-node cluster support
 | —
 | Jobs
 | Jobs, Endpoints

 | Multi-region scheduling
 | —
 | Jobs
 | Jobs, Endpoints

 | Autoscaling
 | —
 | —
 | Endpoints

## Elastic compute over the robust platformElastic compute over the robust platform

The serverless services at Nebius are a natural extension of how an AI infrastructure cloud evolves over time, building on a mature and well-established underlying platform. As the platform develops, it becomes possible to expose compute in more flexible and elastic forms that better match how AI workloads are consumed.

While DevPods, Jobs and Endpoints are still evolving, the underlying platform is built to support reliable, high-performance and elastic AI compute as additional features are introduced. In particular:

- 

We maintain control over the infrastructure lifecycle, including server design, firmware and cluster-level monitoring for proactive hardware health management.

- 

The platform is designed to support secure and compliant compute environments, and aligns with common industry standards and regulatory requirements.

- 

Virtualization is implemented with minimal overhead and delivers a bare-metal level of performance, as demonstrated by public benchmark results, including MLPerf submissions.

This foundation provides a strong basis for expanding serverless capabilities over time.

## How to get startedHow to get started

New serverless tools are available in self-service mode through the Nebius web console and via the CLI, making it easy to start running AI workloads without upfront reservations or long-term commitments.

To get started, sign in to the Nebius console, navigate to AI Services in the left-hand menu and select the service you need. From there, choose from the available GPUs in your region and configure the required runtime settings. If needed, you can also mount object storage or a file system to provide access to data and store results.

DevPods, Jobs and Endpoints use pay-as-you-go pricing based on on-demand compute rates and apply only while workloads are running.

For detailed configuration options and examples, refer to the documentation.

Interested in Serverless AI and want to learn more from Nebius experts? Register for our upcoming virtual events:

- April 9 (Thursday) — Serverless for AI in 2026

- April 16 (Thursday) — Serverless AI for developers

- April 23 (Thursday) — Serverless AI for Life Sciences

- May 5 (Tuesday) — Serverless AI for Robotics and Physical AI

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Mikhail Rozhkov
Technical Product Manager

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- 

How serverless benefits AI practitioners

- 

DevPods, Jobs and Endpoints: Develop, run and serve with zero hassle

- 

DevPods

- 

Jobs

- 

Endpoints

- 

Current limitations and upcoming changes

- 

Elastic compute over the robust platform

- 

How to get started

## See also

### 

Nebius and Eigen AI partner to accelerate frontier open-source AI inference

Nebius and Eigen AI are partnering to bring optimized frontier open-source models to Nebius Token Factory. As part of the collaboration, optimized implementations of models such as DeepSeek, GLM, GPT-OSS, Kimi, Llama, MiniMax and Qwen will be published on the platform, giving developers direct access to high-performance inference through production-ready endpoints and APIs.

March 17, 2026
8 mins to read

### 

Delivering a validated AI Factory stack for agent workloads on Nebius AI Cloud with DataRobot

At NVIDIA GTC 2026, Nebius and DataRobot, with NVIDIA, introduced a validated AI Factory stack for production-grade agent workloads. In this post, we outline how the DataRobot Agent Workforce Platform runs on Nebius AI Cloud to support sustained inference, governance and cost control for AI agents deployed in live business workflows.

March 18, 2026
7 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
