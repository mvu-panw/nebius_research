# SWE-rebench dataset: More than 21,000 open tasks for SWE LLMs

Source: https://nebius.com/blog/posts/swe-rebench-dataset

Skip to main content

The development of capable LLM-based software engineering (SWE) agents requires large-scale, diverse training data that reflects real-world scenarios, yet such datasets are scarce. At Nebius, one of our aims is to democratize AI and empower developers to build capable agents on top of open models. This is why we are releasing SWE-rebench — the next iteration of our work on curating datasets for agentic software engineering — which addresses this need by providing tasks mined and validated from thousands of open-source GitHub repositories using our fully automated pipeline.

Key features of the SWE-rebench dataset

- 

Massive scale: More than 21,000 interactive tasks from more than 3,400 GitHub repositories.

- 

Automated collection: Each task is collected via an automated process powered by a combination of carefully engineered heuristics and LLMs.

- 

Rich annotations: Includes installation configurations, dependency versions and LLM-assessed quality scores.

Alongside the dataset, we are releasing a technical report that details our automated collection pipeline and the dataset’s construction. This paper provides an in-depth look at the innovations enabling continuous task mining.

We believe SWE-rebench will be a valuable resource for training more capable SWE agents, and for benchmarking new models on realistic, interactive tasks. As an example, a curated subset of tasks mined using the SWE-rebench methodology already powers our public SWE-rebench leaderboard, which delivers decontaminated and standardized LLM evaluation on fresh real-world SWE tasks.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Ibragim Badertdinov
Lead ML Engineer at Nebius

## See also

### 

SWE-rebench: A continuously updated benchmark for SWE LLMs

Our AI R&D team presents SWE-rebench, a new benchmark for evaluating agentic LLMs on a continuously updated and decontaminated set of real-world software engineering tasks mined from real GitHub repositories. Our goal with this benchmark is to make evaluation of software engineering LLMs more transparent, reproducible and focused on core model capabilities.

May 14, 2025
1 min to read

### 

Scaling data collection for training software engineering agents

In this follow-up to our previous research blog post, we focus on the data collection process used to train our action generator and critic models. We’re also releasing two datasets on Hugging Face: nebius/SWE-bench-extra, containing 6,411 Issue/Pull-Request pairs, and nebius/SWE-agent-trajectories, featuring 80,036 software engineering agent trajectories, where an agent attempts to solve these issues.

December 20, 2024
9 mins to read

### 

Kvax: Fast and easy-to-use FlashAttention implementation for JAX

Today, we’re open-sourcing Kvax, our FlashAttention implementation based on JAX. Designed for efficient training with long sequences, Kvax supports context parallelism and optimized computation of document masks. It outperforms many other FlashAttention implementations in long-context training with dense packing, achieving state-of-the-art performance.

February 27, 2025
13 mins to read

Sign in to save this post
Sign In
