# Fine-tuning, RL, or distillation? How to choose a post-training method

Source: https://nebius.com/blog/posts/post-training-open-weight-models

Skip to main content

The right post-training method depends on the learning signal you can produce. An open-weight model may perform well on general benchmarks and still return the wrong schema, confuse two customer records, or choose the wrong tool in your application. Post-training adapts the model to those tasks using examples, preferences, scored attempts, or feedback from a teacher model. The test is whether the adapted checkpoint meets your quality, latency, and cost targets on held-out work.

On Nebius, teams can bring their own trainers, frameworks, and evaluation harnesses to Nebius AI Cloud, or use Nebius Token Factory for managed fine-tuning of supported open models.

## TL;DRTL;DR

- Start with a baseline on real tasks, then use failures and feedback to guide each training round.

- Choose the method for the behavior you need to change. SFT, preference tuning, RL, and distillation are options, not a required sequence.

- Bring your own post-training workflow to Nebius AI Cloud, or use Token Factory for a managed starting point.

## Define the task and baselineDefine the task and baseline

Access to open weights lets you adapt a model to your data and workflows, compare checkpoints, and choose how to serve the result, subject to the model’s license. You can decide which parts of the training and serving workflow to run yourself and which to have managed.

Before choosing a method, define the failure you want to fix and evaluate the starting checkpoint on held-out tasks. Track task quality alongside latency and cost. A model that succeeds more often may reduce retries and manual review; a smaller model may meet the same quality bar with less serving compute. Measure those gains against your baseline.

## From production data to the next checkpointFrom production data to the next checkpoint

Use the baseline’s failures to decide what data to collect. Logs, traces, outcomes, and expert feedback can become training examples and new test cases. After each adaptation, compare the new checkpoint with the baseline on held-out tasks, check for regressions, and decide whether it is ready to serve. Usage and failures from the deployed model inform the next round (Figure 1).

Figure 1. A repeatable post-training loop: collect task data, adapt the model, evaluate against the baseline, deploy if it passes, and use production feedback to guide the next round.

## Choosing a post-training methodChoosing a post-training method

Match the method to the feedback you can collect reliably:

- SFT: Use when you have, or can generate, examples of the desired behavior.

- Preference tuning: Use when people can rank responses.

- RL: Use when a verifier can score task attempts.

- On-policy distillation (OPD): Use when a teacher model can grade the student’s own attempts.

Figure 2. Choose a method for the learning signal you can produce: demonstrations, ranked responses, scored attempts, or teacher feedback. These methods can also be combined; they are not a required sequence.

### Supervised fine-tuning (SFT)Supervised fine-tuning (SFT)

Supervised fine-tuning (SFT) teaches a model from examples of the desired behavior. The work includes selecting, cleaning, and balancing useful demonstrations, then testing whether the model learned the task rather than memorizing the training set. For agents, high-quality tool results and trajectories can become demonstrations too.

For a managed starting point, sign up for Nebius Token Factory.

NVIDIA used Tavily, now part of Nebius, to supply live web results while generating approximately 80,000 research trajectories. After filtering, approximately 67,000 became SFT data for NVIDIA Nemotron 3 Super. NVIDIA ran the training.

For a telecom customer, Plurai used Nebius Token Factory to fine-tune Qwen3-4B for entity resolution. In Plurai’s evaluation, resolved accuracy rose from 69% in the customer’s production setting to 89%, while latency fell from 1.0 to 0.15 seconds per request and estimated cost was reduced from $2.87 to $0.076 per 1,000 requests.

### Preference tuningPreference tuning

When a team can compare stronger and weaker responses, preference tuning can teach the model which response to favor. Methods such as direct preference optimization (DPO) are useful when quality is easier to judge by comparison than to express as a single correct answer.

### Reinforcement learning (RL)Reinforcement learning (RL)

Inside the broader post-training cycle, reinforcement learning (RL) runs its own loop: the model attempts a task, a verifier scores the outcome, and the trainer uses that feedback to update the model.

For an agent, an attempt might involve searching a repository, fetching web results with Tavily, running code in a sandbox, or calling other tools provided by the environment. A rollout fleet produces many such attempts. Their outcomes guide training, while collection speed determines how quickly the team can iterate.

Our engineering post, In agentic RL, faster tokens are not enough, explains why routing, environments, and slow trajectories matter alongside token generation. In a Terminal-Bench-based experiment, changes to the rollout system reduced the time to collect a fixed batch of 256 trajectories by 66.9%. That figure measures batch collection, not the full training run.

A Toloka study shows what successive stages can contribute. On 374 held-out simulated enterprise tasks, Toloka reports that a Qwen3.5-4B model’s task success rose from 6.2% to 49.7% after SFT on successful agent traces, then to 70.8% after RL against verifiable environments. The experiment is an early result from a Nebius ecosystem partner.

### Full fine-tuning or LoRAFull fine-tuning or LoRA

Teams choose how much of a model to update. Full fine-tuning changes the model’s existing weights; parameter-efficient methods such as LoRA train a smaller set of added weights. That choice affects the compute needed for an iteration and the artifact a team ultimately serves.

### DistillationDistillation

Distillation transfers behavior from a stronger teacher model to a student. The two approaches below differ in whose attempts the student learns from (Figure 3).

Figure 3. Two distillation paths. Fixed-example distillation trains on teacher-generated data; on-policy distillation trains on feedback about the student’s own attempts. Either path can lead to evaluation and deployment or further training.

- Fixed examples. The teacher, either an RL-trained model or a base model, writes the training data: answers, reasoning traces, or output probabilities. A team curates that data and trains the student on it with SFT. This is the off-policy route. For example, DeepSeek fine-tuned smaller Qwen and Llama models on roughly 800,000 samples curated with DeepSeek-R1.

- On-policy distillation (OPD). The student attempts the task itself, and the teacher scores those attempts token by token. The student learns from feedback on its own outputs rather than from the teacher’s demonstrations.

After either distillation approach, a team can deploy the student or continue training with SFT, preference optimization, or RL. Distillation is not a required final step after RL. The release decision still rests on held-out task quality, latency, and total cost: a smaller model offers little benefit if lost accuracy creates more retries or manual review. When the teacher is a third-party model, its license and output-use terms also govern what training data can be made from it.

## Post-training workloads on NebiusPost-training workloads on Nebius

These teams used Nebius GPU clusters for four different needs: scientific specialization, an RL workflow, task-specific precision and latency, and distributed training at scale.

- The CRISPR-GPT team at Stanford and its collaborators used Nebius AI Cloud to experiment with fine-tuning approaches and train a specialized CRISPR-Llama3 model. They built a 288-case evaluation suite for the scientific tasks it needs to perform.

- Slingshot AI runs training, fine-tuning, and RL workloads for Ash on Nebius clusters, using its own stack and reward signals informed by expert and user feedback.

- Revolut fine-tuned three versions of its PRAGMA transaction model on a dedicated Nebius cluster of 64 NVIDIA H100 GPUs, adapting them for tasks with different precision and latency needs.

- Prime Intellect used Nebius GPU clusters in its SYNTHETIC-2 and INTELLECT-2 training work, including distributed runs across Nebius data centers in Europe and the US. Its platform also gives other builders tools for large-scale post-training and RL.

Nebius supplied the compute for each path; each team owned the task, training workflow, and evaluation that told it whether an iteration was useful.

## Run your pipeline or use managed fine-tuningRun your pipeline or use managed fine-tuning

For teams bringing their own pipeline, Nebius AI Cloud provides GPU compute for experiments and larger training runs, with Serverless Jobs and managed cluster options. Your team can keep its frameworks, recipes, environments, and evaluation methods. For teams that want Nebius to handle more of the training setup, Token Factory offers a managed path for fine-tuning supported open-weight models.

Talk to the Token Factory team about your workload. Bring the starting model, task definition, baseline results, data strategy and deployment requirements.

Prefer self-service? Sign up for Nebius Token Factory.

## ReferencesReferences

DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

The Llama 3 Herd of Models

Tulu 3: Pushing Frontiers in Open Language Model Post-Training

## Explore Nebius Token Factory

Sign up​
Docs and support​

Joe Sarabia
Director of Product, Ecosystem

Di Jin
VP, AI Training at Nebius

Dylan Bristot
Product Marketing, Token Factory

Contents

- 

TL;DR

- 

Define the task and baseline

- 

From production data to the next checkpoint

- 

Choosing a post-training method

- Supervised fine-tuning (SFT)

- Preference tuning

- Reinforcement learning (RL)

- Full fine-tuning or LoRA

- Distillation

- 

Post-training workloads on Nebius

- 

Run your pipeline or use managed fine-tuning

- 

References

## See also

### 

In agentic RL, faster tokens are not enough

Faster model inference does not necessarily mean faster agentic RL training. In this article, we show how improvements to routing, sandbox execution and batch assembly reduced fixed-weight batch collection time by 66.9%, from 591.8 to 196.1 seconds for 256 trajectories.

September 28, 2026
22 mins to read

### 

Three new open-weight models from US companies give builders more choice

Three new open-weight models, Reflection Beam, Meta’s Muse Spark Open, and NVIDIA Nemotron 3.5 Super VL, are now available on Nebius Token Factory. Built for different agent workloads, they span coding and reasoning, multi-file coding and tool use, and visual understanding for documents and web content. All three are served through the same OpenAI-compatible API, making it easier to compare quality, latency, and cost on real tasks.

October 16, 2026
12 mins to read

### 

Nebius achieves NVIDIA Exemplar Cloud on NVIDIA HGX B300 for training workloads

Nebius has achieved NVIDIA Exemplar Cloud on NVIDIA HGX B300 for training workloads, adding to existing Exemplar recognition on NVIDIA H200 and GB300 NVL72. The validation reflects ongoing engineering collaboration with NVIDIA to test and optimize production infrastructure for demanding AI training workloads.

October 8, 2026
7 mins to read

Sign in to save this post
Sign In
