# Building transaction foundation models on Nebius AI Cloud

Source: https://nebius.com/blog/posts/building-transaction-foundation-models-on-nebius-ai-cloud

Skip to main content

Firms are moving beyond task-specific models toward transaction foundation models: transformer architectures trained on proprietary transaction data that produce reusable embeddings across fraud, credit, personalization and risk. NVIDIA’s blog covers the shift and the institutions driving it, including Revolut. The Build Your Own Transaction Foundation Model developer example gives teams a starting point for building transformer embeddings on tabular data using NVIDIA CUDA-X and NVIDIA Nemotron.

This developer example is a training recipe, providing teams with the code and architecture required to build their own foundation model on their own data. It is also available with 1-click deployment on Nebius AI Cloud so teams can go from console to running an API endpoint in minutes instead of manually provisioning GPU instances, pulling container images, configuring networking and managing runtime dependencies. This post covers what comes next: the infrastructure that turns a blueprint into a production foundation model and what we’ve learned from a customer that’s already done it.

## From workflow to production modelFrom workflow to production model

The developer example handles the hardest conceptual leap: applying transformer architectures to tabular financial data rather than unstructured data such as text or images. But moving from a workflow to a production foundation model introduces a different set of challenges that are primarily about infrastructure:

Scale of data preparation. Production transaction foundation models train on billions of events that need joins, aggregations, deduplication and feature engineering before training begins. At this scale, CPU-based data processing becomes the bottleneck, not GPU training. GPU-accelerated data preparation with libraries like NVIDIA cuDF is what makes the pipeline tractable, processing billions of records in the same infrastructure where training runs.

Sustained multi-node training. Transaction foundation models aren’t fine-tuning jobs. They’re full pre-training runs that require sustained GPU compute over days or weeks, with high-bandwidth interconnects that determine whether multi-node training actually scales. The difference between a cluster that can run the workflow and one that can train a production foundation model is interconnect bandwidth and sustained throughput, not just GPU count.

Inference under financial-grade SLAs. Once trained, transaction embeddings need to be served in production, often in real-time fraud scoring and authorization flows where latency is measured in milliseconds and downtime has direct financial consequences. Training infrastructure and inference infrastructure are different workloads, and re-platforming between them adds operational risk.

Data residency and compliance. Transaction data is among the most regulated in any industry. Where it’s stored and processed isn’t just a preference, it’s a compliance requirement that can determine whether a project ships or stays in a sandbox.

## What production looks like: Revolut and PRAGMAWhat production looks like: Revolut and PRAGMA

Revolut offers a concrete example of what it takes to go beyond the developer example. Their transaction foundation model, PRAGMA, follows the same architectural approach: transformer embeddings trained on tabular transaction data. But at production scale: more than 40 billion events from 25 million users, trained on Nebius AI Cloud. PRAGMA was developed jointly by Revolut Research and NVIDIA, with NVIDIA researchers contributing to the training infrastructure design and evaluation methodology — making it a direct expression of how NVIDIA’s full-stack AI platform supports production-scale financial intelligence.

PRAGMA trained on a dedicated cluster of 64 NVIDIA H100 GPUs on Nebius, connected through high-bandwidth NVIDIA Quantum InfiniBand. NVIDIA cuDF handled data preparation across billions of records. The team achieved 3x faster pre-training efficiency and a 21% precision improvement on fraud detection, results that came from the combination of architecture and infrastructure, not architecture alone.

The PRAGMA paper details how compute requirements scale with model size. PRAGMA-S (10M parameters) trained on 16 H100 GPUs in two days. PRAGMA-M (100M) required the same 16 GPUs but two weeks of sustained training. PRAGMA-L (1B) scaled to 32 H100s over two weeks. Sequence packing and dynamic batching delivered 2–5x throughput improvements across all variants. Adapting the pre-trained model to new downstream tasks through LoRA (updating just 1–2% of parameters) took roughly one-eighth the wall-clock time of full pre-training. These numbers show what “production-scale training” actually means in GPU-hours and wall-clock time, and why infrastructure reliability matters as much as raw compute.

The model runs in three variants (10M, 100M, 1B parameters) serving different latency and precision tradeoffs. The 10M model handles real-time fraud detection; the 1B model targets precision-heavy tasks like credit scoring. New tasks are added through LoRA adaptation on 1–2% of parameters rather than full retraining. Inference runs through Nebius Token Factory with dedicated endpoints, the same infrastructure supporting Revolut’s FinCrime AI agents processing two million tasks per month.

This is the AI Factory model applied to model development itself: pre-train once on proprietary transaction data, then adapt rapidly to new downstream tasks — fraud, credit, lifetime value, product recommendation — without full retraining.

The key point is that: the NVIDIA AI blueprints provide the architectural starting point, the infrastructure underneath is what turns it into a production system. Read the full Revolut customer story here.

## Infrastructure for the full lifecycleInfrastructure for the full lifecycle

Nebius AI Cloud supports the full transaction foundation model lifecycle through data preparation, training and production inference.

The Build Your Own Transaction Foundation Model developer example is available with 1-click deployment from the Nebius AI Cloud console via the Containers-Over-VM service. Nebius pulls the correct container image, configures the GPU and exposes the API endpoint. This is the same deployment pattern already in production for NVIDIA NIM microservices and NVIDIA blueprints across life sciences, physical AI and other verticals on Nebius AI Cloud.

Training: GPU clusters with NVIDIA H100 GPUs connected through NVIDIA Quantum InfiniBand provide the sustained compute and bandwidth that foundation model pre-training requires. Nebius clusters deliver mean time between failures exceeding 100,000 GPU-hours and automated node replacement in under 10 minutes — critical when a two-week training run on 32 GPUs cannot afford to restart from scratch. Object storage provides 8 GBps read throughput for loading billion-event datasets into the training pipeline. NVIDIA CUDA-X libraries including NVIDIA cuDF run natively for GPU-accelerated data processing at scale.

Inference: Token Factory provides managed inference endpoints with autoscaling, dedicated resources and a 99.9% uptime SLA. Teams deploy fine-tuned model variants behind production-grade endpoints without managing serving infrastructure.

Data residency: Nebius operates from data centers in Finland with zero data retention and GDPR-ready infrastructure. Full control over deployment region, model selection and data handling. For financial institutions with EU regulatory requirements, this is a deployment prerequisite.

Retrieval: In production, model scores feed into downstream agents that need external context to act (sanctions lists, counterparty data, regulatory filings). Earlier this year, Nebius acquired Tavily, an agentic search API that gives AI agents grounded access to real-time web data.

## Get startedGet started

Explore the developer example and the infrastructure to run it at scale:

- Build Your Own Transaction Foundation Model developer example on build.nvidia.com

- Revolut on the Inference Frontier — full customer story

- PRAGMA: Transaction Foundation Models at Revolut — research paper

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- From workflow to production model

- What production looks like: Revolut and PRAGMA

- Infrastructure for the full lifecycle

- Get started

## See also

### 

Run physical AI workflows, not glue code

The Nebius Physical AI Workbench turns NVIDIA Cosmos 3, NVIDIA Isaac Sim, NVIDIA Isaac GR00T and other Physical AI tools into composable building blocks that agents can wire together. We are building it in the open, and it is available now on GitHub.

June 1, 2026
7 mins to read

### 

Data Lab: Your best dataset is already in your logs

Today, we’re launching Data Lab in Nebius Token Factory. It is a new workspace for turning production logs and existing datasets into reusable training data for post-training workflows. Data Lab helps teams explore inference logs, curate datasets and move directly into model iteration without rebuilding pipelines or copying production data across environments.

May 19, 2026
10 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

Sign in to save this post
Sign In
