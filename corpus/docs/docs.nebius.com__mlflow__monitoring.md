# How to monitor clusters in Managed Service for MLflow

Source: https://docs.nebius.com/mlflow/monitoring

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to monitor clusters in Managed Service for MLflow

You can monitor the state of Managed MLflow clusters on dashboards in the Nebius AI Cloud [web console](https://console.nebius.com/). There are two ways to find the required dashboard:

* Go to  **Observability** → **Metrics** and select the resources you would like to review.
* Go to the page of the cluster you would like to review and switch to the **Metrics** tab.

Use the dashboards to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/mlflow/resources/quotas-limits.md) increases and quickly identify anomalies. In case of issues with your clusters, dashboards also help the Nebius support team investigate the issues.

Data for the dashboards is collected automatically.

> [!NOTE]
>
> Dashboard data becomes available 5–10 minutes after the cluster is created.

## Dashboard filters

Keep `mlflow` selected in the **Group** list. The other groups in the list are used for internal purposes.

To check Managed MLflow container health separately, from the **Pod** list, select the containers you want to review.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## Cluster monitoring metrics

### Resource usage

* **Service containers**

  Number of containers.

* **Total service CPU usage**

  Amount of vCPU that a cluster consumed.

* **Total service memory usage**

  Amount of consumed RAM in MiB, with work memory and cache.

* **Total disk IO usage**

  Disk read/write rate, in bytes per second.

* **Total service network usage**

  Network receive/transmit rate, in bytes per second.

* **Total service disk usage**

  Amount of consumed storage in KiB.

* **Throttling containers (%)**

  Percentage of CPU periods when containers were throttled.

* **Throttling containers in seconds**

  Percentage of CPU seconds when containers were throttled.

* **CPU usage**

  Amount of vCPU consumed per container, including the limit.

* **Memory usage**

  Amount of memory that containers used in a dedicated period, including work memory and cache. Measured in bytes.

* **Network RX/TX**

  Average speed of data received/sent over the network per container, in bytes per second.

* **Disk IO**

  Average IOPS of the cluster disks per container, in operations per second.

* **Disk used space**

  Amount of disk space consumed per container, including the limit.

* **Disk inodes used**

  Number of used [inodes](https://www.kernel.org/doc/html/latest/filesystems/ext4/inodes.html) with files metadata per container, including the limit. A lack of inodes leads to an overall lack of disk space, especially if you generate many small files in an experiment.

### MLflow

* **Experiments count**

  Number of experiments created in Managed MLflow.

* **Runs count**

  Number of training runs.

* **Models count**

  Number of registered models, including versioned models.

* **Users count**

  Number of unique users who are running experiments.
