# Using the serial console for virtual machines in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/serial-console

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Using the serial console for virtual machines in Nebius AI Cloud

The *serial console* is a browser-based, text-only session to your virtual machine’s serial port that you can use to connect to and troubleshoot a VM when normal network access is unavailable. You can also use it for the first-boot setup on custom or third-party images when SSH is not yet configured.

> [!NOTE]
>
> Serial console for Compute VMs is [in preview](https://docs.nebius.com/overview/services.md#service-and-application-stages).

## Prerequisites

* [Add a user for connections to the VM](https://docs.nebius.com/compute/virtual-machines/manage.md#optional-create-a-user-data-configuration) the serial console of which you want to access.
* Make sure you are in a [default group](https://docs.nebius.com/iam/authorization/groups/index.md#default-groups) that has the `admin` [role](https://docs.nebius.com/iam/authorization/roles.md#compute) or in a [custom group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `compute.serial-console-user` role within your tenant or project. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Using the serial console

To open the serial console:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. Select the virtual machine.
3. Click  **Open serial console**.

The console opens in the browser as a dedicated terminal view.

> [!NOTE]
>
> The serial console session is **text-only** and doesn't support a graphical interface.

## Limits and concurrent sessions

Only one serial console session can be active for a given VM at a time. If someone else already has a session open, a new connection will fail until the other session ends. Be sure to close any unused console windows in your browser if you no longer need the session.

## Troubleshooting

### Resource not found

In this case, the VM might be stopped. [Start the VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) and then open the serial console again.

### Connection failed

Another serial console session is already open for this VM. Coordinate with other users, or wait and try again.

### Access denied

If you can't access the serial console and you don't have permission to use it, contact the administrator of your tenant. Ask them to add you to the group with at least the `compute.serial-console-user` role.

### Checking Audit Logs for serial console events

[Audit Logs](https://docs.nebius.com/audit-logs/index.md) records all serial console connection attempts, including failed ones. To find these events, [filter](https://docs.nebius.com/audit-logs/events/filter.md) them by the service: `"service.name='COMPUTE_CONSOLE'"`.

For failed attempts, check the event's `response.error_message` field. For example, the `Permission denied` message in the field indicates access denied.

## See also

* [Connecting to virtual machines](https://docs.nebius.com/compute/virtual-machines/connect.md)
* [Viewing serial logs of virtual machines](https://docs.nebius.com/compute/monitoring/serial-logs.md)
