# Nebius Engineering

Source: https://nebius.com/careers-engineering

Skip to main content

## Nebius in numbers

## Choose your challenge

Site Reliability EngineerBackend EngineerSystem EngineerML EngineerFrontend Engineer 

## Site Reliability Engineer

GPU fleet reliability and the observability stack that keeps NVIDIA HGX clusters running. The CI/CD pipelines, Kubernetes autoscalers, and Terraform infrastructure built to self-heal under pressure.

The hard problems:

- Ensuring reliable training on supercomputer clusters, bridging both low-level hardware domain and the training code to work in concert on thousands of nodes and tens of thousands of GPUs.

- Profiling GPU performance at kernel level across CUDA, ROCm, and InfiniBand to decide whether hardware meets production bar before it ships.

- Running 25,000 CI builds a day on a monorepo at FAANG scale, without making engineers wait.

- Designing telemetry pipelines that turn hundreds of terabytes of signal into a clear answer about what went wrong, not just that it did.

- Developing Kubernetes operators for training, solving non-trivial autoscaling problems for inference, all working on scale of thousands.

- Building the runbooks and automation that catch incidents before they become outages.

See open rolesCheck out the interview guide

## Backend Engineer

The schedulers, control planes, and cloud services that keep tens of thousands of GPUs running reliably across data centers globally.

The hard problems:

- Scheduling VMs across heterogeneous hardware: NVIDIA Hopper and Blackwell, Intel/AMD and ARM/Grace CPUs, InfiniBand fabric topologies, where placement decisions affect whether a distributed training cluster hits its bandwidth or doesn’t.

- Moving from 99.9% to 99.99% SLA: one extra nine means cutting failure time from eight hours a year to 52 minutes, across a stack that includes KubeVirt, custom schedulers, multiple GPU generations, and InfiniBand.

- Scaling 10x from thousands to tens of thousands of RPS, where the bottleneck shifts between Kubernetes, proxy, routing, and billing in ways that only become visible under load.

- Turning Kubernetes into a full application development environment using CRDs, Operators, webhooks, and custom controllers, so VMs run as native Kubernetes resources and the platform can extend at every layer of the stack.

See open rolesCheck out the interview guide

## System Engineer

GPU cluster performance, hardware benchmarking, virtualization, and the networking fabric that makes large-scale AI training possible.

The hard problems:

- 

Profiling GPU performance at kernel level under real training workloads, where a benchmark that passes in isolation breaks at scale because of how NCCL, InfiniBand fabric, and driver config interact.

- 

Defining what “working” means for new hardware architectures including Hopper, Blackwell, Rubin before the industry has established standards for them.

- 

Scheduling VMs across tens of thousands of GPUs and multiple data centers, where a placement decision that’s wrong at scale has direct cost consequences.

- 

Writing and optimising low-level CUDA kernels for inference on hardware newer than its own documentation.

See open rolesCheck out the interview guide

## ML Engineer

Our ML Engineers span Managed Inference (Token Factory), Agentic Search, frontier ML research, fine-tuning and large-scale inference infrastructure, building the models, systems and platforms that power production AI across healthcare, media, robotics and financial services.

The hard problems:

- Optimising GPU kernels and inference runtimes to unlock the full performance of modern accelerators.

- Bringing new GPU architectures—from Hopper to Blackwell and beyond—into production as soon as they’re available.

- Profiling hardware, memory and runtime bottlenecks to squeeze every millisecond from model execution.

- Designing disaggregated inference systems that efficiently orchestrate compute, memory and communication across distributed GPU infrastructure.

- Advancing low-precision training and inference techniques that improve efficiency without sacrificing model quality.

- Scaling fine-tuning and inference for frontier open-weight models while pushing the limits of performance, cost and accuracy.

See open rolesCheck out the interview guide

## Frontend Engineer

We are working on creating UX solutions for external and internal customers. Thousands of AI engineers across healthcare, robotics, media, and retail as well as your own collegues interact with Nebius through what you build.

The hard problems:

- Working with multiple internal customers, while keeping UX consistent across all the different services.

- Working with APIs in multiple datacenters, with changing regional model, while thinking about client latencies.

- Creating completely new UX solutions, not directly related to infrastructure services, such as customer communication services, Cloud shell, IaaC code generation and anything else that will improve customer experience.

- Building a design system that stays coherent as the product surface doubles. And making instruments to facilitate quick delivery across development, design and documentation teams.

See open rolesCheck out the interview guide

## Builder notes

Check out our Builder Updates to stay in the loop on everything we’re building

## OpenClaw security: architecture and hardening guide

## Routing in LLM inference is the difference between scaling and stalling

## What is AI Cloud? Key features, use cases & how to choose

## Meet our builders

## Everyone knows what’s good, but the hard part is achieving it

Q&A with Gleb Evstropov, Director of Engineering

## Building the web layer for AI agents

Q&A with Maxim Akhmedov, Director of Engineering, Agentic Search.

## Your judgment should change the architecture

### Go build

### Move fast

### Own the outcome

### Raise your game

### Make meaningful impact

### Solve difficult problems

## 

Early talent

New to the industry? Check out our Early Talent Program for ambitious graduates and early-career engineers who want to work on business-critical problems across software and ML, as well as infrastructure and platform.
Learn more

## Still reading? You might fit right in
Apply nowView interview guide

## Explore Nebius

Token Factory​
Nebius AI cloud​
Nebius for AI builders​
