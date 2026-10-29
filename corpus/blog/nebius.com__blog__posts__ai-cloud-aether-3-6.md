# Nebius AI Cloud “Aether 3.6”: Operating production AI with more control, efficiency, and confidence

Source: https://nebius.com/blog/posts/ai-cloud-aether-3-6

Skip to main content

Every quarter, we move our AI cloud platform forward by listening to customer feedback and addressing the realities of running AI in production. As companies bring AI into the core of their business with maturity and scale, their needs for control, confidence, and efficiency have evolved, demanding enhanced security for sensitive workloads, enhanced costs and control, and an improved day-to-day developer experience.

This platform release, Aether 3.6, responds to our customers’ needs by bringing together a new, AI-native way to manage your cloud, features to make the dev teams’ work more efficient, a stronger security and compliance foundation, and significant advances in our storage portfolio.

## Nebius Echo: natural-language control over your cloudNebius Echo: natural-language control over your cloud

Nebius Echo is an AI agent built directly into the web console, available the moment you log in, with no setup required. It understands your environment, answers questions about your infrastructure in context, and executes commands with guardrails that prevent unintentional actions.

Today, Echo handles straightforward operations across core services. Looking ahead, it will support infrastructure investigation to help with debugging, and multi-step deployments through Infrastructure-as-Code (IaC).

Echo runs on open-source models hosted on Token Factory, our own inference platform. The same infrastructure our customers use for production managed inference powers Echo itself, giving us direct control over response quality, accuracy, and latency.

Read how and why we built Nebius Echo

## A smoother experience for developersA smoother experience for developers

A significant portion of what ML engineers and data scientists spend time on has nothing to do with ML. It’s onboarding, setup, configuration, and the accumulation of small steps required before a workload actually runs. This quarter, we delivered platform enhancements designed to improve the developer experience.

Managed Service for SkyPilot takes a tool many ML engineers already rely on and removes the setup that often gets in the way. SkyPilot is a widely used open-source framework for running batch jobs and managing workloads across cloud environments, but getting it running has always meant spinning up a VM, configuring the control plane, and managing it yourself. Managed Service for SkyPilot makes a fully managed control plane available with one-click deployment directly from the Nebius console. ML engineers get SkyPilot functionality immediately, without provisioning anything, and can start scheduling jobs within minutes of enabling the service.

The instance creation workflow, whether for managed Kubernetes clusters or virtual machines, has been redesigned from the ground up. It now follows a structured, step-by-step guidance flow that mirrors how teams actually think about setting up their environments. Alongside this, a new version of our pricing calculator is now embedded in the creation flow across all services, giving users accurate cost estimates for their selected configuration and time range before committing. (These features will be fully available in July 2026.)

Figure 1. Step-by-step configuration flow for managed Kubernetes clusters

A unified Notification Center now consolidates critical alerts — billing events, maintenance notifications, and system alerts — directly in the web interface, in addition to email. Notifications are tied to the user and work across tenants, so you can see which tenant a notification belongs to and navigate there directly.

We’ve also added Global Search to the console: a single search bar that finds any service or document and takes you there directly, without manually working through the menu structure.

Figure 2. Global Search simplifies navigation within the console

## New security and governance features for sensitive workloadsNew security and governance features for sensitive workloads

Enterprise AI workloads increasingly operate under compliance requirements that were designed for traditional infrastructure, and meeting them in an AI cloud context demands specific controls. Aether 3.6 delivers a coordinated set of security and governance capabilities for teams running AI at scale in regulated or security-sensitive environments.

Key Management Service (KMS) lets customers create and manage their own cryptographic keys for encrypting workloads and data on Nebius AI Cloud. The service follows the customer-managed encryption keys (CMEK) model, whereby Nebius runs the KMS infrastructure and customers control the key lifecycle. KMS supports symmetric and asymmetric key types, regional key storage, and cryptographic erasure through key material destruction for regulated data deletion requirements. For organizations in healthcare, financial services, and other sectors where key ownership is a prerequisite for cloud adoption, this removes a fundamental barrier.

Many organizations running AI today operate across multiple cloud environments, with Nebius handling heavy compute while other systems run adjacent workloads. Workload Identity Federation (WIF) lets environments communicate securely without long-lived credentials. Workloads in external clouds can interact with Nebius using short-lived federated identities, and the same applies in reverse. This eliminates credential sprawl and the operational burden of managing static secrets across environment boundaries.

For large organizations with Slurm-focused ML teams, getting engineers access to provisioned clusters has historically required manual credential distribution, creating delays, audit gaps, and security exposure. IAM-based access to Soperator, our managed Slurm-on-Kubernetes solution, replaces that flow entirely. ML teams receive access through the same IAM policies that govern the rest of the platform: no manual credential handoff, better auditability, and access that can be revoked or updated centrally.

Managed Kubernetes API access control lets users restrict access to the Kubernetes API server to a defined set of IP ranges, ensuring the cluster control plane is reachable only from known and trusted networks. Access policies can be updated without downtime or cluster recreation, so teams can adapt as their network topology changes.

Budgets brings cost governance to the same level as security controls. Users can now set spending targets for pay-as-you-go usage, configure threshold-based alerts, and receive notifications when costs reach pre-defined thresholds. For FinOps teams managing AI spends across multiple projects and teams, it replaces billing surprises with predictable, controllable costs.

Figure 3. List of budgets presenting current spendings and pre-defined thresholds

Bring Your Own Image (BYOI) extends control to the virtual machine layer, allowing teams to deploy custom OS images rather than relying on platform-provided configurations. This is essential for organizations that maintain hardened or compliance-validated base images.

## Storage for large-scale AI operationsStorage for large-scale AI operations

Whether you’re managing training datasets, serving inference workloads, or running iterative research pipelines, the performance and cost profile of your storage layer directly affects how fast you can move and how steady-state production is reflected on your monthly bill. We build our storage stack in-house — both hardware and software — for maximum optimization, and Aether 3.6 brings several additions to that portfolio.

Object Storage now offers a third storage class alongside Standard and Enhanced: the Intelligent class. Designed for datasets and artifacts with unpredictable access patterns, it matches Standard class performance but automatically moves data to a lower-cost tier if it hasn’t been accessed for 30 days, with no need to configure lifecycle rules manually. Compared to Standard, the Intelligent class carries no request or egress fees, making it cost-effective for large datasets that see heavy use during certain project phases but then go quiet. For teams managing mixed workloads, it removes the need to manually decide where data lives and when to move it.

At the block storage layer, two new features improve cost efficiency and operational hygiene. Disk snapshots introduces native point-in-time copies of boot and secondary disk volumes, enabling backup, rapid recovery, and safe environment cloning without detaching disks or interrupting running workloads (fully available July 1). Managed disks functionality simplifies how block disks are created alongside VMs and ensures they are automatically deleted when the instance is removed. For teams running ephemeral clusters or tools like SkyPilot that rely on clean self-termination, this eliminates orphaned disks and the cost and overhead that comes with them.

New data centers now come equipped with Local SSD disks deployed directly on GPU servers. This storage improvement eliminates I/O bottlenecks, maximizing GPU utilization for the most demanding workloads: high-speed scratch space for training jobs, caching layers for large-scale reasoning inference, and fast intermediate storage for data pipelines handling large volumes between processing stages.

Storage performance is up across several production-critical paths. Using the Enhanced class, Object Storage now shows a 30% read bandwidth improvement for single-threaded connections, allowing clients to reach the full throughput the storage backend delivers. For Shared Filesystem, tests show 3x performance improvement for 4 KB file operations and up to 100x more IOPS for metadata-heavy workloads. Recent tests have also confirmed stable operation when scaling cluster size up to 100 PB, validating that Nebius storage can handle extremely large datasets with intensive parallel access.

## Other platform updatesOther platform updates

Aether 3.6 includes additional improvements to day-to-day operations across the platform. Datadog Log Management now integrates with Nebius AI Cloud logs, making troubleshooting and investigation quicker and easier. Kubernetes has been updated to version 1.34. Audit Log metrics are visible directly in the web console. Failure reasons are surfaced in compute notifications, making it faster to understand why a workload stopped. A full list of changes is available in our changelog.

## Building the cloud for production operationsBuilding the cloud for production operations

These improvements are part of our strategy to make Nebius the infrastructure choice of world-class AI teams, providing a platform to run workloads sustainably and with the governance, experience, and operational efficiency that production AI demands at scale.

And we want to make it easy for you to experience that, whatever stage you are at. So we’re launching the Nebius Builder Program in early preview: an initiative for developers, ML engineers, and AI practitioners who want to get hands-on with the platform without a large upfront commitment. Members receive credits across Nebius AI Cloud, Token Factory, and Nebius Academy, plus access to office hours with Nebius engineers and a builder community.

Alongside it, the Nebius Certification Program launches with its first credential, AI Cloud Ops (Associate), available for $1 during the early-bird period. Developed by Nebius Academy, the Certification Program will expand in July with additional credentials for AI application builders, solutions architects, infrastructure engineers, and business leaders.

If you’re ready to explore Nebius AI Cloud for the first time, we’re introducing a free trial with 5 dollars credit to spend on preemptible VMs so you can try the platform without an upfront billing commitment. The free trial unlocks once a card is linked and verified; standard pay-as-you-go quotas become available when a user tops up their balance by more than 25 dollars.

Sign up for the platform and try the Nebius platform for yourself!

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Narek Tatevosyan
VP of Product

Contents

- Nebius Echo: natural-language control over your cloud

- A smoother experience for developers

- New security and governance features for sensitive workloads

- Storage for large-scale AI operations

- Other platform updates

- Building the cloud for production operations

## See also

### 

Nebius AI Cloud “Aether 3.6”: Operating production AI with more control, efficiency, and confidence

Introducing Aether 3.6. Our latest quarterly platform release responds to how AI teams now operate at scale and with maturity, delivering a smoother developer experience, a stronger security and compliance foundation, advances across our in-house storage portfolio, and natural-language control over your AI cloud.

June 24, 2026
14 mins to read

### 

Introducing the Nebius Agents Blueprint: open architecture for production-ready AI agents

Today we’re introducing the Nebius Agents Blueprint, an open reference architecture for building, operating, and continuously improving AI agents in production. This post covers the six-component composable stack — inference, orchestration, retrieval, grounding, observability, and simulation — and the case study behind it: a compliance audit agent that achieved 72% lower cost and 20% higher precision over a GPT-based prototype by improving the system, not the model.

June 10, 2026
6 mins to read

### 

Introducing Nebius MCP Server: The LLM-native way to manage your AI Cloud

Skip the CLI commands and web console clicks — just ask Claude about your cloud infrastructure. Today, we’re excited to announce the Nebius MCP Server, our integration that connects Claude by Anthropic, or other AI chatbots, to the Nebius AI Cloud infrastructure.

July 16, 2025
5 mins to read

Sign in to save this post
Sign In
