# Slurm vs Kubernetes: Which to choose for model training

Source: https://nebius.com/blog/posts/model-pre-training/slurm-vs-k8s

Skip to main content

## The role of Slurm and KubernetesThe role of Slurm and Kubernetes

Slurm and Kubernetes solve similar problems and offer comparable services. Both can be used for model training or other high-performance computing tasks.

These systems aren’t exact equivalents and can be used for various purposes. Although it’s difficult to characterize Slurm and Kubernetes with a single term, I’ll refer to them as “workload managers, ” focusing only on the key aspects of their functionality.

I expect a workload manager to solve the following three tasks, each essential for effective HPC:

- 

Serve as an entry point for users to access their computing power. You might own half a data center, but you need a way to use it.

- 

“Hold” and manage hardware resources. Your resources are typically delegated to a workload manager to ensure all computational tasks follow the same rules.

- 

Implement scheduling algorithms for allocating resources and executing user workloads.

## How workload managers help trainingHow workload managers help training

Model training is an extremely complex task. It’s not only mentally challenging but also requires meticulous management of a vast stack of hardware and software. Fortunately, you can delegate part of this complexity to a workload manager, which will definitely help you save on headache pills.

Another area where a workload manager helps save money is on highly expensive equipment. These days, you can’t train a model to generate cute kitties on your personal computer (at least if you want them to be cute enough). For serious training, you need numerous servers, racks, high-performance GPUs, GPU switches, high-throughput & low-latency networks, various storage technologies and the like. A workload manager helps you utilize these resources more efficiently and divide them fairly among employees or departments.

If you use a cloud solution, it can also provide you with a simple scaling option based on your current needs.

## What is Slurm?What is Slurm?

First and foremost, Slurm is a nod to Futurama. But it’s also a powerful workload manager officially known as Simple Linux Utility for Resource Management.

This open-source project initially began in 2002 at Lawrence Livermore National Laboratory. A lot has changed since then, and now, after two decades of active development and constant feature additions, it’s no longer all that “Simple.” I think it’s time to replace this word in the acronym with “Sophisticated.”

Slurm is very popular in the HPC field. It’s used in over half of the Top 500 supercomputers worldwide (where our ISEG sits in the 19th spot). If you’re a research lab, university or large corporation doing HPC, you’re likely already familiar with Slurm. Compared to K8s, Slurm has a long history of running workloads for all kinds of institutions performing intense computations.

While Slurm wasn’t originally designed for model training, it has adapted well to current needs (for example, through support for GPU computing). Its original design was also much closer to current ML needs than that of Kubernetes.

It’s worth noting that the primary caretaker and the only team that can provide official enterprise support for Slurm is SchedMD, formed in 2010.

### Slurm designSlurm design

Figure 1. Architecture of a typical Slurm cluster. Source

Users interact with Slurm by connecting to one of the nodes in the cluster and executing command-line utilities. One important feature of this architecture is that users can’t run client utilities from their local computers. Instead, they establish SSH sessions to the cluster and work there: defining jobs as bash scripts, executing them, managing the cluster and reading job outputs from files. The user experience is very old-fashioned and “Linuxy.”

While not required, it’s quite common to have separate Login nodes, which don’t have significant computing power and just serve as an entry point for users.

The nodes where the slurmd daemons run are called Compute or Worker nodes — that’s where your cryptocurrency is actually mined. Usually, a single job uses many workers.

Slurm allows you to split one large job into many steps, some executed sequentially and some in parallel — simply using command-line tools and bash features. Slurm also includes a widely used integration with MPI.

For example, the srun --nodes=4 echo hostname command prints out the names of four nodes in the cluster. It blocks until the job is completed on each node.

The sbatch my_job.sh command starts a batch job that is queued for further execution. This is a non-blocking call.

The bash script you provide usually includes one or more srun calls (which are treated as separate steps) and has special comments telling Slurm about some parameters of the job and the resources it needs.

For example, my_job.sh may look like this:

# General job parameters: name, output file, time limit.
#SBATCH --job-name=my_job
#SBATCH --output=/home/bob/my_job.out
#SBATCH --time=10:00

# First allocation request: 2 nodes with 8 H100 GPUs on each.
#SBATCH --nodes=2
#SBATCH --gres=gpu:h100:8

# Second allocation request: 2 nodes with 8 A100 GPUs on each.
#SBATCH --nodes=2
#SBATCH --gres=gpu:a100:8

# Other resources, common for both allocation requests.
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=4G

# Print info about H100 GPUs.
# It runs the same command on 2 nodes with allocating 1 CPU,
# 4G of memory and 8 H100 GPUs on each.
srun --nodes=2 --cpus-per-task=1 --mem=4G --gres=gpu:h100:8 \
echo "Info about H100 GPUs on node $(hostname):" && \
nvidia-smi & # <- Continue without waiting

# The same step as above but for nodes with A100 GPUs.
srun --nodes=2 --cpus-per-task=1 --mem=4G --gres=gpu:a100:8 \
echo "Info about A100 GPUs on node $(hostname):" && \
nvidia-smi & # <- Continue without waiting

wait # Wait for the previous steps to complete.

# Run NCCL benchmarks on all 4 nodes with allocating 8 CPUs,
# 4G of memory for each CPU, and 8 GPUs of any model.
# Resource allocations for CPUs and memory aren’t specified
# here so values from #SBATCH comments are used.
srun --nodes=4 --gpus=8 \
　　echo "Run NCCL all-reduce benchmark:" && \
　　/usr/bin/all_reduce_perf -b 512M -e 8G -f 2 -g 8

You can retrieve the current execution state of this job by calling squeue, and read the current output in the file /home/bob/my_job.out.

A Slurm cluster also includes controller daemons slurmctld and, optionally, a database daemon slurmdbd, which together form the “control plane” of this system. The database can be used to store job history and various statistics, and to enable some advanced features relevant to multi-tenant clusters: limiting resources for different accounts, QoS, etc. The control plane is lightweight and can easily run on a single machine, but can also be duplicated for higher availability.

### Slurm advantagesSlurm advantages

People who use Slurm for model training have access to all sophisticated features specifically targeted at HPC.

Its scheduler is both clever and efficient, surpassing its competitors. It’s designed for supercomputers and can handle a massive scale (tens of thousands of nodes with hundreds of jobs per second).

Slurm implements deep control of hardware resources. For example, it distinguishes between CPU sockets, CPU cores and hyperthreads. You can even select a CPU that’s physically closer to a PCI bus. It also supports GPU sharding and network topology (you can allocate such a group of nodes so that data transfer between them passes through the least number of switches).

Additionally, Slurm is highly extensible with various plugins that can be a great asset in running ML workloads. For instance, you might want to use the containerization plugin Pyxis, an open-source product from NVIDIA. You can even write your plugins, and it’s not too complicated.

### Slurm drawbacksSlurm drawbacks

The disadvantages of Slurm also stem from its strong focus on HPC. While it provides many features, it lacks universality. Slurm is well-suited only for time-finite workloads on size-limited clusters. This is a relevant problem for ML because people who do training often want to do inference as well. Inference doesn’t work well on Slurm, so they have to maintain a separate system that also needs expensive hardware resources.

Slurm’s support for auto-scaling isn’t great — it’s mostly designed for a fixed scale. Though it provides some techniques for scaling your cluster more easily, it’s not an option for on-premise setups. Still, most cloud solutions have it.

While the initial bootstrapping of a Slurm cluster is quite simple, I can’t say the same about maintaining it over time. Slurm has a very annoying requirement: all nodes must be identical (Linux user and group IDs, software versions and the like). This burden often falls on the users’ shoulders. The life of Slurm administrators is also not easy: there are many “managed” solutions for Kubernetes in different cloud platforms, but there is no truly “managed” solution for Slurm, so the administrators have to do their job and can’t retire.

The user experience can be seen as both a pro and a con. If you got to know Slurm at university, this bash-scripting may be convenient. But if not, you won’t find a user-friendly UI for it. Also, there’s no up-to-date Python framework, so ML engineers sometimes have to switch from their IDEs.

Another consideration is that many large companies use Kubernetes by default for their infrastructure, and Slurm doesn’t play well with it. Some people have to use Kubernetes, even though they would rather prefer Slurm.

We’ve managed to mitigate most of these drawbacks in our new open-source solution: Soperator, which I covered in another article.

## What is Kubernetes?What is Kubernetes?

Kubernetes, or K8s, is a general-purpose orchestration platform for containerized applications. It’s an open-source project with numerous contributors, originally developed by Google in 2014 specifically for managing containers in their cloud.

A year later, Google offered the platform to the Linux Foundation, a move that led to the formation of the Cloud Native Computing Foundation. Within a couple of years, all major cloud providers had launched their own native Kubernetes services — the predecessors to what we now call Managed Services for Kubernetes.

After a period of competition with similar solutions on the market, Kubernetes has emerged as the clear winner. It has become the de facto standard for deploying and managing containerized microservice applications.

While every backend developer has likely heard of Kubernetes, its reputation in the HPC field is less universal. However, most ML engineers are probably familiar with it to some extent.

It’s worth noting that Kubernetes wasn’t originally designed for model training. However, its universal and extensible nature allows it to be adapted for its purpose. Some people prefer to use extensions (called Kubernetes operators) such as KubeRay for ML tasks. Vanilla setups and some self-written custom solutions are also widely used.

We’ve discussed Kubernetes a lot in previous posts, particularly in this one.

### Kubernetes designKubernetes design

On-premise Kubernetes installations are relatively rare. Only large ones sometimes tend to support them, mainly as a cost-saving measure — it’s often cheaper to rent a garage than to use a managed solution with a standard data center.

Here’s the diagram representing the architecture of a Managed Kubernetes cluster in our cloud. Other cloud providers have similar setups:

Figure 2. Architecture of a Managed Kubernetes cluster in Nebius

As you can see, the Kubernetes control plane is considerably more complex than Slurm’s, largely because it has many more responsibilities. It maintains the overall state of the cluster and checks if it matches the expected state. If there’s a discrepancy, the self-healing process is invoked. If a worker node crashes (due to hardware or software issues), K8s moves workloads to other nodes. The design philosophy behind this architecture prioritizes high availability over scheduling efficiency.

The fundamental principle of Kubernetes is that “everything is a resource.” Your entire workload should be represented as a set of resources. Each resource is defined through its manifest, typically in YAML format. Kubernetes is responsible for watching for changes in these manifests and bringing your application to the desired state.

All parts of a typical infrastructure can be represented as K8s resources: Pods are deployable units where your software runs. They can be configured using ConfigMaps and Secrets. Persistent Volumes represent storage, and network exposure is done via Services. There are many other resource types, and anyone can define their own.

To start your model training, you need to create one or more Jobs. While this isn’t the only approach, we’ll describe the simplest example. One job cannot be distributed among worker nodes, but you can launch a separate job on each node (this is an example of why some third-party extensions or custom solutions are used on top of K8s).

Here’s the manifest of a job that performs the NCCL test, similar to what we did in the Slurm example (please note that this job will run on only one node):

apiVersion: batch/v1
kind: Job
metadata:
　name: my-job
spec:
　template:
　　spec:
　　　containers:
　　　- name: nccl-test
　　　　image: nvcr.io/nvidia/nccl:2.11.4-1-cuda11.8-runtime-ubuntu20.04
　　　　command: ["/nccl-tests/build/all_reduce_perf"]
　　　　args: ["-b", "512M", "-e", "8G", "-f", "2", "-g", "8"]
　　　　resources:
　　　　　limits:
　　　　　　cpu: 8
　　　　　　memory: 32Gi
　　　　　　nvidia.com/gpu: 8
　　　restartPolicy: Never
　backoffLimit: 4

Then you need to apply this YAML manifest to the cluster: kubectl apply my_job.yaml.

You can read the output of this job using kubectl logs jobs/my-job.

### Kubernetes advantagesKubernetes advantages

The main benefit of Kubernetes is its universality. People can solve all their tasks using only it, including computationally-intensive tasks (e.g., training) and some production serving (e.g., inference). They can even host their company website in the same system. It has become a de facto standard and is often perceived as part of the underlying infrastructure.

There are many managed solutions on the market that make your life much easier. Even with on-premise installations, ML engineers rarely have to solve problems with Kubernetes themselves, as there are dedicated specialists for this. This is unlike Slurm, where maintaining nodes in an identical state is a shared responsibility.

Autoscaling is a key feature of Kubernetes. K8s is primarily designed for a public cloud environment where additional computing power is always available. If you want to launch a workload that exceeds the current capacity of the cluster, the cluster is automatically scaled up to meet the new requirements. Scaling clusters down is also beneficial for the ML field because the demand changes over time, and it’s too uneconomical to pay for hardware you don’t need at a specific moment.

Kubernetes provides some high availability out of the box. You can configure your workload to be automatically restarted (even on different hardware) if something goes wrong, with almost no effort.

Thanks to many third-party solutions such as KubeRay, training in Kubernetes can offer you user-friendly ways of doing ML, including graphical user interfaces and Python frameworks. Slurm can offer something too, but it’s much more limited.

### Kubernetes drawbacksKubernetes drawbacks

Kubernetes is very powerful and neat, and somewhere outside of ML, there may not even be a choice whether to use it or not. However, when something is good at everything, it’s often not the best at anything. And that’s where the main problem with Kubernetes stems from. While it’s applicable, it’s not targeted at model training and, therefore, lacks many of Slurm’s advanced features relevant for HPC. Kubernetes wasn’t even designed for running time-finite workloads — it was originally created for running conditionally infinite microservice applications.

In particular, Kubernetes can’t boast of advanced scheduling. The vanilla version can’t even offer a way to run a single job on many nodes. Popular extensions are also not known for highly efficient scheduling (neither in terms of the number of hosts in a job nor the number of jobs per second, although the latter is rarely relevant for training). The verbose syntax for reserving nodes is also far away from what you might be used to with Slurm.

Kubernetes also can’t offer such granular management of hardware as Slurm can. While it’s theoretically possible to do the same using, for example, Device Plugins, Slurm currently offers more in this area.

As I mentioned earlier, many of Kubernetes’ drawbacks can be mitigated through third-party extensions. In practice, companies need to install additional Kubernetes operators in their clusters. The list is usually quite long: NVIDIA GPU Operator (also available in the Nebius console), NVIDIA Network Operator, MPI Operator, Training Operator, some solutions for shared filesystems and databases, etc. This significantly complicates the bootstrapping of the system. However, once installed, everything works more or less smoothly if you don’t tinker with it.

I have another, perhaps obvious, point to make. If you use Kubernetes, your workload must be containerized and follow the cloud native approach. Not every distributed application can run in K8s, though almost any can be adapted somehow. While the Cloud Native philosophy is definitely lawful good, many of us are chaotic evil. Otherwise, why would we be bringing the uprising of machines closer?

In any case, Kubernetes developers have been doing their best lately to adapt their creation to ML scenarios and make training more convenient.

## How to make the right choiceHow to make the right choice

Here is a comparison table summarizing all the points I mentioned:

Figure 3. Pros and cons of Kubernetes and Slurm

Neither Slurm nor Kubernetes were originally designed for our modern machine-learning workloads. However, Slurm is currently more adapted to large, distributed training. Kubernetes can counter with self-healing, autoscaling and suitability for tasks other than HPC.

You can also see the two different communities migrating to the AI/ML space: the academics that have been running ML research on Slurm for a very long time, and the Big Tech companies that are much more familiar with Kubernetes and cloud-native approaches.

If you’re choosing between Slurm and Kubernetes, I hope this article helps you make a more informed and structured decision.

Here are my personal recommendations, which are very generalized but suitable for most cases:

- 

Choose Slurm if you want access to advanced features targeted at HPC (but make sure you really need them).

- 

Choose Kubernetes if you’re not sure what you need, or you’re especially interested in autoscaling and ease of maintenance.

If your team already has a background in either academics or Big Tech and you are well familiar with one of the systems, you probably don’t need to switch to the other.

## Slurm and Kubernetes in NebiusSlurm and Kubernetes in Nebius

At Nebius, we offer solutions for both Slurm and Kubernetes.

### Managed KubernetesManaged Kubernetes

Our Managed Service for Kubernetes is well-suited for model training and other GPU-computing workloads. You can read more about it on the service page, in the documentation and in the previous post.

You can deploy it in three ways: via a web console, our CLI or Terraform, for which we’ve built useful templates.

### SoperatorSoperator

We’ve created an open-source project that aims to solve the problem of combining Slurm and Kubernetes.

This solution helps deal with the complexity of Slurm’s environment management and lack of autoscaling. It also implements additional features that are not present in either vanilla Slurm or vanilla Kubernetes.

In general, it can be used in any cloud, but we provide a Terraform recipe only for our cloud. It allows you to get a fully functional Slurm cluster with a single terraform apply.

I’ve explored this solution in another article explaining the architecture and technical decisions we made.

While this article is generally applicable to any HPC workload, it’s mostly focused on model training with GPU computing.

## Explore Nebius AI

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Mikhail Mokrushin
Managed Schedulers Team Leader

## See also

### 

On Kubernetes significance for ML/AI engineers

K8s has become the tool of choice for machine learning teams large and small. What are its properties that have made it today’s industry standard?

November 14, 2023
7 mins to read

### 

Explaining Soperator, Nebius’ open-source Kubernetes operator for Slurm

We’ve built an open-source Kubernetes operator that runs and manages Slurm clusters as Kubernetes resources. From this article, you’ll find out how the community tackled this task previously and the details of the architecture of our solution, which we named Soperator.

September 24, 2024
10 mins to read

### 

Announcing Managed Service for MLflow in public preview

MLflow is a renowned industry tool that streamlines workflows in the model development cycle. We made MLflow more accessible to a broad audience of ML enthusiasts by providing it as a managed solution.

September 3, 2024
5 mins to read

Sign in to save this post
Sign In
