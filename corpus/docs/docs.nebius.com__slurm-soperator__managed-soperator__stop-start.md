# Stopping and starting Soperator clusters in Managed Service for Soperator

Source: https://docs.nebius.com/slurm-soperator/managed-soperator/stop-start

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Stopping and starting Soperator clusters in Managed Service for Soperator

If you are not using the Soperator cluster that you have deployed in Managed Service for Soperator, you can stop it in the [web console](https://console.nebius.com) to save costs. While the cluster is stopped, Managed Service for Soperator [charges you](https://docs.nebius.com/slurm-soperator/managed-soperator/resources/pricing.md) for the cluster's storage resources: the disks of worker, login and controller nodes, and the shared filesystem. The service does not charge you for the cluster's computing resources (GPUs, vCPUs and RAM).

When you need the cluster again, you can start it. Starting the cluster takes around 15 minutes.

The cluster keeps the data that you saved in it, although you can only access it after you restart the cluster.

Computing and storage resources of a stopped cluster count towards [Compute quotas](https://docs.nebius.com/compute/resources/quotas-limits.md), just like a running cluster.

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to stop and start a cluster

**Web console**

1. In the sidebar, go to  **AI orchestration** → **Soperator**.
2. Find the required cluster in the list.
3. Next to the cluster, click  → **Stop**.
