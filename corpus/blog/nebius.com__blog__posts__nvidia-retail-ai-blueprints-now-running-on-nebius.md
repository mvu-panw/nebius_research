# NVIDIA retail AI blueprints, now running on Nebius

Source: https://nebius.com/blog/posts/nvidia-retail-ai-blueprints-now-running-on-nebius

Skip to main content

Nebius has collaborated with NVIDIA to bring two retail AI blueprints to production on Nebius infrastructure: the NVIDIA Agentic Commerce Blueprint and the NVIDIA Retail Catalog Enrichment Blueprint for automated product content. Both are open-source reference architectures built on NVIDIA NIMs that retailers and developers can customize and deploy today with a 1-click deployment on Nebius AI Cloud.

According to NVIDIA’s 2026 State of AI in Retail and CPG survey report, 47% of retailers are already exploring agentic AI and 42% are investing in catalog enrichment, making agentic commerce and product discovery two of the fastest-growing applications in digital retail. These blueprints give both use cases a production-ready architecture.

## Retail’s AI execution challengeRetail’s AI execution challenge

The ambition is clear, with 91% of retailers and CPG organizations actively using or assessing AI (up from 75% two years ago), and nine in ten executives planning to increase their AI budgets this year. The business case is proven, with 89% report AI is helping increase revenue, and 95% say it’s already reducing costs.

But the industry is hitting an execution wall. Nearly half of retailers (47%) are exploring agentic AI, yet most are still in pilot with only 20% having deployed agents. A top implementation barrier is the AI Talent gap, cited by 46% of respondents, up from 31% last year. And as digital commerce grows — now the focus for 61% of respondents — the need for production-ready architectures that teams can deploy without building from scratch has never been more urgent.

The gap isn’t strategy, it’s execution infrastructure. Retailers need production-ready architectures they can deploy now, on infrastructure built for open-model inference at scale.

## Blueprint 1: Retail agentic commerceBlueprint 1: Retail agentic commerce

NVIDIA’s Retail Agentic Commerce blueprint is a reference architecture for AI-powered, protocol-based commerce. It implements the Agentic Commerce Protocol (ACP) and Universal Commerce Protocol (UCP) — open standards that define how AI agents discover products, negotiate promotions and complete transactions on behalf of shoppers, while keeping merchants in full control of pricing, policies and fulfillment.

The blueprint is built on NVIDIA NIM microservices and the NeMo Agent Toolkit:

- Nemotron-Nano-30B-A3B NIM: Compact LLM for natural-language product conversations, checkout negotiation and multi-turn shopping interactions

- NV-EmbedQA-E5-v5 NIM: Semantic search over product catalogs at scale

- Four specialized agents: Search, recommendation, promotion and post-purchase — each scoped to a specific commerce workflow with merchant-defined guardrails

- ACP/UCP protocol layer: Merchant API and Payment Service Provider integration for secure, delegated payment flows

Full architecture is here

This maps to where retailers are headed: 57% of organizations are focused on agentic AI to increase process speed and efficiency. The blueprint gives these teams a production-ready starting point — and Nebius AI Cloud gives them the infrastructure to run it at scale.

Agentic commerce is a space Nebius is investing in broadly. Earlier this year, Nebius acquired Tavily, an agentic search API that gives AI agents grounded access to real-time web data. While Tavily isn’t a component of this blueprint, the acquisition reflects Nebius’s commitment to building the infrastructure layer that agentic AI applications need to run in production.

## Blueprint 2: Retail Catalog Enrichment blueprintBlueprint 2: Retail Catalog Enrichment blueprint

NVIDIA’s Retail Catalog Enrichment blueprint automates the pipeline from raw product images to rich, structured, localized catalog entries — addressing the “sparse data” problem where product images arrive with minimal or inconsistent metadata and teams spend significant time writing and localizing content for each SKU.

The blueprint chains four NVIDIA NIM microservices in a three-stage pipeline — visual analysis, 2D image generation and 3D asset creation:

- Nemotron-Nano-12B-V2-VL NIM: Vision-language model for attribute extraction, localization and quality scoring;

- Nemotron LLM NIM (Llama-3.3-Nemotron-Super-49B): Text generation for brand-aligned product copy and culturally-aware image prompts;

- FLUX.1-Kontext-Dev NIM: Lifestyle 2D imagery with culturally appropriate backgrounds;

- TRELLIS NIM: Interactive 3D .glb assets from 2D product photos.

Full architecture is here

The pipeline chains multiple models per product, multiplied across thousands of SKUs and locales — so the economics of inference at scale are the difference between a demo and a production deployment. NVIDIA Nemotron vision-language models are already live on Nebius AI Cloud. The blueprint’s web search stage (used to gather supplementary product data during enrichment) will be powered by Tavily, connecting Nebius’s recent acquisition directly into a production retail workflow.

## Why Nebius AI CloudWhy Nebius AI Cloud

Both blueprints are open-source reference architectures built on NVIDIA NIM microservices. They can technically run on any cloud with the right GPUs. What Nebius brings is purpose-built AI infrastructure and a direct collaboration with NVIDIA to make deployment fast and production-ready.

- GPU compute for NIM deployment: Both blueprints require GPU compute to run their NIM containers. Nebius provides the throughput production retail demands — peak-hour traffic for Agentic Commerce, catalog-scale batch processing for Enrichment. Infrastructure scales with the workload.

- Managed inference through Token Factory: For teams that prefer API-based model access, Token Factory provides managed inference endpoints with autoscaling and a 99.9% uptime SLA. Optional — the blueprints run self-hosted—but it simplifies operations for teams focused on the application layer.

- Open-model flexibility: Nebius supports the open models these blueprints are built on (Nemotron, Llama and the broader NVIDIA NIM ecosystem) and gives retailers the flexibility to swap, fine-tune or extend models as their needs evolve.

- Infrastructure you control: Full control over deployment region, model selection and data residency. Nebius operates from local data centers with zero data retention and compliance-ready infrastructure.

- Secure, real-time web search: Tavily’s agentic search can be leveraged directly in the Catalog Enrichment pipeline, powering the web search stage that gathers supplementary product data during enrichment.

Teams can deploy both blueprints from the Nebius AI Cloud console. For Agentic Commerce, Nebius pulls the required NIM containers — Nemotron-Nano-30B-A3B and NV-EmbedQA-E5-v5 — configures GPU allocation, and exposes API endpoints. For Catalog Enrichment, Nebius handles the NIM container orchestration across the four-model pipeline on Managed Kubernetes, with GPU resources allocated to match each model’s requirements. In both cases, teams go from blueprint to running deployment without managing container builds, CUDA versions or model-specific environment configurations.

## Building on a proven collaborationBuilding on a proven collaboration

These retail blueprints extend a collaboration between Nebius and NVIDIA that has already delivered production results. At GTC 2026 in March, the two companies announced the Physical AI Data Factory blueprint — a reference architecture for robotics and autonomous systems running NVIDIA OSMO, NVIDIA Cosmos and NVIDIA Isaac Sim on Nebius infrastructure. That blueprint established the pattern: NVIDIA designs the reference architecture, Nebius provides the production infrastructure to run it.

The pattern holds for retail. With 79% of retailers saying open-source models and tools as important to their AI strategy and the talent gap now the number one implementation barrier, the combination of NVIDIA’s open-source blueprints and Nebius’s managed inference infrastructure is designed to close the gap between AI ambition and production deployment.

Nebius already powers AI workloads for leading commerce and visual AI companies including Shopify and Photoroom.

## Get startedGet started

Both blueprints are available as open-source references on NVIDIA’s build platform. To run them on Nebius:

- Explore the NVIDIA Agentic Commerce blueprint and the NVIDIA Retail Catalog Enrichment blueprint

- Read the Nebius AI Cloud docs

- Register for our upcoming webinar

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- Retail’s AI execution challenge

- Blueprint 1: Retail agentic commerce

- Blueprint 2: Retail Catalog Enrichment blueprint

- Why Nebius AI Cloud

- Building on a proven collaboration

- Get started

## See also

### 

Run physical AI workflows, not glue code

The Nebius Physical AI Workbench turns NVIDIA Cosmos 3, NVIDIA Isaac Sim, NVIDIA Isaac GR00T and other Physical AI tools into composable building blocks that agents can wire together. We are building it in the open, and it is available now on GitHub.

June 1, 2026
7 mins to read

### 

Nebius partners with Positronic on Physical AI Leaderboard (PhAIL)

Physical AI is moving from controlled demos to real-world deployment — and that shift demands benchmarks grounded in actual operations, not lab conditions. Today, Nebius joins Positronic as a founding consortium partner of the Physical AI Leaderboard (PhAIL), a new platform that evaluates robot AI models on real hardware using commercially relevant tasks and production-grade metrics.

March 31, 2026
5 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

Sign in to save this post
Sign In
