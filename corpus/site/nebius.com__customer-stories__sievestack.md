# SieveStack: advancing drug discovery with molecular simulations

Source: https://nebius.com/customer-stories/sievestack

Skip to main content

## PremisePremise

SieveStack is building the world’s largest dataset of molecular simulations to train foundational models for AI-enhanced drug discovery. Powered by Nebius and TractoAI infrastructure, SieveStack can scale high-precision data generation, a significant advantage for training a multi-layer foundational model stack that yields progressively more nuanced insights into drug interactions with the human body.

Specializing in molecular dynamics, SieveStack reveals insights beyond the reach of static methods or lab experiments to develop new medicines for hard-to-treat conditions. Founded by former researchers from Stanford and UCSF Labs, SieveStack fills a critical gap in drug discovery: leveraging AI and big data for faster development.

## ContentsContents

Data generation: molecular dynamics

Maximizing model training efficiency

Custom AI workflows with TractoAI

Multi-layer stack of foundational models

Next steps

SieveStack is tapping into AI capabilities to fast-track drug discovery beyond the reach of traditional research methods. With firsthand experience of how slowly academia can adapt to new technologies, the founding team created SieveStack to bridge that gap and enable strategic collaborations to accelerate scientific innovation.

Powered by Nebius cloud-native infrastructure, SieveStack scales the generation and utilization of high-fidelity molecular simulations to uncover new drug-target interactions beyond the reach of laboratory experimental methods. This comes down to two core uses of cloud infrastructure:

- 

Generating high-fidelity synthetic data through molecular dynamics simulations, such as molecular modeling and dynamics.

- 

Training large foundational models on the generated data to help solve crucial drug discovery problems, maintaining over 90% GPU usage with parallelization strategies and TractoAI-driven orchestration.

## Optimizing ML workloads for a competitive edgeOptimizing ML workloads for a competitive edge

Partnering with a responsive, AI-focused cloud infrastructure provider was key for SieveStack to establish a faster, more iterative process, cutting delays between test runs and production by 30-50%, accelerating training by up to four times and speeding up pipeline development for state-of-the-art models.

Relying on TractoAI’s unified compute platform, paired with Nebius support team’s strong understanding of life sciences workflows, it was easier for SieveStack to scale molecular simulations while focusing on innovation.

This case study showcases how SieveStack approached high-fidelity molecular data generation, maximized GPU utilization with a mixed-precision training strategy and built a layered foundational model architecture for progressively deeper insight to boost drug discovery breakthroughs. You’ll also get a glimpse of their orchestration setup and how they turned cloud infrastructure into a significant competitive advantage.

## Data generation: molecular dynamics

The dynamic nature of molecular simulations is the special ingredient in SieveStack’s strategy to push the boundaries of drug discovery. Unlike traditional methods reliant on static snapshots, SieveStack specialises in physics-based modeling and biochemistry to capture compound interactions over time.

Building the world’s largest dataset of hard-to-generate synthetic data, particularly expensive molecular dynamics simulations, is a critical step to train foundational models for AI-powered breakthroughs. However, the continuous nature of simulations poses a challenge for parallelizing workflows. Here’s how SieveStack maximized GPU utilization for data generation.

## Molecular modeling with OpenMMMolecular modeling with OpenMM

For molecular modeling, SieveStack relies on OpenMM, a state-of-the-art engine that simulates atomic interactions over time. To achieve over 90% GPU utilization in this computationally intensive task, the company leverages the NVIDIA Multi-Process Service (MPS) to run multiple OpenMM simulations on a single GPU, boosting total throughput by 15-25%. This alternative implementation of the CUDA API ensures no resources are underutilized, a parallelism technique especially relevant for smaller systems. To ensure numerical stability and accuracy in atomistic calculations, all simulations are performed in FP32 precision, with typical VRAM usage of 1–2 GB per job.

Preventing I/O bottlenecks is another crucial objective in SieveStack’s GPU-heavy workflows. For optimized data pipelines, SieveStack uses memory-mapped storage and asynchronous writes so data movement does not become a limiting factor.

Profiling workflows before scaling helps ensure GPU efficiency remains consistent in production environments. Tools like NVIDIA System Management Interface (nvidia-smi), OpenMM’s built-in reporters and NVIDIA Nsight Systems are essential to monitor GPU occupancy, memory throughput and kernel efficiency.

## Data preprocessing for quality assuranceData preprocessing for quality assurance

SieveStack’s workflow highlights the critical role of input data preprocessing for model accuracy, especially considering the intricate nature of chemistry and protein targets.

To ensure input data quality, the company matches synthetic data with existing experimental lab results from literature using public benchmarks. Rather than relying blindly on academic datasets — which, as they have found, might contain flaws — SieveStack performs their own rigorous preprocessing and quality checks, ensuring consistency and trustworthiness.

## Maximizing model training efficiency

Relying on PyTorch to run model training on NVIDIA H100 GPUs, SieveStack deploys a precision-aware, hardware-optimized strategy to keep compute utilization above 90% and accelerate throughput.

To eliminate I/O stalls and keep the GPUs saturated with data, SieveStack configures PyTorch’s DataLoader with pinned memory, asynchronous prefetching and a high number of workers. This approach makes the most of the NVIDIA H100 GPUs' high memory bandwidth (3.35 TB/s) and large VRAM (80 GB), allowing for increased batch sizes that optimize throughput.

SieveStack relies on mixed-precision training to reduce memory usage by 50% and speed up training by 2 to 4 times without compromising model quality.

- 

They deploy PyTorch’s Automatic Mixed Precision (AMP) to dynamically apply FP8, FP16 and BF16 for most computations, improving performance on transformer and large-scale architectures and securing a 4-9x workload speedup compared to NVIDIA A100 GPUs.

- 

For critical steps like loss computation and weight updates, SieveStack maintains FP32 precision to ensure numerical stability and accuracy. This balance is managed automatically by AMP’s autocast and GradScaler.

- 

Before deploying to production, SieveStack uses PyTorch Profiler and NVIDIA Nsight to identify and address kernel inefficiencies, memory bottlenecks and compute stalls.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Custom AI workflows with TractoAI

TractoAI is SieveStack’s orchestrator tool of choice to deploy applications for data generation and model training. Compared to traditional ML setups relying on fragmented pipelines, SieveStack’s tightly integrated workflows streamline iteration and accelerate the transition from prototype to production by 30-50%.

- 

Jupyter notebooks are the central interface for molecular modeling, data generation and training. SieveStack runs them directly on GPU-backed infrastructure with custom Docker kernels to enable end-to-end workflows — simulation, data preparation, validation and distributed training — without context switching or managing backend systems.

- 

Using Tractorun, TractoAI’s job launcher, SieveStack sends large-scale, multi-GPU training and inference jobs to production directly from the same notebook environment. Tractorun handles scheduling, autoscaling and recovery without requiring Kubernetes or Slurm.

- 

More efficient than disk-based solutions, a performance-optimized storage architecture is critical for SieveStack to achieve 2-3x faster training and development cycles.

- 

Tracto supports structured, columnar and in-memory formats, speeding up parallel reads and writes and enabling direct querying via SQL-like language. By writing output directly to Tracto, SieveStack can filter, aggregate and sample terabyte-scale datasets in seconds. Streamlining outputs from simulation jobs into a training-ready format is essential to avoid costly serialization steps and accelerate data preparation and model evaluation.

## Multi-layer stack of foundational models

SieveStack’s foundational models combine the scalability of ML with the precision of physics-based simulation to uncover new mechanisms of drug-target molecular interaction. Each layer of the stack builds on the outputs of the previous one to provide increasingly detailed insights on candidate drugs, moving from broad exploration to atomistic precision.

While SieveStack’s models already perform well in predicting dynamic drug-target interactions, collaborating with the Nebius’ life sciences team enabled the company to scale high-fidelity synthetic data generation and consistently improve model accuracy. Leveraging Nebius AI-native infrastructure, SieveStack’s model stack runs molecular dynamics at scale to reveal atomic-level motions and unlock insights that cannot be observed experimentally, securing a competitive edge.

## Graph Neural Network (GNN) architectureGraph Neural Network (GNN) architecture

By identifying molecules with similar interaction profiles, SieveStack’s foundational pilot model helps find more suitable drug candidates, for instance, compounds with fewer side effects than a known medicine. Built on a Graph Neural Network (GNN) architecture, the model replicates the natural structure of small molecules.

The model architecture features convolutional layers with attention mechanisms to help uncover key chemical relationships, paired with per-graph normalization and skip connections for stability. This configuration allows the model to aggregate features into a single vector representation to learn and predict interaction properties.

## Trained on 150 million datapointsTrained on 150 million datapoints

To train its first foundational pilot model, SieveStack leveraged TractoAI infrastructure to generate over 3 million molecular snapshots of drug-target interactions in under two weeks, including simulation and engineering time. Spanning across oncology, immunology and neurology complexes, each snapshot encodes 3D spatial and biochemical interaction data.

From this initial dataset of drug-target bindings, SieveStack selected compounds with similar interaction properties to build a training dataset of over 5 million molecular pairs associated with 29 targets with various structures and functions, resulting in over 150 million structure-informed datapoints.

## Model validation and success metricsModel validation and success metrics

The model’s accuracy, generalizability and fidelity are assessed against well-established benchmark datasets like LIT-PCBA and DUDE-Z, with SieveStack’s foundational models outperforming traditional ligand-based and structure-based methods.

To measure discovery impact, SieveStack applies its models to high-complexity tasks, such as predicting the results of expensive molecular dynamics simulations or identifying new compounds that share similar binding interactions with a disease target — an exceptional challenge when analogous compounds have different chemical structures.

## Next steps

SieveStack plans to scale both the training data and model capacity by integrating a greater range of synthetic inputs and increasing the volume of molecular dynamics simulations to expand the pipeline. This strategy aims to improve generalization across disease targets and enhance accuracy in drug discovery applications.

Identifying cryptic pockets and allosteric modulations are two crucial drug design tasks and key next objectives for new foundational models trained on dynamic simulations, a particularly suitable data type for tackling this challenge.

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
