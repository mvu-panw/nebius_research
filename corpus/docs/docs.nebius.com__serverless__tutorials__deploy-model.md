# Deploying a large language model and chatting with it by using Serverless AI endpoints

Source: https://docs.nebius.com/serverless/tutorials/deploy-model

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying a large language model and chatting with it by using Serverless AI endpoints

Serverless AI lets you deploy and manage endpoints without handling infrastructure yourself. With endpoints, you can create an OpenAI-compatible model backend in a few minutes.

This tutorial shows how to prepare your environment, create your first endpoint with an open-source large language model (LLM), and send a chat request.

The endpoint is based on the `vllm/vllm-openai:latest` image. [vLLM](https://github.com/vllm-project/vllm) automatically downloads the model from [Hugging Face](https://huggingface.co) when the endpoint starts. The container exposes an OpenAI-compatible `/v1/chat/completions` API.

For a quick walkthrough of the web console workflow, watch the video below. If you prefer other interfaces or written instructions, follow the steps further down.

[YouTube video player](https://www.youtube.com/embed/Ftr-6JF08ZI)

Visit [Nebius Academy](https://academy.nebius.com/trainer/nebius-ai-cloud-onboarding/lesson/b532ba82-1b87-4d8c-ae82-f99afa32d04d) for video tutorials to help you get started with Nebius AI Cloud.

## Costs

Nebius AI Cloud charges you for [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md).

## Prerequisites

**Web console**

* Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check that you have quotas on the following resources in the region you use:

  * **NVIDIA® L40S for regular VMs without reservations**, under **Compute**, there should be at least one GPU available.
  * **Number of virtual machines**, under **Compute**, there should be at least one VM available.
  * **Allocations**, under **Virtual Networks**, there should be at least one allocation available.

  [Increase quotas](https://docs.nebius.com/overview/quotas.md#change-quotas) if needed.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI to work in the project in the `eu-north1` region.

2. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check that you have quotas on the following resources in the region you use:

   * **NVIDIA® L40S for regular VMs without reservations**, under **Compute**, there should be at least one GPU available.
   * **Number of virtual machines**, under **Compute**, there should be at least one VM available.
   * **Allocations**, under **Virtual Networks**, there should be at least one allocation available.

   [Increase quotas](https://docs.nebius.com/overview/quotas.md#change-quotas) if needed.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check that you have quotas on the following resources in the region you use:

   * **NVIDIA® L40S for regular VMs without reservations**, under **Compute**, there should be at least one GPU available.
   * **Number of virtual machines**, under **Compute**, there should be at least one VM available.
   * **Allocations**, under **Virtual Networks**, there should be at least one allocation available.

   [Increase quotas](https://docs.nebius.com/overview/quotas.md#change-quotas) if needed.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check that you have quotas on the following resources in the region you use:

   * **NVIDIA® L40S for regular VMs without reservations**, under **Compute**, there should be at least one GPU available.
   * **Number of virtual machines**, under **Compute**, there should be at least one VM available.
   * **Allocations**, under **Virtual Networks**, there should be at least one allocation available.

   [Increase quotas](https://docs.nebius.com/overview/quotas.md#change-quotas) if needed.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check that you have quotas on the following resources in the region you use:

   * **NVIDIA® L40S for regular VMs without reservations**, under **Compute**, there should be at least one GPU available.
   * **Number of virtual machines**, under **Compute**, there should be at least one VM available.
   * **Allocations**, under **Virtual Networks**, there should be at least one allocation available.

   [Increase quotas](https://docs.nebius.com/overview/quotas.md#change-quotas) if needed.

## Steps

### Create an endpoint

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.

2. Click  **Create endpoint**.

3. On the page that opens, specify the following endpoint settings:

   * **Configuration**: Custom.

   * **Image path**: `vllm/vllm-openai:v0.18.0-cu130`.

   * **Ports**: `8000`.

   * **Entrypoint command**:

     ```bash theme={null}
     python3 -m vllm.entrypoints.openai.api_server --model Qwen/Qwen3-0.6B --host 0.0.0.0 --port 8000
     ```

   * **Bearer token authentication**: Enabled. Copy and save the generated token.

   * **Computing resources**: With GPU.

   * **Available platform**: NVIDIA® L40S Intel.

   * **Preset**: 1 GPU — 8 CPUs — 32 GiB RAM.

   * **Network**: Public static IP.

4. Click **Create endpoint**.

**CLI**

1. Create a token for authorization and save it to an environment variable:

   ```bash theme={null}
   export AUTH_TOKEN=$(openssl rand -hex 32)
   ```

2. Save the ID of a compatible Hugging Face model in a `MODEL_ID` variable. For faster setup, use a small model, for example:

   ```bash theme={null}
   export MODEL_ID="Qwen/Qwen3-0.6B"
   ```

3. Get a subnet ID (for example, the first subnet in the project) and save it to an environment variable:

   ```bash theme={null}
   export SUBNET_ID=$(nebius vpc subnet list --format jsonpath='{.items[0].metadata.id}')
   echo "SUBNET_ID=$SUBNET_ID"
   ```

4. Create an endpoint:

   ```bash theme={null}
   nebius ai endpoint create \
     --name qs-vllm-chat \
     --image vllm/vllm-openai:v0.18.0-cu130 \
     --container-command "python3 -m vllm.entrypoints.openai.api_server" \
     --args "--model $MODEL_ID --host 0.0.0.0 --port 8000" \
     --platform gpu-l40s-a \
     --preset 1gpu-8vcpu-32gb \
     --public \
     --container-port 8000 \
     --auth token \
     --token "$AUTH_TOKEN" \
     --shm-size 16Gi \
     --subnet-id "$SUBNET_ID"
   ```

**Go SDK**

1. Generate a token for authorization and store it in an `authToken` variable:

   ```go theme={null}
   tokenBytes := make([]byte, 32)
   if _, err := rand.Read(tokenBytes); err != nil {
       return fmt.Errorf("generate endpoint token: %w", err)
   }
   authToken := hex.EncodeToString(tokenBytes)
   ```

2. Save the ID of a compatible Hugging Face model in a `modelID` variable. For faster setup, use a small model, for example:

   ```go theme={null}
   modelID := "Qwen/Qwen3-0.6B"
   ```

3. Get a subnet ID (for example, the first subnet in the project) and store it in a `subnetID` variable. For how to list subnets, see [Getting network and subnet IDs for Nebius AI Cloud resources](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).

4. Create an endpoint:

   ```go theme={null}
   createEndpointSvc := sdk.Services().Ai().V1().Endpoint()
   createEndpointOp, err := createEndpointSvc.Create(
       ctx,
       &ai.CreateEndpointRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "qs-vllm-chat",
           },
           Spec: &ai.EndpointSpec{
               Image: "vllm/vllm-openai:v0.18.0-cu130",
               ContainerCommand: "python3 -m " +
                   "vllm.entrypoints.openai.api_server",
               Args: "--model " + modelID +
                   " --host 0.0.0.0 --port 8000",
               Platform: "gpu-l40s-a",
               Preset:   "1gpu-8vcpu-32gb",
               PublicIp: true,
               Ports: []*ai.EndpointSpec_Port{
                   {
                       ContainerPort: 8000,
                       Protocol: ai.EndpointSpec_Port_HTTP,
                   },
               },
               AuthToken: authToken,
               ShmSizeBytes: 17179869184,
               SubnetId: subnetID,
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
   if _, err = createEndpointOp.Wait(ctx); err != nil {
       return fmt.Errorf("wait for endpoint creation: %w", err)
   }
   ```

   The code uses `modelID` in `Spec.Args`, `authToken` in `Spec.AuthToken` and `subnetID` in `Spec.SubnetId`. Replace `<project_ID>` in `Metadata.ParentId` with the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).

**Python SDK**

1. Generate a token for authorization and store it in an `auth_token` variable:

   ```python theme={null}
   import secrets

   auth_token = secrets.token_hex(32)
   ```

2. Save the ID of a compatible Hugging Face model in a `model_id` variable. For faster setup, use a small model, for example:

   ```python theme={null}
   model_id = "Qwen/Qwen3-0.6B"
   ```

3. Get a subnet ID (for example, the first subnet in the project) and store it in a `subnet_id` variable. For how to list subnets, see [Getting network and subnet IDs for Nebius AI Cloud resources](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).

4. Create an endpoint:

   ```python theme={null}
   create_endpoint_service = EndpointServiceClient(sdk)
   create_endpoint_operation = await create_endpoint_service.create(
       CreateEndpointRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="qs-vllm-chat",
           ),
           spec=EndpointSpec(
               image="vllm/vllm-openai:v0.18.0-cu130",
               container_command=(
                   "python3 -m "
                   "vllm.entrypoints.openai.api_server"
               ),
               args=(
                   f"--model {model_id} "
                   "--host 0.0.0.0 --port 8000"
               ),
               platform="gpu-l40s-a",
               preset="1gpu-8vcpu-32gb",
               public_ip=True,
               ports=[
                   EndpointSpec__Port(
                       container_port=8000,
                       protocol=(
                           EndpointSpec__Port__Protocol.HTTP
                       ),
                   ),
               ],
               auth_token=auth_token,
               shm_size_bytes=17179869184,
               subnet_id=subnet_id,
               disk=EndpointSpec__DiskSpec(
                   type=DiskSpec__DiskType.NETWORK_SSD,
                   size_bytes=268435456000,
               ),
           ),
       ),
   )
   await create_endpoint_operation.wait()
   ```

   The code uses `model_id` in `spec.args`, `auth_token` in `spec.auth_token` and `subnet_id` in `spec.subnet_id`. Replace `<project_ID>` in `metadata.parent_id` with the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).

**JavaScript SDK**

1. Generate a token for authorization and store it in an `authToken` variable:

   ```ts theme={null}
   import { randomBytes } from "node:crypto";

   const authToken = randomBytes(32).toString("hex");
   ```

2. Save the ID of a compatible Hugging Face model in a `modelId` variable. For faster setup, use a small model, for example:

   ```ts theme={null}
   const modelId = "Qwen/Qwen3-0.6B";
   ```

3. Get a subnet ID (for example, the first subnet in the project) and store it in a `subnetId` variable. For how to list subnets, see [Getting network and subnet IDs for Nebius AI Cloud resources](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).

4. Create an endpoint:

   ```ts theme={null}
   const createEndpointService = new EndpointService(sdk);
   const createEndpointOperation = await createEndpointService.create(
     CreateEndpointRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "qs-vllm-chat",
       },
       spec: {
         image: "vllm/vllm-openai:v0.18.0-cu130",
         containerCommand: "python3 -m " +
           "vllm.entrypoints.openai.api_server",
         args: `--model ${modelId} ` +
           "--host 0.0.0.0 --port 8000",
         platform: "gpu-l40s-a",
         preset: "1gpu-8vcpu-32gb",
         publicIp: true,
         ports: [{
           containerPort: 8000,
           protocol: EndpointSpec_Port_Protocol.HTTP,
         }],
         authToken,
         shmSizeBytes: 17179869184n,
         subnetId,
         disk: {
           type: DiskSpec_DiskType.NETWORK_SSD,
           sizeBytes: 268435456000n,
         },
       },
     }),
   ).result;
   await createEndpointOperation.wait();
   ```

   The code uses `modelId` in `spec.args`, `authToken` in `spec.authToken` and `subnetId` in `spec.subnetId`. Replace `<project_ID>` in `metadata.parentId` with the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).

The endpoint creation takes approximately five minutes.

### Check the endpoint status

**Web console**

Wait until the endpoint status is `Running`. You can check the status on the endpoint page.

**CLI**

1. Save the endpoint ID to an environment variable:

   ```bash theme={null}
   export ENDPOINT_ID=$(nebius ai endpoint list --format jsonpath='{.items[0].metadata.id}')
   echo "ENDPOINT_ID=$ENDPOINT_ID"
   ```

2. Check the status of the endpoint:

   ```bash theme={null}
   nebius ai endpoint get $ENDPOINT_ID
   ```

Wait until the endpoint status is `Running`.

**Go SDK**

1. Save the endpoint ID in an `endpointID` variable:

   ```go theme={null}
   lookupEndpointSvc := sdk.Services().Ai().V1().Endpoint()
   endpoint, err := lookupEndpointSvc.GetByName(
       ctx,
       &ai.GetEndpointByNameRequest{
           ParentId: "<project_ID>",
           Name:     "qs-vllm-chat",
       },
   )
   if err != nil {
       return fmt.Errorf("get endpoint by name: %w", err)
   }
   endpointID := endpoint.GetMetadata().GetId()
   fmt.Println("ENDPOINT_ID=" + endpointID)
   ```

2. Check the status of the endpoint:

   ```go theme={null}
   getEndpointSvc := sdk.Services().Ai().V1().Endpoint()
   endpointResult, err := getEndpointSvc.Get(
       ctx,
       &ai.GetEndpointRequest{Id: endpointID},
   )
   if err != nil {
       return fmt.Errorf("get endpoint: %w", err)
   }
   fmt.Println(endpointResult)
   ```

Check the state in the printed result. Wait until the endpoint state is `RUNNING`.

**Python SDK**

1. Save the endpoint ID in an `endpoint_id` variable:

   ```python theme={null}
   lookup_endpoint_service = EndpointServiceClient(sdk)
   endpoint = await lookup_endpoint_service.get_by_name(
       GetEndpointByNameRequest(
           parent_id="<project_ID>",
           name="qs-vllm-chat",
       ),
   )
   endpoint_id = endpoint.metadata.id
   print(f"ENDPOINT_ID={endpoint_id}")
   ```

2. Check the status of the endpoint:

   ```python theme={null}
   get_endpoint_service = EndpointServiceClient(sdk)
   endpoint_result = await get_endpoint_service.get(
       GetEndpointRequest(id=endpoint_id),
   )
   print(endpoint_result)
   ```

Check the state in the printed result. Wait until the endpoint state is `RUNNING`.

**JavaScript SDK**

1. Save the endpoint ID in an `endpointId` variable:

   ```ts theme={null}
   const lookupEndpointService = new EndpointService(sdk);
   const endpoint = await lookupEndpointService.getByName(
     GetEndpointByNameRequest.create({
       parentId: "<project_ID>",
       name: "qs-vllm-chat",
     }),
   );
   const endpointId = endpoint.metadata?.id;
   console.log(`ENDPOINT_ID=${endpointId}`);
   ```

2. Check the status of the endpoint:

   ```ts theme={null}
   const getEndpointService = new EndpointService(sdk);
   const endpointResult = await getEndpointService.get(
     GetEndpointRequest.create({ id: endpointId }),
   );
   console.log(endpointResult);
   ```

Check the state in the printed result. Wait until the endpoint state is `RUNNING`.

### Test the endpoint

**Web console**

1. Get the endpoint's managed HTTPS URL:

   1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
   2. Open the page of the required endpoint.
   3. Wait until the endpoint is running. Then, in the **Network** section, copy the public endpoint from the **Public endpoints** field. Depending on how the endpoint is exposed, this field can show either a managed `https://...` URL or `IP:port`.

2. Test the endpoint by listing available models:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/models" \
     -H "Authorization: Bearer <token>" | jq
   ```

3. Send a chat request to the model:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/chat/completions" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "Qwen/Qwen3-0.6B",
       "messages": [
         {"role": "user", "content": "Say '\''Hello Nebius AI'\'' and nothing else"}
       ]
     }' | jq -r '.choices[0].message.content'
   ```

**CLI**

1. Get the endpoint's managed HTTPS URL and save it to an environment variable:

   ```bash theme={null}
   export ENDPOINT_URL=$(nebius ai endpoint get-by-name --name qs-vllm-chat --format json \
     | jq -r '.status.public_endpoints[] | select(startswith("https://"))' | head -1)
   echo "ENDPOINT_URL=$ENDPOINT_URL"
   ```

2. Test the endpoint by listing available models:

   ```bash theme={null}
   curl "$ENDPOINT_URL/v1/models" -H "Authorization: Bearer $AUTH_TOKEN" | jq
   ```

3. Send a chat request to the model:

   ```bash theme={null}
   curl "$ENDPOINT_URL/v1/chat/completions" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"$MODEL_ID\",
       \"messages\": [{\"role\":\"user\",\"content\":\"Say 'Hello Nebius AI' and nothing else\"}]
     }" | jq -r '.choices[0].message.content'
   ```

**Go SDK**

1. Get the endpoint's managed HTTPS URL:

   ```go theme={null}
   getEndpointURLSvc := sdk.Services().Ai().V1().Endpoint()
   endpointWithURL, err := getEndpointURLSvc.GetByName(
       ctx,
       &ai.GetEndpointByNameRequest{
           ParentId: "<project_ID>",
           Name:     "qs-vllm-chat",
       },
   )
   if err != nil {
       return fmt.Errorf("get endpoint by name: %w", err)
   }
   for _, address := range endpointWithURL.GetStatus().
       GetPublicEndpoints() {
       if strings.HasPrefix(address, "https://") {
           fmt.Println("ENDPOINT_URL=" + address)
           break
       }
   }
   ```

2. Test the endpoint by listing available models:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/models" \
     -H "Authorization: Bearer <token>" | jq
   ```

3. Send a chat request to the model:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/chat/completions" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "Qwen/Qwen3-0.6B",
       "messages": [
         {"role": "user", "content": "Say '\''Hello Nebius AI'\'' and nothing else"}
       ]
     }' | jq -r '.choices[0].message.content'
   ```

   Replace `<endpoint_URL>` with the URL from the previous step and `<token>` with the `authToken` value that you generated earlier.

**Python SDK**

1. Get the endpoint's managed HTTPS URL:

   ```python theme={null}
   get_endpoint_url_service = EndpointServiceClient(sdk)
   endpoint_with_url = await get_endpoint_url_service.get_by_name(
       GetEndpointByNameRequest(
           parent_id="<project_ID>",
           name="qs-vllm-chat",
       ),
   )
   endpoint_url = next(
       (
           address
           for address in endpoint_with_url.status.public_endpoints
           if address.startswith("https://")
       ),
       None,
   )
   print(f"ENDPOINT_URL={endpoint_url}")
   ```

2. Test the endpoint by listing available models:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/models" \
     -H "Authorization: Bearer <token>" | jq
   ```

3. Send a chat request to the model:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/chat/completions" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "Qwen/Qwen3-0.6B",
       "messages": [
         {"role": "user", "content": "Say '\''Hello Nebius AI'\'' and nothing else"}
       ]
     }' | jq -r '.choices[0].message.content'
   ```

   Replace `<endpoint_URL>` with the URL from the previous step and `<token>` with the `auth_token` value that you generated earlier.

**JavaScript SDK**

1. Get the endpoint's managed HTTPS URL:

   ```ts theme={null}
   const getEndpointUrlService = new EndpointService(sdk);
   const endpointWithUrl = await getEndpointUrlService.getByName(
     GetEndpointByNameRequest.create({
       parentId: "<project_ID>",
       name: "qs-vllm-chat",
     }),
   );
   const endpointUrl = endpointWithUrl.status?.publicEndpoints.find(
     (address) => address.startsWith("https://"),
   );
   console.log(`ENDPOINT_URL=${endpointUrl}`);
   ```

2. Test the endpoint by listing available models:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/models" \
     -H "Authorization: Bearer <token>" | jq
   ```

3. Send a chat request to the model:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/chat/completions" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "Qwen/Qwen3-0.6B",
       "messages": [
         {"role": "user", "content": "Say '\''Hello Nebius AI'\'' and nothing else"}
       ]
     }' | jq -r '.choices[0].message.content'
   ```

   Replace `<endpoint_URL>` with the URL from the previous step and `<token>` with the `authToken` value that you generated earlier.

## How to delete the created resources

The endpoint and its computing resources are chargeable. If you don't need the endpoint, delete it, so Nebius AI Cloud doesn't charge for it:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. Find the endpoint and then click  → **Delete**.
3. In the window that opens, confirm the deletion.

**CLI**

```bash theme={null}
nebius ai endpoint delete $ENDPOINT_ID
```

**Go SDK**

```go theme={null}
deleteEndpointSvc := sdk.Services().Ai().V1().Endpoint()
deleteEndpointOp, err := deleteEndpointSvc.Delete(
    ctx,
    &ai.DeleteEndpointRequest{Id: endpointID},
)
if err != nil {
    return fmt.Errorf("delete endpoint: %w", err)
}
if _, err = deleteEndpointOp.Wait(ctx); err != nil {
    return fmt.Errorf("wait for endpoint deletion: %w", err)
}
```

**Python SDK**

```python theme={null}
delete_endpoint_service = EndpointServiceClient(sdk)
delete_endpoint_operation = await delete_endpoint_service.delete(
    DeleteEndpointRequest(id=endpoint_id),
)
await delete_endpoint_operation.wait()
```

**JavaScript SDK**

```ts theme={null}
const deleteEndpointService = new EndpointService(sdk);
const deleteEndpointOperation = await deleteEndpointService.delete(
  DeleteEndpointRequest.create({ id: endpointId }),
).result;
await deleteEndpointOperation.wait();
```
