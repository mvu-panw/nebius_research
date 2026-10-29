# Pay-as-you-go (PAYG) in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/billing-models/payg

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pay-as-you-go (PAYG) in Nebius AI Cloud

*Pay-as-you-go (PAYG)* is a Nebius AI Cloud [billing model](https://docs.nebius.com/signup-billing/billing-models/overview.md) where billing is based on actual resource usage. This model is best suited for users who need cost-effective flexibility without long-term commitments, though you can still opt for the [commitment discounts model](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md) for certain workloads and save money.

## What is billed under PAYG

You are billed for the resources that you use, based on how long or how much you use them.

> For example, you can be billed for computing resources of your Compute virtual machine (VM) that was running for 6 hours, or for storing 300 GiB of data in Object Storage buckets for 5 days.

Resource usage and its costs are tracked in real time by your *PAYG balance*. The [Billing](https://console.nebius.com/billing) section in the web console shows your current balance; usage details are in the **Billing** → **Usage** section.

The PAYG model does not apply to resources that are free of charge or are included in your commitments.

## PAYG prices

Current PAYG prices are shown on the **Billing** → **Payments** → **List prices** tab in the web console. You can also see them in the documentation of paid services:

* [Compute](https://docs.nebius.com/compute/resources/pricing.md) (pricing also applies to [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/resources/pricing.md) and [Serverless AI](https://docs.nebius.com/serverless/pricing-quotas.md))
* [Object Storage](https://docs.nebius.com/object-storage/resources/pricing.md)
* [Managed Service for MLflow](https://docs.nebius.com/mlflow/resources/pricing.md)
* [Managed Service for PostgreSQL®](https://docs.nebius.com/postgresql/resources/pricing.md)
* [Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/managed-soperator/pricing-quotas)

Spot prices for preemptible VM capacity can change over time. You can view spot prices and create pricing policies in the web console. For more information, see [Spot pricing and pricing policies](https://docs.nebius.com/signup-billing/pricing-policy.md).

The following services are provided free of charge:

* Container Registry
* Virtual Networks
* Audit Logs (in [preview](https://docs.nebius.com/overview/services.md#service-and-application-stages))
* SecretStash (in preview)
* Monitoring (in preview)
* Logging (in preview)

Services that are in preview may become paid when they are launched into general availability.

## Paying for PAYG usage

### By bank card

If your payment method is [bank card](https://docs.nebius.com/signup-billing/payments/card.md), you can [top up your PAYG balance manually](https://docs.nebius.com/signup-billing/payments/card.md#topping-up-your-payg-balance) with your card.

We will also automatically charge your card for your PAYG usage:

* At the beginning of each month, if your PAYG balance is negative on its first day.
* When your balance reaches the [threshold](https://docs.nebius.com/signup-billing/payments/threshold.md).

The charge amount brings your balance to zero.

> [!TIP]
>
> To avoid unexpected charges, we recommend that you top up your balance from time to time to keep it positive.

### By bank transfer

If your payment method is [bank transfers](https://docs.nebius.com/signup-billing/payments/bank-transfers.md), you can top up your PAYG balance manually. To do that, request a proforma invoice from the Nebius sales team.

We will also send you an [invoice](https://docs.nebius.com/signup-billing/payments/invoices.md#invoices) for the month's PAYG usage at the beginning of the following month. If your PAYG balance was negative at the end of the previous month, you will need to pay the invoice, using the details contained in it.

## How to stop being charged

If you no longer need a resource, delete it to stop incurring charges. For details on how to delete resources for each chargeable service, see the following instructions:

* **Compute**:
  * [Delete a virtual machine](https://docs.nebius.com/compute/virtual-machines/delete.md)
  * [Delete a volume](https://docs.nebius.com/compute/storage/manage.md#how-to-delete-a-volume)
* **Managed Service for Soperator**: [Delete a cluster](https://docs.nebius.com/slurm-soperator/managed-soperator/manage.md#how-to-delete-a-cluster)
* **Managed Service for Kubernetes**:
  * [Delete a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-delete-clusters)
  * [Delete node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-delete-node-groups)
* **Object Storage**: [Delete a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets)
* **Managed Service for PostgreSQL**: [Delete a cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-delete-clusters)
* **Serverless AI**:
  * [Delete a Devlab](https://docs.nebius.com/serverless/devlabs/manage.md#how-to-delete-a-devlab)
  * [Delete an endpoint](https://docs.nebius.com/serverless/endpoints/manage.md#how-to-delete-an-endpoint)
  * [Delete a job](https://docs.nebius.com/serverless/jobs/manage.md#how-to-delete-a-job)
* **Managed Service for MLflow**: [Delete a cluster](https://docs.nebius.com/mlflow/clusters/delete.md)

> [!NOTE]
>
> If a VM is stopped, you don't pay for its computing resources, but you are still charged for its storage volumes. If you don't need these volumes, delete them to stop being charged.

## See also

* [Viewing PAYG usage](https://docs.nebius.com/signup-billing/usage/view.md#how-to-view-payg-usage)
* [Exporting usage data in the CSV format](https://docs.nebius.com/signup-billing/usage/export.md)

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
