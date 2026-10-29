# OpenHands trajectories with Qwen3-Coder-480B-A35B-Instruct

Source: https://nebius.com/blog/posts/openhands-trajectories-with-qwen3-coder-480b

Skip to main content

Reinforcement learning demonstrates state-of-the-art results on software engineering tasks¹ ², yet it presents significant infrastructure challenges beyond simple compute scale. It requires complex MLOps workflows, including simultaneous stages of inference (collecting traces from the latest policy) and training (updating the policy) that typically require asynchronous setups for efficiency, as well as fine-grained experimentation to resolve instabilities and achieve high performance.

In contrast, behavioral cloning and model distillation, where models learn directly from curated demonstrations, require only standard supervised fine-tuning (SFT) pipelines and serve as a powerful baseline. Among these approaches, rejection fine-tuning (RFT) has proven particularly effective: by training on successful trajectories filtered from multiple solution attempts, RFT captures high-quality behavior without the infrastructure overhead of RL.

While our research primarily focuses on RL, given the strong performance of RFT, we are contributing our accumulated trajectories to support this approach. To expand the set of available datasets containing multi-turn trajectories based on open-source scaffoldings and models, we release nebius/SWE-rebench-openhands-trajectories: 67,074 agent trajectories solving GitHub issues across 1,823 Python repositories from SWE-rebench. The trajectories were generated using Qwen3-Coder-480B-A35B-Instruct³ running on OpenHands (v0.54.0)⁴, one of the most widely adopted open-source agent scaffolding frameworks.

To demonstrate the dataset’s utility, we release RFT checkpoints at two scales:

- 

30B (fine-tuned from Qwen3-30B-A3B-Instruct-2507³): Matches the specialized Qwen3-Coder-30B-A3B-Instruct at 50.3% Pass@1 on SWE-bench Verified.

- 

235B (fine-tuned from Qwen3-235B-A22B-Instruct-2507³): Achieves 61.7% Pass@1 — outperforming the 30B coding specialist model (50.0%) while using half the parameters of Qwen3-Coder-480B-A35B-Instruct (66.5%).

Dataset: 67,074 trajectories | 3,792 resolved issues | 1,823 repositories

Models: 30B, 235B checkpoints

License: cc-by-4.0 for data, Apache-2.0 for models

# DatasetDataset

We collected trajectories from GitHub issues across Python repositories sourced from SWE-rebench, a collection of real-world software engineering tasks.

Model configuration: All trajectories were generated using Qwen3-Coder-480B-A35B-Instruct, one of the most powerful open-source code generation models available to date.

Agent scaffolding: We used OpenHands (v0.54.0), which provides a comprehensive framework for repository exploration, file editing, command execution and test validation.

Trajectory format: Each trajectory contains a sequence of messages with roles of system, user, assistant or tool:

- 

Assistant messages contain function calls in structured tool format, which often yields superior performance on modern architectures compared to the string-formatted commands.

- 

The agent maintains a linear message history, allowing efficient training on the complete sequence of steps.

- 

arguments are serialized to string format for storage efficiency. When training on this data, you may need to deserialize it first to ensure chat templates apply the same formatting (including any additional tags or text) during both training and inference.

The exit_status field contains submit in case the agent completes a trajectory with a terminating action, or an error message from the OpenHands agent otherwise.

Filtering process: We removed all trajectories where the generated code patches failed to apply to the target repository state. This ensures every trajectory represents a valid solution attempt.

After filtering, our dataset contains 32,161 successful trajectories with 67,074 total solution attempts.

 | 
 | 
 | SWE-bench/SWE-smith-trajectories⁶
 | Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k⁸
 | nebius/SWE-agent-trajectories⁹
 | SWE-Gym/OpenHands-Sampled-Trajectories¹⁰
 | R2E-Gym/R2EGym-SFT-Trajectories¹¹
 | nebius/SWE-rebench-openhands-trajectories (Ours)

 | Scaffolding
 | —
 | SWE-agent⁷
 | mini-swe-agent-plus
 | Closed-source
 | OpenHands⁴
 | OpenHands
 | OpenHands (v0.54.0)

 | Bootstrapping model
 | —
 | claude-3-7-sonnet-20250219, claude-3-5-sonnet-20241022, gpt-4o-2024-08-06
 | Unknown*
 | Qwen2.5-72B-Instruct; Llama3-70B-Instruct
 | gpt-4o-2024-08-06; claude-3-5-sonnet-20241022
 | Claude-Sonnet-3.5-v2
 | Qwen3-Coder-480B-A35B-Instruct

 | 
 | Uses function calling
 | ✅
 | ❌
 | ❌
 | ✅
 | ✅
 | ✅

 | Repositories
 | 
 | 129
 | 123
 | 1,202
 | 11
 | Unknown*
 | 1,823

 | Issues
 | Resolved Count
 | 7,270
 | 10,894
 | 838
 | 294
 | 2,048
 | 3,792

 | 
 | Real-world/Synthetic
 | Synthetic
 | Synthetic
 | Real-world
 | Real-world
 | Real-world
 | Real-world

 | Trajectories
 | Total Count
 | 49,897
 | 65,994
 | 80,036
 | 6,055
 | 3,231
 | 67,074

 | 
 | Successful Count
 | 21,513
 | 65,994
 | 13,389
 | 491
 | 3,231
 | 32,161

 | Turns
 | Max Count
 | 151
 | 157
 | 408
 | 50
 | 42
 | 100

 | 
 | Average Count
 | 30.2
 | 34.3
 | 26.4
 | 18.9
 | 16.1
 | 64.3

Table 1: Comparison of statistics across different datasets containing multi-turn trajectories of agent interactions with executable SWE environments. (Scroll to the right).

*Statistic value could not be derived from available data.

Our dataset provides 3× more successful trajectories and covers 1.5× more Python repositories than existing alternatives solving real-world issues, all while relying on fully open-source infrastructure.

# Models and resultsModels and results

We evaluate our fine-tuned models on two complementary benchmarks.

- 

SWE-bench Verified: A challenging, widely adopted benchmark containing 500 curated issues. Due to infrastructure difficulties in applying golden patches for 16 instances, we report results on the subset of 484.

While we cannot definitively determine whether base models encountered this data during pretraining, we explicitly excluded all SWE-bench Verified issues and repositories from our training data to ensure that observed improvements stem from fine-tuning rather than data leakage.

Excluded instances (click to expand)

django__django-10097, matplotlib__matplotlib-20488, psf__requests-1724, psf__requests-1766, psf__requests-1921,
psf__requests-2317, psf__requests-2931, psf__requests-5414, pylint-dev__pylint-4661, pytest-dev__pytest-5262, 
pytest-dev__pytest-7521, scikit-learn__scikit-learn-12973, scikit-learn__scikit-learn-14710, sphinx-doc__sphinx-10466, 
sympy__sympy-13091, sympy__sympy-22714

- SWE-rebench September⁵: A smaller but temporally fresh evaluation set collected after all model training cutoffs, ensuring zero contamination at the issue level. Our training data similarly excludes all SWE-rebench September instances.

We applied rejection sampling fine-tuning (RFT) with a maximum sequence length of 131k tokens.

 | 
 | 
 | Max Turns = 100
 | 
 | 
 | 
 | Max Turns = 500
 | 
 | 
 | 

 | 
 | 
 | SWE-bench Verified (484)
 | SWE-bench Verified (484)
 | SWE-rebench September (49)
 | SWE-rebench September (49)
 | SWE-bench Verified (484)
 | SWE-bench Verified (484)
 | SWE-rebench September (49)
 | SWE-rebench September (49)

 | Model
 | Size
 | Pass@1
 | Pass@5
 | Pass@1
 | Pass@5
 | Pass@1
 | Pass@5
 | Pass@1
 | Pass@5

 | 30B scale
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 

 | Qwen3-30B-A3B-Instruct-2507³
 | 30B
 | 25.2±0.7
 | 44.8
 | 11.8±1.5
 | 24.4
 | 25.7±0.5
 | 44.2
 | 14.2±1.1
 | 26.5

 | Qwen3-Coder-30B-A3B-Instruct³
 | 30B
 | 51.9±0.2
 | 67.3
 | 28.7±1.1
 | 42.8
 | 50.0±0.5
 | 63.0
 | 28.1±1.5
 | 38.7

 | nebius/SWE-rebench-openhands-Qwen3-30B-A3B (Ours)
 | 30B
 | 49.7±0.9 (+24.5)
 | 65.4 (+20.6)
 | 28.1±1.5 (+16.3)
 | 38.7 (+14.3)
 | 50.3±0.7 (+24.6)
 | 68.3 (+24.1)
 | 28.1± 1.0(+13.9)
 | 38.7 (+12.2)

 | 100B+ scale
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 

 | GLM-4.5-Air²
 | 106B
 | 58.2±0.2
 | 73.2
 | 33.8±1.2
 | 42.8
 | —
 | —
 | —
 | —

 | 200B+ scale
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 

 | Qwen3-235B-A22B-Instruct-2507³
 | 235B
 | 45.2±0.8
 | 65.9
 | 29.3±2.4
 | 44.8
 | 46.2±0.4
 | 67.5
 | 25.3±1.9
 | 40.8

 | nebius/SWE-rebench-openhands-Qwen3-235B-A22B (Ours)
 | 235B
 | 59.9±0.1 (+14.7)
 | 73.9 (+8.0)
 | 35.1±1.0 (+5.8)
 | 46.9 (+2.1)
 | 61.7±0.9 (+15.5)
 | 74.3 (+6.8)
 | 34.2±1.5 (+8.9)
 | 44.8 (+4.0)

 | 300B+ scale
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 
 | 

 | GLM-4.5²
 | 355B
 | 64.4 ± 0.5
 | 76.2
 | 33.8 ± 1.7
 | 44.8
 | —
 | —
 | —
 | —

 | Qwen3-Coder-480B-A35B-Instruct³
 | 480B
 | 64.7±0.5
 | 75.8
 | 36.3±1.6
 | 44.8
 | 66.5±0.4
 | 77.8
 | 35.5±1.4
 | 42.8

Table 2. Pass@1 with standard error of the mean and Pass@5 for OpenHands agent with the maximum number of turns set to 100 and 500. Deltas vs. base models are shown in parentheses for fine-tuned models. Metrics are reported in percentages. (Scroll to the right).

# Reproducing OpenHands evaluationReproducing OpenHands evaluation

Evaluation results for agent-based systems are highly sensitive to both model and scaffolding configurations. As OpenHands continues to evolve, results can vary significantly between releases. To ensure reproducibility, we pin our evaluation to a specific library version (v0.54.0) and document all key configuration parameters:

Tool call format: Tool calls in messages from OpenHands agents used as inputs to LLMs can be formatted as strings or lists of dictionaries — different inference engines expect different formats, which affects behavior. This is controlled by the native_tool_calling parameter (None, true or false). To avoid relying on automatic heuristics for input tool call formatting (default None behavior), we recommend explicitly setting this parameter (we used true since all our models supported tool formatting on the inference engine’s side).

Tool call post-processing for Qwen3-Coder-30B-A3B-Instruct: While the larger Qwen3-Coder-480B-A35B-Instruct correctly formatted tool calls for the OpenHands scaffolding, the smaller Qwen3-Coder-30B-A3B-Instruct struggled, causing tool formatting errors. To match the quality reported by the Qwen3 team for the smaller coder model¹², we applied an additional post-processing for assistant steps on the OpenHands side¹³.

Security settings: The security_risk parameter introduced in v0.55.0 controls which operations the agent can perform and requires the agent to manually set a new environment variable (see bug report. To avoid this, we stick to v0.54.0.

History management: To maintain the linear message history required for efficient training, we disabled history truncation when the LLM hits its maximum sequence length (enable_history_truncation=false, enable_default_condenser=true, condenser.type=noop) and prevented LLM access to the truncation tool (enable_condensation_request=false).

Infrastructure stability: The OpenHands README cautions that max_workers>1 is not well-tested. We observed that higher parallelism introduces infrastructure instability, particularly Docker build failures due to timeouts. To facilitate data collection, we increased timeouts during bootstrapping 2–10×, which enabled operation at max_workers=75, but this didn’t guarantee successful trajectory collection for all parallel instances. We recommend max_workers=1 for reliable evaluation.

Patch application: OpenHands-generated patches require specific post-processing to be applied correctly. Using evaluation pipelines not designed to handle OpenHands predictions can result in valid patches being rejected. We implement the required post-processing, resulting in a near-zero patch application failure rate.

While max_iterations (the maximum number of turns) is commonly reported, it alone is insufficient for full reproduction. To enable reproduction of the reported results, we provide a completed reproducibility checklist for our experiments and encourage researchers to use the same checklist when reporting results:

 | 
 | Parameter
 | Values for -Coder- models
 | values for -Instruct-2507 models
 | Values for others

 | Scaffolding
 | Release
 | OpenHands v0.54.0 + patch from¹³
 | OpenHands v0.54.0
 | OpenHands v0.54.0

 | 
 | config.toml
 | nebius/SWE-rebench-openhands-trajectories/config.toml
 | nebius/SWE-rebench-openhands-trajectories/config.toml
 | nebius/SWE-rebench-openhands-trajectories/config.toml

 | Model
 | Name
 | Qwen/Qwen3-Coder-480B-A35B-Instruct, Qwen/Qwen3-Coder-30B-A3B-Instruct
 | Qwen/Qwen3-30B-A3B-Instruct-2507, nebius/SWE-rebench-openhands-Qwen3-30B-A3B, nebius/SWE-rebench-openhands-Qwen3-235B-A22B
 | GLM-4.5-Air, GLM-4.5, Qwen3-235B-A22B-Instruct-2507

 | 
 | dtype
 | bfloat16
 | bfloat16
 | float8

 | 
 | Maximum sequence length
 | 131,072
 | 131,072
 | 131,072 for GLM-4.5-Air, GLM-4.5 262,144 for Qwen3-235B-A22B-Instruct-2507*

 | 
 | Tool formatter
 | vLLM’s “qwen3_coder”
 | vLLM’s “hermes”
 | —

 | 
 | Sampling Parameters
 | Recommended for each model setting, see config.toml
 | Recommended for each model setting, see config.toml
 | Recommended for each model setting, see config.toml

 | Inference engine
 | 
 | vLLM/vLLM-openai:v0.9.0
 | vLLM/vLLM-openai:v0.9.0
 | Nebius Token Factory

 | 
 | Cli command
 | vLLM_USE_V1=1 vLLM serve Qwen/Qwen3-Coder-480B-A35B-Instruct --tensor-parallel-size 8 --served-model-name qwen_3_coder --disable-log-requests --enable-prefix-caching --max-model-len 131072 --enable-auto-tool-choice --tool-call-parser qwen3_xml --tool-parser-plugin ./qwen3coder_tool_parser.py 
 | vLLM_USE_V1=1 vLLM serve Qwen/Qwen3-30B-A3B-Instruct-2507 --tensor-parallel-size 8 --served-model-name qwen_3_instruct_2507 --disable-log-requests --enable-prefix-caching --max-model-len 131072 --enable-auto-tool-choice --tool-call-parser hermes
 | —

Table 3. Reproducibility checklist. (Scroll to the right).

*We used sequence length of 262k for Qwen3-235B-A22B-Instruct-2507 opposite to the value of 131k for all others, but it never exceeded 131k tokens during evaluation, thus its results should be comparable.

# Our fine-tuning methodologyOur fine-tuning methodology

We applied standard RFT training using exclusively successful trajectories (those having resolved=true) with the following configuration:

 | 
 | nebius/SWE-rebench-openhands-Qwen3-30B-A3B (Ours)
 | nebius/SWE-rebench-openhands-Qwen3-235B-A22B (Ours)

 | Base model
 | Qwen3-30B-A3B-Instruct-2507³
 | Qwen3-235B-A22B-Instruct-2507³

 | Batch size
 | 32
 | 32

 | Sequence length
 | 131,072
 | 131,072

 | Epochs
 | 5
 | 3

 | Total tokens seen
 | 8.9B
 | 5.3B

 | Parameters tuned
 | All except: MoE router weights and embeddings
 | All except: MoE router weights and embeddings

 | Optimizer
 | AdamW (beta_1=0.9, beta_2=0.999, epsilon=1e-8)
 | AdamW (beta_1=0.9, beta_2=0.999, epsilon=1e-8)

 | Weight decay
 | 0.1
 | 0.1

 | Gradient clipping norm
 | 1.0
 | 1.0

 | Learning rate
 | cosine schedule with the maximum learning rate of 4e-6
 | cosine schedule with the maximum learning rate of 4e-6

 | Learning rate warmup steps
 | 9
 | 9

 | Losses
 | CE (no MoE-specific balancing losses)
 | CE (no MoE-specific balancing losses)

 | Compute
 | 16x NVIDIA B200 for 65 hours
 | 32x NVIDIA H200 for 60 hours

Table 4. Fine-tuning hyperparameters

# ConclusionConclusion

We contribute three resources to the community: (1) nebius/SWE-rebench-openhands-trajectories, 67,074 open-source trajectories with 3× more successful attempts than alternatives, (2) two RFT checkpoints achieving 50.3% (30B) and 61.7% (235B) Pass@1 on SWE-bench Verified, and (3) complete reproducibility documentation for fine-tuning and OpenHands evaluation. All are released under permissive licenses.

## ContributorsMaria Trofimova, Anton Shevtsov, Ibragim Badertdinov, Konstantin Pyaev, Simon Karasik, Alexander Golubev＊

MT performed fine-tuning; MT and AS ran data collection and evaluation; AS and IB helped debugging; KP and SK helped with infrastructure. AG led the project.

＊Correspondence to alex_golubev@nebius.com

## Citation information
Please cite as:

 | Trofimova et al., "OpenHands Trajectories with Qwen3-Coder-480B-A35B-Instruct", Nebius blog, 2025.

BibTeX citation:

 | @article{trofimova2025openhandstrajs,
  title={OpenHands Trajectories with Qwen3-Coder-480B-A35B-Instruct},
  author={Trofimova, Maria and Shevtsov, Anton and Ibragim, Badertdinov and Pyaev, Konstantin and Karasik, Simon and Golubev, Alexander},
  year={2025},
  journal={Nebius blog},
  note={}
 }

## References

- Team, K., Bai, Y., Bao, Y., Chen, G., Chen, J., Chen, N., ... & Zhang, H. (2025). Kimi k2: Open agentic intelligence. ArXiv: arxiv.org/abs/2507.20534 ↵ 

- Zeng, A., Lv, X., Zheng, Q., Hou, Z., Chen, B., Xie, C., ... & Zhou, Z. (2025). Glm-4.5: Agentic, reasoning, and coding (arc) foundation models. ArXiv: arxiv.org/abs/2508.06471. ↵ 

- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., ... & Qiu, Z. (2025). Qwen3 technical report. ArXiv: arxiv.org/abs/2505.09388 ↵ 

- Wang, X., Li, B., Song, Y., Xu, F. F., Tang, X., Zhuge, M., ... & Neubig, G. (2024). Openhands: An open platform for ai software developers as generalist agents. ArXiv: arxiv.org/abs/2407.16741 ↵ 

- Badertdinov, I., Golubev, A., Nekrashevich, M., Shevtsov, A., Karasik, S., Andriushchenko, A., ... & Yangel, B. (2025). SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents. ArXiv: arxiv.org/abs/2505.20411 ↵ 

- Yang, J., Lieret, K., Jimenez, C. E., Wettig, A., Khandpur, K., Zhang, Y., ... & Yang, D. (2025). Swe-smith: Scaling data for software engineering agents. ArXiv: arxiv.org/abs/2504.21798 ↵ 

- John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik R Narasimhan, & Ofir Press (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. In The Thirty-eighth Annual Conference on Neural Information Processing Systems. ArXiv: arxiv.org/abs/2405.15793 ↵ 

- Wang, Q., Zhang, H., Fu, J., Fu, K., Liu, Y., Zhang, T., ... & Zhou, G. (2025). Klear-AgentForge: Forging Agentic Intelligence through Posttraining Scaling. ArXiv: arxiv.org/abs/2511.05951 ↵ 

- Badertdinov, I., Trofimova, M., Anapolskiy, Y., Abramov, S., Zainullina, K., Golubev, A., Polezhaev, S., Litvintseva, D., Karasik, S., Fisin, F., Skvortsov, S., Nekrashevich, M., Shevtsov, A., & Yangel, B. (2024). Scaling data collection for training software engineering agents. Nebius blog: nebius.com/blog/posts/scaling-data-collection-for-training-swe-agents ↵ 

- Pan, J., Wang, X., Neubig, G., Jaitly, N., Ji, H., Suhr, A., & Zhang, Y. (2024). Training software engineering agents and verifiers with swe-gym. ArXiv: arxiv.org/abs/2412.21139 ↵ 

- Jain, N., Singh, J., Shetty, M., Zheng, L., Sen, K., & Stoica, I. (2025). R2e-gym: Procedural environments and hybrid verifiers for scaling open-weights swe agents. ArXiv: arxiv.org/abs/2504.07164v1 ↵ 

- Team, Q. (2025, July 22). QWEN3-Coder: Agentic coding in the world. Qwenlm blog: qwenlm.github.io/blog/qwen3-coder/ ↵ 

- OpenHands. (n.d.). Fix: Normalize malformed tags (QWEN3) by enyst · pull request #10539 · OpenHands/OpenHands. GitHub: github.com/OpenHands/OpenHands/pull/10539 ↵ 

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

#### See the contributors

Contents

- Dataset

- Models and results

- Reproducing OpenHands evaluation

- Our fine-tuning methodology

- Conclusion

- Contributors

- Citation information

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Behind SWE-rebench: Infrastructure to collect massive datasets of SWE tasks and evaluate agents at scale

Research on SWE agents involves building and running thousands of containers, quickly surpassing the limits of a single host. Our AI R&D team unveils the large-scale infrastructure that powers this research — the backbone behind recent releases such as SWE-rebench — and an open-source part of it to support the broader community.

November 7, 2025
14 mins to read

### 

SWE-rebench: A continuously updated benchmark for SWE LLMs

Our AI R&D team presents SWE-rebench, a new benchmark for evaluating agentic LLMs on a continuously updated and decontaminated set of real-world software engineering tasks mined from real GitHub repositories. Our goal with this benchmark is to make evaluation of software engineering LLMs more transparent, reproducible and focused on core model capabilities.

May 14, 2025
1 min to read

Sign in to save this post
Sign In
