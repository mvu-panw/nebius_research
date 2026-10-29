# Parameters of a virtual machine configuration in Compute

Source: https://docs.nebius.com/compute/virtual-machines/params

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Parameters of a virtual machine configuration in Compute

When you [create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md) (VM) or edit its configuration, you operate with VM settings. Below is the list of the VM settings available in the [web console](https://console.nebius.com) creation wizard and on the VM settings page.

## General

If you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), on the **General** step of the wizard, you choose how Compute allocates resources:

* **Reserved VM**: Capacity is assured by your capacity block groups. This option is for regular VMs with GPUs.
* **Pay-as-you-go VM**: Capacity is subject to availability. This option allows [preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) and VMs without GPUs.

If you do not have capacity block groups, the wizard skips the **General** step and opens **Compute** instead.

## Compute

On the **Compute** step, you configure computing resources. The available settings depend on whether you selected **Reserved VM** or **Pay-as-you-go VM** on the **General** step. If the **General** step was skipped, use the **Pay-as-you-go VM** settings below.

### Reserved VM

* [Platform](https://docs.nebius.com/compute/virtual-machines/types.md). The list shows platforms that match your capacity block groups.

* [**Reservation**](https://docs.nebius.com/compute/virtual-machines/reservations.md) settings: **Region**, **Any (existing and future)**, specific capacity block groups, and **Switch to PAYG** with **When reservation is exhausted** or **Never**.

* Preset.

* (Optional) [GPU cluster](https://docs.nebius.com/compute/clusters/gpu/index.md). Allows accelerating tasks that require high-performance computing (HPC) power, such as training a model.

  A GPU cluster only helps if you add at least two VMs with 8 GPUs each to the cluster.

* VM name.

* Project for the VM location.

### Pay-as-you-go VM

* Select **With GPUs** or **Without GPUs** and the VM type **Regular** or [Preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md).

* [Platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

* **Max price** (for [preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md)): Select or create a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md), or choose **Follow spot price**.

* (Optional) [GPU cluster](https://docs.nebius.com/compute/clusters/gpu/index.md). Allows accelerating tasks that require HPC power, such as training a model.

  A GPU cluster only helps if you add at least two VMs with 8 GPUs each to the cluster.

* VM name.

* Project for the VM location.

## Storage

On the **Storage** step, you can add a boot disk, additional disks and shared filesystems. For disks, you specify their type, size and block size. A boot disk is additionally based on an operating system. For more information about these settings, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

For shared filesystems, you specify the following settings:

* [Name, size and block size](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

* Mount tag for mounting the filesystem to the VM.

  Create your own tag, such as `my-filesystem`. Make sure that it is unique within the VM.

* **Auto mount** option enabled to mount the filesystem to the VM automatically.

## Network

On the **Network** step, you select a [network and subnet](https://docs.nebius.com/vpc/overview.md) and manage the VM addresses:

* **Private address**: Select whether to allocate a random private IP address for the VM or to attach an allocation of a private address.
* **Public address**: Specify whether the VM should have a public IP address and whether it should be static or dynamic.
* **Hostname**: Select **Same as VM ID** or specify a **Custom** hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md).

If you need to secure your VM and make it isolated, you can create a VM without a public IP address. If you need to connect to this VM from the internet, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md). It has an IP address in the internet and an IP address in the VM's network. As a result, you can access the VM via the jump server from the internet. This approach enhances security and still provides access to the VM.

For more information about the settings of the addresses, see [Private and public IP addresses of Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/network.md).

## Configuration

On the **Configuration** step, you configure access, identity and VM startup settings for the VM.

### Access

In the **Username and SSH key** field, you add credentials of the user on behalf of whom you can [connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md).

The access settings include the following:

* Username of the VM user.

  Cannot be `root` or `admin`. These usernames are reserved for internal needs and are not allowed to connect to a VM by SSH.

* [Public key of your SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md#getting-the-public-key).

* Name of credentials to recognize the key in the list of keys.

### Additional

(Optional) **Service account**: Select an existing [service account](https://docs.nebius.com/iam/service-accounts/manage.md) or create a new one. The service account will perform actions on behalf of the VM, for example, run scripts.

### User data

(Optional) Select **Enable custom cloud-init config** and set a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format to customize how the VM starts.

## Review

On the **Review** step, you see a summary of all settings before creating the VM. To edit a section, click  next to the corresponding block on the **Review** step.
