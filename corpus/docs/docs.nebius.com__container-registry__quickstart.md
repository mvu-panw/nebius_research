# Getting started with Container Registry: Create your first registry and manage a Docker image in it

Source: https://docs.nebius.com/container-registry/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Container Registry: Create your first registry and manage a Docker image in it

Container Registry helps you manage Docker images for your resources.

This guide covers how to set up your environment to work with the service, create your first *registry*, push a Docker image to it and run the image.

## Prepare your environment

In this guide, you will use the terminal in your environment, for example, on your local machine, to run commands that create and manage Nebius AI Cloud resources. The commands use the Nebius AI Cloud CLI or SDK and tools that you need to install first.

1. Install Docker Engine:

   * [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
   * [macOS](https://docs.docker.com/desktop/install/mac-install/)

2. Install the tools that manage Nebius AI Cloud resources:

   **CLI**

   1. Install **jq**, which parses JSON outputs from the Nebius AI Cloud CLI and extracts resource IDs for other commands:

      ```bash Ubuntu theme={null}
      sudo apt-get install jq
      ```

      ```bash macOS theme={null}
      brew install jq
      ```

   2. Install the **Nebius AI Cloud CLI** ([how to install](https://docs.nebius.com/cli/install.md)), which manages all Nebius AI Cloud resources:

      ```bash theme={null}
      curl -sSL https://artifacts.nebius.cloud/cli/install.sh | bash
      ```

   3. Configure the **Nebius AI Cloud CLI**:

      ```bash theme={null}
      nebius profile create
      ```

      The last command, `nebius profile create`, will guide you through several prompts. After you complete the prompts, your browser will open the Nebius AI Cloud web console sign-in screen. Sign in to the web console to complete the initialization. If you have access to multiple tenants, the CLI will prompt you to choose a tenant ID. After that, save your project ID in the CLI configuration.

      If the project ID hasn't been configured during the `nebius profile create` flow, [get the project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) and save it in the CLI configuration:

      ```bash theme={null}
      nebius config set parent-id <project_ID>
      ```

   **Go SDK**

   [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

   **Python SDK**

   [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

   **JavaScript SDK**

   [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

3. Create an environment variable for the [region](https://docs.nebius.com/overview/regions.md) in which your project is located:

   ```bash theme={null}
   export REGION_ID=<region_ID>
   ```

   For available region IDs, see [Nebius AI Cloud regions](https://docs.nebius.com/overview/regions.md).

## Create a registry

Create a test registry and save a part of its ID to an environment variable:

**CLI**

```bash theme={null}
export REGISTRY_PATH=$(nebius registry create \
  --name quickstart-registry \
  --format json | jq -r ".metadata.id" | cut -d- -f 2)
```

**Go SDK**

```go theme={null}
createService := sdk.Services().Registry().V1().Registry()
createOperation, err := createService.Create(
    ctx,
    &registry.CreateRegistryRequest{
        Metadata: &common.ResourceMetadata{
            Name: "quickstart-registry",
        },
        Spec: &registry.RegistrySpec{},
    },
)
if err != nil {
    return fmt.Errorf("create registry: %w", err)
}
createOperation, err = createOperation.Wait(ctx)
if err != nil {
    return fmt.Errorf("wait for registry creation: %w", err)
}
registryPath := strings.Split(createOperation.ResourceID(), "-")[1]
fmt.Println(registryPath)
```

The code prints the registry path, which is the registry ID without the `registry-` prefix. Run the code and save its output to an environment variable:

```bash theme={null}
export REGISTRY_PATH=$(<command_that_runs_your_code>)
```

In this command, set the command that runs your code, for example, `go run .`.

**Python SDK**

```python theme={null}
registry_service = RegistryServiceClient(sdk)
create_operation = await registry_service.create(
    CreateRegistryRequest(
        metadata=ResourceMetadata(name="quickstart-registry"),
        spec=RegistrySpec(),
    ),
)
await create_operation.wait()
registry_path = create_operation.resource_id.split("-")[1]
print(registry_path)
```

The code prints the registry path, which is the registry ID without the `registry-` prefix. Run the code and save its output to an environment variable:

```bash theme={null}
export REGISTRY_PATH=$(<command_that_runs_your_code>)
```

In this command, set the command that runs your code, for example, `python3 main.py`.

**JavaScript SDK**

```ts theme={null}
const createService = new RegistryService(sdk);
const createOperation = await createService.create(
  CreateRegistryRequest.create({
    metadata: { name: "quickstart-registry" },
    spec: {},
  }),
).result;
await createOperation.wait();
const registryPath = createOperation.resourceId().split("-")[1];
console.log(registryPath);
```

The code prints the registry path, which is the registry ID without the `registry-` prefix. Run the code and save its output to an environment variable:

```bash theme={null}
export REGISTRY_PATH=$(<command_that_runs_your_code>)
```

In this command, set the command that runs your code, for example, `node main.mjs`.

## Configure Docker

Configure Docker to work with the created registry:

**CLI**

1. Run the Nebius AI Cloud Docker credential helper. It lets you use registries in Container Registry without running the `docker login`.

   ```bash theme={null}
   nebius registry configure-helper
   ```

2. Check that the credential helper is configured:

   1. Open the file from the previous command output, for example, by using the `cat` command:

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

**Go SDK**

1. Get an access token:

   ```go theme={null}
   token, err := sdk.BearerToken(ctx)
   if err != nil {
       return err
   }
   fmt.Println(token.Token)
   ```

2. Run the code and pipe its output into `docker login`:

   ```bash theme={null}
   <command_that_runs_your_code> | \
     docker login cr.$REGION_ID.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the command that runs your code, for example, `go run .`.

   The access token is valid for 12 hours. After it expires, get a new token and log in again.

**Python SDK**

1. Get an access token:

   ```python theme={null}
   token = await sdk.get_token(timeout=None)
   print(token.token)
   ```

2. Run the code and pipe its output into `docker login`:

   ```bash theme={null}
   <command_that_runs_your_code> | \
     docker login cr.$REGION_ID.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the command that runs your code, for example, `python3 main.py`.

   The access token is valid for 12 hours. After it expires, get a new token and log in again.

**JavaScript SDK**

1. Get an access token:

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

2. Run the code and pipe its output into `docker login`:

   ```bash theme={null}
   <command_that_runs_your_code> | \
     docker login cr.$REGION_ID.nebius.cloud \
       --username iam \
       --password-stdin
   ```

   In this command, set the command that runs your code, for example, `node main.mjs`.

   The access token is valid for 12 hours. After it expires, get a new token and log in again.

## Push and run a Docker image

> [!NOTE]
>
> Do not run Docker commands as root. The credential helper is configured for your user account, so root may not be able to access the credentials.

1. Pull an image from the [Docker Hub](https://hub.docker.com/):

   ```bash theme={null}
   docker pull hello-world
   ```

2. Assign the image a tag:

   ```bash theme={null}
   docker tag hello-world \
     cr.$REGION_ID.nebius.cloud/$REGISTRY_PATH/hello-world:hello
   ```

3. Push the image to the Container Registry:

   ```bash theme={null}
   docker push cr.$REGION_ID.nebius.cloud/$REGISTRY_PATH/hello-world:hello
   ```

4. Run the image:

   ```bash theme={null}
   docker run cr.$REGION_ID.nebius.cloud/$REGISTRY_PATH/hello-world:hello
   ```
