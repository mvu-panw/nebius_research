# Pricing in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/resources/pricing

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing in Managed Service for Kubernetes®

This article provides detailed pricing for the Managed Service for Kubernetes in Nebius AI Cloud.

## How charges and prices work

Each group of chargeable items in this article has two time units associated with it:

* **Billing unit**: The minimum unit of usage for which you can be charged.
* **Pricing unit**: The unit of usage for which the prices are shown.

Charges for units smaller than the pricing unit are calculated proportionally.

> For example, for GPUs on running VMs, the **billing unit** is 1 second, and the **pricing unit** is 1 hour (3600 seconds). For 30 minutes of usage, you will be charged half the hourly price.

Prices in US dollars (USD, \$) apply to all customers except for companies from Israel, where prices in Israeli shekels (ILS, ₪) apply instead.

All prices are shown without any applicable taxes, including VAT. Due to rounding errors, usage costs shown in the web console and final charges may slightly differ from calculations based on the prices in this article.

## Prices

### Nodes

You are charged for running nodes in your Managed Kubernetes clusters.

As Managed Kubernetes nodes are Compute virtual machines, their computing resources (GPUs, vCPUs, RAM) and storage are charged according to Compute pricing. For more details, see [Compute pricing in Nebius AI Cloud](https://docs.nebius.com/compute/resources/pricing.md).
