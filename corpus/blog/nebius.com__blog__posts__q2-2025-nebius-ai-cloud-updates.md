# Q2 2025: Nebius AI Cloud updates

Source: https://nebius.com/blog/posts/q2-2025-nebius-ai-cloud-updates

Skip to main content

This quarter, we focused on improving cluster reliability through enhanced autohealing mechanisms and health checks, optimizing performance with extended topology-aware job scheduling and making the cloud more user-friendly for AI developers. We also introduced NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters into production, expanding the range of cutting-edge hardware available on the platform.

# AI clusters got fasterAI clusters got faster

Over the last quarter, we hit several milestones and introduced upgrades to ensure high performance on Nebius AI Cloud:

- 

We submitted MLPerf® Training v5.0 results, achieving top-tier performance by training a Llama 3.1 405B model on 512 and 1,024 NVIDIA Hopper GPU clusters. We recorded training step times of 124.5 minutes on a 128-node cluster and 244.6 minutes on a 64-node cluster. This demonstrates the near-linear scaling of Nebius infrastructure — a 1.97x speedup when doubling the cluster size.

- 

Topology-aware job scheduling is now available for various job schedulers, including Slurm, Kubernetes, Volcano, Kueue and others. Our NVIDIA NCCL tests showed average performance improvements of 10–25%, depending on benchmark parameters. We also integrated NVIDIA Topograph to streamline topology ingestion when needed.

- 

Our ISEG2 system ranks #13 on the Top500 list of the world’s fastest supercomputers, with peak performance of 338.49 PFLOP/s, making it the most powerful commercially available system in Europe and the second worldwide.

# Improved cluster reliabilityImproved cluster reliability

Another focus of our engineering and research efforts this quarter was improving cluster reliability and resiliency. We’ve made a significant step forward by increasing the MTBF metric to 168,000 GPU hours on average per week for a 3,000-GPU cluster. Several factors contributed to this result — here are some of the most tangible ones:

- 

Autohealing capabilities and health checks for Slurm-based clusters have been significantly improved. If a node fails a health check, it gets automatically drained and replaced — all while your training jobs continue running without interruption.

- 

We also introduced this health check framework for virtual machines and Kubernetes clusters, making sure your training processes run seamlessly and providing a consistent, reliable experience across all platform services.

# Upgraded storage for AI workloadsUpgraded storage for AI workloads

Our storage solutions saw several major enhancements:

- 

Continued improvements to Shared Filesystem led to impressive benchmarks — on a 302-host production cluster, we achieved 442 GB/s aggregated write and 987 GB/s aggregated read performance. For larger clusters, we expect read throughput to exceed 1 TB/s.

- 

We now support third-party solutions powered by WEKA and VAST, expanding the range of options for AI-optimized storage.

- 

A new class of Object Storage, designed for streaming data to NVIDIA GPUs and checkpointing, offers up to 2 GiB/s write throughput per GPU.¹

- 

We launched a data migration service that enables clients to transfer large datasets from any S3-compatible source, without deploying additional infrastructure.

# Operational simplicity enhancementsOperational simplicity enhancements

To streamline day-to-day workflows for AI developers, we introduced several major improvements:

- 

Managed Soperator, our fully managed Slurm solution, is now generally available as a one-click, self-service option. You can spin up a training-ready GPU cluster in minutes, with preinstalled libraries and drivers.

- 

On the Kubernetes side, we introduced a graceful node termination handler that ensures smooth eviction and rescheduling of workloads from unhealthy nodes.

- 

Observability was significantly improved with out-of-the-box Grafana dashboards (available via the Grafana marketplace), enhanced logging and expanded performance metrics. Users can now write custom telemetry to the cloud as well.

Click to expand

# Enhanced tools for AI developersEnhanced tools for AI developers

We continue to expand our MLOps capabilities and third-party integrations:

- 

Simplified pricing for Managed MLflow, faster startup times for JupyterLab in Standalone Applications, several new app launches and support for NVIDIA H200 GPUs as an underlying resource.

- 

SkyPilot now can launch any workload with a single sky launch --gpus H100:8 --cloud nebius command. It now supports NVIDIA Quantum-2 InfiniBand and Filesystem, enabling distributed training and inference.

- 

dstack is now integrated with Nebius, allowing you to manage dev environments, execute training jobs and run distributed workloads with full NVIDIA Quantum-2 InfiniBand and Filesystem support.

- 

We started developing integrations with Union.AI (Flyte) and Anyscale. At this stage, both can be installed on Nebius AI Cloud by following the official vendor manuals. These early steps pave the way for native integration and tighter collaboration in the future.

# New milestones in NVIDIA partnershipNew milestones in NVIDIA partnership

- 

NVIDIA AI Enterprise is now available on Nebius, supporting national AI projects and enterprise-grade use cases with access to NVIDIA NIM microservices, NVIDIA NeMo and other foundational components.

- 

Nebius resources are now accessible via NVIDIA DGX Cloud Lepton™, an AI platform with a compute marketplace that connects developers with tens of thousands of GPUs, available from a global network of cloud providers.

- 

Nebius is also now available through NVIDIA DGX Cloud Serverless Inference, offering a cost-efficient, auto-scaling GPU inference platform with multi-cloud flexibility.

# Security and complianceSecurity and compliance

- 

The Audit Logs service is now available in public preview. This new capability provides customers with a complete record of all significant actions taken within their cloud platform. It helps track changes, detect security incidents and meet compliance requirements.

- 

To increase transparency around security and privacy updates, we’ve launched a Trust Portal on our website — a centralized place to access the latest information about how we protect your data.

- 

Identity and Access Management (IAM) has been substantially improved. Now, you can create and manage multiple projects within a single region, create custom groups within a tenant or project, and change tenant names. Read more in the documentation.

# User experience enhancementsUser experience enhancements

There were many minor and major UI and UX changes last quarter aimed at making Nebius AI Cloud simpler and more convenient to use. Here are a few highlights:

- 

Nebius MCP Server has been launched. You can now control, monitor and manage your AI infrastructure through an LLM-based chatbot of your choice. We love using Claude by Anthropic — chatting with the platform and receiving clear, structured responses is both fun and efficient.

- 

GPU compute quotas for self-service users have increased — up to 32 GPUs can now be used without having to contact the support team.

- 

Container images are now available to provide users with one pre-built or any custom container directly from the VM creation page. It removes unnecessary friction, saving you time during the initial configuration stage.

- 

We continue improving billing and cost transparency. One of the most requested updates — the pricing calculator — is now available for several services, so users can quickly estimate the cost of their selected configuration.

- 

Among other UI changes: the “Save your SSH key” widget now simplifies the system administration process and adds a smoother touch to cluster management tasks.

- 

Another usability improvement is context-aware documentation links in the top-right corner of each page in the web console. For example, pages in the Compute section link to VM and cluster documentation, while the Network section links to VPC setup guides.

- 

We introduced Trial statuses at the top of the console UI, to allow users to see their remaining balance, hourly usage and remaining duration of the trial.

All of these updates reflect our continued commitment to delivering a reliable, efficient and developer-friendly AI Cloud. We’re excited about what’s coming next — stay tuned for even more innovation in the upcoming quarter.

¹ Depends on the structure of data stored in the bucket, write concurrency and configuration of upload process parameters. ↵

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- AI clusters got faster

- Improved cluster reliability

- Upgraded storage for AI workloads

- Operational simplicity enhancements

- Enhanced tools for AI developers

- New milestones in NVIDIA partnerships

- Security and compliance

- User experience enhancements

## See also

### 

Q1 2025: Nebius AI Cloud updates

The end of the quarter is a great time to reflect and share a kind of changelog with you, highlighting what’s improved in Nebius AI Cloud over the past three months. This quarter, we launched new regions, released new services for MLOps and enhanced our existing product lineup to minimize your infrastructure concerns even further.

April 9, 2025
7 mins to read

### 

Nebius AI Studio Q2 2025 updates

We kicked off Q2 with a single mission: turn raw compute horsepower into concrete business outcomes. With numerous launches, including groundbreaking models, streamlined fine-tuning, scalable throughput and seamless integrations, Nebius AI Studio has been updated significantly.

July 1, 2025
3 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
