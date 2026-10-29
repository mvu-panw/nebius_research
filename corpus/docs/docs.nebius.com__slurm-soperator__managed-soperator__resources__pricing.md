# Pricing in Managed Service for Soperator

Source: https://docs.nebius.com/slurm-soperator/managed-soperator/resources/pricing

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing in Managed Service for Soperator

This article provides pricing details for Managed Service for Soperator in Nebius AI Cloud.

## How charges and prices work

Each group of chargeable items in this article has two time units associated with it:

* **Billing unit**: The minimum unit of usage for which you can be charged.
* **Pricing unit**: The unit of usage for which the prices are shown.

Charges for units smaller than the pricing unit are calculated proportionally.

> For example, for GPUs on running VMs, the **billing unit** is 1 second, and the **pricing unit** is 1 hour (3600 seconds). For 30 minutes of usage, you will be charged half the hourly price.

Prices in US dollars (USD, \$) apply to all customers except for companies from Israel, where prices in Israeli shekels (ILS, ₪) apply instead.

All prices are shown without any applicable taxes, including VAT. Due to rounding errors, usage costs shown in the web console and final charges may slightly differ from calculations based on the prices in this article.

## Prices

### Cluster resources

You are charged for the following resources:

* Login, worker and [service nodes](https://docs.nebius.com/slurm-soperator/managed-soperator/service-nodes.md) are Compute virtual machines. Their GPUs, vCPUs, RAM and boot disks are charged according to [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md).
* Shared filesystems provisioned for the cluster are also priced in Compute. See [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md#shared-filesystems) for storage rates.
* Any buckets used with the cluster are charged according to [Object Storage pricing](https://docs.nebius.com/object-storage/resources/pricing.md).
