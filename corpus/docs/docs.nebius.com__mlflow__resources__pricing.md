# Pricing in Managed Service for MLflow

Source: https://docs.nebius.com/mlflow/resources/pricing

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing in Managed Service for MLflow

This article provides detailed pricing for Managed MLflow in Nebius AI Cloud.

## How charges and prices work

Each group of chargeable items in this article has two time units associated with it:

* **Billing unit**: The minimum unit of usage for which you can be charged.
* **Pricing unit**: The unit of usage for which the prices are shown.

Charges for units smaller than the pricing unit are calculated proportionally.

> For example, for GPUs on running VMs, the **billing unit** is 1 second, and the **pricing unit** is 1 hour (3600 seconds). For 30 minutes of usage, you will be charged half the hourly price.

Prices in US dollars (USD, \$) apply to all customers except for companies from Israel, where prices in Israeli shekels (ILS, ₪) apply instead.

All prices are shown without any applicable taxes, including VAT. Due to rounding errors, usage costs shown in the web console and final charges may slightly differ from calculations based on the prices in this article.

## Prices

Managed MLflow charges you for the computing resources allocated to clusters and the internal storage size. Also, Object Storage charges you for the buckets attached to Managed MLflow clusters to store artifacts.

Public access to clusters is free of charge.

### Computing resources

You are charged for computing resources in your Managed MLflow clusters.

* **Billing unit**: 1 second
* **Pricing unit**: 1 hour (3600 seconds)

Charges are based on the cluster size that you are using:

**USD**

* Each `small` Managed MLflow cluster uses 6 vCPUs and 24 GiB of RAM. Therefore, one hour of computing resources for a cluster costs 6 × \$0.03 + 24 × \$0.0075 = \$0.36.
* Each `medium` Managed MLflow cluster uses 8 vCPUs and 32 GiB of RAM. Therefore, one hour of computing resources for a cluster costs 8 × \$0.03 + 32 × \$0.0075 = \$0.48.

**ILS**

* Each `small` Managed MLflow cluster uses 6 vCPUs and 24 GiB of RAM. Therefore, one hour of computing resources for a cluster costs 6 × ₪0.093 + 24 × ₪0.02325 = ₪1.116.
* Each `medium` Managed MLflow cluster uses 8 vCPUs and 32 GiB of RAM. Therefore, one hour of computing resources for a cluster costs 8 × ₪0.093 + 32 × ₪0.02325 = ₪1.488.

Starting October 2025, creating `small` clusters is no longer supported.

#### Non-GPU Intel Ice Lake

The platform is only available in the `eu-north1` [region](https://docs.nebius.com/overview/regions.md).

**USD**

| Item | Price per 1 hour |
| - | - |
| Managed MLflow on Non-GPU Intel Ice Lake. CPU | \$0.03 |
| Managed MLflow on Non-GPU Intel Ice Lake. RAM | \$0.0075 |

**ILS**

| Item | Price per 1 hour |
| - | - |
| Managed MLflow on Non-GPU Intel Ice Lake. CPU | ₪0.093 |
| Managed MLflow on Non-GPU Intel Ice Lake. RAM | ₪0.02325 |

#### Non-GPU AMD EPYC Genoa

The platform is available in the `eu-north1`, `me-west1`, `us-central1`, `uk-south1` and `eu-west2` [regions](https://docs.nebius.com/overview/regions.md).

**USD**

| Item | Price per 1 hour |
| - | - |
| Managed MLflow on Non-GPU AMD EPYC Genoa. CPU | \$0.03 |
| Managed MLflow on Non-GPU AMD EPYC Genoa. RAM | \$0.0075 |

**ILS**

| Item | Price per 1 hour |
| - | - |
| Managed MLflow on Non-GPU AMD EPYC Genoa. CPU | ₪0.093 |
| Managed MLflow on Non-GPU AMD EPYC Genoa. RAM | ₪0.02325 |

### Internal storage (disks)

You are charged for disks in your Managed MLflow clusters. Charges are based on disk sizes, regardless of the amount of used space.

* **Billing unit**: 1 byte per 1 second
* **Pricing unit**: 1 GiB per 730 hours (2<sup>30</sup> bytes per 2,628,000 seconds \~ 1 month)

**USD**

| Item | Price per 1 GiB per 730 hours |
| - | - |
| Managed MLflow. Network SSD disk | \$0.071 |

Each Managed MLflow cluster has a 200 GiB disk. Therefore, 730 hours of storage for a cluster cost 200 × \$0.071 = \$14.20.

**ILS**

| Item | Price per 1 GiB per 730 hours |
| - | - |
| Managed MLflow. Network SSD disk | ₪0.221 |

Each Managed MLflow cluster has a 200 GiB disk. Therefore, 730 hours of storage for a cluster cost 200 × ₪0.221 = ₪44.20.

### Buckets for artifacts

You are charged for using Object Storage buckets attached to Managed MLflow clusters to store artifacts. For pricing details, see [Pricing in Object Storage](https://docs.nebius.com/object-storage/resources/pricing.md).
