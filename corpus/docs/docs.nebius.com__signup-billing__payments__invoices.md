# How to read invoices and proforma invoices

Source: https://docs.nebius.com/signup-billing/payments/invoices

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to read invoices and proforma invoices

An *invoice* is a fiscal document that serves as the primary record of consumption and payment for the used services.

A *proforma invoice* is not a fiscal document. It provides details for a bank transfer and serves as a formal document to facilitate advance payment.

Invoices and proforma invoices are issued in the currency set for your account, which is usually USD or EUR.

Nebius displays invoices and proforma invoices in the web console and also sends them to the email address specified in your [billing subscription](https://docs.nebius.com/overview/subscriptions/index.md#billing-subscription). While you cannot change the dates on which invoices and proforma invoices are sent, you can [manage your subscription](https://docs.nebius.com/overview/subscriptions/manage-subscriptions.md) and update the email address to which invoices are sent.

## Invoices

An *invoice* is a document with charges for the billing period.

### Issuing invoices

Regular invoices are issued either monthly or immediately after payment, depending on the type of usage:

* ***[PAYG](https://docs.nebius.com/signup-billing/billing-models/payg.md)***

  Issued monthly and contain details of the previous month's usage. The exact timing may vary slightly, but you should receive the invoice no later than the 15th day of the next month (in accordance with [Dutch VAT rules](https://vat-one-stop-shop.ec.europa.eu/national-vat-rules/netherlands-vat-rules_en)). For example, if your usage is from September, you will receive the invoice in the first half of October.

  In some cases, if the system detects late usage reporting at the end of the month, some charges may be carried over into the next billing cycle. This means that your invoice may include charges from both the current and previous months.

* ***[Commitment discounts](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md)***

  If you make a prepayment, your invoice will be issued immediately after we process your payment. The exact processing timing may vary slightly, but you should receive the invoice within a few business days after you made a payment.

### Invoice contents

An invoice consists of the following parts:

* Consumption amount: the total amount of usage for the reporting period.
* Invoice details: invoice number, your billing address and contact information.
* VAT, if applicable (for details about it, see [Taxes](https://docs.nebius.com/signup-billing/payments/taxes.md)).

To view detailed resource usage information, go to **Billing** → **Usage** in the web console.

### How to access invoices

All invoices are issued in PDF format. To view and download invoices, go to **Billing** → **Payments** → **Documents** in the web console.

Invoices are also sent to your email address either automatically (pay-as-you-go invoices) or manually (commitment discounts invoices).

## Proforma invoices

To pay in advance by bank transfer, you need a *proforma invoice* provided by Nebius. The proforma invoice contains:

* Payment details for a bank transfer (IBAN, BIC and other details).
* Invoice number, VAT ID, your billing address and contact information.
* Payment due date.
* Type of resources to pay for.
* Total cost of services to be paid (both with and without taxes).
* VAT, if applicable (for details about it, see [Taxes](https://docs.nebius.com/signup-billing/payments/taxes.md)).

Nebius issues proforma invoices at the beginning of the usage period and at your request.

Proforma invoices are issued in PDF format. To view and download them, go to **Billing** → **Payments** → **Documents** in the web console.

Nebius also sends proforma invoices to your email address. Since proforma invoices are different from [invoices](#invoices), they are sent separately at different times.
