# Budgets in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/budgets

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Budgets in Nebius AI Cloud

A *budget* tracks your [pay-as-you-go](https://docs.nebius.com/signup-billing/billing-models/payg.md) spending against a threshold you set over a recurring period and sends email alerts when your spending crosses it. Use a budget to monitor costs for your whole account or a specific part of it and to avoid overspending.

A budget does not stop or cap your usage. Budget usage data updates every few hours, so an alert can arrive after your spending has passed an alert threshold. Set a low threshold to have time to react. To limit usage, you can [request a quota decrease](https://docs.nebius.com/overview/quotas.md).

Budget amounts and tracked spending exclude VAT.

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create a budget

1. In the [web console](https://console.nebius.com/), go to  [Billing](https://console.nebius.com/billing) → **Budgets**.

2. Click **Create budget**.

3. In **Details and scope**, specify:

   * **Name**: Enter a name for the budget.
   * **Time period**: Select **Daily**, **Monthly**, **Quarterly** or **Yearly**. Each period starts at 00:00 UTC and is aligned to the calendar — a monthly budget resets on the first of each month, a quarterly one on January 1, April 1, July 1 and October 1, and a yearly one on January 1.
   * **Scope**: Select **All usage** to track your entire pay-as-you-go spending, or **Conditions** to limit the budget to specific usage.

     You can add a condition on a **Region**, **Project**, **Service** or **Product**. With several conditions selected, the budget counts only the usage that matches all of them. See [Example budget scopes](#example-budget-scopes) for quick tips on configuration.

4. In **Amount and alerts**, set the budget **Amount**. The form suggests an amount based on your recent spending for the chosen scope. Choose whether to express your alert thresholds as a percentage of the amount or as an absolute value, then add one or more thresholds in that unit.

   An alert is sent when your actual recorded spending crosses an alert threshold. Budgets do not alert on forecasted spending. To get an early warning, add a low threshold (for example, 50%) in addition to a 100% one.

5. In **Notifications**, select the recipients of the alert emails. To add a recipient that isn't listed, click **Add email**, choose a contact type and click **Continue**:

   * [Tenant contact](https://docs.nebius.com/overview/contacts/index.md#tenant-contacts): a shared mailbox that only tenant administrators manage. Recommended for billing notifications such as budget alerts.
   * [Personal contact](https://docs.nebius.com/overview/contacts/index.md#personal-contacts): an email linked to your Nebius account that only you can access.

   If you add no recipient, the budget still tracks usage but sends no alerts.

6. In **Review**, check the final configuration and click **Create budget**.

Review your budgets from time to time. If your spending grows or your projects change, the configured amounts can make alerts too frequent or too rare.

> **Example budget scopes**
>
> You can combine several budgets, each for its own task:
>
> * **Whole account**: a monthly budget that tracks **All usage**, with the amount set to your expected monthly spending. Use it to catch overspending regardless of its source.
> * **Team or project**: a budget with a **Project** condition that selects one or several projects of a specific team, with alert recipients from that team. Create one budget per team to see which team overspends.
> * **Specific products**: a budget with a **Product** condition that selects your most expensive products — for example, GPUs. To narrow the scope, combine conditions: **Project** and **Product** conditions together track the GPU spending of one team.

## How to check a budget status

In the [web console](https://console.nebius.com/), go to  [Billing](https://console.nebius.com/billing) → **Budgets**.

* The **Budgets** page shows current usage against each budget's amount, period and alert thresholds. Select a budget to see its scope and alert recipients.
* When you receive an alert, go to the [Usage](https://docs.nebius.com/signup-billing/usage/view.md) page and filter by the budget's scope to see which projects, services or resources cause the spending. Then top up your balance if you expect this spending, or [delete the resources](https://docs.nebius.com/signup-billing/billing-models/payg.md#how-to-stop-being-charged) you no longer need.

## How to edit a budget

1. In the [web console](https://console.nebius.com/), go to  [Billing](https://console.nebius.com/billing) → **Budgets**.
2. In the budget's row, click  → **Edit**. You can also edit a budget from its page.

   The wizard reopens with all the steps from [How to create a budget](#how-to-create-a-budget). Every field is editable, including the time period and scope.

## How to delete a budget

1. In the [web console](https://console.nebius.com/), go to  [Billing](https://console.nebius.com/billing) → **Budgets**.
2. In the budget's row, click  → **Delete**. You can also delete a budget from its page.

   Deleting a budget stops its alerts.

## See also

* [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md)
