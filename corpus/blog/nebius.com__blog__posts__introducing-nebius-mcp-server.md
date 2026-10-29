# Introducing Nebius MCP Server: The LLM-native way to manage your AI cloud

Source: https://nebius.com/blog/posts/introducing-nebius-mcp-server

Skip to main content

At NVIDIA GTC Paris back in June, we announced the Nebius MCP Server, our integration that connects Claude by Anthropic or other AI chatbots to the Nebius AI Cloud infrastructure.

As AI assistants become integral to daily workflows, why not use conversational AI to manage your cloud resources too? Whether you need to check the free capacity of your clusters, view a list of VMs or get a cost analysis by project, you can ask Claude to do it for you. Here’s how this conversational approach transforms your infrastructure management workflow.

# LLM-powered infrastructure insightsLLM-powered infrastructure insights

With the Nebius MCP integration, LLMs gain deep knowledge of the Nebius AI Cloud and access to your infrastructure and resources. Our MCP server implements the MCP Tools standard, allowing models like Claude to interact with our cloud, retrieve data about the instances and perform actions.

You can use the AI chat to get any information your team would normally get from the CLI or web console. Claude understands your natural language requests, translates them to CLI commands and generates tables and charts in convenient visual formats.

Leveraging advanced LLM capabilities, you can also make complex requests, like “Show me spending trends and suggest optimizations”. Claude will map your infrastructure, summarize reports, aggregate information and offer recommendations for resource management. It’s like having a dedicated DevOps expert available 24/7 to answer questions and provide insights into your AI infrastructure.

Let’s look at how this works with real queries you might use every day.

# See it in actionSee it in action

AI chat is an intuitive way to ask for information, whether you’re an AI cloud power user or just need ad-hoc answers. Here are some real-world examples of prompts and responses for listing projects, managing VMs and getting insights into NVIDIA GPUs.

### List your projects in a tableList your projects in a table

Get a quick overview of your projects with a prompt like “show me all my projects as a table”. Ask for your preferred formatting, whether it’s a table, CSV or XLS. Claude gets all the necessary context from the Nebius MCP Server:

In this example, Claude generates a table with information about each tenant:

### Manage your VMsManage your VMs

For the prompt “show me all my vms”, Claude checks all your active projects and generates a comprehensive table listing all your virtual machines. You’ll also get an overview in the chat with highlights, like this one:

### Get insights about your GPUsGet insights about your GPUs

For the prompt “show all audit events for vm mks8snodegroup-e00cwafcgcsnvgs7mx-52gnq-n57st”, Claude lists the VM details and audit events, then presents a summary to give you quick insights. Here’s an example of Claude’s observations:

### Ask anythingAsk anything

Make your prompts as simple or complex as you like. Everyday scenarios might include:

- 

Daily infrastructure checks on free capacity and cluster status

- 

Get a report on spending trends over the last month with cost-saving recommendations

- 

Generate a chart showing current cluster utilization with suggestions for optimization

These capabilities are powered by Model Context Protocol (MCP), ensuring secure, controlled access to external resources.

# Understanding MCP: The technology behind our integrationUnderstanding MCP: The technology behind our integration

Model Context Protocol is an open standard developed by Anthropic that enables LLMs to securely connect to external data sources and tools. You can think of it as an API-like technology that bridges the gap between AI capabilities and real-world systems without compromising security.

The integration has three components: an LLM client (Claude Desktop), the Nebius MCP Server and the MCP protocol that allows them to communicate.

Click to expand

MCP offers controlled access to external resources without complex authentication or the risk of exposing sensitive credentials. In our implementation, Claude accesses Nebius AI Cloud via CLI. In other words, Claude sends requests to the Nebius MCP Server, which passes them to the CLI, and the CLI executes commands via calls to the Nebius API. You must be authorized in the CLI before deploying the MCP server.

The Nebius MCP Server enables several key capabilities:

- 

Deep knowledge of Nebius AI Cloud. Nebius MCP Server provides the Nebius cloud documentation and command references to the LLM client. You don’t need to upload information for the LLM

- 

Context awareness. The system understands your tenant structure, permissions and available resources

- 

A complementary tool to supplement existing interfaces. The AI chat is a convenient way to get quick answers to infrastructure questions, but it doesn’t replace the CLI and web console for AI Cloud management. If you need to make updates to resources or create new ones, we recommend using the CLI or web console for better control over these operations

You can learn more about the MCP protocol in our blog post. Ready to experience conversational cloud management firsthand? The setup process is straightforward.

# Getting startedGetting started

If you’re ready to try the Nebius MCP integration, you’ll need to have an active Nebius AI Cloud account with appropriate permissions and an MCP-compatible LLM client (out of the LLMs we’ve tested, Claude Desktop offers the best experience).

To set up the integration:

- 

Install and configure the Nebius CLI

- 

Install the uv package manager

- 

Download the nebius-mcp repository to your computer.

- 

Follow the instructions to add Nebius MCP Server to Claude Desktop.

After installation, test your setup by asking Claude about your Nebius cloud infrastructure.

Once you get started, you’ll quickly discover the natural workflow improvements that conversational infrastructure management brings to your team.

# What’s nextWhat’s next

The Nebius MCP integration combines the precision of traditional tools with the intuitive ease of conversational AI. By streamlining routine monitoring and complex queries for your team, it helps reduce the friction between business needs and technical implementation.

At Nebius, we believe that AI infrastructure should be as intelligent as the workloads it supports. We’ll continue to explore how LLM-native infrastructure management can integrate into every aspect of AI development workflows.

If you’re ready to experience conversational cloud management firsthand, feel free to install the Nebius MCP server.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- 

LLM-powered infrastructure insights

- 

See it in action

- List your projects in a table

- Manage your VMs

- Get insights about your GPUs

- Ask anything

- 

Understanding MCP: The technology behind our integration

- 

Getting started

- 

What’s next

## See also

### 

Understanding the Model Context Protocol: Architecture

As LLM-powered agents become more complex, integrating them with tools, APIs, and private data sources remains a major challenge. Model Context Protocol (MCP) offers a clean, open standard for connecting language models to real-world systems through a modular, plug-and-play interface. In this article, we explore how MCP works.

May 1, 2025
9 mins to read

### 

Nebius AI Cloud is now integrated with SkyPilot

We’re excited to announce our integration with SkyPilot, an open-source framework that simplifies running AI and batch workloads across cloud platforms. This collaboration enables direct access to Nebius AI Cloud resources via SkyPilot.

April 2, 2025
6 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
