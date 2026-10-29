# Behind the AI Cloud “Aether” release: Giving enterprises the control they’ve been asking for

Source: https://nebius.com/blog/posts/behind-aether-release-control-for-enterprises

Skip to main content

At Nebius, we’ve spent the past year working closely with enterprises that are moving AI projects from experiments to business-critical systems. The challenges they raise aren’t about “getting more GPUs” — they’re about how to govern, secure and scale AI infrastructure without creating bottlenecks for their teams.

That’s the backdrop for our latest AI Cloud 3.0 release, named “Aether” and announced today. It introduces features that make our AI Cloud platform better suited for organizations that need to run sensitive workloads at scale, in highly regulated environments, while still keeping the platform easy to use for builders.

# Compliance that opens doorsCompliance that opens doors

One of the biggest blockers to scaling AI in industries like healthcare and finance is regulatory approval. To clear that path, we’ve added new certifications: SOC 2 Type II, (including HIPAA section), and ISO 27001. We’ve also aligned our security program with NIS2, DORA and additional ISO standards. This isn’t just about checkboxes. It means a bank can move faster on fraud detection pipelines, or a hospital can deploy imaging models, without waiting months for infrastructure reviews.

# More control without the red tapeMore control without the red tape

When AI is running in production, IT and security leaders need more than coarse controls — they need granular levers. With Aether, we’ve added:

- A brand new set of observability features that combines metrics from different services, including a Grafana-based dashboard for Managed Soperator (our hosted Slurm solution), displaying performance, reliability (check out industry-leading Mean Time Before Failure numbers in the screenshot 🙂) and power usage metrics. We have added search functionality into logging that gives operators visibility into what’s happening under the hood across the board.

Figure 1. The new Grafana-based dashboard

Figure 2. Storage observability dashboard

- 

Advanced IAM capabilities that unlock faster and better collaboration across multiple teams in secure manner. The goal: to make it easy for administrators to set the right guardrails, without forcing developers into ticket queues or slowing their pace.

- 

Now new tenant definition and creation is self-service, which eliminates the need to raise tasks and waste time.

- 

Finer-grained IAM roles allow access policy enforcement at the level of tenant or project level, depending on use case, including support for custom group creation.

- 

Additional networking options such as Cilium support for Kubernetes and VPC static routing, enable more customization and traffic control.

- 

A new built-in secrets management (MysteryBox) that eliminates the security risks of API keys floating around in scripts.

# Reliability and performance at scaleReliability and performance at scale

Reliability and performance are two of the areas that we are mostly proud of here at Nebius — and that work is always ongoing. Only in the last quarter, we have added additional health checks, reducing the number of maintenance tasks related to network. We are now introducing:

- 

Active health checks that run continuously in Managed Soperator — soon to come for across all managed Kubernetes environments.

- 

Self-healing nodes that can repair themselves when issues arise in Managed Kubernetes and Managed Soperator.

When it comes to performance and specifically storage speed, on top of recent blazing fast numbers (up to 16 GBps per 8 GPU VM for Object Storage and more than 1 TBps for file storage in aggregate), this time we outperformed ourselves; we have now achieved 100% increase in the speed of our homegrown file storage write capabilities (from 4 GBps to 8 GBps for a 8 GPU VM), and more than 50% for read (from 8 GBps to 12 GBps). Similar performance enhancements apply to our WEKA-based storage option, now able to handle almost 20 GBps read/18 GBps write from 16 GBps read/10 GBps write for a 8 GPU VM.

Last but not least, earlier this fall we shared our latest MLPerf® Inference benchmark results and announced that we are one of the first NVIDIA Cloud Partners to reach Exemplar Status for training workloads running on NVIDIA H200 GPUs.

# A smoother experience for AI developersA smoother experience for AI developers

Even as governance expands, we don’t want the platform to feel “heavier.” So we’ve shipped improvements aimed directly at developer productivity with the Aether release:

- A refreshed developer-focused navigation and homepage that matches the way AI and ML teams actually work, including a simplified app launch catalog.

Figure 3. Refreshed UI and navigation

- 

In addition, we are making it easier to consume resources; users can create GPU instances without having to worry about CPU or memory quotas — they are being automatically allocated. The same applies for CPU instances. We also rolling our one SKU for GPU instances to simplify billing and reporting.

- 

We also introduced an easy and fast way to launch apps (e.g., Jupyter, ComfyUI, etc.) as container images over VMs — including bringing your own container images, of course.

Figure 4. New feature: launching VMs with preloaded container app images

- 

On our ecosystem platform integrations, we now support a fully hosted version of SkyPilot API Server (with Managed PostgreSQL) featuring one-click installation.

- 

Furthermore, we added an easy way to connect any Nebius cluster to Anyscale from our web console — on top of the open-source Ray option.

# Let’s build what’s next — togetherLet’s build what’s next — together

Nebius AI Cloud 3.0 “Aether” release is a result of close collaboration with our customers — and the next releases will be too. We will be sharing more details on our upcoming live deep dive and Q&A webinar to see the latest features in action and would also loved to hear from you. In the meantime, check out the walkthrough video below to explore what’s new, and drop us a note with feedback or feature ideas. We’re always listening.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Narek Tatevosyan
VP of Product

Contents

- Compliance that opens doors

- More control without the red tape

- Reliability and performance at scale

- A smoother experience for AI developers

- Let’s build what’s next — together

- Walkthrough video

## See also

### 

Nebius achieves NVIDIA Exemplar Status on NVIDIA H200 GPUs for training workloads

We’re proud to announce that Nebius is one of the first NVIDIA Cloud Partners to achieve NVIDIA Exemplar Status on NVIDIA H200 GPUs for training workloads. This recognition validates that Nebius meets NVIDIA’s rigorous standards for performance, resiliency, and scalability — addressing one of the most pressing challenges in AI infrastructure: ensuring consistent workload performance and predictable cost across clouds.

September 29, 2025
3 mins to read

### 

Fault-tolerant training: How we build reliable clusters for distributed AI workloads

When starting a job, you expect it to run without interruptions. This expectation holds true across many domains, but it resonates especially deeply with machine learning engineers who launch large-scale pre-training jobs. Maintaining a stable training environment is crucial for delivering AI results on schedule and within budget constraints.

August 28, 2025
9 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
