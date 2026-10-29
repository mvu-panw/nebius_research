# MLPerf® Storage v3.0 results: Leading RetinaNet training on Nebius Object Storage

Source: https://nebius.com/blog/posts/mlperf-storage-v3-0-results

Skip to main content

Nebius is proud to submit the MLPerf® Storage v3.0 results. Nebius Object Storage fed 768 simulated NVIDIA B200 accelerators running the RetinaNet training workload, the highest accelerator count of any submission in this round. [1]

All four Closed division results ran on Object Storage with the Enhanced storage class in one of our production regions. Two were training workloads — RetinaNet and Unet3D — and two were checkpointing runs at different Llama 3.1 model scales (8B and 70B). Every run read and wrote directly through the S3 API.

In this blog, we share the full results and methodology.

## What MLPerf Storage measuresWhat MLPerf Storage measures

MLPerf® Storage tests whether a storage system can keep accelerators busy. The benchmark simulates the I/O demand of GPUs running real training workloads. While it doesn’t use physical GPUs, each simulated accelerator places the same load on storage that a real one would. A run validates only if accelerator utilization stays at or above the benchmark’s minimum of 85% for RetinaNet or 90% for Unet3D. This makes accelerator count a useful measure of scale: a submission can only add accelerators if the storage system can supply data fast enough to keep them busy. Therefore, the result reflects storage performance against the I/O patterns of real AI training, rather than a synthetic throughput number.

We submitted using Nebius Object Storage with the Enhanced storage class, which is designed for Nebius AI training and checkpointing. Client nodes ran as publicly available CPU-only virtual machines (the AMD EPYC Genoa cpu-d3 preset) on Ubuntu 24.04 over Ethernet, with capped memory. The tests used the open-source mlpstorage benchmark harness.

## Results at a glanceResults at a glance

Nebius Object Storage fed 768 simulated B200 accelerators on RetinaNet, the highest count of any submission this round, and ran the highest Unet3D accelerator count among object storage submissions. Checkpoint write bandwidth scaled from 2.81 GiB/s on one client node to 19.46 GiB/s on eight. Utilization on both training runs cleared the benchmark’s minimums, at 88.4% and 92.5%.

Table 1. Training results (Closed division; higher is better)

 | Workload
 | Client nodes
 | Simulated accelerators
 | Accelerator utilization
 | Read bandwidth
 | Throughput (samples/s)

 | RetinaNet
 | 32
 | 768 × B200
 | 88.4%
 | 102.83 GiB/s [1]
 | 341,881

 | Unet3D
 | 21
 | 21 × B200
 | 92.5%
 | 114.45 GiB/s [2]
 | 838

Table 2. Checkpointing results, Llama 3.1 (Closed division; higher is better)

 | Model scale
 | Client nodes
 | DP instances
 | Write bandwidth
 | Read bandwidth

 | 8B
 | 1
 | 1
 | 2.81 GiB/s
 | 7.14 GiB/s [3]

 | 70B
 | 8
 | 8
 | 19.46 GiB/s
 | 38.27 GiB/s [4]

All results: MLPerf® Storage v3.0, Closed division, Nebius Object Storage. Training reports accelerator utilization, aggregate read bandwidth, and samples per second; checkpointing reports aggregate read and write bandwidth.

## The highest RetinaNet accelerator count of any submissionThe highest RetinaNet accelerator count of any submission

RetinaNet tests a latency-bound workload made up of many small files, where storage needs to serve large numbers of individual data requests quickly. Nebius Object Storage sustained an aggregate 341,881 samples per second while maintaining 88.4% accelerator utilization. [1]

Nebius ran RetinaNet at the highest accelerator count of all submissions, regardless of storage architecture. Among object storage submissions specifically, that throughput is more than twice the next-best result. [1]

Systems differ in node counts and per-node configuration, so per-host numbers vary by design; what the benchmark validates is utilization at aggregate scale. For teams sizing storage for training pipelines that read many small files, that’s the number that matters, because it measures how many GPUs the storage can feed.

## The highest Unet3D accelerator count among object storage submissionsThe highest Unet3D accelerator count among object storage submissions

Where RetinaNet tests small-file latency, Unet3D tests the other end of the I/O spectrum: a bandwidth-bound workload with large files. Both workloads ran on the same storage service through the same S3 API path.

Nebius posted the highest Unet3D accelerator count among object storage submissions this round. We ran 21 simulated B200 accelerators across 21 client nodes, and Object Storage sustained 114.45 GiB/s of aggregate read throughput at 92.5% accelerator utilization. [2]

## Checkpointing bandwidth scales with cluster sizeCheckpointing bandwidth scales with cluster size

The checkpointing runs covered two scales: Llama 3.1 8B on a single node with one data-parallel instance, and Llama 3.1 70B on eight nodes with eight.

As the cluster grew from one to eight client nodes, aggregate write bandwidth increased from 2.81 GiB/s to 19.46 GiB/s, while aggregate read bandwidth increased from 7.14 GiB/s to 38.27 GiB/s. [3] [4] Both runs wrote and restored checkpoints directly against Object Storage through the S3 API.

## What this means for training on Nebius Object StorageWhat this means for training on Nebius Object Storage

Of the round’s 19 Closed division submitters, only three benchmarked an S3 object storage backend. These results show one service covering the full spread of training I/O: latency-sensitive small files, sustained large-file reads, and checkpoint writes and restores, all through a single S3 path. Teams whose datasets already live in object storage can train against them directly, with nothing extra to provision or tune.

Every number above came from standard CPU-only VM presets, an open-source benchmark harness, and the same Enhanced storage class we offer every customer, in all Nebius AI Cloud regions. Any tenant can reproduce the setup.

To learn how Nebius can support your AI projects at scale, get in touch.

## References

- MLPerf® v3.0 Storage Closed RetinaNet, September 1, 2026, Retrieved from mlcommons.org/benchmarks/storage/, entry v3.0-0074. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v3.0 Storage Closed Unet3D, September 1, 2026, Retrieved from mlcommons.org/benchmarks/storage/ entry v3.0-0075. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v3.0 Storage Closed Checkpointing Llama3.1-8B, September 1, 2026, Retrieved from mlcommons.org/benchmarks/storage/, entry v3.0-0073. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v3.0 Storage Closed Checkpointing Llama3.1-70B, September 1, 2026, Retrieved from mlcommons.org/benchmarks/storage/, entry v3.0-0072. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

John Alexander
Senior Technical Product Marketing Manager at Nebius

Contents

- What MLPerf Storage measures

- Results at a glance

- The highest RetinaNet accelerator count of any submission

- The highest Unet3D accelerator count among object storage submissions

- Checkpointing bandwidth scales with cluster size

- What this means for training on Nebius Object Storage

## See also

### 

MLPerf® Training 6.0: Leading NVIDIA HGX B300 and competitive NVIDIA GB300 NVL72 results on NVIDIA Blackwell Ultra systems

MLPerf® Training 6.0 results are in. Across six configurations on NVIDIA Blackwell Ultra systems, Nebius posted the #1 single-node HGX B300 times for Llama-3.1-8B and GPT-OSS 20B pre-training and came within 3.1% of the fastest GB300 NVL72 result on all three benchmarks at 72 GPUs. This post covers the full results and methodology.

June 16, 2026
14 mins to read

### 

MLPerf® Inference v6.0: Top-tier AI performance on NVIDIA Blackwell and Blackwell Ultra

The results of our MLPerf® Inference v6.0 submission demonstrate Nebius’ ability to maximize efficiency for modern AI inference workloads on the latest NVIDIA Blackwell and Blackwell Ultra platforms.

April 1, 2026
14 mins to read

### 

MLPerf® Training v5.1: Leading results on NVIDIA Blackwell and Blackwell Ultra systems

We’re proud to share the results of our participation in the MLPerf® Training v5.1 benchmark, where Nebius showcased strong performance across several configurations of the latest NVIDIA Blackwell and Blackwell Ultra systems. This round continues our commitment to transparency and collaboration with the MLCommons® community, as we work to ensure the highest quality standards for training and fine-tuning next-generation GenAI models.

November 12, 2025
7 mins to read

Sign in to save this post
Sign In
