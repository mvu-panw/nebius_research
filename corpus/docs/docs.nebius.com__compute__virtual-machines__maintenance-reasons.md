# Maintenance reasons in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/maintenance-reasons

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Maintenance reasons in Nebius AI Cloud

When Compute schedules maintenance for your virtual machine (VM), it assigns a *reason code* that describes why the maintenance was triggered. After you identify the reason, [stop and start your VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-compute-virtual-machines) to prepare it for maintenance. The reason code helps you assess the severity of the error and decide whether additional action is needed.

## How to identify the reason code for a maintenance event

You can view the reason code for maintenance events by:

* Checking the maintenance notification banner in the [web console](https://console.nebius.com/);
* Using the [Nebius AI Cloud CLI](https://docs.nebius.com/cli/index.md) to list all active maintenance events scheduled for resources in a project.

Run the following command, and specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

```bash theme={null}
nebius compute maintenance list-active --parent-id <project_ID>
```

The output contains a list of all maintenance events that are scheduled for resources in the project you specified.

## Reason codes

Maintenance events can be triggered by GPU, InfiniBand™ or node-level errors. The tables below show the reason codes that map to different types of errors.

If maintenance was triggered by a condition that is not mapped to one of these reason codes, Compute assigns `OTHER` as the reason code.

### GPU errors

| Reason code | Description |
| - | - |
| `HW_GPU_PCI_FALLEN_OFF_BUS` | A GPU or NVSwitch has fallen off the PCI bus, typically due to critical thermal or power issues. The affected node is taken out of service for hardware inspection. |
| `HW_GPU_PCI_CONFIG_ERROR` | Unexpected GPU PCI configuration detected, or critical PCI errors observed between the GPU, deltaboard and motherboard. Requires physical hardware maintenance. |
| `HW_GPU_NVLINK_DOWN` | An NVLink connection is down on a Blackwell or newer GPU. Requires a GPU reset or VM restart to recover. |
| `HW_GPU_XID_62` | The GPU internal micro-controller has halted (XID 62). Requires a GPU reset or VM restart. |
| `HW_GPU_XID_109` | GPU context switch timeout (XID 109). Typically not fatal to running workloads, but may require a GPU reset or VM restart. |
| `HW_GPU_XID_119` | GSP RPC timeout (XID 119). Requires a GPU reset or VM restart. |
| `HW_GPU_FW_VERSION_UNAVAILABLE` | DCGM could not report the GPU firmware version. This is usually a symptom of other underlying hardware errors. |
| `HW_GPU_DRIVER_INIT_FAILED` | The NVIDIA® driver failed to initialize one or more GPUs. Typically caused by other hardware errors. |

### InfiniBand™ errors

| Reason code | Description |
| - | - |
| `HW_IB_LINK_DOWN` | The InfiniBand link has been in a physically down state for more than 3 minutes. |
| `HW_IB_PCI_FALLEN_OFF_BUS` | The InfiniBand adapter has fallen off the PCI bus, typically due to critical thermal or power issues. |
| `HW_IB_PCI_CONFIG_ERROR` | Unexpected InfiniBand PCI configuration detected, typically due to critical PCI errors. |

### Node-level errors

| Reason code | Description |
| - | - |
| `HW_NODE_OFFLINE` | The node hosting the VM went offline. The cause may vary. Affected VMs are force-migrated and will experience an unexpected reboot. |

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
