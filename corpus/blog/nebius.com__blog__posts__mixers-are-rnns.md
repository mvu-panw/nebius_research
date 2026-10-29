# How transformers, RNNs and SSMs are more alike than you think

Source: https://nebius.com/blog/posts/mixers-are-rnns

Skip to main content

Even in the age of Mamba and other exciting linear RNNs and state space models (SSMs), transformer architectures still reign supreme as the backbone of LLMs. However, this might soon change: hybrid architectures such as Jamba, Samba and Griffin are quite promising. They are significantly more time- and memory-efficient than transformers, and their capabilities are not greatly diminished compared to attention-based LLMs.

At the same time, recent research has exposed deep connections between different architectural options: transformers, RNNs, SSMs and matrix mixers. This is very exciting because it allows for the transfer of ideas from one architecture to another. In this long read, we’ll mainly follow Transformers are RNNs and Mamba 2, getting elbows deep in algebra to understand how:

- Transformers may sometimes be RNNs (section 2),

- State space models may hide inside the mask in the self-attention mechanism (section 4),

- Mamba may sometimes be rewritten as masked self-attention (section 5).

I find these connections quite fascinating, and I hope you, too, will appreciate them.

If you’re curious to learn more about the architectural development of transformer alternatives, please feel free to check my separate post about them.

# Masked self-attention in LLMs: a reminderMasked self-attention in LLMs: a reminder

A classic LLM self-attention layer looks as follows:

Or, in more detail:

Let’s briefly recall what happens here:

- We multiply matrices QQQ of queries and KTK^TKT of keys. The product is an L×LL\times LL×L matrix of scalar products of queries and keys.

- We normalize the resulting matrix.

- Then, we multiply it elementwise on the L×LL\times LL×L attention mask. The picture shows the default causal mask — the 0-1 matrix in the left. It zeroes products (earlier query, later key), preventing the attention from “looking into the future”.

- Then, we take softmax.

- Finally, we multiply the attention weights (let’s denote this matrix by AAA) on the values VVV; the t‑th row of the output is:

outputt=∑iativi.output_t = \sum_i a_{ti}v_i.outputt​=i∑​ati​vi​.

Thus, iii-th value is taken with the “attention weight of ttt-th query for iii-th key”.

Many design choices in this architecture may be altered. Let’s explore some possible changes.

# Linearized attentionLinearized attention

Softmax in the attention formula ensures that the values are mixed with positive coefficients that sum to 1. This is good because it keeps some of the statistics intact, but it is very restricting; no term would escape its brackets, even if we would love to play with associativity like (QKT)V=Q(KTV)(QK^T)V = Q(K^TV)(QKT)V=Q(KTV). Why do we need associativity, you ask? The thing is that changing the order of multiplication can drastically influence the complexity:

- In the left formula, we need to calculate an L×LL\times LL×L matrix, which gives O(L2d)O(L^2d)O(L2d) complexity cost and O(L2)O(L^2)O(L2) memory cost if we allow this matrix to manifest fully in memory.

- In the right formula, we need to calculate a d×dd\times dd×d matrix, which gives O(Ld2)O(Ld^2)O(Ld2) complexity cost and O(d2)O(d^2)O(d2) memory cost if we allow this matrix to manifest fully in memory.

Thus, as context length grows, the first formula becomes more costly than the second one and ultimately becomes prohibitively expensive.

So, you know what? Let’s crack this softmax open! Let’s write down the formula with the softmax in a bit more detail:

yt=∑s=1Lexp⁡(mts⋅qtksT/d)∑j=1Lexp⁡(mtj⋅qtkjT/d)vsy_t = \sum_{s=1}^L \frac{\exp \left(m_{ts}\cdot q_t k_s^T/ \sqrt{d}\right)}{\sum_{j=1}^L \exp \left(m_{tj}\cdot q_t k_j^T/\sqrt{d}\right)} v_syt​=s=1∑L​∑j=1L​exp(mtj​⋅qt​kjT​/d​)exp(mts​⋅qt​ksT​/d​)​vs​

, where exp⁡(mts⋅qtksT/d)∑j=1Lexp⁡(mtj⋅qtkjT/d)\frac{\exp \left(m_{ts}\cdot q_t k_s^T/ \sqrt{d}\right)}{\sum_{j=1}^L \exp \left(m_{tj}\cdot q_t k_j^T/\sqrt{d}\right)}∑j=1L​exp(mtj​⋅qt​kjT​/d​)exp(mts​⋅qt​ksT​/d​)​ is softmax.

The most inconvenient thing here is the exponent; we just can’t take anything out of it. Let’s just erase it.

yt=∑s=1Lmts⋅qtksT∑j=1Lmtj⋅qtkjTvs.y_t = \sum_{s=1}^L\frac{m_{ts}\cdot q_tk_s^T}{\sum_{j=1}^Lm_{tj}\cdot q_tk_j^T}v_s.yt​=s=1∑L​∑j=1L​mtj​⋅qt​kjT​mts​⋅qt​ksT​​vs​.

Note that the normalizer 1d\frac1{\sqrt{d}}d​1​ vanished.

The problem with this formula is that qtkSTq_tk_S^Tqt​kST​ is not guaranteed to be positive, so we may end up mixing the values with different-sign coefficients (which is counterintuitive); and even worse, the denominator may vanish, breaking everything. We may add a “good” elementwise function ϕ\phiϕ (a kernel) to mitigate it:

yt=∑s=1Lmts⋅ϕ(qt)ϕ(ksT)∑j=1Lmtj⋅ϕ(qt)ϕ(kjT)vs.y_t = \sum_{s=1}^L\frac{m_{ts}\cdot \phi(q_t)\phi(k_s^T)}{\sum_{j=1}^Lm_{tj}\cdot\phi(q_t)\phi(k_j^T)}v_s.yt​=s=1∑L​∑j=1L​mtj​⋅ϕ(qt​)ϕ(kjT​)mts​⋅ϕ(qt​)ϕ(ksT​)​vs​.

The original work suggested ϕ(x)=1+elu(x)\phi(x) = 1 + \mathrm{elu}(x)ϕ(x)=1+elu(x).

This variation of the attention mechanism is called linearized attention. And the good thing is that we can now play with associativity:

yt=ϕ(qt)∑s=1Lmts⋅ϕ(ksT)vsϕ(qt)∑j=1Lmtj⋅ϕ(kjT).y_t = \frac{\phi(q_t)\sum_{s=1}^Lm_{ts}\cdot \phi(k_s^T)v_s}{\phi(q_t)\sum_{j=1}^Lm_{tj}\cdot\phi(k_j^T)}.yt​=ϕ(qt​)∑j=1L​mtj​⋅ϕ(kjT​)ϕ(qt​)∑s=1L​mts​⋅ϕ(ksT​)vs​​.

A word of caution. The relations between MMM, KTK^TKT and VVV in the brackets are now quite complex and are not expressed through just ordinary and elementwise matrix products. We’ll discuss this computational block in more detail in the next section.

Now, if MMM is the causal mask with 111 on the diagonal and below, and 000 above the diagonal

then everything becomes even simpler:

yt=ϕ(qt)∑s=1tϕ(ksT)vsϕ(qt)∑j=1tϕ(kjT).y_t = \frac{\phi(q_t)\sum_{s=1}^t\phi(k_s^T)v_s}{\phi(q_t)\sum_{j=1}^t\phi(k_j^T)}.yt​=ϕ(qt​)∑j=1t​ϕ(kjT​)ϕ(qt​)∑s=1t​ϕ(ksT​)vs​​.

And this can be calculated in a very simple, recurrent way:

I think you won’t be surprised to learn that the ICML 2020 paper where linearized attention was first suggested is called Transformers are RNNs. Note that we have two hidden states here: a vector ztz_tzt​ and a matrix hth_tht​ (ϕ(kt)Tvt\phi(k_t)^Tv_tϕ(kt​)Tvt​ is column⋅\cdot⋅row, so it’s a d×dd\times dd×d matrix). In recent papers, lnearized attention is often presented in an even simpler, distilled way, with no ϕ\phiϕ and no denominator:

yt=qt∑s=1tmtsksTvs.y_t = q_t\sum_{s=1}^tm_{ts}k_s^Tv_s.yt​=qt​s=1∑t​mts​ksT​vs​.

Linearized attention has two important benefits:

- As a recurrent mechanism, it has linear complexity at inference time with respect to the sequence length LLL,

- As a transformer model, it can be efficiently trained in a parallel way.

At this point, you probably have a pressing question: if linearized attention is so cool, why don’t we see it in every LLM and why do we still complain about attention’s quadratic complexity? Alas, linearized attention–based LLMs are less stable during training and reach somewhat lower capability than standard self-attention. It looks as if less information can be squeezed through the fixed‑d×d‑shaped bottleneck than through the adaptable L×L one. You can check experiment results in the this article at Manifest AI, for example.

Further reading. The idea that RNNs and linearized attention are related is rediscovered and revisited in many recent works. Moreover, it’s becoming common in such papers to have a matrix hidden state that is updated as follows:

ht=ht−1+ktTvt,h_t = h_{t-1} + k_t^Tv_t,ht​=ht−1​+ktT​vt​,

where ktk_tkt​ and vtv_tvt​ are a “key” and a “value” of sort, with the output of an RNN layer being something like

qtht=qt(ht−1+ktTvt)=…=q_th_t = q_t(h_{t-1} + k_t^T v_t) = \ldots =qt​ht​=qt​(ht−1​+ktT​vt​)=…=

=qt(k1Tv1+…+ktTvt)==q_t(k_1^Tv_1 + \ldots + k_t^T v_t) ==qt​(k1T​v1​+…+ktT​vt​)=

=(qtk1T)v1+…+(qtktT)vt,=(q_tk_1^T)v_1 + \ldots + (q_tk_t^T)v_t,=(qt​k1T​)v1​+…+(qt​ktT​)vt​,

which boils down to linear attention.

As examples, I would suggest checking these two papers:

- xLSTM — a May 2024 paper suggesting a development of the renowned LSTM recurrent architecture. Its mLSTM block features a matrix hidden state which is updated the already-familiar way:

ct=forget_gatet⋅ct−1+input_gatet⋅vtktTc_t = forget\_gate_t \cdot c_{t-1} + input\_gate_t \cdot v_t k_t^Tct​=forget_gatet​⋅ct−1​+input_gatet​⋅vt​ktT​

and is further multiplied on a “query” to obtain the output. (The paper’s linear algebra setup is transposed to ours: queries, keys and values are columns, not rows; hence the odd order in vtktTv_tk_t^Tvt​ktT​.)

- Learning to (learn at test time), emerging in July 2024, which is another RNN architecture with a matrix hidden state and a very peculiar semantics: it is the parameter WWW of a function which is optimized by gradient descent as we iterate over ttt:

Here, everything is also transposed, so the order is odd again. The math is more complicated than Wt=Wt−1+vtktTW_t = W_{t-1} + v_tk_t^TWt​=Wt−1​+vt​ktT​, but may be simplified to it.

# Exploring attention masksExploring attention masks

Now that we have simplified the masked attention mechanism, we can start developing it again. And there is an obvious room for experiments: choosing a different lower triangular (never look into the future) mask MMM, instead of the ascetic 0-1 causal mask. But first, we need to deal with the emerging inefficiency.

In the previous section, we were actually very lucky to work with a simple 0-1 causal mask MMM. In general case, the recurrent trick doesn’t work anymore:

y1=ϕ(q1)(m11⋅ϕ(k1T)v1)ϕ(qt)(m11⋅ϕ(k1T))y_1=\frac{\phi(q_1)\left({\color{red}{m_{11}}}\cdot \phi(k_1^T)v_1\right)}{\phi(q_t)\left({\color{red}{m_{11}}}\cdot\phi(k_1^T)\right)}y1​=ϕ(qt​)(m11​⋅ϕ(k1T​))ϕ(q1​)(m11​⋅ϕ(k1T​)v1​)​

y2=ϕ(q2)(m21⋅ϕ(k1T)v1+m22⋅ϕ(k2T)v2)ϕ(q2)(m21⋅ϕ(k1T)+m22⋅ϕ(k2T))y_2=\frac{\phi(q_2)\left({\color{red}{m_{21}}}\cdot \phi(k_1^T)v_1 + {\color{red}{m_{22}}}\cdot \phi(k_2^T)v_2\right)}{\phi(q_2)\left({\color{red}{m_{21}}}\cdot \phi(k_1^T) + {\color{red}{m_{22}}}\cdot \phi(k_2^T)\right)}y2​=ϕ(q2​)(m21​⋅ϕ(k1T​)+m22​⋅ϕ(k2T​))ϕ(q2​)(m21​⋅ϕ(k1T​)v1​+m22​⋅ϕ(k2T​)v2​)​

y3=ϕ(q3)(m31⋅ϕ(k1T)v1+m32⋅ϕ(k2T)v2+m33⋅ϕ(k3T)v3)ϕ(q3)(m31⋅ϕ(k1T)+m32⋅ϕ(k2T)+m33⋅ϕ(k3T))y_3=\frac{\phi(q_3)\left({\color{red}{m_{31}}}\cdot \phi(k_1^T)v_1 + {\color{red}{m_{32}}}\cdot \phi(k_2^T)v_2 + {\color{red}{m_{33}}}\cdot \phi(k_3^T)v_3\right)}{\phi(q_3)\left({\color{red}{m_{31}}}\cdot \phi(k_1^T) + {\color{red}{m_{32}}}\cdot \phi(k_2^T) + {\color{red}{m_{33}}}\cdot \phi(k_3^T)\right)}y3​=ϕ(q3​)(m31​⋅ϕ(k1T​)+m32​⋅ϕ(k2T​)+m33​⋅ϕ(k3T​))ϕ(q3​)(m31​⋅ϕ(k1T​)v1​+m32​⋅ϕ(k2T​)v2​+m33​⋅ϕ(k3T​)v3​)​

⋮\vdots⋮

The coefficients mts\color{red}{m_{ts}}mts​ are different now, and there’ll be no recurrent formula relating y3y_3y3​ to y2y_2y2​. Thus, for each ttt we’ll have to compute the sum from scratch, making the complexity asymptotic quadratic by LLL again, instead of linear.

The answer is that we won’t use just any masks MMM, only special, “good” ones. Namely, the ones that can be quickly multiplied (not elementwise!) on other matrices. To see how we can benefit from this property, let’s understand how to calculate

yt=qt∑s=1LmtsksTvsy_t = q_t\sum_{s=1}^Lm_{ts}k_s^T v_syt​=qt​s=1∑L​mts​ksT​vs​

efficiently. First, let’s clarify what’s happening here:

If we descend to the individual index level:

For the further discussion, it will be useful for us to color indices instead of blocks:

Now, we are ready to formulate the four-step algorithm:

Step 1. Take KKK and VVV and create a three-dimensional tensor ZZZ with

ztij=ktivtjz_{{\color{magenta}{t}}{\color{orange}{i}}{\color{teal}{j}}} = k_{{\color{magenta}{t}}\color{orange}{i}}v_{{\color{magenta}{t}}{\color{teal}{j}}}ztij​=kti​vtj​

(Each axis is marked with its length.) This step takes O(Ld2)O(Ld^2)O(Ld2) time and memory.

Note that if we sum this tensor over the magenta axis t{\color{magenta}{t}}t, we’ll get the product KTVK^TVKTV:

∑tktivtj=∑t(KT)itvtj=(KTV)ij\sum_{{\color{magenta}{t}}}k_{{\color{magenta}{t}}\color{orange}{i}}v_{{\color{magenta}{t}}{\color{teal}{j}}} = \sum_{{\color{magenta}{t}}}(K^T)_{\color{orange}{i}{\color{magenta}{t}}}v_{{\color{magenta}{t}}{\color{teal}{j}}}=(K^TV){\color{orange}{i}{\color{teal}{j}}}t∑​kti​vtj​=t∑​(KT)it​vtj​=(KTV)ij

Step 2. Now, we multiply MMM on this tensor (not elementwise!) in such a way that MMM is multiplied on each “column” of ZZZ along the magenta axis t{\color{magenta}{t}}t.

This gives us exactly

∑tmstktivtj=∑tmst(KT)itvtj\sum_{{\color{magenta}{t}}} m_{{\color{cyan}{s}}{\color{magenta}{t}}} k_{{\color{magenta}{t}}\color{orange}{i}} v_{{\color{magenta}{t}}{\color{teal}{j}}} = \sum_{{\color{magenta}{t}}} m_{{\color{cyan}{s}}{\color{magenta}{t}}} (K^T)_{\color{orange}{i}{\color{magenta}{t}}} v_{{\color{magenta}{t}}{\color{teal}{j}}}t∑​mst​kti​vtj​=t∑​mst​(KT)it​vtj​

Let’s denote the result by HHH. Now, it’s only left to multiply everything on qtq_tqt​ which will be done in two more steps.

Step 3a. Take QQQ and multiply elementwise on each j=const{\color{teal}{j}} = \mathrm{const}j=const layer of HHH:

This results in:

qsi∑tmstktivtjq_{{\color{cyan}{s}}{\color{orange}{i}}}\sum_{{\color{magenta}{t}}} m_{{\color{cyan}{s}}{\color{magenta}{t}}} k_{{\color{magenta}{t}}\color{orange}{i}} v_{{\color{magenta}{t}}{\color{teal}{j}}}qsi​t∑​mst​kti​vtj​

This step requires O(Ld2)O(Ld^2)O(Ld2) time and memory.

Step 3b. Sum the resulting tensor along the i{\color{orange}{i}}i axis:

This step also requires O(Ld2)O(Ld^2)O(Ld2) time and memory. And we obtain exactly the thing we need:

∑iqsi∑tmstktivtj\sum_{\color{orange}{i}}q_{{\color{cyan}{s}}{\color{orange}{i}}}\sum_{{\color{magenta}{t}}} m_{{\color{cyan}{s}}{\color{magenta}{t}}} k_{{\color{magenta}{t}}\color{orange}{i}} v_{{\color{magenta}{t}}{\color{teal}{j}}}i∑​qsi​t∑​mst​kti​vtj​

The most crucial step is the second one, and we deliberately omitted its complexity analysis. A naïve estimate is:

- 

O(L2)O(L^2)O(L2) for each matrix multiplication,

- 

Repeating it d2d^2d2 times,

So it’s a whopping O(L2d2)O(L^2d^2)O(L2d2). But we will take not just any MMM. We will take MMM such that the complexity of multiplying MMM on a vector is O(RL)O(RL)O(RL) for some constant (and not very large) RRR.

For example, if MMM is the 0-1 causal matrix, multiplication on it boils down to computing the cumulative sums, and it is done in O(L)O(L)O(L) time. But there are many more options for structured matrices with fast vector multiplication.

In the next section, we’ll discuss one of such matrix types — semiseparable matrices, which will turn out to be tightly connected with state space models.

# Semiseparable matrices and state space modelsSemiseparable matrices and state space models

Let’s recall that (discretized) state space models (SSM) are a class of sequential models connecting 111-dimensional input xtx_txt​, rrr-dimensional hidden state hth_tht​, and 111-dimensial output utu_tut​ in the following way:

ht=Atht−1+Btxt,h_t= A_t h_{t-1} + B_t x_t,ht​=At​ht−1​+Bt​xt​,

yt=Ctht+Dtxty_t = C_t h_t + D_t x_tyt​=Ct​ht​+Dt​xt​

So, in the discretized form, it’s just a fancy linear RNN with a skip connection. Moreover, for the rest of the story, we’ll even forget about skip connections by setting Dt=0D_t = 0Dt​=0.

Now, let’s write our SSM as a single matrix multiplication

y=Mx,y = \mathcal{M}x,y=Mx,

where

So, M\mathcal{M}M is lower triangular, just like the attention masks we discussed earlier.

This type of matrix comes with a great boon:

An L×LL\times LL×L lower triangular matrix whose elements may be presented in this way can be stored using O(rL)O(rL)O(rL) memory and has a matrix-vector multiplication complexity of O(rL)O(rL)O(rL) instead of the default O(L2)O(L^2)O(L2) (see this paper for details).

This means that every state space model gives rise to a structured attention mask M\mathcal{M}M which can be used in an efficient transformer model with linearized attention.

The curious thing, though, is that a semiseparable matrix M\mathcal{M}M is already quite complex and expressive, even without all the query-key-value machinery around it. Moreover, it may itself be a masked attention mechanism. We’ll see this in the next section.

# State space dualityState space duality

Here, we finally arrive at one of the central results of the Mamba 2 paper.

Let’s again consider y=Mu,y = \mathcal{M}u,y=Mu, where u=u(x)u = u(x)u=u(x) is a function of the inputs and M\mathcal{M}M is a semiseparable matrix. Moreover, let’s consider a very special case where each AtA_tAt​ is a scalar matrix: At=atIA_t = a_tIAt​=at​I. Then the formulas become especially simple:

yt=at…a2CtB1u1+at…a3CtB2u2+…+atCtBt−1ut−1+CtBtut.y_t = a_t\ldots a_2C_tB_1u_1 + a_t\ldots a_3C_tB_2u_2 + \ldots + a_tC_tB_{t-1}u_{t-1} + C_tB_tu_t.yt​=at​…a2​Ct​B1​u1​+at​…a3​Ct​B2​u2​+…+at​Ct​Bt−1​ut−1​+Ct​Bt​ut​.

Note that

Ci⏟1×rBj⏟r×1\underbrace{C_i}_{1\times r}\underbrace{B_j}_{r\times 1}1×rCi​​​r×1Bj​​​

is just a number. Moreover, we can stack CiC_iCi​ and BiB_iBi​ in matrices BBB and CCC such that:

Now, we’ll also need the matrix

Then it’s easy to check that

Mu=(G⊗CB)u\mathcal{M}u = (G\otimes CB)uMu=(G⊗CB)u

Have we seen this somewhere? Indeed! It’s masked attention with:

- GGG for the mask,

- CCC for QQQ, the query matrix,

- BBB for KTK^TKT, the transposed key matrix,

- uuu for VVV, the value matrix.

In classic SSMs, BBB and CCC are constants, but Mamba made them data-dependent, reinforcing the alignment. This correspondence between specific state space models and masked attention was introduced in the Mamba 2 paper as state space duality.

Further reading. The idea of using matrix mixers instead of more sophisticated architectures is not new, with one of the notable early examples being MLP-Mixer which employed MLPs instead of convolution or attention for spatial mixing in CV tasks.

Although current research is mostly focused on LLMs, there are also several papers proposing non-transformer, matrix mixture architectures for encoder models. Examples include:

- FNet from Google research a with matrix mixer M\mathcal{M}M based on Fourier transform,

- Hydra, which, among other ideas, proposed an adaptation of semiseparable matrices for non-causal (non-triangular) working mode.

As always, I encourage you to check out our Practical Generative AI course, where the discussions often serve as a source of knowledge and inspiration for posts like this one.

## Explore Nebius AI

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Stanislav Fedotov
AI evangelist at Nebius, AI program lead at AI DT School

## See also

### 

Mixtures of Experts and scaling laws

Mixture of Experts (MoE) has become popular as an efficiency-boosting architectural component for LLMs. In this blog, we’ll explore the steps researchers have taken on the road toward the perfect mixture of experts.

August 6, 2024
8 mins to read

### 

Fundamentals of LoRA and low‑rank fine-tuning

In the next installment of our series of deep technical articles on AI research, let’s switch our attention to the famous LoRA, a low-rank adaptation technique.

May 13, 2024
11 mins to read

### 

Transformer alternatives in 2024

With this article, we are starting a new category on our blog, the one dedicated to AI research. Expect these posts to be very technical and insightful. The first one is about possible alternatives to the key component of the LLM architecture.

March 28, 2024
12 mins to read

Sign in to save this post
Sign In
