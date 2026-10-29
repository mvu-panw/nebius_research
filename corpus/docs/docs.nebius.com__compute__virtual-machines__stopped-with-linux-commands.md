# Charging for a virtual machine that was stopped by using Linux commands

Source: https://docs.nebius.com/compute/virtual-machines/stopped-with-linux-commands

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Charging for a virtual machine that was stopped by using Linux commands

If you connect to your virtual machine (VM) and shut it down by using Linux commands (for example, `shutdown` or `halt`), the VM is not stopped properly. Compute automatically reboots the VM and continues charging you for it. The service considers such a shutdown as a failure and therefore runs the recovery policy.

To stop a VM properly, use Nebius AI Cloud interfaces, for instance, the web console or a CLI command. Then, the VM is stopped reliably, and you are not charged for it. For more information, see [How to stop and start Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/stop-start.md).
