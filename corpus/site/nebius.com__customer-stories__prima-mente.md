# Scaling Pleiades: Uncovering the brain’s biology with Prima Mente

Source: https://nebius.com/customer-stories/prima-mente

Skip to main content

## Long story shortLong story short

Prima Mente is building foundation models to uncover what’s happening in the brain without directly accessing it. With a 32-GPU reserved cluster in Nebius, Prima Mente amped up pre-training throughput by 12%, processing 1.19 million tokens/s on 16 nodes, a critical step in their goal toward scaling model size from 7B up beyond 100B parameters.

Supported by the UK’s Sovereign AI Fund and awarded by Gates Ventures for advancing Alzheimer’s research, Prima Mente bridges data generation, AI modeling and wet lab experimentation to enable earlier diagnostics and new therapies for neurodegenerative diseases.

## ContentsContents

Introduction

Seeing what we cannot observe

Infrastructure for better science: Building Pleiades

How Nebius became the right fit

Dedicated capacity: Making sense of a 60-trillion-token data pool

Beyond a 100B-parameter model

Trust, access, and the future

## Introduction

Prima Mente’s cutting-edge research began from a childhood memory.

When Ravi Solanki was ten, a severe flu landed him, temporarily paralyzed, in a US hospital. He remembers being fully conscious while his body refused to respond, surrounded by clinicians moving with urgency and purpose. The hospital felt like a spaceship at the edge of the frontier, where normal rules of life paused and every decision carried more weight. The experience stayed with him and even encouraged him to pursue a career in medicine, following in his parents’ footsteps. Medicine, he concluded, could be both terrifying and equalizing, and full of exciting unanswered questions. Years later, as a physician, the unanswered questions are what motivated Ravi to accelerate uncovering what modern medicine was still struggling to uncover in the brain.

Prima Mente, founded to make as much of our still-hidden biology observable and solvable as possible, is an AI biology company that generates data, builds general-purpose foundation models, and translates discoveries into on-site research and clinical outcomes within their own wet lab. Right now, they are helping uncover the brain’s complexity through Pleiades, a series of biological foundation models trained on molecular signals in blood, methylation patterns, and other biological data to infer what may be happening in the brain without directly accessing it. Ravi describes that rapid progress is everything for a small startup, and Pleiades can only improve as fast as the data can be collected, organized, trained, tested, and scaled.

Recognizing early on what it would take to run a company at the speed of AI, Ravi tapped co-founder Hannah Madan, whose background bridges pharmacology and business, to help uncover the secrets of the brain. Her superpower is building and leading product and operations functions at early-stage startups. “Ravi helps to set the direction, and I act as the glue that unblocks what we need to make it happen, ” says Hannah. Having grown up a team sports player, Hannah learned from a young age that taking action helped her to figure out the next move. “I knew that this man was not going to be stopped, ” she recounts, recalling the moment they decided to join forces. “To me, it sounds riskier to join a company where I don’t get to grow, develop, and be challenged by the kind of minds we bring into our team, ” she says.

The company operates with a team of experts representing 25 different nationalities, with hubs in London, San Francisco, and an emerging office in the United Arab Emirates (UAE). “In 2024, we deliberately split our time between the US and the UK. London has extraordinary talent, but San Francisco has a collective empathy for building hard things. It’s welcoming and energizing. Even if you have a direct competitor trying to crush you, it’s one of the best places to build AI. We think the balance between the two is important, ” says Ravi. Hannah builds and leads her team by fostering a culture of reflection and collaboration, creating the space for people to exchange ideas and learn quickly from each other. “I believe most people want to do their best work here, but constant learning and communication across the team are paramount to our results.”

## Seeing what we cannot observe

Dementia is the most common cause of death in the UK and the sixth in the United States. Yet, neurodegenerative disease remains one of the least understood in medicine, because clinicians cannot directly observe the complex molecular changes that precede diseases like Alzheimer’s and Parkinson’s. Those early changes dramatically shape diagnosis and treatment, and if properly cataloged, will support rapid new drug discovery.

Because the data used by Prima Mente is noisy, rigor in collecting and organizing it is the foundation of progress. Even samples taken from the same tissue can behave differently depending on handling and context. Pharmaceutical research has struggled for decades with consistent measurement, so modeling cause and effect in large, varied populations has been difficult. “Each cell type in the brain has a specific methylation signal that can help us identify whether that cell is happy, sad, or diseased, ” Hannah describes. Common symptoms like memory loss can stem from a wide range of underlying conditions, often with overlapping presentations that make them difficult to distinguish. By encoding these signals, Prima Mente’s ambition includes more personalized treatment.

Ten to fifteen years ago, computational biology showed promise, but it rarely translated into meaningful clinical outcomes because the compute infrastructure wasn’t ready yet. Today, that same data, when cleaned, aggregated, and combined with billions of parameters inside modern foundation models, can support rapid progress toward disease prevention and drug discovery. And for Ravi, every failed experiment, delayed training, or lost week pushes discovery further from patients. “Speed matters, ” he says. “We either innovate or we die.” He was talking figuratively about the company. What they are building couldn’t have existed even three years ago.

Generative AI now makes it possible to model complex biological systems using decades of heterogeneous data and to learn relationships between symptoms, systems, and care protocols. “We’re aggregating billions of data points collected from patients through partners around the world, ” Ravi says. “And critically, over just the past few years, researchers, clinicians, and industry partners have started to accept AI-led approaches as the most reliable and fastest path to solving our hardest problems. That combination is what makes this moment special.”

## Infrastructure for better science: Building Pleiades

In mid-2025, Prima Mente publicly launched Pleiades, a family of large-scale foundation models trained on whole-human epigenome data, with applications in Alzheimer’s and Parkinson’s disease. Pleiades launched with 90M, 600M, and 7B parameter variants, trained on roughly 1.9 trillion tokens of methylation data. The team relied on managed Kubernetes clusters and a shared distributed filesystem to run dozens of experiments in parallel. Eight months later, with new research leaders in place, the team now works across petabyte-scale multi-omic datasets, with a clear roadmap toward clinical impact.

As datasets expanded into petabyte scale, integrating genomics, epigenomics, proteomics, and other biological layers, stable and reliable infrastructure became critical to good science. The data environment had to support massive concurrency and help the small team run faster. “Nebius accelerated every layer of our training, ” Ravi says. “Their managed services transformed what our small team could do with our data.”

Many of Prima Mente’s biologists and data scientists are not traditional AI engineers, and most now work through multiple AI coding agents running in parallel. “My team keeps asking for a fourth or fifth monitor, ” Ravi laughs. “They want every desk to look like it belongs on a financial trading floor. Watching agents run experiments in real time has become essential. Even an hour of downtime matters to us.”

Luca Giacomoni, a lead AI engineer at Prima Mente, joined in August 2025 and immediately recognized the intensity. The company values high agency, zero-to-one thinking, and moving faster than anyone else. Luca holds a PhD in computer networks and proudly calls himself a “hardcore niche computer scientist.” His background spans reinforcement learning and large-scale foundation models applied to biology, and he thinks in terms of systems, throughput, and what it takes to run week-long experiments reliably.

Luca talks about infrastructure the way a biologist talks about lab conditions. The environment defines what can be tested, repeated and trusted. “Having a partner like Nebius that helps us move faster without downtime means we can shorten training cycles, ” he says. “That’s ultimately about helping patients, and that’s why I’m here.”

Since Luca joined, new data has continued to arrive, and the team is pushing toward a deeper, more holistic understanding anchored in multi-omics analysis that more closely mirrors how disease develops. Discovery at the frontier requires discipline and rigor, but moving more quickly at this stage depends on infrastructure.

## How Nebius became the right fit

“I can’t remember a time before Nebius, ” Hannah begins. Prima Mente needed an environment where dozens of experiments could run simultaneously, reading and writing shared datasets without friction. The company was training its first 90M-parameter model but operating in an environment where compute had to be pieced together wherever it could be found, creating constant overhead as the team adjusted code to shifting infrastructure. “Before Nebius we were very much stuck, ” Luca says. “We had a lot of friction needed to do the science.”

Nebius helped the team spin up secure environments quickly, start small, and scale while keeping systems stable and consistent. “What makes us faster day to day is the continually improving orchestration layer being handled by Nebius so we can focus on experiment design instead of job plumbing.”

Prima Mente scaled Pleiades 1 to 7B parameters far more efficiently than before. “We don’t need to spend two months figuring out how to use the platform, ” Hannah says. “There are a lot of solutions available out of the box. This speeds us up dramatically.”

Nebius’ software stack saves checkpoints consistently and loads data deterministically for easy coordination and observation. It sounds like an engineering detail, but the economics of re-running experiments speak for themselves. If a week-long run fails without recovery, the team loses time and momentum, resulting in missed windows to bring progress to patients.

## Dedicated capacity: Making sense of a 60-trillion-token data pool

Since February 2026, Nebius introduced a reserved cluster configuration that supports longer, multi-node training runs on NVIDIA H200 GPUs so large-scale pre-training doesn’t compete with other tasks. The dedicated cluster gave Prima Mente room to iterate on a new generation of foundation models, while also supporting downstream experiments and the inevitable new questions that surface mid-run. “As the pace of change in AI biology picks up, relying on the cluster is super important for our team to answer bigger and more important questions, ” Hannah says.

Prima Mente is currently working through more than 60 trillion tokens to understand meaningful patterns across an increasing number of layers of cellular biology. Developed in collaboration with Nebius and NVIDIA, low-level optimizations resulted in a 10x scale-up of Prima Mente’s ablation model from 1B to 10B parameters in just a few weeks, while improving throughput from 8,000 to 9,000 tokens per device per second, pushing overall throughput beyond one million tokens per second across 16 nodes. Having demonstrated linear scaling on the current setup, the team expects throughput to double when the ablation model is deployed across the full cluster."When you build the model from scratch, fine-grained control is key, ” Luca says.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Beyond a 100B-parameter model

The team plans to scale Pleiades beyond 100B on the NVIDIA Blackwell platform and by doubling their Nebius reserve capacity. While NVIDIA HGX B300 larger memory capacity allows for higher token throughput, increased batch sizes, and lower checkpointing overhead, high-bandwidth communication is supercharged by NVIDIA NVLink™ and NVIDIA InfiniBand networking, which allows distributed training workloads to scale efficiently.

“Networking matters, ” Luca says. “Storage matters. Checkpointing and failure reduction matter. Having a provider like Nebius who collaborates, explains tradeoffs, and helps translate all of this into software decisions is key for us to scale research.”

## Trust, access, and the future

Prima Mente believes both open and closed models will play a role in healthcare’s future because trust and equity are critical to health outcomes. Over time, they plan to open parts of their work for others to help improve outcomes, particularly for populations that have historically been underserved. In a signal that momentum is building, in early 2026, the FDA cleared the first blood test intended to aid in diagnosing Alzheimer’s disease, potentially reducing reliance on expensive PET scans and invasive spinal taps.

Prima Mente is also among the first startups included in the UK’s Sovereign AI Fund, a £500-million initiative that supports homegrown startups building cutting-edge AI. As the fund’s first cohort focuses on technologies with the potential to reshape daily life, Hannah says the recognition further motivates the company to advance the frontiers of biology research from within the UK. “It validates exactly what we’re doing in this space, and we’re super excited about where we can take AI and life sciences.”

The company’s frontier work has also received $1M recognition through an Alzheimer’s research prize supported by Gates Ventures for their solution PARTHENON, an integrated modeling and discovery platform that acts as a virtual “wet lab, ” enabling researchers to model experiments using virtual cells and the support of an AI co-scientist called Athena, compressing work that normally takes weeks into minutes. “It will allow our models to create an even bigger impact, helping other people make discoveries too, ” Hannah says.

Broadly, workload isolation and data locality will become more critical as AI teams move deeper into regulated environments and serve patients and institutions globally. As foundation models mature, Prima Mente is also building toward inference as a real business that will become embedded in clinical-grade systems. Luca sees Nebius as the platform that will evolve alongside those demands because the team is constantly invited to provide real-time feedback that helps shape future products and solutions.

The goal ahead is simple: make a drug that saves lives, then do it again, and again. Everything else, funding, hiring, partnerships, infrastructure, and sometimes even sleep, are just ways to make that happen faster.

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
