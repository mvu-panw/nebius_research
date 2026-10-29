# SWE-rebench: A continuously updated benchmark for SWE LLMs

Source: https://nebius.com/blog/posts/introducing-swe-rebench

Skip to main content

In today’s landscape of rapid LLM progress, static benchmarks quickly lose their relevance. As models are likely to encounter benchmark data during training, it’s becoming increasingly difficult to distinguish true generalization from memorization. Additionally, agent performance is heavily influenced not just by the model but by the surrounding scaffolding, such as prompts, additional test-time computations and available tools, making fair comparisons across systems challenging.

Today, we present a new LLM benchmark, SWE-rebench, which addresses these issues in SWE domain through:

- 

a standardized evaluation pipeline with fixed scaffolding;

- 

frequent dataset updates sourced from live open-source repositories;

- 

explicit contamination tracking tied to model release dates.

Figure 1. SWE-rebench leaderboard as of today

Our goal with this benchmark is to make evaluation of software engineering LLMs more transparent, reproducible and focused on core model capabilities.

You can explore the benchmark leaderboard and methodology behind it at swe-rebench.com.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Golubev
Lead ML Engineer

## See also

### 

Reasoning critics enable better parallel search for software engineering agents

In this short research blog post, we discuss how reinforcement learning-finetuned reasoning language models can be used as a better alternative to regression-based critics when performing parallel trajectory search in test time, and how to train such models to prioritize precision over recall.

May 1, 2025
10 mins to read

### 

Kvax: Fast and easy-to-use FlashAttention implementation for JAX

Today, we’re open-sourcing Kvax, our FlashAttention implementation based on JAX. Designed for efficient training with long sequences, Kvax supports context parallelism and optimized computation of document masks. It outperforms many other FlashAttention implementations in long-context training with dense packing, achieving state-of-the-art performance.

February 27, 2025
13 mins to read

### 

Scaling data collection for training software engineering agents

In this follow-up to our previous research blog post, we focus on the data collection process used to train our action generator and critic models. We’re also releasing two datasets on Hugging Face: nebius/SWE-bench-extra, containing 6,411 Issue/Pull-Request pairs, and nebius/SWE-agent-trajectories, featuring 80,036 software engineering agent trajectories, where an agent attempts to solve these issues.

December 20, 2024
9 mins to read

Sign in to save this post
Sign In
