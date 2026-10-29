# Mixtures of Experts and scaling laws

Source: https://nebius.com/blog/posts/mixture-of-experts

Skip to main content

MoE has been used in models like Mixtral, DeepSeek-V2, Qwen2-57B-A14B, and Jamba. However, like any architectural component, it has hyperparameters — total number of experts, number of active experts, granularity — that can affect the final model quality.

## MoE reminderMoE reminder

In the world of GPU- and data-intensive LLMs, it’s important to find balance between various precious resources. For example, if we want an LLM to excel at a wide range of tasks, this is enabled by increasing the number of parameters, which in turn makes inference (as well as training) more compute-hungry.

MoE emerged as a way to create an LLM that is large and capable but somewhat less demanding at the inference stage. MoE suggests having several (e.g., 8) independent versions of a Feedforward block (FFN) — “experts” — and a router that decides which (e.g., 2) of these experts are used for each particular token.

Source: Switch Transformers by Google

You might ask, “Why just FFN, and not self-attention as well?” Self-attention is too complex, and FFN blocks usually contain more than half of all the LLM parameters.

The first LLM with MoE was Mixtral-8×7B (read “8 experts with a 7B base model”), created from Mistral-7B by spawning 8 copies of each FFN block of Mistral and adding a routing mechanism that chooses 2 experts for each token. Compared to the 7B parameters of Mistral, it:

- has 47B parameters and was able to compete with 70B models at the time of its creation, but

- uses only 13B active parameters, making it more efficient than similarly-sized counterparts.

Mixtral calculated expert weights like this (source: Hugging Face):

With the final output being equal to: y=ΣiG(x)iEi(x)y=\underset{i}\Sigma G(x)_i E_i (x)y=iΣ​G(x)i​Ei​(x)

Note the random summand in H(x)iH(x)_iH(x)i​ which works as a regularizer for training stabilization.

This only works well if the router is balanced, meaning it doesn’t favor or disregard certain experts. Otherwise, efficiency can be hindered instead of improved. Special “hacks, ” including an auxiliary balancing loss function, are used to keep everything running properly. Moreover, given the router assignment for a current token, Mixtral’s MoE mechanism tries to divide an incoming batch into almost equal parts with overhead not greater than pre-set capacity factor (usually around 1–1.25):

Illustration of token routing dynamics. Each expert processes a fixed batch-size of tokens modulated by the capacity factor. Each token is routed to the expert with the highest router probability, but each expert has a fixed batch size of (total tokens / num experts) × capacity factor. If the tokens are unevenly dispatched then certain experts will overflow (denoted by dotted red lines), resulting in these tokens not being processed by this layer. A larger capacity factor alleviates this overflow issue, but also increases computation and communication costs (depicted by padded white/empty slots. Source: Switch Transformers by Google

Check the Hugging Face post mentioned above for more details.

Note: MoE LLMs are also referred to as sparse, while non-MoE models are called dense by comparison.

## We need more expertsWe need more experts

Mixtral had only 8 experts, but later models went much further.

For example, DeepSeek-V2 has 2 shared experts and 160 routed experts, of which 6 are selected for each token. With 236B total parameters, it has only 21B activated for each token. Shared experts are always invoked; they are said to capture common knowledge across varying contexts. Routed experts are numerous, and some of them turn out to be highly specialized.

The behavior of MoE LLMs with a growing number of experts has been studied in several recent works, and there are good reasons to believe that having many experts is beneficial. I’ll mention two works studying related empirical scaling laws:

- Unified scaling laws for routed language models This paper showed that the validation loss tends to improve with a growing expert count:

The authors also studied the effective parameter count. For example, cB (c billions) is the efficient parameter count of Mixtral-8×7B if a hypothetical Mistral-cB would give the same quality as Mixtral. The researchers found that the gain in effective parameter count diminishes with growing base model size: if Mistral had 1T parameters instead of 7B, creating Mixtral-8×1T out of it wouldn’t improve the quality (same source):

(Here, S-BASE, RL-R, and Hash stand for different ways of distributing a batch between experts more evenly).

The takeaway: Having more experts is beneficial, although the gain diminishes with increasing base model size.

This approach may be criticized for using the same training dataset for all model sizes; this will be addressed in the next paper.

- The next paper, Scaling laws for fine-grained mixture of experts, takes two important steps forward. First, it seeks optimal training dataset sizes for all the models. Second, it introduces the idea of expert granularity. Imagine again Mistral-7B which we are turning into a MoE model. Initially, it becomes Mixtral-8×7B with 8 experts, each outputting d-dimensional vectors. Now, let’s split each expert into G smaller experts that output vectors of dimension d/G:

If G = 2, each original expert becomes two fine-grained experts. Moreover, the router will now choose not 2 out of 8 experts, but 4 out of 16.

Now, the paper studies scaling laws as the balancing of the following parameters:

- Total training compute in FLOPs (which depends on both model size and dataset size),

- Base model size,

- Number of experts,

- Expert granularity,

- Validation loss.

Granularity turns out to be an important hyperparameter. As base model size increases, it seems beneficial to increase granularity (here, N is the model size and D is the training dataset size in tokens):

Source: Scaling laws for fine-grained mixture of experts

It’s also advantageous to increase the number of experts (same source):

The problem is that increasing the number of experts and granularity may eventually hinder model efficiency, as seen in this plot (same source):

Here, for G = 16, the routing cost dominates gains from granularity. Overcomplicated routing will also make things slower at inference.

The takeaway: If we increase granularity in a timely manner, MoE steadily improves quality until routing complexity interferes.

## What if we have a million tiny experts?What if we have a million tiny experts?

From the previous paper’s perspective, model quality may improve infinitely as we increase the number of experts and the granularity toward having something like 1,000,000 small experts — if only the routing process is optimized.

A way to optimize it is suggested in the Mixture of a Million Experts paper. Imagine that we have many small experts eie_iei​, each having a fixed key kik_iki​ (just a constant vector). Let KKK be the number of experts we want to use for each token.

The MoE layer in this paper works differently compared to how it does in Mixtral:

- Calculate a query vector q(x)q(x)q(x),

- Calculate the scalar products q(x)Tkiq(x)^T k_iq(x)Tki​,

- Find KKK maximal q(x)Tkiq(x)^T k_iq(x)Tki​,

- Only for these experts, calculate router scores gi(x)=s(q(x)Tki)g_i (x)=s(q(x)^T k_i)gi​(x)=s(q(x)Tki​),

- Finally, the output is f(x)=Σchosen igi(x)ei(x)f(x)=\underset{\text{chosen i}}\Sigma g_i (x)e_i (x)f(x)=chosen iΣ​gi​(x)ei​(x).

The actual routing closely resembles a nearest neighbor search in a vector database. For that, we have efficient algorithms, but since we need to do it for every token, it can be good to optimize it even further.

The authors suggest using product keys, that is, taking ki=(ci,c’i)k_i=(c_i,c’_i)ki​=(ci​,c’i​), a concatenation of two keys of half the dimension of kik_iki​. For a million experts, it’s enough to have only a thousand different cic_ici​. Thus, instead of doing the nearest neighbor search in a 1,000,000-size database, we only need to do it twice for two 1,000-size databases, which is much more efficient.

The authors go as far as to suggest setting experts eie_iei​ to be one-dimensional (with scalar output). To make the MoE more expressive, they make them multi-head:

- Calculate HHH independent query vectors qh(x)q_h (x)qh​(x),

- Calculate the scalar products qh(x)Tkiq_h (x)^T k_iqh​(x)Tki​,

- For each hhh, find its own set of KKK maximal qi(x)Tkiq_i (x)^T k_iqi​(x)Tki​,

- Only for these experts, calculate router scores gh,i(x)=s(qh(x)Tki)g_{h,i} (x) =s(q_h (x)^T k_i)gh,i​(x)=s(qh​(x)Tki​),

- Finally, the output is f(x)=ΣhΣchosen igh,i(x)ei(x)f(x)=\underset{h}\Sigma \underset{\text{chosen i}}\Sigma g_{h,i} (x)e_i (x)f(x)=hΣ​chosen iΣ​gh,i​(x)ei​(x).

Evaluation results may be summarized in the following plot:

Source: Mixture of a Million Experts

Using their method, called PEER, the authors are able to achieve a stable improvement in perplexity as N (the total total number of tiny experts) increases up to 10242.

The takeaway: With optimized routing, MoE steadily provides quality improvement.

## When many experts can be of use: A case of lifelong learningWhen many experts can be of use: A case of lifelong learning

If you’re capable of training an LLM, you probably want to create a new one every year or so, with new architectural perks, etc. However, between episodes of training from scratch, you may want to update your existing LLM on some new data — to adapt it to a new data distribution. Simply continuing the previous training process may sometimes cause catastrophic forgetting. LoRA is not very capable of grasping new knowledge. So what should you do?

The Lifelong language pretraining with distribution-specialized experts paper suggests freezing the existing parts of the LLM and augmenting it with new experts and gating:

The results are somewhat mixed, but overall the idea is interesting.

This article was inspired by discussions at the paperwatch meetings of the Practical Generative AI course, which is run by the School of AI and Data Technologies. If you’re interested in studying LLMs and other generative models, their internal workings and applications, check out our program.

## Explore Nebius AI

Get started​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Stanislav Fedotov
AI evangelist at Nebius, AI program lead at AI DT School

## See also

### 

Fundamentals of LoRA and low‑rank fine-tuning

In the next installment of our series of deep technical articles on AI research, let’s switch our attention to the famous LoRA, a low-rank adaptation technique.

May 13, 2024
11 mins to read

### 

Nebius AI at the frontiers of physics and maths

In today’s guest post, Ananyo Bhattacharya, Chief Science Writer at the London Institute for Mathematical Sciences, details projects by researchers at LIMS, all based on Nebius infrastructure. We’re honored to host these under our Research Grant program.

August 1, 2024
4 mins to read

### 

Transformer alternatives in 2024

With this article, we are starting a new category on our blog, the one dedicated to AI research. Expect these posts to be very technical and insightful. The first one is about possible alternatives to the key component of the LLM architecture.

March 28, 2024
12 mins to read

Sign in to save this post
Sign In
