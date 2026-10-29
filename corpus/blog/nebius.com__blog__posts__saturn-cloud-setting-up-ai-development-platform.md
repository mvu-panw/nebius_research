# Nebius with Saturn Cloud: Setting Up an AI Development Platform

Source: https://nebius.com/blog/posts/saturn-cloud-setting-up-ai-development-platform

Skip to main content

# Why Saturn Cloud mattersWhy Saturn Cloud matters

When working with raw Kubernetes, infrastructure engineers still have to do a lot of heavy lifting to get AI teams productive: setting up GPU node pools and scaling policies, managing Python and package environments, configuring secure data access and adding the monitoring, logging and cost controls that keep clusters reliable and efficient. These tasks can take weeks to implement before the first model can even run. Saturn Cloud manages this entire layer automatically, providing ready-to-use environments, autoscaling compute, built-in observability and team-level controls out-of-the-box. This allows infrastructure engineers to focus on higher-value initiatives, while their AI teams can be productive on day one: opening notebooks, connecting to data and training models immediately.

# How it worksHow it works

Saturn Cloud installs into a Managed Kubernetes cluster hosted in Nebius AI Cloud. Most deployments are managed by Saturn Cloud, where customers provide Saturn Cloud with access keys to their Nebius account. Saturn Cloud then provisions an MK8s cluster, installs itself and provides ongoing maintenance, support and upgrades. You can also self-manage the deployment if you prefer.

This section covers the installation procedure.

# Installation procedureInstallation procedure

If you are provisioning your own MK8s cluster, Saturn Cloud’s team recommends managing MK8s with Terraform. Here’s a sample Terraform recipe you can customize, or you can write it yourself.

The Terraform recipe creates:

- 

A system node pool (where the Saturn Cloud control plane and supporting microservices run)

- 

A few CPU node pools if you have CPU workloads

- 

A few GPU node pools

Once you have an MK8s cluster, Saturn Cloud can be installed via a Helm chart. To begin, please register your company with Saturn Cloud. The registration process will present you with a short-lived (4-hour) bootstrap API token that you will pass into the Helm chart for the saturn-helm-operator which is publicly hosted on GitHub at oci://ghcr.io/saturncloud/charts/saturn-helm-operator-nebius.

The operator will:

- 

Exchange the 4-hour bootstrap token for a long-lived API token, and keep it refreshed

- 

Set up the necessary secrets for SSL termination at *.your-company.saturnenterprise.io

- 

Install Saturn Cloud and all supporting microservices

# Kubernetes servicesKubernetes services

The supporting microservices include:

- 

Fluent-bit and Elasticsearch for log management

- 

Traefik, along with the Saturn Cloud auth-server, because Saturn Cloud gates network access to deployed resources using RBAC

- 

An SSH proxy so that customers can SSH into your containers if you choose to do so

- 

Prometheus for monitoring and metrics

The Saturn Cloud installation also relies on solutions in MK8s, including:

- The cluster-autoscaler

- Cilium for network policies and encryption

- GPU Operator for GPU management

- Network Operator for interconnect support

# Post-installationPost-installation

Once Saturn Cloud is installed, you will receive an email to reset your password and log in to the admin account. After that, you can invite your team to the installation, and optionally configure SSO for access.

# Saturn Cloud resourcesSaturn Cloud resources

The primary purpose of Saturn Cloud is to manage AI/ML resources. All Saturn Cloud resources utilize public container images that Saturn Cloud has published, which include the most commonly used AI/ML libraries. Most customers end up building their own images either using the Saturn Cloud image builder or with Docker directly.

Saturn Cloud resources also load code from your Git repositories. Because Saturn Cloud resources just run container images with code from your Git repositories, the workloads are entirely portable. They can be easily exported from Saturn Cloud if you choose to do so in the future.

There are three primary resource types:

- 

Development workspaces are K8s deployments that run either JupyterLab or RStudio. They also support SSH, allowing customers to use VS Code, Cursor, PyCharm or any other IDE that supports SSH with Saturn Cloud. Development instances are backed by a Nebius persistent disk mounted in your home directory.

- 

Jobs are K8s jobs that can also be scheduled as K8s cronjobs. Jobs can also be used in multi-node training. Saturn Cloud jobs propagate environment variables so that your training code (for example, torchrun) can coordinate the multiple nodes within the job.

- 

Deployments are K8s deployments that serve HTTP traffic. This is primarily used to deploy LLMs, ML models and dashboards.

All three can also attach Nebius shared filesystems.

All Saturn Cloud resources can be exported or created from a YAML recipe. This facilitates CI/CD patterns where you want to deploy straight to Saturn Cloud from your CI/CD system. For more information, check out the Saturn Cloud docs here.

Ask your Nebius solutions architect or account executive about using Saturn Cloud in your Nebius account. It’s free of charge for accounts approved by the Nebius team.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- Why Saturn Cloud matters

- How it works

- Installation procedure

- Kubernetes services

- Post-installation

- Saturn Cloud resources

## See also

### 

Nebius Status Board: now structured by region

We are introducing updates to the Nebius Status Board to enhance transparency during service outages and provide users with a clearer view of Nebius AI Cloud service availability.

November 5, 2025
1 min to read

### 

Nebius meets enterprise-level security standards: ISO 27001, SOC 2 Type II including HIPAA and more

Today, we are thrilled to announce we achieved major security and compliance milestones. Independent third-party audits have verified that our security controls meet the requirements of SOC 2 Type II (including HIPAA), and align with the principles of NIS2 and DORA. We also obtained ISO 27001 certification, strengthened our practices by incorporating principles from ISO 27701, 27018, 27799, 27032, and standalone ISO 22301.

October 14, 2025
8 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
