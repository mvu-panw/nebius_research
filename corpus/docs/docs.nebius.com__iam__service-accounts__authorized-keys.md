# How to use authorized keys

Source: https://docs.nebius.com/iam/service-accounts/authorized-keys

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to use authorized keys

To authenticate as a service account and perform operations on its behalf, use an *authorized key pair*.

## Prerequisites

**Web console**

1. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. [Create a new service account](https://docs.nebius.com/iam/service-accounts/manage.md#web-console) if needed.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. [Create a new service account](https://docs.nebius.com/iam/service-accounts/manage.md#cli-2) if needed.

5. Get the ID of the service account for which you want to issue the key and save it to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account get-by-name \
     --name <service_account_name> \
     --format jsonpath='{.metadata.id}')
   ```

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. [Create a new service account](https://docs.nebius.com/iam/service-accounts/manage.md#terraform-2) if needed.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. [Create a new service account](https://docs.nebius.com/iam/service-accounts/manage.md#go-sdk-2) if needed.

4. Get the ID of the service account for which you want to issue the key and save it to a variable:

   ```go theme={null}
   serviceAccount, err := sdk.Services().IAM().V1().
       ServiceAccount().GetByName(
           ctx,
           &iam.GetServiceAccountByNameRequest{
               Name: "<service_account_name>",
           },
       )
   if err != nil {
       return err
   }
   serviceAccountID := serviceAccount.GetMetadata().GetId()
   if serviceAccountID == "" {
       return errors.New("service account ID is missing")
   }
   fmt.Println(serviceAccountID)
   ```

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. [Create a new service account](https://docs.nebius.com/iam/service-accounts/manage.md#python-sdk-2) if needed.

4. Get the ID of the service account for which you want to issue the key and save it to a variable:

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(name="<service_account_name>"),
   )
   service_account_id = service_account.metadata.id
   print(service_account_id)
   ```

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. [Create a new service account](https://docs.nebius.com/iam/service-accounts/manage.md#javascript-sdk-2) if needed.

4. Get the ID of the service account for which you want to issue the key and save it to a variable:

   ```ts theme={null}
   const serviceAccountService =
     new ServiceAccountService(sdk);
   const serviceAccount = await serviceAccountService.getByName(
     GetServiceAccountByNameRequest.create({
       name: "<service_account_name>",
     }),
   );
   const serviceAccountId = serviceAccount.metadata?.id;
   if (!serviceAccountId) {
     throw new Error("service account ID is missing");
   }
   console.log(serviceAccountId);
   ```

## Creating a key pair

> [!NOTE]
>
> If you are using the CLI, this step is optional. If you use the `nebius iam auth-public-key generate` command in the [next step](#uploading-the-public-key), the CLI creates the key pair for you.

Create a key pair on your local machine:

```bash theme={null}
openssl genrsa -out private.pem 4096 && \
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

This command creates the `public.pem` and `private.pem` key files in your local directory where you run the command.

## Uploading the public key

> [!NOTE]
>
> To upload an authorized key with Terraform or one of the SDKs, the provider or SDK must already be authenticated with an existing authorized key. You cannot upload the first authorized key for a service account using Terraform or an SDK. If you already have an authorized key, for example, one created with the CLI, proceed to [update the configuration](#updating-the-configuration) to use your existing authorized key with Terraform or the SDK.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM**.
2. Open the **Service accounts** tab.
3. Open the page of the required service account.
4. Click  **Upload authorized key**.
5. Click  **Attach file** and then select `public.pem`.
6. (Optional) Set an expiration date.
7. Click **Upload key**.

The key is displayed on the **Authorized keys** tab.

**CLI**

Depending on whether you already [created a key pair](#creating-a-key-pair), run one of the following commands:

* To upload the public key if you already created a key pair:

  ```bash theme={null}
  nebius iam auth-public-key create \
    --account-service-account-id $SA_ID \
    --data "$(cat public.pem)"
  ```

* To create a new key pair, upload the public key and create a local CLI configuration file in one step:

  ```bash theme={null}
  nebius iam auth-public-key generate \
    --service-account-id $SA_ID \
    --output ~/.nebius/$SA_ID-credentials.json
  ```

To set an expiration date for the key, add the `--expires-at` parameter to either command with a timestamp in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, for example `--expires-at 2026-04-01T20:00:00Z`.

After you complete either option, you can find the authorized key in the [web console](https://console.nebius.com). In the sidebar, go to  **Administration** → **IAM** → **Service accounts**, and select the service account for which you created the authorized key.

**Terraform**

To upload a new authorized key with Terraform:

1. Inside the working directory, create a configuration file, for example `main.tf`:

   ```hcl theme={null}
   resource "nebius_iam_v1_auth_public_key" "sa_authorized_key" {
     name      = "sa_authorized_key"
     parent_id = "<project_ID>"

     account = {
       service_account = {
         id = "<service_account_ID>"
       }
     }

     data       = file("${path.module}/public.pem")
     expires_at = "<expiration_date>"
   }
   ```

   The resource contains the following parameters:

   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `account.service_account.id`: ID of the service account. To copy the service account from the [web console](https://console.nebius.com), go to  **Administration** → **IAM** → **Service accounts**, next to the ID, click .
   * `data`: Contents of the `public.pem` file that you [created in the previous step](#creating-a-key-pair). In the example above, Terraform reads the contents of `public.pem` with the `file()` function. You can also use `trimspace(file(...))` to remove trailing whitespace.
   * `expires_at` (optional): Date and time when the authorized key expires, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, for example `2026-04-01T20:00:00Z`.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

For all available arguments and attributes, see the [full reference](https://docs.nebius.com/terraform-provider/reference/resources/iam_v1_auth_public_key.md).

**Go SDK**

Upload the public key:

```go theme={null}
publicKeyData, err := os.ReadFile("public.pem")
if err != nil {
    return err
}
authPublicKeyService := sdk.Services().IAM().V1().
    AuthPublicKey()
authPublicKeyOperation, err := authPublicKeyService.Create(
    ctx,
    &iam.CreateAuthPublicKeyRequest{
        Spec: &iam.AuthPublicKeySpec{
            Account: &iam.Account{
                Type: &iam.Account_ServiceAccount_{
                    ServiceAccount: &iam.Account_ServiceAccount{
                        Id: "<service_account_ID>",
                    },
                },
            },
            Data: string(publicKeyData),
        },
    },
)
if err != nil {
    return err
}
authPublicKeyOperation, err = authPublicKeyOperation.Wait(ctx)
if err != nil {
    return err
}
authorizedKeyID := authPublicKeyOperation.ResourceID()
fmt.Println(authorizedKeyID)
```

In the code, set the following parameters:

* `Account.ServiceAccount.Id`: ID of the service account for which you want to issue the key.
* `Spec.Data`: Contents of `public.pem` that you [created earlier](#creating-a-key-pair).

After you complete this, you can find the authorized key in the [web console](https://console.nebius.com). In the sidebar, go to  **Administration** → **IAM** → **Service accounts**, and select the service account for which you created the authorized key.

**Python SDK**

Upload the public key:

```python theme={null}
public_key = Path("public.pem").read_text()
auth_public_key_service = AuthPublicKeyServiceClient(sdk)
auth_public_key_operation = await auth_public_key_service.create(
    CreateAuthPublicKeyRequest(
        spec=AuthPublicKeySpec(
            account=Account(
                service_account=Account__ServiceAccount(
                    id="<service_account_ID>",
                ),
            ),
            data=public_key,
        ),
    ),
)
await auth_public_key_operation.wait()
authorized_key_id = auth_public_key_operation.resource_id
print(authorized_key_id)
```

In the code, set the following parameters:

* `account=Account__ServiceAccount(id=...)`: ID of the service account for which you want to issue the key.
* `spec.data`: Contents of `public.pem` that you [created earlier](#creating-a-key-pair).

After you complete this, you can find the authorized key in the [web console](https://console.nebius.com). In the sidebar, go to  **Administration** → **IAM** → **Service accounts**, and select the service account for which you created the authorized key.

**JavaScript SDK**

Upload the public key:

```ts theme={null}
const publicKey = readFileSync("public.pem", "utf8");
const authPublicKeyService =
  new AuthPublicKeyService(sdk);
const authPublicKeyOperation =
  await authPublicKeyService.create(
    CreateAuthPublicKeyRequest.create({
      metadata: ResourceMetadata.create({
        parentId: "<project_ID>",
      }),
      spec: AuthPublicKeySpec.create({
        account: Account.create({
          type: {
            $case: "serviceAccount",
            serviceAccount: Account_ServiceAccount.create({
              id: "<service_account_ID>",
            }),
          },
        }),
        data: publicKey,
      }),
    }),
  ).result;
await authPublicKeyOperation.wait();
const authorizedKeyId = authPublicKeyOperation.resourceId();
console.log(authorizedKeyId);
```

In the code, set the following parameters:

* `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
* The service account for which you want to issue the key, via `Account_ServiceAccount.create({ id: ... })`.
* `spec.data`: Contents of `public.pem` that you [created earlier](#creating-a-key-pair).

After you complete this, you can find the authorized key in the [web console](https://console.nebius.com). In the sidebar, go to  **Administration** → **IAM** → **Service accounts**, and select the service account for which you created the authorized key.

## Updating the configuration

Update your configuration to use the authorized key you created:

> [!TIP]
>
> If you used the web console to upload the public key, you do not need to update any additional configuration.

**CLI**

Create a new CLI profile:

1. [Get the ID of the project](https://docs.nebius.com/iam/manage-projects.md#cli-3) that you want to work in and save it to an environment variable:

   ```bash theme={null}
   export PROJECT_ID=<project_ID>
   ```

2. Initialize the Nebius AI Cloud CLI configuration:

   ```bash theme={null}
   nebius profile create \
     --endpoint api.nebius.cloud \
     --service-account-file ~/.nebius/$SA_ID-credentials.json \
     --parent-id $PROJECT_ID \
     --profile <profile_name>
   ```

3. Check that your new profile has been created and set as default:

   ```sh theme={null}
   nebius profile list
   ```

Now you can run Nebius AI Cloud CLI commands on behalf of the service account. To do this, add `--profile <service_account_profile_name>` to the commands.

**Terraform**

Configure the Nebius AI Cloud provider for Terraform to use an authorized key. Inside your Terraform working directory, add the `service_account` block to the provider configuration, for example in `providers.tf`:

```hcl theme={null}
provider "nebius" {
  service_account = {
    account_id       = "<service_account_ID>"
    public_key_id    = "<authorized_key_ID>"
    private_key_file = "<path_to_private_key>"
  }
}
```

In this configuration:

* `public_key_id`: The ID of the authorized key that you uploaded. To copy the public key ID:
  1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM** → **Service accounts**, and select the service account.
  2. Click **Authorized keys**, and then click  next to the ID of the public key you uploaded.
* `private_key_file`: The path to the `private.pem` file you [created in the previous step](#creating-a-key-pair).

You can also pass these values through environment variables:

```hcl theme={null}
provider "nebius" {
  service_account = {
    account_id_env       = "SA_ID"
    public_key_id_env    = "AUTHKEY_ID"
    private_key_file_env = "AUTHKEY_PRIV_PATH"
  }
}
```

```bash theme={null}
export SA_ID=<service_account_ID>
export AUTHKEY_ID=<authorized_key_ID>
export AUTHKEY_PRIV_PATH=<path_to_private_key>
```

**Go SDK**

Initialize the SDK using the authorized key you created:

```go theme={null}
newSdk, err := gosdk.New(
    ctx,
    gosdk.WithParentID("<project_ID>"),
    gosdk.WithCredentials(
        gosdk.ServiceAccountReader(
            auth.NewPrivateKeyFileParser(
                nil,
                "<path_to_private_key>",
                "<authorized_key_ID>",
                "<service_account_ID>",
            ),
        ),
    ),
)
if err != nil {
    return err
}
defer newSdk.Close()
```

In the code, set the following parameters:

* `WithParentID`'s argument: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
* `NewPrivateKeyFileParser`'s second argument: Path to the `private.pem` file you [created in the previous step](#creating-a-key-pair).
* `NewPrivateKeyFileParser`'s third argument: ID of the authorized key that you uploaded. To copy the ID:
  1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM** → **Service accounts**, and select the service account.
  2. Click **Authorized keys**, and then click  next to the ID of the public key you uploaded.
* `NewPrivateKeyFileParser`'s fourth argument: ID of the service account.

For more information about SDK initialization, see [Initialization and authentication](https://docs.nebius.com/grpc-api/sdk/go.md#initialization-and-authentication).

**Python SDK**

Initialize the SDK using the authorized key you created:

```python theme={null}
new_sdk = SDK(
    parent_id="<project_ID>",
    service_account_private_key_file_name="<path_to_private_key>",
    service_account_public_key_id="<authorized_key_ID>",
    service_account_id="<service_account_ID>",
)
```

In the code, set the following parameters:

* `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
* `service_account_private_key_file_name`: Path to the `private.pem` file you [created in the previous step](#creating-a-key-pair).
* `service_account_public_key_id`: ID of the authorized key that you uploaded. To copy the ID:
  1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM** → **Service accounts**, and select the service account.
  2. Click **Authorized keys**, and then click  next to the ID of the public key you uploaded.
* `service_account_id`: ID of the service account.

For more information about SDK initialization, see [Initialization and authentication](https://docs.nebius.com/grpc-api/sdk/python.md#initialization-and-authentication).

**JavaScript SDK**

Initialize the SDK using the authorized key you created:

```ts theme={null}
const newSdk = new SDK({
  parentId: "<project_ID>",
  credentials: new PkFileReader(
    "<path_to_private_key>",
    "<authorized_key_ID>",
    "<service_account_ID>",
  ),
});
```

In the code, set the following parameters:

* `parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
* `PkFileReader`'s first argument: Path to the `private.pem` file you [created in the previous step](#creating-a-key-pair).
* `PkFileReader`'s second argument: ID of the authorized key that you uploaded. To copy the ID:
  1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM** → **Service accounts**, and select the service account.
  2. Click **Authorized keys**, and then click  next to the ID of the public key you uploaded.
* `PkFileReader`'s third argument: ID of the service account.

For more information about SDK initialization, see [Initialization and authentication](https://docs.nebius.com/grpc-api/sdk/javascript.md#initialization-and-authentication).
