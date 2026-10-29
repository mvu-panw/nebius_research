# Building Dawn. AI-powered mental health wellbeing support: Available anytime, for anyone

Source: https://nebius.com/customer-stories/swordhealth

Skip to main content

## Long story shortLong story short

Sword Health built Dawn, a direct-to-consumer AI wellbeing specialist, to extend mental health support beyond traditional clinician-led care. To make long, safety-sensitive conversations work at scale, Sword Health paired its clinical rigor, MindGuard guardrails and MindEval evaluation framework with Nebius infrastructure. Custom speculative decoding on dedicated Blackwell endpoints let Dawn jump from a 30B model to 200B+, while cutting tail latency from over 20 seconds to under 12 in production today.

Sword Health is an AI care company founded in 2015 that delivers clinically grounded digital health support across musculoskeletal, pelvic, movement and mental health. The company serves employers, health plans, unions and other healthcare organizations, combining AI systems with clinical oversight to expand access, improve outcomes and lower costs. In the case story, Sword Health is shown extending that model with Dawn, an AI wellbeing specialist built for continuous mental health support at scale.

## ContentsContents

A decade of AI Care, now expanded to mental wellbeing

Why mental health AI needs clinical-grade safety

Rebuilding the inference stack for long conversations

From 30B to 200B+: Scaling Dawn without slowing down

Nebius infrastructure behind production-ready AI care

Millions of people struggle with mental health challenges or chronic conditions that require weeks or months of sustained care. Healthcare systems designed for one-on-one care can become strained when clinicians are not readily available. Technology can bridge that gap, bringing clinical judgement, therapeutic expertise and human empathy to more people through AI, while keeping clinicians central to the experience. Sword Health was founded to make that vision a reality.

## A decade of AI Care, now expanded to mental wellbeing

Since 2015, Sword Health has been building AI Care — a model of healthcare delivery where artificial intelligence and clinicians work together to deliver better outcomes at scale. Sword began with musculoskeletal (MSK) health, developing proprietary computer vision and pose-tracking models to guide exercise sessions entirely through AI. From there, Sword expanded into pelvic health with Bloom and movement health with Move, steadily broadening its clinical reach while deepening its AI capabilities.

Running in parallel, Sword has been investing heavily in Phoenix, Sword’s conversational AI platform. Initially built on third-party providers, Phoenix evolved into a suite of fine-tuned small and medium-sized open models (sub-30B parameters) that act as intelligent co-pilots for clinicians, handling between-session patient messaging and ongoing engagement at scale.

Last year, Sword took its first step into mental health with Mind, a B2B solution that follows the same clinician-in-the-loop model that has defined Sword’s products from the start. Now, with Dawn, Sword is breaking new ground: a direct-to-consumer mental health wellbeing solution powered entirely by AI, with no clinician in the loop. Dawn represents a fundamentally new delivery model — one built on a decade of proprietary AI development.

Today, Sword Health serves thousands of organizations across 82 countries, and delivered 10 million AI-guided sessions in 2025 alone. Already in 2026, Sword Health has welcomed 150,000 new enrollments and remains cashflow-positive despite continued investment in model training, inference infrastructure and clinical expertise.

Dawn acts as an AI wellbeing specialist that chats with users, analyzes their progress and helps optimize their long-term recovery journey. Most AI systems are designed for short feedback loops for problems like coding assistants or math solvers, where success is immediate and measurable. Healthcare is fundamentally different. A person recovering from chronic pain may interact with the system dozens of times over several weeks. Mental health wellbeing support may be more involved and much longer, involving months of ongoing conversations. Recovery takes time, and the signals that tell you whether it’s working are delayed and sparse.

“You’re not optimizing for a single response, or an instant response, ” explains Ricardo Rei, Head of AI Research at Sword Health. “Like any clinical setting, you’re optimizing towards the highest quality outcomes that may only become clear after many interactions. That means we have long histories filled with critical insights, and very few shortcuts.”

This is why Sword Health builds its AI systems in close collaboration with on-staff clinicians, who define evaluation criteria, safety boundaries and real-world validation protocols from day one. “Clinical expertise cannot be added later, ” says Rei. “If clinicians aren’t designing the system from the beginning, it’s easy to build entirely the wrong thing.”

## Why mental health AI needs clinical-grade safety

Building an AI system capable of supporting mental health wellbeing at scale requires both a highly capable language model, a welcoming and familiar user experience, and robust safety infrastructure. At the heart of Dawn is MindGuard, Sword Health’s open-source guardrail model, which screens every user message for distress signals before they ever reach the core model. When a signal is detected, MindGuard flags it and informs the LLM before a response is generated. This ensures Dawn can respond with the appropriate level of care and urgency.

However, running a guardrail model in-line adds latency to every interaction, becoming the architecture tradeoff they didn’t want to make. For a mental health wellbeing system, that tradeoff is non-negotiable. Safety cannot be an afterthought.

# Rebuilding the inference stack for long conversationsRebuilding the inference stack for long conversations

Equally important is how Sword Health evaluates Dawn’s performance. Traditional AI benchmarks aren’t designed for mental health because they measure accuracy of single responses, which are more useful for coding or math, not wellbeing. MindEval, Sword Health’s open-source clinical evaluation framework, is designed to assess quality across long, multi-session conversations. It tracks whether the system is genuinely supporting a user’s wellbeing over time, not just generating plausible responses. They chose not to show the typical streaming answers often used by popular chat systems, opting instead for final, thorough answers shown when ready. Together, MindGuard and MindEval reflect Sword Health’s belief that clinical rigor and AI safety must be built in from the start, and that the broader research community benefits when these tools are shared openly.

That distinction between AI answers and AI care is what brought Sword Health to Nebius. In mid-2025, Ricardo Rei was looking for a partner to help solve two of Dawn’s most demanding challenges, training a model that could meet Sword Health’s clinical quality standards, tight healthcare governance and regulatory requirements, and serving it at the best possible price-to-performance ratio.

“The hardest part of healthcare AI isn’t building a model, ” Ricardo explains. “It’s building a complete system that can support real interactions every day, from everywhere.” Over the past twelve months, the team re-architected their approach from the ground up, avoiding common pitfalls and making what Rei describes as a generational leap in the quality of AI Care.

“Designing Dawn requires access to specialized infrastructure, deep health-specific governance, genuine clinical expertise and a lot of specialized data, ” he says. “It requires clinical-grade reasoning from a highly capable model, but also system stability, reliability and consistency across every single interaction. Every conversation builds trust.”

The partnership quickly expanded beyond Dawn. Sword Health migrated its AI Vision models to Nebius cloud, which now powers Thrive, Sword Health’s musculoskeletal care solution that delivered approximately 4 million AI-guided sessions in 2025 alone. With Nebius infrastructure at its core, Sword Health has achieved predictable latency, high reliability and meaningful cost savings, all foundational to scale from day one.

## From 30B to 200B+: Scaling Dawn without slowing down

A Nebius build-a-thon in December became a turning point. The team had been working with a 30B model that wasn’t quite meeting the quality bar Sword Health had set for Dawn. The assumed answer to quality seemed both clear and risky. A significantly larger reasoning model would typically improve the quality of answers, but also make production inference slow down. Reasoning models carry their own overhead, and when MindGuard was used sequentially, known as cascading, it added more latency and more complexity to every interaction.

The answer was not a hardware problem or scaling GPUs, it sat with the inference architecture. The non-streaming user experience, and the cascaded models (Mindguard +MindEval) had to operate inside a strict <12s P99 window and treated with a single latency budget. The Nebius Token Factory team deployed custom speculative decoding trained specifically for Sword Health on dedicated NVIDIA Blackwell endpoints. Achieving a draft model acceptance rate of over 50% meant Dawn could make the leap to a model with over 200B parameters, roughly eight times larger, without becoming unbearably slow in production. They established a baseline, diagnosed tail latency that came down from more than 20 seconds to under 12, and then decided it was ready to move to production.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Nebius infrastructure behind production-ready AI care

Within a month, Sword Health deployed their production instance on Nebius Token Factory by using dedicated NVIDIA Blackwell endpoints. The magic came through custom speculative decoding, KV caching and prefix-aware routing, keeping response times tight on a 200B+ parameter model even using both the guardrail screening and multi-step reasoning. Running in BF16, the setup eliminates concerns about quality degradation from quantization.

The result was a system that cleared Sword Health’s quality bar and reduced tail latency without compromising the responsiveness that real-world users expect.

Dawn maintains a continuous, detailed understanding of each user’s wellbeing journey across sessions, conversing naturally, adapting to users’ progress and surfacing meaningful summaries for clinical review when needed. The goal is to bring the highest quality, most affordable mental health wellbeing support to anyone who needs it.

“AI is the only way to deliver personalized healthcare at global scale, ” Rei says. “Without it, there simply aren’t enough highly skilled humans to meet that need.”

Sword Health’s mission has always been ambitious, to free two billion people from pain by redefining how care is delivered globally. This vision depends on AI systems capable of delivering clinical-grade guidance safely, reliably and at scale. Nebius provides the infrastructure that makes that possible — flexible, high-performance and built to evolve alongside the models that power it.

## More exciting stories

## 

vLLM

Using Nebius’ infrastructure, vLLM — a leading open-source LLM inference framework — is testing and optimizing their inference capabilities in different conditions, enabling high-performance, low-cost model serving in production environments.
Read the story

## 

SGLang

SGLang, a pioneering LLM inference framework, teamed up with Nebius AI Cloud to supercharge DeepSeek R1’s performance for real-world use. The SGLang team achieved a 2× boost in throughput and markedly lower latency on one node.
Read the story

## 

London Institute for Mathematical Sciences

How well can LLMs abstract problem-solving rules and how to test such ability? Research by the London Institute for Mathematical Sciences, conducted using our infrastructure, helps to understand the causes of LLM imperfections.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
