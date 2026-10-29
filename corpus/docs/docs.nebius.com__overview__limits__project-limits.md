# Project limits for capacity block groups

Source: https://docs.nebius.com/overview/limits/project-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Project limits for capacity block groups

*Project limits* let you cap how many GPUs from a [capacity block group (CBG)](https://docs.nebius.com/overview/limits/capacity-block-groups.md) each project can consume. By default, all projects in your tenant can use GPUs from a CBG without restriction, up to the total CBG size. Project limits help prevent any single project from consuming the entire CBG capacity.

## How project limits work

GPU consumption in a project is capped as follows:

* If the project limit is set to `0`, CBG usage is disabled for the project.
* If the project limit is less than or equal to the CBG size, the effective limit equals the project limit.
* If the project limit exceeds the CBG size, the effective limit equals the current CBG size. The configured limit becomes effective when the capacity block group size increases to that value or higher.
* If no project limit is set, the effective limit equals the current CBG size.

## How limits affect running workloads

Reducing a project limit below current usage, or reducing the CBG size below current project usage, does not stop running workloads. However:

* Running workloads might not be able to restart once stopped.
* New CBG allocations are blocked until usage drops below the effective limit.

## See also

* [Capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md)
* [Managing project limits](https://docs.nebius.com/overview/limits/manage-project-limits.md)
* [Quotas](https://docs.nebius.com/overview/quotas.md)
* [Pay-as-you-go (PAYG)](https://docs.nebius.com/signup-billing/billing-models/payg.md)
