# Pricing in Object Storage

Source: https://docs.nebius.com/object-storage/resources/pricing

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing in Object Storage

This article provides detailed pricing for the Object Storage service in Nebius AI Cloud.

## How charges and prices work

Each group of chargeable items in this article has two time units associated with it:

* **Billing unit**: The minimum unit of usage for which you can be charged.
* **Pricing unit**: The unit of usage for which the prices are shown.

Charges for units smaller than the pricing unit are calculated proportionally.

> For example, for GPUs on running VMs, the **billing unit** is 1 second, and the **pricing unit** is 1 hour (3600 seconds). For 30 minutes of usage, you will be charged half the hourly price.

Prices in US dollars (USD, \$) apply to all customers except for companies from Israel, where prices in Israeli shekels (ILS, ₪) apply instead.

All prices are shown without any applicable taxes, including VAT. Due to rounding errors, usage costs shown in the web console and final charges may slightly differ from calculations based on the prices in this article.

## Prices

### Storing data

You are charged for storing data in your Object Storage buckets. Pricing depends on the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) of a stored object.

* **Billing unit**: 1 byte per 1 second
* **Pricing unit**: 1 GiB per 730 hours (2<sup>30</sup> bytes per 2,628,000 seconds \~ 1 month)

**USD**

| Item | Price per 1 GiB per 730 hours |
| - | - |
| Used space in Standard storage | \$0.0147 |
| Used space in Enhanced Throughput storage | \$0.11 |
| Used space in Intelligent storage, Warm tier | \$0.03 |
| Used space in Intelligent storage, Cold tier | \$0.01 |

**ILS**

| Item | Price per 1 GiB per 730 hours |
| - | - |
| Used space in Standard storage | ₪0.046 |
| Used space in Enhanced Throughput storage | ₪0.341 |
| Used space in Intelligent storage, Warm tier | ₪0.093 |
| Used space in Intelligent storage, Cold tier | ₪0.031 |

### HTTP requests on data

You are charged for performing HTTP requests on objects in your Object Storage buckets. Pricing depends on the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) of an object on which you perform requests.

All requests are divided into two classes by their HTTP method. A request using any method in a class counts towards the billing item for the class.

> For example, when 5 PUT requests and 5 DELETE requests are made, this adds 10 requests total to the PUT, POST and DELETE item.

You are not charged for requests on buckets (for example, requests that create or delete buckets, change bucket settings or list objects).

* **Billing unit**: 1 request
* **Pricing unit**: 1000 requests

**USD**

| Item | Price per 1000 requests |
| - | - |
| Standard storage — class A operations (PUT, POST, DELETE) | \$0.0034 |
| Standard storage — class B operations (GET, HEAD) | \$0.00028 |
| Enhanced Throughput storage — class A operations (PUT, POST, DELETE) | Free |
| Enhanced Throughput storage — class B operations (GET, HEAD) | Free |
| Intelligent storage — class A operations (PUT, POST, DELETE) | Free |
| Intelligent storage — class B operations (GET, HEAD) | Free |

**ILS**

| Item | Price per 1000 requests |
| - | - |
| Standard storage — class A operations (PUT, POST, DELETE) | ₪0.01054 |
| Standard storage — class B operations (GET, HEAD) | ₪0.000868 |
| Enhanced Throughput storage — class A operations (PUT, POST, DELETE) | Free |
| Enhanced Throughput storage — class B operations (GET, HEAD) | Free |
| Intelligent storage — class A operations (PUT, POST, DELETE) | Free |
| Intelligent storage — class B operations (GET, HEAD) | Free |

### Egress traffic

You are charged for egress traffic from your Object Storage buckets, that is, traffic to the internet and traffic to another [region](https://docs.nebius.com/overview/regions.md). Pricing depends on the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) of an object.

* **Billing unit**: 1 byte
* **Pricing unit**: 1 GiB (2<sup>30</sup> bytes)

**USD**

| Item | Price per 1 GiB |
| - | - |
| Egress traffic from Standard storage to the internet or another region in Nebius AI Cloud | \$0.015 |
| Egress traffic from Enhanced Throughput storage to the internet or another region in Nebius AI Cloud | Free |
| Egress traffic within the same Nebius AI Cloud region | Free |

**ILS**

| Item | Price per 1 GiB |
| - | - |
| Egress traffic from Standard storage to the internet or another region in Nebius AI Cloud | ₪0.0465 |
| Egress traffic from Enhanced Throughput storage to the internet or another region in Nebius AI Cloud | Free |
| Egress traffic within the same Nebius AI Cloud region | Free |

#### Egress traffic from the Intelligent storage class

For Intelligent storage class, free egress traffic is limited to three times the customer's monthly average used storage capacity. If this limit is exceeded, Nebius may limit read and write bandwidth and/or apply charges according to Object Storage pricing.

> For example, if the monthly average used storage capacity is 1 TiB and egress traffic took more than 3 TiB, the read and write bandwidth may become limited, and charges for the egress traffic may apply.

* **Billing unit**: 1 byte
* **Pricing unit**: 1 GiB (2<sup>30</sup> bytes)

**USD**

| Item | Price per 1 GiB |
| - | - |
| Egress traffic from Intelligent storage, less than 3x the monthly average used storage capacity | Free |
| Egress traffic from Intelligent storage, more than or equal to 3x the monthly average used storage capacity | \$0.05 |

**ILS**

| Item | Price per 1 GiB |
| - | - |
| Egress traffic from Intelligent storage, less than 3x the monthly average used storage capacity | Free |
| Egress traffic from Intelligent storage, more than or equal to 3x the monthly average used storage capacity | ₪0.155 |
