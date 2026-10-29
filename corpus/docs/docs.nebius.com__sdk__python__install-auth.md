# Installation and authentication with the Nebius AI Cloud SDK for Python

Source: https://docs.nebius.com/sdk/python/install-auth

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Installation and authentication with the Nebius AI Cloud SDK for Python

Use the SDK for Python to work with Nebius AI Cloud resources from Python applications.

Install the SDK and initialize it with authentication credentials to [send API requests](https://docs.nebius.com/sdk/python/send-request.md).

For documentation, see:

* [Nebius AI Cloud repository for the Python SDK](https://github.com/nebius/pysdk)
* [Python SDK reference](https://nebius.github.io/pysdk/apiReference.html)

## Supported Python versions

The SDK supports Python 3.10 and later.

If your project uses SDK version 0.2.x, check the migration notes in the [Python SDK repository](https://github.com/nebius/pysdk#migration-from-02x-to-03x) before updating to version 0.3.x or later.

## Installation and update

> [!TIP]
>
> Before installing the SDK, consider creating a [Python virtual environment](https://docs.python.org/3/library/venv.html) for your project to avoid dependency conflicts.

Install the SDK package:

```bash theme={null}
python3 -m pip install nebius
```

If you installed the SDK earlier, update it to the latest version:

```bash theme={null}
python3 -m pip install -U nebius
```

## Initialization and authentication

For server-to-server communication, use a [service account](https://docs.nebius.com/iam/overview.md#accounts-and-members) to authenticate SDK requests. The SDK uses the service account credentials to generate a JSON Web Token, exchange it for an IAM token and refresh the IAM token in the background.

> [!NOTE]
>
> For local usage, authenticate SDK requests by using an IAM token, CLI configuration or a credentials file. For more information, see the [Python SDK repository](https://github.com/nebius/pysdk#how-to).

1. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#creating-a-service-account) and [add it to a group](https://docs.nebius.com/iam/authorization/groups/members.md#adding-a-service-account) that has the [roles](https://docs.nebius.com/iam/authorization/roles.md) needed for your operations. Usually, this means adding it to at least the default `editors` group.

2. Create a private and public key pair:

   ```bash theme={null}
   openssl genrsa -out private.pem 4096 && \
   openssl rsa -in private.pem -outform PEM -pubout -out public.pem
   ```

   This command creates the `private.pem` and `public.pem` files in the current directory.

3. Upload the public key to create an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md):

   ```bash theme={null}
   nebius iam auth-public-key create \
     --account-service-account-id <service_account_ID> \
     --data "$(cat public.pem)"
   ```

   In the command, specify the service account ID.

4. Initialize the SDK with the private key file:

   ```python theme={null}
   from nebius.sdk import SDK

   sdk = SDK(
       user_agent_prefix="<application_name>/<application_version_or_comment>",
       parent_id="<project_ID>",
       service_account_private_key_file_name="<private_key_file_path>",
       service_account_public_key_id="<public_key_ID>",
       service_account_id="<service_account_ID>",
   )
   ```

   In the script, set the following parameters:

   * `<application_name>/<application_version_or_comment>`: Application or library that calls the SDK. The version or comment is optional.
   * `<project_ID>`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
   * `<private_key_file_path>`: Path to the private key file, for example `private.pem`.
   * `<public_key_ID>`: ID of the public key generated for the service account.
   * `<service_account_ID>`: ID of your service account.

   The `SDK` constructor initializes the SDK and uses the service account private key file to authenticate requests.

   The `user_agent_prefix` argument adds a prefix to the [User-Agent header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent) sent with each request. Use `user_agent_prefix` to identify your application in the list of requests.

## What's next

[Send an API request using the Python SDK](https://docs.nebius.com/sdk/python/send-request.md).
