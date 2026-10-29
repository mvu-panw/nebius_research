# Contacts in Nebius AI Cloud

Source: https://docs.nebius.com/overview/contacts

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Contacts in Nebius AI Cloud

A contact is an email address or phone number used to receive notifications on [subscriptions](https://docs.nebius.com/overview/subscriptions/index.md). Add your contacts to Nebius AI Cloud to receive updates about your resources, billing, maintenance and other critical events.

For more information about how to manage contacts, see [Manage contacts](https://docs.nebius.com/overview/contacts/manage-contacts.md).

## Contact types

Nebius AI Cloud supports two types of contacts:

* [Personal contacts](#personal-contacts): associated with your account and can be used across multiple tenants
* [Tenant contacts](#tenant-contacts): associated with a specific tenant and available only within this tenant

### Personal contacts

Personal contacts are email addresses or phone numbers that are associated with your account. Only you have access to your personal contacts. Their list does not change if you switch a tenant.

You can use personal contacts to [subscribe](https://docs.nebius.com/overview/subscriptions/manage-subscriptions.md) to notifications within any tenant where you have sufficient permissions for receiving notifications.

The first personal contact with your email is created automatically when you [sign up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud. After that, you can [create additional contacts](https://docs.nebius.com/overview/contacts/manage-contacts.md#how-to-create-a-contact).

### Tenant contacts

Tenant contacts are shared email boxes or mailing lists that are associated with a specific tenant. For example, you can use an email such as `administrators@example.com`, so all authorized users can access notifications sent to this email.

Only tenant administrators have access to tenant contacts.

Use tenant contacts for [tenant and billing subscriptions](https://docs.nebius.com/overview/subscriptions/index.md). For example, you can add a shared accounting email as a tenant contact to the billing subscription, so the accounting team receives notifications about billing. Alternatively, you can subscribe an engineering mailing list to tenant notifications, so an engineering team does not miss news about maintenance.

Tenant contacts are not associated with any specific user account. As tenant contacts are associated with a tenant, you can only access them within a given tenant.

> [!NOTE]
>
> If a tenant contact contains a shared email box or mailing list, emails from Nebius may be treated as external by your email server. To avoid missing notifications, configure your email server or client to allow notifications from Nebius. For example, if you use Microsoft 365, [create an allowlist](https://learn.microsoft.com/en-us/defender-office-365/create-safe-sender-lists-in-office-365) for trusted senders.
