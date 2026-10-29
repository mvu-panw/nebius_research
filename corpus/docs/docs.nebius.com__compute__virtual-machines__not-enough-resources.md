# "Not enough resources" error for virtual machines in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/not-enough-resources

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# "Not enough resources" error for virtual machines in Nebius AI Cloud

Sometimes, demand for virtual machines and GPUs in certain [Nebius AI Cloud regions](https://docs.nebius.com/overview/regions.md) might be higher than the available supply. When this happens, you might see a "Not enough resources" error when creating or restarting VMs in the affected region.

## Error creating a VM

If you receive a "Not enough resources" error when [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) in an affected region, consider creating the VM with similar resources or in a different region.

> For example, instead of creating the VM on the NVIDIA® H200 NVLink with Intel Sapphire Rapids platform in the `eu-west1` region, you can try NVIDIA® H100 NVLink with Intel Sapphire Rapids in `eu-north1`.

For VMs with GPUs, you can use the [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md) to get information about the availability of computing resources based on your quotas, the current physical capacity and, for preemptible VMs, the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md).

> [!WARNING]
>
> Availability of platforms and presets differs by region and project. To change the platform or preset of a VM, you might need to change its project as well. For more information about availability, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md) and [How to find out platforms and presets available in a project](https://docs.nebius.com/compute/virtual-machines/list-platforms.md).

If your workload does not work with another VM platform or preset, you can request to reserve the required capacity. For more details, [contact the Nebius sales team](https://nebius.com/#ai-contact-form).

## Error restarting a stopped VM

If you get a "Not enough resources" error when restarting a stopped VM in an affected region, check the [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md) for detailed information on available computing resources.
