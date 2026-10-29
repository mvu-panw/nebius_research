# DeepSeek R1 and V3: Chinese AI New Year started early

Source: https://nebius.com/blog/posts/deepseek-r1-v3-chinese-ai-new-year-started-early

Skip to main content

# The rise of DeepSeekThe rise of DeepSeek

DeepSeek consistently works on Mixture-of-Experts (MoE) models that are efficient and open. DeepSeek V2 was released in May 2024 and presented an interesting alternative to Llama 3 70B. Its English performance was slightly below that of Llama, but V2 outperformed Meta’s model on standard Chinese benchmarks.

DeepSeek V3 took another step forward, not only improving performance but also boasting three times faster inference times. It landed in December 2024 and has sent ripples through the AI community ever since. Built on an MoE architecture with a colossal 671 billion parameters, V3 activates only 37 billion parameters per token, keeping both computational load and energy usage low compared to other alternatives. Trained on 14.8 trillion high-quality tokens with Multi-Token Prediction for higher inference speed, DeepSeek V3 processes 60 tokens per second — three times faster than its predecessor. It clocks an 88.5 on the MMLU benchmark — just shy of the leading Llama 3.1 but outperforming notable competitors like Qwen 2.5 and Claude 3.5 Sonnet. On the DROP benchmark, it hits 91.6, showcasing formidable reasoning ability (thou shalt not discuss the problems thou hath with LLM reasoning in this post; thou shalt wait for a separate one). If you’re a programmer, pay attention: DeepSeek V3 outperforms Claude 3.5 Sonnet on Codeforces. I know — I also loved my Sonnet.

# Affordability and opennessAffordability and openness

Perhaps the biggest bombshell is DeepSeek V3’s permissive open-source license, allowing developers to download, tweak, and deploy the model freely — even for commercial projects. This open philosophy isn’t just ideological; it’s also economical. Training DeepSeek V3 cost around $5.58 million over two months — a fraction of what some big-name tech firms burn through. Suddenly, closed-source heavyweights have a real rival that can scale without draining bank accounts. DeepSeek R1 adds insult to injury, beating GPT-o1 on several benchmarks (source):

See in detail

# Data quantity is taken over by data qualityData quantity is taken over by data quality

The trend started by Phi in Textbooks Are All You Need has finally led to broad recognition: now that we have learned how to gather vast amounts of data, data quality controls are the real secret sauce of modern model development.

This is also one of the cornerstone ideas behind the Pleias project co-founded by me. In 2024, Pleias published the Common Corpus — the largest open and permissively licensed text dataset, comprising over 2 trillion tokens. However, it’s the extensive preprocessing tailored for RAG that enabled Pleias 1.0 family of models to punch above their weight on RAG benchmarks. I hope to write several posts on data preprocessing for “model winding” later.

# Frugality is the new blackFrugality is the new black

The open-source community is famously “compute-poor, ” meaning resources are often minimal compared to deep-pocketed labs. But this forced frugality can be a superpower: it drives more efficient algorithms, simpler architectures, and eco-friendly optimizations.

An interesting side note is that, even with constant efficiency improvements, training giant models still demands significant energy. This makes the location and design of clusters crucial. For instance, Nebius’ first own data center is located in Finland, leveraging natural air cooling to cut energy costs and reduce carbon footprints — a concept we often refer to as free cooling. This trend will only accelerate in 2025 as more AI developers and users learn to do more with less.

# AI that is truly open is catching upAI that is truly open is catching up

Closed-shop AI models in Silicon Valley, those “mammoths, ” are looking over their shoulders. DeepSeek V3’s arrival marks the latest step in a critical shift: open-source AI is no longer playing catch-up; it’s inching ahead on key benchmarks and real-world applicability.

I present to you Exhibit A: Sam Altman’s tweets hinting at intensifying competition.

OpenAI undeniably shifted public consensus on what is possible, but competition is intensifying, and the word “open” in its name no longer suffices. The recent announcement of Stargate contrasts with DeepSeek’s frugal approach, which delivers fully open models at a fraction of the cost.

If you want to host DeepSeek R1 in the EU with privacy in mind, it’s available on Nebius AI Studio for a super-competitive price: $0.8 per 1M input tokens. V3 is also live — you can go all in by including it into inference workloads.

Note

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

# The road aheadThe road ahead

It’s safe to say the “Chinese AI New Year” began with a bang a full month early this year. After all, the Year of the Wood Snake signifies “a time of transformation, growth, and introspection.” This applies to both up-and-coming startups and established incumbents in the genAI space. The question is no longer whether open-source AI will catch up, but rather how quickly it will lap the field — and who will harness it for the greatest impact.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius cloud

Sign up​
Docs​

Prof. Dr. Ivan Yamshchikov

## See also

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

Nebius opens its first availability zone in the United States

Scheduled to go live in Q1 2025, the Kansas City availability zone will house thousands of state-of-the-art NVIDIA GPUs, primarily H200 Tensor Core GPUs in the initial phase, with the energy-efficient NVIDIA Blackwell platform expected to arrive in 2025.

November 19, 2024
2 mins to read

### 

Transforming ideas into images: Introducing text-to-image generation on Nebius AI Studio

From concept art to product visuals, text-to-image AI is revolutionizing creative workflows, reducing hours of design work to mere minutes. Today, we’re excited to launch Nebius AI Studio’s text-to-image service, delivering premium, production-ready image generation at a fraction of typical costs.

January 22, 2025
4 mins to read

Sign in to save this post
Sign In
