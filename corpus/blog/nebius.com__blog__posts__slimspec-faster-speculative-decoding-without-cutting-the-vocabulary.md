# SlimSpec: faster speculative decoding without cutting the vocabulary

Source: https://nebius.com/blog/posts/slimspec-faster-speculative-decoding-without-cutting-the-vocabulary

Skip to main content

Speculative decoding only helps in production when the drafter is both fast and accepted often enough by the target model. One hidden bottleneck is the draft model’s LM head: even a lightweight drafter may still spend meaningful compute projecting hidden states into a large vocabulary.

SlimSpec is our low-rank draft LM-head architecture for speculative decoding. Instead of shrinking the vocabulary, it compresses the drafter’s hidden representation while preserving full-vocabulary support. In our EAGLE-3 experiments, SlimSpec reduces LM-head cost by 4-5x versus the standard unembedding projection while keeping acceptance quality competitive.

This research is part of the same direction behind Custom Speculator Training in Nebius Token Factory: train the draft model for the workload you actually serve, then evaluate it with the base model on real traffic. If you are running production inference with repeatable latency or throughput pressure, read the Custom Speculator docs or talk to our team about a spec decoding performance review.

SlimSpec has been submitted to NeurIPS; the preprint is available on ArXiv.

## What this changes in productionWhat this changes in production

For production teams, speculative decoding is not just about making a benchmark faster. The useful question is whether the drafter can propose tokens quickly enough, and accurately enough, to improve the serving path users actually experience.

Vocabulary-reduction methods can make the LM head cheaper, but they introduce a tradeoff: once the drafter cannot propose tokens outside a reduced vocabulary, acceptance quality can suffer. SlimSpec takes a different path. It keeps full-vocabulary support and reduces the cost of the projection itself.

That matters for workloads where throughput, latency, and acceptance rate all have to move together: coding assistants, structured-output agents, enterprise copilots, and other repeated production patterns where generic speculative decoding may leave performance on the table.

## Why the draft LM-head becomes a bottleneckWhy the draft LM-head becomes a bottleneck

In auxiliary-head speculative decoding methods such as MEDUSA, Hydra, and the EAGLE family, the draft-side computation naturally splits into two parts:

Tdraft=Tbackbone+TheadT_{\mathrm{draft}} = T_{\mathrm{backbone}} + T_{\mathrm{head}}Tdraft​=Tbackbone​+Thead​

The backbone produces draft hidden states h. The LM-head maps those hidden states to vocabulary logits. The standard projection is performed by the unembedding matrix:

logits=Wfullh,Wfull∈RV×d\mathrm{logits} = W_{\mathrm{full}}h, \quad W_{\mathrm{full}} \in \mathbb{R}^{V \times d}logits=Wfull​h,Wfull​∈RV×d

where V is the full target vocabulary size and d is the drafter hidden dimension. The cost of this projection is O(Vd)O(Vd)O(Vd), which, in modern LLMs, corresponds to hundreds of millions of operations per drafted token and therefore makes the drafter LM-head a natural computational bottleneck.

## Why vocabulary truncation is not enoughWhy vocabulary truncation is not enough

A natural way to reduce LM-head cost is to reduce the number of logits that the drafter computes. Static methods such as FR-Spec (Zhao et al., 2025), VocabTrim (Goel et al., 2025), and BCL (Shoham, 2026) choose a smaller vocabulary subset. Dynamic methods such as CORAL (Weng et al., 2025), DynaSpec (Zhang et al., 2025), and SpecVocab (Williams et al., 2026) choose an active subset depending on the context.

This helps, but it introduces two problems.

First, if the drafter is restricted to a truncated vocabulary, tokens outside that vocabulary can never be proposed, which creates a hard ceiling on the acceptance rate.

For a target distribution p and draft distribution q, the per-token acceptance rate is governed by the distributional overlap:

α=∑v∈Vmin⁡{p(v),q(v)}\alpha = \sum_{v \in \mathcal{V}} \min\{p(v), q(v)\}α=v∈V∑​min{p(v),q(v)}

where V is the full vocabulary. If the drafter only supports a truncated vocabulary Vtr\mathcal{V}_{\mathrm{tr}}Vtr​, then q(v)=0q(v) = 0q(v)=0 for every token outside Vtr\mathcal{V}_{\mathrm{tr}}Vtr​. This means:

α≤∑v∈Vtrp(v)\alpha \leq \sum_{v \in \mathcal{V}_{\mathrm{tr}}} p(v)α≤v∈Vtr​∑​p(v)

No matter how well the drafter is trained, it cannot accept probability mass assigned to tokens it is unable to propose.

Second, vocabulary truncation can create a train-test mismatch. Forward KL training assumes the drafter can represent the full target distribution, but a truncated drafter assigns zero probability to many tokens — making the KL divergence ill-defined. The usual workaround is to mask and renormalize the target during training, but verification at inference time still uses the original, unmasked target. The drafter is therefore optimized for a distribution it will never actually be evaluated against.

Dynamic vocabulary selection can reduce some of these issues, but it adds inference-time machinery: routing, top-k selection, irregular indexing, and gathering context-dependent subsets of weights. These operations are not as GPU-friendly as dense matrix multiplication and can become bottlenecks themselves.

## SlimSpec: compress the representation, not the vocabularySlimSpec: compress the representation, not the vocabulary

Instead of projecting the drafter hidden state directly into the vocabulary space, SlimSpec first compresses the hidden representation to rank rrr, then maps it to the full vocabulary:

logits=WupWdownh,Wup∈RV×r,Wdown∈Rr×d\mathrm{logits} = W_{\mathrm{up}}W_{\mathrm{down}}h, \quad W_{\mathrm{up}} \in \mathbb{R}^{V \times r}, \quad W_{\mathrm{down}} \in \mathbb{R}^{r \times d}logits=Wup​Wdown​h,Wup​∈RV×r,Wdown​∈Rr×d where r<dr < dr<d. The resulting LM-head cost becomes O(Vr+rd)O(Vr + rd)O(Vr+rd). Since modern LLM vocabularies are large and usually V>>dV >> dV>>d the reduction is approximately linear in the rank ratio:

Vr+rdVd≈rd\frac{Vr + rd}{Vd} \approx \frac{r}{d}VdVr+rd​≈dr​

Relative LM-head GPU time TheadT_{\mathrm{head}}Thead​ across models; lower is better. The underlying TheadT_{\mathrm{head}}Thead​ values are normalized with respect to the full vocabulary baseline, set to 1.0. VocabTrim reduces the draft vocabulary to 64K tokens. Both VocabTrim and SpecVocab can reduce LM-head latency by only about 60%, while SlimSpec achieves an approximately 4-5x reduction.

For example, using r=d/8r = d/8r=d/8 gives a much cheaper LM-head while still preserving full-vocabulary support. This is the key difference between SlimSpec and vocabulary-reduction methods. SlimSpec does not remove tokens from the output space. It keeps all token logits available, but computes them through a thinner intermediate representation.

## LM-head latency alone is not the right objectiveLM-head latency alone is not the right objective

A cheaper LM-head does not automatically mean faster end-to-end decoding. In speculative decoding, throughput depends not only on how fast the drafter runs, but also on how many draft tokens are accepted by the target model. We can write the resulting throughput in tokens per second as:

TPS=τTnon-head+Thead\mathrm{TPS} = \frac{\tau}{T_{\text{non-head}} + T_{\mathrm{head}}}TPS=Tnon-head​+Thead​τ​

where τ\tauτ is the average acceptance length. To compare different LM-head acceleration methods, we can express the relative end-to-end speedup ρTPS=TPSmethod/TPSbaseline\rho_{\mathrm{TPS}} = \mathrm{TPS}^{\mathrm{method}} / \mathrm{TPS}^{\mathrm{baseline}}ρTPS​=TPSmethod/TPSbaseline as:

ρTPS=ρτ1+κ1+νκ\rho_{\mathrm{TPS}} = \rho_\tau \frac{1 + \kappa}{1 + \nu\kappa}ρTPS​=ρτ​1+νκ1+κ​

where:

- ρτ=τmethod/τbaseline\rho_\tau = \tau^{\mathrm{method}} / \tau^{\mathrm{baseline}}ρτ​=τmethod/τbaseline is the acceptance ratio between a selected method and full projection baseline.

- ν=Theadmethod/Theadbaseline\nu = T_{\mathrm{head}}^{\mathrm{method}} / T_{\mathrm{head}}^{\mathrm{baseline}}ν=Theadmethod​/Theadbaseline​ is the LM-head latency ratio between a selected method and full projection baseline.

- κ=Theadbaseline/Tnon-headbaseline\kappa = T_{\mathrm{head}}^{\mathrm{baseline}} / T_{\text{non-head}}^{\mathrm{baseline}}κ=Theadbaseline​/Tnon-headbaseline​ measures how important the LM-head is relative to the rest of the speculative decoding pipeline, independent of the particular LM-head acceleration method.

This makes the trade-off explicit: cheaper LM-head (ν<1)(\nu < 1)(ν<1) improves speedup, but lower acceptance (ρτ<1)(\rho_\tau < 1)(ρτ​<1) drags it back down. Therefore, the best method is not necessarily the one with the cheapest LM-head, but the one that reduces LM-head cost while preserving enough accepted tokens per speculative step.

## Experimental setupExperimental setup

We evaluated SlimSpec using the EAGLE-3 drafter setup across three target models:

- Llama-3.1-8B-Instruct

- GPT-OSS-20B

- Qwen3-30B-A3B-Instruct-2507.

The training corpus was constructed from 660K prompts from Infinity-Instruct-0625, with responses generated by the corresponding target model. This matches the drafter training distribution to target-model samples encountered during inference.

All drafters were trained with 6 speculative tokens and shared weights across positions. We evaluated on three benchmarks:

- MT-Bench — instruction following

- HumanEval — code generation

- GSM8K — mathematical reasoning.

Experiments were run with greedy decoding (temperature =0, using batch sizes 1 and 64 to cover latency-critical and high-throughput serving regimes. The inference setup was based on vLLM 0.17.1 with NVIDIA H200 GPUs.

## ResultsResults

SlimSpec is designed to improve end-to-end speculative decoding throughput, not just reduce the cost of the draft LM-head in isolation. We therefore evaluate each method by how much LM-head latency it removes and how much acceptance quality it preserves.

End-to-end speedup decomposition in the (ν,ρτ)(\nu, \rho_\tau)(ν,ρτ​) plane for Llama-3.1-8B at batch size 1 (κ=0.25)(\kappa = 0.25)(κ=0.25). Dashed lines are theoretical speedup level curves. The shaded region indicates no end-to-end improvement over the full-vocabulary baseline. SlimSpec (red stars) achieves the largest LM-head acceleration ν\nuν while keeping ρτ\rho_\tauρτ​ close to 1.

Static vocabulary truncation methods such as FR-Spec, VocabTrim-T, and BCL follow a clear trade-off curve: smaller vocabularies reduce LM-head cost, but they also reduce acceptance quality. This is expected — once tokens are removed from the draft vocabulary, the drafter can no longer propose them, which limits the achievable overlap with the target distribution.

The dynamic vocabulary truncation method SpecVocab improves this trade-off by preserving more acceptance at similar LM-head latency. However, it introduces context-dependent token selection and additional inference-time routing logic.

SlimSpec shifts the frontier further. Its default rank configuration substantially reduces LM-head latency while keeping acceptance close to the full-vocabulary baseline. This makes it a better operating point for end-to-end speculative decoding than methods that reduce the vocabulary itself.

We next compare SlimSpec against the strongest representative baselines across target models, benchmarks, and serving regimes.

Comparison of SlimSpec with the main baselines. Speedup is measured relative to vanilla inference without a speculator. MT, HE, and GSM denote MT-Bench, HumanEval, and GSM8K, respectively.

The table shows that SlimSpec consistently improves over the full-vocabulary draft LM-head and competitive vocabulary-truncation baselines. For Llama-3.1-8B-Instruct, SlimSpec delivers the best average speedup in both low-latency and high-throughput regimes. For GPT-OSS-20B, it again provides the strongest average result, with especially clear gains at batch size 1. For Qwen3-30B-A3B-Instruct, the improvement is smaller because non-head costs account for a larger share of total latency, leaving less room for LM-head compression to affect end-to-end throughput.

Overall, these results show that SlimSpec provides a strong acceptance-cost trade-off while preserving full-vocabulary support. It avoids the hard acceptance ceiling of static vocabulary truncation and the inference-time routing overhead of dynamic vocabulary methods, making it a simple and practical choice for draft LM-head acceleration.

## Want to apply speculative decoding to your own workload?Want to apply speculative decoding to your own workload?

Custom Speculator Training is now live in Nebius Token Factory. Teams can train workload-specific draft models from their own data, then work with Nebius to evaluate and deploy those drafters against real production traffic.

Talk to your SA about a spec decoding performance review: Custom Speculator Training, Token Factory by Nebius

## Explore Custom Speculator Training

Custom Speculator Training:​
Read the docs:​

## Explore Nebius AI Cloud

Sign up​
Docs​

Anton Plaksin
Senior ML Engineer

Contents

- What this changes in production

- Why the draft LM-head becomes a bottleneck

- Why vocabulary truncation is not enough

- SlimSpec: compress the representation, not the vocabulary

- LM-head latency alone is not the right objective

- Experimental setup

- Results

- Want to apply speculative decoding to your own workload?

## See also

### 

LK losses: Training speculative decoding draft models to directly maximize acceptance rate

We introduce LK losses — training objectives that directly optimize the acceptance rate for speculative decoding draft models. They are a drop-in replacement for KL divergence, with no computational overhead, and they work with any draft architecture and any target model size, to deliver consistent improvements in inference throughput across models ranging from 8B to 685B parameters. We are open-sourcing our trained draft models (LK-Speculators) and training datasets (Infinity-Instruct-Completions). An implementation of LK losses is also available as a pull request to SpecForge.

April 10, 2026
16 mins to read

### 

Train the draft model for your workload

Custom Speculator Training is now in Token Factory. Move from production data to a workload-specific draft model, then deploy it alongside the base model, in one workflow.

June 25, 2026
7 mins to read

### 

LangChain tunes Deep Agents for NVIDIA Nemotron 3 Ultra: top open-model accuracy at 10x lower cost with Nebius Agents Blueprint

LangChain has released a Deep Agents profile tuned for NVIDIA Nemotron 3 Ultra, achieving top agent accuracy among open models at roughly 10x lower cost than closed alternatives — with the model itself untouched. The Nebius Agents Blueprint already pairs Deep Agents with Nemotron 3 Ultra on Nebius Token Factory, and support for the tuned profile is coming soon.

July 8, 2026
5 mins to read

Sign in to save this post
Sign In
