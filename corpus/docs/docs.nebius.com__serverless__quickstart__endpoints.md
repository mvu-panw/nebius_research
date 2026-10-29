# Getting started with Serverless AI endpoints: Deploy an nginx server with authentication

Source: https://docs.nebius.com/serverless/quickstart/endpoints

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Serverless AI endpoints: Deploy an nginx server with authentication

Serverless AI lets you deploy and manage endpoints without handling infrastructure yourself. This quickstart shows how to validate basic endpoint functionality with minimal setup. In the web console, the **nginx** quick-start configuration deploys a ready-made example with preconfigured settings.

## Prerequisites

**Web console**

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
  ```

* Install [jq](https://jqlang.org/) to parse JSON output:

  ```bash Ubuntu theme={null}
  sudo apt-get install jq
  ```

  ```bash macOS theme={null}
  brew install jq
  ```

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

**REST API**

* Get an access token to [authenticate to the REST API](https://docs.nebius.com/rest-api/authentication.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

## Steps

### Create an endpoint

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. Select the **nginx** quick start card.
   The quick start configuration autofills the container image, entrypoint command and default settings.
3. Click **Create endpoint**.

Wait for the endpoint to start running.

**CLI**

Use `nebius ai create` to create a endpoint step by step in the terminal. The command prompts you to enter values to pass as parameters, shows the resulting configuration and then creates the endpoint.

1. Create a token for authorization and save it to an environment variable:

   ```bash theme={null}
   export AUTH_TOKEN=$(openssl rand -hex 32)
   ```

   Use this token in the `--token` parameter when you create the endpoint. You will also need it later to test access to the endpoint.

2. Run the following command:

   ```bash theme={null}
   nebius ai endpoint create \
     --name qs-endpoint-nginx \
     --image nginx:alpine \
     --platform cpu-d3 \
     --preset 4vcpu-16gb \
     --public \
     --container-port 80 \
     --auth token \
     --token "$AUTH_TOKEN" \
     --subnet-id <subnet_ID>
   ```

   Alternatively, you can run `nebius ai create` and specify each value step by step with CLI prompts. The command pre-fills the following values:

   * `--name`: Endpoint name.
   * `--image`: Container image to run. In the given example, the `nginx:alpine` image is used.
   * `--platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `--preset`: Number of vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `--container-port`: Port on which the application listens in the container. Each HTTP port is available through the managed HTTPS URL of the endpoint.
   * `--auth`: Authentication method for the endpoint.
   * `--token`: Token used for endpoint authentication.
   * `--public` (optional): Assigns a public IP address to the endpoint. Not required to reach the endpoint from the internet, because each HTTP port is available through the endpoint's managed HTTPS URL.
   * `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

3. When the CLI prompts you to select a project, region or subnet, select from the values that are available.

4. Review the resulting configuration, then confirm creation.

Wait for the endpoint to start running.

**Go SDK**

1. Generate a token for endpoint authentication and store it in an `authToken` variable, for example with `crypto/rand`:

   ```go theme={null}
   tokenBytes := make([]byte, 32)
   if _, err := rand.Read(tokenBytes); err != nil {
       return fmt.Errorf("generate endpoint token: %w", err)
   }
   authToken := hex.EncodeToString(tokenBytes)
   ```

   Use this token in `Spec.AuthToken` when you create the endpoint. You will also need it later to test access to the endpoint.

2. Create an endpoint:

   ```go theme={null}
   createEndpointService := sdk.Services().Ai().V1().Endpoint()
   createEndpointOperation, err := createEndpointService.Create(
       ctx,
       &ai.CreateEndpointRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "qs-endpoint-nginx",
           },
           Spec: &ai.EndpointSpec{
               Image:    "nginx:alpine",
               Platform: "cpu-d3",
               Preset:   "4vcpu-16gb",
               Ports: []*ai.EndpointSpec_Port{
                   {
                       ContainerPort: 80,
                       Protocol: ai.EndpointSpec_Port_HTTP,
                   },
               },
               AuthToken: authToken,
               PublicIp:  true,
               SubnetId:  "<subnet_ID>",
               Disk: &ai.EndpointSpec_DiskSpec{
                   Type: compute.DiskSpec_NETWORK_SSD,
                   SizeBytes: 268435456000,
               },
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create endpoint: %w", err)
   }
   if _, err = createEndpointOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for endpoint creation: %w", err)
   }
   ```

   In the code, set the following parameters:

   * `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
   * `Metadata.Name`: Endpoint name.
   * `Spec.Image`: Container image to run. In the given example, the `nginx:alpine` image is used.
   * `Spec.Platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `Spec.Preset`: Number of vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `Spec.Ports[].ContainerPort`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
   * `Spec.Ports[].Protocol`: Protocol used by the exposed port.
   * `Spec.AuthToken`: Token used for endpoint authentication, generated in the previous step.
   * `Spec.PublicIp` (optional): Whether to assign a public IP address to the endpoint. Not required to reach the endpoint from the internet, because each HTTP port is available through the endpoint's managed HTTPS URL.
   * `Spec.SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).
   * `Spec.Disk.Type`: Disk type for the underlying VM.
   * `Spec.Disk.SizeBytes`: Disk size in bytes. The example sets 250 GiB.

   After `Wait` completes, `createEndpointOperation.ResourceID()` returns the created endpoint's ID. Save this value because you need it in later steps.

Wait for the endpoint to start running.

**Python SDK**

1. Generate a token for endpoint authentication and store it in an `auth_token` variable, for example with `secrets`:

   ```python theme={null}
   import secrets

   auth_token = secrets.token_hex(32)
   ```

   Use this token in `spec.auth_token` when you create the endpoint. You will also need it later to test access to the endpoint.

2. Create an endpoint:

   ```python theme={null}
   create_endpoint_service = EndpointServiceClient(sdk)
   create_endpoint_operation = await create_endpoint_service.create(
       CreateEndpointRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="qs-endpoint-nginx",
           ),
           spec=EndpointSpec(
               image="nginx:alpine",
               platform="cpu-d3",
               preset="4vcpu-16gb",
               ports=[
                   EndpointSpec__Port(
                       container_port=80,
                       protocol=(
                           EndpointSpec__Port__Protocol.HTTP
                       ),
                   ),
               ],
               auth_token=auth_token,
               public_ip=True,
               subnet_id="<subnet_ID>",
               disk=EndpointSpec__DiskSpec(
                   type=DiskSpec__DiskType.NETWORK_SSD,
                   size_bytes=268435456000,
               ),
           ),
       ),
   )
   await create_endpoint_operation.wait()
   ```

   In the code, set the following parameters:

   * `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
   * `metadata.name`: Endpoint name.
   * `spec.image`: Container image to run. In the given example, the `nginx:alpine` image is used.
   * `spec.platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.ports[].container_port`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.ports[].protocol`: Protocol used by the exposed port.
   * `spec.auth_token`: Token used for endpoint authentication, generated in the previous step.
   * `spec.public_ip` (optional): Whether to assign a public IP address to the endpoint. Not required to reach the endpoint from the internet, because each HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.size_bytes`: Disk size in bytes. The example sets 250 GiB.

   After `await create_endpoint_operation.wait()` completes, `create_endpoint_operation.resource_id` returns the created endpoint's ID. Save this value because you need it in later steps.

Wait for the endpoint to start running.

**JavaScript SDK**

1. Generate a token for endpoint authentication and store it in an `authToken` variable, for example with `node:crypto`:

   ```ts theme={null}
   import { randomBytes } from "node:crypto";

   const authToken = randomBytes(32).toString("hex");
   ```

   Use this token in `spec.authToken` when you create the endpoint. You will also need it later to test access to the endpoint.

2. Create an endpoint:

   ```ts theme={null}
   const createEndpointService = new EndpointService(sdk);
   const createEndpointOperation = await createEndpointService.create(
     CreateEndpointRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "qs-endpoint-nginx",
       },
       spec: {
         image: "nginx:alpine",
         platform: "cpu-d3",
         preset: "4vcpu-16gb",
         ports: [{
           containerPort: 80,
           protocol: EndpointSpec_Port_Protocol.HTTP,
         }],
         authToken,
         publicIp: true,
         subnetId: "<subnet_ID>",
         disk: {
           type: DiskSpec_DiskType.NETWORK_SSD,
           sizeBytes: 268435456000n,
         },
       },
     }),
   ).result;
   await createEndpointOperation.wait();
   ```

   In the code, set the following parameters:

   * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
   * `metadata.name`: Endpoint name.
   * `spec.image`: Container image to run. In the given example, the `nginx:alpine` image is used.
   * `spec.platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.ports[].containerPort`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.ports[].protocol`: Protocol used by the exposed port.
   * `spec.authToken`: Token used for endpoint authentication, generated in the previous step.
   * `spec.publicIp` (optional): Whether to assign a public IP address to the endpoint. Not required to reach the endpoint from the internet, because each HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.sizeBytes`: Disk size in bytes, as a `bigint`. The example sets 250 GiB.

   After `await createEndpointOperation.wait()` completes, `createEndpointOperation.resourceId()` returns the created endpoint's ID. Save this value because you need it in later steps.

Wait for the endpoint to start running.

**REST API**

1. Create a token for endpoint authentication:

   ```bash theme={null}
   openssl rand -hex 32
   ```

   Save the token: it is different from the access token that authorizes REST API requests, and you need it to create and test the endpoint.

2. Send the following request. Specify the endpoint authentication token from the previous step in `spec.authToken`:

   ```bash theme={null}
   curl --request POST \
     --url 'https://api.nebius.cloud/ai/v1/endpoints' \
     --header "Authorization: Bearer <access_token>" \
     --header 'Content-Type: application/json' \
     --data '{
       "metadata": {
         "parentId": "<project_ID>",
         "name": "qs-endpoint-nginx"
       },
       "spec": {
         "image": "nginx:alpine",
         "platform": "cpu-d3",
         "preset": "4vcpu-16gb",
         "ports": [
           {
             "containerPort": 80,
             "protocol": "HTTP"
           }
         ],
         "authToken": "<endpoint_token>",
         "publicIp": true,
         "subnetId": "<subnet_ID>",
         "disk": {
           "type": "NETWORK_SSD",
           "sizeBytes": "268435456000"
         }
       }
     }'

   ```

   In the `Authorization` header, replace `<access_token>` with the access token that you got in the prerequisites.

   The request includes the following parameters:

   * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).
   * `metadata.name`: Endpoint name.
   * `spec.image`: Container image to run.
   * `spec.platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.ports[].containerPort`: Port on which the application listens in the container.
   * `spec.ports[].protocol`: Protocol used by the exposed port. An HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.authToken`: Token used for endpoint authentication.
   * `spec.publicIp` (optional): Whether to assign a public IP address to the endpoint. A public IP address isn't required to reach the endpoint through its managed HTTPS URL.
   * `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.sizeBytes`: Disk size in bytes. The specified value is 250 GiB.

   The response returns the endpoint ID in the `resourceId` parameter. Save this value because you need it in later steps.

Wait for the endpoint to start running.

### Test the endpoint

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. Click the endpoint name to open its details. Wait until the endpoint is running. Then copy its managed HTTPS URL (`https://...`) from the **Public endpoints** field.
3. In a terminal, send a request to the endpoint:

   ```bash theme={null}
   curl -v <endpoint_URL>
   ```

   In the command, specify the managed HTTPS URL that you copied earlier.

   The response should have HTTP status `200 OK`. The body is the default nginx welcome page, which confirms that the endpoint is serving traffic over the managed HTTPS URL.

**CLI**

1. Save the endpoint ID to an environment variable:

   ```bash theme={null}
   export ENDPOINT_ID=$(nebius ai endpoint get-by-name \
     --name qs-endpoint-nginx --format jsonpath='{.metadata.id}')
   ```

2. Get the endpoint's managed HTTPS URL from the **Public endpoints** field:

   ```bash theme={null}
   export ENDPOINT_URL=$(nebius ai endpoint get "$ENDPOINT_ID" --format json \
     | jq -r '.status.public_endpoints[] | select(startswith("https://"))' | head -1)
   ```

3. Test the endpoint with authentication:

   ```bash theme={null}
   curl -v "$ENDPOINT_URL" -H "Authorization: Bearer $AUTH_TOKEN"
   ```

4. Test the endpoint without a token:

   ```bash theme={null}
   curl -v "$ENDPOINT_URL"
   ```

   The test should fail with the error `401 Unauthorized` or `403 Forbidden`.

**Go SDK**

1. Get the endpoint's managed HTTPS URL:

   ```go theme={null}
   getEndpointService := sdk.Services().Ai().V1().Endpoint()
   endpoint, err := getEndpointService.Get(
       ctx,
       &ai.GetEndpointRequest{Id: "<endpoint_ID>"},
   )
   if err != nil {
       return fmt.Errorf("get endpoint: %w", err)
   }
   for _, address := range endpoint.GetStatus().GetPublicEndpoints() {
       if strings.HasPrefix(address, "https://") {
           fmt.Println(address)
           break
       }
   }
   ```

   In `ai.GetEndpointRequest`, set `Id` to the endpoint ID that you saved when you created the endpoint.

   If the code prints no URL, the endpoint isn't running yet. Wait a few seconds and run the code again.

2. Test the endpoint with authentication:

   ```bash theme={null}
   curl -v <endpoint_URL> \
     --header 'Authorization: Bearer <endpoint_token>'
   ```

   Replace `<endpoint_URL>` with the URL that the code printed and `<endpoint_token>` with the `authToken` value.

3. Test the endpoint without a token:

   ```bash theme={null}
   curl -v <endpoint_URL>
   ```

   The test should fail with the error `401 Unauthorized` or `403 Forbidden`.

**Python SDK**

1. Get the endpoint's managed HTTPS URL:

   ```python theme={null}
   get_endpoint_service = EndpointServiceClient(sdk)
   endpoint = await get_endpoint_service.get(
       GetEndpointRequest(id="<endpoint_ID>"),
   )
   endpoint_url = next(
       (
           address
           for address in endpoint.status.public_endpoints
           if address.startswith("https://")
       ),
       None,
   )
   if endpoint_url is not None:
       print(endpoint_url)
   ```

   In `GetEndpointRequest`, set `id` to the endpoint ID that you saved when you created the endpoint.

   If the code prints no URL, the endpoint isn't running yet. Wait a few seconds and run the code again.

2. Test the endpoint with authentication:

   ```bash theme={null}
   curl -v <endpoint_URL> \
     --header 'Authorization: Bearer <endpoint_token>'
   ```

   Replace `<endpoint_URL>` with the URL that the code printed and `<endpoint_token>` with the `auth_token` value.

3. Test the endpoint without a token:

   ```bash theme={null}
   curl -v <endpoint_URL>
   ```

   The test should fail with the error `401 Unauthorized` or `403 Forbidden`.

**JavaScript SDK**

1. Get the endpoint's managed HTTPS URL:

   ```ts theme={null}
   const getEndpointService = new EndpointService(sdk);
   const endpoint = await getEndpointService.get(
     GetEndpointRequest.create({ id: "<endpoint_ID>" }),
   );
   const endpointUrl = endpoint.status?.publicEndpoints.find(
     (address) => address.startsWith("https://"),
   );
   if (endpointUrl !== undefined) {
     console.log(endpointUrl);
   }
   ```

   In `GetEndpointRequest`, set `id` to the endpoint ID that you saved when you created the endpoint.

   If the code prints no URL, the endpoint isn't running yet. Wait a few seconds and run the code again.

2. Test the endpoint with authentication:

   ```bash theme={null}
   curl -v <endpoint_URL> \
     --header 'Authorization: Bearer <endpoint_token>'
   ```

   Replace `<endpoint_URL>` with the URL that the code printed and `<endpoint_token>` with the `authToken` value.

3. Test the endpoint without a token:

   ```bash theme={null}
   curl -v <endpoint_URL>
   ```

   The test should fail with the error `401 Unauthorized` or `403 Forbidden`.

**REST API**

1. Get the endpoint:

   ```bash theme={null}
   curl --request GET \
     --url "https://api.nebius.cloud/ai/v1/endpoints/<endpoint_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * In the request path, the endpoint ID returned in the `resourceId` parameter when you created the endpoint.

   Check the `status.state` parameter in the response. If the state isn't `RUNNING`, wait a few seconds and send the request again.

2. Copy a managed HTTPS URL (`https://...`) from the `status.publicEndpoints` parameter in the response.

3. Test the endpoint with authentication:

   ```bash theme={null}
   curl -v <endpoint_URL> \
     --header 'Authorization: Bearer <endpoint_token>'
   ```

4. Test the endpoint without a token:

   ```bash theme={null}
   curl -v <endpoint_URL>
   ```

   The test should fail with the error `401 Unauthorized` or `403 Forbidden`.

### View logs

> [!NOTE]
>
> Viewing endpoint logs is available only in the web console and CLI.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. In the endpoint list, next to the endpoint, click **View logs**. Alternatively, click  → **View logs**.

**CLI**

View endpoint logs:

```bash theme={null}
nebius ai endpoint logs $ENDPOINT_ID
```

### Delete the endpoint

If you no longer need the endpoint, delete it. Once you delete the endpoint, you will not be charged for it.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. In the endpoint list, find the endpoint and click  → **Delete**.
3. Confirm the endpoint deletion.

**CLI**

```bash theme={null}
nebius ai endpoint delete $ENDPOINT_ID
```

**Go SDK**

Run the following code:

```go theme={null}
deleteEndpointService := sdk.Services().Ai().V1().Endpoint()
deleteEndpointOperation, err := deleteEndpointService.Delete(
    ctx,
    &ai.DeleteEndpointRequest{Id: "<endpoint_ID>"},
)
if err != nil {
    return fmt.Errorf("delete endpoint: %w", err)
}
if _, err = deleteEndpointOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for endpoint deletion: %w", err)
}
```

In `ai.DeleteEndpointRequest`, set `Id` to the endpoint ID that you saved when you created the endpoint.

**Python SDK**

Run the following code:

```python theme={null}
delete_endpoint_service = EndpointServiceClient(sdk)
delete_endpoint_operation = await delete_endpoint_service.delete(
    DeleteEndpointRequest(id="<endpoint_ID>"),
)
await delete_endpoint_operation.wait()
```

In `DeleteEndpointRequest`, set `id` to the endpoint ID that you saved when you created the endpoint.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const deleteEndpointService = new EndpointService(sdk);
const deleteEndpointOperation = await deleteEndpointService.delete(
  DeleteEndpointRequest.create({ id: "<endpoint_ID>" }),
).result;
await deleteEndpointOperation.wait();
```

In `DeleteEndpointRequest`, set `id` to the endpoint ID that you saved when you created the endpoint.

**REST API**

Send the following request:

```bash theme={null}
curl --request DELETE \
  --url "https://api.nebius.cloud/ai/v1/endpoints/<endpoint_ID>" \
  --header "Authorization: Bearer <access_token>"
```

In the request, specify:

* Your access token in the `Authorization` header.
* In the request path, the endpoint ID returned in the `resourceId` parameter when you created the endpoint.

## Expected results

* The endpoint is reachable over its managed HTTPS URL.
* A request without a token in the web console returns `200 OK`.
* A request without a token in the CLI, SDKs or REST API returns `401 Unauthorized` or `403 Forbidden`.
* An endpoint can be deleted successfully.

## See also

* [Deploying a large language model and chatting with it by using Serverless AI endpoints](https://docs.nebius.com/serverless/tutorials/deploy-model.md)
