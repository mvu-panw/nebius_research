# Subscriptions in Nebius AI Cloud

Source: https://docs.nebius.com/overview/subscriptions

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Subscriptions in Nebius AI Cloud

You can subscribe to platform notifications about Nebius AI Cloud resources, billing events or support tickets. Each subscription type includes different notifications, and you can [subscribe](https://console.nebius.com/notify/subscriptions) to each type by using various emails.

For more information about how to manage subscriptions, see [Manage subscriptions](https://docs.nebius.com/overview/subscriptions/manage-subscriptions.md).

## Tenant subscription

With a tenant subscription, you receive notifications related to your tenant and projects. They include, for example, notifications about planned maintenance for resources in the project.

A tenant subscription is a top-level subscription. When you subscribe to tenant notifications, you also automatically get billing and support notifications unless you create dedicated subscriptions for them.

Once you subscribe to tenant notifications, you cannot disable them unless someone else in your tenant is subscribed.

> [!NOTE]
>
> If you use tenant contacts for your subscription, make sure your email server allows notifications from Nebius. They can be treated as external emails. For more information, see [Tenant contacts](https://docs.nebius.com/overview/contacts/index.md#tenant-contacts).

## Billing subscription

With a billing subscription, you receive alerts related to invoices, payment reminders and account balance updates.

Once you subscribe to billing notifications:

* You cannot disable them unless someone else in your tenant is subscribed.
* All tenant subscriptions no longer receive notifications related to billing.

## Support subscription

With a support subscription, you receive notifications about your support tickets. You are prompted to subscribe for notifications when you create a ticket. You are also notified about tickets that the Nebius support team created on your behalf.

If you unsubscribe from support notifications, you stop receiving updates about support tickets.

## Impact on subscriptions if a user is removed from a tenant

If the user loses their rights in a tenant, this can affect their subscriptions, depending on a given use case.

| Use case | Result |
| - | - |
| Subscriptions have both [personal](https://docs.nebius.com/overview/contacts/index.md#personal-contacts) and [tenant contacts](https://docs.nebius.com/overview/contacts/index.md#tenant-contacts). | Notifications will be sent to the tenant contacts and personal contacts of other active users. Nebius AI Cloud will not send notifications to the personal contacts of the user who has lost their rights in a tenant. |
| Subscriptions have only tenant contacts. | Notifications will continue to come because tenant contacts are associated with a tenant, not a user account. |
| Subscriptions only have personal contacts of the users who lose their rights in the tenant. | Notifications will not be sent to any contact. |
