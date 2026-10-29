# The invisible architecture behind great chat apps

Source: https://nebius.com/blog/posts/the-invisible-architecture-behind-great-chat-apps

Skip to main content

Everyone sees the model. No one sees the infrastructure that keeps a chat product alive when 500 QPS of emotional, chaotic human text hits a 70B model.

This guide reveals the engineering patterns behind modern conversational platforms, and how Nebius Token Factory shapes open models, serving pipelines and GPU economics to keep quality stable at scale.

The blueprint presented here is a proof of concept (PoC) grounded in work we conducted with a major conversational AI platform operating hundreds of thousands of concurrent chats. The details are anonymized, but the architectural lessons are real.

# Why chat is the hardest workload in inferenceWhy chat is the hardest workload in inference

Benchmarks make LLMs seem predictable. Chat traffic does not.

A production conversational system is a living organism: constant QPS at the core, sudden spikes during launches or experiments and thousands of long-running sessions where users produce deeply personal, chaotic and/or multi-turn exchanges. Context windows grow all day, and the prefill cost inflates with every message. Users swipe, retry and rate responses in real time and quality is measured not in accuracy but in repetition, output length, emotional consistency or the presence of empty replies. Product metrics don’t shift in minutes — they drift slowly over days.

This creates three fundamental pressures:

- 

Latency must be stable, not just fast. Users abandon or swipe after a bad tail, not a bad median.

- 

Quality must be consistent across millions of micro-interactions. Small sampler bugs or quantization artifacts show up as one-star ratings.

- 

Cost must be tamed. Long contexts mean most GPU time goes into prefill and cache. If you serve chat naively, cost becomes unbounded.

This is why the infrastructure behind chat apps is invisible. When it works, no one thinks about it. When it fails, users notice instantly.

# Token Factory’s architecture for conversational workloadsToken Factory’s architecture for conversational workloads

Nebius Token Factory exists specifically to handle workloads that overwhelm generic inference stacks. The architecture centers around dedicated endpoints with predictable latency, autoscaling tuned to conversational patterns and inference pipelines designed around KV cache behavior. Prefill and decode are handled with precision. Zero-retention inference and regional isolation ensure compliance. Fine-tuning, quantization and distillation pipelines shape the model before it ever hits production. Meanwhile, everything remains accessible through a familiar OpenAI-compatible API.

To you it looks like one endpoint. Behind it sits an architecture shaped entirely around the physics of chat traffic.

# Shaping the model before scaling the infrastructureShaping the model before scaling the infrastructure

The first step in any serious chat deployment is model shaping, not GPU tuning, not caching — model shaping.

In our recent large-scale POC, our partner began with an official FP4 checkpoint of a 70B chat model. It was incredibly fast, but the early A/B signals told a different story. Replies were noticeably shorter, repetition increased, empty outputs appeared more often, session lengths dipped and one-star ratings crept upward. Nothing was catastrophically wrong. The model simply behaved differently than what users expected.

To correct this, we treated quantization and sampler behavior as first-class engineering problems, not optional polish. That meant:

- Re-quantizing the model by using thousands of real anonymized chat sessions instead of small synthetic calibration sets.

- Expanding the calibration dataset from a few hundred examples to tens of thousands, because nuance in chat only appears at scale.

- Experimenting with KV cache precision (FP8 vs. BF16) to recover semantics lost in aggressive FP4 compression.

- Verifying sampler correctness, ensuring temperature, top_p and penalties were actually applied by the inference kernels.

- Validating speculative decoding behavior to confirm it sped things up without flattening style or increasing short replies.

This is the invisible part of chat infrastructure.

If the model’s behavior is misaligned to how users converse, no amount of GPUs, caching or routing can save the experience. Model shaping ensures the serving layer isn’t fighting upstream against the wrong behavior.

# The real shape of prefill and decode in chat systemsThe real shape of prefill and decode in chat systems

A single chat request looks simple. The system behind it isn’t.

Every request moves through two very different phases. Prefill loads the full conversation history, and its cost grows with context length. Decode then generates tokens one by one while batching across many active sessions. These paths have completely different bottlenecks, so optimizing chat means optimizing their relationship, not treating them as one monolithic step.

On Token Factory, this workload required a split architecture built specifically for conversational patterns. We introduced:

- 

Prefill-specialized workers with large memory footprints and high bandwidth for long histories.

- 

Decode-specialized workers tuned for stable batching and consistently low TTFT.

- 

A routing layer that prioritized cache locality, ensuring session continuity rather than naïve round-robin scheduling.

- 

Backpressure controls to prevent decode queues from overrunning during spikes.

In controlled tests, this design allowed a node of four NVIDIA B200 GPUs to sustain around 10 RPS with high cache efficiency. At larger scale, roughly 40 GPUs supported around 100 QPS of real conversational traffic with predictable latency and cost per request.

Prefill/decode disaggregation is one of the key distinctions between simply serving a model and running a real chat platform. It transforms inference from a GPU-bound loop into a balanced system designed around conversational flow.

# KV cache is the economic engine of chat inferenceKV cache is the economic engine of chat inference

In chat systems, most tokens aren’t new. They come from earlier turns in the same conversation. That single fact makes KV cache behavior the most powerful economic lever in conversational inference.

At the start of the POC, cache hit rates were extremely low — around five percent. With cache-aware routing and larger per-GPU buffers, they climbed past thirty percent. After additional tuning, controlled tests reached the fifty to sixty percent range. Each step had an outsized effect: as cache efficiency improved, the GPU cost per 100 QPS dropped by multiples.

We also explored host offloading and vLLM’s LMCache to understand how far cache extension techniques could push capacity beyond on-device limits, especially for ultra-long contexts.

The conclusion was straightforward. Cache isn’t an optimization detail. It’s the hidden economic multiplier. A 70B model does not require 2500 GPUs if you can reuse most of its context tokens. This is how Token Factory achieves four-times cost reductions on real conversational workloads.

And this isn’t theory — we observed these gains directly in mirrored production traffic.

# Quality for chat is a multidimensional problemQuality for chat is a multidimensional problem

In large chat systems, quality isn’t accuracy — it’s behavior.

A model can perform well on benchmarks and still feel wrong in a real conversation. That’s because quality in chat emerges from how the model interacts with users over time, not from how it scores on static inputs.

In our POC, our partner measured quality through product signals that reflected real user engagement: how many sessions people started, how long they stayed active, how often they swiped a reply away, how frequently short or empty responses occurred, how output length varied across turns and how repetition patterns evolved. These indicators gave a far better picture of conversational health than any offline metric could.

When we introduced an early quantized model, several of these behavioral signals drifted. The changes were subtle but noticeable, and they appeared long before any conventional evaluation would have detected a regression. This revealed a few important truths.

Sampler correctness is foundational. Small deviations in temperature or penalty handling can reshape user behavior.

Repetition control is not cosmetic. It meaningfully influences engagement and session depth.

finish_reason anomalies often correlate with user frustration and lower ratings.

Instability corrupts A/B tests. Users penalize outages more severely than content flaws.

Quantization needs nuance. Many chat models require light fine-tuning to restore lost behavioral fidelity.

Serving stability determines signal quality. Traffic spikes distort metrics, so reliability is a prerequisite for trustworthy comparisons.

Token Factory’s post-training pipeline exists specifically to correct these behavioral mismatches. Fine-tuning, distillation and quantization are applied by using real conversational traffic so that the model aligns with how users actually speak — not how benchmarks assume they do.

# Reliability engineering for conversational platformsReliability engineering for conversational platforms

If an email assistant times out once, no one cares. If a chat model spikes to five or eight seconds TTFT for even a few minutes, user behavior changes instantly. Large-scale conversational inference is unforgiving, and the reliability problems it exposes do not resemble benchmark failures.

During the POC, we encountered three broad classes of failures that real chat traffic reliably surfaces: state corruption, traffic-induced overload and infrastructure immaturity. Each class revealed different weaknesses, which we then strengthened in the platform.

### State corruption and inference consistencyState corruption and inference consistency

These were the most dangerous incidents because they produced incorrect or nonsensical outputs:

- 

Decode workers entering invalid request states, leaving sessions stuck until restarted.

- 

KV cache corruption in the prefill-decode pipeline, which occasionally produced gibberish responses.

- 

Malformed token IDs (≥128K) reaching inference, unnecessarily triggering error cascades.

- 

Inconsistent pod reattachment, where restarted workers weren’t reused, silently reducing capacity.

These issues required upgrades to the TensorRT-LLM engine, stricter request validation and more precise lifecycle management for prefill and decode workers.

### Traffic and concurrency overloadTraffic and concurrency overload

Chat traffic does not fail gracefully. It compounds:

- 

Retry storms amplified 500s into full-system instability.

- 

Router queue saturation during heavy prefill-decode imbalance.

- 

Sudden spikes above 3K RPM from the client side that exceeded the reserved budget.

- 

Aggressive liveness probes that restarted healthy workers and destabilized batching.

These failures drove improvements in retry heuristics, backpressure logic and router awareness of where saturation was occurring.

### Region- and platform-level operational gapsRegion- and platform-level operational gaps

Some failures had nothing to do with the model at all, but with ecosystem maturity:

- 

Logging pipelines overwhelmed by high-volume telemetry in a new region.

- 

Cross-regional inconsistencies, as this was the first time running a large dedicated cluster of modern GPUs outside the main region.

- 

Autoscaler and probe defaults not suited to conversational workloads.

These surfaced the need for a more resilient shared operational layer: higher-throughput logging, cross-region parity checks and workload-specific probe configurations.

### The result: A hardened conversational serving layerThe result: A hardened conversational serving layer

Every failure mode in the POC translated into an architectural improvement. Instead of treating them as isolated bugs, we folded them into the serving layer so future chat workloads inherit a more resilient baseline.

Some improvements targeted reliability under load. We introduced more intelligent retry logic, to prevent amplification during partial outages, and refined liveness behavior so only decode workers restart when they truly need to. The router became aware of prefill and decode saturation, allowing it to keep queues stable even during heavy bursts.

Other changes strengthened input validation and inference correctness. Malformed or pathological requests are automatically filtered before they can cascade into 500s. Upgrading TensorRT-LLM eliminated the KV cache corruption that occasionally produced gibberish replies.

We also reinforced operational foundations for multi-region deployments. Logging pipelines were rebuilt to handle high-throughput conversational telemetry, cross-region consistency checks were added for new clusters of modern GPUs and probe and autoscaler configurations were re-tuned specifically for conversational traffic patterns.

Finally, we added a layer of chat-specific observability and redundancy. Dedicated alerts now track tail TTFT, cache drops, finish_reason drift and decode error bursts. Critical endpoints run with X+1 redundancy patterns so a single worker can fail without degrading live user sessions.

None of this is visible to end users. All of it is essential for stable A/B tests and consistent product metrics. Chat systems don’t need perfection, but they do need predictability. Quality can be tuned. Instability cannot.

# Governance and security expectations for chatGovernance and security expectations for chat

Serious chat applications handle sensitive, often personal, conversational data. The infrastructure behind them has to respect that. Token Factory is built so teams can operate large-scale chat workloads without compromising their governance or regulatory posture.

All inference runs in zero-retention mode, ensuring that prompts and outputs are never stored or reused. Deployments are region-locked to the EU or US, meeting data residency requirements by default. The platform is fully SOC 2 Type II, ISO 27001 and HIPAA certified, with optional custom DPAs for organizations that need tighter contractual guarantees. Access is governed with SSO, RBAC and project-level isolation, so multiple teams can work safely within the same environment. Dedicated endpoints run with a 99.9% SLA, giving product teams both isolation and predictable latency.

This combination lets conversational platforms experiment with open models at scale while staying fully aligned with internal security standards and external compliance requirements.

# How a real deployment comes togetherHow a real deployment comes together

A typical deployment on Token Factory follows this arc:

- 

Session profiling. We ingest representative traffic, including prompt lengths, reply lengths, cache locality patterns and sampler settings.

- 

Model selection and shaping. We choose a base model and shape it by using quantization, sampler tuning, fine-tuning, if needed and calibration based on real user behavior.

- 

Inference system design. Prefill/decode disaggregation, cache sizing, routing strategies, batching windows and speculative decoding are tuned to your workload.

- 

Dedicated endpoint deployment. Regional isolation, autoscaling tuned to your traffic profile, predictable latency targets and full observability.

- 

A/B rollout and iteration. We iterate on quality and economics until your product metrics converge.

- 

Scale to steady state. Guaranteed QPS, predictable cost per 100 QPS and managed operations.

This is where the invisible architecture matters most. A conversational workload cannot be solved with a single model update. It is a continuous collaboration between model shaping, inference infrastructure and workload-specific engineering.

# The real takeawayThe real takeaway

The most important thing we learned from running large conversational POCs is this: a great chat experience is not just a great model — it is a system.

It is quantization shaped to your user base, cache locality tuned to your traffic, sampler correctness tested against your engagement metrics, routing that understands conversational load, speculative decoding that does not distort style, error handling that avoids retry storms and tail latency, and post-training alignment grounded in real sessions. It is infrastructure tuned to human conversation, not to benchmarks.

Nebius Token Factory exists so you don’t need a 20-person inference R&D team to run open-source chat models at scale. We take the operational and architectural complexity, and bake it into a dedicated inference layer designed specifically for your workloads.

If you’re operating a conversational product and want to understand how this architecture applies to your traffic, reach out. We can analyze your logs, profile your sessions and work with you to size a dedicated endpoint that delivers the quality, latency and economics your product needs.

You bring the conversations, and we’ll bring the invisible infrastructure to keep them running.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Dylan Bristot
Product Marketing, Token Factory

Contents

- 

Why chat is the hardest workload in inference

- 

Token Factory’s architecture for conversational workloads

- 

Shaping the model before scaling the infrastructure

- 

The real shape of prefill and decode in chat systems

- 

KV cache is the economic engine of chat inference

- 

Quality for chat is a multidimensional problem

- 

Reliability engineering for conversational platforms

- State corruption and inference consistency

- Traffic and concurrency overload

- Region- and platform-level operational gaps

- The result: A hardened conversational serving layer

- 

Governance and security expectations for chat

- 

How a real deployment comes together

- 

The real takeaway

## See also

### 

Post-training by Nebius Token Factory: The missing layer between MVP and production

Post-training by Token Factory is now live, the missing layer between MVP and real production AI. Base models are great for demos, but production needs models trained on your data that are faster, cheaper, and aligned to your workflows. Today, Token Factory makes that possible for every team, without building ML infrastructure.

December 9, 2025
10 mins to read

### 

NVIDIA Nemotron Nano 2 VL in Nebius AI Studio: powering agentic multimodal AI

We’re pleased to announce that Nebius AI Studio now hosts NVIDIA Nemotron Nano 2 VL, a compact, production-ready multimodal reasoning model engineered for real-world document intelligence and video understanding.

October 28, 2025
3 mins to read

### 

Leveraging high-speed, rack-scale GPU interconnect with NVIDIA GB200 NVL72

Let’s explore one of the key features that makes the new NVIDIA GB200 NVL72 stand out: the fifth generation NVIDIA NVLink™ scale-up fabric. We’ll discuss how it redefines infrastructure by moving beyond the traditional 8-GPU NVLink. You’ll see a practical example of how to take advantage of this capability. Finally, we’ll examine a real-world use case: pre-training the Nemotron-4 340B LLM.

October 23, 2025
10 mins to read

Sign in to save this post
Sign In
