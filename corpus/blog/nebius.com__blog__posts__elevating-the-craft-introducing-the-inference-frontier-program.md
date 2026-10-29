# Elevating the craft: Introducing the Inference Frontier Program

Source: https://nebius.com/blog/posts/elevating-the-craft-introducing-the-inference-frontier-program

Skip to main content

## Introducing the Inference Frontier ProgramIntroducing the Inference Frontier Program

While most major advances in AI begin with a breakthrough in training, the real test is what happens when those models have to face the real world — for example, the constraints of bursty traffic, KV cache budgets, batching and queueing tradeoffs, routing, multi-tenant isolation and cost per token. Most teams are solving these exact problems in parallel, yet the useful details rarely get shared. To share the learnings of the engineers and builders doing this critical work, we’re excited to introduce the Inference Frontier Program today, timed alongside our Nebius.Build SF event.

The Inference Frontier Program is a new builder-to-builder initiative to share what’s working in production inference: the wins, tradeoffs and real inference optimizations from teams pushing the frontier. We want to surface concrete architectures, complete with proof points and before-and-after results, no matter where you run. Running throughout 2026, the program exists to recognize these builders and their systems. Starting today, submissions are officially open.

## The inference bottleneckThe inference bottleneck

As AI transitions from experimental sandboxes to real-world applications, the bottleneck is no longer model selection — it’s the systems engineering required to run these models reliably and affordably at scale. You are not just proving the model can run; you are making it run fast, stable and cheap under real traffic.

Inference isn’t just training in reverse. It introduces an entirely different set of compounding complexities. Think about it in layers:

- 

The engine (runtime optimization): This is where you win or lose performance. Prefill and decode have different bottlenecks, so builders lean on knobs like batching, KV or prefix caching, quantization, speculative decoding and the right parallelism for your workload.

- 

The fleet (systems at scale): Even a perfect engine fails if the fleet is run poorly. This is routing and placement, queueing policy, capacity planning, multi-node serving and multi-tenant isolation so one noisy neighbor does not impact everyone’s performance. This is where bursty traffic, context length variability and uneven decode lengths turn into tail latency spikes unless you control scheduling and admission.

- 

Production reality (ops, safety, economics): This is what keeps an app or agent running smoothly and reliably over time: observability that explains where latency went, evals, safety and policy checks that avoid latency cliffs and unit economics that work at scale.

The Inference Frontier Program exists to recognize the builders doing this quiet work and surface their architectural patterns so the ecosystem can advance faster. We want to reward systems, not slogans, and share the learnings of the people building things that actually run.

## What is the Inference Frontier Program?What is the Inference Frontier Program?

This is an ecosystem initiative, meaning it’s entirely infrastructure-agnostic. Great work counts regardless of whether you’re running on Nebius, a hyperscaler, a neocloud or your own metal.

Our core goals are twofold:

- To drive builder-to-builder learnings by sharing and recognizing the work of standout teams and individuals;

- To create a community of builders running inference in production.

To capture the full spectrum of innovation across this community, builders of all kinds — from solo builders, open source maintainers and established ISVs to enterprise platform teams and researchers — are invited to share their real-world inference optimizations and participate. Whether you’re running a single agent or engineered a full-scale platform, no contribution is too small.

## The judges & our founding buildersThe judges & our founding builders

To make sure we’re evaluating technical craft, we’ve put together a judging panel of operators, researchers and ecosystem voices who know what good inference looks like. Our bench includes:

- George Cameron (Co-Founder, Artificial Analysis)

- Professor Song Han (Associate Professor, MIT EECS; Distinguished Scientist, NVIDIA)

- Braden Hancock (AI Researcher, Laude Institute)

- Ryan Hanrui Wang (Co-Founder and CEO, Eigen AI)

- Ujval Kapasi (VP, AI & HPC Frameworks and Libraries, NVIDIA)

- Olga Megorskaya (CEO, Toloka)

- Simon Mo (CEO & Co-Founder, Inferact; Lead, VLLM)

- Dylan Patel (Founder, Semi Analysis)

- Laurelle Roseman (VP of Global Partnerships, Nebius)

- Danila Shtan (CTO, Nebius)

We’re also kicking things off with an initial cohort of incredible teams who have already stepped up to share what they’ve learned. At launch, we’re thrilled to feature the engineering teams behind FlowGPT, Revolut and Monday.com in our first technical deep dives.

## How it worksHow it works

The Inference Frontier Program is an ongoing initiative throughout the year.

- 

The Cadence: Nominations are always open. We’ll publish new technical deep dives on a rolling basis, aiming to feature 1-2 teams per month.

- 

The Deep Dive: If selected, we’ll publish a technical breakdown of what you shipped, what novel techniques you used and the measurable before-and-after proof of how you pulled it off.

- 

The Perks: We want to ensure you get real value out of sharing your work. Featured teams receive:

- Distribution of your work across Nebius and partner channels to reach other practitioners.

- Invitations to share your insights at builder talks, meetups and partner events.

- Access to a peer network of inference builders to exchange ideas and challenges.

- A direct feedback loop with Nebius product and engineering to influence product features and solve real problems.

- End-of-year finals recognition to highlight standout contributions.

(And a quick note on sharing your work: We know your internal metrics might be highly sensitive. Ranges, deltas and anonymized proof points are totally fine. We care about the technical lessons, not getting you in trouble with your boss or legal team!)

## Show us what you’re buildingShow us what you’re building

Submissions are officially open!

- 

Apply for yourself or your team: If you recently shipped an architectural change that crushed your latency or slashed your cost-per-token, we want to hear exactly how you did it.

- 

Nominate a peer: Know a solo dev, open-source maintainer or an infrastructure team doing massive things quietly? Drop their name.

Apply or Nominate for the Inference Frontier Program here.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Waqas Makhdum
Vice President of Developer Relations & Community

Contents

- Introducing the Inference Frontier Program

- The inference bottleneck

- What is the Inference Frontier Program?

- The judges & our founding builders

- How it works

- Show us what you’re building

## See also

### 

Supercharging startups: Nebius accelerates AI-native innovation with NVIDIA

Nebius AI Cloud is collaborating with NVIDIA Inception, a leading program for AI startups with over 22,000 members, to accelerate AI startup innovation. Nebius’ AI Lift program — announced at NVIDIA GTC 2025 — offers eligible NVIDIA Inception members up to $150,000 in cloud credits, access to AI technical expertise and support and a range of other exclusive benefits.

April 9, 2025
3 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

NVIDIA Nemotron 3 Super now available on Nebius Token Factory

NVIDIA Nemotron 3 Super is now available on Nebius Token Factory, bringing a 120B hybrid MoE model optimized for multi-agent systems and complex reasoning workflows to production deployments. With long-context inference and OpenAI-compatible APIs, teams can run Nemotron 3 Super through dedicated GPU endpoints and autoscaling infrastructure without managing their own serving stack.

March 11, 2026
4 mins to read

Sign in to save this post
Sign In
