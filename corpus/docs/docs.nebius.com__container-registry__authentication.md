# How to authenticate in Container Registry

Source: https://docs.nebius.com/container-registry/authentication

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to authenticate in Container Registry

You can authenticate in Container Registry with the help of a short-lived [access token](https://docs.nebius.com/iam/authorization/access-tokens.md) issued by the Nebius AI Cloud CLI or SDK each time, or with a long-lived [static key token](https://docs.nebius.com/iam/authorization/static-keys.md) issued for the Container Registry service.

* For a [local machine](#working-on-a-local-machine), use a Docker credential helper.
* For a [CI/CD environment](#working-in-a-ci/cd-environment), use a service account and either issue a [long-lived static key](#long-lived-static-key-token) and save it in your pipeline settings, or get a [short-lived token](#short-lived-access-token) each time your pipeline runs.

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## Working on a local machine

On your local machine, you can simply configure a Docker credential helper to work with Container Registry.

1. Run the following command:

   ```bash theme={null}
   nebius registry configure-helper
   ```

2. Check that the credential helper is configured:

   1. Open the file from the previous command output, for example, with the `cat` command:

      ```bash theme={null}
      cat ~/.docker/config.json
      ```

   2. Check that the `credHelpers` property contains the following lines:

      ```json theme={null}
      "cr.eu-north1.nebius.cloud": "nebius",
      "cr.eu-north2.nebius.cloud": "nebius",
      "cr.eu-south1.nebius.cloud": "nebius",
      "cr.eu-west1.nebius.cloud": "nebius",
      "cr.eu-west2.nebius.cloud": "nebius",
      "cr.me-west1.nebius.cloud": "nebius",
      "cr.uk-south1.nebius.cloud": "nebius",
      "cr.uk-south2.nebius.cloud": "nebius",
      "cr.us-central1.nebius.cloud": "nebius",
      "cr.us-north1.nebius.cloud": "nebius"
      ```

When you run any `docker` command after this configuration, it requests credentials from `nebius`, which might require you to log in with the help of the [Nebius AI Cloud web console](https://console.nebius.com).

## Working in a CI/CD environment

In your CI/CD environment, you are unlikely to be able to log into the web console. Therefore, you need to [create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#create-a-service-account) and use it to get credentials. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group.

There are two ways to work with a service account:

* Issue a long-lived [static key](https://docs.nebius.com/iam/authorization/static-keys.md) for Container Registry.
* Get a short-lived [access token](https://docs.nebius.com/iam/authorization/access-tokens.md) in each run of your pipeline job.

### Long-lived static key token

To use a long-lived token, you need to [issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md) and store the token in your CI/CD environment configuration.

1. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. Create a static key for your service account:

   **CLI**

   ```bash theme={null}
   nebius iam static-key issue \
     --account-service-account-id=<service_account_ID> \
     --service=CONTAINER_REGISTRY
   ```

   By default, the key lifetime is 6 months. If you need a different lifetime, add the `--expires-at` parameter to this command. It accepts the date of expiration in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, for example `2025-11-23T11:44:43.232142Z`. You can set a lifetime of up to 3 years.

   **Go SDK**

   ```go theme={null}
   staticKeyService := sdk.Services().IAM().V1().StaticKey()
   issuedKey, err := staticKeyService.Issue(
       ctx,
       &iam.IssueStaticKeyRequest{
           Spec: &iam.StaticKeySpec{
               Account: &iam.Account{
                   Type: &iam.Account_ServiceAccount_{
                       ServiceAccount: &iam.Account_ServiceAccount{
                           Id: "<service_account_ID>",
                       },
                   },
               },
               Service: iam.StaticKeySpec_CONTAINER_REGISTRY,
           },
       },
   )
   if err != nil {
       return fmt.Errorf("issue static key: %w", err)
   }
   fmt.Println(issuedKey.GetToken())
   ```

   In the code, set `Id` in `Account_ServiceAccount` to the ID of your service account. `Service` is set to `iam.StaticKeySpec_CONTAINER_REGISTRY`, so the key works only with Container Registry.

   By default, the key lifetime is 6 months. If you need a different lifetime, add `ExpiresAt` to `StaticKeySpec`. You can set a lifetime of up to 3 years.

   **Python SDK**

   ```python theme={null}
   static_key_service = StaticKeyServiceClient(sdk)
   issued_key = await static_key_service.issue(
       IssueStaticKeyRequest(
           spec=StaticKeySpec(
               account=Account(
                   service_account=Account__ServiceAccount(
                       id="<service_account_ID>",
                   ),
               ),
               service=StaticKeySpec__ClientService.CONTAINER_REGISTRY,
           ),
       ),
   )
   print(issued_key.token)
   ```

   In the code, set `id` in `Account__ServiceAccount` to the ID of your service account. `service` is set to `StaticKeySpec__ClientService.CONTAINER_REGISTRY`, so the key works only with Container Registry.

   By default, the key lifetime is 6 months. If you need a different lifetime, add `expiresAt` to `StaticKeySpec`. You can set a lifetime of up to 3 years.

   **JavaScript SDK**

   ```ts theme={null}
   const staticKeyService = new StaticKeyService(sdk);
   const issuedKey = await staticKeyService.issue(
     IssueStaticKeyRequest.create({
       metadata: {},
       spec: {
         account: {
           type: {
             $case: "serviceAccount",
             serviceAccount: { id: "<service_account_ID>" },
           },
         },
         service: StaticKeySpec_ClientService.CONTAINER_REGISTRY,
       },
     }),
   ).result;
   console.log(issuedKey.token);
   ```

   In the code, set `id` in `serviceAccount` to the ID of your service account. `service` is set to `StaticKeySpec_ClientService.CONTAINER_REGISTRY`, so the key works only with Container Registry.

   By default, the key lifetime is 6 months. If you need a different lifetime, add `expiresAt` to `spec`. You can set a lifetime of up to 3 years.

3. Get the static key token from the output.

4. Configure the job that works with Container Registry to use this token:

   ```bash theme={null}
   docker login cr.<region>.nebius.cloud \
     --username iam \
     --password <token>
   ```

   In this command, set the [region](https://docs.nebius.com/overview/regions.md) of the registry with which the pipeline is working.

### Short-lived access token

To use a short-lived access token, you need to get it from the Nebius AI Cloud CLI or SDK in your CI/CD environment. Access tokens have a lifetime of 12 hours.

**CLI**

1. Create an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) for your service account.
2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
3. [Configure a profile](https://docs.nebius.com/iam/service-accounts/authorized-keys.md#configure-your-profile) for your service account in the `.nebius/config.yaml` file.
4. Configure the job that works with Container Registry to generate credentials by using `nebius` and pipe them directly into a `docker` command:

   ```bash theme={null}
   nebius iam get-access-token | \
     docker login cr.<region>.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the [region](https://docs.nebius.com/overview/regions.md) of the registry with which the pipeline is working.

You can do the same if you are using `helm registry login`:

```bash theme={null}
nebius iam get-access-token | \
  helm registry login cr.<region>.nebius.cloud \
    --username iam \
    --password-stdin
```

**Go SDK**

1. [Initialize the Go SDK with the credentials of your service account](https://docs.nebius.com/sdk/go/install-auth.md#initialization-and-authentication).

2. In the code of your job, get an access token:

   ```go theme={null}
   token, err := sdk.BearerToken(ctx)
   if err != nil {
       return err
   }
   fmt.Println(token.Token)
   ```

3. Configure the job that works with Container Registry to run the code and pipe its output directly into a `docker` command:

   ```bash theme={null}
   <command_that_runs_your_code> | \
     docker login cr.<region>.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the command that runs your code, for example, `go run .`, and the [region](https://docs.nebius.com/overview/regions.md) of the registry with which the pipeline is working.

You can do the same if you are using `helm registry login`:

```bash theme={null}
<command_that_runs_your_code> | \
  helm registry login cr.<region>.nebius.cloud \
    --username iam \
    --password-stdin
```

**Python SDK**

1. [Initialize the Python SDK with the credentials of your service account](https://docs.nebius.com/sdk/python/install-auth.md#initialization-and-authentication).

2. In the code of your job, get an access token:

   ```python theme={null}
   token = await sdk.get_token(timeout=None)
   print(token.token)
   ```

3. Configure the job that works with Container Registry to run the code and pipe its output directly into a `docker` command:

   ```bash theme={null}
   <command_that_runs_your_code> | \
     docker login cr.<region>.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the command that runs your code, for example, `python3 main.py`, and the [region](https://docs.nebius.com/overview/regions.md) of the registry with which the pipeline is working.

You can do the same if you are using `helm registry login`:

```bash theme={null}
<command_that_runs_your_code> | \
  helm registry login cr.<region>.nebius.cloud \
    --username iam \
    --password-stdin
```

**JavaScript SDK**

1. [Initialize the JavaScript SDK with the credentials of your service account](https://docs.nebius.com/sdk/javascript/install-auth.md#initialization-and-authentication).

2. In the code of your job, get an access token:

   ```ts theme={null}
   const authorization = sdk.getAuthorizationProvider();
   if (!authorization) {
     throw new Error("authorization is not configured");
   }
   const metadata = new Metadata();
   await authorization.authenticator().authenticate(metadata);
   const header = metadata.get("authorization")[0];
   if (typeof header !== "string") {
     throw new Error("authorization token is missing");
   }
   const token = header.replace(/^Bearer\s+/, "");
   console.log(token);
   ```

   The code uses `Metadata` from the `@grpc/grpc-js` package. Install the package by using `npm install @grpc/grpc-js` and import `Metadata` from it.

3. Configure the job that works with Container Registry to run the code and pipe its output directly into a `docker` command:

   ```bash theme={null}
   <command_that_runs_your_code> | \
     docker login cr.<region>.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the command that runs your code, for example, `node main.mjs`, and the [region](https://docs.nebius.com/overview/regions.md) of the registry with which the pipeline is working.

You can do the same if you are using `helm registry login`:

```bash theme={null}
<command_that_runs_your_code> | \
  helm registry login cr.<region>.nebius.cloud \
    --username iam \
    --password-stdin
```

## Troubleshooting

If you are getting the "Permission denied" error when trying to access Container Registry from your [local machine](#working-on-a-local-machine), double-check that the Docker credential helper was configured correctly:

* Check that the system can find the Nebius AI Cloud CLI binary:

  ```bash theme={null}
  which nebius
  ```

  It should return a path, for example:

  ```bash theme={null}
  /home/user/.nebius/bin/nebius
  ```

  If it does not, reinstall Nebius AI Cloud CLI, and then rerun `nebius registry configure-helper`.

* Check that the system can find the credential helper:

  ```bash theme={null}
  which docker-credential-nebius
  ```

  It should return a path, for example:

  ```bash theme={null}
  /home/user/.nebius/bin/docker-credential-nebius
  ```

  If it does not, rerun `nebius registry configure-helper`.

* Check that the region of the registry you are trying to access is present in the `.docker/config.json` file:

  ```json theme={null}
  "cr.<region>.nebius.cloud": "nebius"
  ```

  If it is not, add it manually or rerun `nebius registry configure-helper`.
