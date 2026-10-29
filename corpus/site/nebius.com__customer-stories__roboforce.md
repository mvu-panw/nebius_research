# Building Robo-Labor: How RoboForce is turning Physical AI into work humans shouldn’t have to do

Source: https://nebius.com/customer-stories/roboforce

Skip to main content

## Long story shortLong story short

RoboForce builds Robo-Labor for dirty, dangerous and repetitive industrial work across solar, data centers, shipping, mining, manufacturing and logistics. With Nebius AI Cloud, NVIDIA Blackwell infrastructure, scalable storage and expert support, RoboForce reduced AI setup pipeline time by 70% and cut iteration cycles from months to days.

RoboForce is a Silicon Valley AI robotics company founded in 2023 that builds scalable, deployable Robo-Labor for demanding industrial environments. Its robots are designed to automate repetitive, physically demanding and safety-critical work across solar, data centers, shipping, mining, manufacturing and logistics.

## ContentsContents

Introduction

The Physical AI inflection point

Three systems, one robot workforce

The road to Nebius

The Physical AI data factory starts now

## Introduction

In a robotics lab in Milpitas, California, Leo Ma and the RoboForce team are building class-leading robots powered by proprietary foundational models designed for dirty, dangerous and sometimes dull places. Deliberately, RoboForce robots don’t look like idealized Hollywood humanoids. They are designed for industrial work that humans should not have to do, but that heavy industry and society still depend on: lifting, fastening, connecting, inspecting, assembling and maintaining operations in environments that are repetitive, remote, hazardous or physically demanding. Ma describes robots working across vast solar farms in harsh sun, deep inside mines with poor air quality and serious safety risks, and in shipping yards or manufacturing facilities where tasks change frequently, and precision, reliability and strength matter every day.

RoboForce began in 2023 when three conditions came together almost at once; progress in physical intelligence, a deeper pool of AI talent and maturing robotics hardware. Ma assembled a team with enough depth across AI, foundation models, hardware, autonomy and deployment to build a complete system from AI model research, robot design and prototype to manufacturing. When asked about the risk of starting his own company, Ma calmly suggested the greater risk was not starting at all. Good ideas, he added, deserve follow-through.

Ma describes RoboForce as “a physical, AI-enabled robotic system, ” a phrase that captures where industrial automation is heading. Mining, solar, shipping, logistics and manufacturing companies are beginning to prepare for robotics that can move through real environments, understand context and perform useful work without constant human oversight. “Our robots are both scalable and easily deployable, ” Ma says. “Customers are asking us about two kinds of efficiency: time and money. Underpinning this is the consistency, precision and safety we deliver.”

RoboForce calls the category Robo-Labor: robots that can perceive, understand and act autonomously in high-stakes industrial environments. The industrial demand is real because the work is essential, labor is constrained and many tasks remain difficult to automate safely. RoboForce has initially targeted the solar industry as a natural proving ground. Solar work is large-scale, physically repetitive, often remote, and increasingly constrained by labor availability and long timelines. Timing is favorable given the global renewable power capacity is expected to increase by 4,600 GW between 2025 and 2030, with solar accounting for almost 80% of that increase.

At Intersolar 2025, a premier global tradeshow and conference RoboForce publicly unveiled its Robo-Labor system, describing a near-future where robots will install and secure modules for large-scale commercial projects, with 1 mm precision in fine-motor movement and manipulation. Ma suggests that RoboForce robots could perform installation labor for the solar industry at three times the efficiency and productivity of human labor, and at one third of the average U.S. labor cost for the same work over time.

RoboForce unveils AI robot workforce at Intersolar 2025

## The Physical AI inflection point

The broader industry is moving towards a future where human labor and robotic labor can work side-by-side. Physical AI lets autonomous systems perceive, understand, reason, and perform or orchestrate complex actions in the physical world. Before robots can work safely in high-stakes environments, they require training, testing and validation in simulation. That’s why in 2026, together with Nebius and Microsoft, NVIDIA released the agentic workflows for video augmentation to provide a unified framework for generating, augmenting and evaluating training data for Physical AI systems. Nebius has brought that blueprint into its AI cloud so teams like RoboForce can connect data generation, simulation, training evaluation and deployment into a faster learning loop.

## Three systems, one robot workforce

For RoboForce, the hardest robotics problem is the relationship between the data system, model system and the robot itself, for evaluating in the field. Data collection and synthesis determine that the robot can learn, model training turns that into behavior and evaluation determines whether the behavior is safe, reliable and useful. To reach production readiness, RoboForce needs all three systems to move quickly, supported by compute performance and reliability, storage, data transfer and throughput.

The first system is the data used for training and reasoning. This includes where the data comes from, how it’s stored, how it is labeled or synthesized, and how it becomes useful for precision movement and real-time decision making. Robotics data is difficult because it’s full of edge cases. A solar installation or maintenance task can change from site to site, season to season, and with harsh sun, sand, wind, rain, shadows, uneven ground, nearby workers, different tools and equipment layouts. RoboForce needs data that can teach the robot what objects are and what can be done with them in changing conditions.

RoboForce systems, data, model, robot

The second is the model system. RoboForce treats Physical AI development like an AI factory, where each model reflects the quality of the broader data, training and evaluation loop. Their factory requires vast amounts of reliable, high-performance NVIDIA accelerated computing, strong cluster stability, fast recovery when failures happen and the capacity to continue experimenting.

Safety raises the stakes for robotic deployment. In consumer AI, a poor answer can often be corrected in the next prompt. In industrial environments, a weak model can cause expensive downtime, damage and injury. RoboForce evaluates safety across three layers: whether the data can be collected safely, whether the model has seen enough variation to behave safely and whether the final robot behavior meets the higher standard required for physical work around people and infrastructure.

The third is the robot itself. TITAN, RoboForce’s general-purpose AI robot, was introduced in May 2025 for demanding industrial environments and is powered by spatial intelligence and modular hardware, and comes in both wheeled and tracked-base variations. Its five core capabilities are pick, place, press, twist and connect, the basic building blocks of many industrial tasks.

TITAN track-based variation is designed for demanding outdoor and industrial environments

TITAN is designed as a single platform that can serve multiple industrial workflows, improving deployment scale and unit economics. It must move well through real environments, reason in high-stakes and ever-changing conditions, recover from anomalies and respond to new task requirements in the field. It also needs to be reliable and strong in harsh environments, handle a 40 kg payload, and deliver 1 mm-level precision through field-proven autonomy and advanced manipulation. Based on close customer collaboration and field tested requirements, TITAN is outfitted with a 1100 mm arm and eight-hour battery pack.

## The road to Nebius

Before working with Nebius, RoboForce’s tools were fragmented across platforms. Data collection, simulation, training, evaluation, deployment and inference all had their own workflows. Ma’s priority was to find a platform partner that could save engineering time, reduce maintenance overhead and help the team improve model quality faster. RoboForce needed stable compute, reliable infrastructure and a more unified environment to streamline its data flywheel, training runs, fine tuning, evaluation and deployment.

Nebius gave RoboForce an AI cloud environment designed for the needs of Physical AI: high-performance compute, scalable storage, fast data movement and expert support across the training and evaluation loop. Highly scalable object storage and a high-performance file system help RoboForce access essential data quickly, while archiving or purging temporary data as needed.

Nebius provides the cloud infrastructure layer while NVIDIA provides the accelerating computing, physical AI software, orchestration and world foundation model technologies underpinning the development pipeline.

The workflow combines real-world robotic data with simulated data generated by using NVIDIA Cosmos world foundation models, while NVIDIA OSMO orchestrates distributed workloads across training and evaluation environments. On Nebius AI Cloud, NVIDIA RTX PRO 6000 Blackwell Server Edition GPUs support simulation and evaluation, while NVIDIA Blackwell-accelerated computing platforms support large-scale model training and experimentation. Together, these pieces form a continuous learning loop across data, simulation, training, evaluation and deployment.

By using Nebius, RoboForce reduced setup pipeline time by 70% and cut iteration cycles from months to days. That speed lets the team spend less time managing infrastructure and more time improving models and in-field robot performance.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## The Physical AI data factory starts now

Ma described the next phase of Physical AI as moving towards integrated systems that better understand context, physics, task sequencing and reasoning. He also sees 2026 as the moment when the industry started acting on the data problem in a more coordinated way through collection kits and methods, and platforms. New model architectures are helping teams avoid being blocked by an ocean of data.

External recognition is beginning to follow. The World Economic Forum (WEF) selected RoboForce as a 2025 Technology Pioneer working on breakthrough technologies. RoboForce’s latest capital raise is aimed at accelerating the flywheel between field data, synthetic data, model training, robot evaluation and deployment. A $52 million funding round from March 2026 brought total funding to $67 million, with proceeds directly accelerating its next-generation robot foundation model, general-purpose robot scaling and manufacturing readiness. RoboForce has also announced more than 11,000 robot orders through letters of intent, active pilot deployments, and planned expansion into data centers, shipping, logistics, mining and manufacturing customers.

Ma’s picture of the future is clear — robot labor will be a trusted companion for industries where work is essential, but not right for people. Reaching that future of useful, world-ready robots depends on a faster data flywheel, model roadmap and partners like Nebius to provide compute, storage, performance and direct engineering support.

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
