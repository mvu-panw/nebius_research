# Nebius Token Factory Inference Service

Source: https://nebius.com/services/token-factory/inference-service

Skip to main content

## Unlimited scalability guarantee

Run models through our dedicated endpoints with autoscaling throughput and consistent performance. Scale seamlessly from prototype to production, no rate throttling, no GPU wrangling.

## Up to 3× cost efficiency

Experience transparent $/token pricing and right-sized serving for RAG, contextual and agentic use cases. Pay only for what you use, with volume discounts and optimized serving pipelines that deliver up to 3× better cost-to-performance (independently verified by Artificial Analysis).

## Ultra-low latency, verified

Our serving pipeline delivers sub-second time-to-first-token, validated by internal and third-party benchmarks. Multi-region routing and speculative decoding keep response times stable under load.

## Benchmark-backed model quality

All hosted models undergo internal validation for accuracy, consistency and multilingual robustness, ensuring production-grade results across diverse workloads.

## Choose speed or economy

Select between Fast and Base flavors. Fast is optimized for lowest latency and interactive workloads, and Base is cost-efficient for high-volume inference or background processing. Switch instantly, no redeploys required.

## No MLOps required

Token Factory gives you enterprise-ready infrastructure out of the box. Provision, deploy and scale without managing GPUs or clusters, our endpoints are already optimized for performance and reliability.

Zülküf Genç
Director of AI

“Prosus, the power behind some of the world’s leading lifestyle and e-commerce brands, has achieved up to 26x cost reductions compared to proprietary models. We move fast, test and iterate quickly, and the flexibility, products and quick responses from Nebius Token Factory allowed us to keep this pace all the way through production. By leveraging Nebius Token Factory’s dedicated endpoints, Prosus was able to secure guaranteed performance and isolation. The addition of autoscaling was the game-changer, allowing us to handle massive workloads of up to 200 billion tokens per day without manual intervention.”

Zülküf Genç
Director of AI

Alex Mashrabov
Founder and CEO

“Running inference at scale with healthy economics requires efficient on-demand and autoscaling capabilities. Nebius was the only provider that met our requirements — reducing overhead, simplifying management, and enabling us to deliver faster, more cost-efficient AI in production.”

Alex Mashrabov
Founder and CEO

Julien Chaumont
CTO

“Hugging Face and Nebius Token Factory share the same mission of making open AI accessible and scalable. By partnering with Nebius, we’ve been able to provide faster and more reliable inference for developers working with large open-source models.”

Julien Chaumont
CTO

Raghav Kohli
General Counsel, Partnerships

“Mithril and Nebius share a vision for making open AI production-ready. By leveraging Nebius Token Factory’s scalable infrastructure, from real-time to batch inference, we’re able to run and optimize large workloads efficiently while keeping the flexibility and transparency of open models.”

Raghav Kohli
General Counsel, Partnerships

## Benchmark-backed performance and cost efficiency

up to 4.5× faster

Time-to-first-token up to 4.5 times faster in Europe than other inference providers. Consistent sub-second latency validated by independent tests

more than 2.5× cheaper

Than GPT-4o with comparable quality on Llama-405B

Top-2 throughput worldwide

Verified on DeepSeek R1 0528 (248 output tokens/sec, outperforming major hyperscalers by up to 3×)

## Top open-source models available

OpenAI

gpt-oss-120B
A 120B-parameter open model delivering near-GPT-4-class performance on complex reasoning and code generation tasks, with transparent weights and fast inference throughput.

131k context

Open license

Moonshot AI

Kimi-K2-Instruct
High-accuracy generalist model optimized for reasoning, dialogue, and structured generation. Strong performance on multilingual and long-context tasks.

131k context

Proprietary open license

NousResearch

Hermes-4-405B
A 405B-parameter instruction model built for nuanced conversation, long-form reasoning, and alignment fidelity. A community-driven alternative to closed-weight instruction models.

128k context

Custom open license

ZhipuAI

GLM-4.5
Compact and efficient 128k-context model that delivers exceptional reasoning and code performance per token. A balanced choice for enterprises prioritizing cost-to-quality efficiency.

128k context

Apache 2.0 License

Qwen

Qwen3-Coder-480B-A35B-Instruct
Massive 480B-parameter code-specialized model for high-precision programming, reasoning and math. Features 262k context and fine-grained JSON control for structured output.

262k context

Apache 2.0 License

Qwen

Qwen3-235B-A22B-Thinking-2507
The latest large reasoning model in the Qwen family, delivering top performance on chain-of-thought and math reasoning. Designed for long-context enterprise workloads.

262k context

Apache 2.0 License

DeepSeek

DeepSeek-R1-0528
State-of-the-art reasoning model achieving GPT-4o-level performance on math, code, and logic. Independently verified by Artificial Analysis for leading throughput and inference speed.

164k context

MIT License

Nebius

And much more...
Take a look at our Playground to see the models available today. We're continuously adding new and diverse models to expand our offerings

## Join our community

Follow Nebius Token Factory' X account for instant updates, LinkedIn for those who want more detailed news, and Discord for technical inquiries and meaningful community discussions.
X/TwitterLinkedInDiscord

## 

A simple and friendly UI for a smooth user experience

Sign up and start testing, comparing and running AI models in your applications.
Try now

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
 model='meta-llama/Meta-Llama-3.1-8B-Instruct-fast'
)

Learn more about our API

## Optimize costs with our flexible pricing

### Start free

Get started in minutes with free credits to explore 60+ open-source models directly in the Playground or through API. No setup, no infrastructure to manage, just plug in your key and start generating.

### Flexible performance tiers

Choose between two optimized configurations to match your workload:

- Fast: sub-second responses for interactive agents, chat, or real-time inference.

- Base: cost-efficient throughput for large-scale or background processing. Switch tiers instantly, same API, same endpoints.

### Enterprise-ready deployment

Scale securely from prototype to enterprise, with predictable performance and transparent $/token pricing with:

- Guaranteed throughput and autoscaling.

- 99.9% SLA and regional routing.

- RBAC, unified billing and SOC 2 type II with HIPAA, ISO 27001 compliance.

## Nebius Token Factory prices

Scale from shared access to dedicated endpoints with 99.9% SLA, transparent $/token and volume discounts for production.
Check out our self-service pricesReach out for dedicated endpoints

## Q&A about Inference Service

Can I use your service for large production workloads?

Yes. Nebius Token Factory is built for large-scale, production-grade AI workloads.

Dedicated endpoints deliver sub-second inference, 99.9% uptime, and autoscaling throughput, ensuring consistent performance for workloads exceeding hundreds of millions of tokens per minute.

Scale seamlessly from experimentation to global deployment, no rate throttles, no GPU management.

I’d like to use another open-source model, what do I do?

We regularly onboard new open-source releases, including Llama, GPT OSS, Qwen, DeepSeek, Mistral and Flux, based on customer demand and benchmarking.

Enterprise users can also request model optimization or custom deployment support through our Solutions team.

Can I get a dedicated instance?

Yes. Dedicated endpoints provide guaranteed isolation, predictable latency, and reserved compute capacity. They include 99.9% SLA, custom autoscaling, and optional regional deployment in EU or US data centers. Contact our team to size your instance for your workload and compliance needs.

How do I deploy my custom fine-tuned models?

You can upload and host your LoRA or fully fine-tuned models directly through the Token Factory dashboard or API. Each deployment runs with transparent $/token pricing and inherits the same security and latency guarantees as standard endpoints.

Full post-training and distillation workflows will soon be available to simplify training, optimization, and deployment in a single pipeline.

How secure is your service and where does my data go?

We provide zero-retention mode, where requests and outputs are never stored or reused for training. All data is processed in facilities with SOC 2 Type II, HIPAA and ISO 27001 certifications. Data centers are located in Finland and France and US and meet EU and US data-residency requirements.

What are your rate limits and can they be increased?

Starter includes high defaults; enterprise removes caps. We size endpoints to your traffic profile. Enterprise customers can lift all limits, unlimited throughput, autoscaling to demand, and per-project tuning based on traffic profiles.

Need more? Reach out to our team, we’ll size your endpoint for your real-world workload.

How can I build RAG applications on your platform?

Nebius Token Factory includes all the building blocks for retrieval-augmented generation (RAG), like state-of-the-art embedding models and seamless integration with our chat and inference APIs. For more information, please check our cookbook.

What models do you support and can I request new ones?

You can request new models directly through your dashboard.

How does your pricing compare to other providers?

Pricing is transparent $/token, with clear input/output separation and volume discounts as you scale. No hidden infrastructure or idle GPU costs, pay only for what you serve.

Do you offer enterprise SLAs, support, and compliance options?

Yes. Enterprise customers benefit from:

- 99.9% SLA with reserved capacity.

- Dedicated Slack / support channel.

- Custom DPAs and compliance packages (SOC 2 Type II, HIPAA, ISO 27001).

- SSO, RBAC, and unified billing for secure team governance.

These options are designed for regulated industries and organizations running mission-critical AI in production.
