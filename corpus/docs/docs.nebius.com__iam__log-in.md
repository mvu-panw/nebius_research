# How to authenticate in Nebius AI Cloud interfaces

Source: https://docs.nebius.com/iam/log-in

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to authenticate in Nebius AI Cloud interfaces

After you [sign up for Nebius AI Cloud](https://docs.nebius.com/signup-billing/sign-up.md), you can work with your resources by using the web console, CLI, Terraform provider or API.

> [!TIP]
>
> To get started with the CLI, Terraform and the API, create an [access token](https://docs.nebius.com/iam/authorization/access-tokens.md) for authentication.

## How to sign in to the web console

1. Open the [Nebius AI Cloud web console](https://console.nebius.com).
2. Select the Google, GitHub or Microsoft account that you used to sign up.

   Alternatively, click **Get started with SSO** and specify your [federation ID](https://docs.nebius.com/iam/overview.md#federations).

## How to get started with the CLI

[Install](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI and then [configure it](https://docs.nebius.com/cli/configure.md).

## How to work with Terraform

Follow the [installation instructions](https://docs.nebius.com/terraform-provider/install.md) to install and configure the Nebius AI Cloud Terraform provider.

## How to authenticate in the API

Authentication in the API depends on whether you use a service account or a user account. In both cases, you create an access token and include it in the `Authorization` HTTP header. For more information, follow the [authentication guide](https://docs.nebius.com/grpc-api/auth.md).
