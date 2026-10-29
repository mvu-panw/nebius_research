# Visibility that drives elasticity: Introducing Capacity Blocks and Capacity Dashboard

Source: https://nebius.com/blog/posts/introducing-capacity-blocks-and-dashboard

Skip to main content

Continuous scarcity of AI compute has become a major decision-making factor for ML teams developing and serving GenAI models. AI leaders are often forced to adjust their business goals, development plans and even headcount expansion, based on the availability of GPU resources. In this environment, any opportunity to secure compute becomes a short-term competitive advantage, giving teams the ability to accelerate experiments, shorten iteration cycles and move product roadmaps forward faster.

As a purpose-built AI cloud provider, Nebius has always treated elasticity as a core value of our platform. But true elasticity requires more than simply having GPUs available — it also depends on the visibility, transparency and predictability that help teams plan and use their compute efficiently. From day one, we’ve offered on-demand access, long-term reservations and, more recently, introduced preemptible VMs to make every unit of capacity accessible.

Today, we’re expanding that elasticity even further with the introduction of Capacity Blocks and Capacity Dashboard — two new capabilities that bring additional clarity to GPU capacity management and give users full confidence in the compute they rely on.

# Build confidently with Capacity BlocksBuild confidently with Capacity Blocks

Capacity Blocks introduce a clear and intuitive way to understand the GPU resources available to your organization at any moment. They show exactly how much reserved capacity you have in Nebius and help you align that capacity with the needs of your workloads and development plans.

With Capacity Blocks, teams can easily track how their GPU resources are distributed over time: when each portion of capacity is booked, when additional expansion is planned, and how future availability aligns with upcoming experiments or production milestones (Figure 1). This visibility allows organizations to plan confidently, ensuring their pipelines run smoothly without unexpected pauses or unused windows of paid capacity.

Figure 1. Capacity Blocks shows different categories of booked capacity allocated for the selected month

In addition, Capacity Blocks streamline the process of creating instances. Users can associate each VM with a specific capacity interval, keeping workloads organized and simplifying capacity management across teams and projects.

Figure 2. Project-based capacity allocation within each Capacity Block

Within each Capacity Block, you can also see how GPUs are allocated between projects (Figure 2). This brings an additional layer of transparency for ML and research teams, enabling more efficient planning, collaboration and workload distribution.

Capacity Blocks is in gradual rollout phase. We are planning to migrate users and enable this feature during Q1 2026.

# Operate predictably with Capacity Dashboard and APIOperate predictably with Capacity Dashboard and API

We’re also introducing a public Capacity API that brings real-time transparency to on-demand and preemptible GPU availability across Nebius AI Cloud. This API gives users direct access to accurate capacity data, enabling them to automate decisions, integrate availability checks into their workflows and build more predictable compute operations.

Figure 3. Example of an API response showing available GPUs

This visibility improves the experience of launching services and virtual instances across the platform. Whether users are creating clusters for any of our managed services or apps, or spinning up individual VMs, they can rely on up-to-date information to choose the right region, fabric and GPU type with confidence.

Our partners who resell or integrate Nebius compute also benefit from this accuracy — the API provides consistent, reliable capacity data that can be surfaced directly in a partner’s own tools and provisioning flows.

For those working in the Nebius web console, the same information is available through the new Capacity Dashboard, a visual widget that shows real-time GPU availability in each region. Instead of checking availability during VM creation, users can explore capacity visually and select resources more easily. The Capacity Dashboard and API enhance transparency across the platform and help teams make faster, better-informed decisions on consuming infrastructure.

Capacity Dashboard and Capacity API are in a private preview state with a limited set of users and will be gradually rolled out to public preview also in Q1 2026. Please contact support or your account executive if you are interested in being included in the first adopter list.

# Building a more transparent platformBuilding a more transparent platform

Availability of AI compute remains a critical factor for ML teams and AI-driven businesses, shaping both day-to-day productivity and long-term strategic decisions. Even small gaps in available infrastructure can slow down experimentation, disrupt research timelines or leave valuable capacity underutilized.

At Nebius, we’re committed to giving our users not only powerful GPU infrastructure but also the clarity and control needed to use that infrastructure to its fullest. With Capacity Blocks and Capacity Dashboard, we’re bringing greater transparency and predictability to capacity management, making elasticity more accessible and more actionable for teams of all sizes.

We will continue to evolve the Nebius platform with features that enhance visibility, improve user experience and ensure that AI practitioners always have the compute they need, exactly when they need it.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- Build confidently with Capacity Blocks

- Operate predictably with Capacity Dashboard and API

- Building a more transparent platform

## See also

### 

Nebius AI Cloud “Aether 3.1” release: Next-gen compute for AI operations at scale

The Nebius AI Cloud 3.1 release continues the evolution of our platform into a transparent, orchestrated, developer-first environment — where performance is accessible, capacity is visible and control feels effortless. Across new platforms based on NVIDIA Blackwell Ultra, smarter capacity management and an improved experience for both developers and platform operators, every enhancement moves us closer to that goal.

December 17, 2025
5 mins to read

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Running NVIDIA NIM and NVIDIA Blueprint in Nebius AI Cloud

In this blog, we will take a look at how teams can deploy the four NVIDIA NIMs available now in our platform, how they can be consumed via their API and how they can fit into larger scientific workflows. It also covers the Virtual Screening Blueprint, which turns folding, molecule generation and docking into a ready workflow that becomes available in JupyterHub shortly after deployment.

December 17, 2025
9 mins to read

Sign in to save this post
Sign In
