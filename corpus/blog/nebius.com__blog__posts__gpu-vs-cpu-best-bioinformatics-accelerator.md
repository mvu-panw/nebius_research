# GPU vs CPU: what is the best bioinformatics accelerator?

Source: https://nebius.com/blog/posts/gpu-vs-cpu-best-bioinformatics-accelerator

Skip to main content

Computationally intensive tasks enable scientific breakthroughs that change our lives for the better. To help accelerate the most critical stages of analysis and experimentation, we compared cloud GPUs and CPUs’ potential to speed up research workflows.

This article will uncover practical insights and performance benchmarks aimed at accelerating iterative searches, vector embeddings, clustering methods, and functional annotation processes. Join us for a webinar on March 25 where we guide you through the research process and discuss GPU’s potential to accelerate scientific discovery.

Inspired by Nobel Prize-winning research on CRISPR-based bacterial immunity mechanisms, our team leveraged GPU acceleration to explore non-CRISPR archaeal defense systems. Studying archaea, a domain of microbes adapted to extreme conditions, can deepen our understanding of fundamental biological principles central to biotechnology and medicine.

# GPU vs CPUGPU vs CPU

Available on Nebius AI Cloud, NVIDIA H100 GPU’s computational power is frequently praised for speeding up AI model training times. To test its performance for large-scale data analysis and research processes, our team compared it with the 8-core Intel Xeon Platinum 8468 with 16 threads. Both the systems were configured with 196 GB of RAM.

The GPU’s performance was at least twice as fast as its CPU counterpart across the four main tasks comprising this bioinformatics example, demonstrating a particularly efficient performance — 26 times faster than CPU — for ML clustering approaches.

### GPU-accelerated homology searchesGPU-accelerated homology searches

Running homology searches to investigate protein sequence similarity is key to gaining insights on common archaeal defense mechanisms.

From the UniProt database, our team retrieved archaeal proteins related to immune or defense functions and filtered out CRISPR-related proteins. The resulting dataset includes 726 archaeal protein sequences associated with non-CRISPR defense systems.

Optimized to run iterative profile searches in huge sequence sets, our team leveraged MMseqs2's search function to identify protein matches. Our team deployed the model with the support of CUDA architecture 9.0 for an enhanced GPU performance:

cmake -DCMAKE_BUILD_TYPE=RELEASE \
 -DCMAKE_INSTALL_PREFIX=. \
 -DENABLE_CUDA=1 \
 -DCMAKE_CUDA_ARCHITECTURES="90" \
 ..

Activating GPU acceleration was essential to significantly cut down MMseqs2's execution times:

mmseqs search \
 ./mmseqs_db/queryDB/queryDB \
 ./mmseqs_db/targetDB/targetDB_gpu \
 ./mmseqs_results/search_results/resultDB \
 ./mmseqs_results/tmp \
 ... \
 --gpu 1 \ 
 ...

Execution time: 4.3 times faster

 | GPU
 | Approximately 3 minutes

 | CPU
 | Approximately 13 minutes

The model’s sensitivity was adjusted to include distant homologs, expanding the dataset to 6,612 sequences.

### Deep learning-derived protein embeddingsDeep learning-derived protein embeddings

Our team used a deep learning model to generate protein embeddings, transforming each protein sequence into a fixed-length embedding vector.

More specifically, we used the ESM-Cambrian model (ESMC_600M) to generate high-dimensional, context-sensitive protein embeddings that implicitly capture functional and structural properties of proteins, which is essential for grouping proteins according to their biological roles.

Although deep learning models are designed for GPU acceleration, we included a GPU vs CPU comparison as an illustrative example.

Execution time: 17.7 times faster

 | GPU
 | Approximately 3 minutes

 | CPU
 | Approximately 53 minutes

### ML-powered clustering approachesML-powered clustering approaches

To group proteins by function, we clustered the protein embeddings with the K-Means model from the cuML library, using custom wrappers to ensure GPU acceleration.

kmeans_model = cuml.cluster.KMeans(n_clusters=11, random_state=123)
labels_gpu = kmeans_model.fit_predict(embeddings_cp)

Execution time: 2.5 times faster

 | GPU
 | 0.2 second

 | CPU
 | 0.5 second

The GPU system stood out when running a dimensionality reduction operation with UMAP. The task was performed by the NVIDIA H100 26 times faster than its CPU counterpart.

umap_model = cuml.manifold.UMAP(n_components=3, n_neighbors=30, random_state=123)
reduced_gpu = umap_model.fit_transform(embeddings_cp)

Where embeddings_cp is a CuPy array of protein embeddings 

Execution time: 26 times faster

 | GPU
 | Approximately 0.5 second

 | CPU
 | Approximately 13 seconds

### AI-driven functional annotationAI-driven functional annotation

We leveraged DeepSeek-V3, a Large Language Model (LLM) available on Nebius AI Studio API, to interpret the protein clusters by summarizing existing descriptions of their assumed biological roles and properties, a process known as functional annotation.

To ensure a more reliable analysis, we excluded protein sequences labeled as hypothetical, uncharacterized, or of unknown function, resulting in 5,441 annotated sequences. We then deployed DeepSeek-R1 for the final synthesis stage.

Derived from aggregated protein databases, these structured descriptions indicate the best candidates for further research to understand how these proteins boost archaeal immunity beyond CRISPR functions.

# ConclusionConclusion

The GPU system outperformed the CPU setup in all stages of the proposed research workflow, especially in crucial computationally-intensive stages such as iterative searches and vector embeddings. Notably, GPU acceleration was key for dimensionality reduction operations, completing the task up to 26 times faster than with CPU support.

While CPUs are generally quicker at handling fewer, sequential tasks, GPUs are better suited for parallel workloads involving simultaneous operations applied to various data points in large datasets, a great fit for scientific methodologies.

For a guided overview of GPU-enhanced bioinformatics and an in-depth discussion on ML’s practical applications in biotech, join us for a webinar on March 25. We have also compiled a detailed implementation guide on a GitHub repository.

## Explore Nebius AI Cloud

Compute Cloud​
Managed Kubernetes​
Object Storage​
Managed PostgreSQL​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Arseniy Sokolov
Biotech AI Solutions Analyst at Nebius

Contents

- GPU-accelerated homology searches

- Deep learning-derived protein embeddings

- ML-powered clustering approaches

- AI-driven functional annotation

- Conclusion

## See also

### 

Nebius extends immediate access to NVIDIA Hopper GPUs

Striving to simplify the user experience, we increased the amount of compute resources immediately available for every user that signs up to our cloud. You can now access 8 NVIDIA H200 GPUs, 16 NVIDIA H100 GPUs and 2 NVIDIA L40S GPUs via our console and start using them immediately.

February 4, 2025
2 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

How transformers, RNNs and SSMs are more alike than you think

By uncovering surprising links between seemingly unrelated LLM architectures, a way might be paved for effective idea exchange and boosting efficiency.

August 21, 2024
10 mins to read

Sign in to save this post
Sign In
