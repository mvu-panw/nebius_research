# Routing is the difference between scaling and stalling

Source: https://nebius.com/blog/posts/routing-is-the-difference-between-scaling-and-stalling

Skip to main content

## TLDRTLDR

When running more than one vLLM replica, routing strategy has a significant impact on performance.

On a real agent-style workload, using cache-aware routing instead of default Kubernetes routing:

- Reduced average inference step time by ~50 percent

- Reduced total runtime by ~36 percent

- Reduced P95 latency from more than a minute to under 20 seconds

The model, hardware and workload were identical. The difference was how requests were routed across replicas.

This blog describes the workload, the routing strategies compared and why cache awareness matters for stateful inference workloads.

## Routing once inference becomes distributedRouting once inference becomes distributed

Many inference discussions focus on model architecture, kernels or hardware efficiency. These factors remain important at all scales.

However, once inference is distributed across multiple replicas, routing strategy becomes an additional determinant of performance. While requests remain independent at the protocol level, their content becomes relevant for scheduling decisions. When successive requests share context, preserving execution locality across replicas affects how much prior work can be reused.

This post examines one concrete workload where routing strategy materially changed system behavior.

## Workload and experiment setupWorkload and experiment setup

This is not a synthetic throughput benchmark. It is an agent-style workload.

We ran SWE-style agent trajectories by using devstral-2-small-2512, with tool calls, growing context windows and sustained concurrency. Each trajectory consists of many sequential inference steps that reuse prior context rather than issuing independent requests.

This type of workload stresses inference systems differently from stateless completion traffic. Requests are correlated, context reuse is uneven and performance depends heavily on how state is handled across steps.

Configuration:

- 300 trajectories executed concurrently

- 6 independent runs per configuration

- vLLM as the inference backend

- Either 1 or 3 vLLM replicas

- Identical model weights and hardware in all cases

The single-replica setup serves as a baseline where cache locality is implicit. The three-replica setup introduces distributed state, making routing decisions relevant to whether context is reused efficiently or repeatedly reconstructed.

Each run consists of thousands of inference steps with skewed context lengths and non-uniform arrival patterns, which are typical of agent and chat workloads but uncommon in stateless benchmarks.

## Routing strategies comparedRouting strategies compared

Every system routes requests in some way, even if only through default Kubernetes services.

In this experiment, we compared two configurations:

- 

Default Kubernetes ClusterIP routing, which distributes requests without regard to request content or model state. In practice, request placement is influenced by

client-side connection reuse and does not attempt to preserve execution locality.

- 

Cache-aware routing implemented in the inference router. For each request, the router attempts to select a replica with the best KV cache match for the request. If such a replica is overloaded, the router falls back to selecting a less-loaded replica.

This means the comparison is between a worst-case routing strategy that is unaware of both request content and cache state and a best-case strategy that combines cache awareness with basic load protection.

No standalone load-aware or least-request-only routing baseline was evaluated in this experiment.

## Three replicas: Observed impactThree replicas: Observed impact

With three vLLM replicas, the difference between routing strategies is substantial.

With cache-aware routing:

- Average inference step time: 4.8 seconds

- P90 latency: 9.6 seconds

- P95 latency: 17 seconds

Total inference time across all steps: ~93k seconds

With default Kubernetes routing:

- Average inference step time: 9.0 seconds

- P90 latency: 15.2 seconds

- P95 latency: 70.8 seconds

Total inference time across all steps: ~183k seconds

Average inference time dropped by roughly 49 percent. Total runtime dropped by about 36 percent.

Same model. Same GPUs. Same traffic. Only routing changed.

## Interpreting latency distributionsInterpreting latency distributions

Median latency differs little between configurations.

This is expected. Median values are relatively insensitive to queueing effects and cache misses.

The primary difference appears in the tail.

With default routing, P95 latency increases sharply due to repeated cold prefills and uneven load distribution across replicas. Individual slow steps propagate through agent trajectories and extend overall runtime.

With cache-aware routing, repeated prefills are avoided more often, leading to tighter latency distributions and lower tail latency.

## Scaling replicas without routing makes things worseScaling replicas without routing makes things worse

Scaling from one to three replicas without cache-aware routing does not improve performance in this workload.

Average step time increases and tail latency worsens. The primary cause is cache fragmentation: context for a given trajectory is repeatedly reconstructed on different replicas, increasing prefill cost.

This illustrates that horizontal scaling alone is insufficient for stateful inference workloads.

## What the router actually changesWhat the router actually changes

Traditional L7 load balancers can preserve affinity at the connection or client level. However, they do not inspect request content or model-specific state.

The router used in this experiment makes routing decisions based on request content and model execution state, allowing it to route requests preferentially to replicas that are more likely to reuse existing KV cache.

Its primary effect is on where related requests execute over time.

For agent-style workloads, multiple sequential requests often share large portions of context. When routing preserves locality, later steps can reuse KV cache produced by earlier ones. When locality is lost, each step pays the full prefill cost again.

In the cache-aware configuration, requests belonging to the same trajectory are more likely to be scheduled on replicas that already hold relevant context. In the default Kubernetes configuration, requests are distributed without regard to prior execution history.

This difference affects how often replicas perform expensive prefills, how decode batches form and how queueing behavior evolves under load.

## Cache behavior as the dominant factorCache behavior as the dominant factor

KV cache reuse is the primary driver behind the observed performance differences.

In this experiment, all requests share a large system prompt, so some cache reuse occurs even without cache-aware routing. However, routing strategy significantly affects how much additional context is reused across steps.

Across three replicas:

- With cache-aware routing, approximately 95 percent of tokens were served from cache.

- Without cache-aware routing, approximately 62 percent of tokens were served from cache.

This difference translates directly into reduced prefill work and lower total inference time. When cache locality is preserved, decode dominates execution for many steps. When locality is lost, repeated prefills dominate instead.

Cache behavior therefore materially affects both latency and total compute consumption for this class of workload.

## Why the single-replica case looks differentWhy the single-replica case looks different

With a single vLLM replica, routing strategy has little impact.

All requests necessarily execute on the same process, and cache locality is implicit. As a result, the performance characteristics of the single-replica setup are largely determined by model behavior and request mix rather than routing.

The role of routing becomes visible once inference is distributed. At that point, preserving locality across replicas determines whether scaling improves or degrades performance.

## The system-level takeawayThe system-level takeaway

Inference performance does not scale linearly with replica count for stateful workloads.

Once requests carry context across steps, replicas are no longer interchangeable. Routing becomes part of the execution path, not just an infrastructure concern.

Different routing strategies form a spectrum, from connection-based and round-robin approaches, to load-aware scheduling, to cache- and memory-aware routing. The results in this post show that ignoring cache locality can negate the benefits of horizontal scaling.

This is why routing decisions disproportionately affect tail latency and total runtime rather than median throughput.

### Limitations and next stepsLimitations and next steps

Cache-aware routing alone is not sufficient.

KV cache is constrained by GPU memory, and under sustained load or large contexts, eviction is unavoidable once the working set exceeds device capacity. Routing cannot prevent this on its own.

Handling these scenarios may benefit from additional signals such as memory pressure or cache eviction behavior being taken into account during routing. These aspects were not evaluated in this experiment.

We will cover cache eviction and memory-aware routing in a follow-up post.

## If this problem looks familiarIf this problem looks familiar

If you are running agent or chat workloads on open models and recognize these failure modes, this is exactly the class of system Token Factory is designed for.

We work with teams to profile real traffic, identify execution-path bottlenecks, design serving stacks that hold under worst-case inputs and tune models and inference pipelines together rather than in isolation.

You can explore Token Factory at tokenfactory.nebius.com, or reach out if you want to walk through your workload and see how these architectural choices apply to it.

We are not trying to make benchmarks look better, we are trying to make systems behave predictably when users show up.

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

TLDR

- 

Routing once inference becomes distributed

- 

Workload and experiment setup

- 

Routing strategies compared

- 

Three replicas: Observed impact

- 

Interpreting latency distributions

- 

Scaling replicas without routing makes things worse

- 

What the router actually changes

- 

Cache behavior as the dominant factor

- 

Why the single-replica case looks different

- 

The system-level takeaway

- Limitations and next steps

- 

If this problem looks familiar

## See also

### 

Why large MoE models break latency budgets and what speculative decoding changes in production systems

Large mixture-of-experts language models promise significant gains in model quality, but deploying them in real products often exposes hard latency limits. This article explains why MoE systems that look efficient in benchmarks struggle under production constraints, and how architectural decisions around routing, batching and serving determine whether latency budgets hold under worst-case inputs and real user behavior.

January 14, 2026
9 mins to read

### 

NVIDIA Nemotron Nano 2 VL in Nebius AI Studio: powering agentic multimodal AI

We’re pleased to announce that Nebius AI Studio now hosts NVIDIA Nemotron Nano 2 VL, a compact, production-ready multimodal reasoning model engineered for real-world document intelligence and video understanding.

October 28, 2025
3 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
