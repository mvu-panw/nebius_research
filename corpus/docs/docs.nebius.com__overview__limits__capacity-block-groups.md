# Capacity block groups in Nebius AI Cloud

Source: https://docs.nebius.com/overview/limits/capacity-block-groups

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Capacity block groups in Nebius AI Cloud

To reserve GPUs for virtual machines (VMs), you can use *capacity block groups*. They reserve a certain number of GPUs in a given region for a [GPU platform](https://docs.nebius.com/compute/virtual-machines/types.md) that you choose. The GPUs are assigned to an [InfiniBand™ fabric](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics).

To reserve GPUs by using capacity block groups, send a request to your Nebius manager. They create capacity block groups for you and prepare an addendum for [commitment discounts](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md) billing. If you are not in contact with a Nebius manager, you can ask [technical support](https://console.nebius.com/support/create-ticket) to connect you with one.

Once capacity block groups are prepared, you can add them to [your VMs](https://docs.nebius.com/compute/virtual-machines/reservations.md#how-to-add-reservations-to-vms) or [your node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md#how-to-add-reservations-to-node-groups) in Managed Service for Kubernetes®. After that, you can examine information about the capacity block groups on the **Limits** page in the [web console](https://console.nebius.com).

> [!NOTE]
>
> GPUs allocated from capacity block groups do not count towards [quotas on the number of GPUs](https://docs.nebius.com/compute/resources/quotas-limits.md#gpu-virtual-machines).

## Intervals in capacity block groups

Every capacity block group consists of *intervals*. Each interval represents a period for which a specific number of GPUs is reserved. Different intervals within the same capacity block group can overlap, follow consecutively or have gaps between them. For example, there can be the following intervals:

1. 60 GPUs reserved from January 1 until January 31.
2. 72 GPUs reserved from January 26 until February 15.
3. 150 GPUs reserved from February 20 until March 31.

> [!NOTE]
>
> Intervals start at 00:00 UTC and end at 23:59 UTC on the dates defined in the interval.

Intervals within a single capacity block group can only be based on the same GPU platform and the same InfiniBand fabric.

## List of capacity block groups

If you go to the **Limits** page and open the **Capacity block groups** tab, you see a list of your capacity block groups. It shows the following:

* Region that the capacity block group belongs to.

* InfiniBand fabric of reserved GPUs.

* GPU platform.

* Status:

  * **Active**: The capacity block group is available for usage; it does not expire soon.
  * **Ending in N days**: The capacity block group contains one active interval remaining, which soon expires. Consider using an active capacity block group instead.
  * **Inactive**: The capacity block group does not have any active intervals.

* Next interval. You can find out when the next interval starts and to what number of GPUs the capacity block group switches. If the last interval is currently running, the page shows **No renewal** instead of the next interval.

* Number of GPUs consumed out of the total number of reserved GPUs. The total number is calculated based on the active intervals within the capacity block group.

## Dashboard of a capacity block group

To open the dashboard that contains detailed information about a given capacity block group:

1. In the [web console](https://console.nebius.com), go to  **Administration** → **Limits**.
2. Open the **Capacity block groups** tab.
3. Click the capacity block group.

On the **Intervals** tab of the dashboard, you can get the following information about intervals that the capacity block group includes:

* ID of an interval.

* Status of an interval:

  * **Active**: Interval is available for usage.
  * **Pending**: Interval will start in the future.
  * **Expired**: Interval has expired. Instead of it, a new active interval should apply.

* Period when an interval is active.

* Number of GPUs that an interval reserves.

This information is displayed as a graph and as a table. You can select the period for which the information should be displayed.

On the **Usage** tab of the dashboard, you can determine what VMs consume the current capacity block group. These VMs are grouped in projects. If you click on the project line, the dashboard displays what VMs consume capacity and how many GPUs they consume. As a result, the dashboard provides a detailed breakdown by VMs and projects.

Some consumption can be marked as **Forbidden** on the **Usage** tab. These are projects that you don't have access to.

## See also

* [Capacity reservations for Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/reservations.md)
* [Capacity reservations for Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md)

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
