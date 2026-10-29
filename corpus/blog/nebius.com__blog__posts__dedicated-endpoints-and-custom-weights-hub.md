# Dedicated Endpoints and Custom Weights Hub: control your production AI stack

Source: https://nebius.com/blog/posts/dedicated-endpoints-and-custom-weights-hub

Skip to main content

## TL;DRTL;DR

Choose your GPU type, define GPUs per replica, set scaling limits, select region and deploy your own model weights to isolated endpoints.

Turn deployment into a defined, controllable part of your production architecture in Nebius Token Factory.

## From model selection to system designFrom model selection to system design

Most AI teams start with the model.

Which model performs best. How to fine-tune it. How to improve quality on domain-specific tasks.

That focus makes sense early on. But once traffic grows and real users depend on your system, the model stops being the only variable. Infrastructure begins to shape user experience, reliability, compliance posture and margins just as much as model quality.

Latency variance affects retention. Scaling behavior affects cost predictability. Deployment region affects regulatory approval.

At that point, you are no longer selecting a model. You are designing a system for production scale.

## Make infrastructure a decision, not a defaultMake infrastructure a decision, not a default

Token Factory now supports Dedicated Endpoints with granular deployment control.

A dedicated endpoint is an isolated deployment of a supported model template, created and managed through a control plane API. You define:

- Region, which determines data residency and latency

- GPU type and number of GPUs per replica

- Minimum and maximum replicas for autoscaling

- Lifecycle operations such as update, enable, disable and delete

Inference runs through OpenAI-compatible APIs using a dedicated routing key tied to your endpoint.

This solves a specific production problem: shared infrastructure hides critical variables. Hardware profile, scaling behavior and routing locality are opaque. That may be acceptable for experimentation. It becomes limiting at scale.

For vertical AI companies, this shows up as tail latency volatility and unpredictable unit economics. For ML platform teams, it shows up in architecture reviews and compliance constraints. For enterprise buyers, it shows up in audit requirements and data residency controls.

Granular deployment control replaces that opacity with defined parameters.

Hardware selection becomes deliberate. Scaling boundaries are explicit. Region is enforced at configuration level.

For example, a team deploying a 70B model can choose H100 GPUs, allocate 2 GPUs per replica, set min_replicas to 2 for guaranteed baseline capacity and cap max_replicas at 8 to bound peak cost. That configuration defines latency headroom and cost exposure before the first request is served.

## Unify training and deploymentUnify training and deployment

Dedicated Endpoints solve one half of the production problem: infrastructure determinism.

You can define hardware, scaling boundaries and regional isolation. You can bound latency and cost before traffic arrives.

But production systems do not stay static.

Models evolve. Prompts change. Traffic shifts. Quality regressions appear under load. Teams fine-tune, distill, recalibrate and iterate.

If training and deployment live in separate systems, iteration becomes friction:

- Checkpoints are exported manually

- Environments drift

- Glue code accumulates

- Serving pipelines are updated out of band

This is where the Custom Weights Hub comes in.

The Custom Weights Hub connects post-training directly to Dedicated Endpoints.

Fine-tuned or distilled checkpoints can be deployed to an existing endpoint without switching tools or environments. The same endpoint can later be updated with a new checkpoint as iteration continues.

Instead of a fragmented workflow:

- Inference logs inform training

- Training produces new checkpoints

- Deployment configuration defines how those checkpoints behave under load.

Dedicated endpoints are managed through a control plane API. Inference runs through region-specific data plane endpoints. Lifecycle operations and traffic execution scale independently.

This separation allows teams to iterate on models without destabilizing serving infrastructure.

The result is not just deployment control. It is a continuous loop from data to post-training to deterministic production.

All of this runs on Nebius AI Cloud, on dedicated NVIDIA GPU clusters in data centers we own and operate across Europe and the US. Customers already run workloads producing hundreds of billions of tokens per day on this infrastructure. With this release, that scale becomes configurable rather than assumed.

## Operating what you defineOperating what you define

Control is only useful if you can see its effects.

Inference Observability provides real-time and historical metrics across:

- End-to-end latency and percentiles (p50, p90, p99)

- Time to first token

- Token throughput

- Active replicas and scaling behavior

- Error rates by status code

- Traffic patterns by prompt size and region

This allows teams to answer practical engineering questions:

When did latency increase? Was it scaling or queueing? Are errors coming from client traffic or infrastructure? Is KV-cache reuse improving tail behavior?

Control without visibility is guesswork. Deployment plus observability is engineering.

This is not Kubernetes exposed in a UI. It is not generic cloud compute. You do not manage clusters, we do.

What you control are the parameters that define how your AI system behaves in production: hardware profile, scaling limits, regional boundaries and model weights. That distinction matters.

## From improving models to engineering systemsFrom improving models to engineering systems

Open models are powerful starting points. Fine-tuning improves alignment. Optimization improves efficiency.

Durable advantage comes from engineering the full system around your product.

With Dedicated Endpoints and the Custom Weights Hub, Token Factory makes deployment a first-class part of that system.

Data shapes the model. Post-training stabilizes it. Deployment configuration defines how it behaves under load.

All inside one platform, on infrastructure we own and operate.

If you are building production AI and need deployment you can define rather than inherit, reach out to us.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Dylan Bristot
Product Marketing, Token Factory

Contents

- TL;DR

- From model selection to system design

- Make infrastructure a decision, not a default

- Unify training and deployment

- Operating what you define

- From improving models to engineering systems

## See also

### 

Routing in LLM inference is the difference between scaling and stalling

When inference becomes distributed, routing strategy can determine whether a system scales or stalls. In this article, we examine a real agent-style workload where cache-aware routing in vLLM reduced average step time by nearly 50 percent and cut P95 latency from over a minute to under 20 seconds — with the same model, hardware and traffic.

February 17, 2026
6 mins to read

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
