# Meet SWE-rebench-V2: A multilingual, executable dataset for training Software Engineering Agents

Source: https://nebius.com/blog/posts/meet-swe-rebench-v2

Skip to main content

We’re introducing SWE-rebench-V2, the next iteration of our large-scale dataset of reinforcement learning (RL) environments for training autonomous software engineering agents (SWEs).

Despite rapid progress in SWE agents, training remains constrained by limited access to diverse, executable, open-source data. To address this gap, we built a fully automated, language-agnostic pipeline for extracting real-world software engineering tasks at scale, allowing us to collect and release this new dataset of training tasks.

SWE-rebench-V2 includes:

- 

32,000+ executable tasks, each with a pre-built Docker environment;

- 

Coverage across 20 programming languages;

- 

100,000+ additional tasks derived from pull requests.

This release is designed to support large-scale, multilingual RL training.

## Key featuresKey features

Executable environments

Every task comes with a pre-built Docker container, enabling reproducible execution out of the box. Environments are configured automatically using a custom interactive setup agent that resolves dependencies and prepares the runtime.

Multilingual at scale

The dataset spans 20 programming languages, including both major ecosystems and underrepresented languages such as Lua and Scala. This enables research on cross-language reasoning and improves robustness beyond Python-only datasets.

Quality filtering and structured metadata

Tasks are filtered and labeled using an ensemble of LLMs. We also extract method signatures exercised by the test suite and generate problem descriptions for pull request–derived tasks, ensuring complete and structured training signals.

## Technical reportTechnical report

Alongside the dataset, we are releasing a technical report detailing the extraction pipeline, filtering methodology and a diagnostic study evaluating modern models on these tasks.

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

Behind SWE-rebench: Infrastructure to collect massive datasets of SWE tasks and evaluate agents at scale

Research on SWE agents involves building and running thousands of containers, quickly surpassing the limits of a single host. Our AI R&D team unveils the large-scale infrastructure that powers this research — the backbone behind recent releases such as SWE-rebench — and an open-source part of it to support the broader community.

November 7, 2025
14 mins to read

### 

SWE-rebench dataset: More than 21,000 verifiable tasks for SWE agents

Our AI R&D team announces the open-source release of the SWE-rebench dataset of more than 21,000 real-world, interactive software engineering tasks. For a detailed methodology and technical report, please see our accompanying paper on arXiv.

June 10, 2025
1 min to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
