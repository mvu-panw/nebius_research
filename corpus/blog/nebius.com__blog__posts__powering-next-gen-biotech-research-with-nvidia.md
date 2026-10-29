# From genome analysis to quantum chemistry: Nebius powers the next generation of biotech research with NVIDIA

Source: https://nebius.com/blog/posts/powering-next-gen-biotech-research-with-nvidia

Skip to main content

How AI infrastructure is unlocking new frontiers in precision medicine, neuroscience, and drug discovery

Bringing new treatments to patients is one of the most resource-intensive and time-consuming pursuits in science. AI is beginning to shift that equation, enabling researchers to analyze biological data faster, at greater scale, and uncover insights that were previously out of reach.

Nebius and NVIDIA are working together to equip biotech startups with the infrastructure and tools they need to seize this opportunity — from training multimodal models on 36 million single cells to simulating electron behavior for quantum drug design.

At its core, Nebius offers a full-stack AI Cloud built on NVIDIA accelerated computing. It provides scalable access to thousands of NVIDIA GPU instances across Europe and the U.S., with support for both managed Kubernetes clusters and Slurm-based orchestration, tailored to diverse workload requirements. The platform natively supports the NVIDIA AI Enterprise software suite, including NVIDIA BioNeMo for biological modeling and simulation, and NVIDIA Parabricks for genomics.

By removing the operational and financial barriers to AI-scale compute, Nebius and NVIDIA are helping biotech teams focus on what they do best: advancing science.

# Prima Mente: AI-driven neuroscience at the epigenetic frontierPrima Mente: AI-driven neuroscience at the epigenetic frontier

Founded by a global team of neuroscientists and AI researchers out of San Francisco and London, Prima Mente is using 256 NVIDIA H200 GPUs interconnected via NVIDIA Quantum-2 InfiniBand deployed in Nebius to build Pleiades, the first foundation model trained on the chemical language of DNA methylation — a key epigenetic marker with implications for early disease detection and precision therapeutics.

Pleiades comes in 90M, 600M, and 7B parameter variants and was pre-trained on approximately 1.9 trillion tokens of methylation data. The model has demonstrated strong generalization on DNA-based benchmarks while enabling novel diagnostic applications unreachable through DNA-only approaches. It lays the foundation for multi-omic analysis in neurodegenerative diseases, starting with Alzheimer’s.

To support this work, Prima Mente uses Nebius’ Managed Kubernetes clusters and shared distributed file system to spin up dozens of experiments in minutes — all reading and writing to the same datasets. With AI-ready infrastructure and hands-on support, the team can iterate rapidly without bottlenecks.

Prima Mente aims to discover new biology that can help patients with neurological disease. Our approach of combining best-in-class longitudinal datasets with advanced AI approaches allows us to answer questions that have been unanswered in the neurosciences for centuries.

The research advances we make have broad applicability to improve the utility and application of AI methods for real biological value creation. Nebius’ life-sciences-ready platform lets us spin up secure clusters in minutes, compressing model-development cycles and accelerating research outcomes for the development of next-generation precision tools for the detection, management, and ultimately treatment of brain-related diseases worldwide.

Ravi Solanki, CEO and Co-Founder of Prima Mente

# Simulacra AI: Scaling quantum chemistry with foundational modelsSimulacra AI: Scaling quantum chemistry with foundational models

Over in London, Simulacra AI is tackling the notoriously complex challenge of simulating quantum phenomena at the molecular level. The company is building a large wavefunction model (LWM) to predict electron behavior in molecules — work that could accelerate drug and material discovery by improving our understanding of chemical reactivity and molecular structure.

Unlike smaller models that fit on a single GPU, Simulacra AI’s architecture spans hundreds of millions of parameters and relies on single program, multiple data (SPMD) partitioning to distribute workloads across many GPUs. This makes model scaling dependent not just on speed, but on memory architecture and inter-GPU bandwidth — an area where NVIDIA hardware systems and Nebius’ infrastructure are tightly aligned.

With access to 16 NVIDIA H200 GPUs and NVIDIA BioNeMo, Simulacra AI is developing a new class of generative models for chemistry — systems capable of producing synthetic data for training or directly predicting molecular properties at scale.

Simulacra AI is redefining the TechBio industry with its Large Wavefunction Models (LWM). Training these models requires diverse, high-quality datasets that span the entire chemical space while remaining optimized for drug discovery and material design. To generate such datasets, Simulacra AI leverages BioNeMo NIM microservices — such as GenMol and MolMIM — which enable the efficient generation of structurally diverse molecules.

Aleksei Ustimenko, Co-Founder and CEO at Simulacra AI

# Converge Bio: Understanding the cell at full resolutionConverge Bio: Understanding the cell at full resolution

Tel Aviv-based Converge Bio is rethinking precision medicine from the ground up. The company’s flagship model, Converge-SC, is a generative AI system trained to analyze the entire transcriptome — more than 20,000 genes per cell — to detect subtle molecular differences between healthy and diseased cells.

Unlike traditional approaches that reduce expression values to discrete tokens, Converge-SC preserves raw numerical data, allowing for deeper biological interpretation and gene-level attribution. Explainability is also built in, helping researchers understand the “why” behind predictions — including the molecular drivers of disease progression or drug resistance.

This capability is essential for developing treatments tailored to individual disease mechanisms, even when patients carry the same diagnosis — such as specific cancer subtypes or drug-resistant variants.

We are witnessing two waves in personalized medicine. The first wave matched existing drugs to patients using genomics and biomarkers. Now, the second wave is about creating entirely new therapies — tailor-made biologics, gene editors, and RNA-based drugs designed for a single individual.

The promise is extraordinary, but so are the challenges. This level of personalization isn’t scalable without a fundamental shift in how therapies are designed. That’s where generative molecular AI comes in. Unlike traditional AI, generative AI doesn’t just analyze data — it invents. It can propose novel molecules, protein sequences, and genetic edits, all customized to an individual’s unique biology.

Dov Gertz, CEO and Co-Founder of Converge Bio

To build Converge-SC, the team trained on over 36 million single cells and ~2TB of transcriptomic data, processed through a rigorous pipeline addressing batch effects and sequencing noise. This required 7000 NVIDIA H100 GPU hours, which Converge accessed via distributed clusters, NVIDIA CUDA and Nebius AI Studio, all optimized for high-throughput training and minimal infrastructure overhead.

# AI infrastructure for the future of life sciencesAI infrastructure for the future of life sciences

As part of NVIDIA GTC Paris at VivaTech, Nebius has announced deeper integration of the NVIDIA AI Enterprise software suite. This includes NVIDIA BioNeMo, a collection of tools, applications, generative AI solutions, and pre-trained microservices (NVIDIA NIM) designed squarely for the biopharma sector.

BioNeMo enables researchers to generate protein structures, predict molecular interactions, and query biological sequences — accelerating time to insight without the need to build models from scratch. This is especially valuable for startups and labs working with limited compute resources.

Optimized for NVIDIA accelerated computing, BioNeMo NIM also delivers significant performance gains. The AlphaFold 2 NIM, for example, runs up to 2–3x faster than the original, open-source version on equivalent hardware, thanks to enhanced NVIDIA CUDA libraries and parallel processing — making large-scale protein prediction far more efficient.

For both data- and compute-intensive workflows, biotechnology teams may benefit from TractoAI, an in-house solution designed for large-scale data storage, advanced data processing and HPC workloads, including BioNeMo NIM utilization. The platform is already being utilized in drug discovery efforts, including docking campaigns and molecular dynamics simulations.

From transcriptomic modeling to quantum simulation and epigenetics, the collaboration between Nebius and NVIDIA is helping biotech startups unlock scientific breakthroughs with enterprise-grade AI tools, leveling the playing field for lean teams to do world-class work.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Ilya Burkov
Global Head of Life Science and Healthcare Growth at Nebius

Contents

- Prima Mente: AI-driven neuroscience at the epigenetic frontier

- Simulacra AI: Scaling quantum chemistry with foundational models

- Converge Bio: Understanding the cell at full resolution

- AI infrastructure for the future of life sciences

## See also

### 

GPU vs CPU: what is the best bioinformatics accelerator?

Speeding up computational tasks is critical to push the boundaries of science and ensure scalability and efficiency. Check out how NVIDIA Hopper GPUs available on Nebius AI Cloud performed against CPU workflows to accelerate homology research, deep learning-enabled protein embeddings and ML clustering.

March 24, 2025
6 mins to read

### 

Supercharging startups: Nebius accelerates AI-native innovation with NVIDIA

Nebius AI Cloud is collaborating with NVIDIA Inception, a leading program for AI startups with over 22,000 members, to accelerate AI startup innovation. Nebius’ AI Lift program — announced at NVIDIA GTC 2025 — offers eligible NVIDIA Inception members up to $150,000 in cloud credits, access to AI technical expertise and support and a range of other exclusive benefits.

April 9, 2025
3 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
