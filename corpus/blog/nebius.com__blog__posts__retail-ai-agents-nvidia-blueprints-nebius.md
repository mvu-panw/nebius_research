# Inventory, store operations, and fine-tuning: Nebius provides early access to three NVIDIA retail agent blueprints

Source: https://nebius.com/blog/posts/retail-ai-agents-nvidia-blueprints-nebius

Skip to main content

An inventory agent’s purchasing recommendation can leave a retailer carrying excess stock or unable to fulfill orders, while a store operations agent needs clear limits on which systems it can access and what it can change. Both need constant evaluation as products, suppliers, and operating conditions change.

Nebius is running three new NVIDIA retail blueprints that address these challenges, launched at GTC Berlin. Building on the shopping assistant and catalog enrichment blueprints we brought to Nebius in June, this next set focuses on the retailer’s operations: testing inventory decisions, helping stores respond to incidents, and improving the models behind those workflows. Nebius provides the infrastructure for simulation and fine-tuning, the runtime for agents, and the inference services they call.

If you’re a retailer looking to deploy one of these blueprints, we’re offering a no-commitment POC. And if you’re looking to use the blueprints yourself, join the Nebius x NVIDIA webinar where we’ll walk through an example blueprint, deployment options on Nebius, and how to adapt it to your systems.

## Blueprint 1: inventory labBlueprint 1: inventory lab

Supply-chain planners need to understand the consequences of a purchasing decision before changing a real order. What happens to cost and fulfillment if a distribution center carries less safety stock? If a supplier’s lead time doubles? If the business changes how it replenishes slow-moving products?

NVIDIA’s Inventory Lab Blueprint combines agents with algorithms, mathematical solvers, and simulation to build and evaluate inventory replenishment policies. The policies can range from learned policies leveraging PyTorch or cugraph-gnn to optimized policies leveraging cuOpt. Agents orchestrate the end-to-end experiment workflow and development and evaluation best practices are enforced with a Nemotron as a judge. The initial goal is to reduce inventory costs while maintaining fulfillment.

The blueprint has four components:

- Supply-chain simulator: Models the movement of products through suppliers, distribution centers, and stores under uncertain demand and lead times.

- Developer agents: Build and test purchasing rules and models.

- Manager agent: Tracks the developer agents and decides which strategies to explore next.

- Arena and judge agent: Evaluate the strategies against the experiment’s objectives.

On Nebius, the experiments run as Slurm jobs on a Managed Soperator cluster of NVIDIA H100 GPUs. Nebius’ Managed Service for MLflow tracks runs so teams can compare results across different assumptions and purchasing strategies. The agents access their reasoning models through the Token Factory model catalog. The whole lab environment is managed through a Devlab running an integrated development environment (IDE) that grants access to the experiments and results.

## Blueprint 2: agent harness for store operationsBlueprint 2: agent harness for store operations

Resolving a store incident can require information from several systems and action from several people. An agent helping with that response needs relevant context, access to permitted tools, and boundaries around its actions.

NVIDIA’s Agent Harness for Store Operations Blueprint provides the framework for that workflow. It helps an agent identify an incident, propose a response, and guide a store manager through the next steps — including providing a morning brief report that highlights the most important information they need to know at the start of their day. Built with NVIDIA Agent Toolkit and an open-source agent runtime, it combines:

- Hermes agent: Manages memory, tool use, and task execution

- NVIDIA OpenShell: Provides a sandboxed runtime and policies governing system access, tool use, and inference traffic.

- Model routing: Directs requests to the appropriate model for the task.

- NVIDIA Nemotron 3 Ultra: Provides the reasoning model, with a vision model for image-based incidents.

In the Nebius deployment of the blueprint, Token Factory serves the models through its public endpoints — NVIDIA Nemotron 3 Ultra for reasoning and a vision model from the catalog for image-based incidents, with NVIDIA Nemotron 3 Nano Omni available as a dedicated endpoint for teams that want an all-Nemotron stack. The Hermes agent and its OpenShell sandbox run on a Nebius CPU virtual machine; no GPUs are needed on the agent side. Teams can scale the agent runtime and model inference independently, without managing a GPU cluster for inference.

## Blueprint 3: intelligent warehouse fine-tuning flywheelBlueprint 3: intelligent warehouse fine-tuning flywheel

A retail warehouse agent must interpret operational data, use enterprise systems and optimization tools correctly, and respect business constraints as products, processes, and operating conditions change. Training may begin without labeled examples, but the deployed agent must work with real warehouse data.

NVIDIA’s Intelligent Warehouse Fine-tuning Flywheel Blueprint turns synthetic data, model training, simulation, and operational feedback into a continuous improvement loop, built around NVIDIA Nemotron models and the NeMo platform:

- Build and expand training coverage: Use a Nemotron teacher model to generate domain-specific examples for labor allocation, inventory exceptions, wave management, and disruptions — including rare scenarios that production data may not capture often enough.

- Specialize and refine models: Use supervised fine-tuning to develop a compact Nemotron warehouse expert, then NeMo RL for reinforcement learning against a warehouse simulator to improve its decisions through reward feedback.

- Evaluate and deploy: Assess task performance, tool use, constraint adherence, and safety before a controlled rollout, with NeMo Guardrails and human oversight.

- Capture experience and repeat: Record operational context, actions, tool calls, and outcomes. Use newly discovered failures to improve datasets, evaluations, and subsequent training cycles.

On Nebius, the flywheel runs entirely on serverless services: teams iterate in Nebius Serverless AI DevLabs, run fine-tuning and evaluation as Serverless AI jobs on NVIDIA accelerated computing, and consume the base and improved models from Token Factory public endpoints — with no cluster to provision. Managed Service for MLflow tracks experiments and checkpoint versioning, and Token Factory serves the resulting models through dedicated endpoints. Together, these capabilities give teams a path from training and evaluating an updated model to deploying it behind the agent’s inference endpoint.

## Right-sizing infrastructure for each blueprint workloadRight-sizing infrastructure for each blueprint workload

Each blueprint comes with different demands on infrastructure. Inventory experiments need compute while simulations run, a store agent needs an application runtime and access to inference, while fine-tuning requires a separate training workflow, followed by evaluation before an updated model reaches users.

Catalog enrichment shows how these choices play out. A pipeline can turn a product photo and sparse metadata into localized descriptions, FAQs, and visual assets. Running that pipeline for thousands of products across multiple markets means deciding how to allocate compute across several models, and whether the work needs to happen interactively or in batches.

Teams can start with the models deployed together on a Nebius virtual machine with NVIDIA H100s. Managed Kubernetes allows them to separate model deployments and scale the busiest components independently. Token Factory provides managed inference for supported language, vision, and embedding models, reducing the number of model services the team operates itself.

A catalog refresh can run offline, while an interactive editing tool needs responsive inference. Model training can run separately from either workflow. Where enrichment needs supplementary product information from the web, Tavily can provide search and retrieval alongside the models.

The new blueprints follow the same principle: match the infrastructure to the work each step performs, connect the workflow to the retailer’s systems, and evaluate it against the business’s requirements.

## See the blueprints in actionSee the blueprints in action

Join Nebius and NVIDIA engineers in a practical webinar, where we’ll walk through an example blueprint, deployment options on Nebius, and how to adapt it to your systems.

To learn more about how retailers run AI on Nebius, see the Retail & Commerce solutions page.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Andrew Eliseev
Head of GTM Retail & Commerce AI

Manuel Gomez
Solutions Architect

David Schulman
Senior Director of Partner Marketing

Contents

- Blueprint 1: inventory lab

- Blueprint 2: agent harness for store operations

- Blueprint 3: intelligent warehouse fine-tuning flywheel

- Right-sizing infrastructure for each blueprint workload

- See the blueprints in action

## See also

### 

Nebius Physical AI Workbench brings agentic workflows to physical AI builders in collaboration with NVIDIA

Customers using Nebius Physical AI Workbench report up to 40% less engineering time with AI agents operating robotics workflows directly. Built in collaboration with NVIDIA and open source on GitHub, it runs data generation, simulation, training, and evaluation in one place. This release adds NVIDIA Cosmos Data Factory and a sim-to-real workflow co-designed with Sereact for Zalando returns.

October 21, 2026
5 mins to read

### 

Introducing the Nebius Agents Blueprint: open architecture for production-ready AI agents

Today we’re introducing the Nebius Agents Blueprint, an open reference architecture for building, operating, and continuously improving AI agents in production. This post covers the six-component composable stack — inference, orchestration, retrieval, grounding, observability, and simulation — and the case study behind it: a compliance audit agent that achieved 72% lower cost and 20% higher precision over a GPT-based prototype by improving the system, not the model.

June 10, 2026
6 mins to read

### 

NVIDIA retail AI blueprints, now running on Nebius

Nebius has collaborated with NVIDIA to bring two retail AI blueprints to production on Nebius infrastructure: the NVIDIA Agentic Commerce Blueprint and the NVIDIA Retail Catalog Enrichment Blueprint for automated product content. Both are open-source reference architectures built on NVIDIA NIMs that retailers and developers can customize and deploy today with a 1-click deployment on Nebius AI Cloud.

June 5, 2026
5 mins to read

Sign in to save this post
Sign In
