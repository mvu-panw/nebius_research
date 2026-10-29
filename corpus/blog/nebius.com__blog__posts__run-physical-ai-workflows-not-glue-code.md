# Run physical AI workflows, not glue code

Source: https://nebius.com/blog/posts/run-physical-ai-workflows-not-glue-code

Skip to main content

Every physical AI team eventually runs into the same bottleneck — and it is rarely the model itself. The real cost is the five weeks of plumbing that come before anyone can train it.

The challenge is everything around the model: simulation, synthetic data generation, curation, training, evaluation and deployment. Each stage may have a best-in-class tool, but stitching them together often requires weeks of integration work before meaningful experimentation can begin. Teams that come to Nebius for GPUs end up spending their first month standing up eight different containers, configuring/integrating storage, converting data between formats and debugging mismatches that have nothing to do with the robot they actually want to ship.

Nebius Nebius Physical AI Workbench: platform architecture

Figure 1. The Workbench platform: agents and the CLI on top, a curated tool layer, a shared data layer, and Nebius compute underneath

The Nebius Physical AI Workbench is how we are tackling that: a curated set of pre-validated physical AI tools, like NVIDIA Cosmos 3, NVIDIA Isaac Sim, NVIDIA Isaac GR00T, and a growing ecosystem of open-source and partner tools unified on a shared data layer and driven by a CLI, an SDK and agents, so a team works with one workbench instead of eight containers on Nebius AI Cloud. It is being actively built, and you can use what works today; the project is open and lives on GitHub.

## Curated, not a dumping groundCurated, not a dumping ground

A marketplace where anyone can dump a tool grows fast and helps no one. Customers still have to find the right tool, trust it, and figure out how to connect it.

The Workbench is curated. We validate strong solutions end to end, open source and partner alike, then pre-wire them to a shared contract: every tool reads and writes through a shared data layer — the same Nebius Object Storage — using standard formats such as MP4, JSON sidecars, .safetensors, URDF and MCAP, so data flows between steps with no conversion tax. You compose rather than glue.

## Powerful tools, pre-wiredPowerful tools, pre-wired

The most powerful tools in physical AI are also the hardest to stand up. NVIDIA’s Physical AI stack is the flagship example, and it is validated to run on the Nebius Physical AI Workbench:

- NVIDIA Cosmos 3 generates and augments photorealistic worlds and synthetic data from a prompt.

- NVIDIA Isaac Sim and Isaac Lab, built on Omniverse, bring physics-accurate simulation and rendering for robot learning.

- NVIDIA Isaac GR00T provides foundation models for robot reasoning, policy generation and motion prediction.

Each is a one-click deploy on the Workbench, validated and working today, backed by Nebius compute and storage and exposed as a headless API. Nebius manages the underlying accelerated infrastructure — including NVIDIA Blackwell, Hopper, and RTX PRO GPUs, orchestration, model serving, storage, IAM, networking and secrets — so teams can focus on building Physical AI applications instead of operating infrastructure.

Also, the same one-click deploy and shared data contract extend to open-source frameworks like FiftyOne, Genesis, LeRobot, and LanceDB, which are validated on the Workbench today, and the partner program is open across curation, synthetic data, simulation, and observability. The goal is simple: anything that speaks a headless API and the standard formats should compose into the same workflows. The Workbench is a neutral platform, not a single-vendor stack.

Figure 2. Left: NVIDIA Cosmos-generated image. Right: NVIDIA Isaac Lab joint renderings (blue) with NVIDIA Isaac GR00T predictions (orange)

## One prompt, one workflowOne prompt, one workflow

To demonstrate how Physical AI workflows can be composed on the Workbench, we asked an agent to assemble a simulation pipeline using Workbench building blocks. From a single prompt Cosmos generates data, NVIDIA Isaac Lab simulates behavior, NVIDIA Isaac GR00T predicts actions, and the eval scores the results. One pipeline, assembled by an agent, on a single platform:

- Prompt Cosmos. “A humanoid robot carrying a box in a warehouse.” Cosmos returns a set of synthetic images.

- Curate. FiftyOne (Voxel51, open source) pulls the good frames out of the synthetic set.

- Simulate. Isaac Lab renders the robot’s joint movements from the scene.

- Predict. Isaac GR00T predicts the next joint movements, overlaid on the render.

- Evaluate. The result feeds a policy and an evaluation step.

## Agents are the interfaceAgents are the interface

This is the part that changes how teams work. Every Workbench component exposes a headless API from day one, which means the npa CLI (npa workbench …), the SDK, and a YAML blueprint all hit the same endpoints, and so does an agent.

Point an agent at the Workbench and it knows the endpoints. Describe the pipeline you want in plain language, and the agent writes the blueprint, configures each component, and launches the run headless, no dedicated MLOps team required. The agent does the wiring so you can steer the research. With the NVIDIA Physical AI agent skills integrated directly into Nebius AI Cloud, developers can automate synthetic data generation, simulation, training, evaluation and deployment workflows using natural-language instructions instead of custom orchestration code.

## The loop that actually ships modelsThe loop that actually ships models

A demo is one pass, but production is a loop. The closed-loop sim-to-real pipeline below is what the Workbench is built toward, drawn straight from how real robotics teams operate; pieces of it run today, and the full loop is where we are headed.

Figure 3. Closed-loop sim-to-real workflow on the Nebius Physical AI Workbench

Raw episodes land in object storage, where a data layer curates, versions, and caches training data. NVIDIA Cosmos 3 then augments high-value examples across new lighting conditions, object configurations, environments, and edge cases, helping teams expand diversity without costly real-world collection. NVIDIA Isaac Sim builds out large-scale training environments from those scenes plus sim assets. The resulting set splits into 80/20 training and validation sets — for example, the policy trains on 8,000 environments and validates on 2,000 held-out ones with a VLM-scored eval. Models that pass predefined quality thresholds are promoted to real-world testing, while those that fall short automatically trigger additional simulation, data generation, or training. The result is a closed-loop workflow that continuously improves model performance through synthetic experience.

The heavy stages are exactly where teams get stuck today. NVIDIA Cosmos augmentation, for instance, is brutally GPU-hungry and painful to scale by hand, but on the Workbench it runs on managed Kubernetes and serverless with autoscaling, so “generate a hundred videos in parallel” becomes a config value rather than a week of cluster work.

NVIDIA Cosmos 3 is now openly available and will soon be available through the Nebius Physical AI Workbench. By combining Cosmos 3 with NVIDIA Isaac technologies, agent-driven workflows, and Nebius AI Cloud infrastructure, developers can accelerate the entire Physical AI lifecycle — from synthetic data generation and simulation to policy training and deployment.

## Open, and yoursOpen, and yours

The Workbench is open source under Apache-2.0, and partners integrate independently. Any vendor can publish a tool to the marketplace and have it compose with everything else. For any solution, drop in your custom container, bring your own model, or self-register any tool that speaks a headless API. It runs in an environment already tested to support it.

Your data stays in your Nebius environment, in the region you choose, EU or US, with a single bill for compute, storage, and managed services and no black-box platform dictating how you work.

## Get startedGet started

Physical AI is rapidly becoming a systems problem rather than a model problem.

Success depends on connecting simulation, synthetic data generation, training, evaluation, and deployment into a repeatable workflow.

The Nebius Physical AI Workbench is designed to make those workflows composable, agent-driven, and production-ready. By combining NVIDIA Cosmos 3, NVIDIA Isaac technologies, and a curated ecosystem of Physical AI tools on Nebius AI Cloud, you can spend less time wiring infrastructure together and more time building intelligent systems.

If you are building physical AI, the Workbench is the shortest path we know from a cloud account to a first training run, and it is open for you to try.

Clone the repo, pick a reference architecture (Video SDG, Curate-Augment-Train, Sim-to-Real, Closed-Loop AV Validation, or Eval-as-a-Service), then run npa workbench or just ask an agent to build it. The reference architectures, the CLI, and the SDK are free and open.

The model was never the hard part. We are working on the rest — openly. Take a look and try it.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Timothy Le
Principal Technology Strategist - Physical AI

Contents

- Curated, not a dumping ground

- Powerful tools, pre-wired

- One prompt, one workflow

- Agents are the interface

- The loop that actually ships models

- Open, and yours

- Get started

## See also

### 

Nebius partners with Positronic on Physical AI Leaderboard (PhAIL)

Physical AI is moving from controlled demos to real-world deployment — and that shift demands benchmarks grounded in actual operations, not lab conditions. Today, Nebius joins Positronic as a founding consortium partner of the Physical AI Leaderboard (PhAIL), a new platform that evaluates robot AI models on real hardware using commercially relevant tasks and production-grade metrics.

March 31, 2026
5 mins to read

### 

Running NVIDIA NIM and NVIDIA Blueprint in Nebius AI Cloud

In this blog, we will take a look at how teams can deploy the four NVIDIA NIMs available now in our platform, how they can be consumed via their API and how they can fit into larger scientific workflows. It also covers the Virtual Screening Blueprint, which turns folding, molecule generation and docking into a ready workflow that becomes available in JupyterHub shortly after deployment.

December 17, 2025
9 mins to read

### 

Game on! UFB and Nebius power the future of robotics

We are thrilled to announce that Nebius is the official technology partner for Season 1 of Ultimate Fighting Bots (UFB)’s Humanoid Sports League — the world’s first multi-format competition platform for physical AI. The two companies will pioneer the use robots by coupling UFB’s growing platform for humanoids with Nebius’s cloud solution for physical AI.

May 13, 2026
9 mins to read

Sign in to save this post
Sign In
