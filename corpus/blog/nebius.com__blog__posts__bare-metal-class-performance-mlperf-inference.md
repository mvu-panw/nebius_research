# Nebius proves bare-metal-class performance for AI inference workloads in MLPerf® Inference v5.1

Source: https://nebius.com/blog/posts/bare-metal-class-performance-mlperf-inference

Skip to main content

Today, we’re happy to share our new performance milestone — the latest submission of MLPerf® Inference v5.1 benchmarks, where Nebius achieved leading performance results for three AI systems accelerated by the most in-demand NVIDIA systems on the market: NVIDIA GB200 NVL72, HGX B200 and HGX H200.

Just this spring, we successfully achieved top-tier performance numbers in the MLPerf Training round by MLCommons®, confirming the smooth and scalable work of Nebius clusters for multi-host, distributed training. The current submission demonstrates Nebius’ ability to deliver outstanding token throughput for inference workloads, proving significant performance gains across all tested configurations.

MLPerf® is a peer-reviewed benchmark suite developed by MLCommons® to evaluate machine learning training and inference performance. It helps industry players and potential customers to navigate through the complexities of measuring performance of AI infrastructure. We appreciate the transparency MLCommons® brings to accumulating and sharing performance results, and how it enables AI practitioners and ML teams to make more informed decisions about their AI infrastructure investments.

This round of MLCommons® benchmarks reflects the continuous improvements by our engineering team to deliver exceptional value for our customers, that make Nebius a leading choice among AI infrastructure providers.

# Virtualized instances with bare-metal performanceVirtualized instances with bare-metal performance

This benchmarking submission gives us the opportunity to showcase our engineering expertise in building high-performance virtualized environments for modern Gen AI workloads. We run our virtual GPU instances without virtualizing NVIDIA GPUs and NVIDIA ConnectX InfiniBand adapters, which results in zero performance degradation and allows us to stay on par with the best industry benchmarks.

MLPerf® Inference v5.1 results, achieved on single-host installations, prove that Nebius AI Cloud delivers top-tier performance results for inference of large foundational models like Llama 2 70B and Llama 3.1 405B models.

# Raising the bar for NVIDIA GB200 NVL72 performanceRaising the bar for NVIDIA GB200 NVL72 performance

With increased GPU memory, the NVIDIA GB200 NVL72 can easily handle large foundational models, equipped with NVFP4 precision, fifth-generation NVIDIA NVLink™, NVLink Switch System and high-speed NVIDIA InfiniBand networking for unparalleled GPU-to-GPU interconnects — making these systems a great choice for distributed training and reasoning model inference.

In MLPerf® benchmarks v5.1, Nebius AI Cloud sets a new peak in performance delivered by NVIDIA GB200 NVL72 systems — compared to the best results of the previous round, our one-host installation achieved 6.7% and 14.2% performance increases running Llama 3.1 405B inference in offline and server modes, respectively [1][2][3][4]. These two numbers also hold the first place for Nebius, among other MLPerf® Inference v5.1 submitters for this model on GB200 systems.

 | 
 | MLPerf® Inference v5.0, best result
 | MLPerf® Inference v5.1, best result
 | Performance increase

 | Llama 3.1 405B, offline mode
 | 801.91 tokens/s [1]
 | 855.82 tokens/s (Nebius) [3]
 | 6.7%

 | Llama 3.1 405B, server mode
 | 522.12 tokens/s [2]
 | 596.11 tokens/s (Nebius) [4]
 | 14.2%

Table 1. Nebius sets new peak performance benchmarks for Llama 3.1 405B inference on NVIDIA GB200 NVL72

Compared to the previous generation of NVIDIA GPUs, the GB200 NVL72 demonstrated a significant leap in inference throughput — one host with 4x Blackwell GPUs achieved a 54.8% performance gain compared to an H200 host powered by 8x GPUs, while normalized per-chip comparison showed a 3.1x performance increase (Figure 1) [3][5].

Figure 1. Per-chip and per-host comparison of GB200 NVL72 and HGX H200 inference throughput [3][5]

# Demonstrating best-in-class results for HGX platformsDemonstrating best-in-class results for HGX platforms

Another NVIDIA Blackwell system Nebius presented in this submission — HGX B200 — shows very promising performance for LLM inference, confirming the advantages of the new model over the previous generation of air-cooled HGX systems.

Running Llama 3.1 405B inference on NVIDIA HGX B200, we recorded 1,660 tokens/s in offline mode and 1,280 tokens/s in server scenario [6][7]. Compared to our NVIDIA HGX H200 results in this MLPerf® submission, we see 3x and 4.3x performance increases in offline and server scenarios respectively [5][8].

Figure 2. Per-host comparison of NVIDIA HGX B200 and HGX H200 inference throughput for Llama 3.1 405B [5][6][7][8]

When it comes to the Llama 2 70B model, the difference between HGX B200 and HGX H200 is also substantial. The B200 system outperforms the H200 3x and 2.9x times, by delivering 101,611 and 101,246 tokens/s in server and offline modes, respectively [9][10][11][12].

Figure 3. Per-host comparison of NVIDIA HGX B200 and HGX H200 inference throughput for Llama 2 70B [9][10][11][12]

For both models, Nebius demonstrated the best performance results in server mode, while in offline and interactive scenarios it shows parity with other submitters.

# Proving the efficient way to scale AI workloadsProving the efficient way to scale AI workloads

NVIDIA Hopper systems are an excellent choice for building cost-optimized inference environments for AI applications. Featuring increased GPU memory, a battle-tested software stack and affordable pricing, NVIDIA HGX H200 systems remain popular among customers using Nebius’ self-service and reserved capacity options.

In this submission, Nebius recorded that Llama 70B inference on HGX H200 systems gives 11% performance increase compared to the best results achieved on H100-powered systems from the MLPerf® Inference v5.0 submission (Figure 4) [9][10][13][14].

Figure 4. Per-host comparison of NVIDIA HGX H200 and HGX H100 inference throughput for Llama 2 70B [9][10][13][14]

Follow the link to see the full list of MLPerf® Inference v5.1 benchmarking results.

# ConclusionConclusion

Researchers and engineers from MLCommons® do a great job of supplying the industry with standardized benchmarks to measure inference and training performance on modern AI platforms. These benchmarks help AI companies stay informed about the current state of AI infrastructure, while providing GPU vendors and neoclouds with a measurement system to evaluate and improve the quality of their products.

But synthetic benchmarks only reflect general trends in how AI infrastructure performance evolves. In real-world scenarios, each case is unique, with multiple dependencies and hidden factors that can hinder or accelerate system performance. That’s why we offer our customers the ability to thoroughly test and fine-tune AI clusters for their specific machine learning setups.

These submission results confirm Nebius’ ability to run AI workloads in highly efficient virtualized environments while delivering performance on par with bare metal installations. They reflect the company’s commitment to exceptional AI infrastructure, built on custom hardware, proprietary software, and energy-efficient data centers. This combination gives AI labs and enterprises supercomputer-level performance and reliability, coupled with the flexibility and simplicity of a hyperscaler.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- Virtualized instances with bare-metal performance

- Raising the bar for NVIDIA GB200 NVL72 performance

- Demonstrating best-in-class results for HGX platforms

- Proving the efficient way to scale AI workloads

- Conclusion

## See also

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

Fault-tolerant training: How we build reliable clusters for distributed AI workloads

When starting a job, you expect it to run without interruptions. This expectation holds true across many domains, but it resonates especially deeply with machine learning engineers who launch large-scale pre-training jobs. Maintaining a stable training environment is crucial for delivering AI results on schedule and within budget constraints.

August 28, 2025
9 mins to read

### 

Introducing Nebius MCP Server: The LLM-native way to manage your AI Cloud

Skip the CLI commands and web console clicks — just ask Claude about your cloud infrastructure. Today, we’re excited to announce the Nebius MCP Server, our integration that connects Claude by Anthropic, or other AI chatbots, to the Nebius AI Cloud infrastructure.

July 16, 2025
5 mins to read

[1] MLPerf® v5.0 Inference Closed Llama3.1-405B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 2 April 2025, entry 5.0-0076. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[2] MLPerf® v5.0 Inference Closed Llama3.1-405B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 2 April 2025, entry 5.0-0076. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[3] MLPerf® v5.1 Inference Closed Llama3.1-405B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0078. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[4] MLPerf® v5.1 Inference Closed Llama3.1-405B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0078. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[5] MLPerf® v5.1 Inference Closed Llama3.1-405B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[6] MLPerf® v5.1 Inference Closed Llama3.1-405B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0077. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[7] MLPerf® v5.1 Inference Closed Llama3.1-405B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0077. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[8] MLPerf® v5.1 Inference Closed Llama3.1-405B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[9] MLPerf® v5.1 Inference Closed Llama2-70B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[10] MLPerf® v5.1 Inference Closed Llama2-70B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[11] MLPerf® v5.1 Inference Closed Llama2-70B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0077. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[12] MLPerf® v5.1 Inference Closed Llama2-70B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 9 September 2025, entry 5.1-0077. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[13] MLPerf® v5.0 Inference Closed Llama2-70B server. Retrieved from mlcommons.org/benchmarks/inference-datacenter 2 April 2025, entry 5.0-0057. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

[14] MLPerf® v5.0 Inference Closed Llama2-70B offline. Retrieved from mlcommons.org/benchmarks/inference-datacenter 2 April 2025, entry 5.0-0057. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See www.mlcommons.org for more information.

Sign in to save this post
Sign In
