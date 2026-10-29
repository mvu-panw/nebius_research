# Open-source NVIDIA Run:ai is now available on Nebius AI Cloud Applications

Source: https://nebius.com/blog/posts/nvidia-run-ai-open-source-nebius-applications

Skip to main content

The full NVIDIA Run:ai platform, a component of NVIDIA DSX OS™ within the NVIDIA DSX AI Factory Platform, is now open source. NVIDIA Run:ai is a Kubernetes-native platform for AI workload and GPU orchestration, with capabilities including fractional GPU allocation, gang scheduling, and team-level quotas that let many teams share one cluster without stepping on each other.

As a launch partner for the release, Nebius has made open-source NVIDIA Run:ai available in Nebius AI Cloud Applications, running on Nebius Service for Managed Kubernetes. Together, Nebius provides high-performance NVIDIA accelerated infrastructure and managed Kubernetes, while NVIDIA Run:ai adds the workload and GPU orchestration needed to allocate that infrastructure dynamically across teams and workloads. This gives AI builders a streamlined way to deploy workloads, improve GPU utilization, and increase throughput.

## What’s newWhat’s new

NVIDIA Run:ai is an integrated platform whose scheduling core is KAI Scheduler, open source since April 2025 under Apache 2.0 and a CNCF Sandbox project. KAI Scheduler provides placement and allocation capabilities including gang scheduling, hierarchical queues, quota fairness, bin-packing, preemption, and fractional-GPU-aware placement.

Now the complete platform and workload orchestration layer is also open source — the UI, CLI, and API where teams submit and manage work, plus user management and dashboards — along with components that can also be adopted independently:

- 

Workload submission through a UI, CLI, and API: run training, inference, and interactive workloads without hand-writing pod specs; existing Kubeflow, Ray, and Argo pipelines connect through automatic pod grouping.

- 

Projects, departments, and quota administration: the management surface for guaranteed team shares and over-quota borrowing, on top of the queue mechanics KAI Scheduler already provides.

- 

Role-based access control and user management: the access layer a shared cluster needs before you can safely hand it to multiple teams.

- 

Monitoring and analytics: cluster and workload dashboards for allocation and utilization.

The platform is also modular. Alongside the integrated whole, NVIDIA is releasing components that can be adopted independently — KAI Resource Management (the projects, quotas, and node-pools layer), the GPU Fractioning Operator (CUDA-native fractional GPUs with hard memory isolation), and Workload Map (the contract that treats PyTorchJobs, RayClusters, and custom resources as first-class workloads). NVIDIA’s blog covers the full component map.

## The utilization mathThe utilization math

Earlier this year, Nebius and NVIDIA published joint benchmarks of fractional allocation with NVIDIA Run:ai, tested on an NVIDIA reference architecture cluster on Nebius AI Cloud. Those benchmarks used the commercial NVIDIA Run:ai v2.24 release. With the full platform now open source, the same demonstrated capabilities are available for partners and organizations to deploy, integrate, and extend directly.

At a 0.5 GPU allocation, workloads held 77% of full-GPU throughput and 86% of concurrent-user capacity (8,768 users against 10,200 at full allocation), with time to first token under one second. On Nebius AI Cloud, co-locating chat, reasoning, and embedding models on shared GPUs served roughly 3x more total users than dedicated allocation, with combined throughput above 350k tokens per second.

If half a GPU delivers 77% of the throughput, all-or-nothing allocation is leaving capacity idle on every GPU that isn’t saturated. Read the full benchmark analysis on the NVIDIA Technical Blog.

## One cluster, many teamsOne cluster, many teams

Applying those gains across a shared GPU cluster requires more than fractional allocation. It requires platform-wide policies for assigning, borrowing, reclaiming, and exposing capacity to users. NVIDIA Run:ai provides that governance layer through projects, departments, quotas, priorities, and a consistent workload-submission experience.

The situation the platform fits is a shared GPU cluster serving several teams with uneven, bursty demand. Without workload and resource orchestration, the common alternatives are static partitions (GPUs sit idle in one partition while another queues) or a free-for-all where whoever submits first wins.

With the full NVIDIA Run:ai platform, each team gets a queue with guaranteed quota that an admin sets in the control plane. When a team’s jobs don’t fill its share, other teams borrow the idle capacity and hand it back through preemption when the owner returns.

Inference teams stack several smaller models on single GPUs with fractional allocation instead of reserving a full device per endpoint, and training teams get gang scheduling, so an eight-node job never starts seven nodes and waits on the eighth.

## Available now in Nebius AI Cloud ApplicationsAvailable now in Nebius AI Cloud Applications

This release is the latest step in co-engineering that runs through the whole stack: joint fractional-GPU benchmarks on Nebius AI Cloud, MLPerf® Training results on the newest NVIDIA platforms, and NVIDIA Exemplar Cloud validation across GPU generations. The infrastructure is validated; open-source NVIDIA Run:ai puts the orchestration layer that gets the most out of it in your hands.

Deploy open-source NVIDIA Run:ai from the Nebius AI Cloud Applications now.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

David Schulman
Senior Director of Partner Marketing

Contents

- What’s new

- The utilization math

- One cluster, many teams

- Available now in Nebius AI Cloud Applications

## See also

### 

Nebius achieves NVIDIA Exemplar Cloud on NVIDIA HGX B300 for training workloads

Nebius has achieved NVIDIA Exemplar Cloud on NVIDIA HGX B300 for training workloads, adding to existing Exemplar recognition on NVIDIA H200 and GB300 NVL72. The validation reflects ongoing engineering collaboration with NVIDIA to test and optimize production infrastructure for demanding AI training workloads.

October 8, 2026
7 mins to read

### 

Nebius and WEKA benchmark distributed KV cache for agentic inference on NVIDIA HGX B300

Nebius and WEKA benchmarked a distributed NVMe KV cache tier for agentic inference on NVIDIA HGX B300 in Nebius AI Cloud. Over eight hours on identical hardware, WEKA NeuralMesh with Augmented Memory Grid served 2.4× more requests than HBM-only, held a 93% cache hit rate against 40%, and kept median time to first token near one second. This post covers the results and the infrastructure underneath.

September 24, 2026
8 mins to read

### 

Nebius Rated Platinum in SemiAnalysis ClusterMAX™ 3.0

SemiAnalysis has named Nebius a Platinum AI cloud provider, the top tier of its ClusterMAX™ 3.0 rating. The rating is based on live testing of production clusters: burn-ins, storage under concurrent load, and automated failure recovery on real NVIDIA GB300 and NVIDIA HGX B300 hardware. This post covers what the testing found and why it matters for teams choosing where to run production AI.

September 23, 2026
7 mins to read

Sign in to save this post
Sign In
