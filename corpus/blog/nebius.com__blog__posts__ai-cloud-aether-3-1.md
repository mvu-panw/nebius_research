# Nebius AI Cloud “Aether 3.1” release: next-gen compute for AI operations at scale

Source: https://nebius.com/blog/posts/ai-cloud-aether-3-1

Skip to main content

AI workloads are growing faster than ever, demanding not only more performance but also better visibility and control. As models scale and competition intensifies, our mission remains the same: to make the AI cloud powerful, transparent and effortless to use.

This release of Nebius AI Cloud 3.1 continues the evolution of our platform into a transparent, orchestrated, developer-first environment — where performance is accessible, capacity is visible and control feels effortless.

Across new platforms based on NVIDIA Blackwell Ultra, smarter capacity management and an improved experience for both developers and platform operators, every enhancement moves us closer to that goal. Here’s what we are delivering.

# Revealing next-gen compute valueRevealing next-gen compute value

We’re proud to be the first cloud provider in Europe to deploy NVIDIA Blackwell Ultra systems in production. We’ve made the latest NVIDIA HGX B300 systems available to customers and recently brought online rack-scale NVIDIA GB300 NVL72 systems.

These new sites received the NVIDIA Quantum-X800 InfiniBand platform, enabling Europe’s first GB300 NVL72 on this next generation of high-speed fabric, delivering 800 Gb/s of end-to-end connectivity with ultra-low latency. Continuing to improve the rest of the stack to unleash the potential of next-gen compute, we’ve also made a series of enhancements to eliminate potential bottlenecks:

- 

Applied hardware-accelerated network, offloading operations from CPUs to NVIDIA ConnectX-8 SuperNICs, which boosts throughput for Object Storage and other high-traffic services.

- 

Optimized the VPC data path, improving data transfer speeds within a region.

- 

Implemented write-back cache for the shared filesystem, enabling faster write operations.

- 

After extensive testing, we confirmed that the shared filesystem can now scale performance linearly up to 4 PB, while its theoretical volume remains effectively unlimited.

Having the latest NVIDIA AI infrastructure in place is a major milestone for us and entails an enormous amount of engineering work behind the scenes. Beyond all the improvements above, we carefully tested and optimized the performance of every single host, reflected in our leading positions among other providers in the latest MLPerf® Training v5.1 benchmark round.

# Making capacity visibleMaking capacity visible

As next-generation GPU systems become available, efficient capacity management becomes just as critical as raw performance. These new accelerators are powerful and in high demand, so having more control over requested and available compute is essential for smooth operations and cost management.

To make this process easier, we’re introducing new tools that bring more clarity and visibility into how resources are planned and managed.

Capacity Blocks introduce a new concept for organizing reserved capacity. Each block represents a defined time interval and number of GPUs — making it easier for operators to plan, track and visualize their reservations. The new design also includes a graphical representation in the console, offering a clear overview of available and booked capacity at a glance.

Figure 1. Capacity Blocks shows different categories of booked capacity allocated for the selected month

Additionally, we’re launching a Capacity Dashboard to provide accurate information about GPU availability across Nebius data centers. Whether creating an on-demand or preemptible VM or cluster, users can now instantly see available GPUs — saving time and improving planning accuracy.

We also introduced project-level quotas, allowing administrators to control usage and resource distribution within a tenant more precisely. By setting project-specific quotas, admins can prevent overconsumption and optimize costs, while ensuring teams have the resources they need to stay productive.

Capacity Blocks is in gradual rollout phase. We are planning to migrate users and enable this feature during Q1 2026.

Capacity Dashboard and Capacity API are in a private preview state with a limited set of users and will be gradually rolled out to public preview also in Q1 2026. Please contact support or your account executive if you are interested in being included in the first adopter list.

# From power to precisionFrom power to precision

As AI workloads grow in complexity, precision becomes just as important as power. Having the best compute only matters if developers can easily orchestrate, scale and monitor their workloads. That’s why the Aether 3.1 release brings several improvements aimed at refining the developer experience — making the AI cloud not only stronger, but also smoother to build on.

We updated Object Storage with lifecycle rules based on last access, which automatically move less frequently accessed data from Enhanced to Standard buckets according to timestamps, helping customers manage storage costs efficiently without manual data migration.

We’ve launched JavaScript SDK to simplify integration of our cloud into partner platforms, added the ability to attach and detach secondary network disks on running VMs, and updated Managed Soperator, our Slurm-on-Kubernetes solution, with enhanced notifications, better reliability during NIC flaps and the ability to scale clusters up or down directly through Slurm commands. Continuing the improvements for MLOps users, we’ve also expanded our ecosystem: dstack is now available as a Kubernetes application in our app catalog, which means it can be deployed easily just with a few clicks.

We’ve made several updates that enhance visibility and usability directly in the interface. The tenant overview page now provides a clearer snapshot of a customer’s environment, displaying key operational metrics and status updates in one place. To help users stay informed, we added proactive notifications and warnings when important alerts or updates haven’t been enabled — ensuring administrators never miss critical information about their workloads or billing.

In addition, billing exports now follow the FinOps Open Cost and Usage Specification (FOCUS) standard, making it easier to analyze and optimize cloud spending using common FinOps tools. This format brings consistency and transparency to cost management, allowing teams to align financial visibility with their operational metrics.

# When control means usabilityWhen control means usability

Security and governance remain at the core of enterprise adoption. As AI projects scale across teams and regions, visibility, compliance and fine-grained access control become essential for building trust and keeping data protected. With Aether 3.1, we continue to expand on how customers can control, monitor and secure their environments without adding complexity or unnecessary risk.

To support this, we introduced per-object access control for Object Storage buckets, enabling administrators to grant precise permissions based on IAM rules. Access can now be defined at the object level, improving data governance while preserving flexibility for different users and workloads.

In network security, new Security Groups for VPC allow more granular control over inbound and outbound traffic, simplifying firewall configuration and reducing exposure to potential risks.

We also enhanced Identity and Access Management (IAM) to make administrative control both stronger and easier to use. The updates include:

- 

Log in with Microsoft accounts for seamless federation,

- 

GUI-based SSO management, in addition to API and CLI,

- 

Administrative project deletion for easier workspace organization,

- 

and new GBAC service roles for clearer, more efficient permission management across services.

Together, these features make Nebius AI Cloud even more secure and manageable — giving enterprises the governance they need in a form that feels intuitive and user-friendly.

# Empowering healthcare and life sciences teamsEmpowering healthcare and life sciences teams

At Nebius, we firmly believe that generative AI is transforming the Healthcare and Life Sciences domain, accelerating innovation and scientific research. To support customers in this industry, we’ve introduced a set of improvements that make Nebius AI Cloud more aligned with the day-to-day needs of research teams.

We’ve extended Audit Logs to include data-plane events, allowing users to track every operation performed on Object Storage objects. This level of observability helps teams implement and verify HIPAA-compliant configurations — a critical requirement for organizations building healthcare or life-science solutions in the cloud.

To further support domain-specific work, customers now have simple access to NVIDIA NIM microservices — Boltz2, Evo-2, GenMol and MolMIM — without the need for an NGC key or NVIDIA AI Enterprise licenses for end users. These models give researchers powerful AI-driven tools for faster iteration in molecular design and early-stage discovery workflows for drug development and life-science research.

# Looking forwardLooking forward

You can check out the video overview of the release below. With the Aether 3.1 release, we’ve continued shaping our AI Cloud platform into an environment where performance is accessible, capacity is visible and control feels effortless. Each improvement, from the latest NVIDIA GPU compute and transparent capacity planning, to new features that provide more governance and better developer experience, are steps we are taking in our vision to continue offering the ultimate AI Cloud for builders. Our direction remains the same: to make Nebius AI Cloud the most transparent, developer-first infrastructure for AI workloads at scale. Stay tuned for more exciting platform announcements coming soon!

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Narek Tatevosyan
VP of Product

Contents

- Revealing next-gen compute value

- Making capacity visible

- From power to precision

- When control means usability

- Empowering Healthcare and Life Sciences Teams

- Looking forward

- Video overview

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Visibility that drives elasticity: Introducing Capacity Blocks and Capacity Dashboard

Today, we’re expanding Nebius AI Cloud’s elasticity even further with the introduction of Capacity Blocks and Capacity Dashboard — two new capabilities that bring additional clarity to GPU capacity management and give users full confidence in the compute they rely on.

December 17, 2025
4 mins to read

### 

Running NVIDIA NIM and NVIDIA Blueprint in Nebius AI Cloud

In this blog, we will take a look at how teams can deploy the four NVIDIA NIMs available now in our platform, how they can be consumed via their API and how they can fit into larger scientific workflows. It also covers the Virtual Screening Blueprint, which turns folding, molecule generation and docking into a ready workflow that becomes available in JupyterHub shortly after deployment.

December 17, 2025
9 mins to read

Sign in to save this post
Sign In
