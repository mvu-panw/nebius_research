# Accelerating physical AI development: How Antioch built the simulation platform for robotics

Source: https://nebius.com/customer-stories/antioch

Skip to main content

## Long story shortLong story short

Antioch enables robotics teams to develop physical AI systems in massively parallel cloud simulation. The platform automates many engineering processes with agents to reduce the dependence on real-world testing in physical AI.

After outgrowing infrastructure that could not keep pace with demand, Antioch moved to Nebius, enabling significantly faster simulations and greater scale while reducing total cost of ownership by 23%. Customers can efficiently develop and evaluate against all of the edge cases that matter in minutes rather than weeks. End-to-end simulation cycles run up to 50% faster on Nebius than the baseline on a major cloud provider. At the same time, the team has seen a 40% increase in the number of parallel simulations on Nebius compared to their previous cloud deployment.

Antioch was founded in early 2025 by Stanford technologists, physical AI leaders, and the founders of Transpose — a national security contractor acquired in 2023.

Antioch focuses on collapsing the sim-to-real gap in robotics, then rapidly scaling simulation in the cloud to massively accelerate development, evaluation, and synthetic data generation for customers.

With engineers from Tesla Autopilot, Google DeepMind, and Meta Reality Labs, Antioch serves physical AI leaders in manufacturing, logistics, warehousing, security, medicine, defense, and mobility. The Antioch platform supports a wide range of hardware morphologies, including humanoids, quadrupeds, UAVs, AMRs, and industrial workcells.

## ContentsContents

The bottleneck holding physical AI back 

Building for the agentic era 

The road to Nebius

New cloud simulation environments in minutes

Simulation at scale: the numbers

The infrastructure layer for a $50 trillion opportunity

## The bottleneck holding physical AI back

Building reliable autonomous systems like robots and drones requires a staggering volume of real-world testing. Every iteration cycle demands hardware in the loop. Teams spend weeks staging environments, running controlled trials, and collecting just enough data to make their next change. At the same time, edge cases are usually too expensive, dangerous or impractical to test in the real world. The result is a slow development cycle that produces robots with poor policy performance.

Antioch was founded to bridge the gap between simulation and reality. The company’s platform replaces hardware-dependent iteration with closed-loop simulation. It is a cloud-hosted environment where AI agents and engineers convert their real systems into digital twins, run massive suites of test scenarios in parallel, and validate autonomous behavior. The result is more predictable robots that are safer in the real world.

“Today, the development of reliable and safe physical AI systems is bottlenecked by expensive, slow, and incomplete real-world testing. The edge cases that degrade real-world performance or create unpredictable behavior are precisely the ones that are prohibitively expensive or impractical to test in the field”

— Harry Mellsop, Co-Founder, Antioch

## Building for the agentic era

Antioch’s platform is industry-agnostic and cloud-hosted, with no setup or configuration required to spin up a simulation environment. Teams simulate various robots — humanoids, quadrupeds, UAVs, autonomous mobile robots, industrial workcells — and Antioch provides digital twin creation pipelines, sensor and hardware model libraries, state-of-the-art scene generation tools, and evaluation frameworks to run those systems through thousands of simulated scenarios.

Antioch is compatible with leading simulation frameworks, like NVIDIA Isaac Sim and Isaac Lab, meaning that teams who have already built simulation capabilities internally can onboard in minutes and benefit from dramatically improved simulation fidelity and cloud scalability.

The platform includes an agent layer that pairs the simulation infrastructure with agents that have native expertise in autonomous systems. When a simulation run surfaces a failure mode, the Antioch agent learns from the replayable telemetry, autonomously proposes improvements to the robotic stack, and retests in parallel simulation to validate the change. The result is a closed feedback loop that compounds accuracy: each simulation run feeds the next, and each agent iteration tightens the system’s performance envelope.

Antioch’s Co-Founder Alex Langshur offers an analogy to the world of software engineering: “Antioch does for physical AI what Cursor, Claude Code, and Codex have done for software engineering. It’s a development environment that changes not just how fast teams work, but what they are capable of building.”

## The road to Nebius

Because Antioch’s customers need simulation environments in seconds, Antioch needed the ability to dynamically provision GPU compute exactly when customers need it. Behind the scenes, that means provisioning the latest-generation NVIDIA GPUs at the precise moment demand arrives and scaling those resources down just as efficiently when a session ends. When usage spikes, whether from a single customer running hundreds of parallel simulations or from multiple onboarding accounts going live simultaneously, the entire experience depends on whether the infrastructure can keep pace.

Among competing options that included hyperscalers, Nebius stood out for infrastructure capability and depth of technical expertise. From a rapid procurement process to sharp architectural consultation and ongoing white-glove support, Nebius approached the engagement as a long-term partner investing in a shared future.

“Nebius clearly understands the step change that physical AI will bring for the cloud compute landscape. Accordingly, it is optimizing to support the rapidly scaling companies, like Antioch, that will define the physical AI era”

— Collin Schlager, Co-Founder & Head of Product, Antioch

In addition, Nebius’ orientation toward the physical AI ecosystem, not just toward GPU capacity, was a key differentiator. Antioch was not looking for a commodity cloud but a partner cloud for robotics. Most importantly, the Nebius Physical AI Workbench provides an open-source framework that connects best-in-class tools across the physical AI development pipeline, from data curation (for example, with Voxel51's FiftyOne), to synthetic scene generation (for example, with NVIDIA Cosmos 3), through to simulation and policy training. For Antioch’s customers, this means the simulation environments they run on Antioch can more easily draw from a richer upstream data pipeline. For Nebius’ customers, it opens a seamless path to integrate with Antioch, delivering a step-change in simulation fidelity and scale compared to alternatives. As a result, curated and synthetically generated training data can flow directly into the simulation layer through pre-wired configurations, not glue code.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## New cloud simulation environments in minutes

Antioch’s proof of concept on Nebius began with a clear set of requirements: latest-generation NVIDIA GPUs, dynamic scaling, and complex lifecycle orchestration. Within a week, Antioch and Nebius had a rollout plan ready. The engineering team ported the Antioch stack to Nebius instances and immediately began running internal development workloads: hundreds of parallelized simulations using both classical and differentiable physics solvers, world models, robotic perception pipelines, and photorealistic rendering.

Once the infrastructure cleared internal benchmarks for durability and scalability, Antioch moved critical customer workloads to Nebius and began onboarding new accounts directly onto Nebius-backed environments. Some of those onboarding periods involved extremely precise and computationally expensive simulations of autonomous manufacturing cells. Nebius provided low-latency GPU access, frontier simulation performance, and uninterrupted reliability.

Today, the experience in the Antioch Console reflects what the infrastructure makes possible. Spinning up a GPU-backed cloud simulation environment takes two clicks and less than five minutes. Once an environment is provisioned, a full simulation run — complete with a complex robot digital twin, multimodal perception pipelines, an autonomous control stack, and a city-scale, high-fidelity environment — can be running in just a few seconds. On Nebius, end-to-end simulation cycles run up to 50% faster than Antioch’s previous baseline.

“Nebius has provided many key unlocks in allowing us to make Antioch even more scalable and user-friendly. Our customers can spin up multiple GPU-backed simulation environments, run compute-heavy workloads, and spin them down quickly and reliably”

— Michael Calvey, Co-Founder & Head of Revenue, Antioch

## Simulation at scale: the numbers

On Nebius infrastructure, Antioch streams optimized simulation scenes to the browser at 100+ frames per second, with physics stepping at 240Hz. Even running heavy perception pipelines and multi-robot fleet simulations simultaneously, Antioch achieves 60+ fps with the full visual livestream active. This level of performance lets engineers watch their autonomous systems operate in real time and intervene when needed. Further, headless simulations, running without a visual output for pure evaluation purposes, step faster than real time to enable rapid sweeps across thousands of scenarios.

The practical impact on Antioch’s customers is significant. For one customer developing a quadrupedal warehouse-surveying robot, the platform reduced time to results from weeks to hours while improving model accuracy. Traditionally, adjusting control algorithm hyperparameters or sensor configuration requires staging a warehouse environment and running scenario testing over the course of weeks. Even then, most edge cases go untested because staging every variant is impractical. With Antioch running on Nebius, the same customer runs, in hours, a far more robust suite of scenarios across numerous environments and conditions.

Nebius has improved efficiency for Antioch’s cloud operations. Contrary to conventional thinking, the Antioch team found that simulation speed compounds as utilization scales. When a customer runs multiple heavy simulations headlessly in parallel, speed and resource utilization both improve. Further, every simulation run is catalogued with replayable telemetry for the Antioch agent to learn from. The agent proposes improvements, retests in parallel, and validates the change before a human engineer reviews it. Every marginal gain in simulation throughput becomes a multiplier across the entire development loop.

Nebius provided industry-leading rates on the most in-demand GPU SKUs, translating directly into lower rates for Antioch customers. Commercial conversations with new robotics and physical AI teams can focus on the core value Antioch delivers, rather than on compute costs. Competitive pricing, combined with other platform advantages, has provided Antioch with a 23% improvement in total cost of ownership (TCO) compared to the previous cloud deployment.

Finally, Nebius allows Antioch developers to control complex cloud orchestration and parallelization from a lean, intuitive CLI. As a result, developer efficiency has improved by 25%. The Nebius team’s deep technical expertise has allowed Antioch to build the new standard for simulation infrastructure. Most issues are resolved within one day.

## The infrastructure layer for a $50 trillion opportunity

To Antioch, manufacturing, logistics, construction, energy, and agriculture collectively represent a $50 trillion global opportunity. As the company scales to meet upcoming demand, Nebius is positioned as a critical long-term partner. The customer base will expand rapidly as a new generation of robotics companies emerges, and simulation will become the central node in every physical AI development cycle.

Beyond raw compute, the Nebius and Antioch partnership reaches into how the physical AI development stack gets built. The Nebius Physical AI Workbench connects the Antioch simulation platform to the broader pipeline that physical AI teams run: from synthetic data generation with NVIDIA Cosmos, through Isaac Sim-based training environments, to policy evaluation — all composable, agent-driven, and running on the same Nebius infrastructure. As Antioch’s customers deepen their development cycles, the combination of Antioch’s simulation platform and the Workbench’s pipeline infrastructure means the full loop from failure detection to validated policy can run as a single workflow, without the custom integration work or glue code.

“Together, we are positioned to become a fundamental layer of the physical AI stack. Nebius provides the cloud infrastructure, and Antioch provides the development platform”

— Harry Mellsop, Co-Founder, Antioch

Explore

Antioch

Nebius for Physical AI

## More exciting stories

## 

Voxel51

Voxel51 develops FiftyOne, an open-source platform that helps physical AI teams understand, curate, and evaluate multimodal datasets. Together with Nebius and NVIDIA, the company built a production synthetic data pipeline that enables teams to generate synthetic scene variations at scale and review them in FiftyOne.
Read the story

## 

Ultimate Bots

Ultimate Bots is building a robot sports league and software for humanoid robots. Its browser-based Studio makes humanoid robotics accessible to creators by turning recorded movement into deployable robot motion in minutes. Powered by Nebius Serverless and NVIDIA’s SONIC foundation model, Studio now supports more than 500 creative workflows each month.
Read the story

## 

RoboForce

RoboForce builds Robo-Labor for dirty, dangerous and repetitive industrial work across solar, data centers, shipping, mining, manufacturing and logistics. With Nebius AI Cloud, NVIDIA Blackwell infrastructure, scalable storage and expert support, RoboForce reduced AI setup pipeline time by 70% and cut iteration cycles from months to days.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
