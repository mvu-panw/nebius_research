# What are GPU clusters and how to choose yours?

Source: https://nebius.com/blog/posts/what-are-compute-clusters-and-how-to-choose-yours

Skip to main content

The AI boom has fueled enormous interest in training and running large foundational models, as well as building agentic AI applications. This has created a pressing need for powerful computational infrastructure because generative AI and large language models (LLMs) require immense computational resources, and it’s impractical to train or fine-tune them on a single GPU. By leveraging parallel computing setups, GPU clusters enable businesses to handle GenAI workloads and LLMs at scale, delivering the speed and efficiency required to stay competitive in the AI race. But what exactly are GPU clusters, and how do you choose the right one for your needs? Let’s dive in.

# What is a GPU cluster?What is a GPU cluster?

In theory, even 2 GPUs working together make a GPU cluster. But when people refer to ‘GPU clusters’, they usually mean multi-node (or multi-host) installations with dozens, hundreds or even thousands of GPUs.

Still, it isn’t just plug and play; you don’t get a number of GPUs and say you have a cluster. To orchestrate GPU clusters, you must employ parallel computing — an approach where one big task (e.g. model training) is broken down into multiple small operations. And each of these operations is assigned to particular interconnected GPUs.

Distributed training and inference accelerates computing operations like large-scale research, heavy-duty image and video processing, big data analytics, and model training. It makes sense to use GPU clusters for these use cases because GenAI workloads and LLMs are very compute demanding, and require parallel processing powers beyond what a single GPU can handle.

You’ve probably used GPT or Meta AI at some point; GPU clusters are what make such large language models (LLMs) and multi modal models (that are much bigger than LLMs) possible.

# Uses of GPU clustersUses of GPU clusters

GPU clusters are mostly used for AI/ML-related activities that typically comprise three functions:

- Training AI models

- Fine-tuning AI models

- Inferencing AI models

### Training AI modelsTraining AI models

GPU clusters are the go to for GenAI model training and it’s easy to understand why. GenAI models are trained on massive datasets — sometimes to the tune of petabytes. In addition, the process starts from raw data collection, followed by preprocessing, then training, and tokenization; all of which can take weeks or months to complete. This goes to show that without GPU clusters, training models at such scale would be impossible.

For context, the old GPT-3 was trained on 300B tokens and 175B parameters — and took months to complete. Bigger models — than GPT-3 — can be created with fewer, more powerful GPU clusters, and in less time too. In summary, using GPU clusters is the only way to create a foundational model from scratch for your AI needs.

### Fine-tuning AI modelsFine-tuning AI models

Although model fine-tuning (or model optimization) typically requires much less computational resources than training, GPU clusters remain important at this phase, as they make fine-tuning significantly faster.

For example, from the GPT assistant training pipeline image above, we can see that for all stages of the foundational model mentioned, the pre-training phase required 1000s of GPU clusters and months of running. On the other hand, the model optimization phases consisted of jobs that took just days to complete when up to hundreds of GPUs were deployed.

### InferencingInferencing

For inferencing, GPU clusters offer high-speed processing and enable seamless failover when some GPUs fail. GPU cluster size may vary depending on the type and quantity of requests the model is expected to serve. Real-time and asynchronous inference workloads serving via web endpoints are defined by the number of end user requests and its content — the more API calls they make, the more GPU compute you need to provision.

# Components of GPU clustersComponents of GPU clusters

Now that we understand what GPU clusters are used for, let’s explore GPU cluster components — hardware, software, networking and storage — and where they fit in.

But before that, it’s important to know that GPU clusters are made up of two functional types of GPU nodes: head node and worker nodes. Each type performs independent roles but also connects to the other. Here’s a closer look.

- 

The head node: There’s usually one head node responsible for cluster management. The head node is a persistent instance or server tasked with orchestrating the cluster, scheduling jobs to worker nodes, and managing cluster resources. It also receives network requests from external systems and passes them to worker nodes.

- 

The worker nodes: This is where all the main compute-heavy jobs like model training and inference happen. There are usually as many worker nodes as required to complete a task. Worker nodes connect to the head node via fast Ethernet connections to receive task schedules, report on job status, and update the head node on GPU cluster resource utilization.

Worker nodes also network with one another ensuring that subtasks assigned to various GPUs are completed cohesively. Worker nodes can be virtual machines (VMs) or physical servers (bare metal servers), depending on the setup and workload.

GPU cluster makeup: Head and worker nodes

While the head node often sits at the top as represented in the image above, in some cases, it sits next to the worker node on the same physical server.

### GPU node hardwareGPU node hardware

A typical worker node in a GPU cluster is a server equipped with one or more GPUs, designed to handle parallel processing tasks efficiently. The key components of the GPU node hardware include the GPU accelerators, high-performance CPUs, system memory (RAM), and NIC, all explained in the table below.

 | Hardware component
 | Function

 | GPU
 | GPU accelerators are the individual processors that form the whole (i.e. the cluster), each designed to handle intensive concurrent computations. Common examples of GPUs include NVIDIA H200 Tensor Core GPU or NVIDIA L40S GPU.

 | CPU
 | CPUs manage the tasks conducted by GPUs; preprocessing data, orchestrating tasks, and feeding data to GPUs. CPUs also run non-parallelizable tasks that require serial processing. Common examples of CPUs include the Intel Sapphire Rapids and AMD Epyc Genoa.

 | RAM
 | GPU memory (or VRAM) is an integral part and a characteristic of GPUs. RAM helps perform server tasks and enable the software running.

 | NIC
 | The network interface card (NIC) is a hardware component that connects GPU nodes to one another, to the cluster network, and to external data sources.<br><br> NICs come with one or more ports; with multiple ports, NICs can either be used to connect GPU nodes to several networks simultaneously or they can be bonded together in units of 2 to improve network bandwidth.<br><br> NICs are deployed in PCIe slots, which are built into motherboards. This way, the PCIe facilitates high-speed connections between the NIC and the rest of the system.<br><br> In GenAI, NICs that support Remote Direct Memory Access (RDMA) are particularly beneficial due to their low-latency, high-bandwidth, and minimal CPU usage. Top examples include the NVIDIA Bluefield-3, NVIDIA Mellanox ConnectX-7, and Intel E810-2CQDA2.

### GPU cluster orchestration softwareGPU cluster orchestration software

GPU cluster software helps to manage the hardware nodes. It includes the operating system (OS) which controls how hardware resources are used, and workload managers that manage cluster nodes and ensure their health. Workload managers often used in GPU clusters are Kuberenetes, Simple Linux Utility for Resource Management (Slurm), a combination of both, or Ray.

- 

Kubernetes handles many tasks including container execution and scaling. It manages your GPU nodes and ensures the exact number of GPUs needed are always running, scaling nodes up or down dynamically in response to traffic.

- 

Slurm automates task scheduling and batch processing. It manages jobs on a queue and shortens wait times between when one batch is completed and the next begins, optimizing cluster resource usage. It equally determines the right task to assign to nodes and monitors nodes to ensure as many jobs are run simultaneously as possible while managing job queues effectively.

- 

Ray lets you containerize GPU workloads, run parallelized tasks smoothly, and scale workloads autonomously. It also runs task scheduling and offers in-memory storage. But in addition to its capabilities as an orchestration platform, Ray has a set of built-in libraries specifically suited to GenAI use cases. Ray Train facilitates distributed model training and fine-tuning at scale, Ray Tune is the Ray go-to library for hyperparameter tuning, Ray Data offers a scalable and flexible set of APIs for processing large volumes of ML data, and there’s more yet.

### GPU cluster networkingGPU cluster networking

GPU cluster networking refers to the communication channels between nodes, facilitated by NICs. For GPU cluster performance to remain at optimal levels, inter-node traffic must be fast and seamless. Now, remember we mentioned earlier that when we think GPU clusters, we think multi-node installations with many GPU-based servers and dozens, hundreds or even thousands of GPUs?

What this means is, if your cluster consists of lower than 8 GPUs, all sitting within the same server, server-to-server networking is not something you should bother with — you have GPU-to-GPU NVLink or Peripheral Component Interconnect Express (PCIe) bus connections to facilitate inter-GPU communication within the node.

But if you have a multi-server setup, usually required for GenAI workloads, then fast interconnect and well-configured NICs are critical to cluster or inter-node networking. The higher the Gbps an NIC offers, the more suited it is to HPC workloads where petabytes of data must move seamlessly across nodes. Some new generation NICs (e.g. ConnectX-7) offer up to 400 Gbps speeds and 800 Gbps in dual port configurations, easily supporting exascale computing requirements.

Now, let’s talk about the networking itself — NICs must support one or more of the major technologies used for GPU cluster networking. These technologies, all designed for fast, bottleneck-free GPU performance include: InfiniBand, RoCE, iWARP, Spectrum-X (NVIDIA’s proprietary Ethernet Networking platform), Elastic Fabric Adapter (AWS’ proprietary networking platform), and a number of others. There’s also Ethernet, the most popular, which works at varying speeds depending on your NIC and use case.

High-speed networking channels are essential because they help to maximize clusters’ computing power, ensure non-blocking, and cut latency and performance bottlenecks. When NICs are improperly configured or low-speed NICs are used, bottlenecks become a big issue, often meaning very little of the GPU resources will be appropriately deployed or performance will be much slower than required.

### GPU cluster file storageGPU cluster file storage

Unlike smaller models where data can be stored in memory, doing the same for GenAI models will be too cost-prohibitive and can lead to data bottlenecks — that’s where file storage comes in. File storage is where model weights, checkpoints, and data are saved to and loaded from during training, fine tuning and inference.

File storage enables data streaming, allowing different nodes to swiftly access distributed data simultaneously — which facilitates parallel computing, the capability that makes GPU clusters so effective for GenAI.

Moreover, file storage is critical for storing model checkpoints — saves or snapshots of the model’s state at a specific time. Consider these use cases of file storage for model checkpointing:

- 

Seamless Recovery. Picture this: During model training, a GPU suddenly fails, a not uncommon scenario. This would ordinarily be a big setback. But checkpoints allow you to retrieve the model’s state so you don’t have to start afresh. The same applies if there’s a mistake at a point in the training — previous error-free saves to the rescue! Or there’s a need to suspend and resume model training? No need to start over.

- 

Model experimentation. By saving state, checkpoints make it possible to train and test run several models at a go, letting you compare model snapshots to determine and choose the best-performing model once training is done. File storage is also critical for large datasets, especially during model training and inferencing for image and video generation.

# How to choose the right GPU clustersHow to choose the right GPU clusters

When selecting GPU clusters, consider your use case (training, fine-tuning or inference) and the type of cluster you need. This will inform your hardware, orchestration software, storage and networking choices. Also, your use case will determine your ideal budget and other business terms, like whether or not you’ll need technical guidance or subscribe to long-term commitments. Here are some considerations to help you choose the ideal GPU clusters.

### Ask the right questions when choosing hardware for cluster nodesAsk the right questions when choosing hardware for cluster nodes

Consider quality and quantity when choosing the right hardware for your cluster. This will determine if your clusters’ performance and scalability will suit your use case in real world scenarios. Consider your budget, desired performance, and cluster stability requirements. Below are some questions you can ask.

For training, how many GPUs do you need? Do you need the latest GPU model with better performance or can you sacrifice speed in favor of budget limitation? Do you need more GPUs with less performance or fewer advanced GPUs?

For inference, how much memory does this GPU have? It’s important because it determines how many GPUs will be needed to serve your GenAI model. For example, if you have a 140GB-sized Llama 3.1 70B BF16 model, you will need at least 4 NVIDIA H100 Tensor Core GPUs or just 2 NVIDIA H200 Tensor Core GPUs.

Once you have a rough idea of your next AI project, ask your cloud service provider if they have appropriate GPU clusters with the storage, networking, software and support you need. And If you are going to run real-time or asynchronous inference online, ask if they have CPU-only compute instances to serve web endpoints for your AI application.

### Verify provider’s cluster management software optionsVerify provider’s cluster management software options

Speaking of cluster management software, the two most popular options on the market are Slurm and Kubernetes. Providers coming from the general software engineering angle tend to prefer Kubernetes while those from the academia and HPC world would choose Slurm.

Natively, Kubernetes works well for scaling clusters — a major plus for model inference. But Kubernetes isn’t ready for the job queuing and scheduling requirements of GenAI model training. Still, a range of tools and libraries work over Kubernetes to enable it to run ML training and inference, but your team must be skilled enough to assemble this stack for your needs.

On the other hand, Slurm provides advanced job scheduling mechanisms allowing you to set up tasks for individual hardware units and create job queues at scale. But, it’s very demanding in terms of scaling and maintenance. Also, its interface may look quite “old-fashioned” for modern ML engineers.

With both having their unique limitations, there’s demand for a middle ground, so some AI cloud providers have developed proprietary Kubernetes-Slurm integrations that combine core features of both software. At Nebius for instance, we’ve developed Soperator, a Kubernetes operator for Slurm, allowing you to use Slurm’s job scheduling capabilities in addition to seamless workload scaling via Terraform. But that’s not all. Soperator also has quite some interesting features for guaranteeing cluster availability — and it’s open source.

### Consider high-speed networking and storageConsider high-speed networking and storage

The ideal GPU cluster is one where fast networking and data access meet reliability and cost efficiency. High-performance, high-speed networking and storage solutions will provide the lightning fast data transfer and retrieval speeds you need for GenAI training, finetuning, and inferencing.

Fast storage and network are also crucial for quick checkpointing, which is in turn vital for effective training. GPU failure rate is generally high; you cannot control this. What you can control is how swiftly and reliably checkpoints are saved and restored in your chosen GPU cluster.

Storage and networking speed, stability, and reliability is especially vital in large scale models with thousands of GPUs because the littlest disruption will cause you huge losses. For networking, InfiniBand is a good choice, and it’s best practice to opt for providers with fast storage and a variety of storage options.

### Consider data center facilitiesConsider data center facilities

Ownership, power efficiency, and sustainability are key issues to consider here.

Ownership: Verify that your vendor has their own facilities or direct control over them — having control over their own infrastructure means they can have engineering teams on site to monitor the facilities, prevent technical issues in advance, or quickly fix issues before they impact your workloads. This directly impacts the reliability and resilience of your GenAI infrastructure.

Power efficiency: Consider a service provider with data centers that consume minimal power. By cutting power consumption, your provider can save on energy bills which can translate to more competitive pricing for you. Efficient cooling infrastructures are some of the things you can look at; they make data centers more power-efficient, thereby making the GPU sustain high performance levels for long periods.

Sustainability: If you are a small startup or in a rush because of the hard competition, sustainability may not seem very important at this time. But the carbon footprint of GenAI — and data centers in general — is becoming huge enough that environmental management regulations are springing up to address it. So partnering with a sustainability-oriented provider demonstrates your commitment to running an eco-friendly business, helps you meet compliance laws, earns you the right reputation, and helps you avoid potential losses in the long term — all good for business.

### Factor in costs and provider offeringFactor in costs and provider offering

There are a number of best practices here, particularly regarding the choice between going for:

- 

Investigate the credibility and future potentials of the provider. Be sure the provider can supply you with top-notch GPU hardware in the long run and any possible risks that may accompany long-term commitments to the provider.

- 

Choose a provider with flexible payment plans (best if the provider offers both reserved pricing and pay-as-you-go models).

- 

Compare the pricing vs. value offered. Besides the GPU pricing model, you must also consider other added services. For instance, will technical support and guidance be included? Are data transfer and storage costs added? Does the provider have its own infrastructure? How quickly does the cluster start working after payment — any form of delay after payment eats into your budget.

# Running GPU clusters with NebiusRunning GPU clusters with Nebius

Nebius helps you set up fast, reliable and cost-efficient GPU clusters using the latest technologies — including the NVIDIA Blackwell GPU-powered clusters. This helps you strike a balance between top-of-the-range speed, budget-friendly pricing (pay-as-you-go model), and best-in-class GPU performance. You can also deploy any of our powerful GPU cluster orchestration software options: Managed Kubernetes, Kubernetes-Slurm integration — Soperator, or Ray Cluster.

Because we understand that legacy software can feel glitchy on next-gen hardware, our skilled engineering teams are developing a custom-made software layer to go with the new-tech NVIDIA hardware. Our goal? Ensuring reliable, glitch-free operations for our customers.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

What is a token in AI? Understanding how AI processes language with tokenization

Explore what tokens are, how they enable AI models to understand and process language, represent text in AI systems and why tokenization is critical for LLMs. This post will also allow you to understand different tokenization techniques, how they affect processing efficiency and how modern NLP models like transformers use them to deliver accurate and context-aware responses.

February 10, 2025
15 mins to read

### 

What is prompt engineering?

Prompt engineering has advanced considerably in the last three years. This article overviews the process and includes several beginner and advanced strategies to help AI teams get the most out of their LLM models.

December 17, 2024
12 mins to read

### 

What is inference?

Machine learning inference tests a model against real-world unseen data. Understand what is inference, and how models are deployed in production.

September 20, 2024
9 mins to read

Sign in to save this post
Sign In
