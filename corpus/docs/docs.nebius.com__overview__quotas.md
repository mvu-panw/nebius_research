# Quotas in Nebius AI Cloud

Source: https://docs.nebius.com/overview/quotas

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas in Nebius AI Cloud

*Quotas* define how much Nebius AI Cloud resources you can use. When you [sign up](https://docs.nebius.com/signup-billing/sign-up.md), your quotas are set to default values. You can request to change them if you need more resources or if you want to limit your usage and costs.

Each [region](https://docs.nebius.com/overview/regions.md) has its own quotas. You can configure different quotas for each project in the region.

## View quotas

To view your quotas and their usage, go to **Administration** → **Limits** → **Quotas** in the [Nebius AI Cloud web console](https://console.nebius.com). Use the filter next to the search box to view only specific service quotas.

## Change quotas

> [!NOTE]
>
> Only users in [groups](https://docs.nebius.com/iam/authorization/groups/index.md) with the `admin` role can change quotas. To check which groups you are in, go to the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

You can request to increase a quota if you need more resources, or to decrease a quota to limit your usage and costs:

**Web console**

1. In the sidebar, go to  **Administration** → **Limits**.
2. On the **Quotas** tab, select the service for which you want to change a quota.
3. In the row of the required quota, click  → **Change quota**.
4. Specify a new quota value and send the request.

You can view your quota requests in the [support center](https://console.nebius.com/support).

## Automatic quota reduction

Nebius AI Cloud may automatically reduce quotas when their usage remains significantly below the assigned limit for a prolonged period. This helps rebalance workloads and free up capacity across the platform.

Running workloads are not affected by quota reductions. Quotas are not reduced below default values.

How it works:

1. You receive an email notification about the planned quota reduction with details about which quotas will be reduced and when the change will take effect.
2. You have a grace period (usually two days) to review the changes. No changes are applied during this period. If your usage increases during the grace period, the reduction is automatically canceled.
3. If your usage doesn't increase during the grace period, the change applies automatically on the date stated in the notification.

   You can request a quota increase at any time if you need more capacity.

## Quotas of services

For more details about quotas of Nebius AI Cloud services, see the service documentation:

* [Audit Logs quotas](https://docs.nebius.com/audit-logs/resources/quotas-limits.md)
* [Compute quotas](https://docs.nebius.com/compute/resources/quotas-limits.md) (also apply to Serverless AI)
* [Container Registry quotas](https://docs.nebius.com/container-registry/resources/quotas-limits.md)
* [DNS quotas](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md)
* [Logging quotas](https://docs.nebius.com/observability/resources/quotas-limits.md)
* [Managed Service for Kubernetes® quotas](https://docs.nebius.com/kubernetes/resources/quotas-limits.md)
* [Managed Service for MLflow quotas](https://docs.nebius.com/mlflow/resources/quotas-limits.md)
* [Managed Service for PostgreSQL® quotas](https://docs.nebius.com/postgresql/resources/quotas-limits.md)
* [Managed Service for Soperator quotas](https://docs.nebius.com/slurm-soperator/managed-soperator/resources/quotas.md)
* [Object Storage quotas](https://docs.nebius.com/object-storage/resources/quotas-limits.md)
* [Key Management Service quotas](https://docs.nebius.com/kms/resources/quotas-limits.md)
* [SecretStash quotas](https://docs.nebius.com/mysterybox/resources/quotas-limits.md)
* [Nebius Tunnels quotas](https://docs.nebius.com/tunnels/resources/quotas-limits.md)
* [Virtual Networks quotas](https://docs.nebius.com/vpc/resources/quotas-limits.md)
