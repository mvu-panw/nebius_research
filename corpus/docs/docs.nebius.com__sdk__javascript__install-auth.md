# Installation and authentication with the Nebius AI Cloud SDK for JavaScript

Source: https://docs.nebius.com/sdk/javascript/install-auth

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Installation and authentication with the Nebius AI Cloud SDK for JavaScript

Use the SDK for JavaScript to work with Nebius AI Cloud resources from JavaScript applications.

Install the SDK and initialize it with authentication credentials to [send API requests](https://docs.nebius.com/sdk/javascript/send-request.md).

For documentation, see:

* [Nebius AI Cloud repository for the JavaScript SDK](https://github.com/nebius/js-sdk)
* [JavaScript SDK reference](https://nebius.github.io/js-sdk/)

## Supported Node.js versions

The SDK supports Node.js 22, 24 and 25.

## Installation and update

Install the SDK package:

```bash theme={null}
npm install @nebius/js-sdk
```

If you installed the SDK earlier, update it to the latest version:

```bash theme={null}
npm install @nebius/js-sdk@latest
```

## Initialization and authentication

For server-to-server communication, use a [service account](https://docs.nebius.com/iam/overview.md#accounts-and-members) to authenticate SDK requests. The SDK uses the service account credentials to generate a JSON Web Token, exchange it for an IAM token and refresh the IAM token in the background.

> [!NOTE]
>
> For local usage, authenticate SDK requests by using an IAM token, CLI configuration or service account credentials. For more information, see the [JavaScript SDK repository](https://github.com/nebius/js-sdk#initialize-the-sdk).

1. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#creating-a-service-account) and [add it to a group](https://docs.nebius.com/iam/authorization/groups/members.md#adding-a-service-account) that has the [roles](https://docs.nebius.com/iam/authorization/roles.md) needed for your operations. Usually, this means adding it to at least the default `editors` group.

2. Generate an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) and create a service account credentials file:

   ```bash theme={null}
   nebius iam auth-public-key generate \
     --service-account-id <service_account_ID> \
     --output <credentials_file_path>
   ```

   In the command, set the following parameters:

   * `--service-account-id`: ID of your service account.
   * `--output`: Path to the service account credentials file, for example, `credentials.json`.

3. Initialize the SDK with the service account credentials file:

   ```javascript theme={null}
   import { SDK } from '@nebius/js-sdk';
   import { CredentialsFileReader } from '@nebius/js-sdk/runtime/service_account/credentials_file';

   const sdk = new SDK({
     userAgentPrefix: '<application_name>/<application_version_or_comment>',
     parentId: '<project_ID>',
     credentials: new CredentialsFileReader('<credentials_file_path>'),
   });

   await sdk.close();
   ```

   In the script, set the following parameters:

   * `<application_name>/<application_version_or_comment>`: Application or library that calls the SDK. The version or comment is optional.
   * `<project_ID>`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
   * `<credentials_file_path>`: Path to the service account credentials file.

   The `SDK` constructor initializes the SDK and uses the service account credentials file to authenticate requests.

   The `userAgentPrefix` argument adds a prefix to the [User-Agent header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent) sent with each request. Use `userAgentPrefix` to identify your application in the list of requests.

## What's next

[Send an API request using the JavaScript SDK](https://docs.nebius.com/sdk/javascript/send-request.md).
