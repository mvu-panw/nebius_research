# In-house AI R&D: Nebius’ secret ingredient for truly AI‑centric cloud

Source: https://nebius.com/blog/posts/llm/in-house-llm-rnd-team

Skip to main content

Severe GPU scarcity and struggles with MLOps are forcing ML engineers to more and more divert focus from model development. Such a shift harms the productivity of these specialists, who are primarily mathematicians and scientists. They are pushed to solve infrastructure issues instead of doing their core ML job.

There’s a gap between ML engineers and the infrastructure they can get from the market. We’re closing such a gap by bringing together three pieces: hardware, software and ML proficiency. Our extensive background in designing servers, racks and the whole DC structure led, for instance, to the construction the world’s #16 supercomputer (as of Nov 2023 — we multiplied our capacity x5 since then). After that, the decision to build a 10K GPU cluster, a scalable infrastructure of 10,000+ cards, was a natural one. Nebius software enables us to provide orchestrated machines on top of that, with diverse tools enhancing the setup.

But then there’s the third piece, ML expertise. To build a full-fledged ML platform — an end-to-end management solution for the entire ML workflow — we realized it’s necessary to perform large-scale distributed training in-house. What else would enable us to practically understand ML engineers’ needs? That’s why we formed the AI R&D team, leveraging our compute capacities to let us deeply specialize the platform, while also advancing our own AI efforts. The team is led by Boris Yangel, a research engineer with more than a decade of experience leading complex AI projects, from neural world models for self-driving cars to text generation and understanding for AI assistants.

This article explains what we mean by dogfooding and briefly explores some of the findings and techniques of the AI R&D team in training, data processing and monitoring.

## What exactly do we mean by dogfoodingWhat exactly do we mean by dogfooding

Among all departments within the company, the AI R&D team interacted most with cloud solutions architects at the initial stages. We take pride in our CSAs — their key competencies lie primarily in assisting clients throughout the entire workload launch cycle, considering their requirements and constraints. To test a hypothesis that could potentially accelerate client onboarding or other processes, architects might run a simple distributed training or verification for themselves, such as an NCCL test across all nodes in a cluster (NCCL, of course, is a library for implementing optimized multi-node communication primitives). However, the AI R&D team’s capabilities in testing deeper hypotheses related to real ML engineer experience are much higher.

The AI R&D team was the first client of Nebius, even before external clients were connected. Among other things, the input of the team helped bring cluster characteristics to the levels now applicable to all users. Later, ML engineers assisted the whole GPU development team (consisting of many teams across Nebius) in optimizing network loads in our data center. They also helped optimize checkpointing, job scheduling and cluster scaling (network, scaling and storage are usually the bottlenecks when building large clusters for model training). Our ML engineers acted as the first 'filter' — their feedback allowed us to identify and address these and other weak points before the public launch of the platform.

The AI R&D team also acts as an early adopter of all our in-house developed hardware technologies. For example, our ML engineers are the first to test new types of nodes for model training (based on SXM5) and inference (PCIe-based). Another example is the introduction of new InfiniBand fabrics — each new fabric initially hosts the AI R&D team.

We see this as a significant competitive advantage, especially when rolling out major features. It lies in the fact that these features are tested by very strong domain experts. They can not only point out that something is not working but also dig much deeper to answer why it is not working. The AI R&D team is capable of investigating issues down to tracing processes within Linux, understanding why their code stumbles upon these processes. This is where the cloud architects' responsibility comes back in, finding ways to get more out of our systems. We hope we’ve conveyed the importance of this symbiotic relationship.

Also, as we all know, the main challenge in distributed model training is hardware failures. If you’ve dealt with general-purpose cloud computing, this might still sound surprising. How is it possible that CPU issues are the rarest while GPU issues are the most common? Yet, it is true. However, our AI R&D team has learned to 'survive' failures with relatively minor losses thanks to self-healing automation. The team’s techniques are passed on to cloud architects, who refactor the resulting code (or get inspired by it) and incorporate it into publicly available playbooks, ensuring resilience in clients' workloads. Our Architect Solution Library is a significantly modified and expanded version of the first playbook that architects handed over to our ML engineers in 2023. Artifacts from the interaction between these two teams also make it into the documentation — specifically, into the guidelines. For instance, we will soon release a guide on decommissioning nodes with failed GPUs. Any major feature we roll out is first fully dogfooded by following a continuously working path: AI R&D team — large reference clients — all Nebius clients. Few players on the market can afford this.

## In-house LLM training infrastructureIn-house LLM training infrastructure

Recently, the team has focused on building a cutting-edge, large-scale training infrastructure. Training models at scale efficiently presents unique challenges in infra management and systems engineering. After thorough testing, we’re confident our solutions effectively address these challenges.

### Efficient distributed trainingEfficient distributed training

Training large models requires tailored sharding strategies, as there’s no one-size-fits-all solution for distributing computations across a cluster. Optimal approaches vary significantly depending on the model’s parameter count and architecture. A flexible training framework that enables experimentation with different sharding strategies without altering model code can significantly accelerate training efforts. This is why we made sharding flexibility a core design principle of the training framework. Its key features include:

- JAX-based: Model code is written in JAX and compiled via XLA.

- Deterministic: Fully deterministic by design, simplifying reliable checkpoint recovery and training issue debugging.

- GPU-first: Training metrics and indicators are written in JAX and compiled into the training graph, avoiding costly device-to-host communication after each training step. Basically, if it can be done on GPU, it is done on GPU.

- Modular: Models are built from standard blocks, easily recombined to experiment with new architectures by adjusting a few lines in a YAML config file.

- Sharding-agnostic: Model developers attribute tensor axes with logical labels. A simple config then maps these labeled axes onto the physical dimensions of the device mesh. Next, the XLA compiler decides how to efficiently orchestrate communications within the chosen sharding scheme to achieve high throughput.

- Standard sharding techniques: Out-of-the-box support for ZeRO, data, tensor, sequence and expert parallelism, with arbitrary combinations. Different sharding schemes can be applied to different subgraphs of the computational graph to further improve throughput.

- Selective checkpointing: Allows rematerialization of select parts of the computational graph during the backward pass, optimizing GPU VRAM usage and reducing the need to store large tensors in memory.

- Custom kernels: Humans can often outperform the XLA compiler. Our framework offers efficient, well-tested kernels for IO-aware attention, mixture-of-expert token routing, grouped matrix multiplications and dropless mixtures of experts. We experimented with the Triton and Pallas kernel languages, achieving notable results. In MoE training, our custom group matrix multiplication kernel outperformed the baseline by 70% for long sequence lengths, allowing for near-zero compute overhead for any expert capacity value. Additionally, our hand-written router kernels significantly reduced routing latency and memory usage. We also identified and fixed a performance issue with the Flash Attention kernel implemented in Triton when running in bfloat16 on H100 GPUs. Our contribution to the Triton repository helped it match the performance in float16 precision, resulting in a 15% speed increase.

### FSDP and HSDPFSDP and HSDP

Our framework supports fully sharded data parallelism (FSDP) and hybrid sharded data parallelism (HSDP) — the first type enables sharding of model parameters across all GPUs in a cluster, while the second allows sharding within a single node with replication across nodes. This approach reduces memory overhead by using additional collective operations, such as all-gather for weights during forward and backward passes. Asynchronous communications allow overlapping the (i+1)th layer weights all-gather with the (i)th layer computation, minimizing overhead unlike tensor parallelism. However, FSDP can suffer slowdowns at large scales due to the slower GPU node interconnect, whereas HSDP mitigates this by using faster NVLink within a single node. Benchmarking our HSDP setup with selective activation checkpointing against PyTorch HSDP, we achieved 36% MFU for a 34B model and 37% MFU for a 70B model, closely approaching the PyTorch team’s reported performance without specific optimizations or low-level communication features.

### Data processing frameworkData processing framework

Large models are trained on vast datasets, often comprising 8–15 trillion tokens. High-quality training data is crucial for model performance, requiring extensive experimentation and complex processing techniques. Our data processing framework is built on top of TractoAI, a Nebius solution for reliable data storage and processing at scale. The framework provides us with:

- Flexible pipelines: Data transformation pipelines consist of atomic, self-contained steps implementing various data processing primitives like text embedding, tokenization, deduplication, sampling, or clustering. New primitives can be added with a few lines of Python code. Backend-agnostic transformations, ones that can run both on the cluster and locally, enabling easy debugging before large-scale execution.

- Direct streaming: Processed data streams directly into the training process from the data cluster, starting from any batch.

- Native integration with TractoAI features: TractoAI offers scalability, reliability, observability into data processing jobs and a convenient UI for inspecting and analyzing data.

### CheckpointingCheckpointing

Training large models requires a robust state checkpointing solution that doesn’t suffer from storage reliability issues or network bandwidth bottlenecks, especially for models with hundreds of billions of parameters. Our solution, tested on checkpoints up to 3.5TB, includes:

- Fully sharded reads and writes: Regardless of the sharding strategy used in training, checkpoints are read and written from all nodes. Resharding occurs via a fast InfiniBand network if necessary. More nodes in training result in faster checkpoint operations.

- Asynchronous writing: Copying checkpoints from VRAM to RAM for quick training resumption, then asynchronously writing the state to storage.

- TractoAI storage backend: We use TractoAI as a robust, scalable checkpoint storage, preventing data loss and network bottlenecks on the storage side.

The AI R&D team also worked extensively with file storage and TractoAI teams to address various bottlenecks uncovered during large-scale checkpointing, so that Nebius customers can benefit from our efforts even when relying on their own training infrastructure. Namely:

- Read- and write-scalable file storage with efficient read-ahead. The file storage team has optimized its performance based on AI R&D team’s use case (3.5 TB checkpoint sharded over 128 hosts) — now, the IO speed is top-notch and scales almost linearly with the number of hosts.

- TractoAI as a performant checkpointing backend for tensorstore. Similarly based on an internal use case, the TractoAI team has contributed a robust GRPC backend to tensorstore (pull request to be merged), an open-source tensor IO library that serves as the backbone of Orbax. On top of this backend, the TractoAI team has implemented tensorproxy, a tensorstore to TractoAI API proxy server. A combination of tensorstore improvements and tensorproxy allowed us to benefit from Cypress, the high-performance and distributed TractoAI storage. This setup worked really well for the AI R&D team and now, given its open-source nature, can be reused by other TractoAI users.

### Cluster monitoringCluster monitoring

No hardware system is 100% reliable, and node failures are nominal at large scales. To ensure high training goodput, we’ve implemented a cluster monitoring system featuring:

- Liveness probes: Continuous monitoring of training job progress. Stale processes are automatically restarted from a checkpoint, quickly recovering from hardware failures that cause deadlocks.

- Node health checks: Ongoing GPU and InfiniBand tests to detect hardware and configuration failures. Problematic nodes are cordoned off and reported to the cloud duty team for resolution.

Our monitoring system has helped us uncover a variety of configuration and hardware issues, which our cloud team has resolved to improve our customers’ experience.

We’ve discussed some of the key components and pipelines established by our AI R&D team, such as distributed training and data processing infrastructure, as well as the challenges that go along with it. We will continue dogfooding our infras. For the team members themselves, being in-house allows the closest possible collaboration with architects and platform developers — the factor that contributed massively to building workflows for own LLM advancements. External clients now don’t have to follow the entire path of the AI R&D team: all the infra elements we developed for ourselves along the way are available to every Nebius client. These efforts enable us to build and advance a fully AI-centric cloud platform, with the possibilities described above being a testimonial of that.

## Explore Nebius

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

### 

Slurm vs Kubernetes: Which to choose for model training

Scaling your machine learning workloads will eventually require resource orchestration. This article compares the most popular options today — Slurm and Kubernetes, covering their design origins, ML adaptations and other factors to consider.

May 29, 2024
13 mins to read

### 

Tips and tricks for performing large model checkpointing

There are various aspects to optimize when training large models. It often lasts weeks and involves managing billions of rows of data, with checkpoints of such models weighing terabytes in some cases. Let’s explore how to handle large model checkpointing.

March 11, 2024
9 mins to read

Sign in to save this post
Sign In
