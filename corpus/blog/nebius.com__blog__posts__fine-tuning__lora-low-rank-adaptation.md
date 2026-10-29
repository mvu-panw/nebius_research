# Fundamentals of LoRA and low‑rank fine-tuning

Source: https://nebius.com/blog/posts/fine-tuning/lora-low-rank-adaptation

Skip to main content

## 1. Introduction1. Introduction

It’s easy to understand why we resort to parameter-efficient fine-tuning of LLMs: fully training them is an extremely costly process.

However, it turns out that a strong pre-trained model doesn’t require many parameters to be adapted for a specific task! This was known as early as 2020 when the authors of Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning ran several experiments with encoder-only models of the BERT and RoBERTa classes to explore the 'intrinsic dimensions' of various problems.

Specifically, they analyzed several tasks, and for each, they determined d90d_{90}d90​: the minimum dimension ddd for which fine-tuning in a ddd-dimensional subspace gives more than 90 percent of full fine-tuning quality. Like this:

The dashed line represents the d90d_{90}d90​ value, and you can see that in many cases, it can be achieved with a ddd significantly smaller than DDD. Note, by the way, that the horizontal axis is logarithmic.

As LLMs matured, several low-parameter fine-tuning techniques emerged, and the most influential of them is LoRA — the abbreviation comes from low-rank adaptation.

In this long read, we will discuss LoRA and some of its modifications. Namely, I will share with you:

- What is rank from a math point of view, and how to wrap your intuition around it.

- What exactly we mean by fine-tuning a model in a low-dimensional subspace.

- Why LoRA updates come in a two-matrix-product form.

- Which exciting developments arose around LoRA recently.

## 2. A few words about rank2. A few words about rank

There are many kinds of layers inside LLMs, but in the end their parameters are stored in matrices (luckily, you don’t often encounter tensors in LLMs). And each matrix has a characteristic called rank. Usually, rank is defined like this:

The rank of a matrix AAA is the maximum number of linearly independent columns (or rows) that can be found in the matrix. (You’ll get the same number if you take rows instead of columns).

While this definition is correct, my experience shows it’s not easy to use. So, let’s consider an equivalent one.

A real matrix AAA of size M×NM\times NM×N is usually more than just a table filled with numbers; it can represent a variety of algebraic entities. Importantly for our discussion, it can represent a linear transformation FA:RN→RMF_A:\mathbb{R}^N\rightarrow\mathbb{R}^MFA​:RN→RM mapping from an NNN-dimensional space to an MMM-dimensional space (mind the order!). My favorite way to characterize rank is:

The rank of a matrix AAA is dim⁡Im(FA)\dim{\mathrm{Im}(F_A)}dimIm(FA​), the dimension of the image of FAF_AFA​.

For example, if AAA is 3×23\times 23×2, it represents a linear transformation R2→R3\mathbb{R}^2\rightarrow\mathbb{R}^3R2→R3, and its rank could be 222 (top picture), or 111 (bottom picture), or even 000 if the image is zero:

While I won’t formally prove the equivalence of these two definitions here, let me remind you that the columns of a matrix of a linear transformation are precisely the images of the standard basis vectors. Here is an example of a 4×34\times34×3 matrix corresponding to a linear map R3→R4\mathbb{R}^3\rightarrow\mathbb{R}^4R3→R4:

If you need a basis for the image of FAF_AFA​, you can take a maximal linearly independent subset of AAA, such as Ae1,Ae2Ae_1, Ae_2Ae1​,Ae2​. Thus, the rank is 222.

## 3. Low-rank adaptation — LoRA3. Low-rank adaptation — LoRA

The essence of LoRA is:

Let’s only do low-rank parameter updates.

To clarify, consider some weight matrix WWW, which is, of course, a matrix of some linear transformation FW:RM→RNF_{W}: \mathbb{R}^M\rightarrow\mathbb{R}^NFW​:RM→RN. A low-dimensional update of FWF_{W}FW​ is a new transformation GGG:

G(x)=FW(x)+F′(x),G(x) = F_{W}(x) + F'(x),G(x)=FW​(x)+F′(x),

where the image of F′F'F′ is low-dimensional.

Here is an example where FW:R2→R3F_{W}:\mathbb{R}^2\rightarrow\mathbb{R}^3FW​:R2→R3 and F′F'F′ has a rank of 111:

You see that adding F′F'F′ changes only what happens on the green line.

LoRA suggests the following:

- We freeze FWF_{W}FW​,

- We only fine tune F′F'F′, and we demand that the rank of its matrix W′W'W′ is ⩽r\leqslant r⩽r, where rrr is a hyperparameter.

The problem is that optimizing W′W'W′ over a subset is usually tricky, to say the least. Can we find a convenient parametrization for rank-⩽r\leqslant r⩽r matrices? It turns out that yes, and for this purpose, we will revisit our dimension-of-the-image description of rank.

## 4. Parametrizing a low-rank matrix4. Parametrizing a low-rank matrix

Let’s take another look at our rank-1 example:

This transformation can be done in two stages:

- First, we map a 2d plane onto a line using a matrix AAA of shape 1×21\times 21×2.

- Then, we embed this line into a 3d space using a matrix BBB of shape 3×13\times 13×1.

Like this:

Now, we have FW(x)=FB(FA(x))F_W(x) = F_B(F_A(x))FW​(x)=FB​(FA​(x)) or, in matrix terms:

W3×2=B3×1⋅A1×2.\underset{3\times 2}{W} = \underset{3\times 1}{B}\cdot \underset{1\times 2}{A}.3×2W​=3×1B​⋅1×2A​.

In exactly the same way, we can demonstrate that any M×NM\times NM×N matrix WWW of rank rrr can be decomposed as

WM×N=BM×r⋅Ar×N.\underset{M\times N}{W} = \underset{M\times r}{B}\cdot \underset{r\times N}{A}.M×NW​=M×rB​⋅r×NA​.

Moreover, if there is a decomposition

WM×N=BM×s⋅As×N,\underset{M\times N}{W} = \underset{M\times s}{B}\cdot \underset{s\times N}{A},M×NW​=M×sB​⋅s×NA​,

then rkW⩽s\mathrm{rk}{W}\leqslant srkW⩽s. Note: the rank can be less if the ranks of AAA and BBB are less than sss.

And that’s exactly what we do in LoRA. We decompose W′=BAW' = BAW′=BA and train matrices BBB and AAA without any additional constraints!

Now, you should better understand what happens in this image (sourced from here):

Now, we can explicitly calculate how much additional memory LoRA requires. For example, if the original WWW was 4096×40964096 \times 40964096×4096, like in Mistral’s q_proj layer, and the LoRA rank is r=8r = 8r=8, then

- AAA is of shape 8×40968\times40968×4096,

- BBB is of shape 4096×84096\times84096×8,

giving 8⋅4096+4096⋅8=65,5368\cdot4096 + 4096\cdot8 = 65,5368⋅4096+4096⋅8=65,536 new parameters which is only about 0.4%0.4\%0.4% of the 4096⋅40964096\cdot40964096⋅4096 parameters of WWW.

There is no general rule, but usually quite small values of rrr are used. It’s reasonable to go with 888, or 161616, or, if you’re especially generous, with 646464, although I wouldn’t start with it. Usually, all dense layers, except for the embedding layer, are fine-tuned, that is:

- Query, key and value projections (q_proj, k_proj, v_proj layers) and the output projection of the attention block (o_proj layers),

- All the dense layers inside the Feedforward block.

Often, a dropout layer is also added before BABABA with p=0.1p=0.1p=0.1 or likewise small.

The one thing I would add is how we initialize BBB and AAA. We want to start fine-tuning from the pre-trained weights WWW, so W′W'W′ should initially be zero. It’s easy to do this by setting the initial BBB to zero, as depicted in the image above.

LoRA has proven itself a worthy companion for any LLM engineer and a default choice for fine-tuning tasks.

It has been observed, though, that LoRA often yields worse results than full fine-tuning. Of course, we could blame a lack of parameters, but there are additional inefficiencies in LoRA, which we’ll discuss in upcoming sections.

### 4.1. Intrinsic dimensionality: experiment details4.1. Intrinsic dimensionality: experiment details

I previously mentioned the paper Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning, which showcased that certain task can be successfully solved with low dimensional parameter updates. I skipped the details of the experiment setup, so I’ll briefly explain it now.

The LoRA update is expressed as:

W↦W+BA,W \mapsto W + BA,W↦W+BA,

where FAF_AFA​ projects to an rrr-dimensional (low-dimensional) space, and FBF_BFB​ embeds the latter into the image space of FWF_WFW​.

What the authors of the Intrinsic Dimensionality paper did is:

- They took specially structured random BBB and froze it.

- They then trained AAA.

This means that for each experiment, they fixed a random subspace and trained the updates within it, while LoRA trains both the subspace (BBB) and the updates within it (AAA).

It’s interesting that we can get meaningful results even when making updates in a randomly selected subspace with a random frozen BBB. But of course, it’s much better to make them trainable.

## 5. PiSSA: using SVD to do updates in a more meaningful subspace5. PiSSA: using SVD to do updates in a more meaningful subspace

When we’re implemetingwe implementdo LoRA, BBB evolves through stochastic gradient descent, allowing the subspace where the updates occur and, develop randomly. This raises the question: can we identify a 'good' starting subspace?

The answer might be yes. We have a good old method for identifying 'meaningful' subspaces, known as singular value decomposition (SVD). Let’s briefly revisit what it is.

By definition, a singular value decomposition (SVD) of a matrix WWW is

WM×N=UM×M⋅ΣM×N⋅VTN×N,\underset{M\times N}{W} = \underset{M\times M}{U}\cdot\underset{M\times N}{\Sigma}\cdot \underset{N\times N}{V^T},M×NW​=M×MU​⋅M×NΣ​⋅N×NVT​,

where:

- 

UUU is orthogonal, meaning the columns uiu_iui​ of UUU are mutually orthogonal vectors of length 111: ⟨ui,uj⟩=0\langle u_i, u_j\rangle = 0⟨ui​,uj​⟩=0 for i≠ji\ne ji=j, and ∣ui∣=1|u_i| = 1∣ui​∣=1. (The same is true for rows of UUU because UUU is square).

- 

VVV is also orthogonal.

- 

Σ=diag(σ1,σ2,…)\Sigma = \mathrm{diag}(\sigma_1,\sigma_2,\ldots)Σ=diag(σ1​,σ2​,…) is diagonal with σ1⩾σ2⩾…⩾0\sigma_1 \geqslant \sigma_2 \geqslant \ldots \geqslant 0σ1​⩾σ2​⩾…⩾0. These σi\sigma_iσi​ are known as the singular values of WWW. Just be aware that Σ\SigmaΣ is not always square; for example:

To move on, we need to tinker with matrices a bit. First, we can put σi\sigma_iσi​ into the columns of UUU and the rows of VTV^TVT (which are the transposed columns of VVV):

Next, we use the following matrix identity:

to reformulate SVD as:

Now, let’s recall that σ1⩾σ2⩾…⩾0\sigma_1 \geqslant \sigma_2 \geqslant \ldots \geqslant 0σ1​⩾σ2​⩾…⩾0. Moreover, in most real cases, the singular values σi\sigma_iσi​ decline rapidly, enabling us to select a reasonable r<M,Nr < M,Nr<M,N such that σr+1\sigma_{r+1}σr+1​ is significantly less than σ1\sigma_1σ1​. We can then suggest that

- (σ1u1)(σ1v1)T+…+(σrur)(σrvr)T(\sqrt{\sigma_1}u_1)(\sqrt{\sigma_1}v_1)^T + \ldots + (\sqrt{\sigma_r}u_r)(\sqrt{\sigma_r}v_r)^T(σ1​​u1​)(σ1​​v1​)T+…+(σr​​ur​)(σr​​vr​)T encapsulates the meaningful components, while

- (σr+1ur+1)(σr+1vr+1)T+(σr+2ur+2)(σr+2vr+2)T+…(\sqrt{\sigma_{r+1}}u_{r+1})(\sqrt{\sigma_{r+1}}v_{r+1})^T + (\sqrt{\sigma_{r+2}}u_{r+2})(\sqrt{\sigma_{r+2}}v_{r+2})^T + \ldots(σr+1​​ur+1​)(σr+1​​vr+1​)T+(σr+2​​ur+2​)(σr+2​​vr+2​)T+… represents 'noise'.

Reapplying the green-and-blue matrix identity, we can depict it this way:

Here, the first part of the sum is meaningful and the second is 'noise'. We can distill this further into:

W=BA+WnoiseW = {\color{orange}{B}}{\color{magenta}{A}} + W_{\mathrm{noise}}W=BA+Wnoise​

Here’s what we have here:

- The summand BA{\color{orange}{B}}{\color{magenta}{A}}BA likely represents the 'important' part of the matrix.

- A{\color{magenta}{A}}A is a projection to an rrr-dimensional space, while B{\color{orange}{B}}B embeds this space into the image space of WWW as the rrr-dimensional subspace SrS_rSr​.

Caution! When using SVD, we persuade ourselves that all the interesting things happen in SrS_rSr​. However, this is not always true. The principal components (σ1u1)(σ1v1)T+…+(σrur)(σrvr)T(\sqrt{\sigma_1}u_1)(\sqrt{\sigma_1}v_1)^T + \ldots + (\sqrt{\sigma_r}u_r)(\sqrt{\sigma_r}v_r)^T(σ1​​u1​)(σ1​​v1​)T+…+(σr​​ur​)(σr​​vr​)T are larger but not necessarily more interesting or useful. Sometimes, the finest details are the most important ones. However, SVD may give us a good starting point for training LoRA.

The PiSSA paper suggests exactly that. The authors take

W=BA+WnoiseW = {\color{orange}{B}}{\color{magenta}{A}} + W_{\mathrm{noise}}W=BA+Wnoise​

as we did earlier and further fine-tune AAA and BBB. The results are nice; the authors claim to beat LoRA in their experiments, and they also show that PiSSA performs better than QLoRA in a quantization strategy when the base model is set to 'nf4' precision and frozen, while the adapters are trained using 'bfloat16' precision.

## 6. DoRA: decoupling magnitude and direction updates6. DoRA: decoupling magnitude and direction updates

The authors of DoRA: Weight-Decomposed Low-Rank Adaptation did an insightful analysis of magnitude and direction updates during full fine-tuning versus LoRA.

Consider the columns of the weight matrix

W=[w1,w2,…,wN]W = \left[\begin{matrix}w_1, w_2,\ldots,w_N\end{matrix}\right]W=[w1​,w2​,…,wN​​]

As we remember, each wiw_iwi​ is the image under WWW of the standard basis vector eie_iei​. During fine-tuning, the vectors wiw_iwi​ change in both magnitude and direction. It’s curious to see that the patterns of these changes differ between full fine-tuning (FT) and LoRA. Let’s explore how. We decompose the matrix as

W=m⊙W∣∣W∣∣,W = m\odot\frac{W}{||W||},W=m⊙∣∣W∣∣W​,

where mmm, also denoted by ∣∣W∣∣||W||∣∣W∣∣ (magnitudes), is the vector

∣∣W∣∣=(∣∣w1∣∣,∣∣w2∣∣,…,∣∣wN∣∣),||W|| = \left(||w_1||, ||w_2||, \ldots, ||w_N||\right),∣∣W∣∣=(∣∣w1​∣∣,∣∣w2​∣∣,…,∣∣wN​∣∣),

W∣∣W∣∣\frac{W}{||W||}∣∣W∣∣W​ (directions) is the following matrix:

W∣∣W∣∣=[1∣∣w1∣∣w1,1∣∣w2∣∣w2,…,1∣∣wN∣∣wN],\frac{W}{||W||} = \left[\begin{matrix}\frac1{||w_1||}w_1, \frac1{||w_2||}w_2,\ldots,\frac1{||w_N||}w_N\end{matrix}\right],∣∣W∣∣W​=[∣∣w1​∣∣1​w1​,∣∣w2​∣∣1​w2​,…,∣∣wN​∣∣1​wN​​],

and ⊙\odot⊙ stands for a special kind of element-wise product.

Now, here’s an image illustrating the patterns of change:

On the ΔM\Delta MΔM axis, we have MAE between ∣∣W∣∣||W||∣∣W∣∣ before and after fine-tuning. On the ΔD\Delta DΔD axis, we have mean (1−cos⁡(⋅,⋅))(1 - \cos(\cdot, \cdot))(1−cos(⋅,⋅)) distance between 1∣∣wi∣∣wi\frac1{||w_i||}w_i∣∣wi​∣∣1​wi​ before and after fine-tuning.

For LoRA, there is a notable positive correlation between ΔD\Delta DΔD and ΔM\Delta MΔM, while for full fine-tuning (FT), these values exhibit a weaker negative correlation. This hints that in LoRA, magnitudes and directions might become entangled in a suboptimal way. To address this, the authors of DORA suggest decoupling them during fine-tuning. Specifically, they update the weight matrix as

W′=m⊙W0+BA∣∣W0+BA∣∣,W' = m \odot \frac{W_0 + BA}{||W_0 + BA||},W′=m⊙∣∣W0​+BA∣∣W0​+BA​,

where:

- W0W_0W0​ is the initial WWW before fine-tuning,

- mmm is a trainable magnitude vector, initialized as ∣∣W0∣∣||W_0||∣∣W0​∣∣,

- BABABA is a low-rank LoRA summand with trainable matrices AAA and BBB,

- Division by ∣∣W0+BA∣∣||W_0 + BA||∣∣W0​+BA∣∣ means division of each column of W0+BAW_0 + BAW0​+BA by its length.

The method can be summarized in this table:

As you could see in the earlier plots, the correlation between magnitude and direction updates exhibits a weak negative correlation, similar to what we see in full fine-tuning. This correlation can be really important, as in experiments, DORA consistently outperformed LoRA (well, if +1 point in quality is enough for you).

This article was inspired by my experience of teaching linear algebra and by discussions at the paperwatch meetings of the Practical Generative AI course by School of AI and Data Technologies. If you’re interested in studying LLMs and other generative models, their internal workings and applications, check out our program.

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

Transformer alternatives in 2024

With this article, we are starting a new category on our blog, the one dedicated to AI research. Expect these posts to be very technical and insightful. The first one is about possible alternatives to the key component of the LLM architecture.

March 28, 2024
12 mins to read

### 

Nebius AI monthly digest, April 2024

Our main news of the past month is that Nebius AI has become available to everyone! We also participated in the MLOps podcast and published several videos about setting up training, as well as stories about how Nebius AI clients are building their models.

May 6, 2024
5 mins to read

### 

Joining AI research community: overview for industry experts

ML communities in industry and academia differ greatly. Today, we’ll bring them a bit closer with an overview of the research world for those building services. Take a moment to explore the neighboring domain, which is much more accessible than it seems.

February 21, 2024
12 mins to read

Sign in to save this post
Sign In
