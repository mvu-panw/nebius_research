# Nebius and LangChain partner to power production-grade AI agents on open models

Source: https://nebius.com/blog/posts/nebius-and-langchain-partner-to-power-production-grade-ai-agents-on-open-models

Skip to main content

Nebius and LangChain have partnered to integrate Nebius Token Factory with LangChain’s Deep Agents. The integration, combined with LangChain’s existing Tavily integration, gives teams building on LangChain a direct path to run agent workloads on production-grade AI infrastructure with open-source models, dedicated endpoints, real-time search and full control over cost and data.

## Agents are production workloads nowAgents are production workloads now

The shift from chatbots to autonomous agents has changed what AI infrastructure needs to support. A single agent interaction can involve a planning step, multiple sub-agent calls, tool use, memory retrieval and retries, with each generating inference requests. Where a chatbot makes one LLM call per user message, an agent workflow can make dozens.

LangChain’s ecosystem has become the default tool for teams building agentic workflows. Production agents introduce an infrastructure question that the framework layer doesn’t answer on its own: where do these agents actually run at scale, with the reliability, throughput and model flexibility that production demands?

## Nebius Token Factory and LangChain Deep Agents: the integrationNebius Token Factory and LangChain Deep Agents: the integration

This is where Token Factory comes in. It supports 30+ open-source models compatible with LangChain Deep Agents — including Llama, Qwen, DeepSeek and NVIDIA Nemotron — with an OpenAI-compatible API, dedicated endpoints, autoscaling and a 99.9% uptime SLA.

Here is how the stack fits together:

- 

Deep Agents is LangChain’s open-source agent framework, built on LangGraph to handle orchestration: planning, sub-agents and tool use

- 

LangSmith provides tracing and evaluation

- 

Token Factory provides the inference backend powering every LLM call the agent makes

- 

Tavily, Nebius’s agentic search API, provides real-time web search and content extraction — giving agents grounded access to live information

This integration brings full observability across the agent stack without additional instrumentation. Teams can point their agent workloads at Token Factory through a configuration change: swap the base URL and model string. The result: agents, LangSmith traces, evaluations and orchestration logic remain untouched.

## Optimizing across every layerOptimizing across every layer

Deep Agents’ architecture supports per-sub-agent model routing, so teams can assign different models to different agent roles: a larger model for planning, a faster model for execution, a lightweight model for tool-calling. This allows cost and quality optimization at each layer rather than running one model for everything.

Source

Source

Token Factory’s growing model catalog makes this practical: teams select from the models that fit each role, and swap freely as new models become available with a simple config change.

Source

The langchain-nebius package also supports embeddings and semantic retrieval through Token Factory, so agents using retrieval-augmented generation can run their full pipeline on one infrastructure provider. For agents that need real-time information, Tavily adds a web access layer to the same stack, so retrieval covers both stored knowledge and the live web.

## Getting startedGetting started

Install the langchain-nebius package from PyPi, point your agent at Token Factory and run it. The integration docs walk through setup end to end.

Want to see it live? Join Nebius and LangChain for a webinar on May 21 where we’ll build a production agent with LangGraph, LangSmith and human-in-the-loop oversight.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- Agents are production workloads now

- Nebius Token Factory and LangChain Deep Agents: the integration

- Optimizing across every layer

- Getting started

Sign in to save this post
Sign In
