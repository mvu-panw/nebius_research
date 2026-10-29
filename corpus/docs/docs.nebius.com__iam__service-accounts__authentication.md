# How to authenticate as a service account

Source: https://docs.nebius.com/iam/service-accounts/authentication

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to authenticate as a service account

When a service account interacts with a resource in Nebius AI Cloud, IAM checks if it has access rights to perform the operation. Authenticated service accounts are given permissions based on their group memberships.

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to authenticate as a service account

To authenticate in a service as a service account:

1. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#creating-a-service-account).

2. Create authentication keys for the service account:

   * [Authorized keys](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) to authenticate in the Nebius AI Cloud CLI or Terraform provider.
   * [Access keys](https://docs.nebius.com/iam/service-accounts/access-keys.md) to authenticate in services with AWS-compatible APIs, such as Object Storage.

3. Configure the interface that will use the created keys:
   * [Nebius AI Cloud CLI configuration](https://docs.nebius.com/cli/configure.md)
   * [Nebius AI Cloud CLI configuration in environments without a browser](https://docs.nebius.com/cli/no-browser.md)
   * [Terraform provider authentication](https://docs.nebius.com/terraform-provider/authentication.md)
   * [AWS CLI configuration](https://docs.nebius.com/object-storage/quickstart.md)
