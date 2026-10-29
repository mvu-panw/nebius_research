# AI infrastructure that speaks your language

Source: https://nebius.com/blog/posts/ai-infrastructure-that-speaks-your-language

Skip to main content

Imagine being able to tell your cloud: “I’m expecting 2,000 daily users on my AI-enabled app. Provision the inference cluster for that, pick the right inference engine, and configure autoscaling.” And it just happens. No call with a solutions architect, no Terraform deep dive, no back and forth with a DevOps engineer.

That’s not where we are today. But it’s exactly where we’re headed, and today we’re taking a concrete step toward it with Nebius Echo, our new AI agent built into the cloud console.

## You already work this wayYou already work this way

If you’ve used Claude Code or OpenAI Codex recently, you know the pattern: describe what you want, the agent figures out the steps, and the work gets done. You no longer write every function by hand. You state intent and review the result.

That shift happened faster than most people expected. And the same expectation is now reaching the tools developers use to manage infrastructure. Why should spinning up a GPU cluster feel like a different era of computing compared to the rest of your workflow?

Making AI infrastructure accessible — and not a barrier to real value — has always been a priority for us. Managed services, MLOps integrated tooling, pay-as-you-go, and truly elastic compute: all of it was built on the premise that you shouldn’t need to be an infrastructure specialist to operate in the AI infrastructure world. You should be able to focus on models, applications, and business outcomes.

With Nebius MCP Server, launched last year, we took the first step toward natural-language infrastructure management: a way for AI agents like Claude Code or Codex to interact with Nebius directly, so anyone already running agentic workflows could extend them to cloud operations. Now we’re taking the next step.

Figure 1. You can access Nebius AI Cloud via different interfaces

## Nebius Echo: your AI agent for your AI cloudNebius Echo: your AI agent for your AI cloud

Today we’re launching Nebius Echo, an AI agent built directly into the Nebius console. It gives you a new way to talk to your infrastructure: ask questions, get answers grounded in the full Nebius documentation, and create resources — all in plain language, with no setup required from the moment you sign in.

Figure 2. Nebius Echo is an AI agent built directly into the web console

Let’s take a look at what Nebius Echo can do today:

- 

Answers questions from the Nebius documentation. Ask about a service, a configuration option, or a concept. Echo draws on the full Nebius documentation to give you a direct, context-aware answer rather than sending you to search for it yourself.

- 

Shows the state of your resources. Query current capacity, running instances, or project status in plain language. Echo pulls this from your cloud environment and surfaces it directly in the conversation.

- 

Executes resource-creation requests in natural language. Spin up a VM, create a serverless endpoint, launch a cluster: describe what you need and Echo handles the API call.

For example: ask “How many H100 GPUs are available in my project right now?” and Echo answers from your live environment. Say “Launch a VM with eight of them,” and Echo turns that into the right API call and creates it without you leaving the conversation or looking up a single command.

The documentation that used to sit in a separate tab now comes to you. The commands that used to require knowing the right syntax now accept plain language. For individuals and teams working with AI infrastructure day to day, that’s a practical difference in how much time you spend before the actual work begins.

If you’d rather work through external agents and developer tools, Nebius MCP Server gives you the same kind of access. Echo lives inside the console; MCP Server brings Nebius into the agent tools you already use. Both run on the same backend, so you can pick whichever fits your workflow and get the same capabilities either way.

## What we’re building nextWhat we’re building next

Nebius Echo today handles documentation questions and individual operations. But that’s just the beginning: The next steps are about giving it deeper context and broader capability, and they’re both in active development.

The first is infrastructure investigation. We’re building the ability for Nebius Echo to correlate infrastructure state, logs, and metrics when something goes wrong, and surface a structured diagnosis rather than making you connect the dots yourself. When a training job crashes or a VM becomes unreachable, Echo will gather the relevant context across sources, tell you what it found, and recommend what to do about it. This capability will be available through both the Echo interface and Nebius MCP Server. Because they share the same backend, your agents can trigger investigations the same way a human would.

The second is a native, in-house Infrastructure-as-Code (IaC) capability we’re actively developing. It will serve as the internal engine that handles the same complexity you’d typically manage with Terraform: multi-step, context-rich deployments with full state management.

Figure 3. Nebius Infrastructure-as-Code (IaC) capability will expand capabilities for agents

Once in place, it enables both Nebius Echo and Nebius MCP Server to handle compound infrastructure tasks end-to-end. This includes natural language requests like the one we imagined at the start of this blog, where Echo builds a deployment plan, confirms it with you, and executes it. Teams with existing agentic pipelines will be able to extend them to the same capability without changing their setup.

Both are planned for later this year.

## Towards an agentic-ready AI cloudTowards an agentic-ready AI cloud

The goal here isn’t just a better chatbot for the console. Rather, think about what it means to have a dedicated cloud architect available whenever you need one: someone who knows your infrastructure, understands your goals, and can turn a high-level requirement into a working deployment. That kind of support has always existed for large teams with the right resources. We’re working to make it the default experience for everyone building on Nebius.

That’s what this direction is really about: not a set of tools, but a different relationship between the people building AI products and the infrastructure that runs them. One where operational expertise is no longer a prerequisite, and where the time between an idea and a running workload keeps getting shorter.

The logical next step is a system that doesn’t wait to be asked. Your application detects it needs more inference capacity; your agent evaluates the options, provisions the right resources, and configures them. All this while you focus on something else entirely. Reliable, predictable, and secure in production. That’s the version of AI infrastructure we’re working toward, and what we’re doing today is what makes it possible.

You can get started with Echo today. Simply sign up for the Nebius console and try it, no setup needed. Ask your first infrastructure questions, inspect your resources, or create a resource in plain language.

Already running agentic workflows? Connect them to your Nebius infrastructure with Nebius MCP Server today.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Oleg Filimoshin
Head of Product — IaaS

Contents

- You already work this way

- Nebius Echo: your AI agent for your AI cloud

- What we’re building next

- Towards an agentic-ready AI cloud

## See also

### 

Introducing Nebius MCP Server: The LLM-native way to manage your AI Cloud

Skip the CLI commands and web console clicks — just ask Claude about your cloud infrastructure. Today, we’re excited to announce the Nebius MCP Server, our integration that connects Claude by Anthropic, or other AI chatbots, to the Nebius AI Cloud infrastructure.

July 16, 2025
5 mins to read

### 

Introducing the Nebius Agents Blueprint: open architecture for production-ready AI agents

Today we’re introducing the Nebius Agents Blueprint, an open reference architecture for building, operating, and continuously improving AI agents in production. This post covers the six-component composable stack — inference, orchestration, retrieval, grounding, observability, and simulation — and the case study behind it: a compliance audit agent that achieved 72% lower cost and 20% higher precision over a GPT-based prototype by improving the system, not the model.

June 10, 2026
6 mins to read

### 

Understanding the Model Context Protocol: Architecture

As LLM-powered agents become more complex, integrating them with tools, APIs, and private data sources remains a major challenge. Model Context Protocol (MCP) offers a clean, open standard for connecting language models to real-world systems through a modular, plug-and-play interface. In this article, we explore how MCP works.

May 1, 2025
9 mins to read

Sign in to save this post
Sign In
