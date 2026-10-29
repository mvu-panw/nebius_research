# GLM models inference

Source: https://nebius.com/services/token-factory/models/glm-models-inference

Skip to main content

## Choose flagship, fast, or established inference

Use GLM-5.3 for demanding agentic work, GLM-5.3-Flash for cost-efficient speed, or GLM-5.2 when you need an established public and dedicated path.

## Up to 1M-token context

Keep large repositories, research trails, tool histories, and long documents in one working context.

## Built for multi-step execution

Apply GLM models to coding, planning, research, and agent workflows that combine reasoning with tools.

## Tool calling and structured workflows

Connect models to external functions and orchestrate multi-step application logic.

## Choose the right input modality

GLM-5.3 and GLM-5.2 serve text workloads, while GLM-5.3-Flash is listed as a vision-capable public model.

## Start shared, move to isolated capacity

Evaluate through public endpoints and use model-specific dedicated availability when your workload needs isolated capacity or regional control.

## Choose your GLM model

From $1.40 / 1M input tokens

## GLM-5.3

Flagship GLM model for demanding coding and agentic workflows

Best for: large-context coding, complex agents, reasoning, research, and tool use

- 1,024K-token context

- FP4 serving configuration

- Tool calling and reasoning available

- Public endpoint available

- $1.40 / 1M input tokens · $4.40 / 1M output tokens

View detailsTry in Playground

From $0.15 / 1M input tokens

## GLM-5.3-Flash

Fast, lower-cost GLM model for agent and multimodal workloads

Best for: high-volume agents, coding, reasoning, tool use, and image-aware workflows

- 1,024K-token context

- FP4 serving configuration

- Vision input, tool calling, and reasoning available

- Public endpoint available

- $0.15 / 1M input tokens · $0.50 / 1M output tokens

View detailsTry in Playground

From $1.40 / 1M input tokens

## GLM-5.2

Long-context GLM model with public and dedicated availability

Best for: bilingual reasoning, long documents, agents, and workloads that may need isolated capacity

- Up to 1,024K-token context

- FP4 and FP8 configurations listed

- Tool calling and reasoning available

- Public and dedicated endpoints listed

- $1.40 / 1M input tokens · $4.40 / 1M output tokens

View detailsTry in Playground

## Benchmarks

Z.ai publishes model-level evaluations for coding, reasoning, and agentic tasks. Use those results to compare model capability, then validate the selected model on your own prompts, tools, latency requirements, and cost profile in Token Factory.

Provider benchmark results describe the model under a specific evaluation harness. They are not a guarantee of Token Factory endpoint throughput, latency, or availability.
View official GLM-5.3-Flash model information

## 

A simple and friendly UI for a smooth user experience

Use the Playground to compare GLM-5.3, GLM-5.3-Flash, and GLM-5.2 on your own coding tasks, long prompts, tool schemas, and image inputs. Refine prompts and export an API-ready request when you are ready.
Try GLM-5.3

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
 model='zai-org/GLM-5.3'
)

Read the inference documentation

## Choose how to run GLM

Deployment option

Best for

What you get

Public endpoints

Evaluation, prototyping, and variable traffic

Pay-per-token access with no deployment required

Dedicated endpoints

Workloads that need isolated capacity or regional control

Model-specific availability; confirm the selected GLM model before committing

Custom deployments

Private weights or specialized requirements

Workload-specific sizing and deployment support

## Frequently asked questions

Which GLM model should I choose?

Start with GLM-5.3 for the flagship long-context experience. Choose GLM-5.3-Flash for lower-cost, high-volume or vision-aware work. Use GLM-5.2 when its dedicated path matches your deployment requirements.

Do the current GLM models support tool calling and reasoning?

The live Token Factory catalog lists tool calling and reasoning for GLM-5.3, GLM-5.3-Flash, and GLM-5.2. Validate your exact schema and reasoning settings before production rollout.

When should I use a dedicated endpoint?

Use a public endpoint to evaluate the model. Move to a dedicated endpoint when you need isolated capacity, regional control, or model-specific performance planning. Dedicated availability varies by model.

Can I fine-tune these GLM models?

The current catalog does not list self-service fine-tuning for these three models. Confirm the required adaptation and deployment path with Nebius.
