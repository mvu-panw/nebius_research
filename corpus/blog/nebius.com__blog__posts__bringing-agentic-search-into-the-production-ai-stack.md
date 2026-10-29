# Nebius and Tavily: Bringing agentic search into the production AI stack

Source: https://nebius.com/blog/posts/bringing-agentic-search-into-the-production-ai-stack

Skip to main content

## IntroductionIntroduction

Nebius has acquired Tavily, to bring agentic search directly into the Nebius AI Cloud platform.

With this, Nebius expands beyond high-performance inference into a more complete stack for building production AI agents. Token Factory handles reasoning at scale and Tavily adds real-time access to the web. Together, they give developers the core primitives needed to build systems that operate on live information, not just static model knowledge.

This is a shift from running models to running real-world AI systems.

## Why agentic search matters nowWhy agentic search matters now

Models have become strong reasoners, but they are still fundamentally static. They do not know what changed five minutes ago and cannot verify claims against the current state of the world. In production, that gap shows up quickly.

Most real workloads depend on fresh information, such as financial analysis, support agents and research workflows. Without a reliable search layer, teams end up stitching together brittle retrieval pipelines or relying on outdated context. But the value of search goes beyond recency.

It also acts as a direction layer for the model. Even when the knowledge exists in pretraining, search helps guide the model toward the right sources, disambiguate queries and anchor responses in relevant context. Instead of relying purely on latent knowledge, the model operates with external signals that improve both accuracy and reliability.

Without this layer, the result is predictable: hallucinations, stale answers and systems that break under real-world conditions. And agentic systems need more than reasoning — they need access to the world.

## What Tavily adds to the Token Factory stackWhat Tavily adds to the Token Factory stack

Tavily is the web access layer built specifically for AI agents. It provides a single API to search, extract and structure real-time web data in formats optimized for LLMs and agent workflows. It is designed for low latency, high relevance and safe interaction with the open web.

Within the Nebius stack, these components work together as a single system: Nebius AI Cloud provides the infrastructure foundation, Token Factory delivers high-performance inference and Tavily adds real-time grounding and web access. Combined, they enable agents that can both reason and operate on live information.

A simple way to think about it: Token Factory helps agents reason, while Tavily helps them know.

## What this unlocks for buildersWhat this unlocks for builders

Bringing inference and search together unlocks a different class of applications. Agents can verify information against live sources instead of relying purely on model weights. Systems can research topics, monitor events and make decisions based on current data. And developers no longer need to stitch together multiple vendors for inference, retrieval and orchestration.

The result is not just better answers, but systems that behave more reliably under real usage.

## Build example: Grounded research agent with Tavily and Token FactoryBuild example: Grounded research agent with Tavily and Token Factory

To make this concrete, consider a simple research agent. The goal is to answer questions that require up-to-date information by combining:

- Tavily for live web search

- Token Factory for reasoning and synthesis

The pattern is straightforward:

- The user asks a question;

- The model decides whether it needs fresh data;

- If needed, it calls Tavily search;

- The results are fed back into the model;

- The model produces a grounded answer.

At a high level, the system looks like this:

The key detail is that search is not hardcoded: the model decides when it is needed. This is not a complex agent framework — it is a minimal, production-relevant loop.

## Short code snippetShort code snippet

Below is a minimal example of how this works by using Tavily as a tool with a Token Factory model.

from openai import OpenAI
from tavily import TavilyClient
import json

# Initialize clients
client = OpenAI(
 base_url="https://api.tokenfactory.nebius.com/v1/",
 api_key="NEBIUS_API_KEY",
)

tavily = TavilyClient(api_key="TAVILY_API_KEY")

# Define Tavily tool
def tavily_search(query: str):
 return json.dumps(tavily.search(query=query, max_results=5))

tools = [{
 "type": "function",
 "function": {
 "name": "tavily_search",
 "description": "Search the web for up-to-date information",
 "parameters": {
 "type": "object",
 "properties": {
 "query": {"type": "string"}
 },
 "required": ["query"]
 }
 }
}]

# Ask a question
response = client.chat.completions.create(
 model="moonshotai/Kimi-K2.5",
 messages=[{"role": "user", "content": "What are the latest AI developments?"}],
 tools=tools,
)

This is the core integration: a model with access to a search tool.

For a full working example with tool-calling loops and structured outputs, see the cookbook.

## Example of what output looks like in practiceExample of what output looks like in practice

A typical interaction looks like this:

- User asks: “What are the latest developments in AI this month?”;

- The model determines the question requires fresh data;

- It calls Tavily search with a focused query;

- Tavily returns recent, relevant results;

- The model synthesizes a response grounded in those sources.

Instead of a generic answer, you get:

- Current information

- Higher factual accuracy

- Responses aligned with the real-world

This is the difference between a demo and a usable system.

## From demo agents to production systemsFrom demo agents to production systems

This pattern becomes critical as systems move into production. Most failures do not come from model quality alone — they come from missing system components.

Production agents require:

- Reasoning to process complex tasks;

- Retrieval/search to access fresh information;

- Reliability and governance to control behavior;

- Deployment infrastructure to scale and perform consistently.

Search is not an add-on, but a core part of the system design.

## Example use casesExample use cases

This pattern shows up across multiple real workloads:

- 

Research agents: Automatically gather and synthesize up-to-date information from the web;

- 

Enterprise copilots: Provide answers grounded in both internal data and current external context;

- 

Monitoring and operations agents; Track changes in markets, vendors, regulations or competitors in real time.

This is no longer theoretical. Teams are already building systems this way.

## Developer angleDeveloper angle

Tavily will continue operating under its current brand and serving its existing developer ecosystem.

Developers can keep using Tavily as they do today, with:

- A simple API for search, extraction and crawling;

- Endpoints optimized for agent workflows;

- Fast and reliable responses designed for real-time systems.

Over time, integration with the Nebius stack will deepen, making it easier to combine inference, search and deployment into a single workflow.

## The bigger Nebius narrativeThe bigger Nebius narrative

This acquisition reflects a broader direction, Nebius is building the production stack for AI systems:

- Infrastructure to run workloads

- Inference to power reasoning

- Search to ground systems in reality

And over time, additional components are required to design, deploy and operate reliable AI agents.

The goal is simple: reduce the gap between building a model and running a real product.

## Learn moreLearn more

Explore Tavily

Explore Token Factory

Read the full cookbook

Talk to us about production agents

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Jakki Jakaj
Head of Marketing at Tavily

Dylan Bristot
Product Marketing, Token Factory

Contents

- Introduction

- Why agentic search matters now

- What Tavily adds to the Token Factory stack

- What this unlocks for builders

- Build example: Grounded research agent with Tavily and Token Factory

- Short code snippet

- Example of what output looks like in practice

- From demo agents to production systems

- Example use cases

- Developer angle

- The bigger Nebius narrative

- Learn more

## See also

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

### 

Nebius and LangChain partner to power production-grade AI agents on open models

Nebius and LangChain have partnered to integrate Nebius Token Factory with LangChain’s Deep Agents. The integration, combined with LangChain’s existing Tavily integration, gives teams building on LangChain a direct path to run agent workloads on production-grade AI infrastructure with open-source models, dedicated endpoints, real-time search and full control over cost and data.

May 13, 2026
6 mins to read

### 

Agent 101: Launching production-grade agents at scale

To go from prototype to production, AI agents need more than just a good model. In this guide, we break down the four components that matter most: reliable LLMs, orchestration frameworks, evaluation tools, and memory systems. We cover how teams are using Nebius AI Studio with CrewAI, ADK, LangChain, and more to ship scalable, observability-friendly agent workflows, all powered by fast, cost-efficient inference.

July 10, 2025
10 mins to read

Sign in to save this post
Sign In
