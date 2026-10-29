# Serving Llama 4 models on Nebius AI Cloud with SkyPilot and SGLang

Source: https://nebius.com/blog/posts/serving-llama-4-skypilot-sglang

Skip to main content

# IntroductionIntroduction

Imagine this: Your customer support chatbot needs to handle thousands of queries daily, but using commercial APIs could cost tens of thousands per month. Or perhaps your company works with sensitive data that can’t be sent to third-party services. Or maybe you need complete control over model configuration and performance tuning. These are exactly the scenarios where deploying your own Llama 4 model makes sense. Instead of paying per token to commercial API providers or sacrificing data privacy, you can run Meta’s powerful open-weight models on your own infrastructure at a predictable fixed cost. Yet when you try to run these powerful models yourself, you quickly run into the classic large-scale ML wall: accelerators are expensive, configurations are complex and suddenly you’re knee-deep in errors instead of building the next cool AI app.

Today, I want to walk you through how to get Llama 4 running on Nebius AI Cloud (recently integrated with SkyPilot!), by using SGLang as the serving framework. This combo provides high throughput, efficient memory usage and none of the typical deployment headaches. Plus, I’ll share some YAML configs you can copy-paste, because who has time to write those from scratch?

# First, why this tech stack?First, why this tech stack?

- 

Llama 4 is Meta’s latest open-weight LLM family, which includes Scout (17B active params with 16 experts) and Maverick (17B active params with 128 experts). These models outperform many proprietary options, while being more manageable for independent teams to run. The Scout model is particularly nice for those with limited resources, as it can fit on a single accelerator and still deliver impressive results.

- 

Nebius AI Cloud offers high-performance instances at competitive prices.

- 

SkyPilot and its serving extension SkyServe are my personal go-to framework for running training and inference workloads across clouds. They handle all the resource optimization, failover and the fiddly deployment bits that nobody wants to deal with.

- 

SGLang is the secret sauce here. It’s a newer LLM serving framework with some real performance tricks up its sleeve, like RadixAttention for automatic KV cache reuse.

# Let’s get cookingLet’s get cooking

First, create a Nebius account.

Then, set up a local environment:

# Install SkyPilot with Nebius support
pip install "skypilot-nightly[nebius]"
# Configure Nebius credentials
wget https://raw.githubusercontent.com/nebius/nebius-solution-library/refs/heads/main/skypilot/nebius-setup.sh
chmod +x nebius-setup.sh
./nebius-setup.sh

When running the setup script, you’ll be prompted to choose a Nebius tenant and project ID. Once that’s done, check that everything is configured properly:

$ sky check nebius
Checking credentials to enable clouds for SkyPilot.
 Nebius: enabled [compute, storage]
To enable a cloud, follow the hints above and rerun: sky check 
If any problems remain, refer to detailed docs at: https://docs.skypilot.co/en/latest/getting-started/installation.html
🎉 Enabled clouds 🎉
 Nebius [compute, storage]
Using SkyPilot API server: http://127.0.0.1:46580

# Single node deployment by using sky launchSingle node deployment by using sky launch

Let’s start with a simple single-node deployment. This is great for development and testing, or when you just need one powerful machine. Save this as llama4-single-node.yaml:

resources:
 accelerators: H100:8
 region: eu-north1
 cloud: nebius
 disk_size: 512
 ports: 8000

envs:
 HF_TOKEN: 
 MODEL_NAME: meta-llama/Llama-4-Scout-17B-16E-Instruct

setup: |
 uv pip install "sglang[all]>=0.4.5" --find-links https://flashinfer.ai/whl/cu124/torch2.5/flashinfer-python
 uv pip install hf_xet
run: |
 python -m sglang.launch_server \
 --model-path $MODEL_NAME \
 --tp $SKYPILOT_NUM_GPUS_PER_NODE \
 --context-length 1000000 \
 --host 0.0.0.0 \
 --port 8000 \
 --trust-remote-code \
 --chat-template llama-4

To launch this configuration and start the model:

export HF_TOKEN=your_huggingface_token_here
sky launch -c llama4-scout llama4-single-node.yaml --env HF_TOKEN

This will create a cluster named llama4-scout and start the model server on it. After about 30 minutes (time for VM provisioning, model downloading, etc.), you can access your endpoint:

export ENDPOINT=$(sky status --endpoint 8000 llama4-scout)
curl http://$ENDPOINT/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{
 "model": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
 "messages": [
 {
 "role": "user",
 "content": "Tell me about Nebius AI"
 }
 ]
 }' | jq .
> {
 "id": "a71c00a45ede482cb049d5ecbe6c3143",
 "object": "chat.completion",
 "created": 1744567791,
 "model": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
 "choices": [
 {
 "index": 0,
 "message": {
 "role": "assistant",
 "content": "Nebius AI! After conducting research, here's what I found:\n\n**Overview**\nNebius AI is a relatively new player in the artificial intelligence (AI) 
 ...

Note that these deployed endpoints are OpenAI API compatible, so you can also use them with the OpenAI Python SDK:

import os
import openai

ENDPOINT = os.getenv("ENDPOINT")
client = openai.Client(base_url=f"http://{ENDPOINT}/v1", api_key="None")

response = client.chat.completions.create(
 model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
 messages=[
 {"role": "user", "content": "Tell me about Nebius AI"},
 ],
 temperature=0
)

print(response.choices[0].message.content)
> Nebius AI! After conducting research, I found that Nebius AI is a relatively new player in the artificial intelligence (AI) landscape. 
...

# Multi-node deployment for larger modelsMulti-node deployment for larger models

For larger models like Llama 4 Maverick (which has 128 experts and 400B parameters), we need a multi-node setup as shown below. Save this as llama4-multinode.yaml.

It’s important to note that the Maverick model is 4x the size of the Scout model, so we need to increase both the disk size and the amount of shared memory.

resources:
 accelerators: H100:8
 region: eu-north1
 cloud: nebius
 disk_size: 1024
 ports: 8000

num_nodes: 2 # Specify number of nodes to launch

envs:
 HF_TOKEN: 
 MODEL_NAME: meta-llama/Llama-4-Maverick-17B-128E-Instruct

setup: |
 uv pip install "sglang[all]>=0.4.5" --find-links https://flashinfer.ai/whl/cu124/torch2.5/flashinfer-python
 uv pip install hf_xet
 # Set up shared memory for better performance
 sudo bash -c "echo 'vm.max_map_count=655300' >> /etc/sysctl.conf"
 sudo sysctl -p
run: |
 export GLOO_SOCKET_IFNAME=(ip -o -4 route show to default | awk '{print5}')
 MASTER_ADDR=(echo"(echo "(echo"SKYPILOT_NODE_IPS" | head -n1)
 TOTAL_GPUS=((((((SKYPILOT_NUM_GPUS_PER_NODE * $SKYPILOT_NUM_NODES))

 python -m sglang.launch_server \
 --model-path $MODEL_NAME \
 --tp $TOTAL_GPUS \
 --dp 8 \
 --enable-dp-attention \
 --dist-init-addr ${MASTER_ADDR}:5000 \
 --nnodes ${SKYPILOT_NUM_NODES} \
 --node-rank ${SKYPILOT_NODE_RANK} \
 --trust-remote-code \
 --torch-compile-max-bs 8 \
 --host 0.0.0.0 \
 --port 8000 \
 --chat-template llama-4

Launch with:

export HF_TOKEN=your_huggingface_token_here
sky launch -c llama4-maverick llama4-multinode.yaml --env HF_TOKEN

SkyPilot and SGLang will automatically distribute the model across the two nodes, to set up the proper communication channels between them. Once the model is loaded, you can use the sky status command to get its endpoint for querying:

 ENDPOINT=$(sky status --endpoint 8000 llama4-maverick)
 curl http://$ENDPOINT/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{
 "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
 "messages": [
 {
 "role": "user",
 "content": "Tell me about Nebius AI"
 }
 ]
 }' | jq .
 > {
 "id": "98a393272d9544b2a9731bc8990615d8",
 "object": "chat.completion",
 "created": 1745262008,
 "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
 "choices": [
 {
 "index": 0,
 "message": {
 "role": "assistant",
 "content": "Nebius AI! That's a relatively new player in the AI landscape, and I'm happy to provide an overview.\n\n**What is Nebius AI?**\n\nNebius AI is an artificial intelligence company
 ...

# The service configuration for SkyServeThe service configuration for SkyServe

Now, let’s use SkyServe to deploy our model as a scalable service with multiple replicas, load balancing and autoscaling. The main difference between sky launch and sky serve is that:

- sky launch creates a single cluster that stays running until you stop it.

- sky serve creates a service with multiple replicas that can scale based on load.

The only change you need to make to the YAML file is to add the service section.

For example, the following is the service configuration for the Maverick model. Add this at the end of the llama4-multinode.yaml file:

service:
 readiness_probe:
 path: /health
 initial_delay_seconds: 5400 # 1.5 hours because the model is large
 timeout_seconds: 20
 replica_policy:
 min_replicas: 1
 max_replicas: 2
 target_qps_per_replica: 2.5
 upscale_delay_seconds: 300
 downscale_delay_seconds: 1200

To deploy as a service:

export HF_TOKEN=your_huggingface_token_here
sky serve up -n llama4-maverick-serve llama4-multinode.yaml --env HF_TOKEN

This command:

- 

Creates a SkyServe controller if one doesn’t exist yet. A controller is a small on-demand CPU VM that manages the deployment of your service, monitors the status of your service and routes traffic to your service replicas.

- 

Deploys the model by using SGLang.

- 

Sets up autoscaling based on our replica policy.

You’ll see output like this:

$ export HF_TOKEN=your_huggingface_token_here
$ sky serve up -n llama4-maverick-serve llama4-multinode.yaml --env HF_TOKEN
Start streaming logs for task job of replica 1...
Job ID not provided. Streaming the logs of the latest job.
├── Waiting for task resources on 2 nodes.
└── Job started. Streaming logs... (Ctrl-C to exit log streaming; job will not be killed)
(setup pid=8313) Using Python 3.10.13 environment at: /home/ubuntu/miniconda3
(setup pid=5833, ip=192.168.0.72) Using Python 3.10.13 environment at: /home/ubuntu/miniconda3
(setup pid=8313) Resolved 137 packages in 2.95s
(setup pid=8313) Downloading pillow (4.4MiB)
(setup pid=8313) Downloading pycountry (6.0MiB)
(setup pid=8313) Downloading llguidance (13.3MiB)
...
(head, rank=0, pid=8313) [2025-04-21 18:50:09 DP0 TP0] Load weight begin. avail mem=76.96 GB
(head, rank=0, pid=8313) [2025-04-21 18:50:10 DP0 TP3] Using model weights format ['*.safetensors']
(head, rank=0, pid=8313) [2025-04-21 18:50:10 DP0 TP1] Using model weights format ['*.safetensors']
...
(worker1, rank=1, pid=5833, ip=192.168.0.72) [2025-04-21 18:50:10 DP3 TP13] Using model weights format ['*.safetensors']
(worker1, rank=1, pid=5833, ip=192.168.0.72) [2025-04-21 18:50:10 DP3 TP12] Using model weights format ['*.safetensors']
(worker1, rank=1, pid=5833, ip=192.168.0.72) [2025-04-21 18:50:11 DP2 TP10] Using model weights format ['*.safetensors']
...
Loading safetensors checkpoint shards: 96% Completed | 53/55 [06:21<00:03, 1.52s/it]
Loading safetensors checkpoint shards: 98% Completed | 54/55 [06:23<00:01, 1.45s/it]
(head, rank=0, pid=8490) [2025-04-21 20:14:11 DP1 TP4] Load weight end. type=Llama4ForConditionalGeneration, dtype=torch.bfloat16, avail mem=25.12 GB, mem usage=51.83 GB.

To check service status:

$ sky serve status
Services
NAME VERSION UPTIME STATUS REPLICAS ENDPOINT 
llama4-maverick-serve 1 1h 58m 25s READY 1/1 http://89.169.102.185:30001 

Service Replicas
SERVICE_NAME ID VERSION ENDPOINT LAUNCHED RESOURCES STATUS REGION 
llama4-maverick-serve 1 1 http://89.169.112.127:8000 2 hrs ago 2x Nebius({'H100': 8}) READY eu-north1

Once the status shows READY, get your service endpoint:

ENDPOINT=$(sky serve status --endpoint llama4-maverick-serve)
curl $ENDPOINT/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{
 "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
 "messages": [
 {
 "role": "user",
 "content": "Tell me about Nebius AI"
 }
 ]
}' | jq .

# Real-world performanceReal-world performance

Enough theory — let’s look at the actual performance numbers. I ran comprehensive benchmarks on both the Scout and Maverick models to see how they perform in real-world scenarios. Here’s what I found.

For the Maverick model (128-expert MoE) running on two 8xH100 nodes:

python -m sglang.bench_serving \
 --backend sglang-oai \
 --base-url $ENDPOINT \
 --dataset-name random \
 --model meta-llama/Llama-4-Maverick-17B-128E-Instruct \
 --num-prompts 500 \
 --max-concurrency 32 \
 --output-file llama4_maverick_benchmark_results.jsonl \
 --apply-chat-template \
 --seed 42

And for comparison, here’s the Scout model (16-expert MoE) on a single 8xH100 node:

python -m sglang.bench_serving \
 --backend sglang-oai \
 --base-url $ENDPOINT \
 --dataset-name random \
 --model meta-llama/Llama-4-Scout-17B-16E-Instruct \
 --num-prompts 500 \
 --max-concurrency 32 \
 --output-file llama4_scout_benchmark_results.jsonl \
 --apply-chat-template \
 --seed 42

The results were fascinating:

 | Metric
 | Llama 4 Maverick (2 nodes)
 | Llama 4 Scout (1 node)

 | Request throughput
 | 2.43 req/s
 | 3.01 req/s

 | Input token throughput
 | 1246.50 tok/s
 | 1544.19 tok/s

 | Output token throughput
 | 1277.31 tok/s
 | 1582.36 tok/s

 | Median TTFT
 | 94.31 ms
 | 69.17 ms

 | Median ITL
 | 20.70 ms
 | 15.80 ms

What’s immediately clear is that Scout actually outperforms Maverick in raw throughput, when comparing a single 8xH100 node to two 8xH100 nodes. This makes sense when you consider the communication overhead between nodes for the distributed Maverick setup (due to tensor parallelism).

Looking at the input and output token throughput separately provides a more nuanced view of performance, as input token processing is typically much faster than output token generation. The Time to First Token (TTFT) and Inter-Token Latency (ITL) metrics are particularly important for real-time applications, as they directly impact user experience. Scout’s 69.17 ms TTFT and 15.80 ms ITL are excellent figures that rival commercial APIs and contribute to smooth conversational experiences.

When we look at the Nebius monitoring dashboard for one of the Maverick nodes, we can see some interesting patterns:

Click to expand

The port data throughput graph shows how the InfiniBand traffic rapidly escalates at the 20:02:00 mark when the model starts loading and distributing weights across nodes. That steep curve represents the significant cross-node communication needed for MoE models.

Click to expand

The NVIDIA NVLink usage shows active communication climbing to ~5.6 GiB. This indicates heavy memory traffic, which is exactly what we’d expect when running a distributed MoE model.

Click to expand

Notice how the power usage jumps from ~130W to ~300W once inference begins. The temperature rises correspondingly, but stays within safe operating ranges.

Click to expand

Perhaps most revealing is the Used Frame Buffer metric, which jumps from 78.4 GB to 79 GB when inference starts. That relatively modest increase highlights one of the key advantages of MoE models — they are memory-efficient during inference because only a subset of experts is activated for any given token. The ~80% utilization shows the system is working hard but not maxed out.

These numbers could definitely be improved by fine-tuning the --tp and --dp parameters of the SGLang server. For example, I could experiment with different tensor parallelism and data parallelism settings to better balance memory usage and computation. The current setup prioritizes stability over maximum performance, which is usually the right choice for production environments.

In practice for most applications, I recommend starting with Scout on a single node. It offers a really good performance-to-cost ratio and avoids the complexity of multi-node setups. However, if your use case requires the extra intelligence that Maverick provides, the distributed setup is definitely viable — just be prepared for about 20% lower throughput and higher infrastructure costs.

# Production readiness: From experiment to deploymentProduction readiness: From experiment to deployment

So far, we’ve focused on getting Llama 4 models deployed and running. But what does it take to make this production-ready for a real application like a customer support chatbot or code completion engine?

### Security for your Llama 4 deploymentSecurity for your Llama 4 deployment

When moving from development to production, you’ll want to consider adding some security enhancements such as:

- API key authentication: Protect your model API endpoints by implementing API key authentication. SGLang supports this via the --api-key parameter, which you can add to your YAML configuration:

envs:
 HF_TOKEN: 
 MODEL_NAME: meta-llama/Llama-4-Scout-17B-16E-Instruct
 AUTH_TOKEN: your_secure_api_key_here # Store securely, consider using env vars

run: |
 python -m sglang.launch_server \
 --model-path $MODEL_NAME \
 --tp $SKYPILOT_NUM_GPUS_PER_NODE \
 --api-key $AUTH_TOKEN \
 # other parameters as before

- HTTPS encryption: For production deployments, secure your traffic with HTTPS. SkyServe supports TLS encryption for your endpoints by adding certificate information to your service configuration:

service:
 readiness_probe:
 path: /health
 headers:
 Authorization: Bearer $AUTH_TOKEN
 tls:
 keyfile: path/to/your/private/key.pem
 certfile: path/to/your/certificate.pem
 # Other service configuration as before

- Authorization headers: Configure your readiness probe and client requests to include authorization headers:

service:
 readiness_probe:
 path: /health
 headers:
 Authorization: Bearer $AUTH_TOKEN
 # Rest of service config

When making requests to your secured endpoint, clients need to include the appropriate authorization header:

curl <https://$ENDPOINT/v1/chat/completions> \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $AUTH_TOKEN" \
 -d '{
 "model": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
 "messages": [
 {"role": "user", "content": "Tell me about Nebius AI"}
 ]
 }'

These security enhancements are essential for production deployments, especially when serving models that might have access to sensitive information or when exposing your API to external users.

### Persistent deployment with the SkyPilot API serverPersistent deployment with the SkyPilot API server

For reliable production deployments, you should use SkyPilot’s client-server architecture instead of running commands from your laptop. This transforms SkyPilot from a single-user system into a scalable, multi-user platform with several key benefits:

- 

Resilient command and control: The SkyPilot API server acts as the central hub for managing all your Llama 4 deployments, ensuring they continue running even if your local machine disconnects or shuts down.

- 

Team collaboration: Multiple team members can connect to the same API server, allowing your entire organization to view and manage resources, without sharing credentials or running all commands from the same machine.

- 

Centralized management: Get a single view of all running clusters, jobs and services across your organization, making it easier to monitor cost and usage.

- 

Fault-tolerant deployment: The SkyPilot API server can be deployed in a cloud-native way with full fault tolerance, eliminating the risk of workload loss.

# A practical use case: Integrating with the llm CLI toolA practical use case: Integrating with the llm CLI tool

Now that we have our Llama 4 model running as a service with an OpenAI-compatible API, let’s integrate it with Simon Willison’s excellent llm CLI tool. This tool provides a convenient command-line interface for interacting with various LLMs and storing conversation history in SQLite.

By default, llm doesn’t include Llama 4 models in its configuration, but since our endpoint is OpenAI API compatible, we can easily add it:

### Installing llmInstalling llm

First, install the llm CLI tool:

pip install llm

### Configuring llm to use our Llama 4 endpointConfiguring llm to use our Llama 4 endpoint

Once installed, we need to tell llm about our Llama 4 endpoint. First, let’s get our endpoint URL:

$ sky serve status --endpoint llama4-scout-serve
http://89.169.102.185:30002

Now, create or edit the extra-openai-models.yaml file in your llm configuration directory (you can find it by running dirname "$(llm logs path)"):

$ llm_config_dir= \
$(dirname \
"$(llm logs path)")
$ echo \
$llm_config_dir
/Users/alexkim/Library/Application Support/io.datasette.llm
$ vim \
$llm_config_dir/extra-openai-models.yaml

Add the following configuration:

- model_id: llama4-scout
 model_name: meta-llama/Llama-4-Scout-17B-16E-Instruct
 api_base: "http://89.169.102.185:30002/v1" # Replace with your endpoint URL

### Testing the integrationTesting the integration

Now, you can use the llm CLI to interact with your deployed Llama 4 model:

$ llm -m llama4-scout\"Who are you\"
I'm an AI assistant designed by Meta. I'm here to answer your questions, share interesting ideas and maybe even surprise you with a fresh perspective. What's on your mind?

You can also start an interactive chat session:

$ llm chat -m llama4-scout
Chatting with llama4-scout
Type 'exit' or 'quit' to exit
Type '!multi' to enter multiple lines, then '!end' to finish
> Who are you?
I'm an AI assistant designed by Meta. I'm here to answer your questions, share interesting ideas and maybe even surprise you with a fresh perspective. What's on your mind?

### Advanced usage with llmAdvanced usage with llm

One of the great features of the llm tool is its ability to log all your interactions with models in SQLite:

$ llm logs -n 3

You can also use system prompts to guide the model:

$ llm -m llama4-scout -s "You are a helpful Python coding assistant." "Write a function to calculate the Fibonacci sequence"

And even use it to process files:

$ cat mycode.py | llm -m llama4-scout -s\"Explain this code\"

The llm tool supports many other features like templates, embeddings and structured output extraction. For more information, see the llm documentation.

This integration with the llm CLI is just one demo use case. The real value of having a self-hosted OpenAI-compatible Llama 4 endpoint is that it can be used with virtually any tool that supports OpenAI-compatible APIs: chat applications, coding assistants, browser plugins, document processors and many other AI-powered tools. You get all the benefits of Meta’s latest models running on your own infrastructure, while maintaining compatibility with the growing ecosystem of OpenAI API-based applications.

# Taking it furtherTaking it further

Once you have this basic setup working, here are some things you might want to explore:

- 

Multi-node deployment for Scout: Even though Scout can fit on a single node, distributing it across multiple nodes can increase throughput. Try setting num_nodes: 2 in the YAML and adjust SGLang’s serving configuration to match your needs (e.g., --nnodes, --dp).

- 

Custom context windows: Llama 4 supports very long contexts. Experiment with the --context-length parameter to find the right balance between context size and memory usage.

- 

Prompt engineering: Try different system prompts and chat templates, to optimize model performance for your specific use case.

# Cleaning upCleaning up

When you’re done experimenting, don’t forget to tear down your resources:

For sky launch deployments:

sky down --all # bring down all your clusters

For sky serve deployments:

sky serve down --all # bring down all your services

# ConclusionConclusion

We’ve walked through the complete process of deploying Meta’s Llama 4 models on Nebius AI Cloud, from initial setup to production-ready configurations. The combination of Nebius AI Cloud’s powerful infrastructure, SkyPilot’s orchestration capabilities and SGLang’s optimized serving framework creates a robust solution for running state-of-the-art AI models on your own terms.

This approach offers several compelling advantages over commercial API solutions:

- 

Cost predictability: Instead of paying per token, which can quickly add up for high-volume applications, you get a fixed infrastructure cost regardless of usage volume.

- 

Data privacy: Your data never leaves your controlled environment, making this ideal for organizations with sensitive information or compliance requirements.

- 

Complete customization: You have full control over model configurations, context windows and performance optimizations that aren’t possible with hosted API services.

- 

OpenAI API compatibility: Your deployed endpoint works seamlessly with the vast ecosystem of tools and applications built for the OpenAI API, from chat interfaces and coding assistants to document processors and browser extensions.

- 

Performance control: As we’ve seen in the benchmarks, you can fine-tune throughput, latency and resource allocation to match your specific requirements.

Just a year ago, deploying models of this scale and quality required specialized expertise and significant resources that were exclusive to large tech companies. Today, with the tools and techniques outlined in this guide, smaller teams and individual developers can build solutions by using the same powerful models that power commercial services.

Whether you’re building a specialized customer support system, a coding assistant that needs access to proprietary code, or any application that requires both control and cutting-edge AI capabilities, this deployment strategy provides a practical path forward. The future of AI isn’t just about model capabilities — it’s also about who can access and deploy those capabilities for specific use cases. With open-weight models like Llama 4 and tools like SkyPilot, SGLang and cloud providers like Nebius, that future is becoming more open and accessible by the day.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Kim
Cloud Solutions Consultant

Contents

- Introduction

- First, why this tech stack

- Let’s get cooking

- Single node deployment by using sky launch

- Multi-node deployment for larger models

- The service configuration for SkyServe

- Real-world performance

- Production readiness: From experiment to deployment

- Security for your Llama 4 deployment

- Persistent deployment with the SkyPilot API server

- A practical use case: Integrating with the llm CLI tool

- Installing llm

- Configuring llm to use our Llama 4 endpoint

- Testing the integration

- Advanced usage with llm

- Taking it further

- Cleaning up

- Conclusion

## See also

### 

Nebius AI Cloud is now integrated with SkyPilot

We’re excited to announce our integration with SkyPilot, an open-source framework that simplifies running AI and batch workloads across cloud platforms. This collaboration enables direct access to Nebius AI Cloud resources via SkyPilot.

April 2, 2025
6 mins to read

### 

Bulk Object Storage data migration with SkyPilot

Moving large datasets between S3 buckets is often slow, unreliable and frustrating — especially across accounts or clouds. In this post, we share a fast, fully open-source workaround using SkyPilot, s5cmd and Nebius AI Cloud.

April 24, 2025
6 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
