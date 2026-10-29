# The role of compute cluster networking for AI training and inference

Source: https://nebius.com/blog/posts/cluster-networking-for-ai-training-inference

Skip to main content

Modern AI workloads demand computational power far beyond traditional hardware. A typical generative AI (GenAI) job requires tight coordination between tens of thousands of GPUs over several weeks. These GPUs must continuously exchange data across a network to maintain efficiency. Without a high-performance networking infrastructure, even the most powerful GPUs face bottlenecks that slow down training and limit scalability.

# What are GPU cluster networking technologies?What are GPU cluster networking technologies?

GPU cluster networking technologies are high-speed interconnects linking together GPUs in a cluster. A GPU cluster is a multi-server installation ranging from a few dozen to several thousand GPUs, as the project requires. The typical AI server or GPU server contains 4-8 GPUs. The latest rack solutions feature up to 72 chips in a single optimized platform.

GPU cluster networking technologies fall into two broad categories.

### Intra-server communication elementsIntra-server communication elements

They facilitate communication within the AI server. For example, Peripheral Component Interconnect Express (PCIe) is the standard bus connecting GPUs to the server’s CPUs and memory. NVIDIA NVLink is a technology with bidirectional direct interconnect within the server.

### Inter-server communication elementsInter-server communication elements

Some new-generation NICs support remote direct memory access (RDMA), which moves data directly between the memory of two servers using specialized RDMA-capable network adapters (such as InfiniBand or RDMA over Converged Ethernet (RoCE)). Data exchange bypasses the CPU, reducing computational overhead and enabling faster, more efficient communication.

### How networking works in GPU clusters for AIHow networking works in GPU clusters for AI

You can think of a GPU cluster network as working over three layers.

Layer 1 is the standard network technologies like VPC links, transit gateways, firewalls and other security layers that connect the GPU cluster to the outside world. Input data from your end users comes to your AI application and reaches the cluster through this layer. After final data processing, the output from the AI model is communicated to end users through this layer. Similarly, any training data inputs from internal knowledgebases go through this layer before reaching the model.

Layer 2 comprises the inter-server elements connecting the different GPU servers.

Layer 3 is made of intra-server elements connecting the GPUs within a server. Data flows through layers 2 and 3 within the model — during model training and inference.

# Designing GPU clusters for AIDesigning GPU clusters for AI

When building your AI data center, you should explore various networking topologies to optimize network connections. A network topology provides a template for connecting the different GPU servers and networking technologies to maximize efficiency. There are several, but we describe three that are more popular.

### Fat-tree topologyFat-tree topology

A two-level fat-tree topology, or the spine-leaf architecture, is commonly used for AI training with 8-GPU servers. In a typical setup:

- 

Each server has 8 GPUs and each GPU is connected to a dedicated leaf switch via its NIC.

- 

A leaf switch has 128 ports with 64 ports dedicated to GPUs, allowing 512 GPUs per group (64 GPUs per cluster × 8 clusters).

- 

Each leaf switch connects upward to a spine switch, ensuring a full-mesh connection between all leaf and spine switches.

- 

In a standard deployment, there are 64 spine switches, each connecting to all 128 leaf switches.

A three-level fat-tree topology extends the spine-leaf model by adding another layer of switches. The spine switches connect to an additional layer of core switches to further aggregate network traffic. This design supports tens of thousands of GPUs, ensuring network congestion does not become a limiting factor as the cluster scales.

### Torus topologyTorus topology

The torus topology connects GPUs in a grid-like structure, allowing direct communication between servers while minimizing reliance on centralized switches.

In a 2D torus, GPUs are arranged in a grid, where each server connects to its four immediate neighbors (left, right, top, bottom). The edges of the grid wrap around, forming a continuous loop—moving off one edge brings you back on the opposite side. Each GPU connects only to its nearest neighbors, reducing the required long-distance network links.

A 3D torus extends the 2D torus by adding another dimension, creating a cube-like structure, where each server connects to six neighbors (left, right, front, back, top, bottom). This reduces the average number of hops required for communication compared to 2D torus.

### Dragonfly topologyDragonfly topology

Dragonfly topology connects every server to every other server in the cluster, reducing the hops required for inter-group communication. The network is divided into multiple groups, each containing a set of routers and AI servers. Routers within a group are fully connected to each other. Each router also connects to a subset of routers in other groups via direct global links. It incorporates redundant pathways, ensuring that alternative paths can be used to maintain uninterrupted communication even if a router or link fails.

The Dragonfly+ topology is an enhanced version of Dragonfly that further improves scalability and fault tolerance.

# Why are GPU cluster networking technologies critical for AI training?Why are GPU cluster networking technologies critical for AI training?

AI model training involves massive datasets and complex computations. High-speed cluster networking technologies in layers 2 and 3 help as follows:

### Real-time data exchangeReal-time data exchange

GPU cluster networking technologies support real-time training and inference. For example, reinforcement learning requires AI agents to constantly update their models based on new experiences. It requires continuous data exchanges between GPUs to synchronize model parameters and exchange gradients for real-time training data. GPU cluster networking makes this possible.

### ScalabilityScalability

Large-scale AI model training involves processing massive datasets and performing trillions of mathematical operations. The computational demand grows exponentially as models become larger.

For example, an LLM with 175 billion parameters requires approximately 3.14E23 FLOPs (floating point operations) for full training. If trained on a single modern accelerator, it would take approximately 165 years to complete. By distributing the workload across 1,024 accelerators, the training time theoretically drops to around 16 days.

However, without an optimized network, increasing the number of GPUs does not translate to a proportional increase in performance. GPU cluster networking elements are necessary to avoid diminishing returns due to communication overheads between GPUs.

### Parallel processing efficiencyParallel processing efficiency

AI workloads rely on parallelism to accelerate training. There are two primary types of parallelism:

- 

Data parallelism — different GPU groups process different data subsets of a large training dataset.

- 

Model parallelism — different GPU groups handle separate parts of a large model.

Efficient networking ensures that parallelized computations remain synchronized without excessive communication delays.

### Lower costsLower costs

During network congestion, GPUs remain idle, waiting for data, leading to wasted compute cycles. Overall operational slowdown increases energy costs in a data center and higher training costs billed per GPU hour in the cloud. A well-optimized GPU cluster network minimizes data transfer delays and the associated costs.

# Best practices in GPU cluster networking for AIBest practices in GPU cluster networking for AI

Consider the following GPU cluster management best practices.

### Optimize network topologyOptimize network topology

Fat Tree offers non-blocking connections, Torus provides efficient multi-dimensional routing and Dragonfly minimizes hops between groups. Select the appropriate topology for balancing latency and bandwidth requirements in AI workloads. Fat Tree and 2D-Torus are preferred for smaller workloads, while 3D Torus and DragonFly+ are better suited for large numbers of clusters.

### Implement traffic optimizationImplement traffic optimization

Traditional network optimization techniques are effective in GPU cluster networking, too. Implement load balancing, adaptive routing and congestion control mechanisms to dynamically adjust data paths based on current network conditions.

### Monitor and tune performanceMonitor and tune performance

Tools such as Prometheus and TensorBoard provide insights into network health and performance metrics. Regular data analysis allows for informed adjustments, ensuring optimal operation and aiding in the convergence of AI models by minimizing delays and resource contention.

### Ensure data synchronizationEnsure data synchronization

In distributed AI training, you can use software alongside topologies to enhance synchronization. For example, Ring-AllReduce is an algorithm that organizes GPUs in a logical ring topology. Each GPU communicates only with its two immediate neighbors, passing data chunks around the ring in multiple steps to optimize bandwidth utilization.

### Implement fault toleranceImplement fault tolerance

Implement fault tolerance measures like redundancy and auto-scaling to enhance system reliability. For example, checkpointing strategies periodically save model states to reduce the impact of unexpected failures.

# Future trends in GPU cluster networking technologiesFuture trends in GPU cluster networking technologies

Many advances are happening in the space that promise better performance and efficiency at lower costs.

### Optic technologiesOptic technologies

Photonics-based switches aim to deliver speeds up to 1.6 Tbps per port. Ultra-fast optical transceivers in the GPUs can provide even lower latency.

### AI-optimized network architecturesAI-optimized network architectures

Smart Network Interface Cards (SmartNICs) and software-defined networking are enabling more efficient data flow and processing. Traditional networking infrastructures are being reengineered to improve communication efficiency between GPUs, leading to faster and more reliable AI model training.

### Cloud and edge AI networkingCloud and edge AI networking

The convergence of cloud and edge computing is reshaping AI training paradigms. They allow you to use techniques like federated learning to train across multiple data sources. For example, you can implement decentralized model training across diverse devices for data privacy.

### Automated network managementAutomated network management

AI-driven tools facilitate dynamic network tuning, predictive maintenance and anomaly detection to deliver advanced congestion control and adaptive routing.

# ConclusionConclusion

GPU clusters perform to their full potential when supported by the right networking infrastructure. Cluster networking technologies for AI are designed to support high-speed data operations at both inter- and intra-server levels. Designing the right cluster topology is just the start. You must also use software-based strategies to optimize your network and monitor for ongoing performance.

While GPU cluster networking technologies are complex, Nebius helps you set up fast and reliable GPU clusters that balance performance and cost. You get access to AI clusters and deploy powerful cluster orchestration software like Managed Kubernetes and Soperator. We are also developing a custom-made software layer to go with the latest hardware.

Get started with reliable, glitch-free operations with GPU clusters in the Nebius AI Cloud.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- What are GPU cluster networking technologies?

- Intra-server communication elements

- Inter-server communication elements

- How networking works in GPU clusters for AI

- Designing GPU clusters for AI

- Fat-tree topology

- torus-topology

- Dragonfly topology

- Why are GPU cluster networking technologies critical for AI training?

- Real-time data exchange

- Scalability

- Parallel processing efficiency

- Lower costs

- Best practices in GPU cluster networking for AI

- Optimize network topology

- Implement traffic optimization

- Monitor and tune performance

- Ensure data synchronization

- Implement fault tolerance

- Future trends in GPU cluster networking technologies

- Optic technologies

- AI-optimized network architectures

- Cloud and edge AI networking

- Automated network management

- Conclusion

## See also

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

GPU vs CPU: what is the best bioinformatics accelerator?

Speeding up computational tasks is critical to push the boundaries of science and ensure scalability and efficiency. Check out how NVIDIA Hopper GPUs available on Nebius AI Cloud performed against CPU workflows to accelerate homology research, deep learning-enabled protein embeddings and ML clustering.

March 24, 2025
6 mins to read

### 

The difference between AI training and inference

AI training and inference are critical stages in the machine learning lifecycle, each with distinct objectives and computational requirements. Let’s explore the key distinctions between AI training and inference, their unique resource demands and best practices for building scalable ML workflows.

July 25, 2025
10 mins to read

Sign in to save this post
Sign In
