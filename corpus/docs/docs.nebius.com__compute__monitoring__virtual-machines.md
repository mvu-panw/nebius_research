# Monitoring virtual machines in Nebius AI Cloud

Source: https://docs.nebius.com/compute/monitoring/virtual-machines

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring virtual machines in Nebius AI Cloud

You can monitor GPUs, vCPUs and network statuses on the dashboards in the Nebius AI Cloud [web console](https://console.nebius.com). There are two ways to find the required dashboard:

* Go to  **Observability** → [Metrics](https://console.nebius.com/observability/metrics) and select the resource you would like to review.
* Go to the page of the VM you would like to review and switch to the **Metrics** tab.

Use the dashboard to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/compute/resources/quotas-limits.md) increases and quickly identify anomalies. In case of VM issues, dashboards help the Nebius support team investigate the issue.

Data for the dashboard is collected automatically. For more information about metrics collection, see [Monitoring agent on Compute virtual machines](https://docs.nebius.com/observability/agents/monitoring-agent.md).

## Explore the dashboard

The VM usage data becomes available 5–10 minutes after the VM is created.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## GPU monitoring metrics

The corresponding [NVIDIA metrics](https://docs.nvidia.com/datacenter/dcgm/latest/dcgm-api/dcgm-api-field-ids.html) are shown next to the Nebius AI Cloud metric.

* **GPU utilization** (`DCGM_FI_DEV_GPU_UTIL`)

  Percentage of time a GPU spends executing tasks.

* **Memory utilization** (`DCGM_FI_DEV_MEM_COPY_UTIL`)

  Percentage of time GPU memory was in use (performing read or write tasks) in a dedicated period.

* **Free frame buffer in MB** (`DCGM_FI_DEV_FB_FREE`)

  Amount of free frame buffer memory.

* **Used frame buffer in MB** (`DCGM_FI_DEV_FB_USED`)

  Amount of used frame buffer memory.

* **Total frame buffer of the GPU in MB** (`DCGM_FI_DEV_FB_TOTAL`)

  A constant. The total amount of frame buffer memory.

* **Reserved frame buffer in MB** (`DCGM_FI_DEV_FB_RESERVED`)

  A constant. Amount of frame buffer memory reserved for the internal use of the hardware: drivers, firmware, etc.

* **The number of bytes of active PCIe rx/tx** (`DCGM_FI_PROF_PCIE_RX_BYTES`, `DCGM_FI_PROF_PCIE_TX_BYTES`)

  Number of bytes a GPU received from (rx) or transmitted to (tx) its host VM and other devices over PCIe. Both header and payload of each PCIe packet are included.

* **SM clock for the device** (`DCGM_FI_DEV_SM_CLOCK`)

  Frequency of the main GPU clock.

* **Memory clock for the device** (`DCGM_FI_DEV_MEM_CLOCK`)

  Frequency and total amount of operations in time spans.

* **Current clock throttle reasons** (`DCGM_FI_DEV_CLOCK_THROTTLE_REASONS`)

  A bitmask of [possible reasons for GPU throttling](https://docs.nvidia.com/datacenter/dcgm/2.2/dcgm-api/group__dcgmFieldConstants.html).

  For example, if the GPU is throttling because it has overheated and slowed down, the chart will show 72: code 0x40 for overheating (`DCGM_CLOCKS_THROTTLE_REASON_HW_THERMAL`) + code 0x8 for slowdown (`DCGM_CLOCKS_THROTTLE_REASON_HW_SLOWDOWN`) = 72 in decimal.

* **Power usage for the device** (`DCGM_FI_DEV_POWER_USAGE`)

  Current energy consumption by a GPU in watts.

* **Total energy consumption for the GPU since the driver was last reloaded** (`DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION`)

  Cumulative energy consumption by a GPU since the recent driver reload in millijoules.

* **Memory temperature for the device** (`DCGM_FI_DEV_MEMORY_TEMP`)

  Memory temperature in degrees Celsius.

* **Current temperature readings for the device** (`DCGM_FI_DEV_GPU_TEMP`)

  GPU core temperature in degrees Celsius.

* **Current power limit for the device** (`DCGM_FI_DEV_POWER_MGMT_LIMIT`)

  A constant. Power consumption limit after which the GPU will be throttled.

* **Slowdown temperature for the device** (`DCGM_FI_DEV_SLOWDOWN_TEMP`)

  A constant. Temperature threshold after which the GPU will be throttled until it cools down.

* **The number of bytes of active NVLink (RX/TX)**(`PROF_NVLINK_TX_BYTES`, `PROF_NVLINK_RX_BYTES`)

  Number of bytes a GPU received from (rx) or transmitted to (tx) its host VM and other devices over NVLink, not including protocol headers, in bytes per second.

If you have a [GPU cluster](https://docs.nebius.com/compute/clusters/gpu/index.md), the following metrics become available and help monitor InfiniBand™ connection:

* **Link Downed Total**

  Number of times the port failed to recover the link and downed it.

* **Link Error Recovery Total**

  Number of times the port recovered the link after error.

* **Port Data Total (RX/TX)**

  Number of bytes all GPUs received (rx) or transmitted (tx) via the port, including packets with errors.

* **Port Discards TX Total**

  Number of transmitted packets discarded by the port when the port was down or not responding.

* **Port Errors RX Total**

  Number of received packets with errors, including physical, mailformed data and link packet errors and overrun buffer.

* **Port Packets Total (RX/TX)**

  Speed of receiving (rx) or transmitting (tx) packets on all GPUs, including packets with errors and excluding link packets. Calculated in packets per second.

* **Transfer Rate**

  Data transferring speed, calculated in bytes per second.

## vCPU monitoring metrics

* **CPU utilization**

  Percentage of time vCPUs spend executing tasks.

* **RAM**

  Amount of total and used memory.

* **Disk bytes**

  Average data transfer throughput of the VM's disks. Measured in bytes per second.

* **Disk operations**

  Average IOPS of the VM's disks. Measured in operations per second.

* **Network bytes**

  Average data transfer speed of the VM's network. Measured in bytes per second.

* **Network packets**

  Average packets transfer speed of the VM's network. Measured in packets per second.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
