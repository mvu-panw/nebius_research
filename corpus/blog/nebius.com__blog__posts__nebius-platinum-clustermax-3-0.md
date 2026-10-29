# Nebius Rated Platinum in SemiAnalysis ClusterMAX™ | Nebius

Source: https://nebius.com/blog/posts/nebius-platinum-clustermax-3-0

Skip to main content

SemiAnalysis has rated Nebius Platinum in ClusterMAX™ 3.0, its highest tier for evaluating AI cloud providers.

The verdict in their own words? “Nebius is unquestionably an industry leader with strong offerings in every category.”

Platinum is proof of the kind of AI infrastructure we’ve been building: performant, resilient, observable, and engineered to hold up when real workloads hit real clusters.

SemiAnalysis didn’t stop at peak GPU performance. Over several months, its team ran training and inference workloads on live NVIDIA GB300 and NVIDIA HGX B300 clusters: burn-ins, storage under concurrent load, node and full-rack recovery.

Real racks, real conditions, the kind of load that breaks the type of infrastructure that only looks good on paper.

## Good clusters are reliableGood clusters are reliable

When you think of a good cluster, you think of it being boring and reliable.

This is how SemiAnalysis described us: “A good cluster is generally boring. On Nebius, burn-ins run without errors; Slurm is topology-aware; the packages we need are on the cluster and generally recent; WAN is good; the orchestration layers are free of footguns.”

For infrastructure teams, that kind of boring is hard to build, and when you’re choosing where to run production AI, it means less time firefighting infrastructure and more time running the workloads you actually care about.

The report also singled out Soperator, our open-source Slurm-on-Kubernetes solution, as a technical point of distinction: it combines the scheduling model HPC teams expect from Slurm with Kubernetes underneath, using a /jail persistent volume backed by VirtioFS to abstract away the storage complexity that usually comes with running Slurm over Kubernetes.

Soperator can run on-premises or in other clouds, and its adoption already extends beyond Nebius. SemiAnalysis noted that other vendors supplied test clusters built on Soperator.

SemiAnalysis’s take: “Nebius’s approach makes this stress-free for the operator.”

## Stress the storage. Find the problem. Fix it. Test againStress the storage. Find the problem. Fix it. Test again

Testing surfaced real problems, and Nebius fixed them before the report closed.

Under high-concurrency storage workloads, SemiAnalysis found slow 4 KiB sequential allocating writes and metadata consistency issues during concurrent directory creation at 128+ ranks.

So we retuned the filesystem. Then they tested it again.

The errors were resolved. Per-client performance outperformed the median, and SemiAnalysis verified that the storage layer scaled to demanding workloads across two racks.

## Break a node. See what happensBreak a node. See what happens

SemiAnalysis also tested what happens when the hardware itself stops cooperating. After a synthetic error was injected into an NVIDIA GB300 NVL72 rack, Nebius detected the failure immediately and automatically returned the node to service. No manual intervention was required. That matters on NVIDIA GB300 NVL72, where node failures are considerably more complicated to handle than on traditional NVIDIA HGX systems.

SemiAnalysis notes that the other NVIDIA GB300 NVL72 racks it tested did not automatically reboot and return failed nodes.

“The fact that this process is self-driving counts in Nebius’ favor.”

## Visibility is paramountVisibility is paramount

Automation only matters if operators can see what’s happening underneath it. SemiAnalysis called the dashboards we provided “an excellent suite” for cluster health visibility.

Health checks, automated remediation, and observability are the same problem from three angles: keeping GPU infrastructure operational without making customers manage that complexity themselves.

## The bar stays highThe bar stays high

Platinum is significant because of what sits behind it: independent testing of the infrastructure, including the parts that are difficult to get right and easy to overlook.

It’s the standard we’ve been building for.

Learn more about the results here.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

Introducing the Nebius AI Builder Program: build AI systems you own on an open, independent stack

Today we’re launching the Nebius AI Builder Program: one place to build and scale AI systems on open models and independent tools, with no lock-in to a single vendor. Members get $400+ in credits and discounts across the stack, cookbooks with working code, free courses from Nebius Academy and NVIDIA DLI, certifications, expert office hours, and a community of builders.

September 10, 2026
9 mins to read

### 

Nebius achieves NVIDIA Exemplar Cloud on NVIDIA GB300 for training: Validated performance for hyperscale AI

Nebius has achieved NVIDIA Exemplar Cloud status on NVIDIA GB300 NVL72 for training, meeting the 95% performance threshold across NVIDIA’s reference benchmarking recipes. In this post, we explain what this validation means in practice and how it fits into Nebius’s broader work with NVIDIA on building production-grade AI infrastructure.

April 29, 2026
6 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

Sign in to save this post
Sign In
