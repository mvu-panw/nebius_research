# How to stop and restart a Serverless AI Devlab or endpoint

Source: https://docs.nebius.com/serverless/maintenance/stop-start

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to stop and restart a Serverless AI Devlab or endpoint

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
  ```

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**REST API**

* Get an access token to [authenticate to the REST API](https://docs.nebius.com/rest-api/authentication.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Devlabs

If you don't need your Devlab now but you want to preserve it, you can stop the Devlab and then restart it later. While the Devlab is stopped, you're not billed for computing resources, but you're billed for the disk of the underlying [Compute virtual machine](https://docs.nebius.com/compute/index.md) (VM). Data under the workspace path persists across stop and restart operations. If you mount a volume to a Devlab, you're also charged for the volume even if the Devlab is stopped.

### How to stop and restart a Devlab

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. Find the Devlab and then click  → **Stop** or **Restart**.
3. In the window that opens, confirm the action.

**CLI**

1. List Devlabs and copy the required ID:

   ```bash theme={null}
   nebius ai devlab list
   ```

2. To stop a Devlab, run the following command:

   ```bash theme={null}
   nebius ai devlab stop <devlab_ID>
   ```

3. To restart a Devlab, run the following command:

   ```bash theme={null}
   nebius ai devlab restart <devlab_ID>
   ```

## Endpoints

If you don't need your endpoint now but you want to preserve it, you can stop the endpoint and then restart it later. Computing resources of stopped endpoints aren't billed. However, if you mounted a volume to the endpoint, you're charged for the volume even if the endpoint is stopped.

When you stop an endpoint, Serverless AI releases the underlying Compute VM and its disk but preserves the endpoint's configuration, including a reserved IP address and a public HTTPS URL. When you restart the endpoint, Serverless AI creates a new VM and once again pulls the container image that was used earlier. As a result, the endpoint is available at the same URL and IP address. The URL and address only change if you delete the endpoint and create a new one.

Since the original VM and its disk are released when you stop an endpoint, no data on this disk is preserved. Unlike Devlabs, endpoints don't preserve the workspace on the disk across stop and restart operations.

### How to stop and restart an endpoint

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. Find the endpoint and then click  → **Stop** or **Restart**.
3. In the window that opens, confirm the action.

**CLI**

1. To get the endpoint ID, list all endpoints:
   ```bash theme={null}
   nebius ai endpoint list
   ```
   In the output, copy the ID of the required endpoint.
2. Restart the endpoint:

   ```bash theme={null}
   nebius ai endpoint restart --id <endpoint_ID>
   ```

   This command stops and then starts the endpoint, so you reboot it.

To stop the endpoint without restarting it, run the following command:

```bash theme={null}
nebius ai endpoint stop --id <endpoint_ID>
```

To start the endpoint, run the following command:

```bash theme={null}
nebius ai endpoint start --id <endpoint_ID>
```

**Go SDK**

1. List endpoints:

   ```go theme={null}
   listEndpointService := sdk.Services().Ai().V1().Endpoint()
   endpoints, err := listEndpointService.List(
       ctx,
       &ai.ListEndpointsRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("list endpoints: %w", err)
   }
   fmt.Println(endpoints)
   ```

   In `ai.ListEndpointsRequest`, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3). In the response, copy the `Metadata.Id` of the required endpoint.

2. Restart the endpoint:

   ```go theme={null}
   endpointService := sdk.Services().Ai().V1().Endpoint()
   restartEndpointOperation, err := endpointService.Restart(
       ctx,
       &ai.RestartEndpointRequest{
           Id: "<endpoint_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("restart endpoint: %w", err)
   }
   if _, err = restartEndpointOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for endpoint restart: %w", err)
   }
   ```

   In `ai.RestartEndpointRequest`, set `Id` to the endpoint ID that you copied. This code stops and then starts the endpoint, so you reboot it.

To stop the endpoint without restarting it, run the following code:

```go theme={null}
stopEndpointService := sdk.Services().Ai().V1().Endpoint()
stopEndpointOperation, err := stopEndpointService.Stop(
    ctx,
    &ai.StopEndpointRequest{
        Id: "<endpoint_ID>",
    },
)
if err != nil {
    return fmt.Errorf("stop endpoint: %w", err)
}
if _, err = stopEndpointOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for endpoint stop: %w", err)
}
```

In `ai.StopEndpointRequest`, set `Id` to the endpoint ID that you copied.

To start the endpoint, run the following code:

```go theme={null}
startEndpointService := sdk.Services().Ai().V1().Endpoint()
startEndpointOperation, err := startEndpointService.Start(
    ctx,
    &ai.StartEndpointRequest{
        Id: "<endpoint_ID>",
    },
)
if err != nil {
    return fmt.Errorf("start endpoint: %w", err)
}
if _, err = startEndpointOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for endpoint start: %w", err)
}
```

In `ai.StartEndpointRequest`, set `Id` to the endpoint ID that you copied.

**Python SDK**

1. List endpoints:

   ```python theme={null}
   list_endpoint_service = EndpointServiceClient(sdk)
   endpoints = await list_endpoint_service.list(
       ListEndpointsRequest(parent_id="<project_ID>"),
   )
   print(endpoints)
   ```

   In `ListEndpointsRequest`, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3). In the response, copy the `metadata.id` of the required endpoint.

2. Restart the endpoint:

   ```python theme={null}
   restart_endpoint_service = EndpointServiceClient(sdk)
   restart_endpoint_operation = await restart_endpoint_service.restart(
       RestartEndpointRequest(id="<endpoint_ID>"),
   )
   await restart_endpoint_operation.wait()
   ```

   In `RestartEndpointRequest`, set `id` to the endpoint ID that you copied. This code stops and then starts the endpoint, so you reboot it.

To stop the endpoint without restarting it, run the following code:

```python theme={null}
stop_endpoint_service = EndpointServiceClient(sdk)
stop_endpoint_operation = await stop_endpoint_service.stop(
    StopEndpointRequest(id="<endpoint_ID>"),
)
await stop_endpoint_operation.wait()
```

In `StopEndpointRequest`, set `id` to the endpoint ID that you copied.

To start the endpoint, run the following code:

```python theme={null}
start_endpoint_service = EndpointServiceClient(sdk)
start_endpoint_operation = await start_endpoint_service.start(
    StartEndpointRequest(id="<endpoint_ID>"),
)
await start_endpoint_operation.wait()
```

In `StartEndpointRequest`, set `id` to the endpoint ID that you copied.

**JavaScript SDK**

1. List endpoints:

   ```ts theme={null}
   const listEndpointService = new EndpointService(sdk);
   const endpoints = await listEndpointService.list(
     ListEndpointsRequest.create({
       parentId: "<project_ID>",
     }),
   );
   console.log(endpoints);
   ```

   In `ListEndpointsRequest`, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3). In the response, copy the `metadata.id` of the required endpoint.

2. Restart the endpoint:

   ```ts theme={null}
   const restartEndpointService = new EndpointService(sdk);
   const restartEndpointOperation = await restartEndpointService.restart(
     RestartEndpointRequest.create({
       id: "<endpoint_ID>",
     }),
   ).result;
   await restartEndpointOperation.wait();
   ```

   In `RestartEndpointRequest`, set `id` to the endpoint ID that you copied. This code stops and then starts the endpoint, so you reboot it.

To stop the endpoint without restarting it, run the following code:

```ts theme={null}
const stopEndpointService = new EndpointService(sdk);
const stopEndpointOperation = await stopEndpointService.stop(
  StopEndpointRequest.create({
    id: "<endpoint_ID>",
  }),
).result;
await stopEndpointOperation.wait();
```

In `StopEndpointRequest`, set `id` to the endpoint ID that you copied.

To start the endpoint, run the following code:

```ts theme={null}
const startEndpointService = new EndpointService(sdk);
const startEndpointOperation = await startEndpointService.start(
  StartEndpointRequest.create({
    id: "<endpoint_ID>",
  }),
).result;
await startEndpointOperation.wait();
```

In `StartEndpointRequest`, set `id` to the endpoint ID that you copied.

**REST API**

1. List endpoints:

   ```bash theme={null}
   curl --request GET \
     --url "https://api.nebius.cloud/ai/v1/endpoints?parentId=<project_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * The [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in the `parentId` query parameter.

   In the response, copy the `metadata.id` of the required endpoint.

2. Restart the endpoint:

   ```bash theme={null}
   curl --request POST \
     --url 'https://api.nebius.cloud/ai/v1/endpoints/restart' \
     --header "Authorization: Bearer <access_token>" \
     --header 'Content-Type: application/json' \
     --data '{
       "id": "<endpoint_ID>"
     }'

   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * `<endpoint_ID>`: Endpoint ID that you copied.

To stop the endpoint without restarting it, send the following request:

```bash theme={null}
curl --request POST \
  --url 'https://api.nebius.cloud/ai/v1/endpoints/stop' \
  --header "Authorization: Bearer <access_token>" \
  --header 'Content-Type: application/json' \
  --data '{
    "id": "<endpoint_ID>"
  }'

```

To start the endpoint, send the following request:

```bash theme={null}
curl --request POST \
  --url 'https://api.nebius.cloud/ai/v1/endpoints/start' \
  --header "Authorization: Bearer <access_token>" \
  --header 'Content-Type: application/json' \
  --data '{
    "id": "<endpoint_ID>"
  }'

```
