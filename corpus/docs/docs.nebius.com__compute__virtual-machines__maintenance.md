# Maintenance of Compute virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/maintenance

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Maintenance of Compute virtual machines

The Compute service performs maintenance for all virtual machines, including nodes of [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/index.md) clusters and [Soperator](https://docs.nebius.com/slurm-soperator/overview/why-slurm-soperator.md) clusters. To ensure that maintenance is performed successfully, [stop and start VMs](https://docs.nebius.com/compute/virtual-machines/stop-start.md) until the specified date. You can open the list of VMs via the red banner on the top of the screen. For example:

![maintenance-banner](https://mintcdn.com/nebius-ai-cloud/3vrg63wLg56IgavR/_assets/compute/maintenance-banner-for-all-vms.png?fit=max\&auto=format\&n=3vrg63wLg56IgavR\&q=85\&s=42a1d39ac2ff2bf9ddb13045e09e748a)

> [!WARNING]
>
> If you do not stop VMs on time, the service will automatically stop them after the due date to perform maintenance. Delayed maintenance may cause VM instability.

If you need to keep your VMs running, [contact the support team](https://console.nebius.com/support/create-ticket) to request rescheduling maintenance of the affected VMs. You can request to reschedule it up to two times, and you can postpone the maintenance by up to seven days each time.
