# Train the draft model for your workload

Source: https://nebius.com/blog/posts/train-the-draft-model-for-your-workload

Skip to main content

## Train the draft model for your workloadTrain the draft model for your workload

Speculative decoding is usually introduced as a throughput trick: run a small, fast draft model ahead of the large one, verify its guesses in parallel, and watch tokens per second climb. That framing undersells what it actually does in production. In real systems, speculative decoding reshapes the execution path that decides whether p90 and p99 latency stay predictable under load.

Which is why the draft model matters more than most teams realize.

A generic draft model is tuned for average traffic. It doesn’t know that your users write code in Go, or that your agent repeatedly asks for structured JSON, or that your copilot spends most of its day completing the same four or five prompt shapes. On recurring, domain-specific workloads, a generic drafter plateaus, and the gap between benchmark performance and production behavior becomes the thing your SLOs absorb.

Today we are launching Custom Speculator Training in Nebius Token Factory. Teams can train workload-specific draft models from their own data, then deploy them inside the same platform that serves the base model.

## Why generic speculators plateauWhy generic speculators plateau

Speculative decoding works by having the draft model propose tokens that the target model verifies. The more often proposals are accepted, the larger the throughput and latency win. Acceptance rate is workload-dependent: a drafter trained on general instruction data can only approximate the distribution your product actually generates.

For narrow, high-volume workloads (code assistants, enterprise copilots, structured-output agents, chat with repeated prompt shapes) that approximation leaves real performance on the table. A drafter trained on the traffic you serve narrows that gap.

The goal is not a better benchmark number. The goal is a more predictable execution path.

## What you can do with Custom Speculator TrainingWhat you can do with Custom Speculator Training

Inside Token Factory, the workflow is one loop.

- 

Bring your training data. Use Data Lab to attach S3-compatible files in place, query production logs, and merge them with synthetic seed datasets. Or upload a curated JSONL file directly through the Post-training console or the Files API. For the launch set of models, we are providing synthetic datasets to 6 leading OS frontier models for free to accelerate your training, so teams can start training even when their own logs alone are not enough.

- 

Train the drafter. Pick the target base model, point the training job at your prepared dataset, run a job from the Post-training page. Preset hyperparameters cover the common case. For advanced users, full hyperparameter control is exposed (decoding heads, loss type, learning rate, scheduler, drafter type) without making that complexity the default. Training uses the same Post-training pipeline that already runs supervised fine-tuning on Papyrax, our distributed training framework.

- 

Deploy alongside the base model. The trained drafter lands in Custom Weights. From there, it attaches to a Dedicated Endpoint with the base model and serves real traffic. At launch, deployment is reviewed by our solutions engineers, so teams get a human-in-the-loop check before a custom drafter sees production load.

- 

Measure on the workload that matters. Acceptance rate, tokens per second, end-to-end latency, all visible alongside the rest of your serving metrics. If the workload changes materially, retrain.

The June 25, 2026 launch covers the API and UI, Eagle 3 and our Nebius-optimized Eagle 3 architectures, and the current supported model set configured in Papyrax. Jobs start from the Post-training page. Data preparation rides on Data Lab, which has been live since May.

The same launch package also points toward broader support over time. Public model-support claims stay tied to the approved launch set rather than implying universal arbitrary-model coverage on day one.

## Built on a platform already runningBuilt on a platform already running

Custom Speculator Training isn’t a standalone feature. It plugs into rails that have been settling into production for months. Post-training has been live since December 2025. Data Lab shipped in mid-May with S3 import in place and the dataset merge workflow. RL Platform v1 entered private preview a few days later. Custom Speculator is the moment the loop closes: customers now shape both model behavior and serving behavior on their own data, in one platform.

## Built on research we ship in the openBuilt on research we ship in the open

Our research team has published LK Losses, a novel loss function that directly optimizes draft-token acceptance rate rather than proxying it through KL divergence, along with the LK-Speculators model family on Hugging Face and a public contribution to SpecForge. Across models from 8B to 685B parameters, LK Losses show consistent improvements in acceptance rate over KL-trained baselines.

The research is starting to shape the broader open ecosystem too. The vLLM project recently picked up an upstream change inspired by the LK Losses analysis of probabilistic rejection sampling, fixing how draft proposal probabilities flow through the verification path. The work that powers Custom Speculator Training is the work the open community is now building on.

That research is what Custom Speculator Training productizes. The open artifacts stay open. The training pipeline, the data tooling, and the deployment path are what Token Factory adds on top.

## What this changes in productionWhat this changes in production

Better throughput on recurring workloads. Speculative decoding performs best when the drafter and target agree often. A drafter trained on the distribution your product actually serves raises that agreement rate where it matters.

More stable latency under load. Acceptance rate is about predictability as much as speed. A workload-matched drafter tightens the gap between median and tail latency on the traffic your system sees every day.

Better unit economics as volume scales. Faster serving reduces GPU-seconds per request. That matters most where it always matters most: at the point where a product graduates from successful pilot to expensive steady state.

Serving behavior you control. Public APIs do not let you train the fast path. When your drafter is trained on your data, the part of the stack that most affects how your product feels is no longer commodity.

Control surfaces that match the team. For most teams, preset hyperparameters are the right starting point. For the teams who want to tune (decoding heads, loss type, learning rate, scheduler, drafter architecture), the control is there without being in the way.

## Who this is forWho this is for

This launch is built for teams that already have production traffic and care about how it performs:

- 

ML and platform engineers running open-source models behind real products: copilots, agents, coding tools, enterprise chat, reasoning systems.

- 

AI product teams whose workload is concentrated enough that a workload-specific drafter can plausibly outperform a generic one.

- 

Enterprise accounts already using generic speculative decoding on Token Factory who have hit the ceiling of what a general drafter can do on their traffic.

If you are still shipping a first prototype on highly variable traffic, a generic drafter is the right starting point. Come back when you have repeatable workload patterns and a performance target worth chasing.

## How to get startedHow to get started

Custom Speculator Training goes live on June 25. If you are a current Token Factory customer with a production workload and a concrete performance goal, talk to your solutions engineer. We will help you scope the dataset, run the first training job, and review the deployment before it starts serving.

If you are new to Token Factory, start with a Dedicated Endpoint on the base model, gather traffic, then come back to train the drafter once you have enough signal.

The real question in production is no longer whether speculative decoding exists. It is whether the draft model is shaped for the traffic you actually serve. Custom Speculator Training is how you do that inside Token Factory.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Dylan Bristot
Product Marketing, Token Factory

Contents

- Train the draft model for your workload

- Why generic speculators plateau

- What you can do with Custom Speculator Training

- Built on a platform already running

- Built on research we ship in the open

- What this changes in production

- Who this is for

- How to get started

## See also

### 

Nebius AI Cloud “Aether 3.6”: Operating production AI with more control, efficiency, and confidence

Introducing Aether 3.6. Our latest quarterly platform release responds to how AI teams now operate at scale and with maturity, delivering a smoother developer experience, a stronger security and compliance foundation, advances across our in-house storage portfolio, and natural-language control over your AI cloud.

June 24, 2026
14 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

### 

NVIDIA Nemotron 3 Super now available on Nebius Token Factory

NVIDIA Nemotron 3 Super is now available on Nebius Token Factory, bringing a 120B hybrid MoE model optimized for multi-agent systems and complex reasoning workflows to production deployments. With long-context inference and OpenAI-compatible APIs, teams can run Nemotron 3 Super through dedicated GPU endpoints and autoscaling infrastructure without managing their own serving stack.

March 11, 2026
4 mins to read

Sign in to save this post
Sign In
