# How SynthLabs and TractoAI are tackling AI infrastructure challenges

Source: https://nebius.com/customer-stories/synthlabs

Skip to main content

## Long story shortLong story short

Training models to reason requires a new generation of AI infrastructure capable of managing massive datasets, coordinating distributed search processes, and handling complex post-training optimization. Synthlabs significantly simplified their training infrastructure setup using TractoAI serverless platform. Synthlabs research engineers leveraged TractoAI distributed offline inference capability to accelerate the release of the first open source reasoning dataset.

SynthLabs is a startup advancing post-training techniques for large language models through open science. By combining RLHF with synthetic feedback (RLAIF), the team develops interpretable, scalable alignment methods that reduce reliance on human-labeled data, improve model controllability, and enable more efficient adaptation across tasks.

## ContentsContents

Laying the foundation for next-gen AI reasoning

SynthLabs and TractoAI join forces

Technical challenges

First results of the partnership between SynthLabs and TractoAI

— High quality dataset for reinforcement learning

— Data validation challenges

Driving the adoption of AI reasoning in enterprises

## Laying the foundation for next-gen AI reasoning

Recent AI advancements demonstrate remarkable capabilities in complex reasoning tasks, from solving mathematical proofs to writing sophisticated code. SynthLab’s recent research on Meta Chain-of-Thought (Meta-CoT) showcases how modern language models internalize complex reasoning processes, advancing beyond simple pattern matching to sophisticated search and exploration strategies.

Training reasoning models requires a new generation of AI infrastructure capable of managing massive datasets, coordinating distributed search processes, and handling complex post-training optimization.

## SynthLabs and TractoAI join forces

To tackle these infrastructure challenges head-on, SynthLabs Research and TractoAI are partnering to develop and document solutions for training advanced reasoning models. By combining SynthLabs’ expertise in AI reasoning with TractoAI, both teams aim to create a blueprint for the next generation of AI training systems.

## Technical challenges

AI reasoning infrastructure is still in its infancy. There’s no off-the-shelf solution for this level of complexity, so AI teams must innovate and continuously adapt. Our partnership is leading the way by validating and scaling infrastructure to meet these unique needs. The critical capabilities to deliver on our vision include:

High-performance compute requirements. Training advanced reasoning models demands substantial compute power. For instance, to achieve the necessary scale and model accuracy the training infrastructure needs to utilize many high-end GPUs, starting from 128 NVIDIA H100s. This high volume of GPU accelerators is required to deliver results more quickly.

Multi-node training. To accommodate these large compute requirements, AI reasoning models necessitate multi-node training runs.

Distributed data processing. Creating quality reasoning datasets and constantly auditing them at scale with the help of LLMs.

SynthLabs sought a platform enabling a small team of researchers to rapidly prototype and iterate on AI reasoning software components. They had prior experience building solutions with Microsoft Azure and Lambda Labs but found TractoAI to be better suited to their unique needs. TractoAI’s platform was built for researchers and data scientists to seamlessly support running data- and compute-heavy AI workloads.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## First results of the partnership between SynthLabs and TractoAI

## High quality dataset for reinforcement learningHigh quality dataset for reinforcement learning

SynthLabs published Big Math — the largest open-source dataset of high-quality mathematical problems, available on Hugging Face for researchers and ML practitioners to experiment with reinforcement learning (RL) in LLMs.

Big Math was developed to address a critical gap in reasoning datasets: the lack of high-quality, verifiable problems at scale. More details on how the dataset was created can be found in the research paper published by the SynthLabs team.

## Data validation challengesData validation challenges

One of the challenges in the process of creating this dataset was validating its accuracy. To that end, SynthLabs used a technique that relies heavily on evaluating the output of a language model, where they prompt a language model to answer all of the questions in the original dataset (nearly 650,000 problems). This step was massively compute-intensive, and the team found TractoAI particularly well suited to this job.

Built on a distributed storage and computation runtime, TractoAI offers powerful tools for running large-scale map-reduce operations across hundreds or thousands of GPUs. This made it easy to schedule and coordinate hundreds of thousands of LLM inference calls — a common practice when scaling evaluation on reasoning-related datasets.

SynthLabs found TractoAI’s ability to automatically scale up and schedule offline inference jobs with respect to the map operators particularly impactful. The platform’s design eliminates the complexity typically associated with distributed computing for AI workloads. SynthLabs’ engineers simply set up notebooks as if processing a single row of data, and TractoAI’s map function handled all the scaling and distribution automatically.

What made this especially powerful was TractoAI’s inference servers. Rather than manually orchestrating GPU allocation, the system duplicates instances as needed and scales resources to match the workload. This allowed the SynthLabs team to focus entirely on the quality of reasoning models instead of infrastructure challenges.

## Driving the adoption of AI reasoning in enterprises

The combination of SynthLabs’ expertise in AI reasoning and TractoAI’s scalable infrastructure creates a powerful foundation for enterprises looking to develop reasoning capabilities in their specific domains. Whether in engineering, scientific research or other technical fields, our joint solution enables organizations to focus on their unique challenges while building on proven frameworks for reasoning model development.

We remain committed to collaborating with enterprises to identify and solve complex reasoning challenges within their respective domains. Organizations interested in exploring how reasoning models can transform their technical operations are encouraged to reach out to either SynthLabs or TractoAI to learn more about our joint capabilities.

## More exciting stories

## 

Recraft

Recraft, recently funded in a round led by Khosla Ventures and former GitHub CEO Nat Friedman, is the first generative AI model built for designers. Featuring 20 billion parameters, the model was trained from scratch on Nebius.
Read the story

## 

Dubformer

Dubformer is a secure AI dubbing and end-to-end localization solution that guarantees broadcast quality in over 70 languages. The company manages two of its most resource-intensive tasks on Nebius: ML itself and the deployment of models.
Read the story

## 

Unum

In our field, effective partnerships that harness complementary strengths can drive significant breakthroughs. Such is the case with the collaboration between Nebius and Unum, an AI research lab known for developing compact and efficient AI models.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
