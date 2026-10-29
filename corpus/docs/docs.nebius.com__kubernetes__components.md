# Components in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/components

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Components in Managed Service for Kubernetes®

This article provides a quick overview of the Managed Service for Kubernetes components, their interactions and functions.

A Managed Service for Kubernetes cluster consists of:

* [Control plane](#control-plane-components)
* [Node components](#node-based-control-plane-components)
* Sets of worker VMs ([nodes](#node) and [node groups](#node-group)) that run groups of containerized applications ([Pods](#pod))

## Control plane components

**Control plane** components manage the overall state of the cluster.

### API server

The **API server** exposes the Kubernetes API to customers, acting as a frontend for [REST](https://www.geeksforgeeks.org/rest-api-introduction/) operations.

To learn more, see the official Kubernetes documentation for [kube-apiserver](https://kubernetes.io/docs/concepts/overview/kubernetes-api/).

### Scheduler

**Scheduler** is responsible for determining which [node](#node) runs a particular [Pod](#pod) with specified containers.

When selecting a node to allocate a Pod, the scheduler takes into account quotas, resource requirements, deployments, taints and tolerations and other factors.

To learn more, see the official Kubernetes documentation for [Kubernetes scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/).

### Cluster autoscaler

In Managed Service for Kubernetes, the **cluster autoscaler** seamlessly adds nodes when there are unschedulable Pods, and removes underutilized nodes as needed.

For more information, see [Autoscaling in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md).

### Controller manager

**Controller manager** runs controllers to implement Kubernetes API behavior.

To reduce complexity, multiple controllers are compiled into one binary and run as a single process. Below are examples of frequently used controllers:

* **Node controller** ensures that each node is operational. If a node shuts down, node controller tries to restart it or relocate its Pods and containers to other nodes.
* **Replication controller** ensures that the same Pods are deployed across multiple nodes if required.
* **Endpoint controller** ensures that containers are accessible to users.

To learn more, see the official Kubernetes documentation for [kube-controller-manager](https://kubernetes.io/docs/concepts/architecture/controller/).

### etcd

**etcd** is a consistent and highly available key-value store for API server data. By default, a Managed Kubernetes cluster is [created](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) with three etcd stores. This ensures high availability: The cluster is more reliable; data stored in etcd is more likely to be accessed in case of failures.

The enabled high availability does not affect the cost of the cluster.

You can find in-depth information on etcd in its [official documentation](https://etcd.io/docs/).

## Node-based control plane components

These components are located not in the control plane itself, but on each [node](#node) running on the cluster.

### kubelet

**kubelet** ensures that [Pods](#pod) and their containers are running. It communicates with the [scheduler](#scheduler) and [controller manager](#controller-manager).

To learn more, see the official Kubernetes documentation for [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/).

### kube-proxy

**kube network proxy** manages traffic flow, ensuring that network rules work on [nodes](#node).

To learn more, see the official Kubernetes documentation for [kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/).

### Cilium

**Cilium** ensures that only specific services and traffic can access certain [Pods](#pod). For example:

* Some [Pods](#pod) might contain sensitive data, and Cilium enforces rules that only certain internal services or authorized users are allowed to access it.
* If a [node](#node) requires restricted access, Cilium ensures that only internal services with proper credentials or traffic with specific labels are allowed.

Also, Cilium provides observability into traffic between [Pods](#pod) and [nodes](#node) to optimize network paths and enforce network security policies.

You can find in-depth information on Cilium in its [official documentation](https://docs.cilium.io/en/stable/index.html).

## Worker components

This section describes the components that run and manage user workloads on your Managed Service for Kubernetes cluster.

### Node

In Managed Service for Kubernetes, **nodes** are [Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/types.md).

There must be at least one node in a cluster for applications to function properly.

On [supported platforms, presets and regions](https://docs.nebius.com/compute/storage/local-disks.md#availability), you can enable [local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) for worker nodes. Local SSD disks provide ephemeral storage intended for temporary data. By default, Managed Service for Kubernetes uses them as the node's [local ephemeral storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/).

> [!WARNING]
>
> Do **not** modify Managed Service for Kubernetes nodes in Compute. Kubernetes nodes are listed on the **Kubernetes nodes** tab of the **Virtual machines** page, but manage them in the **Managed Service for Kubernetes®** section instead.

To learn more, see the official Kubernetes documentation for [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/).

### Node group

**Node groups** in Managed Service for Kubernetes organize [nodes](#node) that serve a specific purpose. All nodes in a group share the same template. The number of nodes per node group cannot exceed 100.

See more details in [Creating and modifying Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md).

Node groups can use the cluster autoscaler to seamlessly add or remove nodes as needed. For more information, see [Autoscaling in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md).

### Pod

**Pod** is a group of one or more containers with shared storage and network resources.

In a Managed Service for Kubernetes cluster, each Pod has a unique IP address so that workloads don't conflict.

To learn more, see the official Kubernetes documentation for [Pods](https://kubernetes.io/docs/concepts/workloads/pods/).

### Taints and tolerations

**Taints** act like restrictions or rules for specific [nodes](#node).

**Tolerations** are like clearances or permissions that certain [Pods](#pod) have to be placed on specified [nodes](#node).

To learn more, see the official Kubernetes documentation for [taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).

### DaemonSets

**DaemonSets** ensure that every node creates a Pod with a certain type of container.

In Kubernetes, DaemonSets are used for infrastructure-related workloads, such as logging, monitoring or networking agents that must be deployed on every node.

To learn more, see the official Kubernetes documentation for [DaemonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/).
