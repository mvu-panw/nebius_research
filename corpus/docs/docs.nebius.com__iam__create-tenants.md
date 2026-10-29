# Creating a tenant in Nebius AI Cloud

Source: https://docs.nebius.com/iam/create-tenants

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating a tenant in Nebius AI Cloud

When you sign up for Nebius AI Cloud, the platform creates a [tenant](https://docs.nebius.com/iam/overview.md#tenants) for you automatically. After the sign-up, you can create additional tenants regardless of whether you have access to any tenants or not. As a result, you can work in an isolated environment with dedicated billing.

## Prerequisites

1. Do not use [single sign-on](https://docs.nebius.com/iam/federations/saml-sso.md) (SSO) when you register and log in. Users who use this type of authentication cannot create tenants.
2. [Sign up for Nebius AI Cloud](https://docs.nebius.com/signup-billing/sign-up.md) if you have not done so yet.
3. If you have access to ten or more tenants, [contact technical support](https://console.nebius.com/support/create-ticket) and ask them to grant you access for creating an additional tenant.

   If you have ten or more tenants, by default you cannot create one more tenant. First, you need to request access rights for this. After that, you can proceed to the creation process as usual.

   This limitation does not apply to tenant invitations. If you are invited, for example, to the eleventh tenant, you can accept the invitation and be added to this tenant.

## How to create a tenant

**Web console**

1. If you have access to a tenant, expand the list of tenants and then click  **Create tenant**.

   If you do not have access to any tenant, click  **Create tenant**. If an error is displayed and the **Create tenant** button is missing, you might have logged in by using SSO, or you have reached the limit on the number of tenants.

2. In the window that opens, specify the following:

   * **Prefix** that is added to the tenant name. Nebius AI Cloud generates a random and unique name. You can customize it and add a prefix.

     After the tenant is created, you can [rename](https://docs.nebius.com/iam/rename-tenants.md) it.

   * **Email** that Nebius AI Cloud uses to send notifications about the new tenant, its projects and maintenance of services. The specified email becomes your personal contact within this new tenant.

     > [!WARNING]
     >
     > A tenant must have at least one email subscribed to its notifications, so an email is required.

     For more information, see [Contacts in Nebius AI Cloud](https://docs.nebius.com/overview/contacts/index.md).

3. Click **Create tenant**.

After that, Nebius AI Cloud creates a tenant and a [project](https://docs.nebius.com/iam/overview.md#projects) per [region](https://docs.nebius.com/overview/regions.md) in it.

If you receive an error stating that a [tenant subscription](https://docs.nebius.com/overview/subscriptions/index.md#tenant-subscription) is not created, manually subscribe a contact to tenant notifications via the [Administration → Notification settings](https://console.nebius.com/notify) section of the web console. For more information, see [How to subscribe to notifications](https://docs.nebius.com/overview/subscriptions/manage-subscriptions.md#how-to-subscribe-to-notifications).
