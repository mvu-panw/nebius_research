# Combining Slurm and Kubernetes by using Soperator

Source: https://docs.nebius.com/slurm-soperator/overview/why-slurm-soperator

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Combining Slurm and Kubernetes by using Soperator

[Slurm](https://slurm.schedmd.com) is widely used for managing machine learning (ML) workloads. It is dedicated to efficient resource management, allowing you to split large jobs into many steps, then run them in parallel for distributed ML training. But Slurm is not cloud-native. [Kubernetes®](https://kubernetes.io/) complements Slurm, as it provides auto-scaling and self-healing capabilities. However, Kubernetes is not tailored to model training needs. Features that Slurm and Kubernetes provide could be combined for an optimal solution.

[Soperator](https://github.com/nebius/soperator) is an open-source Kubernetes operator that solves this problem. It runs Slurm nodes as Kubernetes Pods. A Soperator cluster is based on a Kubernetes cluster and uses Slurm as an additional infrastructure layer. Nebius AI Cloud offers [options to deploy Soperator clusters](https://docs.nebius.com/slurm-soperator/deploy/overview.md) that provide high availability and automatic scaling, to save computing resources and costs.

## Features of a Soperator cluster

### Easy scaling

Thanks to the Kubernetes infrastructure layer, a Soperator cluster scales automatically to your current workload. This allows you to have sufficient resources during the compute-heavy stages of building your project and scale down when you do not need to use — and pay for — as much computing power.

### High availability

The underlying Kubernetes cluster already has self-healing capabilities, such as automatic Pod restart. In addition, Soperator continuously monitors the state of the cluster and compares it to the configuration declared in the YAML manifests of Kubernetes resources. If there are any discrepancies, Soperator restores the configuration.

### Unified storage

All login and worker nodes share the same root filesystem. This lets you work with a Soperator cluster in the same way as with other Slurm installations, such as an on-premises cluster. For example, you can run jobs with `sbatch` without any need to run each job in a container.

With the shared filesystem, you do not need to keep nodes synchronized, because they have an identical state by default. The changes that you make on one node are spread across all other nodes. For example, these changes can include the installation of packages, the download of datasets or adding Linux users.

### Secure environment

User actions are isolated in a dedicated container-like environment. This ensures that users cannot accidentally interfere with the cluster configuration.

### Out-of-the-box solution

Soperator clusters are provisioned with all necessary software pre-installed and ready to use. The software versions have been thoroughly tested and work together, to ensure optimal performance. However, if you have specific requirements, you can change software versions. The configuration of the Slurm cluster is also fine-tuned and does not require additional setup on your side.

In Nebius AI Cloud, you can deploy a managed Soperator cluster in just a few clicks, or apply for a professional solution from Nebius for larger or enterprise-scale GPU workloads. For more details, see [Deploying Soperator clusters](https://docs.nebius.com/slurm-soperator/deploy/overview.md).

### Automated health checks

Soperator regularly runs the following health checks:

1. Quick checks that use Slurm's [HealthCheckProgram](https://slurm.schedmd.com/slurm.conf.html#OPT_HealthCheckProgram). They check that there are no critical software or hardware issues.
2. Longer checks that run [NVIDIA® Collective Communications Library (NCCL) tests](https://github.com/NVIDIA/nccl-tests) as regular Slurm jobs. They check GPU performance and drain nodes that do not meet the test benchmark.
3. Slurm [Prolog and Epilog](https://slurm.schedmd.com/prolog_epilog.html) scripts. They perform GPU health checks before and after each Slurm job runs.
4. Compute maintenance events. They monitor all GPU and InfiniBand™ devices for errors. Soperator uses maintenance events for Slurm and automatically replaces all faulty nodes.

### Monitoring

You can monitor the performance and status of various parts of the system:

* Underlying Kubernetes cluster metrics, including node metrics, Pod resource metrics and all event logs.
* Slurm metrics, including job queue size, job statuses, node states and resource consumption.
* GPU (NVIDIA DCGM) metrics.

## See also

* [Soperator cluster architecture](https://docs.nebius.com/slurm-soperator/overview/architecture.md).
* [Explaining Soperator, Nebius' open-source Kubernetes operator for Slurm](https://nebius.com/blog/posts/soperator-in-open-source-explained) in the Nebius blog.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
