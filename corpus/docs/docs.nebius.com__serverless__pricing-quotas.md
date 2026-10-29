# Pricing and quotas in Serverless AI

Source: https://docs.nebius.com/serverless/pricing-quotas

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing and quotas in Serverless AI

Serverless AI does not have its own quotas and pricing; the service applies the quotas and pricing of Compute.

## Pricing

Billing of Devlabs, endpoints and jobs depends on whether the deployment is running or stopped:

* While a Devlab, job or endpoint is running, you are billed for its computing resources and storage under Compute VM and disk pricing.
* While a Devlab is stopped, you are billed for the entire container disk but not for computing resources.
* While an endpoint is stopped, you are not billed for computing resources or storage.

  Jobs cannot be stopped.

If you mount an [Object Storage bucket](https://docs.nebius.com/object-storage/overview.md#buckets) or a [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to a Serverless AI resource, separate billing for the bucket and filesystem applies, including when this resource is stopped.

## Quotas

When you create Devlabs, endpoints or jobs, they count toward Compute quotas. If the quotas are exceeded, resource provisioning fails with the `QuotaExceeded` error.

Before you create a Serverless AI deployment, check the quotas required for Serverless AI and [increase them](https://docs.nebius.com/overview/quotas.md#change-quotas), if required.

Devlabs, endpoints or jobs are based on the same resources, so you need the same quotas for them. When you calculate what values for the quotas you need, consider that each Serverless AI deployment includes the following resources:

* Virtual machine (VM), a regular or [preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md) one.
* GPUs if you use a GPU [platform](https://docs.nebius.com/compute/virtual-machines/types.md). The platform availability depends on the [region](https://docs.nebius.com/overview/regions.md).
* vCPUs. You need a dedicated quota for vCPUs only if you run a VM without any GPUs.
* [Network SSD disk](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
* Public IPv4 address if the deployment configuration includes it.
* [Allocations](https://docs.nebius.com/vpc/overview.md#allocation) that represent public and private IP addresses.
* (Optional) Shared filesystem or bucket if you mount an additional volume to the deployment.

To run multiple Serverless AI deployments, multiply each resource by the number of these deployments.

### Quotas to check

Required quotas:

| Quota | Description | Minimum required size |
| - | - | - |
| Regular VMs | If you use regular VMs. | Number of running deployments. |
| Preemptible VMs | If you use preemptible VMs. | Number of running deployments. |
| GPUs | If you use regular VMs with a GPU platform. The quota depends on what platform and preset you select. Each platform has its own quota. The preset defines the number of GPUs. | \[GPUs in the preset] × \[number of running deployments]. |
| vCPUs | If you use non-GPU VMs. Depend on what preset you select. | \[vCPUs in the preset] × \[number of running deployments]. |
| Disks | Each VM includes only one disk. | Number of running deployments. |
| Disk capacity (Network SSD) | Capacity for all running disks. | Total disk size across all running deployments. |
| Public IPv4 addresses | If the deployment configuration includes a public address. | Number of running deployments. |
| Allocations | Each IP address represents an allocation, so check the number of allocations no matter whether you use a public or private endpoint. | \[Number of running deployments] + \[number of public addresses of these deployments]. |

Optional quotas that apply when you mount a volume:

| Quota | Description | Minimum required size |
| - | - | - |
| Buckets | If you create a bucket. | Number you need. You can reuse the same bucket for several deployments. |
| Shared filesystems | If you create a shared filesystem. | Number you need. You can reuse the same filesystem for several deployments. |

You also need quotas for size of objects in buckets or for shared filesystem capacity. However, they depend on the size of the files that you're going to store.

### Example

You create an endpoint:

```bash theme={null}
nebius ai endpoint create \
   --name my-endpoint-45jcjmdh \
   --platform gpu-l40s-a \
   --preset 1gpu-8vcpu-32gb \
   --disk-size 100Gi \
   --public \
   --volume "<bucket_ID>:/output:rw" \
   ...
```

In this case, you need at least 1 VM, 1 GPU for the `gpu-l40s-a` platform, 1 disk, 100 GiB for the Network SSD disk capacity, 1 public address, 2 allocations and 1 bucket.

You don't need dedicated quotas for RAM and vCPUs because Compute automatically provides them together with GPU quotas.

If you add the `--preemptible` parameter to the command, you'd create an endpoint that runs on a preemptible VM. In this case, you need different quotas: 1 preemptible VM, 1 disk, 100 GiB for the Network SSD disk capacity, 1 public address, 2 allocations and 1 bucket.

## See also

For more information about the quotas and pricing, see:

* [Quotas for VMs and filesystems](https://docs.nebius.com/compute/resources/quotas-limits.md)
* [Quotas for public addresses](https://docs.nebius.com/vpc/resources/quotas-limits.md)
* [Pricing for VMs and shared filesystems](https://docs.nebius.com/compute/resources/pricing.md)
* [Pricing for buckets](https://docs.nebius.com/object-storage/resources/pricing.md)
