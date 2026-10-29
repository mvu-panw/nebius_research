# Three new open-weight models from US companies give builders more choice

Source: https://nebius.com/blog/posts/three-new-open-weight-models-from-us-companies-give-builders-more-choice

Skip to main content

The open model ecosystem is growing in both capability and breadth. This week, Reflection Beam, Muse Spark Open from Meta, and NVIDIA Nemotron 3.5 Super VL join that momentum, with all three available on Nebius Token Factory from day zero. Alongside the advances from Chinese labs, these US releases signal a thriving ecosystem with more labs contributing more approaches. Users and builders stand to benefit most: more choice, more flexibility, and more ways to match a model to the work they need done.

That choice also opens more paths to specialization. Builders can select a model for its strengths today, then adapt it to their own data, tools, and workflows through post-training. As the pool of capable open models expands, so does the opportunity to build models tailored to specific applications. These three releases offer different starting points, each addressing a different part of an agent’s job.

Each model fits a different kind of agent work.

- 

Beam is a text-only coding and reasoning model with adjustable reasoning effort, priced at $0.25 per million input tokens.

- 

Muse Spark Open, an open weights release from Meta, is built for multi-file coding and tool use, and accepts text, image, and video input via API.

- 

Nemotron 3.5 Super VL brings visual understanding to documents and web content, with 12 billion active parameters.

All three are mixture-of-experts models served through the same OpenAI-compatible API.

Qwen, DeepSeek, and Kimi are among the open models builders can already run on Nebius Token Factory. New releases from Reflection, Meta, and NVIDIA add more options for coding agents and visual workflows. All three use the same OpenAI-compatible API, so you can start comparing text responses by changing the model ID. Then judge each on the work your application needs to do: answer quality, latency, and cost per successful run.

## Reflection Beam: built for coding agentsReflection Beam: built for coding agents

Beam is Reflection’s first open-weight model, released under Apache 2.0. It is a mixture-of-experts model with 501 billion total parameters and 23 billion active per token. It reads and writes text only, and it is aimed squarely at coding, reasoning, and agentic work. Reflection trained it with reinforcement learning across roughly a million environments and reports a context window of up to 1 million tokens. A reasoning-effort setting lets you trade depth of thinking for speed and cost.

Try it on a real bug or refactor in a repository you know, with a test that makes success unambiguous. Look at the patch and the path the agent took to get there, not just its first answer. Then lower the reasoning effort and see how much quality you keep at a lower cost.

On Token Factory: 0.25 USD per million input tokens and 1.00 USD per million output tokens. Try Beam.

## Muse Spark Open: Meta’s coding model, now with open weightsMuse Spark Open: Meta’s coding model, now with open weights

Muse Spark Open, an open weights model from Meta, is a mixture-of-experts model with 816 billion total parameters and 42 billion active parameters. It is built for debugging, multi-file refactors, codebase understanding, and tool use. It accepts text, image, and video input via API. For a coding task, an agent can work from a screenshot of the broken state alongside the code. Token Factory serves the FP4 checkpoint.

Try it first on a debugging task that spans several files. Judge the whole run: did it find the right files, call the right tools, and land a fix you would merge? Then add a screenshot of the failing UI and see whether the outcome changes.

On Token Factory: 1.25 USD per million input tokens and 4.25 USD per million output tokens. Try Muse Spark Open.

## NVIDIA Nemotron 3.5 Super VL: agents that work from what they seeNVIDIA Nemotron 3.5 Super VL: agents that work from what they see

Nemotron 3.5 Super VL is built for agents that combine visual understanding with reasoning and tool use. It is the most compact of the three, at 120 billion parameters with 12 billion active, and ships under the OpenMDW 1.1 license. NVIDIA positions it for targeted code validation, web research, document understanding, and customer-service workflows. These tasks depend on evidence the model can see, not only on text supplied in a prompt.

Try it on a document-heavy workflow your team already runs, such as invoices, charts, or forms. Check whether the agent pulls out the right evidence and whether its next step follows from what it saw. With 12 billion active parameters, measure its response time and cost per successful task, especially at high volume.

On Token Factory: 0.30 USD per million input tokens and 0.90 USD per million output tokens. Try Nemotron 3.5 Super VL.

## Compare them with what you already runCompare them with what you already run

Token Factory serves all three through an OpenAI-compatible API. The loop below sends the same text prompt to each model and reports response time and token usage. Add the model you use today to the list as a baseline. This text-only loop does not test image or video inputs, or tool use. Save a representative prompt as task.md, install the OpenAI Python package, and set NEBIUS_API_KEY before running it. The Token Factory quickstart shows how to create an API key.

import os
from pathlib import Path
from time import perf_counter
from openai import OpenAI

client = OpenAI(
 base_url="https://api.tokenfactory.nebius.com/v1/",
 api_key=os.environ["NEBIUS_API_KEY"],
)

prompt = Path("task.md").read_text(encoding="utf-8")
messages = [{"role": "user", "content": prompt}]
models = [
 "reflection/beam",
 "meta-models/muse-spark-open",
 "nvidia/Nemotron-3.5-Super-VL",
]

for model in models:
 started = perf_counter()
 response = client.chat.completions.create(
 model=model,
 messages=messages,
 max_tokens=8192,
 )
 elapsed = perf_counter() - started
 print(model, f"{elapsed:.1f}s", response.usage.total_tokens)
 print(response.choices[0].message.content)

Decide what success means before you run anything, and run each task more than once. This example measures response time and token usage for a single text request. Evaluate the complete workflow separately using the questions below.

- 

Was the result correct, and would a reviewer accept it?

- 

Did the agent call the right tools in the full workflow?

- 

How many retries did it need?

- 

How long did the whole task take, and what did it cost?

Those answers can change your choice even when the leaderboard order does not.

One tip for reasoning models: give them a generous output budget. A model that thinks before it answers can spend a small max_tokens limit entirely on reasoning and return an empty reply. Check the output budget before treating that as a verdict on the model.

## Choosing a model for your workloadChoosing a model for your workload

A good evaluation leaves you with a model choice for a specific workload and evidence you can show your team: accepted outputs, failed cases, task time, and cost.

Try Beam, Muse Spark Open, and Nemotron 3.5 Super VL in the Token Factory playground. For help evaluating a production workload, talk to the Token Factory team.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Nebius team

Contents

- Reflection Beam: built for coding agents

- Muse Spark Open: Meta’s coding model, now with open weights

- NVIDIA Nemotron 3.5 Super VL: agents that work from what they see

- Compare them with what you already run

- Choosing a model for your workload

## See also

### 

Nebius achieves NVIDIA Exemplar Cloud on NVIDIA HGX B300 for training workloads

Nebius has achieved NVIDIA Exemplar Cloud on NVIDIA HGX B300 for training workloads, adding to existing Exemplar recognition on NVIDIA H200 and GB300 NVL72. The validation reflects ongoing engineering collaboration with NVIDIA to test and optimize production infrastructure for demanding AI training workloads.

October 8, 2026
7 mins to read

### 

In agentic RL, faster tokens are not enough

Faster model inference does not necessarily mean faster agentic RL training. In this article, we show how improvements to routing, sandbox execution and batch assembly reduced fixed-weight batch collection time by 66.9%, from 591.8 to 196.1 seconds for 256 trajectories.

September 28, 2026
22 mins to read

### 

Nebius Rated Platinum in SemiAnalysis ClusterMAX™ 3.0

SemiAnalysis has named Nebius a Platinum AI cloud provider, the top tier of its ClusterMAX™ 3.0 rating. The rating is based on live testing of production clusters: burn-ins, storage under concurrent load, and automated failure recovery on real NVIDIA GB300 and NVIDIA HGX B300 hardware. This post covers what the testing found and why it matters for teams choosing where to run production AI.

September 23, 2026
7 mins to read

Sign in to save this post
Sign In
