# Kvax: Fast and easy-to-use Flash Attention implementation for JAX

Source: https://nebius.com/blog/posts/kvax-open-source-flash-attention-for-jax

Skip to main content

# Video from ICLR 2025Video from ICLR 2025

You can read the post below and/or watch an ICLR 2025 talk about Kvax by our senior engineer Sergei Skvortsov, its main author:

# IntroIntro

### Long-context training for AI agentsLong-context training for AI agents

At Nebius, we conduct research across a wide range of AI-related topics. One recent area of our interest is learning and planning for LLM-based software engineering agents. We recently shared our findings on how test-time search can improve these agents, as well as datasets designed to facilitate training of such systems. To conduct agent-related research, we rely on robust infrastructure and a high-performance training framework that lets us test our hypotheses quickly and efficiently. A specific challenge in agent-based learning that our training infrastructure addresses via a custom Flash Attention implementation is training on long token sequences. Today, we’re excited to share this component of our training framework with the community!

In agent-based systems, long contexts are essential for enabling models to consider all previous steps in the decision-making process. Training LLMs in a multi-GPU setup is a challenging task, especially for long contexts, as it requires addressing several engineering challenges, including optimizing sharding, identifying and eliminating bottlenecks, and minimizing computational waste. As discussed in our earlier blog post, our training framework is built on the JAX framework, which relies on the XLA compiler. This setup limits our ability to use dynamic shapes at runtime, leaving us with two possible approaches when training data sequences are shorter than the maximum context length:

- 

Padding the data to match the maximum batch sequence length.

- 

Packing multiple data sequences into a single batch sequence, a technique known as dense packing. Since some sequences can be very long, a large sequence length is necessary to avoid truncation. However, sequences vary in length, and on average, multiple shorter sequences can be efficiently packed within a single batch sequence.

The first approach leads to inefficient use of computational resources, as padding tokens consume the same amount of compute as meaningful tokens while having no effect on gradients. Although various techniques like sparse computations address this issue, they are often difficult to implement and introduce additional overhead. In training scenarios involving very long contexts, padding tokens can quickly outnumber useful tokens, significantly wasting GPU compute and memory.

The second approach, dense packing, fills each batch sequence with multiple shorter data sequences that are processed together, substantially reducing compute waste and boosting performance. However, dense packing requires a specialised mask, known as a document mask, to ensure tokens from different data sequences do not attend to each other. The simplest implementation of this mask involves dynamically computing it using an auxiliary tensor containing segment ids.

Although Kvax supports efficient computation of the attention operation with both methods, we primarily focus on optimising the second approach, as it is more challenging to implement but delivers better utilization of compute resources.

### Optimising attention with Flash AttentionOptimising attention with Flash Attention

The attention operation has quadratic time and memory complexity, making it increasingly costly as sequence length grows. Numerous solutions have been proposed, but the most impactful and widely adopted has been Flash Attention. Introduced in 2023, Flash Attention significantly improved the efficiency of attention computation.

The core idea behind Flash Attention is to compute attention blockwise within a single fused CUDA kernel, eliminating the need to store the entire seq_len × seq_len attention weight matrix in GPU memory during the forward pass. Flash Attention employs tiling to make the algorithm I/O-aware, reducing the number of read and write operations across different GPU memory levels. These optimizations greatly accelerate attention computations while substantially reducing GPU memory usage. Flash Attention has since become a critical algorithm for large language models, enabling significant increases in context length.

Flash Attention has evolved through three versions, each introducing optimizations for efficiency and performance. Our implementation builds upon Flash Attention 2, which improved memory efficiency and parallelism compared to the first version. Flash Attention 3 includes more advanced hardware-based optimizations for the Hopper GPU architecture, although not all these features are currently supported in the Triton language, ​​which we use to build our implementation.

The original Flash Attention paper also introduced an optimisation for computing causal masks, known as Block-Sparse Flash Attention. In this approach, blocks of the attention weight matrix containing only zero values are skipped, further enhancing efficiency. Today, this technique is widely recognised as the standard for attention implementations and is commonly used across the industry.

Example of a blockwise calculated attention matrix with seq_len = 20 and block_size = 5, with a causal mask

### Ways to improve performance of Flash Attention. Document maskWays to improve performance of Flash Attention. Document mask

As mentioned earlier, during dense packing, an additional document mask must be applied to the attention weight matrix to prevent tokens from different data sequences from attending to each other. There are blocks in the attention matrix that contain only zeros and can be skipped, following the approach from Block-Sparse Flash Attention. The positions of these blocks depend on the data and need to be calculated at runtime. Skipping these blocks saves computational resources and significantly speeds up the attention operation, especially when multiple data sequences are packed into a single batch sequence.

Example of a blockwise calculated attention matrix with seq_len = 20 and block_size = 5, with document and causal masks

The idea behind block-sparse computation of the document mask is quite simple: it takes fewer computational resources to calculate attention separately for each data sequence than for the entire batch sequence at once. Given attention’s quadratic time complexity, we can express this mathematically: the square of the batch sequence length (lll) is always greater than or equal to the sum of squares of the lengths of individual data sequences (lil_ili​):

l2=(∑i=1nli)2=∑i=1nli2+2∑1≤i<j≤nlilj≥∑i=1nli2l^2=\bigg( \sum_{i=1}^{n} l_i \bigg) ^2 = \sum_{i=1}^{n}l_i^2 + 2 \sum_{1\leq i < j\leq n} l_i l_j \geq \sum_{i=1}^{n} l_i^2l2=(i=1∑n​li​)2=i=1∑n​li2​+21≤i<j≤n∑​li​lj​≥i=1∑n​li2​

Leveraging this fact, Kvax precomputes document mask blocks based on segment indices using a high-performance Triton kernel, achieving both high speed and reduced GPU memory consumption.

### Parallelism techniques of attention operationParallelism techniques of attention operation

Different techniques enable sharding of the attention operation across multiple GPUs, significantly improving performance and reducing GPU memory consumption. One such technique is tensor parallelism, where the attention operation is sharded across GPUs along the axis of attention heads, as each head can be computed independently. While this method effectively reduces the computational load per GPU, it has limitations, such as the number of attention heads potentially being smaller than the number of GPUs, as well as communication overhead.

Another effective way to enhance performance and reduce GPU memory consumption when training LLMs with long sequences is distributing the input sequence across multiple GPUs in chunks. This technique, known as context parallelism, reduces the sequence length processed by each GPU. While most operations in the transformer architecture are pointwise and can be processed independently across sequence chunks, the attention operation requires access to the full sequence to compute results. Several methods exist for implementing context parallelism in attention operations, including Ring Attention and an all-gather–based approach, described in the Llama 3 training paper.

In Ring Attention, the query, key and value tensors are initially split into chunks, each assigned to a different GPU. During execution, each GPU computes attention results for its local query chunk while exchanging key and value tensor chunks with other GPUs in a ring-like fashion. This iterative exchange enables attention computation across the entire batch sequence. Communication overhead is minimised by overlapping data transfers with computation, ensuring minimal impact on performance.

Block-by-block computation of Ring Attention. Source

In the all-gather–based approach, the query, key and value tensors are also split across GPUs. However, before computing attention, an all-gather operation is performed on the key and value tensors, ensuring that each GPU has a full copy of these tensors. This introduces an additional communication step before computation begins, but its impact on performance is minimal due to the Grouped Query Attention (GQA) technique, which keeps tensor sizes small. This method is particularly effective for handling document masks.

Kvax supports both tensor parallelism and the all-gather–based approach for context parallelism.

# Technical details of Kvax implementationTechnical details of Kvax implementation

Kvax is implemented using the Triton kernel language. It builds upon the Fused Attention module in the Triton library, incorporating several modifications and additional features to enhance performance and flexibility.

### Computation of document maskComputation of document mask

Kvax supports two types of attention masks: positional masks and document (or segment) masks.

- 

The positional mask is computed using the query_positions and kv_positions tensors to prevent tokens from attending to future tokens. Also known as a causal mask, it is defined as query_positions≥kv_positionsquery\_positions \geq kv\_positionsquery_positions≥kv_positions.

- 

The document mask is built using the query_segment_ids and kv_segment_ids tensors to prevent tokens from different data sequences from attending to each other. It is defined as query_segment_ids==kv_segment_idsquery\_segment\_ids == kv\_segment\_idsquery_segment_ids==kv_segment_ids.

Both masks are computed by a high-performance Triton kernel called within the create_attention_mask function. This kernel calculates the mask blockwise using only position and segment indices, eliminating the need to construct a full batch_size × seq_len × seq_len tensor. This approach enables efficient attention mask computation with minimal GPU memory usage.

Additionally, this method allows Kvax to support other mask types, such as sliding window masks, although these are not yet implemented. For a complete list of unsupported features, refer to the Limitations section of the Kvax readme.

### How the attention mask is storedHow the attention mask is stored

In Kvax, there are four types of blocks used to compute the attention weight matrix:

- 

Full blocks — Contain only tokens from the same data point, with no tokens hidden by the causal mask. In this case, attention is computed without constructing a mask or loading segment and position tensors.

- 

Left partial blocks — Positioned to the left of full blocks (this is accurate for the forward pass; the backward pass might differ slightly). These blocks don’t contain tokens hidden by the positional mask, so only the document mask is computed.

- 

Right partial blocks — Similar to left partial blocks but positioned to the right of full blocks. These blocks may include tokens hidden by both the document and positional masks, so both masks must be computed.

- 

Empty blocks — Fully masked-out blocks that don’t contribute to attention calculations and are skipped to optimize performance.

Example of a blockwise calculated attention matrix with seq_len = 20 and block_size = 5, with document and causal masks

In Kvax, the attention mask is constructed by dividing the entire batch sequence (specifically, the query sequence during the forward pass) into blocks. The block size is defined in FlashAttentionParamsConfig, resulting in a new matrix with dimensions (batch_size × seq_len / block_size × 4). Each row of this matrix is represented by four integer values: (lower_bound, lower_full_bound, upper_full_bound, upper_bound). The attention mask, after block separation, is as follows:

- (0, lower_bound) — Empty blocks

- (lower_bound, lower_full_bound) — Left partial blocks

- (lower_full_bound, upper_full_bound) — Full blocks

- (upper_full_bound, upper_bound) — Right partial blocks

- (upper_bound, seq_len / block_size) — Empty blocks

This structure efficiently represents the attention mask, allowing unnecessary computations to be skipped. It requires only 3 × batch_size × seq_len / block_size × 4 × 4 bytes to store the full mask, where the factor of 3 corresponds to the three masks: one for the forward pass and two for the backward pass (covering the dquery and dkey/dvalue loops). The final 4 represents the number of bytes per int32 value.

At runtime, these four values are loaded, and the attention operation is computed in three inner loops:

- Left partial blocks

- Full blocks

- Right partial blocks

This approach optimizes performance by avoiding unnecessary calculations while maintaining flexibility in handling attention masks.

Combined causal and document attention mask for the forward pass, drawn by the print_mask function. The y-axis corresponds to query blocks, while the x-axis corresponds to key-value (KV) blocks. White blocks indicate full blocks, while grey blocks indicate partial blocks. Parameters: Sequence length = 4096, Number of data sequences = 3, Number of pad tokens = 400.

### Context parallelismContext parallelism

As mentioned, Kvax uses the all-gather–based approach described in the Llama 3 training paper. In this method, an all-gather operation is performed on the key and value tensors to collect the full tensors on every GPU before calculating attention, ensuring these tensors are replicated across all GPUs. This enables each GPU to independently compute the forward pass for its chunk of the query tensor, with each GPU receiving the correct chunk of the attention operation output. The outer loop distributes query chunks across GPUs, while the inner loop computes outputs independently using the key and value tensors.

During the backward pass, the gradients for the query, key and value tensors (dquery, dkey and dvalue) must be computed. For dquery, the same strategy as the forward pass is applied. Conversely, when computing dkey and dvalue, the inner and outer loops are reversed. Since the full query tensor isn’t locally available, an AllReduce operation is performed on the dkey and dvalue tensors at the end of computation on each GPU.

### Balancing between GPUsBalancing between GPUs

To optimize performance during context parallelism (CP), the LLaMA 3 training article recommends shuffling tokens across the sequence length:

“In CP, we partition across the sequence dimension, and specifically, we partition the input sequence into 2 × CP chunks so each CP rank receives two chunks for better load balancing. The i-th CP rank received both the i-th and the (2 × CP−1−i)-th chunks.”

Kvax implements this approach as well. The query input tensor is split into 2 × CP chunks along the sequence axis, and each GPU stores two chunks: the i-th and the (2 × CP − 1 − i)-th chunks. Before the forward pass, the key and value tensors are unpermuted to maintain their original order. Additionally, an auxiliary tensor, query_global_offset, is used to pass the global position of the query tensor into the kernel, ensuring the correct positional mask is applied during computation.

Causal attention mask with token balancing across 4 GPUs for forward pass, drawn by the print_mask function. The y-axis corresponds to query blocks, while the x-axis corresponds to key-value (KV) blocks. White blocks indicate full blocks, while gray blocks indicate partial blocks.

To enable this logic, set permute_tokens_for_load_balance to True in flash_attention_triton function and use the permute_tokens_context_parallelism function before starting the calculations. Afterward, use the unpermute_tokens_context_parallelism function to unpermute tokens before computing the loss. For further details, please refer to the example in the How to use section of the Kvax readme.

### How context parallelism and document mask work togetherHow context parallelism and document mask work together

As mentioned, Kvax fully supports using document masks and context parallelism together.

Combined causal and document attention mask with token balancing across four GPUs for the forward pass, drawn by the print_mask function. The y-axis corresponds to query blocks, while the x-axis corresponds to key-value (KV) blocks. White blocks indicate full blocks, while gray blocks indicate partial blocks.

To effectively combine these features, we implemented several techniques:

- 

To calculate dkey and dvalue during the backward pass, we add a “fake” axis to the mask tensors, resulting in shapes [batch_size, shard_axis, kv_seq_len / block_size]. In this case, we need to calculate the [batch_size, kv_seq_len / block_size] mask on every GPU, which can’t be directly split along the context parallelism (CP) axis because kv_seq_len isn’t sharded. Each GPU has a unique mask segment, based on its chunk of the query tensor. To address this, we introduce the auxiliary axis shard_axis to distribute the attention mask across GPUs. To reconstruct the full mask, we concatenate masks along this shard_axis, as implemented in the print_mask function.

- 

When computing dkey and dvalue with load balancing enabled, each GPU holds only two chunks of the query sequence during the backward pass. To switch between their global offsets, we use an auxiliary flag, load_second_global_offset, which loads the new offset value at the midpoint of the sequence.

- 

When context parallelism is enabled, Kvax employs two separate kernel implementations for the backward pass. The first kernel calculates dquery, while the second handles dkey and dvalue. If context parallelism is disabled, the entire backward computation occurs within a single Triton kernel.

# ResultsResults

### Kvax vs. CuDNNKvax vs. CuDNN

We tested Kvax using JAX 0.4.34, which includes a CuDNN-based attention implementation. Initially, we compared Kvax’s performance against CuDNN while varying the number of data sequences per batch sequence. To facilitate this comparison, we constructed and passed an attention mask to the CuDNN kernel (the implementation details can be found here).

Key findings:

- 

CuDNN encountered an error when the number of elements in the attention mask exceeded max(int32).

- 

CuDNN exhibited poor performance when the batch sequence contained more than one data sequence, due to the significant attention mask data movement required by the kernel.

To analyze performance with long sequences, we selected the following parameters:

- Batch size: 1

- Batch sequence length: 32768

- Number of attention heads: 16

- Attention head size: 128

We set batch_size = 1 to avoid the error mentioned above.

Note: Since performance depends heavily on the data when using a document mask, results may vary for different data sequence lengths. In these experiments, we set the data sequence length to the batch sequence length divided by the number of data sequences, adding a small amount of noise.

Comparison of Kvax and CuDNN attention implementations; forward pass only

Comparison of Kvax and CuDNN attention implementations; forward + backward pass

As the results show, CuDNN outperforms Kvax when the batch sequence contains a single data sequence. However, its performance significantly deteriorates when the number of data sequences exceeds one.

### Kvax vs. other attention implementationsKvax vs. other attention implementations

We also compared Kvax against several alternative attention implementations using Pytorch 2.5.1:

- 

CuDNN: jax.nn.dot_product_attention(..., implementation="cudnn")

- 

FA2: torch.nn.functional.scaled_dot_product_attention (without an attention mask)

- 

Flex Attention: torch.nn.attention.flex_attention, with Triton autotuning enabled via torch._inductor.config.max_autotune = True

For this comparison, we selected parameters similar to those used in Llama 3.1 8B:

- 

Number of attention heads: 32

- 

Number of KV heads: 8

- 

Attention head size: 128

To maintain a constant workload of batch_size × seq_len = 131072, we increased the batch sequence length while reducing the batch size accordingly.

Comparison of attention implementations with causal masks; forward pass only

Comparison of attention implementations with causal masks; forward + backward pass

For the second experiment, we used twelve data sequences per batch sequence.

Comparison of attention implementations with causal + document masks; forward pass only

Comparison of attention implementations with causal + document masks; forward + backward pass

In the graphs, “ERROR” corresponds to the same issue described in the Kvax vs. CuDNN section, while “OOM” indicates an out-of-memory error.

### Context parallelism vs. tensor parallelismContext parallelism vs. tensor parallelism

In this section, we evaluated different parallelism strategies while holding the following parameters constant:

- 

Batch size: 4

- 

Number of attention heads: 32

- 

Number of KV heads: 8

- 

Attention head size: 128

We increased the batch sequence length while simultaneously scaling the number of GPUs.

In this context, “balancing” refers to distributing tokens across GPUs for improved load efficiency, as described in the previous section.

Comparison of Kvax with tensor and context parallelism with causal mask; single data sequence per batch sequence

In this graph, we compared context and tensor parallelism using combined causal and document masks with twelve data sequences per batch sequence. To illustrate the differences in execution time clearly, we included a dense context parallelism version calculated without skipping zero blocks masked by the document mask.

Comparison of Kvax with tensor and context parallelism using document and causal masks; twelve data sequences per batch sequence

# ConclusionConclusion

Kvax is a high-performance attention implementation for the JAX framework, built for efficient training of large language models on long sequences. It supports data, tensor and sequence parallelism, all combinable with causal and document masks for maximum flexibility. Kvax is easy to use and provides an attention operation that can be effortlessly integrated into your codebase. Available under the Apache 2.0 license on GitHub, Kvax is ready to enhance your LLM training performance.

## ContributorsSergei Skvortsov, Filipp Fisin, Maria Trofimova, Boris Yangel＊

SS wrote the implementation, SS and FF devised the approach, BY, FF and MT reviewed the code for the release. BY led the project.

＊Correspondence to byangel@nebius.com

## Citation information
Please cite as:

 | Skvortsov et al., "Kvax: Fast and easy-to-use Flash Attention implementation for JAX", Nebius blog, 2025.

BibTeX citation:

 | @article{skvortsov2025kvax,
   title={Kvax: Fast and easy-to-use Flash Attention implementation for JAX},
   author={Skvortsov, Sergei and Fisin, Filipp and Trofimova, Maria and Yangel, Boris},
   year={2025},
   journal={Nebius blog},
   note={}
 }

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

#### See the contributors

Contents

- 

Video

- 

Intro

- Long-context training for AI agents

- Optimising attention with Flash Attention

- Ways to improve performance of Flash Attention. Document mask

- Parallelism techniques of attention operation

- 

Technical details of Kvax implementation

- Computation of document mask

- How the attention mask is stored

- Context parallelism

- Balancing between GPUs

- How context parallelism and document mask work together

- 

Results

- Kvax vs. CuDNN

- Kvax vs. other attention implementations

- Context parallelism vs. tensor parallelism

- 

Conclusion

- 

Contributors

- 

Citation information

## See also

### 

Scaling data collection for training software engineering agents

In this follow-up to our previous research blog post, we focus on the data collection process used to train our action generator and critic models. We’re also releasing two datasets on Hugging Face: nebius/SWE-bench-extra, containing 6,411 Issue/Pull-Request pairs, and nebius/SWE-agent-trajectories, featuring 80,036 software engineering agent trajectories, where an agent attempts to solve these issues.

December 20, 2024
9 mins to read

### 

Leveraging training and search for better software engineering agents

In this blog post, we’ll share some of our recent findings on how search can enhance agentic systems for software engineering. Specifically, we’ll demonstrate how we’ve built an SWE-agent-based system that exclusively uses open-weight LLMs and achieves a 40.6% resolved rate on SWE-bench Verified.

November 15, 2024
10 mins to read

### 

In-house AI R&D: Nebius’ secret ingredient for truly AI‑centric cloud

It wouldn’t be possible for us to build a machine-learning platform without advancing in the field ourselves.

July 29, 2024
9 mins to read

Sign in to save this post
Sign In
