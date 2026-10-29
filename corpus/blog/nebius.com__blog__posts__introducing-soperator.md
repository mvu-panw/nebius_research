# Introducing Soperator: a Kubernetes Operator for Slurm

Source: https://nebius.com/blog/posts/introducing-soperator

Skip to main content

Today, we’re happy to announce Soperator, our Slurm-based workload manager running inside Kubernetes cluster.

The modern model training is a complicated and challenging process. Working with ambitious goals and building large ML models on multi-node GPU environment requires effective workload orchestration and convenient cluster management tooling.

To make this process easier and more manageable, we designed a unique solution combining the best of both worlds — advanced job scheduling capabilities and hardware control of Slurm and flexibility and scalability of Kubernetes.

Compared to typical Slurm installations, Soperator provides you with simplified scaling and cluster management experience. Additionally, it is packed with all the necessary drivers and components, making it GPU-ready out of the box. And we made it open source, available for every ML and HPC enthusiast for free.

## Slurm and Kubernetes joined forcesSlurm and Kubernetes joined forces

Originally designed in 2002, Slurm has proved to be a robust job orchestrator that can handle massive compute clusters in the HPC field. Today, its ability to manage multiple workloads in parallel becomes very useful for large-scale ML training.

However, this benefit goes hand in hand with some inherent limitations like old-fashioned user experience or necessity to maintain all cluster nodes in identical state. That’s why we decided to merge Slurm with Kubernetes, extracting as much value as possible from this collaboration.

Figure 1. How our Kubernetes operator for Slurm works

Kubernetes is a modern container orchestrator designed to be a versatile solution for cloud-native environments. It is flexible, scalable and useful for running different workloads within a single system. These characteristics make it very handy for being a perfect addition to Slurm functionality.

Below, we reveal the key advantages this product offers to model ML and HPC teams.

### Profound scheduling and orchestrationProfound scheduling and orchestration

The most distinctive feature of Slurm is the ability to plan and allocate plenty of jobs across thousands of computational nodes. Being able to precisely utilize expensive compute resources reduces total expenses and increases the overall efficiency of your training system. It becomes beneficial when you need to train a large ML model on a highly distributed GPU cluster.

The ability to schedule jobs in sequences and run them in parallel helps ML teams to effectively allocate cluster resources between several engineers working on different projects.

### Fault-tolerant trainingFault-tolerant training

Model training is a very compute-intensive process, generating significant pressure on the hardware layer. In such conditions, GPU cards tend to increase their failure rate, which, in turn, creates substantial disturbances for the entire workflow. For highly distributed installations, this challenge multiplies.

Our approach to running Slurm in Kubernetes solves this issue by introducing a hardware health check mechanism that monitors GPU status and reallocates workloads if any problems arise. Combined with internal Kubernetes high availability features, this brings a seamless training experience and can significantly reduce the total amount of required GPU hours.

### Simplified managementSimplified management

Mature Slurm users know how bulky this software is. Having to maintain an identical state of every node of your cluster becomes a severe limitation for managing multi-node installations for distributed ML training. To address this issue, we’ve implemented a shared root file system providing a unified file environment across all cluster nodes. This upgrade allows you to scale cluster resources up and down with ease and simplifies overall system maintenance.

Moreover, we’ve applied a Terraform operator for managing this solution to make the overall user experience friendlier.

These changes make Soperator more accessible to ML teams, lowering the requirements of in-house DevOps expertise.

If you want to learn more about Soperator’s features and their implementation, feel free to check our in-depth article.

## Made open sourceMade open source

At Nebius, we believe that only together we can create better technologies. That’s why we made this product open-source, providing ML and HPC communities with the opportunity to use this technology for their endeavors and improve it according to their specific needs.

We published Soperator on GitHub in the following repositories:

- 

github.com/nebius/soperator — the main repository with the source code and Helm charts for deploying it.

- 

github.com/nebius/soperator-terraform — this repository contains Terraform recipe that helps you deploy Soperator in our cloud with ease.

- 

github.com/nebius/slurm-deb-packages — this repository is used for building some open-source code (such as Slurm or NCCL) and publishing packages in GitHub releases. You can use it even if you are not interested in this solution.

## What’s nextWhat’s next

Today, we’re releasing the very first public version of our solution. It’s ready to work in production and we would be happy to see it in action. But we are not going to stop here and continue to develop this technology according to the community and market requirements.

Here are some important points from the existing product roadmap: improving security and isolation capabilities, improving scalability and stability of the cluster, implementing support for the upcoming software and hardware updates, etc.

## Getting StartedGetting Started

If you are interested in using Soperator for your ML environment, fill in the contact form or deploy Managed Soperator right away via self-service.

For those who want to quickly test this solution in Nebius, we’re happy to offer an application image that could be deployed over 8 GPUs in a couple of clicks.

## Explore Nebius

Sign up​
Documentation​

## Related resources

Product page​
Explaining Soperator​
Slurm vs. Kubernetes​
Main GitHub repo for Soperator​

Andrey Kuyukov
Product Marketing Manager at Nebius

## See also

### 

Explaining Soperator, Nebius’ open-source Kubernetes operator for Slurm

We’ve built an open-source Kubernetes operator that runs and manages Slurm clusters as Kubernetes resources. From this article, you’ll find out how the community tackled this task previously and the details of the architecture of our solution, which we named Soperator.

September 24, 2024
10 mins to read

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
