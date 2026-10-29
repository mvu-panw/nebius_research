# Kubernetes® version deprecation policy in Managed Service for Kubernetes

Source: https://docs.nebius.com/kubernetes/version-deprecation

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Kubernetes® version deprecation policy in Managed Service for Kubernetes

This article describes how Managed Service for Kubernetes handles Kubernetes version deprecation.

## How many versions are available

Managed Service for Kubernetes supports a limited set of Kubernetes minor versions. At any time, no more than four Kubernetes minor versions are available:

* No more than three supported versions: fully supported for new and existing clusters.
* One deprecated version: supported for existing clusters, receives updates from Managed Service for Kubernetes, but **isn't available** for creating new clusters.

See the current list in [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

## When a version becomes deprecated

A version becomes **deprecated** when a newer minor version is introduced and the oldest supported version moves out of the supported set. A deprecated version stays available for existing clusters for **two months**, after which it becomes unavailable. Creating new clusters with that version isn't possible.

The end-of-life date for each version is shown in [nebius mk8s cluster list-control-plane-versions](https://docs.nebius.com/cli/reference/mk8s/cluster/list-control-plane-versions.md).

If your cluster uses a deprecated version, you'll see a notification in the [web console](https://console.nebius.com/mk8s), when using Terraform, or when reading cluster info via [nebius mk8s cluster get](https://docs.nebius.com/cli/reference/mk8s/cluster/get.md).

When a version reaches its end-of-life date, clusters using it are upgraded automatically within a short period.

## How clusters are upgraded by the service

Managed Service for Kubernetes keeps clusters within the supported version window to maintain security and reliability.

* **Control plane**: upgraded automatically when your cluster with a deprecated version reaches end of life.
* **Node groups**: upgraded automatically only when required to keep the control plane within the [Kubernetes version skew policy](https://kubernetes.io/releases/version-skew-policy/#kubelet) (no more than three minor versions behind the control plane). Node groups are upgraded to match the control plane version, so they can jump several versions at once.

> For example, if your cluster's control plane is running 1.35 and its worker nodes are running 1.33, when 1.35 is deprecated, both the control plane and the worker nodes are upgraded to 1.36.

## How to upgrade your cluster yourself

You can upgrade your cluster on your own schedule. This gives you control over timing and allows you to prepare workloads in advance.

See the step-by-step guide in [Setting and upgrading Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/manage-versions.md).

## Risks of not upgrading a cluster yourself

If you don't upgrade a cluster in time, Managed Service for Kubernetes will upgrade your cluster automatically. This can introduce the following risks:

* The cluster specification and status don’t match. Managed Service for Kubernetes doesn’t modify the cluster specification; however, the cluster continues to be updated, as reflected in its status.
* Unexpected maintenance timing for control plane or node group upgrades.
* Workload disruption from node replacements during node group upgrades.
* Compatibility issues due to Kubernetes API removals.
* Larger version jumps, which are harder to validate than planned, gradual upgrades.

To reduce risk, plan upgrades ahead of deprecation dates and keep clusters on supported versions.
