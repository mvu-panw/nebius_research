# Accelerating the data flywheel for physical AI: How NormaCore is standardizing robot fleet management

Source: https://nebius.com/customer-stories/normacore

Skip to main content

## Long story shortLong story short

NormaCore is building the missing infrastructure layer for physical AI: a unified runtime, a high-fidelity telemetry database, and Nebius cloud integration that closes the loop from data collection and processing to model training and physical deployment. With Nebius providing S3-compatible storage and on-demand GPU compute through one integration point, NormaCore and its users can collect demonstrations, train vision-language-action (VLA) models, and deploy updated policies, all without stitching together multiple vendors.

NormaCore is a European robotics infrastructure and software company building the missing data layer for physical AI. It provides an open-source runtime and high-fidelity telemetry database that standardize hardware control and data capture across heterogeneous robot fleets today, while working toward a broader fleet-scale learning platform where every hour of robot operation improves a shared model. Its integration with Nebius closes the loop from on-robot data capture to cloud storage and VLA model training.

## ContentsContents

The data that gets thrown away

Born in the lab, built for the fleet

From arm to algorithm and back

One provider, one bill, one closed loop

The flywheel starts here

The robotics industry’s tools and platforms are fragmented. Every hardware manufacturer ships a different SDK. Every research lab hand-builds its own data pipeline. Most of the telemetry that robots generate — every motor command, every sensor reading, every error state — gets thrown away because storing it at full fidelity is simply too expensive. The result is an industry that cannot build the data flywheel that physical AI requires.

NormaCore was founded to fix this. The company is developing a robotic fleet management platform designed to standardize control and data acquisition across heterogeneous hardware. The company is working to provide the missing infrastructure layer that modern robotics has needed but never had.

The team is growing fast — with an active open-source community that has generated over 600 GitHub stars on their main repository.

## The data that gets thrown away

Fleet-scale learning refers to the process of using every hour of robot operation to improve a shared model. It requires two things that the robotics industry does not yet have: a runtime that unifies hardware, and a storage layer that can keep telemetry at full fidelity without bankrupting the operator.

Today, researchers spend most of their time on infrastructure instead of science. Most telemetry is discarded. Training pipelines are rebuilt from scratch for every new hardware platform. The result is that the data flywheel for physical AI is not optimized when compared to that of generative AI, where more data produces better models which attract more users, and generate more data.

NormaCore is building the infrastructure to accelerate the flywheel by orders of magnitude.

“Robotics has no standard data layer. Every manufacturer ships a different SDK. Every lab hand-builds its own pipeline. Most telemetry is thrown away because storing it in full fidelity is too expensive. As a result, researchers spend their time on infrastructure instead of science, and the industry cannot build the data flywheel that physical AI needs”

— Alex Batsuev, Co-Founder, NormaCore

## Born in the lab, built for the fleet

The architecture of NormaCore is rooted in a fundamental insight: the next frontier of computing is the physical world. Recognizing this early on, Alex Batsuev and Dmitriy Samsonov applied the rigor of backend systems development to robotics infrastructure. Starting in early 2022, they focused on creating “zero-cost” abstractions — highly efficient systems that hide complexity without sacrificing performance. Through a series of technical innovations, NormaCore now powers vision-language-action (VLA) models, offering a universal, fragmentation-free environment for physical AI operations.

NormaCore has three main areas of innovation: a unified runtime, a custom database engine, and a 3D-printable reference arm. Station is an open-source runtime that unifies fragmented hardware SDKs into a single, consistent interface. Station blurs the line between research and production: developers use the same tools for rapid prototyping and fleet deployment, removing the costly rewrite that typically separates the two phases.

Underpinning the stack is NormFS, a custom database engine that captures, compresses, and encrypts high-frequency telemetry for long-term fleet analysis. NormFS functions as a continuous black-box recorder. It is a permanent, queryable and secure record of everything a robot does across its operational life, purpose-built for the data volumes that AI-driven robotics generates.

NormaCore also built ElRobot, a 3D-printable 7+1 DOF (degrees of freedom) reference arm optimized for teleoperation and demonstration recording, along with an open-source parallel jaw gripper. The platform runs on standard Linux or macOS and is validated across open-source hardware including OpenArm, SO-101, and Dogzilla. Research on vision-language-action (VLA) foundation models extends the stack further, with support for continuous training workflows that aim to generalize control policies across diverse hardware.

The platform is powered by a rapidly growing open-source community, with active deployments expanding across a global developer network that has already generated over 620 stars on the main GitHub repository. In addition to NormaCore’s ElRobot, the stack is natively validated to run on diverse hardware platforms, including the SO-101, OpenArm, and Yahboom’s Dogzilla mini.

## From arm to algorithm and back

The NormaCore stack is designed as a closed loop. Station, running on the robot, captures demonstrations and operational telemetry directly into NormFS. NormFS compresses and encrypts that data locally, then synchronizes it to Nebius object storage over a standard S3-compatible API. When a dataset is ready for training, NormaCore deploys serverless GPU instances on Nebius, runs the training job, and pulls the resulting policy back to the fleet, all through a single provider.

For academic labs and open-source communities using Station, this means time spent on robotics research rather than provisioning cloud resources and managing separate storage and compute providers. For the commercial hardware partners that NormaCore is now recruiting, the same standardized stack (Station on the robot, NormFS for data, Nebius for storage and training) can follow them from prototype to production fleet without a rebuild.

At a recent hackathon, a team of three developers used the combined power of NormaCore’s systems on Nebius to successfully complete a complex project in approximately 24 hours. The project involved recording, storing, and filtering a dataset, fine-tuning the SmolVLA model, and setting up robot hardware. The team achieved this without prior API knowledge, expensive hardware, or time-consuming, error-prone manual infrastructure setup.

When NormaCore’s capabilities are deployed at scale, the VLA model becomes self-improving. Every robot in the field generates telemetry. Every dataset can improve the shared model. Every improvement makes each robot more capable. This is the data flywheel that fleet-scale robotics needs, made practical by a single-provider integration with Nebius.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## One provider, one bill, one closed loop

NormaCore needs two things from a cloud provider: affordable, reliable object storage for the telemetry that NormFS captures, and on-demand GPU compute for training VLA models that turn that data into deployable policies.

Most general-purpose clouds price storage and compute separately in a way that penalizes the continuous, high-volume workloads that robotics generates. Telemetry doesn’t arrive in neat batches. Instead, it streams constantly from every sensor on every robot in a fleet. In addition, training runs don’t follow a predictable schedule; they spin up when enough new data warrants an update. Infrastructure designed for web workloads is poorly suited to this pattern.

Nebius provides both through a single integration: S3-compatible storage for long-term telemetry retention, and serverless GPU compute for training and inference. For NormaCore and its users, this means one provider, one bill, one integration point, and a unified workflow from data capture to model deployment. Streamlined integration helped NormaCore transition from initial evaluation to full production use in less than 3 hours.

“A researcher running Station on an SO-101 arm can collect demonstrations into NormFS, push the dataset to Nebius object storage, spin up GPU instances for training, and pull the resulting policy back to the robot without stitching together three different vendors”

— Dmitriy Samsonov, Co-Founder, NormaCore

The Nebius platform also offered the vital capability to store and process high-fidelity telemetry data strictly within Europe, a secure and compliant foundation for an expanding global user base. The single-provider model has shifted the team’s day-to-day focus from engineering plumbing to advanced scientific exploration and research workflows that were previously impossible. For example, the team has furthered its investigation into distributed learning capabilities with EGGROLL (Evolution Guided General Optimization via Low-rank Learning, an algorithm for training massive AI models).

## The flywheel starts here

NormaCore’s broader ambition is to develop a foundation model that improves with every robot in every fleet and uses the most diverse, highest-fidelity telemetry dataset in the industry. The infrastructure to make that possible is being built now, on an open-source runtime, a custom data engine, and a cloud that doesn’t penalize the workloads that physical AI demands.

NormaCore is recruiting commercial hardware partners for integration, with the goal of expanding the platform from the open-source community to production fleet deployments. Over the next 6–12 months, NormaCore will launch experimental deployments in key industries such as agriculture, logistics, and retail.

## More exciting stories

## 

Antioch

Antioch is building a cloud simulation platform for physical AI, letting robotics teams replace hardware-in-the-loop testing with thousands of scenarios run in parallel. On Nebius, teams spin up a GPU-backed simulation environment in under five minutes, stream scenes at 100+ frames per second, and run end-to-end simulation cycles up to 50% faster.
Read the story

## 

Voxel51

Voxel51 develops FiftyOne, an open-source platform that helps physical AI teams understand, curate, and evaluate multimodal datasets. Together with Nebius and NVIDIA, the company built a production synthetic data pipeline that enables teams to generate synthetic scene variations at scale and review them in FiftyOne.
Read the story

## 

Ultimate Bots

Ultimate Bots is building a robot sports league and software for humanoid robots. Its browser-based Studio makes humanoid robotics accessible to creators by turning recorded movement into deployable robot motion in minutes. Powered by Nebius Serverless and NVIDIA’s SONIC foundation model, Studio now supports more than 500 creative workflows each month.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
