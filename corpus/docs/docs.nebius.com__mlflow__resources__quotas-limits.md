# Quotas in Managed Service for MLflow

Source: https://docs.nebius.com/mlflow/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas in Managed Service for MLflow

Managed Service for MLflow has quotas on clusters, computing resources and SSD storage.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

## Clusters

A Managed MLflow cluster and its resources count toward the quotas throughout the lifecycle of the cluster, from its creation to deletion, regardless of whether the cluster is in use or idle.

Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| :- | :- |
| Clusters | 10 |
| Total vCPUs across clusters | 80 |
| Total RAM across clusters | 320 GiB |
| Network SSD disks total size across clusters | 1.95 TiB |
