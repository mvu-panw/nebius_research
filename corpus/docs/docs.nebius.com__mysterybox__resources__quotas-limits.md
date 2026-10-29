# SecretStash quotas

Source: https://docs.nebius.com/mysterybox/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# SecretStash quotas

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

SecretStash has quotas on the number of secrets.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| :- | :- |
| Secrets | 3000 |

> [!NOTE]
>
> A deleted secret counts toward the quota for 30 days after you delete it.
