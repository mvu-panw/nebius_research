# Running StringZilla on GPUs: Accelerating bioinformatics with Unum

Source: https://nebius.com/customer-stories/unum-stringzilla

Skip to main content

## Long story shortLong story short

Boosting biological data processing capabilities is essential to draw breakthrough insights from rapidly growing DNA, RNA, and protein datasets. Powered by Nebius, Unum optimized StringZilla — an open-source, high-speed string processing library — with hardware-specific kernels to efficiently leverage GPU parallelism at the software layer. By streamlining heavy computations, StringZilla enables faster analysis of longer sequences, outperforming standard algorithms for large-scale omics datasets.

Unum designs scalable data processing solutions like StringZilla to help organizations and life sciences teams analyze petabytes of data faster and more efficiently. As a deep-tech research company, Unum advances storage, analytics, search, and AI modeling to enable the next generation of data infrastructure.

## ContentsContents

Beginning

Improvements in sequence alignment

Improvements in rolling fingerprints

How to use StringZilla on Nebius?

The escalating demand for biological data processing is outpacing the growth of transistor density on modern chips. With an unprecedented volume of protein, DNA, and RNA sequence data now being generated, the computational biology software layer requires redesign to leverage parallel hardware architectures like GPUs more effectively. Enabled by Nebius, the Unum team has spent the last year porting StringZilla, a high-speed string processing library, to GPUs. This effort marks the v4 release of the project, extensively detailed in the StringWa.rs benchmarks.

Data source

Those improvements to StringZilla primarily address two types of problems: scoring pairwise sequence alignments and computing fingerprints. Both are critical for navigating vast omics datasets. Fingerprinting powers the “retrieval” phase of searches, while more computationally intensive pairwise scoring is used for “reranking” the retrieved samples.

Both computational tasks are common in pre-clinical drug design and now part of many AI for Biology pipelines, such as the original AlphaFold by DeepMind. This case study will explore how StringZilla performs against other sequence comparison algorithms and a CPU-based rolling hash baseline. We’ll also show you how to get started with StringZilla on Nebius to speed up your own high-performance bioinformatics workloads.

# Improvements in sequence alignmentImprovements in sequence alignment

Sequence alignment and its underlying algorithms are essentially an extension of the traditional computing problem of measuring Levenshtein edit distances between two strings. However, in bioinformatics, several key differences exist:

- Substitution costs may not be uniform, varying for each character pair.

- Scoring can be both global and local, comparing entire strings or only parts of them.

- Gap extension costs may or may not match gap opening costs.

Global alignment scores with equivalent gap opening and extension costs are referred to as Needleman-Wunsch (NW) scores. When"affine” gap costs are used, they are called Needleman-Wunsch-Gotoh (NWG) scores. Similar terminology applies to Smith-Waterman and Smith-Waterman-Gotoh for local alignments. This diversity in the underlying algorithms presents a complex challenge when designing high-performance software for CPUs and GPUs, especially given the historical inaccuracies found in original research papers. StringZilla now provides accurate scoring kernels for all variants of these algorithms across several hardware architectures, including baseline C++ and CUDA code, as well as specialized AVX-512 kernels for modern x86 CPUs and Hopper kernels accelerated with DP4A and DPX instructions. When compared to most CPU-only Python packages for this task, the results are striking:

CUPS is the measure of performance in such dynamic programming algorithms. It stands for Cell Updates Per Second, and the M at the start implies a million.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

As demonstrated, while numerous Python packages implement Levenshtein distance, only a select few — such as StringZilla — can run on GPUs. Furthermore, the charts reveal that StringZilla performs significantly better with longer sequences, a crucial advantage to enable biological data processing at scale.

It is easy to imagine that most general-purpose tools do not offer functionality to handle arbitrary substitution matrices. Our new baseline for comparison is BioPython, which, like most other Python packages listed above, implements all alignment logic in lower-level C language for enhanced performance.

# Improvements in rolling fingerprintsImprovements in rolling fingerprints

Fingerprinting encompasses a much more diverse family of tasks, lacking a clear baseline for comparison despite the existence of libraries like datasketch and scikit-learn. For a simple baseline, a Rust program utilizing traditional 64-bit Rabin-Karp rolling hashes was employed. This quickly demonstrated that even for just 1024-dimensional fingerprints, sustaining 0.5 MB/s of hashing throughput per core is challenging.

# How to use StringZilla on Nebius?How to use StringZilla on Nebius?

Using StringZilla on Nebius is straightforward. Simply spin up a CPU or GPU instance and install one of the following packages, depending on your choice:

bash pip install stringzillas-cpus # for multi-core CPUs 

bash pip install stringzillas-cuda # for CUDA-capable GPUs 

On multi-GPU instances, distribute workloads with the DeviceScope class. The same approach applies when calling from Rust or via the stable C ABI, which makes StringZilla accessible from almost any language.

Unlike BLAST, MMSeq2, and many other bioinformatics tools that can only be invoked from the command line, StringZilla is library-first. It provides well-defined scoring and fingerprinting algorithms that run deterministically on both CPUs and GPUs. The results are guaranteed to match, so a GPU can always be treated as a drop-in accelerator. This makes pipelines more portable, reproducible, and easier to maintain — while still delivering the performance needed for modern AI-for-Biology workloads.

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
