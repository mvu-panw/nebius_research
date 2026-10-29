# How to collect journald logs from Compute virtual machines

Source: https://docs.nebius.com/observability/logs/journald

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to collect journald logs from Compute virtual machines

The monitoring agent installed on Compute virtual machines can collect [journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) logs from systemd services and forward them to Observability Logs. This allows you to centralize and analyze system-level logs from your VMs.

## Enable journald log collection

To enable journald log collection, you need to set specific labels on your Compute virtual machine. You can do this when creating a VM or by updating an existing one.

For Managed Service for Kubernetes® nodes, see [How to enable journald logs](https://docs.nebius.com/kubernetes/logs.md#how-to-enable-journald-logs).

### Configuration labels

Use the following labels to configure journald log collection:

| Label | Description | Example value |
| - | - | - |
| `nebius.o11y.systemd-logs-collection.enabled` | Enables or disables journald log collection. | `true` or `false` |
| `nebius.o11y.systemd-logs-collection.units` | Specifies which systemd units to collect logs from. Separate multiple units with semicolons. If not specified, logs from all units are collected. | `sshd.service;docker.service` |

## How to set labels

**CLI**

When creating a new VM by running [nebius compute instance create](https://docs.nebius.com/cli/reference/compute/instance/create.md), pass the labels through the `--labels` parameter:

```bash theme={null}
nebius compute instance create \
  --name my-vm \
  --labels "nebius.o11y.systemd-logs-collection.enabled=true,nebius.o11y.systemd-logs-collection.units=sshd.service;docker.service" \
  --resources-platform cpu-e2 \
  --resources-preset 2vcpu-8gb \
  --boot-disk-existing-disk-id <boot_disk_ID> \
  --boot-disk-attach-mode READ_WRITE \
  --network-interfaces '[{"name": "default-subnet", "subnet_id": "<subnet_ID>", "ip_address": {}}]'
```

To update labels on an existing VM, run [nebius compute instance update](https://docs.nebius.com/cli/reference/compute/instance/update.md):

```bash theme={null}
nebius compute instance update \
  --id <VM_ID> \
  --labels "nebius.o11y.systemd-logs-collection.enabled=true,nebius.o11y.systemd-logs-collection.units=sshd.service;docker.service"
```

To set multiple labels, separate them with commas.

**Terraform**

When creating a new VM, include the labels in the resource configuration:

```hcl theme={null}
resource "nebius_compute_v1_instance" "my_vm" {
  name      = "my-vm"
  parent_id = "<project_ID>"

  labels = {
    "nebius.o11y.systemd-logs-collection.enabled" = "true"
    "nebius.o11y.systemd-logs-collection.units"   = "sshd.service;docker.service"
  }

  resources = {
    platform = "cpu-e2"
    preset   = "2vcpu-8gb"
  }

  boot_disk = {
    attach_mode = "READ_WRITE"
    existing_disk = {
      id = nebius_compute_v1_disk.boot_disk.id
    }
  }

  network_interfaces = [
    {
      name      = "default-subnet"
      subnet_id = "<subnet_ID>"
      ip_address = {}
    }
  ]
}
```

> [!WARNING]
>
> After updating labels on an existing VM via the CLI or Terraform, you must [stop and then start the VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md) for the changes to take effect.

For more details on creating and managing VMs, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

## View collected logs

After configuring journald log collection, you can view the collected logs in Grafana®. For instructions on how to connect and query logs, see [How to view logs in Grafana®](https://docs.nebius.com/observability/logs/grafana.md).

## Collected attributes

The monitoring agent extracts the following attributes from journald log entries:

| Attribute | Description |
| - | - |
| `SYSTEMD_UNIT` | The systemd unit that generated the log entry. |
| `syslog.identifier` | The syslog identifier of the process. |
| `BOOT_ID` | A unique identifier for the current boot session. |
| `CAP_EFFECTIVE` | The effective capabilities of the process. |
| `SYSTEMD_CGROUP` | The control group path of the process. |
| `GID` | The group ID of the process. |
| `PID` | The process ID of the process that generated the log. |
| `UID` | The user ID of the process. |
| `CMDLINE` | The command line of the process. |
| `TRANSPORT` | The transport mechanism used to deliver the log (for example, `journal` or `syslog`). |
| `STREAM_ID` | The stream identifier for stdout/stderr streams. |
| `SYSLOG_FACILITY` | The syslog facility number. |
| `SYSLOG_IDENTIFIER` | The syslog identifier string. |

## Data enrichment

In addition to the journald attributes, the monitoring agent enriches log entries with the following metadata:

| Attribute | Description |
| - | - |
| `instance_id` | The unique identifier of the Compute VM. |
| `container_id` | The ID of the VM's parent project. |
| `mk8s_cluster_id` | The Managed Kubernetes cluster ID, if the VM is a cluster node. |
| `mk8s_node_group_id` | The Managed Kubernetes node group ID, if the VM is a cluster node. |
| `gpu_cluster_id` | The GPU cluster ID, if the VM is part of a GPU cluster. |

## See also

* [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md)
* [How to view logs in Grafana®](https://docs.nebius.com/observability/logs/grafana.md)
* [Monitoring agent on Compute virtual machines](https://docs.nebius.com/observability/agents/monitoring-agent.md)
