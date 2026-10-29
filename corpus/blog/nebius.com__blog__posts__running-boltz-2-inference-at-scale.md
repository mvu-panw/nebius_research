# Running Boltz-2 inference at scale in Nebius

Source: https://nebius.com/blog/posts/running-boltz-2-inference-at-scale

Skip to main content

AI foundation models are redefining drug discovery by accurately predicting how molecules interact with disease-related proteins, accelerating the identification of compounds with real therapeutic potential at unprecedented speed. With large-scale in silico experimentation, drug discovery teams can test assumptions faster and narrow down the most promising candidates for downstream optimization.

Boltz-2 stands out among biomolecular models for nearing the accuracy of more GPU-intensive simulations at the atom level while delivering predictions at an exponentially higher speed, allowing teams to move from exploration to decision-making faster. When deployed in parallelized high-performance computing pipelines, Boltz-2 simulations can reach screening throughput levels of up to hundreds of thousands of compounds per day.

Purpose-built to enable intensive drug discovery workloads, Nebius provides a vertically integrated, secure and compliant AI Cloud optimized for running inference at scale. In this article, we’ll present a reproducible framework for deploying Boltz-2 using Managed Kubernetes, GPU node groups and shared filesystems — from single-GPU experiments to production-grade, multi-node screening pipelines.

# Accelerating drug discovery with Boltz-2Accelerating drug discovery with Boltz-2

Modeling biomolecular interactions accurately while maintaining speed is one of the central challenges in biology and drug discovery. Proteins, nucleic acids and small molecules form complex, often dynamic assemblies and their structural details determine biological function and therapeutic effect. Among these properties, binding affinity — the strength of interaction between a small molecule and its protein target — is one of the main factors behind a compound’s potency and a crucial filter in hit discovery and lead optimization. An essential step in the drug discovery pipeline is hit discovery, the process of identifying molecules that effectively bind to a specific target and are worth enhancing in lead optimization, when top candidates are refined for clinical testing.

In silico prediction of binding affinity remains difficult despite its importance in drug design. Approaches like free-energy perturbation (FEP), which model molecular behavior at the atomic level, can near experimental accuracy, but their heavy compute demands and requirement for expert handling make them unsuitable for high-throughput screening. Although methods like molecular docking reduce complexity and precision for faster results, they frequently lack the ranking power required for confident decision making.

Boltz-2 is a structural-biology foundation model that combines high-quality structure prediction and affinity estimation. It uses a co-folding trunk for protein–ligand complex prediction, a dedicated affinity module (PairFormer + prediction heads) and controllability features — such as conditioning on experimental method (X-ray / NMR / MD), pocket/distance steering and multimeric templates — to improve robustness. These advances let Boltz-2 produce structure and affinity outputs that align well with experiments while running orders of magnitude faster than FEP, enabling high-throughput ranking and screening of hundreds of thousands of compounds per day on parallel high-performance computing.

Boltz-2 already works in real pipelines: retrospective and prospective tests show it helps hit-to-lead optimization, large-scale hit discovery and generative design loops that are later validated with targeted FEP. It produces experimentally relevant hypotheses at scales that were previously impractical for physics-based methods. However, model advances alone don’t solve the engineering problems of production inference. At scale, Boltz-2 depends on large, low-latency datasets — ligand libraries, the Chemical Component Dictionary (CCD), MSA caches and the like — so you need solid operational patterns: efficient data locality and caching, parallel job orchestration with GPU-aware scheduling, fault tolerance and reproducibility for long runs and cost-aware lifecycle management to avoid idle expensive resources.

# Scaling Boltz-2 inference in Nebius AI CloudScaling Boltz-2 inference in Nebius AI Cloud

This article focuses on the infrastructure and workflow patterns required to run Boltz-2 reliably in Nebius AI Cloud. Specifically, we’ll cover:

- Cluster orchestration and job scheduling.

- Managed Service for Kubernetes® to reduce operational burden.

- GPU node groups sized for Boltz-2’s memory and throughput.

- Shared filesystem for centralized model caches, ligand libraries and outputs.

We’ll also translate Boltz-2’s scientific requirements into a concrete operational blueprint you can use for both exploratory experiments and production-grade screening pipelines.

In this complementary tutorial, you can find tested, runnable commands and manifests to set up a Managed Service for a Kubernetes cluster and a shared filesystem to run Boltz-2 inference in Nebius.

# Resource requirements and scalingResource requirements and scaling

Boltz-2 has about 1 billion trainable parameters. In addition to the model weights, it requires a large cache (ligand libraries and Chemical Component Dictionary).

Running inference needs GPUs with high memory capacity. For this benchmark, we’ll use NVIDIA L40S GPUs with 48GB VRAM each: ~11 GB for structure prediction and ~7–8 GB for affinity prediction. That leaves spare capacity for batching and multiple concurrent jobs.

Assuming ~40-60 seconds per protein-ligand prediction, 16 cards running in parallel would yield on the order of 1,000 predictions per hour (≈960–1,440 depending on per-prediction runtime). This is why we run Boltz-2 on a multi-node Kubernetes cluster instead of a single VM. For small workloads (just a few molecules), a standalone VM or Jupyter session is sufficient. At scale, however, Kubernetes orchestration and shared storage become essential.

# Orchestrating workflows with Managed KubernetesOrchestrating workflows with Managed Kubernetes

Kubernetes, alongside Soperator/Slurm, is a rewarding option of how to do distributed AI in Nebius AI Cloud. It ensures that all components — compute nodes, storage volumes and jobs — are orchestrated automatically, allowing life sciences teams to experiment, iterate and scale on a structured environment.

For Boltz-2 inference, Kubernetes handles:

- Job scheduling — distributing protein–ligand tasks evenly across GPUs.

- Resilience — if a pod fails, it is automatically restarted.

- Parallelism — hundreds of inference jobs can run concurrently.

- Resource management — GPU, CPU and RAM allocations are tracked cluster-wide.

Without orchestration, researchers would need to manually launch and monitor hundreds of jobs. Kubernetes makes large-scale biomolecular inference manageable and predictable.

Our Managed Service for Kubernetes provides a control plane that takes away the operational overhead of setting up, patching and scaling clusters, so teams can focus on experimentation and decision-making.

Why it matters for Boltz-2:

- No need to manually install GPU drivers, as they come preconfigured.

- Node groups can be created with one command and scaled up or down depending on workload.

- Security and IAM are integrated with the cloud platform.

- This allows research teams to focus on drug discovery experiments rather than infrastructure plumbing.

# Data platform and workflowData platform and workflow

This section describes the data platform required to run Boltz-2 in Nebius AI Cloud, and the repeatable workflow for packaging, launching, and cleaning up inference runs. For tested, runnable commands and Kubernetes manifests, see the complementary tutorial.

### Shared filesystem for large datasetsShared filesystem for large datasets

A critical enabler is the shared filesystem, mounted across all nodes. Boltz-2 requires:

- Ligand libraries

- Chemical Component Dictionary

- Multiple sequence alignments (MSAs)

- Input YAML batch files

With a shared filesystem:

- All nodes can read from the same dataset without duplicating it locally.

- Prediction results are written back to a common location.

- Workflows remain synchronized, even across dozens of nodes.

In Nebius AI Cloud, this is implemented with a network SSD filesystem, attached through the CSI driver and exposed to Kubernetes as a PersistentVolumeClaim (PVC).

### Workflow overviewWorkflow overview

Running Boltz-2 in Nebius follows a simple, repeatable workflow:

- 

Set up the environment: install CLI tools to manage cloud resources.

- 

Package the model runner: build a container image with Boltz-2 code and dependencies, push it to Nebius Container Registry.

- 

Create a Kubernetes cluster with GPU nodes: launch a Managed Kubernetes cluster with a GPU node group. Attach a shared filesystem.

- 

Upload input data: place YAML job batches and MSAs into the shared PVC.

- 

Pre-load model cache: pre-download ligand libraries and CCD data into the shared filesystem.

- 

Run inference jobs: launch multiple parallel jobs via Kubernetes, each processing a batch of inputs.

- 

Collect results: gather predictions (structures and affinities) from the shared filesystem.

- 

Clean up resources: delete GPU node groups, PVCs and registries to stop billing.

# Getting startedGetting started

With this robust operational blueprint, drug discovery teams can confidently deploy Boltz-2 inference at scale in Nebius AI Cloud’s secure and compliant environment. By relying on Managed Kubernetes to orchestrate GPU node groups and a shared filesystem to centralize model caches and ligand libraries, researchers can set up high-throughput, experimentally relevant in silico drug screening pipelines.

This reproducible framework provides a reliable, scalable and cost-aware foundation to simulate molecular interactions with near-atomic precision exponentially faster. Talk to an expert today and start building your workflows — from exploratory experiments to production-grade screening pipelines.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- 

Accelerating drug discovery with Boltz-2

- 

Scaling Boltz-2 inference in Nebius AI Cloud

- 

Resource requirements and scaling

- 

Orchestrating workflows with Managed Kubernetes

- 

Data platform and workflow

- Shared filesystem for large datasets

- Workflow overview

- 

Getting started

## See also

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

From genome analysis to quantum chemistry: Nebius powers the next generation of biotech research with NVIDIA

As part of NVIDIA GTC Paris at VivaTech, Nebius has announced deeper integration of the NVIDIA AI Enterprise software suite. This includes NVIDIA BioNeMo, a collection of tools, applications, generative AI solutions, and pre-trained microservices (NVIDIA NIM) designed squarely for the biopharma sector.

June 25, 2025
5 mins to read

### 

Behind SWE-rebench: Infrastructure to collect massive datasets of SWE tasks and evaluate agents at scale

Research on SWE agents involves building and running thousands of containers, quickly surpassing the limits of a single host. Our AI R&D team unveils the large-scale infrastructure that powers this research — the backbone behind recent releases such as SWE-rebench — and an open-source part of it to support the broader community.

November 7, 2025
14 mins to read

Sign in to save this post
Sign In
