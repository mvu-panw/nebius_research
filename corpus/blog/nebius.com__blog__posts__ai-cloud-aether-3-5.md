# Nebius AI Cloud “Aether 3.5”: Frictionless compute for real world AI

Source: https://nebius.com/blog/posts/ai-cloud-aether-3-5

Skip to main content

At Nebius, we continuously invest in the foundations: expanding cluster capacity, improving orchestration, strengthening reliability, and optimizing performance across our AI infrastructure. Scale matters, especially when training frontier models or running production workloads at high intensity.

At the same time, scale alone is not enough. As AI moves from research to real-world deployment in robotics, industrial systems, biotech pipelines, and scientific computing, access to compute becomes just as important as raw performance. Teams need to start faster, iterate more freely, and maintain precise control without being slowed down by operational overhead.

With Aether 3.5, we focused on making Nebius AI Cloud more frictionless: more elastic, more self-service, more configurable, and more accessible to different categories of AI builders.

This release introduces new serverless capabilities, the NVIDIA RTX PRO™ 6000 Blackwell Server Edition GPU for applied AI use cases, improved cluster configuration tools, streamlined data operations, and platform-level enhancements that reduce routine complexity while preserving full control.

Our goal is simple: to remove the barriers between ideas and real-world AI solutions by providing compute that is powerful, efficient, and built to scale.

## Serverless: elastic compute without infrastructure overheadServerless: elastic compute without infrastructure overhead

A key step toward frictionless AI development is removing infrastructure management where it adds little value. With the Serverless feature set, teams can run containerized workloads without touching the infrastructure complexity. You define the workload, allocate the required resources, and run it on demand. This approach improves elasticity and shortens the path from idea to execution, while keeping costs aligned with actual usage.

Serverless AI in Nebius includes three core services designed to support different stages of the AI lifecycle: DevPods, Jobs and Endpoints. DevPods provide ready-to-use development environments for experimentation, interactive work, and early-stage prototyping. Jobs handle batch workloads such as model training, fine-tuning, evaluation, or data processing. Endpoints allow you to test model performance in a controlled, production-ready inference setup.

Together, these services reduce operational overhead and simplify iteration cycles. Teams can experiment, process data, optimize models, and deploy inference workloads without maintaining cluster infrastructure, while still working within a flexible and predictable compute environment suited for real-world AI use cases.

Jobs and Endpoints are currently available in public preview through the Nebius web console and CLI. DevPods are in private preview and are expected to become generally available in the next three months.

## NVIDIA RTX PRO 6000 Blackwell Server Edition: expanding access to applied AI workloadsNVIDIA RTX PRO 6000 Blackwell Server Edition: expanding access to applied AI workloads

We are expanding our GPU lineup with the addition of the NVIDIA RTX PRO 6000 Blackwell Server Edition, bringing a new tier of cost-effective, high-throughput compute to Nebius AI Cloud. Built on the Blackwell architecture, this GPU uniquely combines RTX capabilities with strong single-precision (FP32) performance, making it particularly suitable for applied AI workloads in areas such as robotics, physical simulations, and drug discovery.

With 96 GB of high-speed GDDR7 memory, RTX PRO 6000 Blackwell enables larger models and datasets to run efficiently on a single GPU, making it a practical option for teams optimizing inference pipelines. It offers a balanced combination of performance and cost, expanding access to high-quality compute beyond top-tier training configurations.

By adding RTX PRO 6000 Blackwell to our infrastructure, we give more teams the ability to match hardware to workload requirements, improving efficiency while maintaining the performance standards expected from Nebius AI Cloud.

Please contact your account manager to check availability; self-service access will be available at a later stage.

## Data Transfer Service: a simple service to move data between S3-compatible environmentsData Transfer Service: a simple service to move data between S3-compatible environments

Efficient data movement is a fundamental part of any AI workflow. With our new Data Transfer Service, users can easily move and replicate datasets between S3-compatible storage and across different regions within Nebius AI Cloud, without relying on manual scripts or ad hoc processes.

The service is designed to be straightforward: you define the source and destination, configure transfer parameters, and launch the operation directly from the console or via API. Transfers can be monitored throughout the process, giving users visibility and control while keeping the workflow simple and predictable.

By making intra-cloud data movement more structured and accessible, we reduce routine operational effort and help teams manage datasets more efficiently across projects and regions.

Figure 1. Configuration of Data Transfer Service

Data Transfer Service is in private preview and is expected to become generally available later next month.

## Managed Soperator: better control from the startManaged Soperator: better control from the start

We continue to evolve our Slurm-on-Kubernetes orchestration with updates to Managed Soperator, giving users more flexibility when setting up and configuring their clusters. A new configuration wizard simplifies the initial setup process, helping teams define core parameters in a structured and transparent way.

We have expanded configuration capabilities to provide deeper control over cluster architecture. Users can define Node Sets with different GPU or CPU configurations, setup partitions to manage workload priorities, and select storage options that match performance and capacity requirements. These improvements make it easier to tailor clusters to specific project needs while preserving the full control expected from a Slurm-based environment.

We have also strengthened integration with identity and access management systems, including support for enterprise SSO, enabling teams to manage access policies in line with their internal security standards.

## New Applications: faster access to all the tools you needNew Applications: faster access to all the tools you need

We have updated the Applications section of the Nebius console to make it easier to discover, select, and run the tools required for AI development. It brings together curated images, frameworks, and preconfigured environments, allowing users to start workloads without spending time on manual setup.

Figure 2. Updated navigation in the Applications marketplace

Navigation and filtering have been improved to provide a more intuitive “choose what you need” experience. Users can quickly browse categories, search for specific tools, and launch environments that match their requirements in just a few steps. In addition, we have introduced a unified product card presenting deployment options in one place. Users can now compare the benefits of each option and choose the solution that best fits their needs.

The updated Applications space also supports uploading and running any models from the NVIDIA NIM Microservices catalog, which can be deployed directly from the console. With pay-as-you-go pricing and simplified setup, this reduces time to first run and helps teams move from idea to execution faster.

## Platform improvements: Security, visibility, and operational controlPlatform improvements: Security, visibility, and operational control

Alongside new capabilities, Aether 3.5 introduces a set of platform-level improvements focused on security, transparency, and day-to-day operational efficiency. These updates strengthen the foundations of Nebius AI Cloud while keeping control in the hands of users.

We now support Kubernetes 1.33, ensuring access to the latest stability and ecosystem improvements. Encryption support has been expanded to additional boot disk configurations, reinforcing data protection across environments.

To improve visibility and troubleshooting, Kubernetes Audit Logs are now generally available, and Kubernetes Node Events are accessible with defined retention policies. Audit events can also be exported to external security systems, enabling integration with existing monitoring and compliance workflows.

We have introduced the ability to create custom boot images from user disks, and developed a Nebius plugin for Packer, allowing teams to standardize configurations and maintain consistency across cluster environments. We have refined roles and permissions model for distributors, resellers, and end customers to better align responsibilities and access rights.

Aether 3.5 also brings improvements in cost and capacity management. For NVIDIA HGX B200, we now provide a 1-GPU preset, making it easier to run ad hoc workloads. SkyPilot can now use Kubernetes Autoscaler on Nebius to search for available capacity across deployed regions and scale from zero when GPUs become available. With the public API for billing export, users can now receive FOCUS-compliant data without using object storage buckets.

Together, these improvements reduce administrative friction while strengthening governance, observability, and control across the platform.

## Documentation and transparencyDocumentation and transparency

We have also updated our documentation space, moving to a new engine with improved structure and navigation. The refreshed design makes it easier to explore services, understand configuration options, and find relevant guides more quickly.

For a detailed overview of all updates included in this release, you can refer to our changelog, where features and improvements are listed in a structured and transparent way.

## ConclusionConclusion

With Aether 3.5, we continue to strengthen the foundation of Nebius AI Cloud while making advanced AI infrastructure more accessible and easier to use. From serverless workflows and new RTX PRO 6000 Blackwell GPUs to improved cluster configuration, streamlined data mobility, and platform-level enhancements, this release is focused on reducing friction without compromising control.

As AI systems increasingly move beyond widespread foundation models into robotics, industry, healthcare, and scientific discovery, the ability to access and manage compute efficiently becomes a critical enabler. Our objective is to support teams building AI that addresses real-world challenges by providing infrastructure that adapts to their needs at every stage.

We will keep expanding our capabilities, refining our platform, and lowering barriers to entry so that more teams can experiment, iterate, and scale with confidence.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Narek Tatevosyan
VP of Product

Contents

- 

Serverless: elastic compute without infrastructure overhead

- 

NVIDIA RTX PRO 6000 Blackwell Server Edition: expanding access to applied AI workloads

- 

Data Transfer Service: a simple service to move data between S3-compatible environments

- 

Managed Soperator: better control from the start

- 

New Applications: faster access to all the tools you need

- 

Platform improvements: Security, visibility, and operational control

- 

Documentation and transparency

- 

Conclusion

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Nebius AI Cloud “Aether 3.1” release: Next-gen compute for AI operations at scale

The Nebius AI Cloud 3.1 release continues the evolution of our platform into a transparent, orchestrated, developer-first environment — where performance is accessible, capacity is visible and control feels effortless. Across new platforms based on NVIDIA Blackwell Ultra, smarter capacity management and an improved experience for both developers and platform operators, every enhancement moves us closer to that goal.

December 17, 2025
5 mins to read

### 

Nebius and Eigen AI partner to accelerate frontier open-source AI inference

Nebius and Eigen AI are partnering to bring optimized frontier open-source models to Nebius Token Factory. As part of the collaboration, optimized implementations of models such as DeepSeek, GLM, GPT-OSS, Kimi, Llama, MiniMax and Qwen will be published on the platform, giving developers direct access to high-performance inference through production-ready endpoints and APIs.

March 17, 2026
8 mins to read

Sign in to save this post
Sign In
