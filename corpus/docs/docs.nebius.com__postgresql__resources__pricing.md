# Pricing in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/resources/pricing

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing in Managed Service for PostgreSQL®

This article provides detailed pricing for Managed Service for PostgreSQL in Nebius AI Cloud.

## How charges and prices work

Each group of chargeable items in this article has two time units associated with it:

* **Billing unit**: The minimum unit of usage for which you can be charged.
* **Pricing unit**: The unit of usage for which the prices are shown.

Charges for units smaller than the pricing unit are calculated proportionally.

> For example, for GPUs on running VMs, the **billing unit** is 1 second, and the **pricing unit** is 1 hour (3600 seconds). For 30 minutes of usage, you will be charged half the hourly price.

Prices in US dollars (USD, \$) apply to all customers except for companies from Israel, where prices in Israeli shekels (ILS, ₪) apply instead.

All prices are shown without any applicable taxes, including VAT. Due to rounding errors, usage costs shown in the web console and final charges may slightly differ from calculations based on the prices in this article.

## Prices

Managed PostgreSQL charges you for the computing resources allocated to cluster hosts and the storage size.

Public access to clusters is free of charge.

### Hosts

You are charged for running hosts in your Managed PostgreSQL clusters.

* **Billing unit**: 1 second
* **Pricing unit**: 1 hour (3600 seconds)

**USD**

Charges are based on the resource preset that you are using. For example, using a `4vcpu-16gb` cluster for 1 hour costs 4 × \$0.034 + 16 × \$0.009 = \$0.28.

**ILS**

Charges are based on the resource preset that you are using. For example, using a `4vcpu-16gb` cluster for 1 hour costs 4 × ₪0.1054 + 16 × ₪0.0279 = ₪0.868.

#### Non-GPU Intel Ice Lake

The platform is only available in the `eu-north1` [region](https://docs.nebius.com/overview/regions.md).

**USD**

| Item | Price per 1 hour |
| - | - |
| Managed PostgreSQL® on Non-GPU Intel Ice Lake. CPU | \$0.034 |
| Managed PostgreSQL® on Non-GPU Intel Ice Lake. RAM | \$0.009 |

**ILS**

| Item | Price per 1 hour |
| - | - |
| Managed PostgreSQL® on Non-GPU Intel Ice Lake. CPU | ₪0.1054 |
| Managed PostgreSQL® on Non-GPU Intel Ice Lake. RAM | ₪0.0279 |

#### Non-GPU AMD EPYC Genoa

The platform is available in the `eu-north1`, `eu-west1`, `me-west1`, `us-central1`, `uk-south1` and `eu-west2` [regions](https://docs.nebius.com/overview/regions.md).

**USD**

| Item | Price per 1 hour |
| - | - |
| Managed PostgreSQL® on Non-GPU AMD EPYC Genoa. CPU | \$0.034 |
| Managed PostgreSQL® on Non-GPU AMD EPYC Genoa. RAM | \$0.009 |

**ILS**

| Item | Price per 1 hour |
| - | - |
| Managed PostgreSQL® on Non-GPU AMD EPYC Genoa. CPU | ₪0.1054 |
| Managed PostgreSQL® on Non-GPU AMD EPYC Genoa. RAM | ₪0.0279 |

### Storage

You are charged for the disks attached to existing Managed PostgreSQL hosts. Charges are based on disk sizes, regardless of the amount of used space.

* **Billing unit**: 1 byte per 1 second
* **Pricing unit**: 1 GiB per 730 hours (2<sup>30</sup> bytes per 2,628,000 seconds \~ 1 month)

**USD**

| Item | Price per 1 GiB per 730 hours |
| - | - |
| Managed PostgreSQL®. Network SSD disk | \$0.071 |

**ILS**

| Item | Price per 1 GiB per 730 hours |
| - | - |
| Managed PostgreSQL®. Network SSD disk | ₪0.221 |

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
