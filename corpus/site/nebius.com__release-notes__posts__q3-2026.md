# What was new in Q3

Source: https://nebius.com/release-notes/posts/q3-2026

Skip to main content

## Cloud PlatformCloud Platform

Connect AI workloads to your existing operations, manage resources more precisely, and spend less time getting environments ready. Read the blog here.

### Connect securely to your on-premises data center or other cloudConnect securely to your on-premises data center or other cloud

What changed: Cloud Interconnect provides a dedicated private connection between Nebius AI Cloud and your network through neutral interconnection facilities, with MACsec encryption on the last mile. Aggregate available 100G and 400G ports for higher bandwidth.

Why it matters: Connect on-premises data centers, colocation sites, or another public cloud without routing traffic over the public internet, and without a bilateral agreement between providers.

### Benefit from new Preemptible VMs spot pricingBenefit from new Preemptible VMs spot pricing

What changed: Preemptible VMs now use dynamic pricing that reflects demand for each GPU type and region. View the current price and up to 30 days of price history before launching a workload.

Why it matters: Use pricing trends to schedule workloads that can tolerate interruption and take advantage of lower-cost capacity when demand is quieter.

### Move data between object storage and Nebius Shared FilesystemMove data between object storage and Nebius Shared Filesystem

What changed: Data Transfer Service now supports Nebius Shared Filesystem, through filesystem buckets, as a source or destination, alongside S3-compatible object storage.

Why it matters: Move datasets into and out of Nebius Shared Filesystem without writing custom transfer scripts or operating your own transfer infrastructure. Simplify migration and data movement across regions.

### Manage and better understand your stored dataManage and better understand your stored data

What changed: New Object Storage capabilities give teams more ways to organize and review their data:

- Object tagging: Track objects using tags and apply lifecycle rules to objects carrying specific tags.

- Bucket Inventory: Review object listings with metadata including last access, last modification and encryption status.

Why it matters: Understand what you’re storing, identify older or less-used data, and manage its lifecycle with less manual work.

### Control and account for cloud consumptionControl and account for cloud consumption

What changed: Three additions connect resource usage to ownership and budgets:

- Cost allocation labels: Attribute spending across teams, projects and environments.

- Monthly usage and cost breakdown: Download a structured PDF for accounting and reconciliation.

- Capacity Block Group project limits: Control how much reserved capacity each project can consume.

Why it matters: See where spending goes, give teams clearer accountability, and keep one project from consuming an entire shared capacity pool.

### Get from development to running workloads fasterGet from development to running workloads faster

What changed: Serverless AI removes more of the setup between an idea and a running workload

- Serverless AI Devlab: Launch a persistent CPU or GPU workspace using a curated template or your own image, and access it through a managed HTTPS URL.

- Direct Python execution: Run Python files as Serverless Jobs without first building a Docker container.

- File injection: Supply local files or inline content to Jobs, Endpoints and Devlab environments at launch.

- Pre-built templates: Start with validated configurations, aligned framework versions and a recommended GPU type.

Why it matters: Spend less time packaging code, configuring environments and passing files into workloads, and more time developing, testing and iterating.

### Extend your security posture management with WizExtend your security posture management with Wiz

What changed: Native cloud security posture management support, starting with Wiz, gives security teams visibility into misconfigurations in their Nebius environment.

Why it matters: Teams using Wiz can assess their Nebius infrastructure alongside the rest of their cloud estate.

### Run cloud commands from your browser with Cloud ShellRun cloud commands from your browser with Cloud Shell

What changed: Cloud Shell provides a pre-authenticated command-line terminal in the Nebius console.

Why it matters: Run cloud commands without configuring local tools, and make development services reachable for testing and collaboration.

### Automate infrastructure through REST APIAutomate infrastructure through REST API

What changed: Every public Nebius service is now accessible over HTTP and JSON using your existing IAM credentials. A published OpenAPI specification helps tools and agents discover and use the APIs.

Why it matters: Bring Nebius infrastructure management into scripts, CI pipelines and agent workflows using a familiar API format.

### Manage infrastructure in a AI-native wayManage infrastructure in a AI-native way

What changed: Two updates for AI agents make the infrastructure management more efficient:

- 

Nebius Echo, our AI infrastructure agent: Manage longer conversations by using an expandable chat window, a revised layout and chat history.

- 

Public GitHub repository of Nebius skills: Apply guidance from customer engineering into instructions coding agents can read and act on

Why it matters: Communicate with your Nebius cloud infrastructure using AI agents more effectively and execute commands more accurately.

### Also this quarterAlso this quarter

- 

Certified Kubernetes: Nebius Managed Kubernetes achieved CNCF Kubernetes conformance certification, supporting compatibility with upstream Kubernetes tooling and workloads.

- 

Public application marketplace: Browse AI/ML images, frameworks and preconfigured environments from nebius.com without signing in.

- 

LanceDB guide: Get started with generating, storing and querying vector embeddings using LanceDB and Nebius Object Storage.

- 

Tunnels: Make a local service reachable for testing without opening firewall ports.

## Managed Inference | Token FactoryManaged Inference | Token Factory

Day-0 zero access to more open weight models, clearer serving metrics and new ways to optimize inference for your workload.

### Optimize inference with a draft model trained on your dataOptimize inference with a draft model trained on your data

What changed: Custom Speculator Training lets you train a workload-specific draft model on your own data and deploy it alongside a supported base model.

Why it matters: Tailoring speculative decoding to your traffic can improve inference throughput and latency for recurring workloads.

### More open-weight models, including Day-0 releasesMore open-weight models, including Day-0 releases

What changed: The expanded model lineup includes GLM-5.2, GLM-5.3, GLM-5.3-Flash, Kimi K2.7 Code, Kimi K3, NVIDIA Nemotron 3.5 Lightning, DeepSeek V4 Flash-0731, DeepSeek V4 Pro 0813, DeepSeek V4.1 Flash, Qwen 3.8-27B and K2 Horizon. An updated Model Catalog and more comprehensive model pages make discovery easier and clarify the distinction between models and deployed endpoints.

Why it matters: Explore a broader selection of models for your workloads and understand your deployment options in one place.

### Build agent workflows with the Responses APIBuild agent workflows with the Responses API

What changed: Stateless Responses API support brings tool calling, structured outputs and streaming to agent workflows.

Why it matters: Connect models to tools and request structured responses while managing application state in your own system.

### See what drives inference performanceSee what drives inference performance

What changed: Expanded observability includes active GPU counts, GPU utilization, KV-cache hit rate and clearer streaming-latency reporting.

Why it matters: Understand how serving resources are being used, investigate bottlenecks and make better-informed decisions about capacity and performance.

### Run batch inference on capacity that scales to zeroRun batch inference on capacity that scales to zero

What changed: Batch Inference 2.0 (in private beta for selected customers) runs asynchronous inference on dedicated batch capacity that scales to zero between jobs.

Why it matters: Process workloads that do not need an immediate response without keeping batch compute running between jobs.

### Use Token Factory in more coding workflowsUse Token Factory in more coding workflows

What changed: New integrations connect Token Factory with Hermes, OpenCode, Cline and Kimi Code.

Why it matters: Use Token Factory models within more of the coding agents and development tools your team already works with.

## Agentic Infrastructure | TavilyAgentic Infrastructure | Tavily

Improved search accuracy, broader coverage and new integrations.

### Ground agents in more accurate search resultsGround agents in more accurate search results

What changed: Tavily improved evidence ranking, deduplication, contradiction handling, index coverage and freshness. In its published evaluation, Tavily ranked #1 in accuracy across the providers tested on SealQA-Hard, SealQA-0 and SimpleQA-Verified.

Why it matters: Agents get more relevant evidence, with fewer redundant or conflicting results to work through.

### Find better evidence on people, companies and newsFind better evidence on people, companies and news

What changed: Tavily expanded coverage of people, companies and news to support workflows across sales, go-to-market, compliance, onboarding and market intelligence.

Why it matters: Help agents research prospects, understand markets, verify entities and gather evidence for risk assessments.

### Bring web search into more applications and agent workflowsBring web search into more applications and agent workflows

What changed: New integrations connect Tavily’s real-time search and extraction directly to Convex, OpenCode and NanoClaw.

Why it matters: Give applications, coding agents and assistants in Slack, Telegram and the CLI access to current web evidence with less custom integration work.

### Also this quarterAlso this quarter

- ISO 27001:2022 certified. Tavily’s information security management system is now certified to the latest ISO 27001 standard.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Contents

- 

Cloud Platform

- Connect securely to your on-premises data center or other cloud

- Benefit from new Preemptible VMs spot pricing

- Move data between object storage and Nebius Shared Filesystem

- Manage and better understand your stored data

- Control and account for cloud consumption

- Get from development to running workloads faster

- Extend your security posture management with Wiz

- Run cloud commands from your browser with Cloud Shell

- Automate infrastructure through REST

- Manage infrastructure in a AI-native way

- Also this quarter

- 

Managed Inference | Token Factory

- Optimize inference with a draft model trained on your data

- More open-weight models, including Day-0 releases

- Build agent workflows with the Responses API

- See what drives inference performance

- Run batch inference on capacity that scales to zero

- Use Token Factory in more coding workflows

- 

Agentic Infrastructure | Tavily

- Ground agents in more accurate search results

- Find better evidence on people, companies and news

- Bring web search into more applications and agent workflows

- Also this quarter

Sign in to save this post
Sign In
