# Nebius and Outerbounds form strategic technology partnership through integration

Source: https://nebius.com/blog/posts/nebius-outerbounds-strategic-technology-partnership-integration

Skip to main content

# Key benefits of Nebius AI Cloud for powerful integrationKey benefits of Nebius AI Cloud for powerful integration

Our mission at Nebius is to democratize AI infrastructure by empowering innovation and growth through high-performance, scalable, cost-effective and secure AI cloud solutions. Nebius AI Cloud is dedicated to unlocking the full potential of modern applications, data analytics and AI workloads, while delivering exceptional customer experiences, to drive the future of cloud computing for AI.

Today, we bring powerful full-stack infrastructure for AI developers and practitioners across startups, enterprises and science institutes to build and deploy generative AI applications and rapidly deliver scientific breakthroughs by training and running ML models within a secure, high-performance and cost-optimized cloud environment. The platform’s structure adheres to industry standards, with Compute Cloud as the key infrastructure service, enabling users to manage virtual machines that are equipped with NVIDIA GPUs and available in our global data centers. Managed Service for Kubernetes® handles multi-node deployment of these machines and orchestration, with routine cluster maintenance stages handled by Nebius.

Another essential component of our cloud is S3-compatible Object Storage. The service offers secure, scalable and cost-effective storage, allowing you to efficiently access, share and manage vast amounts of unstructured data.

To understand how Nebius AI Cloud integrates with Outerbounds, it is also important to discuss Managed Service for PostgreSQL® from the PaaS segment of our platform. Managed PostgreSQL provides a reliable and convenient solution for storing structured data in the cloud, with maintenance, deployment and other processes also handled by us under a managed concept. PostgreSQL is widely used in our field for various purposes, including model development and AI apps.

# Metaflow: Developer-friendly APIs for the full stack of AI and MLMetaflow: Developer-friendly APIs for the full stack of AI and ML

Metaflow was originally developed at Netflix to streamline and support a wide range of internal ML and AI use cases, including computer vision, custom deep learning models and causal inference. In 2019, Netflix open-sourced Metaflow, leading to its rapid adoption by top ML and AI teams at companies like Goldman Sachs, Ramp, GE Healthcare, Amazon Prime Video, Zillow and many others.

Metaflow was built to access a common challenge, faced by all ML and AI teams: How to equip developers with a toolchain, natively in Python, which grants them easy access to the full stack of infrastructure needed by real-world ML and AI projects, covering:

- High-throughput, secure access to data

- Various forms of scalable compute

- Production-grade workflow orchestration

- Comprehensive tracking and versioning

- Support for various deployment patterns

Building on this robust infrastructure stack, developers have the flexibility to design and deploy complete ML/AI systems using their preferred modeling frameworks, including XGBoost, PyTorch, TorchTune, DeepSpeed and more.

# Nebius + Metaflow = Full stack AI, backed by top-notch infrastructureNebius + Metaflow = Full stack AI, backed by top-notch infrastructure

Through our collaboration with Outerbounds, the company founded by Metaflow’s creators, we have ensured that Metaflow integrates smoothly with Nebius, enabling a development experience that combines Metaflow’s API with Nebius’ AI infrastructure.

The result is a seamless, full-stack AI toolchain where:

- 

Metaflow provides a rich set of stable, production-ready and easy-to-use APIs that help develop ML/AI-focuses workflows quickly, run them at scale and deploy to production confidently.

- 

As said, Nebius provides a complete stack of backend services for Metaflow projects, including Object Storage and metadata databases, as well as deep and broad access to compute resources, orchestrated through Managed K8s. Nebius AI Cloud infrastructure offers high-performance capabilities, enabling rapid processing for intensive ML and AI workloads. Users benefit from flexible scaling, allowing them to dynamically adjust capacities based on real-time needs, optimizing cost efficiency and performance.

This code snippet shows how Metaflow APIs map to managed services provided by Nebius:

Click to view raw

Get started with Metaflow on Nebius by following deployment readme on GitHub.

# Nebius + Outerbounds = Enterprise-ready AI InfrastructureNebius + Outerbounds = Enterprise-ready AI Infrastructure

Outerbounds was founded by the creators of Metaflow to address recurring needs of companies that use Metaflow to power business-critical applications. While Metaflow provides a robust technical foundation for ML/AI projects, many enterprises have a number of additional needs related to their organizational setup and bespoke development workflows:

- 

How to secure Metaflow projects, integrating them to the company’s existing user identities, security policies and data governance rules.

- 

How to manage multiple environments, such as staging and production and CI/CD workflows between them.

- 

How to manage multiple compute pools and complex compute workloads, including fine-tuning and distributed training of GenAI models cost-efficiently.

- 

How to manage dependencies and containerize projects automatically with minimal overhead.

- 

How to equip developers with cloud-based, secure development environments.

The Outerbounds platform runs securely in the customer’s cloud accounts, following the Bring-Your-Own-Cloud (BYOC) deployment model. As a result, Outerbounds is the platform of choice for many business-critical applications in financial services, large-scale workloads in life sciences and state-of-the-art fine-tuning of large-scale custom AI models, amongst many other use cases. Thanks to BYOC, the customer doesn’t have to pay any extra markup on compute, making the platform especially suitable for compute-heavy workloads requiring cost-efficient access to compute at scale.

We have partnered with Outerbounds to create a first-class integration between the Outerbounds platform and Nebius AI Cloud, empowering even the most demanding ML and AI teams with seamless access to cutting-edge resources. Nebius’ and Outerbounds’ integration enables teams to rapidly iterate, deploy sophisticated models and streamline AI development, significantly reducing time-to-market while ensuring reliability and efficiency at every stage.

# Example: A production-grade workflow for LLM finetuningExample: A production-grade workflow for LLM finetuning

To see the stack in action, watch the video demonstrating the fine-tuning process of a large language model:

- 

Nebius is included as a compute pool in Outerbounds, allowing you to access top-notch hardware resources in our Compute Cloud without having to rewrite code or change your security policies, defined through Outerbounds’ unified control plane.

- 

You can use Nebius seamlessly alongside your existing cloud resources, without having to migrate data or existing workloads.

- 

Develop projects rapidly on Outerbounds cloud workstations which can be configured to have direct access to Nebius, allowing developers to iterate quickly with state-of-the-art hardware.

- 

The example uses Torchtune for fine-tuning, orchestrated by Metaflow that provides a rich, battle-hardened feature set for building end-to-end ML/AI systems, allowing you to build reactive production systems, not just one-off experiments.

- 

Thanks to the integration, you can execute the workflow on Nebius with a single command — just add @nebius in the workflow — optionally running parts of the workflow in your existing cloud environments.

- 

Outerbounds takes care of containerizing the project automatically in a few seconds, removing a key source of friction when execution workloads remotely.

- 

You can observe the run on the Outerbounds UI, leveraging real-time @cards to visualize progress and results.

- 

The integration supports efficient @model loading, avoiding expensive data egress between clouds.

- 

The example task runs on one compute node. For larger models, you can leverage Metaflow’s support for distributed training, powered by interconnected Nebius clusters.

- 

Metaflow’s @checkpoint is integrated with our Object Storage, allowing you to build resilient training and finetuning workflows.

- 

The stack provides a developer-friendly, rapid development experience using off-the-shelf tools like Torchtune, combined with a paved path to production and best practices for CI/CD, development workflows and continuous improvement of production systems.

- 

The stack is not a black box: You have full visibility to all operational metrics of your workflows, thanks to in-depth infrastructure monitoring provided by Nebius, as well as cross-cloud cost optimization tools available in the Outerbounds UI.

The video succinctly demonstrates the critical role of a seamlessly integrated stack in production-grade generative AI systems. These systems combine advanced models, meticulously orchestrated data processing and business logic, all running on cutting-edge infrastructure — continuously refined through iteration and improvement by human developers.

The Nebius-Outerbounds partnership will continue to evolve. We plan to add support for additional cutting-edge GPUs, expand our range of managed services available to Outerbound users and further enhance our integration to ensure the experience of using Nebius with Outerbounds is as efficient as possible.

# SummarySummary

The new Nebius-Outerbounds stack provides a complete, developer-friendly solution for building business-critical AI/ML systems powered by state-of-the-art computational resources:

- Nebius provides top-notch AI infrastructure optimized for Generative AI workflows.

- Metaflow provides a popular, battle-hardened, developer-friendly software stack for architecting end-to-end ML/AI systems.

- Outerbounds provides a unified, managed platform, allowing you to develop, deploy and scale Metaflow workflows securely across your cloud accounts, and now on Nebius.

You can start building with the stack today!

# Getting startedGetting started

To get started:

- Sign up for Nebius AI Cloud

- Contact Outerbounds to start a free trial and connect Nebius AI Cloud

- Join Metaflow community on Slack for open-source Metaflow support.

## Explore Nebius AI Cloud

Compute Cloud​
Managed Kubernetes​
Object Storage​
Managed PostgreSQL​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alex Salikov
Head of External Solutions Department

Ville Tuulos
CEO and Co-Founder at Outerbounds

Contents

- Key benefits of Nebius AI Cloud for powerful integration

- Metaflow: Developer-friendly APIs for the full stack of AI and ML

- Nebius + Metaflow = Full stack AI, backed by top-notch infrastructure

- Nebius + Outerbounds = Enterprise-ready AI Infrastructure

- Example: A production-grade workflow for LLM finetuning

- Summary

- Getting started

## See also

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

Slurm vs Kubernetes: Which to choose for model training

Scaling your machine learning workloads will eventually require resource orchestration. This article compares the most popular options today — Slurm and Kubernetes, covering their design origins, ML adaptations and other factors to consider.

May 29, 2024
13 mins to read

### 

On Kubernetes significance for ML/AI engineers

K8s has become the tool of choice for machine learning teams large and small. What are its properties that have made it today’s industry standard?

November 14, 2023
7 mins to read

Sign in to save this post
Sign In
