# Understanding pre-trained AI models and their applications

Source: https://nebius.com/blog/posts/understanding-pre-trained-ai-models

Skip to main content

# Pre-trained AI models definedPre-trained AI models defined

Pre-trained AI models are neural networks trained on large, diverse datasets to perform specific tasks like image recognition, language processing, etc. Pre-trained models can also be trained to perform more than one core task; when this is the case, they are referred to as pre-trained multi-task generative AI models (or multimodal pre-trained models).

As pre-trained models are trained on widely-varied data, they learn generalized patterns, providing developers with solid foundation models that can either be used as is or tweaked to build specialized models faster and easier.

The process of customizing pre-trained AI models involves techniques such as transfer learning and fine-tuning:

- 

Transfer learning refers to repurposing a model trained for one task to suit a new but related task. It involves using the pre-trained model as a feature extractor for building a specialized model, a technique where a model — say a pre-trained convolutional neural network (CNN) model — has its lower layers “frozen”, and used to extract features for creating a replacement final (or classifier) layer suited to the image type the new model is meant for.

- 

Fine-tuning involves retraining a pre-trained model for a new task or to improve its accuracy by adjusting its weights.

# How are AI models trained?How are AI models trained?

Training (pre-trained) AI models is a complex multistage process that involves exposing models to knowledge patterns and performing computationally intensive operations based on the model’s preferred architecture.

Here’s a breakdown of how AI model training works and common challenges/considerations of AI model training.

### Data collection and curationData collection and curation

AI model training begins with curating vast datasets from diverse sources, including web crawls, journals, Wikipedia and GitHub repos. The pre-training data, usually in one (for unimodal pre-trained models) or more (for pre-trained multi task generative AI models) of text, audio, image, code, format etc., is then cleaned. This involves filtering, de-identification and balancing to filter for noise, biases, harmful content, etc.

Source

Both processes are aimed at building LLM models that execute sophisticated tasks with human-like reasoning but without human failings and biases. After cleaning, data is tokenized — into a format the model can understand; models don’t work with text. There are various tokenization methods, including word-based and character-based tokenization.

# Model architecture selectionModel architecture selection

Foundation models broadly use a deep learning architecture, with multilayered neural networks trained to simulate human-like decision-making. But selecting a specific model architecture — the computational framework that defines how it processes data and produces results — depends on the task the model is supposed to achieve.

For example, transformer architectures are commonly used for natural language processing (NLP) because of their self-attention mechanism, which enables them to generate the most logical and statistically probable output.

Diffusion models are often employed in text-to-image pre-trained models for their ability to “diffuse” and reverse the diffusion of training data. This capability, when combined with a CNN (as the diffusion model’s core neural network), makes them excel at generating high-quality images from text prompts.

But beyond this, other considerations come into play, and model size is one. Parameter size must be carefully tuned in relation to training data to achieve the right parameter-to-token ratio: too many tokens per parameter, and the model overfits; too few, and the model underfits.

Enterprises developing pre-trained models must also consider the benefits vs. trade-offs of choosing between a dense model and a mixture of expert (MoE) model. Dense transformer models like Llama-3 prioritize generalized knowledge but are compute intensive. Conversely, MoE models like DeepSeek-R1 optimize compute and prioritize specialized knowledge but are more complex to build.

# Training techniquesTraining techniques

Once the model architecture is in place, deep learning begins and can be done using any of the following techniques: supervised, unsupervised, self-supervised and reinforcement learning.

### Supervised learningSupervised learning

This involves training a model on a labeled dataset, providing input-output pairs that helps the model’s algorithm determine its accuracy on training data.

A common application of supervised learning is classification problems where an algorithm is trained to accurately predict a discrete category based on labeled input.

Another application of supervised learning models is regression problems where an algorithm is trained to predict the continuous value of a variable in relation to another (labeled) input variable.

Source

### Reinforcement learning (RL)Reinforcement learning (RL)

In RL models, an algorithm is trained based on a reward system; as the algorithm interacts with its environment it receives feedback on the accuracy of its output, in the form of rewards or penalties.

An important use case for RL is sequential decision-making models, where agents are given intermittent feedback that ensures every step in the sequence of actions is leading to the desired output.

### Unsupervised learningUnsupervised learning

Unsupervised learning models are trained with unlabeled data and no desired outcome stated. From this, the algorithm is left to discover patterns and extract features on its own, although with tasks that help it infer some “ground truth”, e.g. filling in missing blanks in sentences, estimating missing parts of images, etc.

Unsupervised learning is commonly employed for training anomaly detection and data segmentation models.

### Self-supervised learningSelf-supervised learning

This learning technique deploys unsupervised learning for supervised learning tasks like classification and regression. Basically, the algorithm self-generates implicit labels from unlabeled data, instead of being fed supervisory signals.

This allows models to discover unknown patterns themselves, effectively solving the challenge of having to label the massive datasets used in training LLMs — an important upside of unsupervised and self-supervised learning.

However, training models this way can be more compute intensive as learning occurs over multiple iterations and requires some degree of hyperparameter tuning to optimize how the foundation model learns from large datasets.

Training dynamics considered include learning rate, attention heads, batch size and dropout rate. These dynamics are tuned using techniques like grid search, random search, etc., to balance for speed and output accuracy during model inference.

Self-supervised learning was used to train popular transformer models like GPT and BERT, computer vision models like Momentum Contrast (MoCo) and text-to-image models like DALL-E.

# Computational resources and infrastructureComputational resources and infrastructure

### Hardware accelerators: GPUsHardware accelerators: GPUs

Training foundation models is a costly, time-consuming process that requires several iterations to complete and lots of fault-resistant hardware.

So, to build more sophisticated models while dramatically reducing the training time, high-performance GPUs (graphical processing units) like GB200 NVL72 and HGX B200 are deployed.

These GPUs allow for larger batch sizes, faster throughput, shorter computation and processing times, which all add up to about 4x better training speeds and efficiency compared to lower range GPUs like H100.

### NetworkingNetworking

These GPUs offer parallel computing capabilities and advanced networking options, which makes it possible to build high-speed GPU clusters for distributed training. With each GPU offering 400 Gb/s speeds or more, GPU clusters connected via high-speed interconnects like NVIDIA Quantum-2 InfiniBand and Spectrum™-X Ethernet, can handle exaflop-scale calculations per second.

### SoftwareSoftware

Software is used to orchestrate the training process. Frameworks like PyTorch and TensorFlow are used to build, automate and monitor ML workflows. These frameworks run on workload managers like Kubernetes, Simple Linux Utility for Resource Management (Slurm) and Ray, which handle container execution, scaling, task scheduling and similar tasks.

### StorageStorage

Storage options for pretraining LLMs include filesystem, object storage and local SSD cache. Several considerations come into play when choosing the right storage and these considerations impact overall performance.

For instance, high-performance shared filesystem is needed for checkpointing and for use cases where high-speed data streaming to GPU accelerators is essential to the training process.

Similarly, scalable cost-effective object storage is needed for storing large (terabyte-scale) data volumes especially where high-speed data streaming isn’t an issue. But where fast read/write speeds are critical, the object storage can be combined with a high-bandwidth local SSD cache solution.

And where data type (text, image, etc.), pattern (read/write) and size is widely varied, a versatile storage like object storage is equally useful.

# Challenges of training large-scale modelsChallenges of training large-scale models

Here are the top obstacles to training LLMs and steps to mitigate them:

### Computational demandsComputational demands

Unlike small language models (SLMs) like BERT Mini, which have fewer parameters (11 million) and require limited computational resources to train, large-scale models are compute-intensive. They require top-of-the-range hardware at scale, driving up training costs substantially.

A way to side-step this challenge is to use pre-trained models. However, if training a new model is a must, techniques like mixed-precision training or knowledge distillation can help compress model sizes and reduce computational demands.

### ComplexityComplexity

As models grow larger, they also become more complex to train. Training time, data quality issues, data processing challenges (gathering, cleaning and tokenization of massive training data), number of iterations required and many more obstacles become more difficult to manage.

Nonetheless, you can cut training time by scaling GPU hardware, although that increases training costs. For data quality and processing issues take advantage of publicly available datasets and open-source tools like SpaCy.

### Ethical considerationsEthical considerations

Ethical risks like copyright infringement, ingesting harmful content, sensitive personal identifier information (PII) exposure and model bias must also be handled proactively. This can be done by using bias detection algos, deepfake detectors and guardrail models.

### Hardware failuresHardware failures

Despite optimization techniques and state-of-the-art hardware, training large-scale models pushes hardware to their limits with GPUs overheating and power grids getting strained, leading to hardware failures. Unfortunately, when this happens training gets disrupted or worse, the training process is lost.

Two important ways to handle this are to ensure hardware redundancy (additional hardware costs needed) and to store model checkpoints in high-speed storage (but large models need huge and costly storage).

# How are pre-trained AI models being used?How are pre-trained AI models being used?

Some real-world applications of pre-trained models include:

- 

Healthcare: Pre-trained models like Alphafold 3 and NVIDIA MONAI Zoo have transformed diagnostic imaging and medical research, enabling faster, more accurate disease diagnosis, anomaly detection, genomic analysis, drug discovery and treatment planning.

- 

Finance: Pre-trained models within frameworks like Morpheus are changing how the finance industry approaches risk assessment and fraud detection by providing real-time data, analyzing transaction patterns, evaluating market risks and discovering anomalies in real time.

- 

Technology: In the tech space, coding assistants (e.g. GitHub Copilot) are automating software development with code generation, code translation (across programming languages) and debugging capabilities, moving developers from weeks of writing code to days and from days of debugging to hours.

- 

NLP: Here, pre-trained models like Claude 3 are streamlining tasks like intent recognition, sentiment analysis, language translation and more, helping enterprises automate previously long-drawn processes.

- 

Media and entertainment: Pre-trained content and image generation models are creating human-sounding text as well as realistic images, videos and video games, pushing the boundaries of creativity while streamlining creative processes. Content moderation models are also being used to flag harmful or inciting content, especially on social media platforms.

- 

Pre-trained models are equally being employed in autonomous vehicle development for object detection, in customer relations for call center automation and in e-commerce for product recommendation and personalized search.

# Pros and cons of using pre-trained modelsPros and cons of using pre-trained models

### ProsPros

There are numerous benefits to using pre-trained models, including:

- 

As enterprises get to skip the resource-intensive, time-consuming process of model training and head straight for fine-tuning, using pre-trained models helps reduce training times and computational costs.

- 

Model training requires deep technical expertise; so, with training out of the picture enterprises have less of a need to employ or train costly model development expert teams.

- 

Pre-trained LLMs, due to their rich knowledge base and transfer learning advantage, boast improved performance on specialized tasks, post fine-tuning.

- 

Pre-trained models make previously inaccessible LLMs (due to cost and complexity) available to smaller organizations and startups, even those with limited AI expertise. These businesses can upskill their teams through AI automation courses, allowing them to invest in retrofitting existing models rather than building from scratch.

### ConsCons

Pre-trained models, no doubt, abstract the myriad challenges of training LLMs and lower the entry barrier for using large-scale models. However, using pre-trained models isn’t without some downsides. Let’s take a closer look at the most concerning limitations.

- 

Potential bias inheritance: Models learn from the human bias present in their training data. This bias includes potential disparities in the way a pre-trained model’s algorithm identifies people of certain gender, demography, race, etc.

For example, models associating “nurses” with female pronouns, misidentifying people from specific races, etc. Where these biases aren’t carefully filtered out, the specialized model may inherit them.

- 

Limited customization: Pre-trained models have a general-purpose design, often lacking niche expertise. And this means they may not be great to use as is for high-specialization tasks.

- 

Performance variability: All LLMs aren’t built equally, and some — due to factors like quality of training data, parameter-to-token ratio, model architecture, etc. — underperform compared to others.

### How can you mitigate the limitations of pre-trained AI models?How can you mitigate the limitations of pre-trained AI models?

Concerning as the downsides discussed may seem, there are tried and trusted countermeasures for abstracting them. Let’s explore these solutions, one at a time.

- 

Countermeasure for limitation 1: You can mitigate bias by using bias detection toolkits like AI Fairness 360 and Fairlearn. These tools comprise metrics and algorithms (e.g. Hierarchical Bias-Aware Clustering (HBAC) algorithm) for detecting potential disparities in model algorithm.

If the potential for bias is identified, the tools dig into the layers of the pre-trained model and highlight specific areas to allow you to fine-tune them for more balanced output.

- 

Countermeasure for limitation 2: Where highly nuanced tasks are required, fine-tuning and transfer learning can significantly improve model specialization.

As these models have already been trained on vast volumes of generalized data, freezing/unfreezing specific layers or fine-tuning pre-trained models on a small subset of niche-specific data can deliver the desired customized capabilities.

- 

Countermeasure for limitation 3: An easy way to handle this is to examine your preferred pre-trained model’s AI performance metrics before choosing it. These metrics, including accuracy, retention rate, precision and F1-score, show how well your chosen pre-trained model generates, predicts or classifies data.

# Discover the power of pre-trained AI models for your businessDiscover the power of pre-trained AI models for your business

Pre-trained models, such as GPT-4, DeepSeek-R1 and Claude 3, relieve enterprises of the burden of model training, having been “trained” on vast datasets beforehand. These models are not only driving AI adoption, they are also encouraging innovation.

They allow small businesses to harness the potential of large language models (LLMs) across diverse applications by simply fine-tuning the models at a fraction of their training costs. They also improve efficiency, eliminating the need to endlessly replicate LLMs, where fine-tuning to boost model specialization will do.

But choosing the right pre-trained model is essential; enterprises must carefully balance the strengths and limitations of pre-trained models. Equally important, enterprises must consider how suited the model is for their software architecture to ensure seamless integration. Looking to explore pre-trained models or learn which is the right fit for you? Check the Nebius AI Cloud services or chat with us today.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

AI model performance metrics: in-depth guide

Metrics provide a mathematical basis to assess AI model quality. Organizations use a range of metrics to measure every aspect of the AI model — from output, to speed, user experience and even ethics. This article covers 30+ metrics you can use to track AI progress.

December 13, 2024
12 mins to read

### 

AI model hosting options

This blog explores the process of AI model hosting, where trained models are deployed and made accessible via APIs for users and applications. It covers the complexities of running AI workloads in distributed environments, the different technology layers involved and key factors like performance, cost and security when choosing the best hosting option.

December 11, 2024
10 mins to read

### 

Leveraging training and search for better software engineering agents

In this blog post, we’ll share some of our recent findings on how search can enhance agentic systems for software engineering. Specifically, we’ll demonstrate how we’ve built an SWE-agent-based system that exclusively uses open-weight LLMs and achieves a 40.6% resolved rate on SWE-bench Verified.

November 15, 2024
10 mins to read

Sign in to save this post
Sign In
