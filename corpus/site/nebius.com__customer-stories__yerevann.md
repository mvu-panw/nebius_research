# YerevaNN: LLMs for molecular optimization

Source: https://nebius.com/customer-stories/yerevann

Skip to main content

## PremisePremise

Recent advancements in LLMs have opened new possibilities for generative molecular drug design. Researchers from YerevaNN and Yerevan State University present three Nebius-based models, continuously pre-trained on a novel corpus of 110M molecules with computed properties, totaling 40B tokens. A genetic algorithm integrates the models to optimize molecules with promising properties.

YerevaNN is a non-profit research center dedicated to advancing the field of machine learning through innovative research and development initiatives in Yerevan, Armenia. Founded in 2016, the laboratory builds scalable AI models for new biotech modalities, including molecules, multispectral imagery and radar data.

## ContentsContents

Flash Attention, compute capability and custom Torch extensions

Environment management

Fully sharded data parallel training

Optimizing simple DataLoaders for text

Leveraging CPU compute for traditional optimization workloads: docking

Moving data

YerevaNN is transforming generative molecular drug design with LLMs. To expedite implementation, the research center leveraged Flash Attention 2 to speed up computation, FSDP model sharding to reduce memory requirements and post-backward prefetch to decrease communication overhead while maintaining training speed. YerevaNN also maximized parallelism throughout ranks, DataLoader workers and CPU-intensive workloads.

By maximizing training efficiency, YerevaNN accelerated tokenization and docking runs for molecular modeling, improving performance by 8% over previous methods. The processing rates of Nebius-based models reached 180,000 words per second.

 | Words per Second
 | Setup

 | 140 000
 | batch size =1

 | 180 000
 | batch size =4

## Flash Attention, compute capability and custom Torch extensions

## What is Flash Attention?What is Flash Attention?

Flash Attention and Flash Attention 2 are low-level, hardware-optimized implementations of the attention mechanism to decrease memory requirements and speed up computation. In flash attention, this is achieved by reducing the number of read and write operations between different levels of memory hierarchy, since the primary bottleneck in computing attention is memory bandwidth and not compute capacity. Flash attention 2 further increases efficiency by parallelizing workloads across sequence length, minimizing shared memory access within a single attention block and reducing the number of non-matmul FLOPs.

## Custom Torch extensionsCustom Torch extensions

Since flash attention is distributed as a Python package and a Torch extension, it needs to be built against the currently installed PyTorch and CUDA versions. This is why flash attention is installed with the pip install flash-attn --no-build-isolation command, where the --no-build-isolation flag indicates to pip that the package and subsequent extension building should not be set up in an isolated environment.

As a result, the package correctly compiles against the currently installed version of the CUDA toolkit, with access to the necessary environment variables and CUDA headers to interface with the CPP libraries in use. This process differs from most pip packages, which have little to no dependencies on CPP libraries, system installs or path variables.

## Compute capabilityCompute capability

Another critical factor to make the most of flash attention is the hardware-specific CUDA compute capability. This is sometimes referred to as the SM version, indicating the Streaming Multiprocessor architecture that communicates the instructions and features available to applications at runtime.

This is important for both Flash Attention and mixed precision, since hardware with compute capability less than 7 (corresponding to the Ampere architecture) does not support the required fp16 or bf16. To maximize the benefits of the latest architectural improvements, the training runtime must have a correct understanding of the machine’s compute capability. The next section will compare different methods of portable environment management.

## Environment management

## CondaConda

For reproducibility and ease of use, Conda is a suitable package manager that integrates well with pip, carries packages not available via PyPI and, more specifically, allows for the installation of the CUDA toolkit. More recently, Conda supports the installation of CUDA software bundles within virtual environments.

Upon installation, Conda will correctly set the relevant CUDA-related environment variables needed for PyTorch and compile CUDA extensions like Flash Attention. A common practical challenge in Conda environments is quickly porting them to other machines with consistent behavior.

### Environment filesEnvironment files

Among Conda’s environment porting utilities, conda env export > environment.yml is the most common one, able to provide package-specific version numbers for pip- and Conda-managed packages. Despite being cross-platform, these files don’t contain build-specific information and are not guaranteed to reconstruct an identical Conda environment on another machine. Portability can also take longer if the specified packages are not already stored on disk.

A more thorough alternative is to run conda list --explicit > environment.yml, which links to specific tarballs for package installation. This approach, however, results in less readable files and does not support cross-platform environment generation. Although the explicit environment files solve some of the issues related to regular Conda environment specification, rebuilding a setup from an explicit environment file takes time. Most critically, this method does not allow specifying the package installation sequence.

### Conda-PackConda-Pack

Conda-Pack is a third-party utility that allows users to take an existing Conda environment on a source machine and package it into a tar archive. On a target machine with the same platform and hardware architecture, the user can simply extract the archive file and activate an identical Conda environment without having to rebuild it by downloading and installing packages. Furthermore, Conda-Pack facilitates flash attention compilation by solving installation order issues, pre-arranging the necessary CUDA, PyTorch and packaging dependencies.

To achieve 30% faster environment porting times, YerevaNN chose Conda-Pack to package Conda environments for training on local machines and simply decompress them on the Nebius H100 systems for use. In this particular case, CUDA, PyTorch and Flash Attention must be recompiled on H100 systems for compatibility with compute capability 9.X features. Besides using Conda-Pack, the CUDA, PyTorch and Flash Attention packages were reinstalled to maintain consistency and leverage the H100’s 9.X compute capability.

## Environment porting timesEnvironment porting times

 | Conda-Pack
 | Installing from the Env File

 | 135 seconds
 | 195 seconds

## Fully sharded data parallel training

## What is FSDPWhat is FSDP

Fully Sharded Data Parallel Training (FSDP) is a PyTorch-native model for architecture implementation that allows for model sharding and partitioning of optimizer parameters and gradients. In contrast to DP and DDP, which require that each NVIDIA GPU maintains a complete copy of model parameters, optimizer states and gradients, FSDP’s model sharding affords users additional memory during training for larger batch sizes at the cost of additional communication overhead through NCCL.

FSDP functions by first organizing model and optimizer parameters into modules split across NVIDIA GPUs consisting of at least one model layer. Precisely when it is time for a module to perform a forward or backward pass, the state from the other ranks is collected, the pass is computed, and all components are resharded again. To rapidly shard and reconstruct each module’s full layer, the communication can be configured to coincide with other compute operations. Module selection can also be manually or automatically configured. These elements will be further detailed below.

## FSDP units: memory savings and weight sharingFSDP units: memory savings and weight sharing

Considering FSDP units are the smallest level of organization gathered and reconstructed during backwards and forward passes for computation, manual or automatic configuration can have a meaningful impact on both training throughput and correctness.

Throughout the process, the primary tradeoff in FSDP module selection is between communication overhead and the number of layers simultaneously residing on GPUs when performing computation. Including more layers in a single FSDP module will require additional memory as the reconstructed unit will be larger, but the communication between graphics processing units will be less frequent. On the other hand, while a lighter module configuration demands less memory, communication will occur more often, since each layer will need to be sharded and reconstructed independently during a pass.

Weight sharing is another critical constraint on FSDP module configuration. Since FSDP has no built-in mechanism to manage shared weight parameters, weight-sharing layers must be placed on the same FSDP unit for coordinated reconstruction and gradient updates. Otherwise, the same parameters will have redundant gradient updates across units. For transformer models, modules that should be placed in the same FSDP instance are specified in the implementation as _no_split_modules. This step ensures the library’s auto-wrap policy groups all weights within specified modules in the same FSDP unit when wrapping layers.

## Backward and forward prefetchBackward and forward prefetch

To reduce the communication overhead when reconstructing FSDP units before computation, each unit can be prefetched during the preceding execution. This can be achieved via two methods.

The first option, BACKWARD_PRE, fetches the next unit when the current one starts the gradients calculation. This approach requires the most memory.

Another option for reduced memory usage is BACKWARD_POST, which sequences the prefetching operation after the gradients computation. At this point, the current unit’s parameters are sharded between GPUs, so that only its gradients are kept in memory alongside the subsequent unit’s parameters. This approach partially decreases overlap and, consequently, training speed.

If prefetching is disabled altogether, the next unit reconstruction does not start until after the current unit’s parameters and gradients have been sharded, slowing down training speed significantly. For a more balanced performance, YerevaNN opts for BACKWARD_POST to fit a desirable batch size while preserving high training speed.

## Limitations to be avoidedLimitations to be avoided

During FSDP implementation, YerevaNN encountered limitations that caused silent failures or lacked support, functioning only in specific cases. Unless these issues are specifically addressed with better integration, benefit validation and functionality corrections, the following methods pose a risk if integrated with FSDP.

### CPU offloadingCPU offloading

Since the sharded FSDP units remain idle until their turn to be reconstructed for computation, storing them in system memory seems like the logical choice for increased memory savings at the cost of additional IO operations between the two. While in principle this approach should decrease memory usage, in practice, CPU offloading can lead to errors with partially frozen models, as reported on GitHub.

### Torch CompileTorch Compile

Sharded model compilation is an active work in progress at PyTorch, which announced support for the use of FSDP and Torch Compile in May 2024. While enabling Torch Compile and FSDP may not raise errors, the approach is still prone to failure.

Support for graph breaks in compiled models is not available either, and there are currently no plans for it to be provided. As discussed in a PyTorch developers forum, action must be taken to avoid unsupported numpy operations and data types or print statements.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Optimizing simple DataLoaders for text

## Functionality criteriaFunctionality criteria

For smoother implementation, it’s important to specify the relevant criteria for the intended DataLoader functionality. YerevaNN boiled it down to 3 key requirements:

- 

No offline pre-processing, ensuring all data transformation co-occurs with the training process. Eliminating intermediate data representations accelerates training startup, prevents the need for cache regeneration for ablation studies, avoids NCCL timeout errors and reduces load on disk storage capacity.

- 

Immediate training pickup from checkpoints. The ability to describe and save DataLoader states during training allows operations to be resumed seamlessly during checkpoint load.

- 

Sufficient parallelization and speed, preventing training bottlenecks due to feature implementation costs.

## Parallelizing DataLoadersParallelizing DataLoaders

### Rank parallelismRank parallelism

As model training will leverage multiple devices, each rank will have a main process to perform data pre-processing operations. As there are eight chips in a node, at least eight processes will perform data transformations in a single-threaded manner.

### DataLoader workersDataLoader workers

To further increase parallelism, the main processes of each rank can be leveraged to manage a large number of CPU-only processes dedicated to data preparation. If this feature is disabled, all data will be handled on the main processes, delaying execution instructions from being sent. Assigning one additional process for data loading removes this bottleneck and greatly increases throughput.

### Tokenizer parallelismTokenizer parallelism

One of the most computationally intensive operations in text preprocessing for language model training is text tokenization, converting substrings into model vocabulary indices. HuggingFace’s tokenizers library supports a lower level of parallelism for the simultaneous tokenization of multiple texts passed into the tokenizing function in a batch.

### YerevaNN’s ConfigurationYerevaNN’s Configuration

YerevaNN leveraged rank parallelism to make the most of the eight available nodes. This approach avoids training loop problems related to workload asymmetries caused when all computational load is concentrated on a single accelerator.

Using a single DataLoader worker allowed YerevaNN to avoid data pre-processing from being carried out on the main processes, preventing training delays. With this setup, the researchers were also able to verify in advance whether the code was sufficiently optimized for one additional CPU process to generate a mini-batch without negative effects on training throughput. Finally, tokenizer parallelism allowed the DataLoader worker to leverage multiple threads.

## Iterable datasets, line by lineIterable datasets, line by line

When distributing workloads across ranks, it’s essential to assign similar volumes to different units to avoid process desynchronization and prevent potential errors, freezes and NCCL timeouts. An easy and readable solution involves sending all lines within each file to the same graphics processing unit, provided that the same data is not accessed by several of them and no data is skipped over.

This approach works for a flexible number of files with different sizes and quantities of lines. It also generates a known and well-defined mapping of sample line numbers and the corresponding NVIDIA GPU it was processed on, improving observability and facilitating debugging. Moreover, this method eliminates internal communication for data pre-processing, since each rank reads a file line and handles all necessary data transformation beforehand.

## Resuming trainingResuming training

In practical machine learning applications, it’s often necessary to stop and resume training from prior runs to handle bugs, problematic batches or hardware errors. For results to be nearly identical to uninterrupted training runs, both low-level and more abstracted machine learning frameworks can handle saving and loading a model along with optimizer states. For this approach to be successful, the DataLoader must be able to reproduce the sequence of batches that would have been given to the model had the training not been stopped.

YerevaNN’s solution to this challenge involved a mapping between file paths and byte offsets after every line. To ensure the DataLoader state was always up to date, this mapping was saved to a file during checkpoints. When loading, training was resumed by seeking the byte offset stored in the mapping. As opposed to the HuggingFace implementation, which requires a full traversal through the iterable dataset up until the same step is reached, YerevaNN’s approach is much faster, since the single seek call for each file is independent from the amount of previously computed data.

## Leveraging CPU compute for traditional optimization workloads: docking

## Advantages of CPU workloadsAdvantages of CPU workloads

YerevaNN’s efficient and compact DataLoader implementation ensures text-based model training requires lower CPU usage on an H100 system, since text data transformation is relatively lightweight compared to other data modalities. In this case, training used 16 out of 156 CPU cores, saturating all eight accelerators on a node. This setup leaves plenty of room for additional CPU-only workloads to run simultaneously to take full advantage of HPC-grade hardware.

## Parallelizing dockingParallelizing docking

In molecular modeling, docking is a CPU-intensive workload that simulates the binding interaction of a molecule to a protein to evaluate its potential as an effective drug. This method consists of sampling different molecular conformations to evaluate the strength of attraction between molecules and protein structures. In practice, docking involves the calculation of multi-dimensional molecular properties, evaluating resultant scores of molecular conformations and the execution of traditional search algorithms.

Docking methods often support low-level multiprocessing for a single molecule-protein pair, which can be further parallelized by running docking for a collection of molecules. YerevaNN implemented both levels of parallelism to significantly expedite docking runs across thousands of molecules. The runtime of 5000 docking results decreased from approximately 48 hours to just 4 hours when parallelized across 128 CPU cores, where 8 cores were leveraged for per-molecule parallelization.

## Serving via APIServing via API

Since Nebius servers are available out of the box, directly in the cloud, it’s easy to implement the basic API endpoints required for training. This solution is especially beneficial when compute is required concomitantly with CPU-intensive workloads.

This API approach is also helpful in cases when only a sample of local data is required for computation, or when multiple cloud systems, local or external, need access to computation results. Implementing a simple API access point to enable docking computations on the Nebius system allowed YerevaNN to fully leverage Nebius compute while using CPUs for docking and routing results to local servers.

## Moving data

YerevaNN privileged faster data transfer methods for a more efficient use of cloud hardware, considering access is time-contingent and data availability is essential for effective compute utilization.

When transferring data from local storage, rsync -avz --partial --progress rdkit_computed_rel+form/ [admin@](<mailto:admin@195.242.16.19>)<server-url>:/home/admin/ changed directory permissions and impeded the connection to the server via SSH. In case this error occurs, troubleshooting is possible by checking SSH logs in the /var/logs/auth.log file.

Moreover, YerevaNN preferred SCP over rsync to avoid additional checks and overhead, since there was no need for rsync’s more sophisticated features such as incremental file transfer, synchronization or symlink handling.

YerevaNN found scp -C to be twice as fast as scp, since data is compressed and decompressed at, respectively, the input and output streams. Since this approach reduces the network bandwidth utilization of a single stream, it enhances parallelism by simultaneously moving all necessary files in separate streams, where each process is responsible for the compression of a single file. On the target machine, a separate process is spawned to decompress each incoming file. This parallel implementation of scp brought 200 MB/s vs. 10 MB/s of rsync -avz in terms of raw data transferred.

## More exciting stories

## 

vLLM

Using Nebius’ infrastructure, vLLM — a leading open-source LLM inference framework — is testing and optimizing their inference capabilities in different conditions, enabling high-performance, low-cost model serving in production environments.
Read the story

## 

SGLang

SGLang, a pioneering LLM inference framework, teamed up with Nebius AI Cloud to supercharge DeepSeek R1’s performance for real-world use. The SGLang team achieved a 2× boost in throughput and markedly lower latency on one node.
Read the story

## 

London Institute for Mathematical Sciences

How well can LLMs abstract problem-solving rules and how to test such ability? Research by the London Institute for Mathematical Sciences, conducted using our infrastructure, helps to understand the causes of LLM imperfections.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
