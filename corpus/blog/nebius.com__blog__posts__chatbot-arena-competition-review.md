# Chatbot Arena Human Preference Predictions: tech review

Source: https://nebius.com/blog/posts/chatbot-arena-competition-review

Skip to main content

A few weeks ago, the LMSYS competition on Kaggle finally finished. It presented a challenging task: predicting human preferences in comparisons between large language models. For context, the Chatbot Arena and leaderboard are popular tools where users can ask questions and compare models side by side. Users aren’t aware of the model names during evaluation, which makes it unbiased. The results are aggregated into an Elo rating system, which you can view on the leaderboard here.

Since I work with LLMs daily and sometimes spend time in the arena, it was especially interesting to participate. After a significant shake-up (Kaggle knew harder, though!), we dropped to 33rd place, but it was still a lot of fun. I learned many new things and greatly appreciate the Kaggle community for that experience.

Moreover, the competition was computationally demanding. With LLMs delivering strong results, running experiments across many iterations required significant GPU resources. Thanks to my colleagues at Nebius for providing an H100 GPU with easy access and great pricing, which made this possible.

This competition highlighted several useful techniques, including datasets, model comparisons, pseudolabeling, LLM ensembling methods and optimizations for both training and inference (Chris Deotte even managed to run a 33B model on 2xT4 GPUs). Let me know if you’re interested in hearing more about this.

One of the most inspiring results from the competition came from distillation, which helped the winning team secure first place. The author’s approach was about training a large model (such as Llama3-70B or Qwen2-72B) in a 5-fold setup and then distilling predictions (using KL divergence loss) into a Gemma2-9B model for each fold, resulting in five versions of Gemma. To obtain a single model, the author averaged the LoRA layers from the distilled versions of Gemma. All of this was achieved using a cluster of 8xA100 80G GPUs.

Model distillation continues to prove its strength. We’ve seen it succeed in many cases, including the latest Llama 3.1 models, and this competition is just another example of its potential.

## Explore Nebius AI

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Alexander Golubev
Lead ML Engineer

## See also

### 

How transformers, RNNs and SSMs are more alike than you think

By uncovering surprising links between seemingly unrelated LLM architectures, a way might be paved for effective idea exchange and boosting efficiency.

August 21, 2024
10 mins to read

### 

In-house AI R&D: Nebius’ secret ingredient for truly AI‑centric cloud

It wouldn’t be possible for us to build a machine-learning platform without advancing in the field ourselves.

July 29, 2024
9 mins to read

### 

Fundamentals of LoRA and low‑rank fine-tuning

In the next installment of our series of deep technical articles on AI research, let’s switch our attention to the famous LoRA, a low-rank adaptation technique.

May 13, 2024
11 mins to read

Sign in to save this post
Sign In
