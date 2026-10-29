# Lifecycle of a Compute virtual machine

Source: https://docs.nebius.com/compute/virtual-machines/lifecycle

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Lifecycle of a Compute virtual machine

Every virtual machine (VM) in Compute can have one of the following statuses:

* `Stopped`: VM is stopped.
* `Starting`: VM is launching.
* `Running`: VM is running.
* `Stopping`: VM is stopping.
* `Deleting`: VM is being deleted.
* `Error`: VM crashed and cannot be restored.

  When a VM assumes this status, delete this VM and create a new one. You cannot stop and start a VM with the `Error` status.

## Transitions between VM statuses

### VM is being created

`Stopped` → `Starting` → `Running`

If you [create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) by using the CLI or Terraform, you can specify `"stopped": true` in the VM configuration. In this case, the VM is created with the `Stopped` status. The status does not change until you [launch this VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md).

### VM is being started

`Stopped` → `Starting` → `Running`

When a VM is `Starting`, its hypervisor launches the VM's operating system. Additionally, the service allocates computing resources to the VM, such as RAM, GPUs and CPUs.

When a VM is `Running`, it functions fully. This influences [billing](#when-compute-charges-for-the-vm-usage) and [quotas](#when-compute-quotas-are-released). The service charges you for a running VM. Also, the number of resources occupied in the tenant or project increases.

### VM is being stopped

`Running` → `Stopping` → `Stopped`

When a VM is `Stopping`, its hypervisor shuts down the operating system of this VM. Before the OS is turned off completely, the hypervisor gracefully terminates all running processes within 60 seconds to prevent data loss. After that, the VM is `Stopped`.

### VM is being deleted

`Running` → `Deleting`

After the `Deleting` status, a VM is removed from the list of VMs and the occupied quotas are released.

### VM crashed and is being recovered

If the VM recovery is successful, statuses of this VM change in the following order:

`Running` → `Stopping` → `Stopped` → `Running`

If Compute cannot start the VM properly during the recovery, for example, because of a lack of available resources, the VM goes through one of the following lifecycles:

* `Running` → `Stopping` → `Stopped` → `Starting` → `Stopping` → `Stopped` or `Error`
* `Running` → `Stopping` → `Stopped` or `Error`

## When Compute charges for the VM usage

When you create a VM, Compute starts [charging](https://docs.nebius.com/compute/resources/pricing.md) for it once the VM assumes the `Running` status.

When you delete a VM, Compute stops charging for it once you send the deletion command. For example, you click the  **Delete** button or run a [CLI command](https://docs.nebius.com/cli/reference/compute/instance/delete.md).

When a VM has crashed, Compute stops charging for it when recovery begins. If the VM is recovered successfully, the service continues charging. If not, the charging does not start again.

## When Compute quotas are released

[Compute quotas](https://docs.nebius.com/compute/resources/quotas-limits.md) are only released after the VM deletion. If a VM is `Stopped`, the quotas are still occupied. To avoid running out of the quotas, revise your list of VMs from time to time and delete unused VMs. Stopping them will not help.
