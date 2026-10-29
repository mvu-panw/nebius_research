# Nebius Token Factory Becomes First AI Cloud to Adopt NVIDIA Groq 3 LPX

Source: https://nebius.com/blog/posts/nvidia-groq-3-lpx-nebius-token-factory

Skip to main content

Nebius is the first AI cloud to adopt NVIDIA Groq 3 LPX, boosting inference token generation for NVIDIA Vera Rubin NVL72 in Nebius Token Factory. NVIDIA Groq 3 LPX is purpose-built for extremely fast token generation, which is the rate at which tokens are produced and value is realized for an individual user or agent. An extension of the NVIDIA Vera Rubin platform and in conjunction with Token Factory production inference platform, Groq 3 LPX gives developers a major boost in inference performance for agentic use cases where speed and responsiveness matter.

## Production agentic workloads are changing inference requirementsProduction agentic workloads are changing inference requirements

Inference has two distinct jobs: context and generation. Context involves ingesting long prompts, large codebases, and persistent multi-turn agent state. Generation produces the tokens a user or agent actually sees and acts on.

An agent can make dozens of sequential model calls to complete a single task. Each step depends on the one before it, so latency compounds across the entire workflow. As a result, the speed of generation increasingly determines how quickly an agent can get useful work done.

NVIDIA Groq 3 LPX is purpose-built for long-context, low-latency performance. Each NVIDIA LPX rack couples 256 LPU accelerators with 128 GB of on-chip SRAM and 640 TB/s of scale-up bandwidth, fully liquid-cooled using the NVIDIA MGX rack architecture.

## Fastest Gemma 4 31B inference performance ever recordedFastest Gemma 4 31B inference performance ever recorded

Artificial Analysis benchmarked NVIDIA Groq 3 LPX running Gemma 4 31B at 3,400 output tokens per second for a single user, the fastest performance ever recorded for that model. With NVIDIA Vera Rubin NVL72, NVIDIA projects up to 35x higher inference throughput per megawatt for 2T-parameter models at long-context and low-latency than GB200 NVL72, a measure of what extreme codesign unlocks at agentic-scale token volume.

## Faster generation, no re-architectureFaster generation, no re-architecture

Token Factory provides production inference across leading open models, with serverless and dedicated endpoints, autoscaling, observability, function calling, structured outputs, and the infrastructure required to operate models at scale.

A fast token means very little if getting it requires re-architecting a stack for new silicon. Nebius’s approach is the opposite: NVIDIA Vera Rubin NVL72 and Groq 3 LPX will run on the same Token Factory platform developers are already running at scale, initially supporting a subset of models alongside familiar features like autoscaling, and observability.

## Developers get speed, scale, and lowest token costDevelopers get speed, scale, and lowest token cost

Token Factory already ships the pieces multi-agent systems depend on: native function calling, structured JSON outputs, and built-in safety guardrails for tool-calling agents, on top of dedicated endpoints with sub-second latency targets. With NVIDIA Groq 3 LPX on that same platform, developers building multi-agent pipelines, real-time coding assistants, and latency-sensitive reasoning applications get faster generation the same way they call every other Token Factory endpoint today: same platform, same operating model, faster tokens where the workload demands it.

## Get started on Token FactoryGet started on Token Factory

For teams already running production traffic on Token Factory, adding NVIDIA Groq 3 LPX to a latency-sensitive workload is a model-selection change, not a migration: no new SDK, no new vendor relationship, no new billing setup.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- Production agentic workloads are changing inference requirements

- Fastest Gemma 4 31B inference performance ever recorded

- Faster generation, no re-architecture

- Developers get speed, scale, and lowest token cost

- Get started on Token Factory

## See also

### 

Nebius achieves NVIDIA Exemplar Cloud on NVIDIA GB300 for training: Validated performance for hyperscale AI

Nebius has achieved NVIDIA Exemplar Cloud status on NVIDIA GB300 NVL72 for training, meeting the 95% performance threshold across NVIDIA’s reference benchmarking recipes. In this post, we explain what this validation means in practice and how it fits into Nebius’s broader work with NVIDIA on building production-grade AI infrastructure.

April 29, 2026
6 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

### 

NVIDIA retail AI blueprints, now running on Nebius

Nebius has collaborated with NVIDIA to bring two retail AI blueprints to production on Nebius infrastructure: the NVIDIA Agentic Commerce Blueprint and the NVIDIA Retail Catalog Enrichment Blueprint for automated product content. Both are open-source reference architectures built on NVIDIA NIMs that retailers and developers can customize and deploy today with a 1-click deployment on Nebius AI Cloud.

June 5, 2026
5 mins to read

Sign in to save this post
Sign In
