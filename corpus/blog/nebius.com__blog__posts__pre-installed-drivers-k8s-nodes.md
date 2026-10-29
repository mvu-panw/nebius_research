# Pre-installed drivers are now available for Kubernetes nodes

Source: https://nebius.com/blog/posts/pre-installed-drivers-k8s-nodes

Skip to main content

Preparing a GPU cluster requires some effort and careful attention from your engineering team. It can become a significant challenge in terms of deploying and configuring a compute environment.

Today, we’re happy to announce a small yet meaningful enhancement that makes the cluster preparation process much easier and faster: Managed Service for Kubernetes can now start a node with an AI/ML-ready image. This image includes drivers for NVIDIA GPUs, drivers for NVIDIA Quantum InfiniBand-based networking and other components required for the proper operation of a GPU-accelerated environment.

### Faster compute provisioningFaster compute provisioning

Having this new type of image significantly reduces the time for deploying nodes in Kubernetes clusters. We expect this update will accelerate node start-up, making it up to 3x faster than when using the driverless K8s image. This doesn’t just shorten the time to value for our customers — it brings more scalability and efficient compute provisioning for GPU clusters.

In particular, it will make a big difference for model inference installations. Quick node initialization allows for rapid cluster scaling when demand increases and additional capacity needs to be provisioned.

### Enhanced UX and availabilityEnhanced UX and availability

Pre-installed drivers also make the setup process and maintenance more user-friendly and hassle-free for all Nebius users. You won’t need to figure out the list of required software, search for installation packages, install the components, or ensure that the cluster is ready to use. The installation process, as well as the driver update process, requires additional expertise — GPU and network operators have many dependencies, making troubleshooting and maintenance complex and challenging for administrators.

With this new approach, all these routines become streamlined and standardized, leaving no room for outdated software or misconfigured components.

This feature is now available for all Managed Kubernetes clusters using NVIDIA GPU-enabled nodes.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

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

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
