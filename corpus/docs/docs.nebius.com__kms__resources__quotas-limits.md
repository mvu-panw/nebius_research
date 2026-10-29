# Quotas and constraints in Key Management Service

Source: https://docs.nebius.com/kms/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas and constraints in Key Management Service

## Quotas

Key Management Service has quotas on the number of symmetric and asymmetric keys.

| Quota name | Default value per [tenant](https://docs.nebius.com/iam/overview.md#tenants) |
| :- | :- |
| Symmetric keys | 3000 |
| Asymmetric keys | 3000 |

> [!NOTE]
>
> A deleted key counts towards the quota for 30 days after you [delete](https://docs.nebius.com/kms/manage/delete-restore.md) it.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

## Constraints

The number of [manual rotations](https://docs.nebius.com/kms/manage/rotate.md) for a symmetric key can't exceed 100. If you exceed this limit, the request fails with the `HTTP 400` error.

To increase this limit for a specific symmetric key, [contact support](https://console.nebius.com/support).
