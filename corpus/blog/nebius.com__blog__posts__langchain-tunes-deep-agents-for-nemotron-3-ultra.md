# LangChain tunes Deep Agents for NVIDIA Nemotron 3 Ultra: top open-model accuracy at 10x lower cost with Nebius Agents Blueprint

Source: https://nebius.com/blog/posts/langchain-tunes-deep-agents-for-nemotron-3-ultra

Skip to main content

Today, LangChain released a Deep Agents profile tuned for NVIDIA Nemotron 3 Ultra, achieving top agent accuracy among open models at roughly 10x lower cost than closed alternatives, with no changes to the model itself. LangChain optimized how the agent plans, calls tools, and executes tasks, improving overall agent performance through better orchestration. Those gains come from the harness around the model — and it’s a lever most teams overlook.

The Nebius Agents Blueprint already pairs LangChain Deep Agents with open-source models including NVIDIA Nemotron 3 Ultra served on Nebius Token Factory, giving you a production-ready foundation for building AI agents. Support for the NVIDIA Nemotron optimized Deep Agents profile is coming to the Nebius Agents Blueprint soon.

## An agent’s cost comes from the harness, not the modelAn agent’s cost comes from the harness, not the model

An agent’s cost is a function of how many tokens it burns on the way to an answer. Every planning step, tool call, retry, and repeated read adds to the bill. The model sets the ceiling on quality; the harness — the prompts, tool definitions, and middleware around the model — decides how efficiently it reaches that ceiling. A generic harness makes an open model do more work than it needs to. A harness tuned to a specific model removes the wasted steps.

LangChain tuned Deep Agents to Nemotron 3 Ultra through an eval-driven loop: run the task suite, find the failing and wasteful patterns, adjust prompts, tools, and middleware, then repeat until performance converges. The result ships as a profile you load directly in Deep Agents. No fine-tuning, no retraining — the model is untouched. The gains come entirely from the runtime around it.

Combined with NVIDIA Nemotron 3 Ultra open weights, you can customize the complete agent stack, from model to the harness, for your own proprietary workflows while maintaining flexibility over deployment and infrastructure.

## Why harness improvements translate to lower costWhy harness improvements translate to lower cost

For a single-turn chatbot, token efficiency is rarely more than a rounding error. But for an agent that runs for minutes across dozens of tool calls, inefficiencies compounds: one poorly sequenced run can multiply the inference bill substantially.

Tuning the harness attacks the cost at its source: fewer redundant reads, tighter tool use, less scope drift. Same model, same quality target, far fewer tokens to get there. That’s how an open model lands within reach of frontier accuracy at a fraction of the cost per task, without needing a bigger model or retraining.

## Run it with the Nebius Agents BlueprintRun it with the Nebius Agents Blueprint

The Nebius Agents Blueprint is an open reference architecture with runnable recipes for building, running, and improving AI agents in production. It already pairs LangChain Deep Agents for orchestration with NVIDIA Nemotron 3 Ultra served on Nebius Token Factory for inference, alongside retrieval, grounding, observability, and simulation.

The tuned Deep Agents profile is coming to the Blueprint. Because the Blueprint can already run Deep Agents against the Nemotron 3 Ultra endpoint, adopting the tuned profile is a configuration change, not a migration. You can benefit from the latest Deep Agents improvements while keeping the rest of the application architecture unchanged.

Get started with the Nebius Agents Blueprint to deploy LangChain Deep Agents with NVIDIA Nemotron 3 Ultra on Nebius Token Factory in minutes, and pick up the tuned profile the moment it lands.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Devang Sachdev
Vice President of Strategy

## See also

### 

Introducing the Nebius Agents Blueprint: open architecture for production-ready AI agents

Today we’re introducing the Nebius Agents Blueprint, an open reference architecture for building, operating, and continuously improving AI agents in production. This post covers the six-component composable stack — inference, orchestration, retrieval, grounding, observability, and simulation — and the case study behind it: a compliance audit agent that achieved 72% lower cost and 20% higher precision over a GPT-based prototype by improving the system, not the model.

June 10, 2026
6 mins to read

### 

Nebius and LangChain partner to power production-grade AI agents on open models

Nebius and LangChain have partnered to integrate Nebius Token Factory with LangChain’s Deep Agents. The integration, combined with LangChain’s existing Tavily integration, gives teams building on LangChain a direct path to run agent workloads on production-grade AI infrastructure with open-source models, dedicated endpoints, real-time search and full control over cost and data.

May 13, 2026
6 mins to read

### 

Nebius AI Cloud “Aether 3.6”: Operating production AI with more control, efficiency, and confidence

Introducing Aether 3.6. Our latest quarterly platform release responds to how AI teams now operate at scale and with maturity, delivering a smoother developer experience, a stronger security and compliance foundation, advances across our in-house storage portfolio, and natural-language control over your AI cloud.

June 24, 2026
14 mins to read

Sign in to save this post
Sign In
