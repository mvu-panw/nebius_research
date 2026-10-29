# What is supervised fine-tuning in LLMs? Unveiling the process

Source: https://nebius.com/blog/posts/fine-tuning/supervised-fine-tuning

Skip to main content

Supervised fine-tuning (SFT) uses domain-specific labeled data to tune the model parameters. The model can import knowledge from a specific domain with significantly less data and training time. A fine-tuned model retains the general knowledge from its initial pre-training and expands its knowledge base using the additional dataset.

This article will discuss everything there is to know about supervised fine-tuning, including its working mechanism, benefits, challenges, and more.

## What is supervised fine-tuning?What is supervised fine-tuning?

A foundation large language model like GPT or Llama is trained on large amounts of data containing knowledge from various domains and fields. These pre-trained language models are an excellent source of general knowledge and for casual conversation but are not very helpful in task-specific scenarios.

Supervised fine-tuning uses a custom-labeled dataset to fine-tune the model for downstream tasks. The dataset contains in-depth knowledge regarding a specific domain and helps the LLM understand the intricacies required to perform niche tasks.

The supervised learning process uses the foundation model’s weights as the base and adjusts them according to the new data seen. For example, a model fine-tuned on IT documents will better understand computer systems. It will also perform better in assisting the user.

Although fine-tuning is less computationally expensive than pre-training, it must be noted that supervised fine-tuning is more expensive than unsupervised pre-training. The SFT approach compares its results with ground truths, whereas the latter only looks for patterns in unlabelled data. Due to this, SFT has higher accuracy at the cost of higher computation.

## How does supervised fine-tuning work?How does supervised fine-tuning work?

Delivering an LLM from a basic language model to a deployable solution is a three-step solution. These steps train and tweak the model until it is ready for domain-specific tasks. They include:

- 

Pretraining: The first step is to create a baseline foundation model by pre-training existing popular LLM architectures. The pre-training is the most expensive step of the pipeline as it requires a vast dataset covering knowledge from all corners.

Moreover, it requires expensive hardware and several days of training. For reference, the original BERT-base model was trained for four full days on 64 Google TPUs. However, the pre-trained model covers all knowledge areas and can be further specialized.

- 

Data labeling: The second step is to obtain the task-specific dataset. The data collection process can be overwhelming, especially for niche domains, requiring collecting, processing, and labeling text elements. ML engineers must collect a high-quality dataset covering all potential examples for the best results.

- 

Fine-tuning: Once all the data is collected and the pre-trained model is ready, we can continue with supervised learning. The specialized data set trains the base weights of the foundation model and tweaks them to cover additional knowledge from a specific domain. The final model retains the general information from its original knowledge base but has an in-depth understanding of the particular domain.

The fine-tuned model can be integrated into existing systems for task automation. It can also be used for cross-referencing queries or as ground truth for domain-specific questions.

## Benefits of supervised fine-tuningBenefits of supervised fine-tuning

SFT can be cumbersome, especially due to the required data collection and labeling a cumbersome process, especially due to the data collection and labeling required. However, it has several benefits that make it worth the effort. They include:

- 

Improved performance. The additional dataset and training allow the model to learn task-specific patterns, improving its domain understanding. The fine-tuned model better understands the provided data and performs better on related queries. Not only does the model produce factually accurate responses, but it also constructs them appropriately for the task. For example, as a call center agent, the LLM is expected to provide relevant information and generate responses courteously.

- 

Data efficiency. SFT is particularly beneficial in data-limited scenarios where data scarcity might bottleneck a model’s training from scratch. Since a pre-trained model already covers a vast knowledge base, it requires very little additional information for fine-tuning. The pre-existing knowledge covers subtleties like sentence structuring, the semantics of human conversation, and even some parts of the domain knowledge. The additional SFT procedure requires comparatively less data to turn the model into a subject matter expert.

- 

Resource and cost efficiency. Fine-tuning requires a relatively small dataset, making it computationally inexpensive. Compared to the tens or hundreds of GPUs required for a foundation model, SFT can be performed on limited hardware resources in a few hours. Fine-tuning saves organizations from hefty cloud or physical GPU costs, improving the final application’s ROI. Data efficiency also reduces costs, as less time and resources must be spent collecting and annotating datasets.

- 

Versatility and flexibility. Fine-tuning allows developers to use and train a single foundation model for multiple domains. The model can power various use cases, and the responses can be structured according to each domain’s requirements. Moreover, during fine-tuning, developers can introduce new, company-specific regulations and tweak the output response as desired. For example, the model can be taught not to output certain responses or deny answering certain questions to comply with company guidelines or local regulations.

## Common supervised fine-tuning techniquesCommon supervised fine-tuning techniques

A deep learning model consists of multiple layers, each responsible for understanding different aspects of the task. These layers contain the model weights, which are updated during SFT.

However, not all the layers need to be updated for fine-tuning. Different supervised learning techniques update model weights in different ways. Each technique is suitable for different use cases and resource availability. Let’s discuss some popular SFT techniques.

### Full fine-tuningFull fine-tuning

Full fine-tuning is similar to training a model from scratch since it involves updating all parameters. This technique can be costly as the pre-trained model can contain billions of parameters that need updating.

Full fine-tuning yields the most accurate results as the model learns data features across all its layers. Moreover, it provides maximum flexibility as the model learns new data patterns across all its layers. It understands all language subtleties for the specific domain and can be a good option if time and resources are not constrained.

### Parameter-efficient fine-tuning (PEFT)Parameter-efficient fine-tuning (PEFT)

PEFT is a resource- and time-efficient alternative to full fine-tuning. It works by keeping existing model layers frozen. Instead, it adds extra task-specific layers to be trained for downstream tasks. The frozen weights retain the model’s knowledge from its pre-training, and the additional modules learn to perform domain-specific tasks. Developers may even choose to unfreeze some of the model layers for better learning.

Since PEFT only updates selected parameters, it has a significantly small computational cost compared to full fine-tuning. However, as the model largely remains untouched, PEFT provides less accurate results but can be a good option if resources are limited.

### Instruction fine-tuningInstruction fine-tuning

Instruction fine-tuning uses a dataset similar to normal SFT, but instead of targeting the knowledge base, it aims to improve the model’s instruction-following capabilities. The dataset comprises instruction-response pairs that teach the model to construct responses following certain steps.

Instruction fine-tuning helps train models for automation processes that require instruction following to execute commands.

## Fine-tuning vs. Retrieval augmented generation (RAG)Fine-tuning vs. Retrieval augmented generation (RAG)

Both fine-tuning and Retrieval Augmented Generation (RAG) improve the model’s performance in task-specific use cases. However, their implementations and model interactions are vastly different.

Fine-tuning uses labeled data to train the model and update its weights directly. The SFT procedures include data collection and lengthy model training operations, depending on the hardware available. They are time- and resource-consuming, but the knowledge is infused within the model and carries no additional overhead once the training is complete.

RAG, on the other hand, relies on external knowledge to improve an LLM’s responses. It attaches an external data source containing domain-specific information to the language model. RAG implementation requires no labeled data, as no training is involved. Instead, it analyzes the user’s query at runtime and extracts the relevant information from the data store.

The RAG architecture includes key modules like an efficient vector datastore, vector data optimization, and efficient information retrieval algorithms to improve the system response time.

When a user enters a query, it is:

- Converted into an embedding.

- Compared to the knowledge vectors in the external knowledge base.

- Close-matching vectors are retrieved from the database.

- An appropriate response is formed using the retrieved knowledge.

RAG is ideal for scenarios requiring frequent database updates. While SFT requires a lengthy training process for knowledge updates, RAG only needs data updates in the external knowledge store. However, RAG always requires an external database connection, which might not be possible in all scenarios.

Moreover, SFT takes the lead in improving model performance since it provides greater flexibility regarding model behavior, response structuring, and instruction following. SFT also allows the same model to be trained for various tasks when labeled data is available.

## Evaluating the effectiveness of supervised fine-tuningEvaluating the effectiveness of supervised fine-tuning

Once the fine-tuning operation is complete, the model must be evaluated for performance monitoring. The judgment criteria for LLMs remain the same as conventional AI and metrics like accuracy, precision, recall, and F1-score are still relevant. We also have metrics, like BLEU and ROUGE scores, that are purpose-built for text outputs. The selection of metrics depends on the task at hand.

- Accuracy: This is a general metric that judges the model’s overall response. The accuracy percentage depicts how many of the provided answers agree with the ground truth.

- Precision: Precision judges the model based on the false positives in the response. A higher precision means the model can better judge the positive category.

- Recall: Recall judges the model on its ability to discern false negatives. A higher recall means that the model produces fewer false negatives and is better for use cases where it is critical to miss any positives.

- F1-score: The F1-score balances precision and recall. It is the harmonic mean between the two and provides a balanced evaluation of the model.

- BLEU score: This metric is purpose-built for machine translation use cases. It compares the machine’s output to reference and human translations and provides a score between 0 and 1. 0 means there is no overlap between the two, while 1 represents a perfect overlap.

## Common issues with supervised fine-tuningCommon issues with supervised fine-tuning

SFT has various benefits, but it also accompanies certain challenges that must be addressed. These include:

- Overfitting: The model can overfit on the fine-tuning dataset and perform poorly on unseen examples. This can be solved by using regularization techniques or applying dropout during fine-tuning.

- Hyperparameter tuning: SFT might be more efficient than pre-training, but the hyperparameter tuning operations can be cumbersome. Finding the optimal learning rate and batch size is time-consuming, and using sub-optimal settings will disturb training efficiency.

- Data quality issues: Model performance after fine-tuning largely depends on the quality of the training data. The model will display inconsistent performance if the data does not contain adequate, clean information. Therefore, ensuring quality data collection, annotation, and pre-processing is imperative.

- Catastrophic forgetting: Since SFT updates model weights directly, the update procedure may overwrite the previous knowledge learned during pre-training. The model will still be good for task-specific cases but will not perform well in general scenarios. However, techniques like Functionally invariant paths (FIP) are known to reduce the effect of catastrophic forgetting.

## ConclusionConclusion

Supervised fine-tuning is a powerful technique for modifying LLMs and aligning their outputs with specific use cases. It allows developers to teach LLMs new information and modify their behavior with limited labeled data and without long-running training.

Models can be fine-tuned by modifying the entire architecture or a few layers depending on resource and data availability. Moreover, LLMs can also be taught instruction followed by fine-tuning instruction-response pairs. However, certain challenges, like catastrophic forgetting and data quality issues, can hinder the model’s performance in general and task-specific scenarios.

Overall, SFT allows pre-trained LLMs to be used with various applications. It makes language models accessible and their use convenient for the general audience.

## FAQ

What is supervised fine-tuning and what is it for?

Supervised fine-tuning (SFT) uses labeled data to train LLMs for domain-specific applications. Its goal is to teach a model new information without an extensive dataset or long training routines.

Can you give fine-tuning examples?

An example of fine-tuning is using medical documents to tune a pre-trained LLM. The fine-tuned model will retain its previous knowledge and understand medical terminologies and queries.

What is self-supervised fine-tuning?

Self-supervised fine-tuning works in two steps. First, it pre-trains a model on massive amounts of unlabelled data (self-supervised training). Next, it fine-tunes the model using a labeled dataset for downstream tasks.

Why can fine-tuning be problematic?

Fine-tuning can lead to challenges like over-fitting, hyper-parameter tuning, and catastrophic forgetting.

## Explore Nebius AI

Get started​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

### 

Fundamentals of LoRA and low‑rank fine-tuning

In the next installment of our series of deep technical articles on AI research, let’s switch our attention to the famous LoRA, a low-rank adaptation technique.

May 13, 2024
11 mins to read

### 

Demo: applying retrieval-augmented generation with open tools

Retrieval-augmented generation (RAG) is a technique that enhances language models by combining generative AI with a retrieval component. Let’s examine a quick example of applying RAG in a real-world context.

April 18, 2024
6 mins to read

Sign in to save this post
Sign In
