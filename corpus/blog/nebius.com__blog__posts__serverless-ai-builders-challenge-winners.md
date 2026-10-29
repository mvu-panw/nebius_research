# Serverless AI Builders Challenge | Nebius

Source: https://nebius.com/blog/posts/serverless-ai-builders-challenge-winners

Skip to main content

The Nebius Serverless AI Builders Challenge results are in, and the community delivered. In total, 35 projects qualified across AI & ML, Scientific AI & Healthcare, and robotics. We invited builders to create something real with Nebius Serverless AI using Serverless AI Jobs, Serverless AI Endpoints, or both. Every entry shipped its code in a public repo and explained the approach in a technical blog post.

A panel of domain experts and Nebius engineers reviewed every valid submission across six criteria: technical implementation, reproducibility, educational content quality, product usage depth, real-world usefulness, and originality. Here’s what won.

## The winnersThe winners

First place went to Shmulik Avraham’s MediSimplifier, which fine-tunes 7–8B models with LoRA to simplify hospital discharge summaries without dropping a clinical fact. Discharge papers are written at a college reading level that most patients can’t parse, and misunderstood instructions drive avoidable hospital readmissions. MediSimplifier rewrites them in plain language. Serverless AI let him run the entire research project without reserving a single GPU, and he noted an H100 was available immediately every time he submitted a single-GPU job. He ran seven ablation jobs in parallel (20 minutes instead of three hours sequentially), served the winning model on a Serverless AI Endpoint, and paid $320 in actual billing for everything, failed jobs included. He didn’t expect to find that two cross-family LLM judges scoring identical outputs showed near-random agreement (Cohen’s κ = 0.11), or that chain-of-thought prompting amplified the disagreement instead of reducing it, so he now recommends at least two cross-family judges for any LLM-as-judge evaluation at scale.

Second place went to Andrei Goldenberg’s evaluation dashboard, which benchmarks up to three models on your own data across quality, latency, and cost. Public leaderboards rank models on generic benchmarks that never saw your prompts, and teams that ship the headline leader often pay a premium for quality their task doesn’t need, so testing on your own task is the difference between guessing and knowing. The dashboard mixes hosted Nebius Token Factory models with self-hosted vLLM Serverless AI Endpoints in a single leaderboard and splits the deploy cost from the eval cost, so the comparison stays honest and the only thing he brings is his own data. Serverless made each test disposable. The harness spins up a GPU endpoint, runs the eval, and tears it down, which means he paid for minutes of GPU time per comparison instead of renting a box that idles between tests. Two findings fell out. Self-hosting only wins on cost at high utilization, and reasoning models silently score 0% on correct answers unless you strip their <think> blocks before parsing.

Third place went to Zaher Khateeb’s Balagan, a chaos-engineering harness that injects faults into multi-agent systems, including one agent covertly instructed to lie, and measures what happens to the quality of their collective decisions. Companies increasingly wire several AI agents together to make decisions that matter, and a single crashed or compromised agent can quietly corrupt the outcome, so Balagan works like a fire drill that finds the weak point before production traffic does. The workload fit serverless exactly. He needed 225 short, independent trials run once, so a Serverless AI Endpoint kept the GPU alive only while the model served and a CPU-only Serverless AI Job ran the orchestration for cents, and Object Storage carried the checkpoints for under a cent, on one platform and one bill. He killed the sweep mid-run to prove it and the resubmitted job picked up where it stopped. The sweep finished in 63 seconds against a single NVIDIA L40S, and his entire measured bill, a second full sweep and several kill-and-recover demos included, came to $3.64. The heatmap showed that fault type matters more than fault count. Flat majority voting survived both a crashed agent and a live saboteur at 100% accuracy, but at roughly 2.8× the tokens of a hierarchy, which lost one trial in five to a dead aggregator.

The top three places and seven special awards go to the following builders and teams.

 | Place
 | Winner or team
 | Submission Blog Post
 | GitHub Repo

 | 1st
 | Shmulik Avraham
 | Medical text simplification with LoRA
 | https://github.com/deepset01-sys/medisimplifier-nebius

 | 2ns
 | Andrei Goldenberg
 | The best model on the leaderboard isn’t always the best model for you
 | https://github.com/goldandrei/Nebius-Serverless

 | 3rd
 | Zaher Khateeb
 | I paid an LLM to sabotage my multi-agent system on purpose
 | https://github.com/zahere/balagan

 | Special Award — AI & ML
 | Piotr Janik
 | From git push to fine-tuned model in production
 | github.com/piotrjanik/nebius-actions

 | Special Award — HCLS
 | Christofer Harry, Dmitry Sadchikov (Team Lity)
 | Serverless document recognition: KYC for a legal copilot
 | https://github.com/dsadchikov/docs-proc-nebius

 | Special Award — Robotics
 | David Cox
 | Soft surface picking
 | https://github.com/robotcompanyDave/rc-nebius-challenge-2026-public

 | Special Award — Agents
 | Efthymios Fousekis
 | Building Archon: from financial documents to controlled records
 | https://github.com/upgradedev/archon_nebius

 | Special Award — Best Student Work
 | Diego Mariano
 | Clinical AI proves its robustness — it shouldn’t have
 | https://github.com/diegom4riano/nebius-fmri-adversarial

 | Special Award — Best CPU Example
 | Andrei Parfenov
 | A grounded LLM planner for swim trainings
 | https://github.com/andreiparfenov/swimming-coach-serverless

 | Special Award — Community Choice
 | To be voted on at the Serverless AI office hours on August 25. Join us and cast your vote!
 | —
 | —

Another 20 builders and teams took home the Awesome Serverless Award. See the full list of winning projects for every repo and post.

## Explore the projectsExplore the projects

Congratulations to the winners and thank you to everyone who submitted. Every winning project is fully public, so you can read the approach, clone the code, and run it yourself. The Community Choice award is still open. Register for the Serverless AI office hours on Tuesday, August 25 to see the winners’ showcase live and cast your vote.

Try Nebius Serverless AI and run your first Job or Endpoint in minutes.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- The winners

- Explore the projects

## See also

### 

Introducing DevPods, Jobs and Endpoints: Easy compute access with serverless AI

The serverless services at Nebius are a natural extension of how an AI infrastructure cloud evolves over time, building on a mature and well-established underlying platform. As the platform develops, it becomes possible to expose compute in more flexible and elastic forms that better match how AI workloads are consumed.

March 26, 2026
12 mins to read

### 

Game on! UFB and Nebius power the future of robotics

We are thrilled to announce that Nebius is the official technology partner for Season 1 of Ultimate Fighting Bots (UFB)’s Humanoid Sports League — the world’s first multi-format competition platform for physical AI. The two companies will pioneer the use robots by coupling UFB’s growing platform for humanoids with Nebius’s cloud solution for physical AI.

May 13, 2026
9 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

Sign in to save this post
Sign In
