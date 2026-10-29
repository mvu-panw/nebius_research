# How to set up alerts

Source: https://docs.nebius.com/observability/alerts

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to set up alerts

You can set custom alerts for virtual machines in Compute and buckets in Object Storage. Alerts notify you when resource usage crosses the specified thresholds.

To create a new alert:

1. In the [web console](https://console.nebius.com), go to  **Observability** → **Alerts**.

2. Click  **Create alert**.

3. In the window that opens, set conditions for the alert:

   * **Metric**: The metric that you want to be notified on.
   * **Handler** and **Object Type**: Additional filters for Object Storage buckets that may appear depending on **Metric**.
   * **Condition**: Choose if you want to be notified when the value exceeds or drops below the threshold.
   * **Threshold**: The value that triggers the alert.
   * **Duration**: Time during which the condition is met.

   The service, resource type and ID are filled in automatically.

4. Click **Continue**.

5. Click **Add email**, and then specify the required email. You can choose from the list that includes all emails that you have already used for [notifications](https://docs.nebius.com/overview/subscriptions/manage-subscriptions.md). If you have admin rights, you can see all contacts from your tenant in this list. If you don't have admin rights, you can see only your own contacts, even if some other user in your tenant is subscribed to the same alert.

   If you want to add a new email, verify it by using the code that the service sends to this email.

6. Click **Create alert**.

To review existing alerts:

1. In the [web console](https://console.nebius.com), go to  **Observability** → **Alerts**.
2. Click  and select one of the options to edit or delete an alert, or to change the notification email.

Alerts can have the following statuses:

* `Firing`: The alert condition is met, and the alert is active.
* `Pending`: The condition is met, but it needs to last longer before the alert becomes firing.
* `Normal`: The condition is not met, and the alert is inactive.
