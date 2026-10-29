# OpenAI GPT-OSS models inference

Source: https://nebius.com/services/token-factory/models/openai-gpt-oss

Skip to main content

## Configurable reasoning depth

Tune reasoning effort to balance latency and accuracy for agent loops and multi-step planning.

## Long-context stability (131K)

Cache-aware routing and prefill optimizations keep latency and cost predictable across long sessions.

## Tool-native outputs

Reliable function-calling and structured responses for safe agent execution and easier orchestration.

## Lower cost per decision

Fewer retries and shorter agent loops reduce total cost per task, not just cost per token.

## Production post-training

Optional calibration, distillation, and sampler tuning based on real traffic to preserve reasoning quality at scale.

## Enterprise controls & zero retention

Dedicated endpoints, RBAC, region-locking, and zero-retention options for regulated workloads.

## Choose your GPT-OSS model

From $0.15 / 1M input tokens

## gpt-oss-120B

Frontier reasoning model for complex, multi-step tasks.

Best for: agentic systems, planning, research, complex coding

- 131K context

- Apache 2.0 open license

Capabilities:

- Deep reasoning

- Native tool use

- Structured outputs

- Fine-tuning support

View detailsDeploy

From $0.05 / 1M input tokens

## gpt-oss-20B

Efficient reasoning model with high throughput

Best for: cost-sensitive agents, coding assistants, scalable inference

- 131K context

- Apache 2.0 open license

Capabilities:

- High throughput

- Tool use

- Structured outputs

- Cost-efficient

View detailsDeploy

## Benchmarks

GPT-OSS models deliver competitive frontier-level reasoning across standard evaluations. The 120B model targets maximum reasoning depth, while the 20B variant balances strong performance with higher throughput and lower cost.

## AIME (2024–2025)

- Strong multi-step mathematical reasoning.

- 120B approaches frontier-level scores.

- 20B maintains high accuracy relative to its size.

## MMLU / GPQA

- Broad general reasoning and knowledge coverage.

- 120B leads on complex domain tasks.

- 20B offers strong cost-performance efficiency.

## SWE-Bench

- Reliable code reasoning and structured task execution.

- Both models support tool use and structured outputs.

Benchmarks measure accuracy. At scale, tail latency, retry rates, and cache efficiency dominate real cost. Nebius Token Factory optimizes for those production signals.
View detailed model evaluations

## 

A simple and friendly UI for a smooth user experience

Use the Playground to compare reasoning depth, tool-call fidelity, and cost behavior across GPT-OSS models. Refine prompts, test agent flows, and export production-ready API snippets when you’re ready.
Try now

- 
- 

## Familiar API at your fingertips

import openai
import os

client = openai.OpenAI(
 api_key=os.environ.get("NEBIUS_API_KEY"),
 base_url='https://api.tokenfactory.nebius.com/'
)

completion = client.chat.completions.create(
 messages=[{
 'role': 'user',
 'content': 'What is the answer to all questions?'
 }],
 model='openai/gpt-oss-120b'
)

Learn more about our API

## Choose how to run GPT-OSS

Deployment option

Best for

What you get

Serverless inference

Prototyping, variable traffic

Pay-per-token pricing, autoscaling, zero setup

Try serverless

Dedicated endpoints

Production agents

Guaranteed throughput, predictable latency, isolation

Deploy dedicated endpoint

Custom deployments

Large-scale or regulated workloads

Custom tuning, compliance controls, enterprise SLA

Talk to an expert

## Frequently asked questions

How do GPT-OSS models differ from OpenAI API models?

GPT-OSS models are open-weight and Apache 2.0 licensed, giving you full control over deployment, fine-tuning, and cost. There is no vendor lock-in or usage restriction.

Can I fine-tune GPT-OSS on Nebius?

Yes. Nebius Token Factory supports fine-tuning, distillation, and post-training pipelines that can be deployed directly to production endpoints.

When should I use dedicated endpoints for GPT-OSS?

Dedicated endpoints are recommended for production agents, predictable latency requirements, and workloads with sustained or spiky traffic.

How does GPT-OSS perform on reasoning benchmarks?

GPT-OSS performs competitively on AIME, MMLU, GPQA, and SWE-Bench. In production, Nebius focuses on reducing retries and tail latency to improve real-world outcomes.
