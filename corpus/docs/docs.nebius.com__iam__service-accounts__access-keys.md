# How to use access keys to authenticate in Nebius AI Cloud as a service account

Source: https://docs.nebius.com/iam/service-accounts/access-keys

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to use access keys to authenticate in Nebius AI Cloud as a service account

*Access keys* in Nebius AI Cloud are used to authenticate [service accounts](https://docs.nebius.com/iam/overview.md#accounts-and-members) in AWS-compatible services, such as Object Storage. To work with such services using their CLIs (for example, AWS CLI), create an access key and add it to the CLI configuration. The key ID is included in your requests and can be viewed. The secret key is used to sign the request parameters and is not included in the request.

Access keys can be issued without an expiration date.

Do not confuse [access tokens](https://docs.nebius.com/iam/authorization/access-tokens.md) with access keys. Access tokens are used for authentication in Nebius AI Cloud interfaces.

## Prerequisites

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Install jq to extract IDs and tokens from JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

5. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#cli-2), if you don't have one already.

6. Get the ID of the service account for which you want to issue the key and save it to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account get-by-name \
     --name <service_account_name> \
     --format jsonpath='{.metadata.id}')
   ```

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#go-sdk-2), if you don't have one already.

4. Get the ID of the service account for which you want to issue the key:

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

3. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#python-sdk-2), if you don't have one already.

4. Get the ID of the service account for which you want to issue the key:

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

3. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#javascript-sdk-2), if you don't have one already.

4. Get the ID of the service account for which you want to issue the key:

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

**CLI**

Create an access key pair and save its ID to an environment variable:

```bash theme={null}
export ACCESS_KEY_ID=$(nebius iam v2 access-key create \
  --account-service-account-id $SA_ID \
  --expires-at <optional_expiration_date> \
  --description 'AWS CLI key' \
  --format jsonpath='{.metadata.id}')
```

Where `--expires-at` allows you to create a temporary access key. To set the key expiration date, use the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format. Here's how to store an environment variable with a one-year expiration date:

```bash Ubuntu theme={null}
EXPIRES_AT=$(date -d "+1 year" "+%Y-%m-%dT%H:%M:%SZ")
```

```bash macOS theme={null}
EXPIRES_AT=$(date -j -v+1y "+%Y-%m-%dT%H:%M:%SZ")
```

Then pass the variable as `--expires-at $EXPIRES_AT`.

**Go SDK**

Create an access key pair:

```go theme={null}
createAccessKeyService := sdk.Services().IAM().V2().
    AccessKey()
accessKeyOperation, err := createAccessKeyService.Create(
    ctx,
    &iamv2.CreateAccessKeyRequest{
        Spec: &iamv2.AccessKeySpec{
            Account: &iam.Account{
                Type: &iam.Account_ServiceAccount_{
                    ServiceAccount: &iam.Account_ServiceAccount{
                        Id: "<service_account_ID>",
                    },
                },
            },
            ExpiresAt: timestamppb.New(time.Date(
                2100, 10, 30, 8, 30, 0, 0, time.UTC,
            )),
            Description: "AWS CLI key",
            SecretDeliveryMode: iamv2.SecretDeliveryMode_INLINE,
        },
    },
)
if err != nil {
    return err
}
if _, err = accessKeyOperation.Wait(ctx); err != nil {
    return err
}
accessKeyID := accessKeyOperation.ResourceID()
```

In the code, `Spec.ExpiresAt` allows you to create a temporary access key, set as a `*timestamppb.Timestamp` value. If you don't set it, the access key is issued without an expiration date.

**Python SDK**

Create an access key pair:

```python theme={null}
access_key_service = AccessKeyServiceClient(sdk)
access_key_operation = await access_key_service.create(
    CreateAccessKeyRequest(
        spec=AccessKeySpec(
            account=Account(
                service_account=Account__ServiceAccount(
                    id="<service_account_ID>",
                ),
            ),
            expires_at=datetime(2100, 10, 30, 8, 30, tzinfo=timezone.utc),
            description="AWS CLI key",
            secret_delivery_mode=SecretDeliveryMode.INLINE,
        ),
    ),
)
await access_key_operation.wait()
access_key_id = access_key_operation.resource_id
```

In the code, `spec.expires_at` allows you to create a temporary access key, set as a `datetime` value. If you don't set it, the access key is issued without an expiration date.

**JavaScript SDK**

Create an access key pair:

```ts theme={null}
const accessKeyService = new AccessKeyService(sdk);
const accessKeyOperation = await accessKeyService.create(
  CreateAccessKeyRequest.create({
    metadata: ResourceMetadata.create({
      parentId: projectId,
    }),
    spec: AccessKeySpec.create({
      account: Account.create({
        type: {
          $case: "serviceAccount",
          serviceAccount: Account_ServiceAccount.create({
            id: "<service_account_ID>",
          }),
        },
      }),
      expiresAt: dayjs('2100-10-30T08:30:00Z'),
      description: "AWS CLI key",
      secretDeliveryMode: SecretDeliveryMode.INLINE,
    }),
  }),
).result;
await accessKeyOperation.wait();
const accessKeyId = accessKeyOperation.resourceId();
```

In the code, `spec.expiresAt` allows you to create a temporary access key. If you don't set it, the access key is issued without an expiration date.

## Configuring your AWS CLI profile

In this example, you will configure the AWS CLI to work with Object Storage on behalf of the service account.

**CLI**

1. Get the access key pair AWS ID and save it to an environment variable:

   ```bash theme={null}
   export ACCESS_KEY_AWS_ID=$(nebius iam v2 access-key get \
     --id $ACCESS_KEY_ID \
     --format json | jq -r '.status.aws_access_key_id')
   ```

2. Get the secret key and save it to an environment variable:

   ```bash theme={null}
   export SECRET_ACCESS_KEY=$(nebius iam v2 access-key get \
     --id $ACCESS_KEY_ID \
     --format json | jq -r '.status.secret')
   ```

3. Add the key to the AWS CLI configuration:

   ```bash theme={null}
   aws configure set aws_access_key_id $ACCESS_KEY_AWS_ID
   aws configure set aws_secret_access_key $SECRET_ACCESS_KEY
   ```

4. Depending on your project [region](https://docs.nebius.com/overview/regions.md), add the Nebius AI Cloud region ID and the Object Storage endpoint URL to the AWS CLI configuration:
   ```bash theme={null}
   aws configure set region <region_ID>
   aws configure set endpoint_url https://storage.<region_ID>.nebius.cloud
   ```
   For example, run the following commands for a project in `eu-north1`:
   ```bash theme={null}
   aws configure set region eu-north1
   aws configure set endpoint_url https://storage.eu-north1.nebius.cloud
   ```

**Go SDK**

1. Get the access key pair AWS ID:

   ```go theme={null}
   getAccessKeyService := sdk.Services().IAM().V2().AccessKey()
   accessKey, err := getAccessKeyService.Get(
       ctx,
       &iamv2.GetAccessKeyRequest{Id: "<access_key_ID>"},
   )
   if err != nil {
       return err
   }
   fmt.Println(accessKey.GetStatus().GetAwsAccessKeyId())
   ```

2. Get the secret key. This uses a separate `GetSecret` operation instead of the regular `Get` request, because the access key secret isn't returned by the standard get call:

   ```go theme={null}
   getSecretAccessKeyService := sdk.Services().IAM().V2().
       AccessKey()
   accessKeySecret, err := getSecretAccessKeyService.GetSecret(
       ctx,
       &iamv2.GetAccessKeySecretRequest{Id: "<access_key_ID>"},
   )
   if err != nil {
       return err
   }
   fmt.Println(accessKeySecret.GetSecret())
   ```

3. Add the key to the AWS CLI configuration, using the AWS access key ID and secret printed in the previous steps:

   ```bash theme={null}
   aws configure set aws_access_key_id <AWS_access_key_ID>
   aws configure set aws_secret_access_key <AWS_secret_access_key>
   ```

4. Depending on your project [region](https://docs.nebius.com/overview/regions.md), add the Nebius AI Cloud region ID and the Object Storage endpoint URL to the AWS CLI configuration:
   ```bash theme={null}
   aws configure set region <region_ID>
   aws configure set endpoint_url https://storage.<region_ID>.nebius.cloud
   ```
   For example, run the following commands for a project in `eu-north1`:
   ```bash theme={null}
   aws configure set region eu-north1
   aws configure set endpoint_url https://storage.eu-north1.nebius.cloud
   ```

**Python SDK**

1. Get the access key pair AWS ID:

   ```python theme={null}
   get_access_key_service = AccessKeyServiceClient(sdk)
   access_key = await get_access_key_service.get(
       GetAccessKeyRequest(id="<access_key_ID>"),
   )
   print(access_key.status.aws_access_key_id)
   ```

2. Get the secret key. This uses a separate `get_secret` operation instead of the regular `get` request, because the access key secret isn't returned by the standard get call:

   ```python theme={null}
   get_secret_service = AccessKeyServiceClient(sdk)
   access_key_secret = await get_secret_service.get_secret(
       GetAccessKeySecretRequest(id="<access_key_ID>"),
   )
   print(access_key_secret.secret)
   ```

3. Add the key to the AWS CLI configuration, using the AWS access key ID and secret printed in the previous steps:

   ```bash theme={null}
   aws configure set aws_access_key_id <AWS_access_key_ID>
   aws configure set aws_secret_access_key <AWS_secret_access_key>
   ```

4. Depending on your project [region](https://docs.nebius.com/overview/regions.md), add the Nebius AI Cloud region ID and the Object Storage endpoint URL to the AWS CLI configuration:
   ```bash theme={null}
   aws configure set region <region_ID>
   aws configure set endpoint_url https://storage.<region_ID>.nebius.cloud
   ```
   For example, run the following commands for a project in `eu-north1`:
   ```bash theme={null}
   aws configure set region eu-north1
   aws configure set endpoint_url https://storage.eu-north1.nebius.cloud
   ```

**JavaScript SDK**

1. Get the access key pair AWS ID:

   ```ts theme={null}
   const getAccessKeyService = new AccessKeyService(sdk);
   const accessKey = await getAccessKeyService.get(
     GetAccessKeyRequest.create({id: "<access_key_ID>"}),
   );
   console.log(accessKey.status?.awsAccessKeyId);
   ```

2. Get the secret key. This uses a separate `getSecret` operation instead of the regular `get` request, because the access key secret isn't returned by the standard get call:

   ```ts theme={null}
   const getSecretService = new AccessKeyService(sdk);
   const accessKeySecret = await getSecretService.getSecret(
     GetAccessKeySecretRequest.create({id: "<access_key_ID>"}),
   );
   console.log(accessKeySecret.secret);
   ```

3. Add the key to the AWS CLI configuration, using the AWS access key ID and secret printed in the previous steps:

   ```bash theme={null}
   aws configure set aws_access_key_id <AWS_access_key_ID>
   aws configure set aws_secret_access_key <AWS_secret_access_key>
   ```

4. Depending on your project [region](https://docs.nebius.com/overview/regions.md), add the Nebius AI Cloud region ID and the Object Storage endpoint URL to the AWS CLI configuration:
   ```bash theme={null}
   aws configure set region <region_ID>
   aws configure set endpoint_url https://storage.<region_ID>.nebius.cloud
   ```
   For example, run the following commands for a project in `eu-north1`:
   ```bash theme={null}
   aws configure set region eu-north1
   aws configure set endpoint_url https://storage.eu-north1.nebius.cloud
   ```
