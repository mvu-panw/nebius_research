# Introducing Managed SkyPilot API Server on Nebius AI Cloud

Source: https://nebius.com/blog/posts/managed-skypilot-api-server-tech-overview-and-setup

Skip to main content

Since our initial SkyPilot integration in April 2025, developers have been able to deploy AI workloads seamlessly on Nebius infrastructure through SkyPilot’s unified interface. This integration has enabled teams to provision GPU instances with simple YAML configs by specifying resources like accelerators: H100:8, and letting SkyPilot handle the infrastructure provisioning. Teams could also mount cloud storage directly and automatically mount Nebius object storage buckets to compute instances by using file_mounts, while leveraging high-performance interconnect for distributed training workloads.

However, this initial integration relied on SkyPilot’s local API server model — where each developer ran SkyPilot commands from their individual machines. While this approach worked well for individual users, it created several limitations for teams.

The other option is for teams to self-host SkyPilot’s remote API server. However, self-hosting can have significant operational overheads, especially as teams scaled their AI workloads and needed more sophisticated infrastructure management.

# The solution: Managed SkyPilot API ServerThe solution: Managed SkyPilot API Server

Today, we’re excited to announce the launch of Managed SkyPilot API Server on Nebius AI Cloud — a fully managed solution that automates the deployment and ops of the SkyPilot API server into a one-click experience, eliminating operational overhead entirely.

Click to expand

# Benefits of centralized AI InfrastructureBenefits of centralized AI Infrastructure

The centralized API server approach changes how both individuals and teams work with AI infrastructure, delivering immediate value across multiple areas.

### ProductivityProductivity

The server enables asynchronous execution, letting you launch multiple jobs without blocking your terminal to submit hyperparameter sweeps or experiment batches in parallel. With multi-device access, you can start a training job from your office and monitor it from home simply by connecting to the same API server. Production workflow integration becomes seamless with orchestrators like Apache Airflow, while SkyPilot manages your diverse infrastructure.

### Collaboration and efficiencyCollaboration and efficiency

Centralized deployment means you set up once, and then team members onboard by using a single endpoint, without distributing credentials or managing individual installations. Teams benefit from resource sharing where they can share GPU clusters, monitor each other’s jobs and coordinate resource usage across the organization. When one team member spins up an expensive multi-GPU cluster, others can submit jobs to it. This enables true collaboration where teams share configurations, coordinate experiments and maintain institutional knowledge.

### Operational excellenceOperational excellence

The platform provides unified visibility through a single view for all running clusters, jobs and services across your entire infrastructure. Job observability allows you to monitor training progress, view logs and track resource utilization across all team workloads. This centralized visibility helps identify idle resources and optimize cloud spending. The cloud-native deployment ensures fault tolerance, making sure your workloads survive infrastructure changes.

## Why choose managed over self-hosted?Why choose managed over self-hosted?

Managing a production-grade deployment involves significant operational complexity that can distract teams from their core AI research and development.

### Self-hosting challengesSelf-hosting challenges

- Kubernetes expertise required: Setting up persistent storage, configuring ingress controllers, managing SSL certificates.

- Ongoing maintenance: Monitoring server health, handling upgrades, managing authentication.

- Database management overhead: Maintaining a separate PostgreSQL database for job state, handling backups, ensuring high availability and managing schema migrations.

- Infrastructure overhead: Provisioning and maintaining the underlying Kubernetes cluster.

### Advantages of the solution managed by NebiusAdvantages of the solution managed by Nebius

- One-click deployment: Provision your SkyPilot API server directly from our console.

- Zero operational overhead: We handle all infrastructure management, monitoring and maintenance.

- High availability: Fault-tolerant deployment with automatic failover and recovery, with state backed by Nebius' Managed Service for PostgreSQL.

This managed approach is designed specifically for small to mid-size ML teams who want to focus on AI innovation rather than infrastructure operations. While larger enterprises often have dedicated DevOps teams and require extensive customization, most ML teams simply want a reliable, shared platform that works out of the box.

# Deploying your serverDeploying your server

Ready to eliminate infrastructure complexity and unlock centralized AI workload management? Managed SkyPilot API Server is available through the Nebius console. You can deploy your API server in minutes through the web UI, share a single endpoint URL for instant team access and start launching jobs and sharing resources right away.

### Current capabilities and roadmapCurrent capabilities and roadmap

The current release supports two compute infrastructure options:

- Nebius Platform API: Direct access to high-performance interconnected GPU clusters

- Nebius Managed Kubernetes Service: Your existing Kubernetes clusters are automatically discovered and available for workloads

Coming soon: Support for additional cloud providers (AWS, GCP, Azure) will be added, preserving SkyPilot’s core value proposition of multi-cloud flexibility and failover capabilities, as well as Nebius' design principle of ecosystem interoperability to avoid lock-in. SSO authentication support will also be available for seamless enterprise integration.

## Technical implementationTechnical implementation

### Connecting to your API serverConnecting to your API server

Once the SkyPilot API server is provisioned, you can connect to the server:

$ export SKY_USERNAME='<replace with your username>'
$ export SKY_PASSWORD='<replace with your password>'
sky api login -e "https://\SKY_USERNAME:\$SKY_PASSWORD@public-...nebius.cloud"

### Configuring the SkyPilot API serverConfiguring the SkyPilot API server

After provisioning, you’ll have access to the SkyPilot API server web UI:

The admin user needs to configure the SkyPilot API server by specifying the project ID and, optionally, IB fabric filesystem IDs. Access the configuration through the button in the top right corner of the web UI and update it with your Nebius settings:

Click to expand

nebius:
 region_configs:
 us-central1:
 # replace with your project_id
 project_id: project-u00w5qcypr00qq5k6de40z
 fabric: us-central1-a
 filesystems:
 # replace with your filesystem_id
 - filesystem_id: computefilesystem-u00ka4d0q8959st67e
 mount_path: /mnt/data
 attach_mode: READ_WRITE

This configuration allows you to:

- Specify which project ID to use in each region.

- Optionally, configure shared filesystems for your compute instances (highly recommended).

Nebius shared filesystems provide high-performance storage that automatically mounts to your SkyPilot instances. This enables efficient multi-node data access for training datasets and model checkpointing without data duplication across instances.

### Working with Kubernetes clustersWorking with Kubernetes clusters

Nebius Managed Kubernetes clusters are automatically discovered by the SkyPilot API server. You can verify available clusters:

$ sky check k8s
Checking credentials to enable infra for SkyPilot.
 Kubernetes: enabled [compute]
 Allowed contexts:
 └── nebius-mk8s-my-cluster-1: enabled.
 └── nebius-mk8s-my-cluster-2: enabled.
 ...

GPU workload requirements: To run GPU workloads on these Kubernetes clusters, ensure they are properly configured with: drivers/GPU operator, Device Plugin, Network operators (for interconnect support in distributed training).

### Advanced team managementAdvanced team management

Once the admin is connected to the API server dashboard, they’ll be able to create other users, control their permissions and organize them into teams and workspaces. Watch how an admin creates a new user and how that user can immediately start launching GPU clusters:

# Example: User launches a test job
$ sky launch -c my-cluster --gpus=H200:1 --infra nebius/us-central1 -- nvidia-smi
Command to run: nvidia-smi
Considered resources (1 node):
--------------------------------------------------------------------------------------------------------
INFRA INSTANCE vCPUs Mem(GB) GPUS COST ($) CHOSEN
--------------------------------------------------------------------------------------------------------
Nebius (us-central1) gpu-h200-sxm_1gpu-16vcpu-200gb 16 200 H200:1 3.50 ✔
--------------------------------------------------------------------------------------------------------
Launching a new cluster 'my-cluster'. Proceed? [Y/n]: Y
...
(sky-cmd, pid=4095) Wed Sep 3 14:16:04 2025
(sky-cmd, pid=4095) +-----------------------------------------------------------------------------------------+
(sky-cmd, pid=4095) | NVIDIA-SMI 570.172.08 Driver Version: 570.172.08 CUDA Version: 12.8 |
(sky-cmd, pid=4095) |-----------------------------------------+------------------------+----------------------+
(sky-cmd, pid=4095) | GPU Name Persistence-M | Bus-Id Disp.A | Volatile Uncorr. ECC |
(sky-cmd, pid=4095) | Fan Temp Perf Pwr:Usage/Cap | Memory-Usage | GPU-Util Compute M. |
(sky-cmd, pid=4095) | | | MIG M. |
(sky-cmd, pid=4095) |=========================================+========================+======================|
(sky-cmd, pid=4095) | 0 NVIDIA H200 On | 00000000:8D:00.0 Off | 0 |
(sky-cmd, pid=4095) | N/A 31C P0 75W / 700W | 0MiB / 143771MiB | 0% Default |
(sky-cmd, pid=4095) | | | Disabled |
(sky-cmd, pid=4095) +-----------------------------------------+------------------------+----------------------+
(sky-cmd, pid=4095)
(sky-cmd, pid=4095) +-----------------------------------------------------------------------------------------+
(sky-cmd, pid=4095) | Processes: |
(sky-cmd, pid=4095) | GPU GI CI PID Type Process name GPU Memory |
(sky-cmd, pid=4095) | ID ID Usage |
(sky-cmd, pid=4095) |=========================================================================================|
(sky-cmd, pid=4095) | No running processes found |
(sky-cmd, pid=4095) +-----------------------------------------------------------------------------------------+
✓ Job finished (status: SUCCEEDED).

# Alternatively, you can run the same job on your Managed K8s cluster:
# $ sky launch -c my-cluster --gpus=H200:1 --infra k8s/nebius-mk8s-my-cluster-1 -- nvidia-smi

The workspaces feature provides powerful multi-team management capabilities, including resource isolation to separate infrastructure configurations and track usage by team or project, flexible access control to create private workspaces with specific user permissions and multi-tenant management to manage complex cloud computing environments with minimal administrative overhead.

Click to expand

# Transform your AI infrastructure todayTransform your AI infrastructure today

Managed SkyPilot API Server represents our commitment to making enterprise-grade AI infrastructure accessible to teams of all sizes. By eliminating the operational barriers that have historically prevented teams from adopting centralized AI infrastructure management, we’re enabling ML teams to get more done in less time.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Kim
Cloud Solutions Consultant

Contents

- 

Limitations of the local server

- 

The solution: Managed SkyPilot API Server

- 

Benefits of centralized AI Infrastructure

- 

Productivity

- 

Collaboration and efficiency

- 

Operational excellence

- Why choose managed over self-hosted?

- 

Self-hosting challenges

- 

Advantages of the solution managed by Nebius

- 

Deploying your server

- 

Current capabilities and roadmap

- Technical implementation

- 

Connecting to your API server

- 

Configuring the SkyPilot API server

- 

Working with Kubernetes clusters

- 

Advanced team management

- 

Transform your AI infrastructure today

## See also

### 

Nebius AI Cloud is now integrated with SkyPilot

We’re excited to announce our integration with SkyPilot, an open-source framework that simplifies running AI and batch workloads across cloud platforms. This collaboration enables direct access to Nebius AI Cloud resources via SkyPilot.

April 2, 2025
6 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

Bulk Object Storage data migration with SkyPilot

Moving large datasets between S3 buckets is often slow, unreliable and frustrating — especially across accounts or clouds. In this post, we share a fast, fully open-source workaround using SkyPilot, s5cmd and Nebius AI Cloud.

April 24, 2025
6 mins to read

Sign in to save this post
Sign In
