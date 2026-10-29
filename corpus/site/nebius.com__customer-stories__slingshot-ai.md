# Training Ash, Slingshot AI’s foundation LLM for psychology

Source: https://nebius.com/customer-stories/slingshot-ai

Skip to main content

## Long story shortLong story short

Slingshot AI is developing a foundation LLM for psychology to address the global need for mental health support. Ash is a chatbot designed to provide long-term support by helping users identify patterns and meet developmental goals. By collaborating with Nebius, Slingshot ran Ash’s large-scale AI training, fine-tuning and inference workloads on high-performance GPU clusters — ensuring a fast and seamless model development cycle.

Slingshot AI, a New York-based startup, is pioneering new technologies for mental health. With $93 million raised and a leadership team featuring Casper co-founder Neil Parikh and AI expert Daniel Reid Cahn, Slingshot develops AI mental health tools that offer adaptive guidance and evidence-based support tailored to each user. Their app Ash is grounded in psychological insights and uses a foundation model for psychology.

## ContentsContents

The quiet mental health evolution

One billion people with mental health needs

Training recipe and reward signals

Streamlining workflows with SkyPilot

Guardrail architecture for emergencies

## The quiet mental health evolution

As mental health struggles such as anxiety and depression continue to maintain all-time highs, we’re witnessing a quiet but major shift in the landscape of support. Today, the largest provider of mental health support in the world is likely not a network of trained specialists, but general-purpose AI chatbots — tools that were never trained on psychological data and operate with little relevant oversight.

And that is precisely what Slingshot AI aims to change. While general-purpose AI models offer immediate access, they aren’t designed for sensitive mental health support and lack clinical safeguards. This is where Ash comes in.

Ash is Slingshot AI’s flagship voice/text chatbot, trained on the world’s largest and most diverse behavioral health dataset to become the first foundation model for psychology. The goal was to teach Ash not just what professionals say, but the action grammar and art of human support itself.

Nebius provided enterprise-grade GPU clusters and cloud infrastructure to train and optimize Ash’s AI models quickly and securely. Launched in July 2025, Ash now scales globally as a free Android and iOS app, relying on Nebius for re-training jobs, RL and inference for some of its models.

Slingshot AI was one of the winners of Nebius’ inaugural AI Discovery Award — a nod to their creative approach and technical ambition. Recognition from Nebius gave the team a welcome boost as they scaled up, with access to an infrastructure that lets innovators move fast from bold ideas to real-world impact.

## One billion people with mental health needs

Ash’s debut is timely — the numbers tell a story of a mental health system buckling under demand. More than 1 billion people are living with mental health needs, and only 9% of those with depression receive minimally adequate treatment, according to the World Health Organisation. In the U.S., the story is no different, as an estimated 23% of Americans struggle with their mental health and only half receive any help.

This is the gap Slingshot AI was built to fill — not by replacing humans, but by creating a new type of support for the high volume of everyday struggles such as stress, anxiety, relationship troubles and more. Ash operates 24/7 and will cost less in a year than a single session of traditional support.

Co-founded by Neil Parikh, who previously scaled sleep products manufacturer Casper to an IPO, and Daniel Cahn, an AI engineer with experience in mental health crisis technology, Slingshot raised $93 million from investors including a16z, Radical Ventures and Forerunner Ventures.

Slingshot AI’s technology takes a very different path from other mental health apps. Instead of building a ChatGPT-wrapper and tweaking it with freudian-style prompts, Slingshot devoted 18 months to training Ash to build something fundamentally new.

## Training recipe and reward signals

The training process for a psychology LLM involves learning from a large collection of behavioral health data. The model absorbs therapeutic language, frameworks and techniques. These include diverse approaches like Cognitive Behavioral Therapy, Acceptance and Commitment Therapy, psychodynamic methods, Gestalt, motivational interviewing and more.

Clinicians then adjust the model to evolve the support to a digital AI context and build in guidance for complex health situations. General-purpose AI assistants are trained to tell users what they want to hear. Effective support often requires the opposite, a thoughtful journey that involves tension. Teaching an AI to push back appropriately requires extensive work during the fine-tuning phase.

Ash’s final training phase uses reinforcement learning. The model continuously improves by analyzing conversation outcomes and user behavior, creating a feedback loop that optimizes therapeutic interventions over time — something human therapists rarely employ at scale.

RL requires a reward signal to function. The reward system for Ash’s AI relies on a combination of expert-driven evaluation and user-generated signals. One of its sources is a reward model trained on thousands of comparisons written by clinical experts, ensuring the AI’s actions align with positive, long-term clinical outcomes.

Alongside this, the team gathers feedback signals from real user sessions — including ratings, actions like returning to the app and nuanced linguistic cues—distilling these into a comprehensive value model that captures engagement across hundreds of thousands of interactions.

Additionally, Ash leverages an “LLM-as-a-judge” scheme, using a strong general model to provide comparative scores. To balance all inputs, the system assigns the greatest weight to expert-driven reward models, then blends value signals from users and LLM evaluations into a final score that guides the AI toward effective therapeutic behavior.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Streamlining workflows with SkyPilot

To achieve an optimal latency balance and improve support quality, Ash is mixing models of different sizes, from 32B to 235B, throughout the dialogue. They were trained on fast Nebius clusters with technologies like DeepSpeed and Zero-3 that reduce memory consumption and eliminate redundant data copies. Another great tool for streamlined operations, SkyPilot, helped automate training runs and reduced the infrastructure burden for developers by removing the need to manage remote GPU servers directly.

“Training on Nebius is multiple times cheaper than using training API providers that charge a noticeable margin for convenience. With tools like managed SkyPilot, the workflow becomes just as smooth while keeping the cost dramatically lower, ” says Slingshot’s ML Infrastructure Lead Alexey Bukhtiyarov.

Switching to powerful Nebius infrastructure made it much easier to start training the large Qwen3-235B backbone and “push the frontier of specialized AI for mental health”, Bukhtiyarov says. Looking ahead, his team is planning to deploy managed Kubernetes for inference to automate scaling and efficiently handle fluctuating user loads.

## Guardrail architecture for emergencies

Enterprise-class security is a must for apps that work with sensitive data. Nebius infrastructure is compliant with SOC 2 Type II with HIPAA, ISO 27001 and other certifications that ensure health data privacy and cloud protection.

Another critical element for a mental health app is a robust crisis management system. Ash must detect situations requiring immediate human intervention and redirect users to emergency services.

For this, the model uses a two-pass guardrail architecture. The first pass is a fast classifier that scans user inputs for signs of unsafe requests before the model processes them.

Any input that gets flagged then goes through an additional check by an LLM tuned for safety. This layer decides whether to block the content, replace it, or allow it to pass. Every flagged session is reviewed by a clinician to confirm that the AI gave appropriate information, like emergency contacts.

A study conducted by New York University and Slingshot AI found that Ash identified moments of risk with 100% accuracy across multiple tests and human reviews. “It’s an early signal, but an encouraging one, that when designed thoughtfully, AI can be transparent, responsible and deeply pro-human, ” Slingshot AI co-founder Neil Parikh said.

During a 10-week trial, 76% of users reported decreased depression symptoms, and 77% measured lower anxiety levels — improvements that rival those achieved through traditional therapy, according to the study.

The $2 billion AI mental health market is projected to reach $12 billion by 2034, driven by the demand for accessible and personalized interventions. In contrast to general-purpose conversational AI, mental health apps are built for the most sensitive job and require dedicated, expert-tuned LLMs like Ash, running on secure and scalable AI infrastructure like Nebius.

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
