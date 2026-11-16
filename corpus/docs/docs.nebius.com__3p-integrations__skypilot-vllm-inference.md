# Running vLLM inference on a Managed Service for Kubernetes® cluster with SkyPilot

Source: https://docs.nebius.com/3p-integrations/skypilot-vllm-inference

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running vLLM inference on a Managed Service for Kubernetes® cluster with SkyPilot

[vLLM](https://docs.vllm.ai/) is an open-source inference and serving engine for large language models that provides an OpenAI-compatible API. SkyPilot simplifies running vLLM inference on Kubernetes: you specify the container image, GPU requirements, and commands in a configuration file, and SkyPilot launches the task on the selected cluster.

In this tutorial, you will use Managed Service for SkyPilot to launch a vLLM server on a Managed Service for Kubernetes cluster, serve the `Qwen2.5-7B-Instruct` model on a single GPU, and send an inference request to the server.

## Costs

Nebius AI Cloud only charges you for running Managed Kubernetes nodes. For more details, see [Pricing in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/resources/pricing.md). Managed Service for SkyPilot is free of charge.

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Install the [SkyPilot CLI](https://docs.skypilot.ai/en/stable/getting-started/installation.html).

## Steps

### Prepare the infrastructure

> [!NOTE]
>
> Create the Managed SkyPilot server and the Managed Kubernetes cluster in the same Nebius AI Cloud [project](https://docs.nebius.com/iam/manage-projects.md).

1. In the [web console](https://console.nebius.com/), go to  **AI orchestration** → **SkyPilot**.

   If you don't have a Managed SkyPilot server in your project, a landing page opens.

2. Click  **Create server**.

   The creation page opens.

3. Enter a name for the server or keep the default one.

4. Click **Create server**.

5. Connect the SkyPilot CLI to your Managed SkyPilot server:

   1. In your terminal, run:

      ```bash theme={null}
      sky api login -e "https://skypilot.nebius.cloud"
      ```

      The browser opens automatically.

   2. Select your Managed SkyPilot server, and click **Connect**.

   3. Follow the instructions to authenticate to Nebius AI Cloud and sign in to SkyPilot CLI.

   4. In your terminal, verify that the CLI displays the following:

      ```text theme={null}
      Logged into SkyPilot API server at: https://skypilot.nebius.cloud
      ```

6. [Create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) named `vllm-k8s-cluster`, and add a GPU node group.

   The Managed Kubernetes cluster will provide the GPU for running the vLLM server.

### Verify that SkyPilot can access your Managed Kubernetes cluster

1. In the [web console](https://console.nebius.com/), go to  **AI orchestration** → **SkyPilot**.

2. On the Managed SkyPilot server page, click **How to connect**.

3. In the window that opens, click the public endpoint URL.

   The SkyPilot dashboard opens in the browser.

4. In the SkyPilot dashboard, go to the **Infra** tab, and click **Refresh**.

   The dashboard lists the Managed Kubernetes clusters available to SkyPilot, including `vllm-k8s-cluster`.

5. In your terminal, verify that SkyPilot can access your Managed Kubernetes cluster:

   ```bash theme={null}
   sky check kubernetes
   ```

   The context for `vllm-k8s-cluster` is listed as enabled. For example:

   ```text theme={null}
   Kubernetes: enabled [compute]
     Allowed contexts:
     └── vllm-k8s-cluster: enabled.
   🎉 Enabled infra 🎉
     Kubernetes [compute]
       Allowed contexts:
       └── vllm-k8s-cluster
   ```

### Prepare the vLLM task configuration and launch the vLLM server

1. Create and enter a directory for the task configuration file:

   ```bash theme={null}
   mkdir ~/vllm-inference-tutorial
   cd ~/vllm-inference-tutorial
   ```

2. In this directory, create a `vllm.yaml` task configuration file. Replace `<gpu_platform>` with the [GPU platform](https://docs.nebius.com/compute/virtual-machines/types.md#gpu-types) of your node group, such as `H200`:

   ```yaml theme={null}
   resources:
     cloud: kubernetes
     image_id: docker:vllm/vllm-openai:v0.11.0
     accelerators: "<gpu_platform>:1"

   run: |
     vllm serve Qwen/Qwen2.5-7B-Instruct
   ```

   This file defines a Kubernetes workload that requests one GPU of the specified platform and starts vLLM. The container image provides vLLM version `v0.11.0` and its runtime dependencies. When the task starts, vLLM downloads the `Qwen/Qwen2.5-7B-Instruct` model from Hugging Face Hub and serves it through an OpenAI-compatible API.

   > [!TIP]
   >
   > To customize the model server, you can add parameters to the `vllm serve` command in the task configuration file. For example, you can configure request logging or supply a custom chat template. For available options, see the `vllm serve` [reference documentation](https://docs.vllm.ai/en/v0.11.0/cli/serve.html).

3. Launch the task that starts the vLLM server:

   ```bash theme={null}
   sky launch \
      -c vllm-inference \
      --infra k8s/vllm-k8s-cluster \
      vllm.yaml
   ```

   When prompted, confirm the launch.

   This command creates a `vllm-inference` SkyPilot environment in the Managed Kubernetes cluster named `vllm-k8s-cluster` and runs the task defined in `vllm.yaml`.

4. Wait until the logs confirm that the SkyPilot environment was launched and the vLLM server started successfully:

   ```text theme={null}
   ✓ Cluster launched: vllm-inference.
   ...
   INFO:     Application startup complete.
   ```

   You may now exit log streaming. The vLLM server continues to run.

### Send an inference request

* To ask a question, send the following request to the vLLM server:

  ```bash theme={null}
  sky exec vllm-inference 'curl --silent --show-error \
     http://127.0.0.1:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d "{
        \"model\": \"Qwen/Qwen2.5-7B-Instruct\",
        \"messages\": [
        {
           \"role\": \"user\",
           \"content\": \"Explain what a GPU is in simple terms (1-2 sentences).\"
        }
        ],
        \"max_tokens\": 128,
        \"temperature\": 0.2
     }"'
  ```

  The generated answer is in `choices[0].message.content`:

  > [accordion] Response example
  >
  > ```text wrap theme={null}
  > {"id":"chatcmpl-d3eb883a907f41d4a7e269dbd0918ebe","object":"chat.completion","created":1792065449,"model":"Qwen/Qwen2.5-7B-Instruct","choices":[{"index":0,"message":{"role":"assistant","content":"A GPU, or graphics processing unit, is a specialized processor designed to handle the complex calculations required for rendering images, videos, and animations, making it much more efficient at tasks related to visual output than a standard CPU.","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":null},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":44,"total_tokens":89,"completion_tokens":45,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}
  > ```

* To constrain the response to a predefined set of values, ask the model to select from the provided possible answers:

  ```bash theme={null}
  sky exec vllm-inference 'curl --silent --show-error \
     http://127.0.0.1:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d "{
        \"model\": \"Qwen/Qwen2.5-7B-Instruct\",
        \"messages\": [
        {
           \"role\": \"user\",
           \"content\": \"Classify the sentiment of the following sentence: The application is easy to use and works perfectly.\"
        }
        ],
        \"structured_outputs\": {
           \"choice\": [\"positive\", \"negative\", \"neutral\"]
        },
        \"max_tokens\": 16
     }"'
  ```

  The generated answer is in `choices[0].message.content`:

  > [accordion] Response example
  >
  > ```text wrap theme={null}
  > {"id":"chatcmpl-3c7e5f832edd42f5a2f2d2c4f3e238dd","object":"chat.completion","created":1792582733,"model":"Qwen/Qwen2.5-7B-Instruct","choices":[{"index":0,"message":{"role":"assistant","content":"positive","refusal":null,"annotations":null,"audio":null,"function_call":null,"tool_calls":[],"reasoning_content":null},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}],"service_tier":null,"system_fingerprint":null,"usage":{"prompt_tokens":48,"total_tokens":50,"completion_tokens":2,"prompt_tokens_details":null},"prompt_logprobs":null,"prompt_token_ids":null,"kv_transfer_params":null}
  > ```

In these examples, `max_tokens` defines the maximum number of tokens generated in the answer. `temperature` controls randomness; lower values such as `0.2` reduce variation between responses. For more information on the parameters, see the [vLLM documentation](https://docs.vllm.ai/en/v0.11.0/serving/openai_compatible_server.html).

## How to delete the created resources

Some of the created resources are chargeable. If you don't need the resources created for this tutorial, delete them:

* Delete the SkyPilot environment:

  ```bash theme={null}
  sky down vllm-inference -y
  ```

* Delete the Managed SkyPilot server:

  1. In the [web console](https://console.nebius.com), go to  **AI orchestration** → **SkyPilot**.
  2. On the Managed SkyPilot server page, go to the **Settings** tab.
  3. In the **Danger zone** section, click **Delete server**.
  4. In the window that opens, confirm the deletion.

* [Delete the Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-delete-clusters).

## See also

* [Examples: vLLM inference with SkyPilot](https://github.com/nebius/nebius-ps-services/tree/main/examples/inference/vllm)
