# Choosing storage for deep learning: a comprehensive guide

Source: https://nebius.com/blog/posts/choosing-storage-for-deep-learning

Skip to main content

## Good-Better-Best (GBB) frameworkGood-Better-Best (GBB) framework

The rapid evolution of deep learning models has brought about unprecedented growth in both their size and complexity. This trend, while pushing the boundaries of what is technologically possible, has also placed immense demands on the underlying infrastructure, particularly in terms of data management and storage.

As organizations seek to benchmark their current setups and plan future infrastructure investments, we employed the Good-Better-Best (GBB) approach to laying out our benchmarks.

- 

Good: Meets baseline requirements for effective operations. Such solutions might be sufficient for smaller, less complex models or for organizations just beginning to scale their deep learning initiatives.

- 

Better: Provides significant improvements in performance, scalability, or efficiency. These are often the sweet spot for organizations that have outgrown their initial setups and need more robust infrastructure to handle increasing demands.

- 

Best: Represents state-of-the-art solutions offering top-tier performance and scalability. These solutions are typically adopted by organizations at the forefront of deep learning, where cutting-edge performance is vital for maintaining a competitive edge.

Please keep in mind that optimal solutions are not one-size-fits-all; they constantly change based on specific use cases and evolve with technological advancements. Therefore, the specific values provided here should only be considered within the current context, as they may shift with future developments.

## Data preparation and tokenizationData preparation and tokenization

The first stage in any deep learning pipeline is data preparation, which, in the context of LLMs, you can read about here. It is a critical phase that transforms raw data into a format suitable for model training. This process involves several key tasks, including data cleaning, concatenation, formatting, and updating metadata. For tasks involving computer vision, data augmentation is also a vital step that helps improve model generalization.

- 

Pre-computed augmentation: Applies transformations in advance, increasing storage requirements but potentially speeding up training.

- 

On-the-fly augmentation: Applies transformations dynamically during training, saving storage costs but increasing computational load.

A more advanced technique gaining traction is the use of heterogeneous clusters that combine CPU and GPU nodes. In this setup, CPU nodes handle preprocessing and augmentation tasks, freeing up GPUs to focus exclusively on model training. Frameworks like Ray are particularly effective in managing such clusters, offering in-memory storage and flexible scheduling that optimize performance.

From a storage perspective, data preparation presents several unique challenges. The file sizes involved can vary widely, from as small as 4KB to several gigabytes. Additionally, the read/write patterns are often unpredictable, with frequent read-modify-write operations that require robust storage solutions. In many cases, distributed computing resources are involved, further complicating the storage requirements. Given these challenges, the choice of storage solutions becomes critical.

### Recommended storage solutionsRecommended storage solutions

- 

S3-compatible object storage like the one Nebius provides: Enables excellent scalability and compatibility with various data processing frameworks. It is particularly advantageous when prepared data needs to be streamed to different GPU providers for training. Object storage’s durability and cost-effectiveness make it an attractive choice for large datasets.

- 

Shared filesystem: Best used for heterogeneous clusters, which implies that data, CPU, and GPU compute must be within one provider’s network.

## Data streaming for trainingData streaming for training

Efficient data streaming to GPU accelerators is key for maintaining high utilization rates and minimizing training time. This process typically involves transferring datasets from storage to the host machine’s RAM and then moving the data into GPU memory in batches.

The choice of storage solutions at this stage can significantly impact overall performance, with key factors including:

- Dataset size (ranging from 1GB to 100TB+)

- File sizes (from 39KB image files to 110MB TFRecord files)

- Model size (smaller models require more frequent data streaming)

Recent developments in storage technology have made significant strides in improving the interfacing with object storage systems. For example, AWS and Mosaic have introduced connectors that allow to optimize performance when streaming data from S3-compatible storage, thereby reducing transfer overhead and simplifying data pipelines. This is particularly beneficial when dealing with large-scale datasets, where efficient data shuffling between epochs is essential for preventing biases and ensuring that the model generalizes well.

Performance targets for data streaming:

 | Compute components
 | Operation
 | Good, GB/s
 | Better, GB/s (H100/H200)
 | Best, GB/s (B100/B200)

 | Single GPU
 | Read
 | 0.5
 | 1
 | 2

 | Single node
 | Read
 | 4
 | 8
 | 16

### Recommended storage solutionsRecommended storage solutions

- 

High-performance shared filesystem: The default solution for most training workloads. Nebius’s file storage, with its distributed nature and high performance, excels in such scenarios, offering efficient shuffling capabilities that are crucial for large-scale setups. For example, Nebius offers a shared filesystem that provides lower latency compared to object storage and POSIX compatibility, which can be crucial for certain applications.

- 

S3-compatible object storage: For those dealing with large-scale data but with less stringent performance needs — especially when dataset size exceeds 1TB.

- 

Local SSD cache: Local storage could be placed between S3 and GPU instances and used as a cache to accelerate subsequent epochs, further optimizing the training process.

## BandwidthBandwidth

As deep learning models and datasets grow in size, the bandwidth requirements for storage solutions become increasingly critical. Both aggregate bandwidth, which is the maximum data transfer capacity between the storage cluster and all its clients, and client bandwidth, the maximum data transfer capacity for a single virtual machine, must be carefully considered.

During our study, we found that in larger clusters, aggregate bandwidth requirements do not scale linearly, which can present challenges.

Performance targets for bandwidth:

 | Number of nodes (8 GPUs per node) in training cluster
 | 8
 | 16
 | 32
 | 64
 | 256

 | Good — text-only datasets
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.134
 | 0.534
 | 4.667
 | 12
 | 20

 | Better — multimodal LLM training
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.267
 | 1.067
 | 9.334
 | 24
 | 40

 | Best — image/video generation models
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.667
 | 2.667
 | 23.336
 | 60
 | 100

A tiered storage approach can be particularly effective in managing these varying bandwidth requirements.

### Recommended storage solutionsRecommended storage solutions

- Compressed images, compressed audio, and text data can be stored in both shared filesystem and S3-compatible object storage solutions, as the bandwidth requirement is not very high.

- Image and video generation models might necessitate a high-performance shared filesystem or S3-compatible object storage with local SSD cache solution capable of handling massive bandwidth and I/O requirements.

## CheckpointingCheckpointing

Checkpointing, the process of saving a model’s state at a particular point during training, is crucial for resuming training after interruptions.

Checkpoint size is a key consideration, typically requiring 12 bytes per model parameter (4 bytes for model parameters, 8 bytes for optimizer state). For context:

- 

BERT-like models: ~2B parameters

- 

GPT-3 and successors: 175B+ parameters

- 

Cutting-edge models: Approaching or exceeding 1 trillion parameters

For a 300B parameter model, our own and clients’ experience suggests allocating about 30 minutes daily for checkpoint writing and aiming for under 10 minutes per checkpoint read.

There are two main types of checkpointing: synchronous and asynchronous. Each comes with its own set of trade-offs.

Synchronous checkpointing, while simpler to implement and highly reliable, can pause training during the saving process. This requires extremely high write bandwidth, especially for large models, to minimize the impact on overall training time. For example, a model with 300 billion parameters might require several terabytes of storage for each checkpoint, with write speeds needing to exceed 100 GB/s to keep overhead manageable.

Asynchronous checkpointing, on the other hand, allows training to continue while the checkpoint is being saved. This can potentially lead to faster overall training times, but it comes with a higher risk of checkpoint corruption if a node fails during the process.

Performance targets for checkpointing:

 | 
 | 2B model
 | 8B model
 | 70B model
 | 180B model
 | 300B model

 | Checkpoint size, GB
 | 24
 | 96
 | 840
 | 2160
 | 3600

 | Number of nodes in training cluster
 | 2-8
 | 4-16
 | 16-128
 | 32-256
 | 64-2048

 | Good: 5% overhead on writing = 180 seconds per hour
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.4
 | 1.2
 | 10
 | 24
 | 40

 | Write sync, GB/s
 | 0.2
 | 0.6
 | 5
 | 12
 | 20

 | Write async, GB/s
 | 0.02
 | 0.06
 | 0.5
 | 1.2
 | 2

 | Better: 2.5% overhead on writing = 90 seconds per hour
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.6
 | 2.2
 | 20
 | 48
 | 80

 | Write sync, GB/s
 | 0.3
 | 1
 | 10
 | 24
 | 40

 | Write async, GB/s
 | 0.03
 | 0.1
 | 1
 | 2.4
 | 4

 | Best: 1% overhead on writing = 36 seconds per hour
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 1.5
 | 6
 | 48
 | 120
 | 200

 | Write sync, GB/s
 | 0.7
 | 3
 | 24
 | 60
 | 100

 | Write async, GB/s
 | 0.07
 | 0.3
 | 2.4
 | 6
 | 10

### Recommended storage solutionsRecommended storage solutions

- 

High-performance shared file system: For large-scale clusters.

- 

Tiered approach: Recent checkpoints on high-performance storage, older ones on cost-effective solutions.

## Fine-tuningFine-tuning

Fine-tuning, a process that adjusts a pre-trained model to better fit a specific task, operates on a smaller scale compared to initial training but still requires careful consideration of storage needs.

Unlike initial training, fine-tuning typically involves shorter durations — ranging from minutes to hours — and a reduced need for intermediate checkpoints. This difference stems from the shorter duration and smaller checkpoint sizes required (since the optimizer state isn’t needed): just 4 bytes per model parameter.

Performance targets for fine-tuning:

 | 
 | 2B model
 | 8B model
 | 70B model
 | 180B model
 | 300B model

 | Checkpoint size, GB
 | 8
 | 32
 | 280
 | 720
 | 1200

 | Good: Read & write duration: 60 seconds
 | 
 | 
 | 
 | 
 | 

 | Read & write not slower than, GB/s
 | 0.268
 | 1.068
 | 9.334
 | 24
 | 40

 | Better: Read & write duration: 30 seconds
 | 
 | 
 | 
 | 
 | 

 | Read & write not slower than, GB/s
 | 0.534
 | 2.134
 | 16.667
 | 48
 | 80

 | Best: Read & write duration: 12 seconds
 | 
 | 
 | 
 | 
 | 

 | Read & write not slower than, GB/s
 | 1.334
 | 5.334
 | 46.667
 | 120
 | 200

### Recommended storage solutionsRecommended storage solutions

- 

Shared file system: for multi-node fine-tuning

- 

Local NVMe SSD: single-node fine-tuning and short-term storage of recent checkpoints.

## InferenceInference

Inference, which focuses on the deployment of models for real-time or batch predictions, shifts the emphasis from write performance to rapid read access.

During inference, the storage system must deliver model weights at high speed to minimize startup time and handle bursty traffic through auto-scaling. This places additional demands on the storage infrastructure, which must be capable of rapidly providing model data to newly spawned inference instances.

Performance targets for inference scenarios:

 | 
 | 2B model
 | 8B model
 | 70B model
 | 180B model
 | 300B model

 | Checkpoint size, GB
 | 8
 | 32
 | 280
 | 720
 | 1200

 | Number of nodes in cluster
 | 1
 | 1
 | 1
 | 1 with H200 or 2 with H100
 | 2

 | Good: Read for 60 seconds
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.15
 | 0.6
 | 5
 | 12
 | 20

 | Better: Read for 30 seconds
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.3
 | 1
 | 10
 | 24
 | 40

 | Best: Read for 15 seconds
 | 
 | 
 | 
 | 
 | 

 | Read, GB/s
 | 0.7
 | 3
 | 19
 | 48
 | 80

### Recommended storage solutionsRecommended storage solutions

- 

Shared filesystem: For sharing data within inference cluster in use cases like autoscaling.

- 

Object storage: For sharing inference results with the public.

## Storage solutions overviewStorage solutions overview

A tiered storage approach often provides the best balance for managing the diverse demands of deep learning scenarios.

A high-performance shared filesystem is ideal for active data and recent checkpoints, offering the speed and reliability needed for demanding training and inference tasks. Object storage serves as a cost-effective solution for long-term storage and archival. Local NVMe SSDs or high-performance network block storage provide the necessary speed for caching and quick data retrieval.

 | Storage type
 | Use cases

 | Shared filesystem
 | Data streaming, checkpointing, and sharing any data between GPU hosts.

 | Object storage (S3-compatible)
 | Large dataset storage, sharing inference results, potential for data streaming.

 | Network block storage and local NVMe SSDs
 | Boot disks, SSD cache, additional storage for self-managed solutions.

## Key takeawaysKey takeaways

One of the main lessons here is the importance of flexibility. What works well for one stage of the machine learning lifecycle might not be suitable for another. For instance, the storage requirements for data preparation are vastly different from those needed for inference.

Another important aspect to consider is the integration of storage solutions with other components of the deep learning infrastructure. Whether it’s ensuring that storage systems are aligned with the latest GPU accelerators, or that they can seamlessly integrate with data processing frameworks, the ability to create a cohesive and well-integrated system is crucial for maximizing performance.

Ultimately, the goal is to create a storage foundation that not only meets today’s needs but is also adaptable enough to handle tomorrow’s challenges. The decisions you make about storage will have a profound impact on your ability to train and deploy cutting-edge models, manage large-scale datasets, and ultimately deliver value from your AI initiatives.

## Explore Nebius AI

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Igor Ofitserov
Technical Product Manager at Nebius AI

## See also

### 

H100 and other GPUs  — which are relevant for your ML workload?

Let’s break down the differences between NVIDIA’s top-tier GPUs and identify workloads where each GPU model performs at its best.

November 21, 2023
11 mins to read

### 

Slurm vs Kubernetes: Which to choose for model training

Scaling your machine learning workloads will eventually require resource orchestration. This article compares the most popular options today — Slurm and Kubernetes, covering their design origins, ML adaptations and other factors to consider.

May 29, 2024
13 mins to read

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

Sign in to save this post
Sign In
