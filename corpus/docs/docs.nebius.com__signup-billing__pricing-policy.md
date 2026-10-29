# Spot pricing and pricing policies in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/pricing-policy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Spot pricing and pricing policies in Nebius AI Cloud

*Spot pricing* is dynamic pricing for preemptible virtual machines (VMs) and Nebius AI Cloud services that run on preemptible VMs. Instead of using a fixed preemptible discount, Nebius sets a current spot price for each preemptible GPU platform.

To control your maximum hourly price, you can create a *pricing policy*. A pricing policy defines the highest spot price at which preemptible resources can run for one GPU hour on a specific platform. If you don't want to set a maximum price, you can choose to [follow the current spot price](#following-the-spot-price) when creating a preemptible resource.

For detailed instructions, see [Managing pricing policies](https://docs.nebius.com/signup-billing/manage-pricing-policy.md).

## How spot pricing works

Each preemptible GPU platform has a spot price and a price range.

* **Spot price**: The current price for one GPU hour. This price may change as often as every 15 minutes based on factors such as capacity availability, cluster utilization and demand.
* **Price range**: The minimum and maximum values within which the spot price can change. The upper value is lower than the [regular pay-as-you-go (PAYG) price](https://docs.nebius.com/compute/resources/pricing.md) for the same platform.
* **Max price**: The value that you set in a pricing policy. It's the highest spot price at which your resources that use the policy can run.

Spot prices can change before and during resource usage. The current spot price becomes the applicable price when the resource starts using preemptible VM capacity. During use, the applicable price can change at the next 15-minute update.

To track spot prices and their history, see [Getting spot prices](https://docs.nebius.com/signup-billing/spot-prices.md). You don't need a Nebius AI Cloud account to view them.

Before incurring charges, you can check the current spot price and price range on the **Billing** → **Pricing** → **Pricing history** page in the [web console](https://console.nebius.com). When you create a new preemptible resource, the web console shows the current spot price for the selected resource based on its GPU count and an estimated hourly cost. The estimate assumes the spot price doesn't change during that hour, so the actual charge can differ if the spot price changes.

When you create or start a preemptible VM, you accept the current spot price if it is lower than or equal to the max price in your policy, or if you choose to follow the spot price. If you use a pricing policy, you pay the spot price, not the max price. If the spot price exceeds the max price, preemptible resources that use the policy are stopped.

> [!WARNING]
>
> Spot pricing doesn't guarantee resource availability. Preemptible resources may be stopped if capacity is needed elsewhere or if the current spot price exceeds the max price set in the selected pricing policy.

For more information about preemptible VM behavior, see [Preemptible virtual machines](https://docs.nebius.com/compute/virtual-machines/preemptible.md).

## Following the spot price

Selecting the **Follow spot price** option when creating a preemptible resource allows it to run at the current spot price without a pricing policy. Use this option if you accept spot price changes and don't need to set the maximum price.

When you follow the spot price, the resource is charged at the current spot price for each pricing interval. The price can change every 15 minutes, including while the resource is running. Because no max price is set, the resource is not stopped when the spot price increases, but it can still be stopped if capacity is needed elsewhere.

## Pricing policies

A pricing policy belongs to a project and applies to one GPU platform.

If the max price is lower than the current spot price, the policy is shown as **Blocked** in the web console. Resources that use a blocked policy can't start until the spot price decreases and you restart them, or until you increase the max price set in the policy.

The max price is set in your billing currency, per GPU hour.

> For example, if a preemptible VM has 8 GPUs and runs for 30 minutes, but the spot price changes after 15 minutes, the computing cost is calculated for each pricing interval:
>
> * First 15 minutes at \$2.00 per GPU hour: 8 GPUs × 0.25 hours × \$2.00 = \$4.00
> * Next 15 minutes at \$2.50 per GPU hour: 8 GPUs × 0.25 hours × \$2.50 = \$5.00
>
> Total: \$4.00 + \$5.00 = \$9.00

## Services that use spot pricing

Spot pricing applies to preemptible VMs with GPUs. Depending on the service and resource type, this can include:

* [Compute preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md).
* [Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md) that use preemptible VMs.
* [Serverless AI jobs](https://docs.nebius.com/serverless/jobs/manage.md) and [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md) that run on preemptible VMs.
* Other Nebius AI Cloud services where you select preemptible GPU capacity.

If a service doesn't let you select preemptible GPU capacity, spot pricing isn't available for that resource.

## Usage and invoices

Spot prices can change during a billing period. Your invoice shows the total consumption for the billing period and doesn't list every spot price change separately.

To check detailed usage for each price interval, export usage data in the [FinOps Open Cost and Usage Specification (FOCUS) 1.2](https://focus.finops.org/focus-specification/v1-2/) format. The export contains the effective hourly price for VM usage and the time period for each charge. For more information, see [Exporting usage data as CSV](https://docs.nebius.com/signup-billing/usage/export.md).

## See also

* [Managing pricing policies](https://docs.nebius.com/signup-billing/manage-pricing-policy.md)
* [Getting spot prices](https://docs.nebius.com/signup-billing/spot-prices.md)
* [Preemptible virtual machines](https://docs.nebius.com/compute/virtual-machines/preemptible.md)
* [Capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md)
* [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md)
* [Pay-as-you-go in Nebius AI Cloud](https://docs.nebius.com/signup-billing/billing-models/payg.md)
* [Exporting usage data as CSV](https://docs.nebius.com/signup-billing/usage/export.md)
