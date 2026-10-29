# Serving Qwen3 models on Nebius AI Cloud by using SkyPilot and SGLang

Source: https://nebius.com/blog/posts/serving-qwen3-skypilot-sglang

Skip to main content

Following our exploration of Llama 4 models on Nebius AI Cloud, I’m excited to switch gears and focus on another groundbreaking collection of open models: Alibaba’s new Qwen3 family. Released just days ago, these models have been creating quite a stir in the open-source AI community. Let’s dive into how to deploy them by using the same powerful SkyPilot + SGLang combination we discussed previously.

# Meet Qwen3: A new open standardMeet Qwen3: A new open standard

If you haven’t been following the community chatter in the past few days, Qwen3 represents a major milestone for open-source AI models. As Nathan Lambert noted, Qwen3 provides “the best of both worlds for open models — peak performance and size scales.”

What sets Qwen3 apart is both its impressive benchmark performance and its range of model sizes. The flagship Qwen3-235B-A22B (an MoE model with 235 billion total parameters, but only 22 billion activated parameters per token) achieves competitive results against models like DeepSeek R1, OpenAI o1 and Gemini 2.5 Pro. Meanwhile, Qwen3-32B, a dense model, performs comparably to much larger models despite being small enough to run on a single accelerator.

Most importantly for those of us building applications: all Qwen3 models are released under the Apache 2.0 license, which is far more permissive than what we’ve seen with many other open models. This means greater flexibility for developers and organizations looking to build on top of these capabilities.

# Let’s deploy Qwen3 on Nebius AI CloudLet’s deploy Qwen3 on Nebius AI Cloud

Now that we understand what makes Qwen3 special, let’s get these models running on Nebius AI Cloud infrastructure by using our established SkyPilot + SGLang stack. First, you need to install SkyPilot and configure it to run on Nebius AI Cloud.

### Deployment configurationDeployment configuration

I’ve prepared two YAML configurations that you can use to deploy different Qwen3 models.

For the dense model that can run on a single accelerator:

# qwen3-32B-serve.yaml
resources:
 accelerators: H100:1
 region: eu-north1
 cloud: nebius
 ports: 8000

envs:
 MODEL_NAME: Qwen/Qwen3-32B

setup: |
 uv pip install "sglang[all]>=0.4.6.post1" hf_xet

run: |
 python3 -m sglang.launch_server \
 --model $MODEL_NAME \
 --port 8000 \
 --host 0.0.0.0 \
 --reasoning-parser qwen3 

service:
 readiness_probe: /health
 replica_policy:
 min_replicas: 1
 max_replicas: 2
 target_qps_per_replica: 2.5
 upscale_delay_seconds: 300
 downscale_delay_seconds: 1200

And for the flagship MoE model that requires more memory:

# qwen3-235B-A22B-serve.yaml
resources:
 accelerators: H100:8
 region: eu-north1
 cloud: nebius
 disk_size: 1024
 ports: 8000

envs:
 MODEL_NAME: Qwen/Qwen3-235B-A22B

setup: |
 uv pip install "sglang[all]>=0.4.6.post1" hf_xet

run: |
 python3 -m sglang.launch_server \
 --model $MODEL_NAME \
 --port 8000 \
 --host 0.0.0.0 \
 --tp $SKYPILOT_NUM_GPUS_PER_NODE \
 --reasoning-parser qwen3 

service:
 readiness_probe: /health
 replica_policy:
 min_replicas: 1
 max_replicas: 2
 target_qps_per_replica: 2.5
 upscale_delay_seconds: 300
 downscale_delay_seconds: 1200

Notice that unlike Llama 4 Maverick, which requires multiple nodes for deployment, even the massive Qwen3-235B-A22B can run on a single node! This is a testament to the architecture efficiency that the Qwen team has achieved with their MoE implementation.

### FP8 quantization: Doing more with lessFP8 quantization: Doing more with less

Recent research provides insights into FP8 quantization that could drastically reduce the memory footprint of these large models. With FP8 quantization, we could deploy these models with less than half of the memory requirements, meaning even the massive Qwen3-235B-A22B could potentially run on just four accelerators instead of eight, resulting in a dramatically reduced deployment cost.

Similarly, while we previously discussed that Llama 4 Maverick requires a multi-node setup, with FP8 quantization, it could actually fit into a single node. Alternatively, if you have access to the newer hardware, Llama 4 Maverick would work on a single node of eight NVIDIA H200 GPUs — even without quantization — due to the additional memory available.

What makes FP8 particularly compelling is the minimal impact on model quality. For production deployments, this means you can achieve greater efficiency without sacrificing the quality that makes these models valuable in the first place.

### Launching the servicesLaunching the services

Assuming you’ve already set up SkyPilot with Nebius integration, you can launch these models with:

# Deploy the 32B dense model
sky serve up -n qwen3-32b qwen3-32B-serve.yaml

# Deploy the 235B MoE model
sky serve up -n qwen3-235b qwen3-235B-A22B-serve.yaml

The deployment process is similar to what we saw with Llama 4, but you’ll notice the --reasoning-parser qwen3 parameter. This is because Qwen3 comes with a unique “hybrid thinking modes” feature that allows the model to alternate between step-by-step reasoning and quick responses.

So the response from the deployed APIs will look something like this:

ENDPOINT=$(sky serve status --endpoint qwen3-235b)
curl $ENDPOINT/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{
 "model": "Qwen/Qwen3-235B-A22B",
 "messages": [
 {
 "role": "user",
 "content": "Tell me about Nebius AI"
 }
 ]
}' | jq .
> {
 "id": "4453e5f240c34471a4f731bb0316fad3",
 "object": "chat.completion",
 "created": 1745972323,
 "model": "Qwen/Qwen3-235B-A22B",
 "choices": [
 {
 "index": 0,
 "message": {
 "role": "assistant",
 "content": "**Nebius AI: Overview and Key Information**\n\n**Company Background** ...",
 "reasoning_content": "Okay, I need to figure out what the user is asking about Nebius AI. Let me start by recalling any information I have on this company. ...",
 "tool_calls": null
 },
 "logprobs": null,
 "finish_reason": "stop",
 "matched_stop": 151645
 }
 ],
 "usage": {
 "prompt_tokens": 14,
 "total_tokens": 1432,
 "completion_tokens": 1418,
 "prompt_tokens_details": null
 }
}

# Real-world performanceReal-world performance

I’ve run comprehensive benchmarks on both Qwen3 models, to see how they perform in real-world conditions. Below is what I found after running SGLang’s benchmarking tool:

### Qwen3-235B-A22B (MoE model)Qwen3-235B-A22B (MoE model)

Request throughput: 1.60 req/s
Input token throughput: 781.20 tok/s
Output token throughput: 866.14 tok/s
Median Time to First Token: 133.39 ms
Median Inter-Token Latency: 27.53 ms

### Qwen3-32B (Dense model)Qwen3-32B (Dense model)

Request throughput: 1.35 req/s
Input token throughput: 659.47 tok/s
Output token throughput: 731.17 tok/s
Median Time to First Token: 159.27 ms
Median Inter-Token Latency: 29.37 ms

What immediately jumps out is how competitive the performance metrics are between these two models, despite the vast difference in their parameter counts and hardware requirements. The Qwen3-32B model provides roughly 85% of the throughput of its much larger sibling, while running on just a single accelerator!

# Running your own benchmarksRunning your own benchmarks

One of the great advantages of our SkyPilot + SGLang setup is how easy it makes benchmarking. You don’t need to use expensive instances for benchmarking — you can run comprehensive benchmarks from a simple CPU-only instance.

Here is a benchmark.yaml file I created, which makes this process straightforward:

resources:
 region: eu-north1
 cloud: nebius
 cpus: 32

envs:
 ENDPOINT: 
 MODEL_NAME: 

setup: |
 uv pip install "sglang[all]>=0.4.6.post1" 

run: |
 python -m sglang.bench_serving \
 --backend sglang-oai \
 --base-url $ENDPOINT \
 --dataset-name random \
 --model $MODEL_NAME \
 --num-prompts 100 \
 --max-concurrency 32 \
 --output-file qwen3_out.jsonl \
 --apply-chat-template --seed 42

### Running benchmarks on your deployed modelsRunning benchmarks on your deployed models

Once you have your Qwen3 models deployed as services, you can easily benchmark them with a single command. For the 32B model:

sky launch -c bench benchmark.yaml \
--env ENDPOINT=$(sky serve status --endpoint qwen3-32b) \
--env MODEL_NAME=Qwen/Qwen3-32B -y

And for the 235B MoE model:

sky launch -c bench benchmark.yaml \
--env ENDPOINT=$(sky serve status --endpoint qwen3-235b) \
--env MODEL_NAME=Qwen/Qwen3-235B-A22B -y

These commands automatically:

- Spin up a CPU-only instance (much cheaper than GPU instances).

- Install SGLang’s benchmarking tools.

- Connect to your deployed model endpoint.

- Run 100 random prompts to test throughput and latency.

The benchmarking process tests how the model performs under concurrent load (up to 32 simultaneous requests), giving you a realistic view of production capabilities. This makes it easy to experiment with different configuration parameters and see their impact on performance.

# Qwen3 vs. Llama 4: A quick comparisonQwen3 vs. Llama 4: A quick comparison

When we compare our Qwen3 benchmarks to our previous findings with Llama 4 models, a few observations stand out:

- 

Efficiency: Qwen3’s MoE architecture seems more efficient than Llama 4 Maverick. The Qwen3-235B-A22B model runs comfortably on a single node, while Llama 4 Maverick requires a multi-node setup.

- 

Latency: Qwen3 models show decent TTFT metrics (133-159 ms), comparable to what we saw with Llama 4 Maverick (94 ms).

- 

Licensing: Perhaps the biggest advantage for many developers is Qwen3’s Apache 2.0 license, which places fewer restrictions on commercial use than Llama 4’s license.

It’s worth noting that now that the ML community has had a chance to try Llama 4 models, there’s a lot of anecdotal evidence suggesting that these models have weaker performance than their benchmarks might indicate. Using r/LocalLLama jargon, they could have been “benchmaxxed” — optimized specifically for benchmark tests rather than real-world usage scenarios. This makes Qwen3’s strong performance even more notable, as early adopters are reporting consistent results across both benchmarks and practical applications.

# The thinking mode advantageThe thinking mode advantage

One unique feature of Qwen3 that deserves special attention is its hybrid thinking modes. These models can operate in two distinct modes:

- 

Thinking mode: The model takes time to reason step-by-step before delivering an answer, similar to chain-of-thought reasoning. This improves accuracy on complex problems.

- 

Non-thinking mode: For simpler queries where speed matters more than depth, the model can provide quick responses.

This flexibility is particularly valuable for production applications, as you can dynamically toggle between these modes, based on the query complexity. According to Qwen3’s benchmarks, this capability can take an evaluation score from a ~40% range (thinking disabled) to an ~80% range (thinking enabled). The SGLang integration with --reasoning-parser qwen3 makes this feature seamlessly available in our deployments.

# Building real applications by using Qwen3Building real applications by using Qwen3

Just like with our Llama 4 deployment, the Qwen3 endpoints we’ve set up are OpenAI API compatible. This means you can use them with any tools or libraries that support the OpenAI API format.

For instance, to send a chat request to your deployed Qwen3-32B model:

export ENDPOINT=$(sky serve status --endpoint qwen3-235b)
curl $ENDPOINT/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{
 "model": "Qwen/Qwen3-235B-A22B",
 "messages": [
 {
 "role": "user",
 "content": "Explain the concept of mixture-of-experts models in simple terms."
 }
 ]
}' | jq .

Or for Python users:

import os
import openai

ENDPOINT = os.getenv("ENDPOINT")
client = openai.Client(base_url=f"{ENDPOINT}/v1", api_key="None")

response = client.chat.completions.create(
 model="Qwen/Qwen3-32B",
 messages=[
 {"role": "user", "content": "Explain the concept of mixture-of-experts models in simple terms."},
 ],
 temperature=0
)

print(response.choices[0].message.content)

> **Mixture-of-Experts (MoE) Models: A Simple Explanation**

Imagine a company where a team of specialists works together to solve problems. When a new task arrives, a manager (the **gating network**) quickly assesses the problem and decides which specialists (the **experts**) are most qualified to handle it. Each expert focuses on their area of expertise—like marketing, engineering, or finance—and contributes their opinion. The manager then combines these opinions, giving more weight to the most relevant experts, to create a final solution.

**How It Works in Machine Learning:**
1. **Experts:** These are individual models (like small neural networks), each trained to excel at specific parts of a larger problem. For example, one might specialize in recognizing animals, another in vehicles, and so on.
2. **Gating Network:** This acts as the "manager." It examines the input (e.g., an image or text) and decides which experts are best suited to handle it. It assigns weights to each expert’s output—like saying, "Expert A should contribute 70%, Expert B 30%."
3. **Combining Outputs:** The final answer is a blend of the experts’ predictions, guided by the gating network’s weights. This ensures the model focuses computational resources only on the most relevant experts for each input.

**Why Use MoE?**
- **Efficiency:** Instead of using one giant model for everything, smaller experts handle specific tasks, saving time and resources.
- **Scalability:** You can add more experts (e.g., for new topics) without retraining the entire system.
- **Performance:** Specialization often leads to better accuracy, as experts can focus on their niche without getting confused by unrelated data.

**Real-World Analogy:** 
Think of MoE like a doctor’s office. When you visit, a nurse (the gate) assesses your symptoms and calls in the right specialists—a cardiologist, dermatologist, etc.—who collaborate to diagnose you. You don’t need every doctor to examine you; just the relevant ones, making the process faster and more effective.

**Key Insight:** 
MoE models work smart, not hard. By dividing labor among experts and using a gatekeeper to coordinate, they tackle complex problems efficiently—like a well-run team!

# Multilingual support: A global solutionMultilingual support: A global solution

One standout feature of Qwen3 is its amazing multilingual support spanning 119 languages and dialects. This makes these models particularly valuable for global applications or businesses serving diverse linguistic communities.

The model covers major language families, including Indo-European, Sino-Tibetan, Afro-Asiatic, Austronesian, Dravidian, Turkic and more. In practical terms, this means you can build applications that serve users in languages ranging from English and Chinese, to Arabic, Indonesian, Tamil or Turkish — all by using the same model.

# Conclusion: Open models at warp speedConclusion: Open models at warp speed

When I wrote the Llama 4 deployment guide, I genuinely didn’t expect we’d be discussing even better, smaller and more permissively licensed models the next week! Yet here we are with Qwen3, and it feels like we’re watching the open-source AI race accelerate to warp speed.

What’s most striking isn’t just the raw performance of these models, but how quickly the deployment barriers are falling. A year ago, running models of this caliber required specialized infrastructure and a team of ML engineers. Today, with a handful of YAML files and cloud credits, any developer with basic Python knowledge can deploy state-of-the-art AI.

For those looking to move these deployments from experimentation to production, all the security considerations, authentication mechanisms and scaling strategies we covered in the “Production readiness: From experiment to deployment” section of our Llama 4 post apply equally well here. The OpenAI-compatible API means you can plug these endpoints into existing workflows, with minimal changes.

The truth is, we’re entering an era where the bottleneck isn’t the models themselves, but our creativity in applying them. With Qwen3’s permissive Apache 2.0 license removing many of the commercial restrictions we’ve seen with other open models, the real question becomes not “can we deploy this?” but “what will we build with it?”.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Kim
Cloud Solutions Consultant

Contents

- Meet Qwen3: A new open standard

- Let’s deploy Qwen3 on Nebius AI Cloud

- Deployment configuration

- FP8 quantization: Doing more with less

- Launching the services

- Real-world performance

- Qwen3-235B-A22B (MoE model)

- Qwen3-32B (Dense model)

- Running your own benchmarks

- Running benchmarks on your deployed models

- Qwen3 vs. Llama 4: A quick comparison

- The thinking mode advantage

- Building real applications by using Qwen3

- Multilingual support: A global solution

- Conclusion: Open models at warp speed

## See also

### 

Serving Llama 4 models on Nebius AI Cloud with SkyPilot and SGLang

Let’s walk through how to get Llama 4 running on Nebius AI Cloud (recently integrated with SkyPilot) by using SGLang as the serving framework. This combo provides high throughput, efficient memory usage and none of the typical deployment headaches.

May 8, 2025
12 mins to read

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
