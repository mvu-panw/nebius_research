# Commitment discounts in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/billing-models/committed-usage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Commitment discounts in Nebius AI Cloud

*Commitment discounts* are a Nebius AI Cloud [billing model](https://docs.nebius.com/signup-billing/billing-models/overview.md) that allows you to get discounts on [pay-as-you-go](https://docs.nebius.com/signup-billing/billing-models/payg.md) prices by committing to specific usage for a set time period. If you intend to run long-term, stable workloads in Nebius AI Cloud, commitment discounts might help you save money. All usage that is not covered by the discounts is billed as pay-as-you-go (PAYG).

The commitment discounts model is only available if you have signed up for Nebius AI Cloud as a company.

Commitment discounts are grouped in *orders* in the web console. An order represents your addendum and has the same ID as your addendum number. You can see order IDs on the **Commitment discounts** page (**Billing** → **Discounts** → **Commitment discounts**) in the web console.

## What is billed in the commitment discounts

Commitment discounts include the types of resources you are going to use (chosen from [eligible types](#resource-types-eligible-for-the-commitment-discounts)), how much of them and for how long.

> For example, you can commit to 365 days of running 64 VMs, each with 8 NVIDIA® H100 GPUs, 128 vCPUs and 1600 GiB of RAM, and using a 128 TiB SSD shared filesystem.

All paid resources that are not included in your commitment discounts are billed under PAYG.

## Resource types eligible for the commitment discounts

Nebius AI Cloud resources of the following types can be included in the commitment discounts:

* Computing resources (GPUs, vCPUs, RAM) in Compute [VM platforms](https://docs.nebius.com/compute/virtual-machines/types.md)
* Disks and shared filesystems

## Paying for the commitment

You will be charged for the entire commitment on the dates agreed upon with the Nebius sales team. Generally, the commitment discounts are prepaid.

The charge is made by using your selected payment method: [bank card](https://docs.nebius.com/signup-billing/payments/card.md) or [bank transfers](https://docs.nebius.com/signup-billing/payments/bank-transfers.md).

> [!TIP]
>
> You can track invoices and ensure timely payment under **Billing** → **Payments** → **Documents** in the web console.

## How to apply for commitment discounts

To take advantage of the commitment discounts, you need to [sign up for Nebius AI Cloud](https://docs.nebius.com/signup-billing/sign-up.md) as a company. During or after signup, follow these steps:

1. [Contact the Nebius sales team](https://nebius.com/prices#ai-contact-form) to arrange your commitment discounts.
2. Make a payment as agreed with the sales team.
3. Create resources that are included in your commitment discounts, for example, Compute VMs. Their usage will be automatically excluded from PAYG billing and will not be reflected in your PAYG balance.

## How to change your commitment discounts

If you want to change your commitment discounts, for example, extend, shorten or cancel them, the following conditions apply:

* **Extending the discounts** is subject to the available capacity at the time of the request.
* **Shortening or canceling the discounts** can only be done if allowed by the terms of your addendum and in accordance with it. Nebius AI Cloud reserves the right to refuse requests to cancel or shorten your discounts. Fees or changes to the original discounts may also apply based on the addendum terms.

To request changes to your commitment discounts, [contact the Nebius sales team](https://nebius.com/prices#ai-contact-form).

## How to stop being charged for resources outside your commitment

All resources not covered by your commitment discounts are billed under [PAYG](https://docs.nebius.com/signup-billing/billing-models/payg.md). If you no longer need these resources, delete them to stop incurring additional charges. For instructions on how to delete resources for each service, see [How to stop being charged](https://docs.nebius.com/signup-billing/billing-models/payg.md#how-to-stop-being-charged) for PAYG.

## See also

* [Viewing commitment discounts](https://docs.nebius.com/signup-billing/usage/view.md#how-to-view-commitment-discounts)
* [Exporting usage data in the CSV format](https://docs.nebius.com/signup-billing/usage/export.md)
