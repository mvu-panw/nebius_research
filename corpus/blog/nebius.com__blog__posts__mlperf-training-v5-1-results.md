# MLPerf® Training v5.1: Leading results on NVIDIA Blackwell and Blackwell Ultra systems

Source: https://nebius.com/blog/posts/mlperf-training-v5-1-results

Skip to main content

We’re proud to share the results of our participation in the MLPerf® Training v5.1 benchmark, where Nebius showcased strong performance across several configurations of the latest NVIDIA Blackwell and Blackwell Ultra systems.

This round continues our commitment to transparency and collaboration with the MLCommons® community, as we work to ensure the highest quality standards for training and fine-tuning next-generation GenAI models.

Our results reflect not only the exceptional capabilities of the latest NVIDIA platforms but also the engineering depth behind Nebius AI Cloud. With this submission, we demonstrate the performance and efficiency of the top-notch GPUs that empower Nebius to benefit customers training the world’s most advanced models.

# Engineered for GenAI workloadsEngineered for GenAI workloads

Designed from the ground up for AI, Nebius’ infrastructure combines hardware innovation and software-level optimization, ensuring reproducible efficiency for modern AI workloads spanning multimodal training and LLM fine-tuning tasks.

Each layer of our AI cloud stack is carefully tuned to achieve consistent GPU utilization and minimize infrastructure overhead, from custom-designed servers to hypervisor-level optimizations that deliver bare-metal-class performance on virtual instances.

Our testing included two new models in the MLPerf suite, Llama-3.1-8B and FLUX.1, representing widely adopted LLM and multimodal architectures. Across all submissions, Nebius demonstrated stable and efficient results, confirming the platform’s readiness for high-performance GenAI training.

“This benchmark round introduced two new models, Llama-3.1-8B and FLUX.1-Schnell, making it especially interesting to observe their performance across different systems, ” said Dr Anton Lokhmotov, Founder and CEO of KRAI, a Founding Member of MLCommons® and the company supporting our MLPerf® benchmark verification. “Nebius showed solid performance results across the board, demonstrating their commitment to delivering outstanding value through the most advanced GPU systems in the industry”.

# Top-tier results across scalesTop-tier results across scales

In this MLPerf® Training v5.1 submission, Nebius benchmarked two systems powered by NVIDIA:

- NVIDIA HGX™ B300, tested with 8 GPUs on a single host

- NVIDIA HGX™ B200, tested with 8 GPUs on a single host, and in multi-node setups with 16 and 32 GPUs

We evaluated three models: Llama-2-70B (LoRA fine-tuning), Llama-3.1-8B (pre-training), and FLUX.1 (pre-training), measuring training time in minutes, where a lower value indicates better performance. The results are summarized below:

 | 
 | 8x NVIDIA Blackwell Ultra GPUs
 | 8x NVIDIA Blackwell GPUs
 | 16x NVIDIA Blackwell GPUs
 | 32x NVIDIA Blackwell GPUs

 | Llama-2-70B LoRA (training time/place)
 | 8.48 min / 1st [1]
 | 9.55 min / 2nd [2]
 | 5.82 min / 1st [3]
 | 3.10 min / 1st [4]

 | Llama-3.1-8B (training time/place)
 | 75.84 min / 1st [5]
 | 85.37 min / 6th [6]
 | 51.83 min / 1st [7]
 | 27.83 min / 1st [8]

 | FLUX.1 (training time/place)
 | -
 | -
 | -
 | 93.17 min / 1st [9]

In total, Nebius achieved seven first-place results out of nine submissions, reaffirming the platform’s efficiency in utilizing GPU resources for large-scale AI training.

We also resubmitted results from MLPerf Training v5.0 (Llama 3.1 405B training), maintaining continuity and demonstrating consistent excellence across benchmark generations.

# Blackwell Ultra delivers noticeable gainsBlackwell Ultra delivers noticeable gains

Across both Llama-2-70B LoRA and Llama-3.1-8B, the HGX B300 system showed an average 12.6% reduction in training time, underscoring the advantages of Blackwell Ultra — higher FP4 performance and expanded 270 GB memory per GPU.

Figure 1. Llama-2-70B LoRA training performance on 8x HGX B300 vs. 8x HGX B200 [1][2]

Figure 2. Llama-3.1-8B training performance on 8x HGX B300 vs. 8x HGX B200 [5][6]

These results confirm that the HGX B300 system is an excellent choice for performance-intensive foundation model training, offering superior speed and stability within Nebius’ virtualized environment.

# Predictable scaling of performancePredictable scaling of performance

Nebius also demonstrated excellent scaling on HGX B200 systems, increasing cluster size from 8 to 32 GPUs. Both Llama models showed ~3.1x speed-up when scaling from a single 8-GPU node to a 32-GPU cluster, confirming efficient interconnect utilization and software-level scaling.

Figure 3. Llama-2-70B LoRA scaling on HGX B200 from 8 to 32 GPUs shows excellent acceleration [2][3][4]

Figure 4. Llama-3.1-8B scaling on HGX B200 from 8 to 32 GPUs demonstrates efficient multi-node scalability. [6][7][8]

This scalability means that customers can train or fine-tune models faster simply by extending their cluster size — accelerating research cycles and shortening time-to-deployment for AI applications.

Such predictable scaling behavior helps enterprises and research teams to plan infrastructure deployments and extensions more carefully and with less risk.

# ConclusionConclusion

Our MLPerf® Training v5.1 submission reinforces Nebius’ prominent position in AI training performance, continuing the strong results achieved in previous rounds.

Through careful tuning and deep integration with our infrastructure, the NVIDIA HGX B300 and HGX B200 systems deliver consistent, high-efficiency performance for modern GenAI workloads. As a Reference Platform NVIDIA Cloud Partner, Nebius works closely with NVIDIA to ensure that these systems operate at their full potential, to achieve optimal utilization and stability in large-scale distributed training environments.

Our customers benefit from achieving exceptionally high GPU utilization in the cloud, which accelerates research and development, and creates new breakthroughs in language, vision and multimodal AI. From building large-scale models to deploying novel products, Nebius empowers innovators to turn ideas into tangible advances in artificial intelligence.

To learn how we can support your AI projects at scale, contact us.

## References

- MLPerf® v5.1 Training Closed Llama2-70b-lora, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0008. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama2-70b-lora, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0005. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama2-70b-lora, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0006. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama2-70b-lora, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0007. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama3.1-8b, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0008. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama3.1-8b, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0005. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama3.1-8b, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0006. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Llama3.1-8b, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0007. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v5.1 Training Closed Flux1, 12 November 2025, Retrieved from mlcommons.org/benchmarks/training/, entry 5.1-0007. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- Engineered for GenAI workloads

- Top-tier results across scales

- Blackwell Ultra delivers noticeable gains

- Predictable scaling of performance

- Conclusion

## See also

### 

Leveraging high-speed, rack-scale GPU interconnect with NVIDIA GB200 NVL72

Let’s explore one of the key features that makes the new NVIDIA GB200 NVL72 stand out: the fifth generation NVIDIA NVLink™ scale-up fabric. We’ll discuss how it redefines infrastructure by moving beyond the traditional 8-GPU NVLink. You’ll see a practical example of how to take advantage of this capability. Finally, we’ll examine a real-world use case: pre-training the Nemotron-4 340B LLM.

October 23, 2025
10 mins to read

### 

Nebius achieves NVIDIA Exemplar Status on NVIDIA H200 GPUs for training workloads

We’re proud to announce that Nebius is one of the first NVIDIA Cloud Partners to achieve NVIDIA Exemplar Status on NVIDIA H200 GPUs for training workloads. This recognition validates that Nebius meets NVIDIA’s rigorous standards for performance, resiliency, and scalability — addressing one of the most pressing challenges in AI infrastructure: ensuring consistent workload performance and predictable cost across clouds.

September 29, 2025
3 mins to read

### 

Nebius proves bare-metal-class performance for AI inference workloads in MLPerf® Inference v5.1

Today, we’re happy to share our new performance milestone — the latest submission of MLPerf® Inference v5.1 benchmarks, where Nebius achieved leading performance results for three AI systems accelerated by the most in-demand NVIDIA systems on the market: NVIDIA GB200 NVL72, HGX B200 and HGX H200.

September 10, 2025
6 mins to read

Sign in to save this post
Sign In
