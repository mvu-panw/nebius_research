# Fault-tolerant training: How we build reliable clusters for distributed AI workloads

Source: https://nebius.com/blog/posts/how-we-build-reliable-clusters

Skip to main content

When starting a job, you expect it to run without interruptions. This expectation holds true across many domains, but it resonates especially deeply with machine learning engineers who launch large-scale pre-training jobs. Maintaining a stable training environment is crucial for delivering AI results on schedule and within budget constraints.

At Nebius, we’ve made significant progress over the past several months in improving cluster reliability, ensuring fault-tolerant training for all our customers. These improvements led to 169,800 GPU hours or 56.6 hours of stable operation for a 3,000-GPU production cluster, as recorded by one of our customers.

At the same time, feedback from another customer, Mirage (formerly Captions), a leading AI video company, underscores the stability of Nebius clusters and shows how crucial they are for driving progress in AI development.

“With Nebius, our long-running training jobs have been more predictable and efficient. The increased automation in fault handling and the low incident rate let us dedicate more time to iterating on new models, rather than managing infrastructure.”

Gaurav Misra, Co-Founder and CEO of Mirage

In this article, we guide you through the main concepts and metrics shaping the reliability of AI clusters, and share the techniques Nebius engineers use to ensure fault-tolerant training for our customers.

# The challenge of running training jobs on a multi-node clusterThe challenge of running training jobs on a multi-node cluster

Distributed AI training means running a model across multiple nodes, each of which processes a portion of the workload and synchronizes with the rest. This makes training faster, but also more fragile. If a single node fails, it can interrupt the entire job, resetting the training progress to the last checkpoint and wasting precious compute time. In a 1,024-GPU cluster, this means 1,023 healthy GPUs remain idle while the failed node is restored or replaced.

As the cluster size increases, the risk of failure grows proportionally. Each additional node brings more hardware and software complexity, making it easier for things to go wrong. The data from the Revisiting Reliability in Large-Scale Machine Learning Research Clusters paper illustrates this fact clearly. Their Mean Time To Failure (MTTF) metric on different cluster scales is given below:

- On 1024 GPUs, MTTF is 7.9 hours

- On 16,384 GPUs, MTTF is 1.8 hours

- On 131,072 GPUs, MTTF is 14 minutes

### Reasons for job interruptions during large-scale trainingReasons for job interruptions during large-scale training

As we can see, job interruptions are inevitable. Moreover, they are expected on large training clusters and may happen due to:

- Planned events (cluster maintenance or user-initiated restarts)

- Unplanned infrastructure failures (hardware, networking, storage)

- User-side issues (training code bugs, misconfigurations)

Meta’s research paper found that for a 54-day training job on a 16,000 GPU cluster, about 78% of unexpected job interruptions were attributed to hardware issues, while software bugs take just about 12.9% of interruptions.

The most common hardware failures stem from backend network issues, filesystem problems and GPU malfunctions, highlighting that infrastructure-level failures are the primary cause of training job interruptions. These components are also the ones over which users have the least visibility and control.

 | Failure symptoms
 | Failure domain
 | 
 | 
 | Likely failure cause

 | 
 | User program
 | System software
 | Hardware infra
 | 

 | OOM
 | ✓
 | x
 | x
 | User bug

 | GPU unavailable
 | x
 | ✓
 | ✓
 | PCIe error, driver/BIOS, thermals

 | GPU memory errors
 | x
 | x
 | ✓
 | Thermal noise, cosmic rays, HBM defect or wear

 | GPU driver/firmware error
 | x
 | ✓
 | x
 | Outdated software, high load

 | GPU NVLink error
 | x
 | x
 | ✓
 | Electro/material failure, switch

 | Infiniband link
 | x
 | x
 | ✓
 | Electro/material failure, switch

 | Filesystem mounts
 | x
 | ✓
 | x
 | Failed frontend network, drivers in D state, storage backend

 | Main memory errors
 | x
 | x
 | ✓
 | Circuit wear, thermal noise, cosmic rays

 | Ethlink errors
 | x
 | x
 | ✓
 | Electro/material failure, switch

 | PCIe errors
 | x
 | x
 | ✓
 | GPU failure, poor electrical contacts

 | NCCL timeout
 | ✓
 | ✓
 | ✓
 | Userspace crash, deadlock, Failed hardware

 | System services
 | ✓
 | ✓
 | ✓
 | Userspace interference, software bugs, network partition

Table 1. Taxonomy of failures. Source: Revisiting Reliability in Large-Scale Machine Learning Research Clusters

At the same time, many unexpected infrastructure-level failures may remain unclear to cluster operators and cannot be attributed with certainty to the cause of the failure, which prevents effective troubleshooting. Hence, granular observability and proactive health monitoring become critical.

# Importance of tracking your actual GPU utilizationImportance of tracking your actual GPU utilization

For large-scale ML training, running GPUs doesn’t necessarily mean that they are contributing to the actual progress of model development. The cluster may appear busy while jobs are restarting, stuck in queues or recovering from failures. Job interruptions stretch the total training time by adding extra time of unnecessary GPU consumption, when these compute units stay idle for the actual model training.

To see how effectively we use the reserved GPU time, we can track goodput — the ratio of compute time spent on making actual progress in a machine learning job to the total training time.

There are various definitions of goodput and several relatively close terms, describing cluster compute utilization like Effective Training Time Ratio (ETTR) or Model FLOPs Utilization (MFU), which we leave out of this article.

Figure 1. The structure of cluster idle compute time during the ML training process. Click to expand

If we leave out of the equation the planned cluster setup and maintenance time, the main factor impacting the goodput metric will be the reliability-related idle compute time, caused by job interruptions and checkpointing.

According to Figure 1, we can calculate the percentage of goodput by the following formula:

Goodput = Useful compute time / (Useful compute time + Idle compute time) where the Idle compute time consists of:

- Checkpointing time: The process also takes time and causes a short progress interruption. Potential loss of up to one minute with an AI-optimized storage.

- Lost training time from the last checkpoint: Every failure discards progress made since the last checkpoint. Potential loss of up to several hours (depending on checkpoint frequency).

- Recovery time after failures: The system needs time to detect the failure and trigger the restoration process that includes node replacement, job restart and model initialization. Potential loss from dozens of minutes to hours (depending on the level of automation).

This approach clearly demonstrates how reliability measures can impact the effectiveness of investments in AI infrastructure and the profitability of AI products. Reducing the time your GPU cluster stays down leads to faster model development, shorter time-to-market and frees up cluster capacity for additional experiments.

# How we measure the reliability of AI clustersHow we measure the reliability of AI clusters

While the goodput metric quantifies the business impact of poor cluster reliability, other key metrics provide engineers with actionable insights for enhancing AI infrastructure reliability: Mean Time Between Failure (MTBF), Mean Time To Failure (MTTF) and Mean Time To Recovery (MTTR).

Figure 2. Key metrics to measure AI cluster reliability. Click to expand

At Nebius, we focus on MTBF and MTTR to track the progress of our continuous effort to improve cluster stability.

### MTBF: How often failures happenMTBF: How often failures happen

MTBF measures how long the cluster runs before a failure occurs. We express it in GPU hours — the total uptime across all cluster GPUs, divided by the number of infrastructure-related failures (e.g., GPU crashes, PCIe errors, network faults).

MTBF = Number of GPUs * Operational time / Number of infra failures

For example, a 1,024-GPU cluster running for 336 hours with 13 infra failures yields an MTBF of 26,446 GPU hours. To convert this metric to regular hours, you just need to divide the value by the number of GPUs in the cluster, coming to ~25.8 hours.

We use MTBF to track the inherent stability of our infrastructure. A rising MTBF indicates better component reliability, improved firmware or driver behavior, or successful prevention strategies (e.g., smarter job scheduling or health gating). Conversely, declining MTBF highlights regressions in customer experience and cluster reliability.

The higher the MTBF, the fewer job restarts, the less wasted compute and the smoother your AI training lifecycle.

### MTTR: How quickly the system recoversMTTR: How quickly the system recovers

MTTR measures the average time it takes to detect, isolate and resolve infrastructure failures, bringing the affected node or cluster segment back to a healthy, schedulable state.

MTTR = Total resolution time / Number of infra failures

Total resolution time includes all steps to replace a broken node and provision a ready-to-use healthy node: node isolation, spare node provisioning and state reattachment (e.g., drivers, environment, cluster fabric).

# How we make AI clusters reliable at NebiusHow we make AI clusters reliable at Nebius

AI cluster reliability is a multi-layered discipline that requires tight alignment between engineering efforts across the entire infrastructure stack. At Nebius, we build a vertically-integrated AI cloud, making sure that every piece of this stack is well-tuned and aligned to ensure system reliability. We can define five core components with automation at every step, which constitute our approach to deliver a predictable and stable environment for large-scale distributed training.

- Multi-stage acceptance tests

- Passive and active health checks

- Workload isolation and migration

- Node replacement and state recovery

- End-to-end observability and proactive notifications

Let’s take a closer look at each of these reliability techniques.

### Multi-stage acceptance testsMulti-stage acceptance tests

We have a unique opportunity to enhance the cluster reliability from the very first stage — by designing server components, developing proprietary firmware and performing meticulous control on the contract manufacturing site.

#### On-site factory testsOn-site factory tests

First, tests start at the factory, right after the server is assembled. We test the performance of each server node, making sure that it leaves the factory only if all its components, from thermal cooling and power supply to GPU and NVMe performance, run as expected.
Examples of checks (click to expand)

- Thermal stability: gpu_burn stress test

- Power stress: GPU impulse load to verify PSU peak handling

- NVIDIA diagnostics: DCGM -4 (8–12 hours with EUD plugin) and etc

- Performance benchmarks: SuperBench kernels, NCCL, HPL (LINPACK) and Nebius’ own JAX-based LLM training test

- Background monitoring: dmesg, Ethernet/IB link flap detection, system error logs

#### Node deployment testsNode deployment tests

Once the hardware is deployed on the data center site, we run the next round of tests before the node’s first boot or after it has been redeployed following remediation. This test stage ensures stable operation of the node before adding it to the cluster network.
Examples of checks (click to expand)

- DCGM diagnostics: Run dcgmi diag -4 with an EUD plugin in a 30-min loop to validate GPU, PCIe, power and thermal stability

- Background monitoring: Track dmesg, Ethernet/IB counters and link stability during all tests

- Gpu_burn + NCCL p2pBandwidth: Stress GPUs and validate interconnect bandwidth

- SuperBench: Execute suite of compute, memory and communication benchmarks (GEMM, gpu-copy, mem-bw, nccl-bw, ORT/TensorRT inference, etc.)

- Nebius LLM test: Run JAX-based MoE training to validate end-to-end workload readiness

- Partner diagnostics (NVIDIA Field Diagnostics): NVIDIA proprietary extended GPU diagnostics

#### Virtual platform testsVirtual platform tests

We run diagnostic tests on the virtualization layer for VM images, nodes and cluster fabric, making sure that the cloud environment works reliably under intensive workloads.
Examples of checks (click to expand)

Passive checks

- Instance/shape sanity: Verify VM state, platform type (H100/H200/L40S/B200), GPU count, InfiniBand setting, SSH IP

- Virt/PCIe config: Check MaxReadReq, pvpanic device, PCIe settings

- NVIDIA GPU status: Confirm GPU count, ECC mode, VBIOS version

- Fabric status: Validate NVLink/PCIe topology, DCGM discovery

- InfiniBand sanity: Ensure correct CX7 device count, active ports, consistent firmware, pkeys

- Observability wiring: Validate IAM token, metrics density, collect agent logs

Active checks

- DCGMI diagnostics (level 2): 11-min GPU, PCIe, NVLink stress test

- CUDA samples: deviceQuery, vectorAdd, multiGPU, P2P, bandwidth tests

- SuperBench copy throughput: Validate GPU↔CPU bandwidth vs thresholds

- OSU MPI: osu_hello / osu_init sanity check

- NCCL all-reduce: Intra-host GPU collective bandwidth validation

- NCCL ring over InfiniBand: InfiniBand transport check with ring algorithm

#### Pre-provisioning cluster testsPre-provisioning cluster tests

Finally, we launch multiple production-like checks and benchmarks (such as NVIDIA DGX tests) to ensure the cluster meets all performance targets and is fully stable for distributed AI workloads.
Examples of checks (click to expand)

- NCCL collectives: Validate InfiniBand network health, detect broken or degraded links

- MLPerf Training: Benchmark distributed training workloads for GPU and interconnect performance

- NVIDIA DGX Benchmarks: Cross-check cluster performance against industry-standard workloads

- GPU Fryer: Stress GPUs to detect abnormal thermal throttling or degradation

- HPL (LINPACK): Load GPUs heavily; sensitive to packet loss and interconnect instability

- InfiniBand Ring / All-to-All (no NVLink): Verify InfiniBand link stability under collective communication

- ClusterKit: Run NVIDIA IB bring-up suite to check bandwidth and latency

- InfiniBand topology checks: Validate core–spine–leaf connections and rail assignments via UFM API; with no discrepancies

- HPL on host groups: Run on 8, 16, 32-node subsets; require <1% performance variance

- NCCL on host groups: Same as above, testing collectives across POD/Core nodes

- DCGM long diagnostics: Run extended 8–12h GPU stress tests with an EUD plugin across PODs; all must pass

- Gpu_burn: Thermal stability check at rack level; no overheating tolerated

- GPU impulse test: Apply simultaneous impulse load to node/rack; PSU must sustain peak wattage

Only after all these tests pass do we release the hardware into a customer-available capacity. This upfront investment helps us prevent failures before they happen, improving MTBF and delivering consistent performance from day one.

### Passive and active health checksPassive and active health checks

When the cluster starts to operate, the first step in terms of reliability is to identify the issue as soon as possible. For this purpose, we have comprehensive health checks. They help us indicate which nodes within the cluster are not healthy enough for job scheduling and queuing.

Why is it important?

- 

Problem identification: With comprehensive health checks, it usually takes only seconds to identify issues and mitigate job failures. In comparison, without health checks, issues can only be identified when jobs fail under workload.

- 

Root cause identification: With proper health check setup, the reasons behind issues are shown instantly, which helps identify root causes and address problems. Without health checks, identifying the reason behind node failures can be challenging and could require hours of investigation.

We developed a suite of passive and active health checks that operate continuously in the background and monitor all critical components of the system: GPU units, system software, network interconnects and more.

#### Passive health checksPassive health checks

Passive health checks continuously collect, aggregate and analyze data in the background. They are designed to detect early signs of degradation or failure without interfering with workloads. Below are some examples of parameters we monitor with passive health checks.
Examples of checks (click to expand)

GPU hardware and driver

- Driver and library version consistency (CUDA, NCCL, etc.)

- ECC (Error-Correcting Code) error detection

- Temperature monitoring and throttling alerts

- Power state monitoring and utilization tracking

- XID/SXID error reporting (GPU exception codes)

- PCIe bus health and power status

InfiniBand network

- Link status validation (up/down detection)

- Hardware error counters (e.g., retries, CRC, dropped packets)

System and topology

- Disk usage and available capacity

- NVLink topology: presence, number of active links, bandwidth health

- NCCL collectives health tracking (e.g., timeouts, hangs)

#### Active health checksActive health checks

Active health checks are executed during specific cluster lifecycle events or during idle periods. They proactively detect faults before jobs are scheduled, helping prevent training interruptions and improve overall reliability.

This functionality is enabled by default on Soperator-based clusters and is available in preview mode for Managed Kubernetes environments upon request.
Examples of checks (click to expand)

- 

DCGM diag 2, 3: Run NVIDIA GPU diagnostics (quick in r2, extended stress test in r3) to check power, memory, PCIe and thermal health, detecting both common and hidden hardware faults.

- 

Single-node All-Reduce performance (NCCL test with NVLink): Runs NCCL All-Reduce on each node to validate high-performance GPU-to-GPU communication using NVLink.

- 

Single-node All-Reduce performance (NCCL test with Infiniband): Executes the same All-Reduce test forced to use Infiniband instead of NVLink.

- 

Multi-node All-Reduce performance (NCCL test with both NVLink and Infiniband): Executes a distributed All-Reduce test that checks NVLink communication among GPUs within one node, and Infiniband communication within different nodes.

- 

ib_write_bw / ib_write_lat (GPU Target): Measures InfiniBand bandwidth and latency between GPUs via RDMA to ensure optimal inter-node GPU network performance.

- 

ib_write_bw / ib_write_lat (CPU Target): Tests InfiniBand speed from CPU memory to detect PCIe or NIC-related network bottlenecks or instabilities.

- 

GPU-fryer: Stresses GPU compute and memory to detect thermal instability, throttling or silicon degradation under full load.

- 

Memory Bandwidth Check (membw): Benchmarks memory throughput (GPU HBM or CPU DRAM) to verify healthy memory subsystem and catch bandwidth-limiting faults.

- 

ML model training: Runs a small-scale distributed training job to verify that GPUs, networking, containers and scheduling work end-to-end like in production.

### Workload isolation and job fail preventionWorkload isolation and job fail prevention

Once an issue is identified, the next step is to isolate the defective node from scheduling availability and prevent cascade job failures. Additionally, we need to mitigate the effect on the customer’s ongoing workload, to prevent job failures. Below is the description of our approach.

#### Critical faultsCritical faults

- 

The system automatically drains unhealthy nodes, removing them from the scheduling pool while allowing in-progress jobs to finish when possible. This approach excludes cascade job failures, and node draining happens in seconds without any manual intervention, as it does with non-automated flow.

- 

The system sends an ’emergency checkpointing’ signal to the customer’s training framework, prompting it to save job progress before termination. It could save hours of training progress. This feature is coming soon.

- 

For network connectivity issues, the system re-routes the communication (e.g., AllReduce) of the affected node via healthy links. It can cause some temporal performance degradation, but prevents job failures and loss of training progress. This feature is coming soon.

#### Non-critical faultsNon-critical faults

The system labels the affected node for proactive remediation without affecting running workloads.

“We are experimenting with TorchFT, a new PyTorch library enabling per-step fault tolerance in distributed training. Unlike traditional setups, TorchFT allows the training to continue even if individual nodes or GPUs fail, avoiding a full job restart. While still evolving, TorchFT shows strong potential for large-scale LLM training and workloads requiring high fault resilience.

If you are interested in adopting TorchFT, we are happy to support integration and share some insights.”

### Node replacement and state recoveryNode replacement and state recovery

When a faulty node is drained and becomes idle, our orchestration mechanisms automatically replace it with a healthy spare. We keep a dedicated spare buffer of GPU capacity for each customer to ensure quick provisioning of a new node and eliminate the risk of node downtime due to capacity shortages. The new node automatically appears in the cluster with all pre-installed drivers and dependencies, getting ready to work immediately after provisioning.

With the full automation approach in Nebius, this task takes minutes instead of hours with manual intervention.

### End-to-end observability and proactive notificationsEnd-to-end observability and proactive notifications

An important part of reliability is observability. Transparency in infrastructure is key to a great customer experience.

We have different layers of observability: system metrics, health control, etc. Let’s take a look at the health control stack for Soperator, our managed Slurm-based orchestrator.

- 

Jobs monitoring: We provide aggregated information about jobs on the cluster, enabling you to select a job for detailed investigation.

- 

Worker monitoring: You can also see aggregated information and individual details for worker nodes. All failures in infrastructure on the cluster with reasons (e.g., GPU XID, IB issues, etc) are recorded here. You can identify the causes of job failure and also check if any cluster issues are resolved or ongoing

- 

Overall cluster health: It contains all information related to GPU, CPU and storage health status.

Additionally, we proactively notify customers regarding cluster issues, planned maintenance and job failures, to prevent silent fails and wasted time. We have a dedicated Slack channel integration with our customers for fast, effective and convenient communication. Customers can customize notifications for events like:

- 

Real-time interruption alerts: Immediate notifications when training jobs fail or stall​. Detected critical health issues that may impact their workloads.

- 

Degradation detection: Detect and notify on hidden issues around performance degradation. This feature is coming soon.

Without proper observability, job failure analysis consumes hours of valuable ML engineer time. With integrated dashboards and real-time notifications, we reduce troubleshooting time from hours to minutes, providing immediate visibility into the root causes of failures.

# Battle-tested reliability for production AI clustersBattle-tested reliability for production AI clusters

Thanks to our unique fault management strategies, we can provide our customers with reliable AI infrastructure for large-scale distributed workloads, and reduce time and cost wastage in training interruptions.

Synthetic benchmarks cannot fully capture the behavior of large-scale AI clusters under real-world workloads. To provide a more realistic picture, we also measure the reliability of customer production environments running intensive distributed training.

In the beginning of the article, we mentioned an anonymous customer who ran multiple LLM training jobs on a 3,000-GPU (375-node) cluster. This system achieved a peak MTBF of 56.6 hours (169,800 GPU hours), with an average of 33.0 hours over the past several weeks. Although each training environment is unique and conclusions about one cluster cannot be applied directly to another, we can see how cluster reliability translates into fewer interruptions and less effort required from ML teams during large-scale training.

When it comes to the cluster’s ability to restore its state, we achieve an average MTTR of 12 minutes across most of our installations. This impressive result is possible through end-to-end automation of the recovery process: from early-stage fault diagnosis to spinning up replacement nodes without human intervention.

“With training jobs spread across hundreds of GPUs, even small interruptions can throw off delivery schedules. The stability we get from Nebius clusters lets us plan large experiments without constantly adjusting for potential failures.”

Drew Jaegle, Head of AI at Mirage

# Getting startedGetting started

We believe the reliability metrics we’ve shared above speak for themselves, but building resilient AI infrastructure goes far beyond numbers. It is a continuous effort. That’s why we develop and continuously improve a full stack of mechanisms to detect failures early, recover quickly and keep clusters running with minimal disruption — even under the demanding conditions of large-scale, long-running training.

Our focus is to increase goodput and help you get the best return on your AI infrastructure investment. High availability at scale reduces unplanned interruptions, shortens recovery cycles and keeps teams focused on advancing their work rather than managing incidents.

If you’re looking for a robust cloud purpose-built for large-scale AI training — or just want to learn more about our platform — feel free to reach out.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Roman Luchkov
Product Lead at Nebius

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- 

The challenge of running training jobs on a multi-node cluster

- Reasons for job interruptions during large-scale training

- 

Importance of tracking your actual GPU utilization

- 

How we measure the reliability of AI clusters

- MTBF: How often failures happen

- MTTR: How quickly the system recovers

- 

How we make AI clusters reliable at Nebius

- 

Multi-stage acceptance tests

- 

Passive and active health checks

- 

Workload isolation and job fail prevention

- 

Node replacement and state recovery

- 

End-to-end observability and proactive notifications

- 

Battle-tested reliability for production AI clusters

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

Reasoning critics enable better parallel search for software engineering agents

In this short research blog post, we discuss how reinforcement learning-finetuned reasoning language models can be used as a better alternative to regression-based critics when performing parallel trajectory search in test time, and how to train such models to prioritize precision over recall.

May 1, 2025
10 mins to read

Sign in to save this post
Sign In
