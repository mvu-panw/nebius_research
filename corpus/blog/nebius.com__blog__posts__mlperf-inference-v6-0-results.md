# MLPerf® Inference v6.0: Top-tier AI performance on NVIDIA Blackwell and Blackwell Ultra

Source: https://nebius.com/blog/posts/mlperf-inference-v6-0-results

Skip to main content

Today we’re announcing our latest submission to the MLPerf® Inference v6.0 benchmark suite, the industry-standard benchmark for measuring AI inference performance developed by MLCommons®.

In this round, Nebius continued to demonstrate strong results for AI inference workloads running on the latest NVIDIA platforms. Our submission includes systems built on NVIDIA Blackwell and Blackwell Ultra GPUs — NVIDIA HGX B200, NVIDIA HGX B300 and the rack-scale NVIDIA GB300 NVL72 system.

We benchmarked three models in this round: DeepSeek R1, Qwen3-VL 235B and gpt-oss 120B. Two of these models, Qwen3-VL 235B, a multimodal model capable of understanding both visual and text inputs; and gpt-oss 120B, a large open-source language model, were introduced to the MLPerf® Inference benchmark suite in this release. Together with DeepSeek R1, these benchmarks represent the type of frontier-scale models increasingly used in modern AI applications.

The MLPerf® benchmark suite continues to evolve alongside the AI industry, introducing new workloads that reflect the latest trends in large language and multimodal models. Our results in this round demonstrate Nebius’ readiness to run these frontier-scale workloads on cutting-edge AI infrastructure.

## Ready for frontier model inferenceReady for frontier model inference

In the MLPerf® Inference v6.0 round, Nebius benchmarked three NVIDIA AI systems built on the latest Blackwell and Blackwell Ultra architectures:

- NVIDIA HGX B200

- NVIDIA HGX B300

- NVIDIA GB300 NVL72

Overall, Nebius achieved 10 first-place results out of 16 benchmark submissions, along with other vendors submitting results. We also submitted five additional use cases where we were the only submitter, so we do not count them as first-place results. Below is the table with all 21 submissions:

 | Submission results*
 | HGX B200 (8 Blackwell GPUs)
 | HGX B300 (8 Blackwell Ultra GPUs)
 | GB300 NVL72 (1 Blackwell Ultra GPU)
 | GB300 NVL72 (8 Blackwell Ultra GPUs)
 | GB300 NVL72 (72 Blackwell Ultra GPUs)

 | DeepSeek R1 (server)
 | 51,693 / 1st [1]
 | 60,413 / 1st [2]
 | —
 | 64,510 / 1st [3]
 | 575,580 / 1st [4]

 | DeepSeek R1 (offline)
 | 58,582 / 1st [5]
 | 69,319 / 3rd [6]
 | —
 | 76,347 / 2nd [7]
 | 673,936 / 1st [8]

 | Qwen3-VL 235B (server)
 | —
 | 45 / — [9]
 | 43 / 1st [10]
 | —
 | —

 | Qwen3-VL 235B (offline)
 | —
 | 78 / — [11]
 | 61 / 3rd [12]
 | —
 | —

 | gpt-oss 120B (server)
 | 87,444 / 1st [13]
 | 100,437 / 5th [14]
 | 14,973 / — [15]
 | —
 | 1,096,770 / 1st [16]

 | gpt-oss 120B (offline)
 | 85,921 / 2nd [17]
 | 106,885 / 5th [18]
 | 15,372 / — [19]
 | —
 | 1,046,150 / 1st [20]

 | gpt-oss 120B (interactive)
 | 13,155 / — [21]
 | —
 | —
 | —
 | —

*Performance units: Tokens per second for LLM benchmarks (DeepSeek R1, gpt-oss 120B); queries per second for Qwen3-VL 235B (server); samples per second for Qwen3-VL 235B (offline). Higher values indicate better performance

Particularly notable are the results on the full-rack GB300 NVL72 system, where our engineering team demonstrated strong performance for large language model inference workloads running on 72 NVIDIA Blackwell Ultra GPUs across 18 nodes.

## Leading results on rack-size NVIDIA Blackwell Ultra systemsLeading results on rack-size NVIDIA Blackwell Ultra systems

One of the key results in this submission comes from the full-rack GB300 NVL72 system. In this configuration, 18 nodes with a total of 72 NVIDIA Blackwell Ultra GPUs work together to serve large-scale inference workloads.

Running DeepSeek R1 and gpt-oss 120B models on this system demonstrates how efficiently our engineering team can utilize the potential of latest Blackwell Ultra GPUs, including full-rack size installations.

Figure 1. Blackwell Ultra GPUs demonstrate strong scaling behavior for large model inference on a GB300 NVL72 system [3][4][7][8]

The results show linear scaling performance when moving from smaller configurations to the full-rack GB300 NVL72 system (Figure 1). As the number of GPUs increases, inference throughput grows accordingly, illustrating the ability of the platform to efficiently support large production deployments of modern AI models efficiently.

## Growing performance across GPU generationsGrowing performance across GPU generations

The MLPerf® Inference v6.0 results also illustrate how inference performance evolves across successive versions of the NVIDIA Blackwell and Blackwell Ultra platforms.

To demonstrate the performance differences across these systems, we compare results for two frontier LLMs, DeepSeek R1 and gpt-oss 120B, running on 8-GPU configurations of these NVIDIA platforms.

For the DeepSeek R1 benchmark, both server and offline inference scenarios show consistent performance improvements as we move from HGX B200 to HGX B300 and further to the GB300 NVL72 system.

Figure 2. DeepSeek R1 inference performance scaling across 8-GPU configurations of HGX B200, HGX B300 and GB300 NVL72 [1][2][3][5][6][7]

A similar pattern can be seen in the gpt-oss 120B benchmark when comparing HGX B200 and HGX B300 systems running 8 GPUs.

Figure 3. gpt-oss 120B inference performance scaling across 8-GPU configurations of HGX B200 and HGX B300 [13][14][17][18]

## ConclusionConclusion

The results of our MLPerf® Inference v6.0 submission demonstrate Nebius’ ability to maximize efficiency for modern AI inference workloads on the latest NVIDIA Blackwell and Blackwell Ultra platforms. From single-node systems to the full-rack GB300 NVL72 configuration, these benchmarks highlight the capability of our global infrastructure to support demanding large language and multimodal models.

Achieving these results requires constant work across the entire AI infrastructure stack. At Nebius, we continuously test, tune and optimize our platform to ensure that the newest NVIDIA hardware delivers its full potential in our customer environments. This includes everything from rigorous server acceptance testing to cloud software optimization and multi-stage cluster validation.

These results also reflect our close collaboration with NVIDIA, where joint engineering efforts help unlock the performance of new GPU platforms and bring them to production environments faster.

We continue to refine and improve every layer of our AI cloud platform to ensure our customers can run the most demanding AI workloads with confidence.

To learn how we can support your AI projects at scale, contact us.

## References

- MLPerf® v6.0 Inference Closed DeepSeek R1 server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0083. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0084. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0082. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0081. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0083. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0084. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0082. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed DeepSeek R1 offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0081. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed Qwen3-VL 235B server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0084. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed Qwen3-VL 235B server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed Qwen3-VL 235B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0084. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed Qwen3-VL 235B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0083. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B server, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0081. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0083. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0079. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B offline, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0081. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

- MLPerf® v6.0 Inference Closed gpt-oss 120B interactive, 30 March 2026, Retrieved from mlcommons.org/benchmarks/inference-datacenter/, entry 6.0-0083. Result verified by MLCommons Association. The MLPerf name and logo are registered and unregistered trademarks of MLCommons Association in the United States and other countries. All rights reserved. Unauthorized use strictly prohibited. See mlcommons.org for more information. ↵

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- Ready for frontier model inference

- Leading results on rack-size NVIDIA Blackwell Ultra systems

- Growing performance across GPU generations

- Conclusion

## See also

### 

MLPerf® Training v5.1: Leading results on NVIDIA Blackwell and Blackwell Ultra systems

We’re proud to share the results of our participation in the MLPerf® Training v5.1 benchmark, where Nebius showcased strong performance across several configurations of the latest NVIDIA Blackwell and Blackwell Ultra systems. This round continues our commitment to transparency and collaboration with the MLCommons® community, as we work to ensure the highest quality standards for training and fine-tuning next-generation GenAI models.

November 12, 2025
7 mins to read

### 

Nebius AI Cloud “Aether 3.5”: Frictionless compute for real world AI

This release introduces new serverless capabilities, the NVIDIA RTX PRO™ 6000 Blackwell Server Edition GPU for applied AI use cases, improved cluster configuration tools, streamlined data operations and platform-level enhancements that reduce routine complexity while preserving full control.

March 26, 2026
8 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

Sign in to save this post
Sign In
