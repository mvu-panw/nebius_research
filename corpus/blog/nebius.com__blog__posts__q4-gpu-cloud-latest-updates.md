# Implemented in Q4: our GPU cloud’s updates

Source: https://nebius.com/blog/posts/q4-gpu-cloud-latest-updates

Skip to main content

### General updatesGeneral updates

In October, we announced the Paris (eu-west1) region availability zone will be one of the first in Europe to offer NVIDIA H200 GPUs. Please contact us to access them.

### Compute CloudCompute Cloud

- 

Added support for NVIDIA H200 GPUs on the platform.

- 

Added AMD platform configuration (cpu-d3).

- 

Added new monitoring dashboards to the console: CPU, GPU, RAM, NVIDIA NVLink metrics, NVIDIA Quantum InfiniBand metrics, Ethernet metrics.

- 

Selecting the type of public IP address (static or dynamic) is now available when creating a VM in GUI, CLI or Terraform.

### Cluster managementCluster management

Soperator

- 

Enabled sshd on worker nodes for direct, secure access and streamlined troubleshooting.

- 

Introduced support for enroot without requiring root privileges, enabling more flexible and secure containerized workflows.

- 

Added dockerd support for container runtime management.

- 

Integrated apparmor for enhanced security profiles and workload isolation.

- 

Introduced Slurm partitions to provide logical separation of resources and improve scheduling efficiency.

- 

Launched a Slurm REST API, allowing programmatic cluster management, job submission and querying cluster states.

- 

Supported CPU-only and GPU-only cluster types, enabling users to tailor their infrastructure precisely to their workload requirements.

Managed Service for Kubernetes

- 

Added load balancer support to expose services to the internet and internal networks.

- 

Added new monitoring dashboards to the console: CPU, GPU, RAM, NVIDIA NVLink metrics, NVIDIA Quantum InfiniBand metrics, Ethernet metrics.

- 

Launched a node autoscaler to dynamically add or remove nodes based on resource demands.

- 

Introduced integration with our Container Registry service for seamless image management.

- 

Enabled high availability for clusters by default, ensuring a redundant control plane at no additional cost.

- 

Added support for ReadWriteOnce block volumes with CSI over block storage in preview mode. Please contact support or your cloud solutions architect to start using them.

- 

Added support for setting up clusters in custom subnets, enabling Kubernetes clusters to connect to client’s private address space via VPN.

Container Registry

- Introduced Container Registry in preview stage, available free of charge.

### Data storeData store

Shared Filesystem

- 

Launched filesystem resize feature. Performance of the filesystem will increase for every 4 TB of size.

- 

Added support for retrieving available platforms and presets via API and CLI.

- 

Enabled resizing of filesystems and disks without requiring recreation.

Object Storage

- Added performance and consumption metrics to the console.

Managed Service for PostgreSQL

- 

Added performance metrics to the console.

- 

Added support for Run:ai.

- 

Launched private cluster endpoints (available only from the user’s VPC).

- 

Added an ability to enable and disable public cluster’s endpoints.

- 

Added pool size settings and some minor settings related to PostgreSQL cluster parameters.

- 

Added an ability to update the created cluster by changing cluster parameters (number of hosts, number of CPU, memory size), PostgreSQL parameters (password, autovacuum settings, etc.) or pooler settings.

### MLOps services and appsMLOps services and apps

Managed Service for MLflow

- 

Private and public endpoints are now supported.

- 

Added MLflow logs to the web console.

- 

Added MLflow performance metrics to the web console.

### Cloud platform featuresCloud platform features

Network

- 

Added “number of available public IP addresses” as a public quota in the console.

- 

Ability to change the range of IP addresses for a private network is now available.

- 

Wireguard VPN solution has been added for secure remote access.

Identity and Access Management

- 

Added GitHub authentication to the console.

- 

Customers now have the ability to configure their custom federations via SAML2 protocol via API.

API

- 

Released the API repository.

- 

Go SDK and Python SDK are released in preview mode. Please contact support or your cloud solutions architect to start using them.

Status page

- Now you can subscribe on incidents on the status page.

### Nebius AI StudioNebius AI Studio

- 

Our portfolio of LLMs now includes more than 30 models.

- 

The platform now supports increased rate limits of 100M+ tokens per minute and beyond.

- 

Added the newest Llama-3.3-70B-Instruct model.

- 

Added Guard models.

- 

Added specialized Med42 and Llama3-OpenBioLLM-8B models.

- 

Vision models are now also available.

- 

LoRA is available in preview mode.

To learn about the latest updates in Nebius AI Studio, check out a separate post.

Note

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

## Explore Nebius

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

We’re launching a new Nebius platform built from the ground up

We have developed a new version of Nebius platform that we believe will serve your needs even better. It is already being tested by our in-house LLM R&D team and a number of clients. Now, we are rolling it out to everyone.

October 16, 2024
4 mins to read

### 

Nebius monthly digest, November 2024

This month’s digest is our most packed so far. We’re opening pre-orders for NVIDIA Blackwell GPU-powered clusters, expanding to a new US data center in Q1 2025 and opening offices there. Both of our R&D teams, AI and hardware, shared their latest developments, and more.

December 4, 2024
2 mins to read

### 

Nebius monthly digest, October 2024

October has been so eventful that it’s hard to know where to begin. But the most important news is that you can now take advantage of the newly rebuilt Nebius platform! We also delivered a keynote at TechCrunch Disrupt, reduced prices dramatically, celebrated 1 year since our public launch — and more.

November 4, 2024
2 mins to read

Sign in to save this post
Sign In
