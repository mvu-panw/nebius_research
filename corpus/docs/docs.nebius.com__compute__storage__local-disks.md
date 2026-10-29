# Using local SSD disks on Compute virtual machines

Source: https://docs.nebius.com/compute/storage/local-disks

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Using local SSD disks on Compute virtual machines

Local SSD disks are Non-Volatile Memory Express (NVMe) drives physically attached to the compute host that runs a virtual machine (VM). Local SSD disks offer low-latency storage, but they are *ephemeral*. When the VM is stopped or deleted, the data is lost.

## Availability

Local SSD disks are available:

* Only in the `uk-south1`, `eu-west2` and `us-north1` [regions](https://docs.nebius.com/overview/regions.md).
* Only on the NVIDIA® B300 NVLink with Intel Granite Rapids platform (`gpu-b300-sxm`) with the eight-GPU preset `8gpu-192vcpu-2768gb`.

The capacity of local SSD disks is fixed by the platform and preset. This configuration adds `6 × 3.84 TB` of local storage.

## How to add local SSD disks

Local SSD disks can be enabled when [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm). They are not created as a separate storage resource, and you cannot add them to an existing VM or change this setting later.

You can create [RAID](https://en.wikipedia.org/wiki/RAID) on top of your local SSD disks, for example, to combine multiple disks into a single logical storage for higher performance or easier management.

## Lifecycle and data persistence

Local SSD data persistence depends on whether the event affects the Compute VM or only the VM operating system:

* If you reboot the VM operating system from inside the VM, for example by using `sudo reboot`, data is expected to persist because the Compute VM is not stopped or deleted.
* If you stop or delete the VM in Compute, data on local SSD disks is lost.
* If the host or a local disk fails, the Compute VM enters maintenance mode and data is lost.

When a Compute VM is stopped or deleted, the local SSD disks are released and sanitized with additional cleanup checks to clear the disks of all data before reuse.

## When to use durable storage instead

Use durable storage instead of local SSD disks if you need any of the following:

* Data that must survive VM stop, deletion or rescheduling events. Use [Network disks](https://docs.nebius.com/compute/storage/types.md#disks), [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) or [Object Storage](https://docs.nebius.com/object-storage.md).
* Data sharing across several VMs. Use [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) or [Object Storage](https://docs.nebius.com/object-storage.md).
* Snapshots, backup workflows or long-term retention. Use [Network disks](https://docs.nebius.com/compute/storage/types.md#disks), [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) or [Object Storage](https://docs.nebius.com/object-storage.md).
* User-defined capacity that is independent of the selected VM preset. Use [Network disks](https://docs.nebius.com/compute/storage/types.md#disks) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems).

## See also

* [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md)
* [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm)
* [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md#local-ssd-disks)
