# AI model performance metrics: In-depth guide

Source: https://nebius.com/blog/posts/ai-model-performance-metrics

Skip to main content

Your AI model is deployed to production. But how do you know if it is performing as expected? Many organizations use human feedback loops to assess output quality. However, manual checks are limited by human judgment and are less useful at scale. Enterprise-grade quality control requires AIOps implementation. Your goal should be to set up a CI/CD/CT pipeline that continuously integrates, tests, and deploys model changes in production.

But how are you going to quantify any improvements achieved? That’s where metrics come into play. AI model performance metrics present a system of evaluation and comparison. You evaluate the model in exactly the same manner, using the same dataset, both before and after a change. Comparing the two values gives you a clear measure of improvement.

This article explores different AI model metrics and their evaluation methods. Like many open-source AI models you can work with, there are innumerable metrics and benchmarks, and new papers on different metrics are published frequently. We only cover popular examples in this guide.

## Model quality metricsModel quality metrics

Relevancy metrics for LLM output evaluation (Source)

These metrics determine whether your AI model output addresses the given input in a concise and informative manner.

You can broadly group them into two categories:

- 

Statistical scorers statistically compare model output with a predefined ideal output (reference text).

- 

Model-based scorers use one AI model to evaluate the output of another.

We give some examples below.

### PerplexityPerplexity

Perplexity measures how well a language model predicts a word sequence. It relates to the next word’s probability distribution in your reference text sequence. A model assigning high probabilities to the correct next word receives a low perplexity score, indicating accuracy.

### BLEU scoreBLEU score

The Bilingual Evaluation Understudy (BLEU) score compares the n-grams (n consecutive words) with those of a reference text for translation tasks. A higher BLEU score indicates closer alignment between the generated text and the reference.

### ROUGE scoreROUGE score

Recall-Oriented Understudy for Gisting Evaluation (ROUGE) evaluates how many n-grams from the reference text are captured in the generated output. It measures the output quality of summary tasks by highlighting how much critical information is retained in the generated summary.

### Word error rate (WER)Word error rate (WER)

Word Error Rate (WER) measures the number of substitutions, deletions, and insertions needed to transform the generated output into the reference text. It is useful for measuring the output quality of speech-to-text tasks. A lower WER indicates better output quality.

### METEORMETEOR

Metrics like BLEU, WER, etc., check how closely your AI model output matches the reference text. They are not useful for evaluating open-ended tasks as they penalize phrasing variations (even if the output is otherwise semantically correct).

The Metric for Evaluation of Translation with Explicit ORdering (METEOR) addresses some weaknesses. It uses stemming, synonym matching, and ordering constraints to evaluate model output more flexibly. It considers the semantic meaning of words rather than n-gram matches.

### BERTScoreBERTScore

Some metrics, like BERTScore and BLEURTScore, use the LLM BERT to compare your model’s output with reference text. Instead of comparing text with text, BERT compares the vector embeddings. It converts reference and output text to their mathematical representation and compares them at that level. It can factor in semantics and assess more complex models.

### GPTScoreGPTScore

GPT compares your model’s output with the one it generates. For example, let’s say your model generates a document summary. GPT also generates the same results and then compares them. It assesses your model’s output against self-generated text to calculate the GPTScore.

## RAG metricsRAG metrics

RAG workflow (Source)

Many organizations implement RAG workflows as part of their AI model deployment. It is a cost-effective way of giving pre-trained AI models access to new information that is not part of their training data.

User input to the AI model is first passed to an intelligent search system. The system retrieves data relevant to the user’s query from the organization’s database and then passes it to the model. The model’s final output combines information from its training data and the organization’s knowledge base.

If your team implements AI models with RAG workflows, consider including the following metrics.

### FaithfulnessFaithfulness

This metric checks how accurately your model’s output reflects the RAG workflow information. For example, let’s say your RAG workflows retrieve HR policy documents for your model’s reference. If your model quotes HR policies from the document, it gets a high faithfulness score.

### Other metricsOther metrics

Other metrics mathematically check your model’s final output against retrieved data.

For example:

 | Metric
 | Calculation

 | Answer relevancy
 | The percentage of final output sentences that relate directly to retrieved data.

 | Contextual relevancy
 | The percentage of retrieved text relevant to user input.

 | Contextual recall
 | The percentage of final output that can be attributed to the retrieved text.

## User metricsUser metrics

Even if your AI model’s output is high quality, you need to check if it meets the needs of your end users. For example, if your users want text summaries but your AI model is better at classification, the output is not what the users expect. You must check user engagement with your model to justify costs, increase revenue, and justify any new feature changes. Some examples of metrics in this category.

### User satisfactionUser satisfaction

You calculate it manually from survey data or ratings that users provide. For quick feedback, you can simply ask users to rate the AI model response with some stars, thumbs up, or thumbs down. For more detailed information, ask pointed questions that can be mathematically aligned.

For example:

 | Metric
 | Question

 | Interaction rate
 | On average, how long do you interact with the AI model at a time?

 | User acceptance rate
 | How often do you accept the AI model response in your workflow?

 | Task completion rate
 | How often does the AI model response help you in completing your task?

High values indicate alignment between model performance and user expectations.

### Engagement rateEngagement rate

Measures how often users interact with the AI model’s output. You can calculate it by computing the number of daily/weekly/monthly:

- 

Users who submit prompts

- 

AI model responses without errors

- 

User views of responses

- 

User clicks on any reference links in the response

### Retention rateRetention rate

Monitors how often users return to use the AI model over time. High retention suggests users find continuous value in AI outputs, while low retention could indicate a lack of perceived usefulness.

### Conversion rateConversion rate

This metric assesses how often interactions with the AI model lead to desired outcomes, such as purchases or other business goals. It is useful for mapping investment vs. revenue growth and returns for commercial models.

## Speed metricsSpeed metrics

Speed metrics track model efficiency. You want the AI model to generate timely responses with minimum resource consumption. Some examples include…

 | Metric
 | Explanation
 | Indicator
 | Use case most relevant to

 | Latency
 | Measures the time it takes for the model to process a request and generate a response.
 | Lower latency indicates faster responses.
 | Real-time applications like chatbots or virtual assistants.

 | Cold start time
 | Measures how long the model takes to become operational after being initialized or restarted.
 | Lower values indicate higher efficiency.
 | Serverless AI applications.

 | Throughput
 | Number of tasks or queries the model can handle within a given time frame.
 | High throughput indicates your model can serve a large number of concurrent users.
 | Search engines or recommendation systems.

 | Resource utilization
 | The amount of computational resources (e.g., CPU, GPU, memory) the model consumes when processing input.
 | Low values indicate cost-efficient operations.
 | Non-commercial operations to keep costs low.

 | Scalability
 | Latency and resource consumption as input size/number of concurrent users increases.
 | High scalability is a must for enterprise AI.
 | Commercial operations.

## Cost metricsCost metrics

Cost metrics are important to keep track of AI investment, returns, operational expenses, and profits. Cost calculations vary depending on how your model is trained and deployed. If you are using existing LLMs via APIs/prompt engineering, you must keep track of prompt length, the number of API requests per user interaction, etc. If running your model on self-managed or cloud infrastructure, you must track costs against resource consumption. You’ll also need to factor in training, RAG workflows, and ongoing maintenance costs.

Some example metrics include:

### LLM call costLLM call cost

It is the expense you incur when making API calls to a third-party LLM provider, such as OpenAI.

It is calculated per API call based on:

- 

The number of tokens processed per request

- 

Amount of text input

- 

Amount of text output in each API call

You should track LLM call costs to optimize the frequency and length of API requests.

### Infrastructure costsInfrastructure costs

For AI models you deploy, cost calculations include compute utilization based on the number of tokens processed. Tokens represent the characters or words the model generates or analyzes. 429 responses (HTTP status codes for 'Too Many Requests') indicate that the system is overwhelmed by requests, possibly signaling that CPU/GPU capacity has peaked. So those need to be factored in as well.

Beyond compute, infrastructure costs include storage and networking needed for training and inference. Infrastructure costs are usage-based for models deployed on cloud platforms like Nebius.

### Operation costOperation cost

Operation cost refers to the ongoing expenses of running, maintaining, and securing the AI model over time. This includes costs associated with bug fixes, software updates, user support, monitoring, and security measures. Costs can vary depending on the AI model complexity, usage patterns, and tools you use.

## Responsible AI metricsResponsible AI metrics

Responsible AI is built on the three pillars of accountability, transparency, and accuracy.

### AccuracyAccuracy

AI model hallucination is a known challenge. AI models unpredictably generate false or misleading information. For critical use cases (like medical diagnosis), you may want to check your LLM output for factual accuracy before sharing data with the customer. You can consider using the following metrics.

#### SelfCheck GPTSelfCheck GPT

GPT self-evaluates its own output for factual consistency and generates this score. It generates multiple outputs for a given prompt and then compares them for any hallucinations. The higher the score, the more accurate the output.

#### QAG ScoreQAG Score

Question Answering and Generation Score uses a yes-no count to check your model’s output.

Other LLM checks as follows:

- 

Generate a series of close-ended questions based on your output.

- 

Answer them with yes or no.

- 

Calculate the QAG score by counting yes/no frequency.

For example, let’s say your model generates some information on the 9/11 attacks:

“On September 11, 2001, the United States experienced one of the most devastating terrorist attacks in its history. Nineteen hijackers from the extremist group al-Qaeda took control of four commercial airplanes, deliberately crashing them.”

Your evaluating model may generate questions like:

- 

Did the United States experience an attack on September 11, 2001?

- 

Was it the most devastating attack?

- 

Were 19 hijackers involved in the attack?

Then, the score is calculated based on the Yes/No frequency.

To complement accuracy metrics like SelfCheckGPT and QAG Score, metrics for accountability and transparency in Responsible AI can focus on ensuring that AI models operate ethically, fairly, and provide explanation. Below are suggested metrics for these two pillars.

### AccountabilityAccountability

Accountability is the ability to trace AI decisions back to responsible parties so the system behaves ethically. AI decisions are based on its training data. Some metrics to consider include:

 | Bias detection score
 | Bias detection tools can assess whether certain groups are over- or under-represented in training data.

 | Fairness score
 | Measures how equitably the model treats different demographic groups.

 | Model accountability index (MAI)
 | Assesses the degree to which the AI model complies with established legal and regulatory requirements.

### TransparencyTransparency

Transparency refers to the model’s ability to explain its decisions and the openness with which it operates. Some metrics include:

#### Explainability scoreExplainability score

This metric measures how easily non-experts can understand a model’s outputs and decisions. Tools like SHAP (Shapley Additive Explanations) or LIME (Local Interpretable Model-agnostic Explanations) provide insights into why a model made a particular decision.

#### Model transparency indexModel transparency index

This tracks whether the model adheres to guidelines requiring disclosure of its training data, algorithms used, and performance on key metrics. It evaluates how openly an organization shares information about its model’s workings, such as its sources of training data, biases detected, or accuracy trade-offs.

Stanford Transparency Index for Foundation Models (Source)

## ConclusionConclusion

AI model performance metrics are not just about output speed or user experience. They assess every aspect of your AI model, from training data to output quality. An organization’s AI maturity is indicated by the metrics it uses for measuring and monitoring AI performance. Metrics are critical for responsible AI development across industries.

## FAQ

What are metrics in AI?

Metrics in AI are quantitative measures used to evaluate a model’s performance, accuracy, and effectiveness. They help assess how well an AI model performs tasks, such as classification, summarization, or generation, by comparing predicted results with ideal outcomes

What is the best metric to evaluate model performance?

The best metric depends on the task. For classification, accuracy, precision, recall, and F1-score are common. For regression, mean squared error (MSE) and R-squared are preferred. Selecting the right metric depends on the problem`s goal and data characteristics.

What are the metrics for generative AI model performance?

Metrics for generative AI models include perplexity (for text), BLEU (for translation), and Fréchet Inception Distance (FID) for images. These metrics evaluate the quality, coherence, and diversity of generated content, ensuring it closely resembles human-created data.

What are the metrics for Gen AI productivity?

Metrics for Generative AI productivity include task completion time, user satisfaction, and output quality. These measure how effectively a generative AI tool assists in automating creative tasks, enhancing workflow efficiency, and maintaining high-quality outputs.

## Explore Nebius

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

Tips and tricks for performing large model checkpointing

There are various aspects to optimize when training large models. It often lasts weeks and involves managing billions of rows of data, with checkpoints of such models weighing terabytes in some cases. Let’s explore how to handle large model checkpointing.

March 11, 2024
9 mins to read

### 

On Kubernetes significance for ML/AI engineers

K8s has become the tool of choice for machine learning teams large and small. What are its properties that have made it today’s industry standard?

November 14, 2023
7 mins to read

Sign in to save this post
Sign In
