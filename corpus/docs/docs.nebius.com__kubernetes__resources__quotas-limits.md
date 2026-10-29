# Managed Service for Kubernetes® quotas and constraints

Source: https://docs.nebius.com/kubernetes/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managed Service for Kubernetes® quotas and constraints

## Quotas

Managed Service for Kubernetes has quotas on the number of clusters and uses the same quotas on nodes and IP addresses as Compute.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

### Clusters

| Quota name | Default value, `eu-north1`, `eu-west1`, `eu-west2`, `eu-south1`, `uk-south1`, `uk-south2`, `us-central1`, `us-north1` | Default value, `me-west1`, `eu-north2` |
| :- | :- | :- |
| Clusters per [region](https://docs.nebius.com/overview/regions.md) | 2 | 0 |

### Nodes

Managed Service for Kubernetes nodes comply with the same quotas as Compute virtual machines. You can find them in [Quotas in Compute](https://docs.nebius.com/compute/resources/quotas-limits.md).

### Network

See [Quotas in Virtual Networks](https://docs.nebius.com/vpc/resources/quotas-limits.md).

## Constraints

Certain Managed Kubernetes resources have technical constraints that may depend on your quotas, but can't be changed directly.

### Kubernetes feature gates

[Alpha Kubernetes feature gates](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-stages) can't be enabled in Managed Kubernetes clusters. A feature introduced behind an Alpha feature gate is available only in a [supported Kubernetes version](https://docs.nebius.com/kubernetes/versions.md) where the feature is enabled by default. If necessary, [upgrade your cluster](https://docs.nebius.com/kubernetes/manage-versions.md) to such a version.

### Nodes

The number of nodes you can create in a Managed Kubernetes cluster depends on the type of used IP address and whether high availability control plane is enabled. This number is limited by your **Allocations** [quota](https://docs.nebius.com/vpc/resources/quotas-limits.md).

> For example, with the default **Allocations** quota of 1000, you can create up to 498 nodes across all clusters when using only private IP addresses with no high availability, or up to 331 nodes when using both private and public IP addresses with high availability enabled.

For more information, see [Network requirements for Managed Service for Kubernetes® clusters](https://docs.nebius.com/kubernetes/networking/requirements.md).
