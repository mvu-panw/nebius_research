# Nebius AI Cloud: Q3 2026 updates

Source: https://nebius.com/blog/posts/compute-cloud-platform-q3-2026

Skip to main content

Listening to customers helps shape what we build next. As they scale training and inference, their priorities extend beyond just GPU performance: connecting workloads to existing systems, keeping control of resources and costs, and helping teams move faster.

Those priorities shaped our Q3 work on the cloud platform: the infrastructure and tooling layer of the Nebius AI Cloud. Here’s a look back at what we built, from private connectivity, updated demand-based GPU pricing to simpler ways for developing and running workloads.

Let’s walk you through some of the key areas that we have been focusing on.

## Connect AI workloads securely to existing environmentsConnect AI workloads securely to existing environments

AI environments are heterogeneous by design, and this release treats that as a requirement: a private network path into Nebius, updates to our Data Transfer Service and integrations that slot into the security tooling larger organizations and enterprises already run.

Cloud Interconnect is a dedicated private connection between Nebius AI Cloud and customer networks. It gives enterprises a secure, predictable, high-bandwidth path that never touches the public internet, with MACsec encryption on the last mile. That means no performance penalty for protecting traffic. Customers choose what sits on the other end whether that’s on-premises data centers, colocations, or another public cloud. The result is that multicloud becomes something customers build on their own terms, with no bilateral agreement between providers to wait on. And because available 100G and 400G ports can be aggregated, bandwidth scales with the most demanding requirements.

Our Data Transfer Service now supports Nebius Shared Filesystem, alongside S3-compatible object storage. Customers can move data between any S3-compatible storage and in and out of Nebius filesystems with no custom scripts and no transfer infrastructure to stand up. That’s particularly important when migrating onto Nebius and replicating data across regions.

Compatibility shapes how we build the platform. This quarter, our Managed Kubernetes service achieved CNCF Kubernetes conformance certification, validating its alignment with upstream standards. That supports customers’ ability to use familiar tools and maintain portability as their infrastructure needs change.

We’re also working to make it easier for security teams to extend their existing practices to Nebius. Our upcoming Audit Logs export for SIEM integration will feed Nebius activity into established security workflows through a customer-owned Nebius Object Storage bucket, without requiring a service to poll our API. Retention, encryption and access settings will remain under the customer’s control.

That work will extend to cloud security posture management, starting with native support for Wiz. The goal is to let teams investigate misconfigurations in their Nebius environment alongside the rest of their infrastructure, using the security tools they already rely on.

## Control AI spend and make better use of capacityControl AI spend and make better use of capacity

As more teams share an AI platform, understanding consumption becomes as important as provisioning resources, especially with current market conditions. Customers need to know which workloads generate costs and how shared capacity is allocated.

Last year, we introduced our Preemptible Virtual Machines (PVMs) instances offering. PVMs run short-term, flexible workloads on platform capacity that is already allocated but sitting idle. Adoption came quickly, including among Serverless AI users. In a market where GPU capacity is limited, pulling more usable compute out of every deployed GPU creates more AI value from the same energy input, at a significantly reduced price for the user.

This quarter we announced Spot pricing for PVMs, that sets pricing dynamically and algorithmically, reflecting real demand for a specific GPU type in a specific Nebius region. The current price and up to 30 days of history are visible. We think this benefits everyone: cost-sensitive teams can see when a pool is typically quiet and schedule flexible work into those windows, and teams that care more about finishing than saving can follow the price and keep running.

Other new features help organizations be more in control of usage. Cost allocation labels let organizations attribute spending across teams, projects and environments using their existing labeling structure. A monthly usage and cost breakdown provides a downloadable PDF for accounting and reconciliation. Project limits for Capacity Block Groups let administrators control how much of a reserved pool each project can consume, preserving capacity for other teams.

Specifically around storage, new Object Storage tagging lets teams track objects by tag and apply lifecycle rules to objects carrying specific tags. And finally, Bucket Inventory catalogs and analyzes existing buckets, giving quick access to an object list when you need to audit or report on last access, last modified date, or encryption status.

## Build faster with new Serverless AI featuresBuild faster with new Serverless AI features

“A working Python script should be a short step away from a running job”. Since launching Serverless Jobs and Endpoints earlier this year, feedback from customers and the Serverless AI Builders Challenge has helped us identify where that path still takes too much effort: preparing environments, packaging code and getting configuration files into a workload. Those steps became the focus of this quarter’s Serverless AI updates.

One example was particularly telling: developers trying to pass a single fine-tuning configuration into a job were creating and mounting an S3 bucket to do it. That was a recurring onboarding blocker we could address directly. File injection now lets them supply the configuration at launch. The same thinking led us to support Python files directly in Serverless Jobs, removing the need to build a Docker container before running them.

We also want the work invested in an environment to carry forward. Serverless AI Devlab gives developers a CPU or GPU workspace that preserves their progress when compute stops or restarts. They can start with a familiar environment such as JupyterLab, Coder Server, or bring their own image. Across Serverless AI, new validated templates now bring together compatible framework versions and recommended GPU types, reducing the setup decisions required for a first run.

These are practical changes, but their effect compounds as teams experiment. Each configuration they can pass directly, environment they can reuse and packaging step they can skip shortens the next iteration.

## Less friction between you and the work that mattersLess friction between you and the work that matters

One theme runs through the rest of this last quarter: less time getting to the work, more time on the work itself. It’s an ongoing priority for us to make developers’ lives easier so they can focus on their actual work instead of managing infrastructure.

This quarter, we made both interactive access and automation more straightforward. Cloud Shell gives users a pre-authenticated terminal in the browser, while the REST API makes every public Nebius service accessible over HTTP and JSON using existing IAM credentials. Teams can bring Nebius into their scripts and CI pipelines, with a published OpenAPI specification that tools and agents can also consume.

And as agents take on more infrastructure work, access alone is only part of the problem. They also need practical knowledge of how to use the platform well. Our new public GitHub repository of Nebius skills puts guidance from customer engineering into instructions coding agents can read and act on. Alongside that, improvements to Nebius Echo, including chat history and more room for longer conversations, support the multi-step work users are already doing with our infrastructure agent.

The same attention to unnecessary setup extends to evaluating and testing on Nebius. Teams can now browse the AI/ML application marketplace before signing in, see which environments are available and plan around them. Once developing, they can use Tunnels to make a local service reachable for testing without opening firewall ports. These are moments where the platform can make the next step easier, from choosing an environment to sharing something that works.

## The results speak for themselvesThe results speak for themselves

The most rewarding moment for our engineering team, beyond witnessing our customers’ success, is seeing how the industry has been recognizing us lately. Our MLPerf Storage v3.0 submission supported the highest simulated accelerator count in the round on RetinaNet, alongside results for checkpoint writes and restores. Our MLPerf Inference v6.1 results were one of only two submissions on the next-generation NVIDIA Vera Rubin NVL72 platform and we earned five first-place results across 20 available category entries. And SemiAnalysis awarded Nebius Platinum in ClusterMAX™ 3.0, its highest tier, after evaluating training and inference workloads on live clusters.

For us, these are meaningful signals that the engineering behind the platform is translating into performance and reliability customers can use. Their feedback will continue to shape what we build next.

This blog covers the cloud platform layer of that work. For everything we delivered across Nebius AI Cloud — including managed inference with Token Factory and agentic search with Tavily — explore our Q3 What’s New page.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Narek Tatevosyan
VP of Product

Contents

- Connect AI workloads securely to existing environments

- Control AI spend and make better use of capacity

- Build faster with new Serverless AI features

- Less friction between you and the work that matters

- The results speak for themselves

## See also

### 

Nebius Rated Platinum in SemiAnalysis ClusterMAX™ 3.0

SemiAnalysis has named Nebius a Platinum AI cloud provider, the top tier of its ClusterMAX™ 3.0 rating. The rating is based on live testing of production clusters: burn-ins, storage under concurrent load, and automated failure recovery on real NVIDIA GB300 and NVIDIA HGX B300 hardware. This post covers what the testing found and why it matters for teams choosing where to run production AI.

September 23, 2026
7 mins to read

### 

Introducing spot pricing for preemptible VMs

Nebius introduces dynamic spot pricing for preemptible VMs, automatically adjusting prices based on available capacity and real-time demand. Users can set a maximum price to control costs or follow the spot price to prioritize access to capacity. The new pricing model gives AI teams more flexibility to manage their GPU compute spending.

September 22, 2026
9 mins to read

### 

Introducing the Nebius AI Builder Program: build AI systems you own on an open, independent stack

Today we’re launching the Nebius AI Builder Program: one place to build and scale AI systems on open models and independent tools, with no lock-in to a single vendor. Members get $400+ in credits and discounts across the stack, cookbooks with working code, free courses from Nebius Academy and NVIDIA DLI, certifications, expert office hours, and a community of builders.

September 10, 2026
9 mins to read

Sign in to save this post
Sign In
