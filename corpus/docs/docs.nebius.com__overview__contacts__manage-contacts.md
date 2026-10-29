# How to manage contacts in Nebius AI Cloud

Source: https://docs.nebius.com/overview/contacts/manage-contacts

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage contacts in Nebius AI Cloud

Nebius AI Cloud supports two types of contacts:

* [Personal contacts](https://docs.nebius.com/overview/contacts/index.md#personal-contacts) are associated with your account and can be used across multiple tenants where you have sufficient permissions.
* [Tenant contacts](https://docs.nebius.com/overview/contacts/index.md#tenant-contacts) are non-personal contacts associated with a specific tenant and can only be used within this tenant.

> [!NOTE]
>
> Only tenant administrators can access and manage tenant contacts.

## How to open contacts

**Web console**

1. In the sidebar, go to  **Administration** → **Notification settings**.
2. On the page that opens, go to the required tab: **Personal contacts** or **Tenant contacts**.

The personal contact list contains all the emails and phone numbers that you have added to Nebius AI Cloud and that are associated with your account.

As personal contacts are shared between tenants you have access to, switching tenants does not affect the list of personal contacts.

The tenant contact list contains all the shared email boxes and mailing lists that have been added to Nebius AI Cloud. As tenant contacts are associated with a tenant, a list of displayed contacts depends on the tenant that you have selected.

## How to create a contact

You can add an email to personal or tenant contacts, or a phone number to personal contacts. To do so:

1. [Open the contacts](#how-to-open-contacts).

2. Click **Add email** or **Add phone number**, depending on what contact you would like to add.

3. In the window that opens, enter the required contact and click **Send code**.

   A verification code is sent to the specified email or phone number.

4. Enter the received code and click **Confirm**.

After you create a contact, you can [sign it up for subscriptions](https://docs.nebius.com/overview/subscriptions/manage-subscriptions.md#how-to-subscribe-to-notifications).

## How to verify a contact

If you added a contact and did not enter a verification code for it, you can let Nebius AI Cloud verify this contact independently:

1. [Open the contacts](#how-to-open-contacts).

2. In the line of the contact with the **Not Verified** label, click **Resend verification code**.

   A verification code is sent to the selected email or phone number.

3. In Nebius AI Cloud, enter the received code and click **Confirm**.

## How to remove a contact

> [!WARNING]
>
> You cannot unsubscribe from [tenant and billing notifications](https://docs.nebius.com/overview/subscriptions/index.md) if nobody else in your tenant receives them. Ask someone in your tenant to subscribe before you remove your contacts.

To remove a contact:

1. [Open the contacts](#how-to-open-contacts).
2. In the line of the required contact, click  → **Remove contact**.
3. In the window that opens, perform the following actions:

   * If the contact has no active subscriptions, confirm that you want to remove the contact.
   * If the contact has at least one active subscription, either select a replacement contact for active subscriptions and then click **Remove and replace contact**, or click **Only remove contact** to proceed without replacing the contact.

     If you are removing a tenant contact, we recommend replacing it with another tenant contact. If you replace it with a personal contact, other tenant administrators will not be able to manage subscriptions of this contact and can miss important notifications about the tenant.
