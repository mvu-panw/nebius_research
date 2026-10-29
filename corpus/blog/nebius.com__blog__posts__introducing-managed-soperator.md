# Introducing Managed Soperator: Your quick access to Slurm training

Source: https://nebius.com/blog/posts/introducing-managed-soperator

Skip to main content

We’re thrilled to announce that Managed Soperator, our fully managed Slurm-on-Kubernetes solution, is now available for everyone in self-service.

This means you can get a ready-to-work Slurm training cluster literally in minutes. The cluster will run on provisioned NVIDIA GPUs and be delivered with all necessary pre-installed libraries and drivers — allowing you to start ML training immediately.

By developing it as a managed service on our platform, we provide you with the shortest time to value, allowing you to skip negotiations with customer service and avoid frightening manual Slurm configuration.

Just set up the cluster parameters, click a button and enjoy your ready-to-work training environment.

# AI training clusters in one-clickAI training clusters in one-click

We hear a lot of feedback from our customers and colleagues that the powerful job scheduling capabilities of Slurm fall short of the expectations of many ML developers and researchers, especially among the younger generation.

This isn’t a problem if your endeavors are covered by a dedicated team of DevOps engineers; but for a small group of ML developers or independent researchers provisioning a Slurm-powered cluster, this could be a very frustrating experience.

Nebius’ Slurm/Soperator have enabled us to orchestrate distributed computing workloads with real-time streaming of petabyte-scales of data to train models. Its ease of use, fault tolerance and efficient orchestration are unique among computing infrastructure solutions.

Dhruv Pal, Tilde

In this managed implementation, we made all infrastructure provisioning and configuring processes happen in the background, hidden from the user’s view. Additionally, Managed Soperator has a full set of features that come with all managed applications on Nebius AI Cloud.

We developed Managed Soperator with a very simple idea in mind — to empower a broad audience of modern AI developers with this job-scheduling tool, to allow them to focus on inspiring AI research and creativity rather than tedious operational routines.

# Slurm becomes cloud-nativeSlurm becomes cloud-native

The core technology of our managed solution is Soperator, our in-house developed Kubernetes operator for Slurm. We released it as an open-source project last autumn. Today, it helps us quickly deploy thousand-GPU clusters for our clients, simplifying the deployment process and cutting down the provisioning time from weeks to a couple of days.

It also has proven reliability for multi-host, fault-tolerant training. Our recent results at MLPerf® Training v5.0, the most trustworthy peer-reviewed industry benchmark suite, demonstrate the value of Soperator as an orchestration tool for 512 and 1,024 GPU training.

One of the most noticeable features of Soperator is its shared root filesystem that allows us to scale the cluster size easily, without complicated package management at every new node.

Figure 1. Running Slurm on Kubernetes with Soperator

This approach helped us to wrap Slurm capabilities into a cloud-native format, significantly simplifying the operational overhead of this solution.

# Slurm-on-Kubernetes solutions by NebiusSlurm-on-Kubernetes solutions by Nebius

Today, we have three options to get a Slurm-based cluster:

- Managed Soperator as a fully managed application on Nebius AI Cloud.

- Professional Soperator as a customized and tailored solution deployed by Nebius solution architects for large-scale training installations.

- Soperator as open-source software.

The table below shows the differences and features of each of these options.

 | 
 | Managed Soperator
 | Professional Soperator
 | Soperator

 | Solution
 | Slurm-based clusters
 | Slurm-based clusters
 | Kubernetes operator for Slurm

 | Delivery model
 | Self-service app
 | Professional service
 | Open-source software

 | Cloud environment
 | Nebius
 | Nebius
 | Cloud agnostic

 | Pre-installed AI/ML-drivers and libraries
 | Yes
 | Yes
 | Yes

 | All types of containers supported
 | Yes
 | Yes
 | Yes

 | Passive health checks
 | coming soon
 | Yes
 | No

 | Active health checks
 | coming soon
 | Yes
 | No

 | Topology-aware job scheduling
 | coming soon
 | Yes
 | No

 | Auto-healing mechanism
 | coming soon
 | Yes
 | Nebius AI Cloud, only

 | Free software, consumption-based pricing
 | Yes
 | Yes
 | Yes

You may notice that many important features are marked as “coming soon” and available only in the Professional version. This reflects our vision of bringing the best of this technology to its managed implementation. Our developers are working on this right now.

# Getting startedGetting started

To start using Managed Soperator, sign up for the console, add billing details and set up your cluster parameters. The system will provision the GPU compute and deploy the Slurm environment automatically.

In its current version, you can create a cluster with up to 32 NVIDIA GPUs. However, if you need more, feel free to contact us via the contact form or Support Center, and we will be happy to provide you with a bigger cluster and turn it into a professional version if necessary.

If you want to contribute to Soperator as open-source software, make sure to check the GitHub page of this product.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Andrey Kuyukov
Product Marketing Manager at Nebius

Roman Luchkov
Product Lead at Nebius

Contents

- AI training clusters in one-click

- Slurm becomes cloud-native

- Slurm-on-Kubernetes solutions by Nebius

- Getting started

## See also

### 

Introducing Soperator: a Kubernetes Operator for Slurm

We’ve developed Soperator, a Slurm-based workload manager with a modern and simplified user experience for ML and HPC cluster orchestration.

September 24, 2024
4 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

Running Nextflow workflows with Seqera Platform and Slurm on Nebius AI Cloud

A wave of advancements, including the generation of massive amounts of data, is transforming how researchers and companies reshape science. Access to compute and workflow management systems is essential to benefit from the new wave of tools. In this blog post, we’ll explore how to leverage Seqera Platform and Slurm on Nebius AI Cloud to deploy scalable Nextflow workflows.

February 19, 2025
11 mins to read

Sign in to save this post
Sign In
