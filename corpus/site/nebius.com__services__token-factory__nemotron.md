# NVIDIA Nemotron and Nebius Token Factory

Source: https://nebius.com/services/token-factory/nemotron

Skip to main content

## Why digital health teams use Token Factory

### Own your model foundation

Healthcare moves too fast for a one-size-fits-all approach. Nemotron open weights mean you can fine-tune on your own clinical datasets, adapt to your patient population, and build a model that compounds in value over time.

### Built for regulated industries like Healthcare

From a startup scaling across markets to a health system with strict data residency requirements, Nemotron deploys on the infrastructure you own. No shared cloud dependencies, no data leaving your environment.

### From evaluation to production, with urgency

Nebius Token Factory removes the infrastructure bottleneck — serverless fine-tuning, dedicated endpoints, and per-token pricing so you can move from model selection to shipped agent without standing up your own compute.

## Nemotron family models at Token Factory

NVIDIA NemotronTM is a family of open models, weights, and libraries purpose-built for customization, giving digital health companies the foundation to deploy specialized clinical agents across ambient care, decision support, and patient outcome modeling.

## Nemotron 3 Nano 30b

Compact MoE model optimized for efficient reasoning, chat, and coding with strong multilingual support and long-context RAG/agent workflows.

## Nemotron 3 Nano Omni

The most open, efficient, and accurate omni-modal reasoning model for agentic AI.

## Nemotron 3 Super 120b

Hybrid MoE model optimized for efficient multi-agent AI and complex reasoning tasks.

## Nemotron 3 Ultra 550b

Frontier hybrid MoE model optimized for long-running autonomous agents, deep research, and high-throughput workflows.

## Why use Nemotron

Nemotron on Token Factory can improve output quality and performance while reducing inference costs.

up to 26×

## reduced inference spend

40%

## reduced latency

2×

## improved throughput

## Choose your path for a quick start

## 

Playground

Experiment, compare models and tune prompts side-by-side.

## OpenAI-compatible API

Move your endpoint to Token Factory and switch models in seconds.

import os
from openai import OpenAI

client = OpenAI(
 base_url="https://api.tokenfactory.us-central1.nebius.com/v1/",
 api_key=os.environ.get("NEBIUS_API_KEY"))

response = client.chat.completions.create(
 model="nvidia/nemotron-3-super-120b-a12b",
 messages=[
 {"role": "system", "content": "You are helpful assistant"},
 {"role": "user", "content": [{"type": "text", "text": "Hello"}]}])

print(response.to_json())

Trusted by AI practitioners and partners

## Start building today
Go to GitHubJoin Discord
