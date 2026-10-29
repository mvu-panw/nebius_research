# Installation and authentication with the Nebius AI Cloud SDK for Go

Source: https://docs.nebius.com/sdk/go/install-auth

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Installation and authentication with the Nebius AI Cloud SDK for Go

Use the SDK for Go to work with Nebius AI Cloud resources from Go applications.

Install the SDK and initialize it with authentication credentials to [send API requests](https://docs.nebius.com/sdk/go/send-request.md).

For documentation, see:

* [Nebius AI Cloud repository for the Go SDK](https://github.com/nebius/gosdk)
* [Go SDK reference](https://pkg.go.dev/github.com/nebius/gosdk)

## Supported Go versions

The SDK supports Go 1.24 and later. New SDK versions include breaking changes in the underlying libraries.

If your project uses an earlier SDK version, pin the dependency to `~v0.1,<v0.2` in your `go.mod` file.

## Installation and update

Install the SDK package:

```bash theme={null}
go get github.com/nebius/gosdk
```

If you installed the SDK earlier, update it to the latest version:

```bash theme={null}
go get -u github.com/nebius/gosdk
```

## Initialization and authentication

For server-to-server communication, use a [service account](https://docs.nebius.com/iam/overview.md#accounts-and-members) to authenticate SDK requests. The SDK uses the service account credentials to generate a JSON Web Token, exchange it for an IAM token and refresh the IAM token in the background.

> [!NOTE]
>
> For local usage, authenticate SDK requests by using an IAM token. For more information, see the [Go SDK repository](https://github.com/nebius/gosdk#using-an-iam-token).

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

   ```go theme={null}
   import (
      "fmt"

      "github.com/nebius/gosdk"
      "github.com/nebius/gosdk/auth"
   )

   sdk, err := gosdk.New(
      ctx,
      gosdk.WithUserAgentPrefix("<application_name>/<application_version_or_comment>"),
      gosdk.WithParentID("<project_ID>"),
      gosdk.WithCredentials(
         gosdk.ServiceAccountReader(
            auth.NewServiceAccountCredentialsFileParser(
               nil,
               "<credentials_file_path>",
            ),
         ),
      ),
   )
   if err != nil {
      return fmt.Errorf("create gosdk: %w", err)
   }
   defer sdk.Close()
   ```

   In the script, set the following parameters:

   * `<application_name>/<application_version_or_comment>`: Application or library that calls the SDK. The version or comment is optional.
   * `<project_ID>`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
   * `<credentials_file_path>`: Path to the service account credentials file.

   The `gosdk.New` constructor initializes the SDK and uses the service account credentials file to authenticate requests.

   The `WithUserAgentPrefix` method adds a prefix to the [User-Agent header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent) sent with each request. Use `WithUserAgentPrefix` to identify your application in the list of requests.

## What's next

[Send an API request using the Go SDK](https://docs.nebius.com/sdk/go/send-request.md).
