# Nebius and WEKA benchmark shared KV cache for agentic inference on NVIDIA HGX B300

Source: https://nebius.com/blog/posts/nebius-weka-shared-kv-cache-benchmark-hgx-b300

Skip to main content

Every turn of an agent loop is a new inference request, and its prompt is the entire session so far. A coding agent that makes fifty tool calls sends fifty requests, each one carrying every earlier prompt, tool output and model reply. The inference engine skips recomputing that history only while its KV cache is still resident in GPU memory, and that memory is shared with the model weights.

Long sessions fill it quickly; once a session’s blocks are evicted, its next turn prefills the full history to process the few thousand tokens it actually added. Spilling KV blocks to host DRAM buys more capacity, but that memory belongs to one node. A request that the router lands anywhere else has no cache to hit and prefills from zero.

WEKA® NeuralMesh™ with Augmented Memory Grid™ offers a distributed KV cache storage layer that significantly expands the amount of storage GPUs can quickly access during LLM Inference. The longer requests are and the more users you serve, the more benefits this storage tier provides.

To measure how much of that recompute a shared cache tier eliminates under sustained load, Nebius and WEKA ran an eight-hour soak test of Augmented Memory Grid on NVIDIA HGX B300 instances in Nebius AI Cloud, replaying real agentic coding traffic against DeepSeek-V4-Pro. The result: 2.4× the requests served on the same serving node, with a 93% cache hit rate against 40% for HBM alone.

## What the benchmark held constantWhat the benchmark held constant

Both runs used one eight-GPU HGX B300 serving node at TP=8, the same vLLM stack, the same 512-session active pool drawn from a corpus of more than 5,000 captured agentic sessions, and the same eight-hour window. The only variable was the KV cache tier: GPU HBM alone, or HBM backed by Augmented Memory Grid pooling local NVMe across an eight-node B300 cluster over GPUDirect RDMA on the InfiniBand fabric.

The workload was replayed production traffic, not synthetic prompts. Each session’s context grew turn over turn as the agent re-read its history, with some contexts approaching 900,000 tokens. Keeping 512 of these sessions active pushed the working set well past what HBM can hold, which is exactly the condition a cache tier exists to handle.

## Augmented Memory Grid served 2.4× the requests at a quarter of the error rateAugmented Memory Grid served 2.4× the requests at a quarter of the error rate

Over eight hours on the same serving node, the two configurations diverged on every metric that matters for capacity planning.

- 

Requests served: 55,694 on Augmented Memory Grid vs. 23,015 on HBM-only, with a 0.64% error rate against 2.32%.

- 

Output tokens per GPU-hour: 169,000 against 46,000, a 3.7× difference.

- 

Cache hit rate: 93% against 40%. Augmented Memory Grid prefilled 4,400 uncached tokens per request instead of 33,900, and 3.2× fewer in total across the run despite serving 2.4× the requests.

- 

Time to first token (TTFT): p50 at 1.05 s against 5.68 s (5.4x lower), with p95 at 3.82 s against 23.12 s (6.0x lower).

- 

Requests under a 5-second TTFT bar: 97% against 44%.

The stability result matters as much as the headline numbers. HBM-only degraded across the run as the working set outgrew GPU memory: median TTFT climbed from 6.7 s in the first hour to 7.9 s in the last, and the timeout rate rose from 1.1% to 5.2%. Augmented Memory Grid held median TTFT inside a 0.98–1.14 s band and never exceeded a 1.3% error rate in any hour. A decaying tier forces you to provision for its worst hour. This one did not decay.

Figure 1. HBM-only median TTFT rises from 6.7 s to 7.9 s as the working set grows; Augmented Memory Grid holds between 0.98 s and 1.14 s

## The infrastructure underneathThe infrastructure underneath

The benchmark ran on standard NVIDIA HGX B300 instances in Nebius AI Cloud, configured as an eight-node cluster with the following setup.

- 

GPUs: 8 × NVIDIA B300 SXM per node, 270 GB HBM each.

- 

Interconnect: NVIDIA ConnectX-8 at roughly 800 Gb/s per GPU, with GPUDirect RDMA on the NVIDIA Quantum InfiniBand fabric.

- 

Cache tier: six local NVMe drives per node, pooled by WEKA NeuralMesh 5.1 into a shared tier.

- 

Serving stack: vLLM v0.23 with Augmented Memory Grids KV-cache offload engine, serving nvidia/DeepSeek-V4-Pro-NVFP4 at a one-million-token maximum context.

The RDMA path is what makes a shared tier viable at inference latencies. KV blocks move from HBM to NVMe on any node in the cluster without a CPU hop, so cached context is not owned by the machine that filled it. Teams evaluating shared KV cache on Nebius B300 clusters can request a proof of concept through Nebius sales.

## Read the full benchmarkRead the full benchmark

WEKA’s post covers the methodology in detail: the replay dataset and how it was captured, why HBM-only was the baseline for DeepSeek-V4, tail-latency analysis, and the hour-by-hour stability data. The dataset and capture tooling are open-sourced alongside it.

Read the full benchmark on the WEKA blog.

Sign up for a proof of concept with Nebius.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

David Schulman
Senior Director of Partner Marketing

Hooman Ramezani
Solutions Architect

Alexey Averin
Senior Technical Product Manager

Contents

- What the benchmark held constant

- Augmented Memory Grid served 2.4× the requests at a quarter of the error rate

- The infrastructure underneath

- Read the full benchmark

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

MLPerf® Inference v6.1: Previewing NVIDIA Vera Rubin NVL72 and leading full-rack Nebius system with NVIDIA GB300 NVL72 results

Nebius submitted results across seven system configurations to MLPerf® Inference v6.1, our broadest round to date. We took five first-place results, including both DeepSeek R1 scenarios on the full-rack Nebius GB300 NVL72, and were one of only two providers to post preview results on NVIDIA Vera Rubin NVL72, where we led per-GPU Server throughput on DeepSeek R1.

September 16, 2026
16 mins to read

### 

Nebius Token Factory Becomes First AI Cloud to Adopt NVIDIA Groq 3 LPX

Nebius is he first AI cloud to adopt NVIDIA Groq 3 LPX, to Nebius Token Factory, adding generation-optimized performance purpose-built for agentic AI. Independently benchmarked at 3,400 output tokens per second for a single user on Google Gemma 4 31B, NVIDIA Groq 3 LPX pairs with NVIDIA Vera Rubin NVL72 so developers get it through the same Token Factory catalog and API they already use.

August 24, 2026
4 mins to read

Sign in to save this post
Sign In
