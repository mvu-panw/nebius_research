# SGLang: Turbocharging DeepSeek inference

Source: https://nebius.com/customer-stories/sglang

Skip to main content

## Long story shortLong story short

Serving a powerful large language model like DeepSeek R1 at speed and scale is no small feat. SGLang, a pioneering LLM inference framework, teamed up with Nebius AI Cloud to supercharge R1’s performance for real-world use. SGLang achieved a 2× boost in throughput and markedly lower latency on one node. In practice, this means faster answers from R1, even on long prompts or with dozens of users at once.

SGLang is an open-source fast serving framework for large language models and vision-language models. Its mission is to make interaction with LLMs faster and more controllable by co-designing both an efficient backend runtime and a flexible front-end interface for AI applications. The framework supports a wide range of models and innovations, such as prefix caching, continuous batching and quantization.

## ContentsContents

Challenge: Maximizing LLM throughput for DeepSeek R1

Approach: Collaboration and benchmark-driven optimization

Optimization techniques

Performance tuning guide: Quick principles

Takeaways

Acknowledgements

## Challenge: Maximizing LLM throughput for DeepSeek R1

For the detailed story we focus on R1, which is, of course, a large-scale reasoning model known for its complex inference patterns and high computational load. Serving such a model to end-users poses significant challenges:

- 

Heavy computation: R1 requires immense compute for each query. Standard inference setups often became a bottleneck, limiting the model’s responses to only a few tokens per second per instance. SGLang needed to overcome this to ensure a seamless user experience.

- 

Long contexts: The model excels at tasks requiring long context (e.g., solving multi-step problems, reading lengthy documents). However, processing prompts of thousands of tokens can dramatically slow down generation if the system isn’t optimized for long sequences. The team observed that as input lengths grew, throughput dropped and latency to first token increased — an unacceptable trade-off for interactive use.

- 

High concurrency: In real deployments, multiple users or requests hit the model simultaneously. R1 needed to handle dozens of concurrent generation requests without grinding to a halt. Ensuring scalability of throughput with rising concurrency (16, 32, up to 80 parallel requests) was a core challenge.

- 

Latency sensitivity: Users not only care about how many tokens per second the model can generate overall, but also how quickly it starts responding. The “time-to-first-token, ” especially at the 99th percentile (worst-case scenario), needed improvement so that even under heavy load, every user gets a prompt answer. SGLang set out to reduce these tail latencies, which were initially quite high (tens of milliseconds or more).

- 

Maintaining accuracy: Any optimization, especially those involving lower precision or altered model behavior, had to preserve the model’s output quality. R1’s hallmark is its strong reasoning ability — SGLang could not sacrifice accuracy or coherence for speed. Thus, the challenge was achieving performance gains in a balanced way.

In summary, the task was to squeeze the most out of R1’s inference — more tokens per second, support for longer prompts and stable low latency — all on reliable infrastructure that can be scaled up for production. This is where Nebius AI Cloud entered the picture.

## Approach: Collaboration and benchmark-driven optimization

To tackle these challenges, SGLang collaborated with Nebius AI Cloud’s solution architects and infrastructure in a methodical, data-driven optimization effort. The approach consisted of several phases:

- 

Establishing a performance baseline: First, the teams deployed R1 on Nebius AI Cloud by using a standard serving setup, to measure baseline performance. This included running a diverse benchmark suite covering varying input sizes and concurrency levels, be it throughput and latency on short 100-token prompts or long 10,000-token prompts, under loads of 16–80 concurrent requests. This comprehensive baseline highlighted how throughput dipped and latencies spiked in certain scenarios, quantifying the gaps to close. Nebius’ logging and monitoring tools made it easy to gather detailed metrics across these runs.

- 

Identifying bottlenecks: With baseline data in hand, the SGLang team analyzed the parts of the inference pipeline that were limiting performance. The profiling pointed to the attention mechanism as the primary hotspot. Specifically, R1’s use of multi-latent attention (MLA) — a sophisticated attention variant — gave excellent reasoning quality but added overhead, especially as the sequence length grew. Additionally, standard FP16 GEMM (general matrix multiply) ops and numerous small kernels were creating inefficiencies. The team zeroed in on potential solutions: optimize the attention algorithm, exploit lower precision arithmetic and reduce kernel launch overhead. The analysis also considered memory usage (due to large key/value caches for long contexts) and how concurrency was handled by the scheduler.

- 

Rapid experimentation on Nebius infrastructure: Nebius AI Cloud provided SGLang with on-demand access to AI compute clusters and flexible tooling to try out improvements. This allowed the team to iterate quickly. Nebius’ support for containerized workloads and custom drivers meant SGLang could integrate experimental libraries (like custom CUDA kernels) without hassle. Over a series of experiments, they incrementally upgraded the serving stack by swapping out the default attention mechanism for the new FlashAttention-3 algorithm, enabling FP8 precision with DeepSeek’s proprietary DeepGEMM library and then adjusting the SGLang’s serving engine configuration. This increased the maximum decode batch size to better utilize CUDA Graphs and tweak memory management for cache utilization.

Each trial provided data on throughput (measured in tokens/sec and queries/sec) and latencies (median and 99th percentile), which guided further tweaks. This tight feedback loop was crucial — what could have taken weeks of guesswork was accomplished in days, thanks to Nebius’ robust experimentation environment.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Optimization techniques: Key innovations implemented

Here are key ideas that enabled the boost to DeepSeek’s throughput:

FlashAttention-3: The latest iteration of the FlashAttention-3 algorithm was deployed, to accelerate R1’s attention calculations. FlashAttention-3 leverages asynchronous Tensor Core operations and optimizes memory access patterns to compute attention far more efficiently than standard methods.

Dynamic MLA-to-MHA switching: R1 uses MLA in its architecture — a novel attention mechanism that maintains latent states to enhance reasoning. However, MLA’s additional computations can become a burden when the prompt (prefix) is very long. SGLang implemented a smart switch: for long prompt prefixes beyond a certain length, the model automatically reverts to standard multi-head attention (MHA). This hybrid approach preserves MLA’s benefits for decoding but avoids its overhead on long contexts.

DeepGEMM (FP8 matrix multiplication): The team utilized DeepGEMM, a custom CUDA library released by DeepSeek AI. DeepGEMM is specialized for FP8 arithmetic — it performs 8-bit floating point matrix multiplied with fine-grained scaling, to maintain numerical stability at twice the speed. This change provided a huge boost to throughput, as these matrix multiplications form the bulk of the computation in each token generation step. Careful calibration in DeepGEMM allowed for the negligible precision loss.

Kernel fusion: Another optimization was fusing kernels to eliminate unnecessary overhead. In the original serving workflow, certain operations ran back-to-back as separate kernels. Each kernel launch has overhead and can introduce pipeline stalls. SGLang merged several of these operations into single kernels. This reduced the per-token latency and made the execution more bandwidth-efficient. Especially under high concurrency, kernel fusion ensured that the workload was continuously handled. The impact was seen as an uptick in throughput across all tested scenarios and smoother latency curves during inference.

Partial KV cache loading: Handling long contexts means large key/value (KV) caches for attention. SGLang used partial KV cache loading — if a new request comes in with a prompt that is an extension of a previously seen prompt, the system can reuse the cached keys/values for the shared prefix instead of loading a completely new cache. This technique, supported by Nebius’ memory management capabilities, saved time whenever users had overlapping query contexts or during iterative dialogue with the model. It effectively amortized the cost of long prompt processing over multiple tokens.

Data-parallel attention computation: Lastly, to further increase speed under heavy loads, SGLang parallelized the attention computation across available compute when possible. This data-parallel attention splits the workload of computing attention for multiple queries, ensuring that even as request counts grow, the attention stage doesn’t become a serial bottleneck. Nebius AI Cloud’s infrastructure allows experiments with distributing attention for very large batch sizes. The outcome was that the system maintained nearly flat throughput when scaling from 16 to 32 to 64 concurrent requests — a testament to effective parallelization.

Each of these optimizations on its own provided a piece of the overall performance puzzle. The true power was realized when all techniques were combined in the final deployment.

## Performance tuning guide: Quick principles

Benchmarking and parameter tuning can seem complex, but some simple rules of thumb can streamline the process.

- 

Analyze server logs: Server logs provide insights into request numbers, token usage and generation throughput. Familiarize yourself with parsing them as they offer the quickest way to identify optimization opportunities.

- 

Enable CUDA Graphs: CUDA Graphs often provide the most significant improvement in latency and throughput. It should be enabled by default, unless specific constraints prevent its use.

- 

Optimize CUDA Graphs max batch size: If memory permits, increasing the CUDA Graphs batch size can improve utilization. Test incremental increases and monitor latency to find the optimal setting for your workload.

- 

Align parameters with the workload: Optimal settings depend on request patterns (batch size variance, sequence lengths, concurrency) and service-level objectives. Re-benchmark when these patterns change. Evaluate the effectiveness of parameter adjustments by observing the generation throughput in the logs under your specific workload.

## Takeaways: Fast infrastructure + Clever optimizations = A winning combination

This SGLang-Nebius case study underlines several important lessons and reaffirmed best practices in the realm of AI infrastructure:

- 

Infrastructure matters: The right cloud infrastructure is a catalyst for innovation. By providing ready access to the latest hardware and a flexible environment for custom code, Nebius AI Cloud allowed SGLang to try bold ideas quickly. If they had been constrained by limited hardware or rigid environments, implementing something like FlashAttention-3 or custom kernels would have been far slower, if not impossible. The case demonstrates that for AI startups and frameworks, collaborating with an agile infrastructure provider can drastically shorten the path to breakthroughs.

- 

Collaborative tuning yields big wins: Performance optimization for LLMs is a multi-faceted challenge —it spans model internals as well as system-level orchestration. The success here came from close collaboration: Nebius’ engineers and SGLang’s developers put their heads together to tackle the problem from all angles. SGLang knew the models; Nebius knew the hardware and scaling. Together, we achieved what neither might quickly do alone. This highlights the value of cloud providers working hand-in-hand with clients on technical deep-dives, not just providing resources.

- 

Layered optimizations — no silver bullet, but cumulative impact: There wasn’t one single trick that made DeepSeek R1 fast; it was the accumulation of many optimizations. From algorithmic changes (FlashAttention-3, MLA/MHA toggle) to low-level improvements (FP8 and kernel fusion) to configuration tuning (batch sizing, caching), each contributed to the final result. Organizations looking to speed up AI workloads should adopt a holistic approach: profile the system, address each bottleneck methodically and stack improvements. Small percentages can multiply into big gains when done across the board.

In conclusion, the SGLang and Nebius AI Cloud collaboration vividly demonstrates how pairing cutting-edge model-serving software with a powerful, flexible cloud infrastructure can unlock new levels of performance. R1 can now reach its audience faster and more efficiently, reinforcing SGLang’s product value. For Nebius, it’s another success story of enabling AI innovators to achieve their goals. The journey doesn’t end here — both teams are looking at what’s next, whether it’s applying these optimizations to other models like DeepSeek-V3, or exploring additional techniques (such as advanced parallelism or model pruning) to continue the march toward high-speed, accessible AI for all. The message is clear: with the right collaborations and technology, even the toughest AI inference challenges can be overcome, one token (or 10,000) at a time.

## Acknowledgements

The SGLang team would like to express heartfelt gratitude to the following collaborators:

SGLang Core Team and Community Contributors — Baizhou Zhang, Ke Bao, Yineng Zhang, Jingyi Chen, Cheng Wan, Jiexin Liang, Liangsheng Yin, Xiaoyu Zhang, Yi Zhang, Byron Hsu and many others.

## More exciting stories

## 

Simulacra AI

Simulacra AI is combining ab initio quantum chemistry with deep learning to build a scalable large wavefunction model (LWM) to generate high-accuracy datasets for drug and material discovery pipelines.
Read the story

## 

SynthLabs

Synthlabs significantly simplified their training infrastructure setup using TractoAI serverless platform. Synthlabs research engineers leveraged TractoAI distributed offline inference capability to accelerate the release of the first open source reasoning dataset.
Read the story

## 

Unum

In our field, effective partnerships that harness complementary strengths can drive significant breakthroughs. Such is the case with the collaboration between Nebius and Unum, an AI research lab known for developing compact and efficient AI models.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
