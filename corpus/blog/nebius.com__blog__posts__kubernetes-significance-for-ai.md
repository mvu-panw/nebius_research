# On Kubernetes significance for ML/AI engineers

Source: https://nebius.com/blog/posts/kubernetes-significance-for-ai

Skip to main content

In the ever-evolving landscape of machine learning, the infrastructure that supports it plays a pivotal role, standing out as the key component that enables seamless execution of algorithms, training of intricate models, and effortless data management.

When we talk about the infrastructure, the spectrum is broad. There are simplistic, lightweight models that don’t require immense computational power. Such models can be deployed on a single node. Other times, one node won’t be enough, and you’ll need to do parallel training across numerous nodes outfitted with GPUs. The latter is standard practice for high-performance tasks such as training LLMs or parsing vast data arrays.

Network-wise, the best way to achieve such parallelism is to interconnect the GPU nodes using InfiniBand. This solution offers speeds in the hundreds of gigabits per second and an efficient switched fabric topology. InfiniBand is the defining element in building and managing fault-tolerant, scalable multi-node infrastructure.

When we turn to software operating these InfiniBand-connected GPU compute resources, Kubernetes emerges as a standout for orchestrating. But what makes Kubernetes so good in this particular field? There are two main criteria.

K8s clusters in Nebius AI

## Criterion 1: Kubernetes as a productCriterion 1: Kubernetes as a product

At its core, K8s is an orchestrator, adept at autoscaling your fleet of machines exactly when needed. Whether it’s handling standalone applications (pod autoscaler) or managing physical nodes (node autoscaler), its flexibility is unmatched.

From an infrastructure perspective, node autoscaling is the standout feature of Kubernetes. Instead of juggling individual virtual machines, users can seamlessly control the entire cluster as they go. It’s a lifesaver, particularly when it comes to machine learning.

In other words, you only have to deploy a K8s cluster with multiple GPU-equipped nodes, and the system will orchestrate them from that point on. Using tools like Terraform, which we’ll discuss below, you can define your compute resource needs, set limits on the number of nodes, and then let K8s work its magic. It autonomously replaces crashed nodes, starts new nodes as needed, or shuts down excess active nodes to ensure the training cycle is uninterrupted.

This autonomy means ML engineers can focus on what they love most — training algorithms — without getting bogged down by infrastructure nuances.

## Criterion 2: Native toolingCriterion 2: Native tooling

After deployment, an ML engineer’s work is far from done. From driver installation to tool and environment setup, the MLOps life is complicated. Take GPU driver installation, for example. It’s an extremely time-consuming, yet non-negotiable step; every node needs the right driver.

With Kubernetes, though, this process becomes a breeze. By using a Helm chart with a GPU operator, engineers can instruct the K8s cluster to handle driver installation and testing for an entire zoo of newly deployed nodes. But what if there’s a need for driver modifications — for instance, to account for corner cases? In this scenario, the YAML file serves as the universal command center. Set the driver type you need, and you’re good to go.

This centralized approach, combined with tools like Helm charts and cron jobs, makes software maintenance much less of a chore, which applies to both low- and high-level software. Change something once, and it’s applied everywhere. Achieving such streamlined operations on regular VMs would require writing cumbersome scripts and applying them across your VM fleet, costing both time and money.

Today, Kubernetes has no real alternatives: it’s established itself as the de-facto industry standard. The days of deploying standard Docker containers are long gone. The shift to K8s containers is evident, and for good reason. Its long-standing presence means a wealth of knowledge is readily available, smoothing the learning curve and encouraging collaborative learning.

## From self-managed to cloud provider-managed KubernetesFrom self-managed to cloud provider-managed Kubernetes

Let’s say we all agree that Kubernetes is one of the most effective ways to orchestrate VM clusters for ML and related tasks. But while K8s offers automation for VM clusters, it doesn’t exempt ML practitioners from some infrastructure responsibilities. Kubernetes itself needs setup, configuration, and continuous monitoring.

This is where managed Kubernetes comes in. In the Nebius AI implementation, the Managed Service for Kubernetes shifts all master maintenance to the platform side. Updates and patches, security-related or otherwise, are installed without any hands-on intervention. All you have to do is set the version and release channel — and a single button click in the UI sets the updates in motion. We also provide out-of-the-box operational logging, so instead of wrestling with kubectl in the terminal, users can see all the logs in an easy-to-use GUI.

Creating a cluster using Managed Kubernetes in Nebius AI

Suppose a pod is acting up due to a stuck job. Our experience shows that most admins, experienced with kubectl or not, would prefer to look at a GUI first, and only then run the necessary kubectl command. This is a significant increase in admin efficiency, sparing them some of the updating, patching, and versioning responsibilities.

These kinds of maintenance tasks are a lot of work, especially with large clusters. On top of that, without managed Kubernetes, an engineer has to keep track of all K8s updates and read up on any new vulnerabilities, which can be quite a time sink. With Managed Service for Kubernetes, these concerns evaporate.

## A separate deployment product, TerraformA separate deployment product, Terraform

Though the benefits of K8s are evident, it’s not one of the K8s tools that offers an easy entry into actual deployment. For that purpose, there’s a separate product called Terraform.

Terraform falls under the “infrastructure as code” umbrella. It’s a tool to manage infrastructure state, allowing you to outline configurations using a few pages of code. Such tools have been around for quite a while. If you work at a major IT firm, you might recognize another product in this domain — the open-source solution, Salt. Configuration managers and various other tools that translate infrastructure deployment into pages of code are all encompassed by the concept of “infrastructure as code.”

But what made Terraform the industry standard? Its user-friendliness and declarative nature. Writing manifests with Terraform is straightforward, and reading them is even more so. Furthermore, a range of supplemental tools and widgets are available for Terraform. It’s gained widespread popularity, and most cloud vendors have their own Terraform provider, enabling clients to interact with infrastructure just as they would via the UI or CLI, if not more extensively.

A fitting real-world analogy would be construction. If setting up a cluster equates to raising an architectural masterpiece, then the Terraform manifest serves as its blueprint.

Terraform is intelligent. Let’s say you’ve made a specific change in the cluster parameters, and you click Apply. Terraform will notice the modification and ask if the changes are indeed correct. After your confirmation, it won’t touch the broader infrastructure but will only adjust the needed particular fragments. You can also deploy this same configuration in a different directory or another cloud.

Kubernetes and Terraform work harmoniously since their core philosophies align. Terraform tackles a potentially challenging task — deploying clusters reproducibly. When considering an ML-ready setup with numerous GPUs, you might think along these lines: “I should deploy Kubernetes, but do I want to do it directly? I might need to replicate my cluster in the future, and having a comprehensive outline would be beneficial. Let me draft a manifest using the Terraform provider right away, encapsulating all my requirements from Kubernetes.”

You need to do this just once. The configuration you describe can be intricate, for instance, housing numerous nodes with H100 and A100 graphics cards. There might also be a GPU operator ensuring the correct GPU drivers are installed for each node group. The successful deployment of the manifest means it’s been tested and can be safely redeployed whenever needed. Given a sufficiently detailed blueprint, constructing a building that deviates from it becomes nearly impossible.

Terraform has many advantages, but one that stands out is indeed the reproducibility. Here’s one potential use case: when onboarding a client, our team of architects at Nebius AI can provide them with a ready-made manifest. Instead of having to figure out how the configuration tailored for that particular client functions within the cloud platform’s infrastructure, you can quickly skim through the manifest, plug in necessary parameters in a few places (or perhaps even avoid that altogether), and get a fully operational cluster. There’s no need for in-depth knowledge of Kubernetes — a basic understanding of Terraform’s principles is enough. This kind of expertise is much more commonly found in DevOps and MLOps teams.

## Freedom from vendor lock-inFreedom from vendor lock-in

Probably the last important thing about Kubernetes is that it’s platform agnostic. Imagine that you urgently need to switch cloud providers, either for cost savings or feature upgrades, and you need to take your ML workloads and environment with you. Migration could be a nightmare if your ML operations are tied to proprietary tools unique to your current cloud provider. Sure, extracting might be possible — but it’ll require almost insurmountable effort.

However, if you’ve been deploying your workloads on a server built on Kubernetes, especially managed Kubernetes, then you can migrate whenever you please. The only requirement is that your cloud provider is in sync with the K8s quality benchmarks, be it versions, tools, or the client-provider division of responsibilities.

At Nebius AI, we follow these standards diligently. This way, the ML teams are fully protected from vendor lock-in, and migration becomes a matter of person-hours, not weeks or months.

Having dived into Kubernetes, especially its managed variant, we uncovered four pillars relevant to ML tasks: the convenience of hassle-free infrastructure orchestration, one-click native tool installations, Terraform for reproducible deployment, and the absence of vendor lock-in. Here’s hoping your focus remains on creative tasks, like brainstorming that unique ML flow, free from the infrastructure routine.

## Managed Service for Kubernetes

Learn more​

## Documentation

Docs​
Step-by-step guides​

Levon Sarkisyan
CSA Team Leader

## Related links

Managed Kubernetes​
Documentation​

Sign in to save this post
Sign In
