# Q1 2025: Nebius AI Cloud updates

Source: https://nebius.com/blog/posts/q1-2025-cloud-updates

Skip to main content

### General updatesGeneral updates

This quarter, we announced the deployment of several more data center regions. The data center in New Jersey, built by our partner DataOne, will be dedicated solely to NVIDIA Blackwell-architecture GPUs. We will also be colocating a cluster of NVIDIA H200 GPUs at Verne’s data center campus in Iceland. Additional information about the availability of these regions will be released soon.

### Compute CloudCompute Cloud

- 

As we add more and more regions, we changed our compute instance creation interface — it now displays all available platforms in Nebius for a selected project, regardless of region. If a platform isn’t available in the region of the current project, it is easy to switch to a different project to access it.

- 

Our hardware monitoring system has been improved. Every time a system detects an issue on the hardware level, it sends a notification to other components of the cloud stack, enabling them to perform autohealing actions. The system also allows customers to receive notifications via email, API or Slackbot.

### Cluster managementCluster management

Managed Service for Kubernetes

- 

This service has been integrated with the hardware monitoring system. Cluster nodes with detected issues will be tagged with taint to prevent new workloads from being scheduled here. By default, you will receive a maintenance notification to stop-start this node manually, but you can also create your own automation to react on such failures, like combining capabilities of our cluster autoscaler and Draino or Descheduler, to remove such nodes from the cluster automatically.

- 

The CoreDNS customization mechanism has been released. CoreDNS is a key component in Kubernetes. Customizing CoreDNS allows clients to tune it to fit their needs.

- 

Kubernetes images with pre-installed GPU and network drivers are now available for our clusters. The boot image significantly reduces node provisioning time and node management overhead.

- 

Kubernetes default Cilium CNI now comes with Hubble enabled by default. Hubble is an observability layer built on top of Cilium, which provides powerful network visibility features for Kubernetes environments. Hubble offers deep visibility into network communications between services, pods and containers.

- 

Hubble and Cilium metrics are now shipped to Grafana and Prometheus that are available in Applications for Managed Kubernetes.

Container Registry

- Container Registry became publicly available. The service has increased stability and performance, to handle many more parallel requests. Thanks to Static Token support, it’s become much easier to integrate Container Registry into CI/CD tools such as Argo CD.

Slurm-based clusters (Soperator)

- 

Node autohealing has been introduced, to replace faulty nodes automatically and minimize disruptions to customer training jobs.

- 

Cluster inline health checks have been added to identify and isolate problematic nodes quickly, to prevent job scheduling on compromised hardware.

- 

Topology-aware training is now enabled, significantly enhancing training efficiency by optimizing for cluster topology.

- 

Automated jail backups have been activated, automatically backing up user data to ensure reliability and data protection.

- 

A comprehensive job monitoring dashboard is now available, providing detailed visibility into job workloads and enhancing operational insights.

### Data storeData store

Shared filesystem

- 

Hot size up for the Nebius Shared Filesystem is available. A customer can now size up a filesystem on a running instance.

- 

Cold attach and detach for the Nebius shared filesystem is available. A customer can now attach or detach a filesystem to a stopped instance, without re-creating the virtual machine.

Network disks

- Cold attach and detach for disks is available. A customer now can attach or detach a secondary disk to a stopped instance, without re-creating the virtual machine.

Object Storage

- 

Increased network throughput between GPU nodes and Object Storage (also mentioned in Network).

- 

Introduced the “Enhanced” Object Storage class to private preview, allowing ~5x more read and write throughput per TB of utilized S3 bucket capacity.

Managed Service for PostgreSQL

- 

Released Managed Service for PostgreSQL to GA.

- 

Introduced SLA and increased service stability.

- 

Cluster monitoring dashboard is now enriched with additional information about database performance, replication parameters and connection pooler performance.

- 

Backups management: Users are now able to view restore their backups by using an API, CLI or Console UI.

### MLOps services and appsMLOps services and apps

Managed Service for MLflow

- 

Released Managed Service for MLflow to GA.

- 

Increased default resources and quotas for the MLflow cluster.

- 

Improved services reliability by migrating a metadata database to Managed PostgreSQL.

- 

Updated MLflow version to 2.20.2.

Standalone Applications

- Released JupyterLab in the Standalone Applications service.

Integrations

- 

We’ve successfully implemented integrations with Metaflow and Outerbounds, creating a more connected and versatile cloud experience. The Metaflow integration allows data scientists to build and deploy data workflows that transition smoothly between local development and Nebius AI Cloud resources. The Outerbounds integration further enriches our ML platform ecosystem, with additional enterprise-grade capabilities. With several clicks, you can deploy Metaflow on Nebius AI Cloud. For more information, see Metaflow on Nebius AI Cloud: Minimal viable stack. Additional details are available in our blog.

- 

We have also implemented integration with SkyPilot, an open-source framework that simplifies running AI and batch workloads across cloud platforms. For more information, see Running AI workloads on Compute virtual machines by using SkyPilot.

- 

Nebius was also confirmed as an ecosystem partner for NVIDIA Dynamo, an open-source inference serving framework for deploying generative AI in large-scale distributed environments. NVIDIA Dynamo provides the most efficient solution for scaling test-time compute. Dynamo on NVIDIA Blackwell boosts through put on DeepSeek-R1 by 30x. For access to the private preview, please contact your manager, CSA or Support.

### Cloud platform featuresCloud platform features

Monitoring and logging

- 

Open monitoring and logging has opened for preview. Contact Support or CSA for access.

- 

Added an API errors graph to Object Storage.

- 

Our customers can now set up service provider alerts to be delivered via email.

Network

- 

Increased network throughput between GPU nodes and Object Storage.

- 

Dedicated private address space per region, to avoid inter-region IP conflicts.

- 

Released an update to the network interfaces API. Guest VM OS network interfaces names now match the names in the resource specification.

- 

VPC becomes a full-fledged cloud service. Network and subnets management are available via the public API and console.

Identity and Access Management

- 

Provided IAM enhancements to power other services with authentication.

- 

Implemented functionality in the public API to allow users to provide more granular access (not only four predefined groups). There is currently no support for the Console, only gRPC/CLI/TF. Documentation is upcoming.

- 

Implemented functionality of user-defined project creation. The admins of a tenant can create new projects in publicly available regions.

API

- 

Nebius CLI now supports editing resources via a text editor, for easy updating of existing resources.

nebius compute gpu-cluster edit --id computegpucluster-e00p******** --editor nano

- 

The Go SDK has been released. For more information, see GoSDK on our GitHub.

- 

The Python SDK has been released in preview. For more information, see PySDK.

Billing

- 

Promo codes: Whether you’re running a startup, are part of a research team or a Fortune 500 company that’s comparing cloud providers, you can now easily enter a promo code and get credits directly in your account.

- 

GPUs for the people: We’ve increased our default quotas, including for H200s, so you can get started with training and inference even faster.

- 

Documentation availability: Documentation is now easier to find, with improved linking in our console.

- 

Reserves: Getting the best price for reserving resources or Committed Usage Discounts is now simpler to dive into by using improved graphs and tables.

Notification management

- Subscriptions management is now available via the console, from the user menu in the top right corner, for all users; or directly by using this link. Users can now change their subscription settings for tenant-level and billing notifications.

Customer support

@nebius_support has arrived! Seamless support in Slack for customers who have account managers — just tag, ask and then follow up in Slack or our Support Center. Please contact your account manager or CSA to enable the bot in your Slack channel.

More updates and new MLOps product releases to come in Q2! We’re continuously improving Nebius AI Cloud to ensure greater reliability, user convenience and observability.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

Nebius monthly digest: March 2025 and NVIDIA GTC

NVIDIA GTC was the highlight of last month for us. Our extensive participation included being a platinum sponsor, a strong presence with the booth, two tech talks, interviews with our leaders, partners and customers, and much more.

April 7, 2025
4 mins to read

### 

Q4: Nebius cloud updates

After completing a full rewrite of our cloud from the ground up in October, we began improving the foundation that we brought to the market. The features and tools we have introduced since then span our entire range of cloud services, from Compute Cloud with NVIDIA accelerated computing in a new region, to managed MLOps solutions.

December 18, 2024
4 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
