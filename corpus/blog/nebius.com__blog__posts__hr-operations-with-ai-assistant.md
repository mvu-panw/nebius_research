# How we streamlined HR operations with an AI assistant (and why you should too)

Source: https://nebius.com/blog/posts/hr-operations-with-ai-assistant

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

In today’s fast-paced business environment, HR departments are often overwhelmed with repetitive questions and routine tasks. From vacation policies to benefits explanations, HR professionals spend countless hours answering the same questions from employees. This leaves them with less time to focus on strategic initiatives and complex personnel matters. This is where AI technology steps in to transform how HR operations.

At Nebius, we addressed this challenge by developing an intelligent HR Assistant powered by the Nebius AI Studio platform. This sophisticated solution automatically handles most HR-related questions while recognizing when to escalate sensitive topics to human HR professionals. The result? A reduced burden on our HR team, allowing them to focus on strategic initiatives — plus, employees enjoy much faster responses as an added bonus.

In this article, we’ll explore how the HR Assistant works, from its ability to understand context and retrieve relevant information to its smart handling of sensitive topics. Curious about AI in HR or planning to implement it? Let’s explore how technology can streamline HR tasks without losing the personal touch that matters.

# Key takeawaysKey takeaways

### Business impactBusiness impact

- Transformed HR efficiency: Automated responses to 150+ monthly HR queries, freeing up 13+ hours of specialist time for strategic initiatives.

- Lightning-fast responses: Employees get answers in seconds instead of waiting hours or days, significantly improving the workplace experience.

- Enterprise-grade reliability: The solution seamlessly scales to handle repetitive questions, allowing HR teams to focus on high-value work.

- Consistency: Ensures document-based, standardized responses to common HR inquiries across the organization, reducing the risk of misinformation.

### Why it mattersWhy it matters

- Employees receive instant, accurate answers 24/7.

- HR teams can focus on strategic, high-value work.

- Sensitive topics are still handled with a personal touch.

- The solution scales effortlessly across multiple countries.

# How our HR Assistant works: A technical overviewHow our HR Assistant works: A technical overview

At its core, the HR Assistant leverages natural language processing (NLP) techniques and retrieval-augmented generation (RAG) to provide accurate, context-aware responses to employee queries. Like most modern companies, we maintain a Confluence knowledge base with several spaces containing articles that address HR-related questions. The HR Assistant taps into these articles to handle employee inquiries.

### General structureGeneral structure

The HR Assistant pipeline is presented in image 1. Under the hood, it relies on two types of NLP models: text-to-text generation and embedding models. Thanks to Nebius AI Studio, integrating these models into your application is seamless and requires just a few lines of code. The best part? With AI Studio’s OpenAI-compatible API, switching from OpenAI models to AI Studio models is as simple as changing a single client argument. Let’s explore how to harness these powerful models in action!

These models can be accessed through simple requests, but using the OpenAI client is more convenient. First, import and set up the client:

from openai import Client
client = Client(
 base_url="https://api.studio.nebius.ai/v1",
 api_key="<GET YOUR NEBIUS AI STUDIO API KEY AT https://studio.nebius.ai/settings/api-keys>",
)

Alternatively, you can configure environment variables and initialize the client without any arguments:

export OPENAI_BASE_URL=https://api.studio.nebius.ai/v1
export OPENAI_API_KEY=<GET YOUR NEBIUS AI STUDIO API KEY AT https://studio.nebius.ai/settings/api-keys>

from openai import Client
client = Client()

To make a call to text generation LLM, provide a list of messages formatted as a list of dictionaries:

messages = [
 {
 "role": "system",
 "content": system_message,
 },
 {
 "role": "user",
 "content": user_message,
 },
]
completion = client.chat.completions.create(
 model=model, # selected model from AI Studio models
 messages=messages,
 max_length=256, # maximum length of the model response in tokens
 top_p=0.01, # to increase the determinism of the model response 
)

For embedding models, you can input either a text or a list of texts, which will be automatically processed in batches:

client.embeddings.create(
 model=model, # selected model from AI Studio models
 input=[text1, text2],
)

For more details on AI Studio models, visit Docs.

For our production infrastructure — including the Kubernetes cluster, PostgreSQL database, object storage and more — we rely on Nebius Cloud, which streamlines deployment at every step.

Now that we’ve covered how to integrate AI Studio models into our application, let’s break down the key components that make the HR Assistant both efficient and reliable.

### Question contextualizationQuestion contextualization

When a user asks a follow-up question within an ongoing conversation rather than starting a new, independent query, they may reference previous context. To ensure the retriever can find the most relevant documents, we must first contextualize the user’s question. This mimics the natural flow of human conversation, allowing employees to receive precise answers that account for prior exchanges. To achieve this, we send the query to an LLM and request it to reformulate the user’s question into a standalone query, incorporating context from the conversation if necessary. We use the following prompt:

Given a chat history and the latest user question, which might reference context in the chat history, formulate a standalone question (query) that can be understood without the chat history.

Do not answer the question — only reformulate it if needed, or return it as is.

Your response will be passed to the retriever, which will extract relevant articles based on your output.

Hence, return only the query and nothing else.

### Intelligent topic routingIntelligent topic routing

Not all HR matters should be handled by AI — some topics (especially compensation-related issues) require human HR intervention. We maintain a predefined list of topics for where the bot should redirect the user to their HR manager, including salary and performance-related questions, questions about receiving an offer from another company, etc. To determine whether a message pertains to any of these topics, we make another LLM call. If the model detects a restricted topic, we automatically forward the user’s message to their HR manager.

This process is highly efficient (0.3–0.5 seconds on average) because we only require a single output token (“0” or “1”). We leverage the guided_choice feature of AI Studio models to force the model to always output either “0” or “1”. To fully harness the potential of this feature, the prompt should explicitly instruct the model to output only “0” or “1”. Since LLMs tend to assign exaggerated probabilities to the most likely token due to their training loss function, it’s beneficial to reinforce this binary choice.

Modern LLMs are smart but not omniscient. Because this is a complex multi-class classification task without fine-tuning, we recommend using few-shot learning instead of zero-shot classification. Including at least one example per topic in the prompt significantly improves accuracy. These examples should mimic real employee questions, incorporating style, potential abbreviations, errors and other natural language elements. This will reduce the amount of “shock” the model experiences when dealing with such questions.

Due to confidentiality reasons, we cannot share the exact prompt. Generally, it looks as follows:

You are a helpful HR AI assistant at Nebius.
You strive to help the users (employees) with their questions.
Your goal is to check whether the user’s (employee’s) request is related to any of the topics below.
If it is related to any of these topics, output "1". Otherwise, output "0". Don’t output anything else.

Topics:
1. <topic_1>
- Example: "<example_of_the_question_related_to_topic_1"
...
n. <topic_n>
- Example: "<example_of_the_question_related_to_topic_n"

Examples for few-shot learning:
"""
User: in what countries does Nebius have offices
Assistant: 0

User: <example_related_to_some_of_the_topics_above>
Assistant: 1
...
"""

### Location-aware intelligenceLocation-aware intelligence

Modern companies often operate across multiple countries, each with its own regulations and policies. Our HR Assistant is designed to handle this complexity intelligently. For instance, when an employee asks about non-working days, the answer can vary significantly between countries — in 2024, for example, the Netherlands and Serbia shared only two common public holidays. To retrieve the most relevant documents from the knowledge base in such cases, we need to incorporate the user’s location into the query sent to the retriever.

At the same time, some inquiries are location-agnostic. These can be general questions about the company (“Is Nebius publicly listed through an IPO?”) or about company-wide policies (“Can you explain the differences between various types of employee leave policies (e.g., parental leave, sick leave, etc.)?”). If we unnecessarily include the user’s location in the retriever query for such questions, the retriever might incorrectly prioritize location-specific articles, leading to the omission of more relevant, general answers.

To address this, we make an additional LLM call to determine whether the user’s location (country) should be included in the retriever query. Similar to the previous LLM call, this classification requires only a single output token (“0” or “1”), ensuring rapid processing — approximately 0.3–0.5 seconds on average with AI Studio models.

Our prompt for this step is provided below:

You are a helpful HR AI assistant at Nebius.

You answer users’ (employees’) questions based on the relevant articles from our Confluence (knowledge base).

Nebius has offices and employees scattered around the world, and responses to many employees' questions depend on the employee’s country.

Your task is to determine, given a user’s (employee’s) question, whether the user’s location (which is not provided in the query by default) needs to be integrated into the question to make a correct query to Confluence (knowledge base).

You should output "1" if the question requires knowing the employee's country (location), and "0," if the question is country-agnostic.

If you output "1", the user's location will be added at the end of the query. For example, if the user’s country is "Netherlands":

Question: "Where can i have lunch near the office?" will be transformed to "Where can i have lunch near the office? Netherlands"

Question: "what are non-working days" will be transformed to "what are non-working days Netherlands"

Respectively, if you output 0, the question remains unchanged.

Always output either 0 or 1 and nothing else.
Examples for few-shot learning:
User: Where can i have lunch near the office?
Assistant: 1

User: refer a friend
Assistant: 0

<more_few_shot_learning_examples>

### Searching for relevant information in the knowledge baseSearching for relevant information in the knowledge base

After preprocessing the input question, the HR Assistant retrieves relevant information from our internal knowledge base. In our case, this means tapping into our Confluence portal, which contains HR-related documents, including policies, FAQs and guidelines for employees across different regions.

To perform the retrieval, we use two parallel approaches:

- 

Embeddings search. Before launching our HR Assistant, we embed every article in our knowledge base — along with its sections, subsections and titles — using a state-of-the-art, commercially permissible LLM, BGE-ICL, which has an embedding size of 4,096. To ensure no details are lost in a single embedding vector, we split each Confluence article into logical sections and subsections. The extracted textual data is then divided into two groups: “contents” (includes articles, sections and subsections) and “titles”. Our experiments showed that embedding search within titles can yield relevant articles even when the search across contents struggles to do so. We optimize this step by parallelizing these two types of embedding searches.

When an employee asks a question, the system generates an embedding for this query and calculates its cosine similarity against each stored embedding for contents and titles. It then picks the articles corresponding to the top-k1 most similar contents and to the top-k2 most similar titles to employ later for generating a response.

Since internal documentation typically doesn’t contain millions of articles, we can optimize search performance by storing all embeddings in RAM instead of using a vector database. In our case, the number of articles is around 1000, and the total number of content embeddings (since we also include sections and subsections) is around 3000. Therefore, simple matrix multiplication will cost:

⟨vector_dim⟩×⟨length_matrix_size⟩×⟨right_matrix_size⟩×⟨dtype_bit⟩⟨bits_to_bytes⟩×⟨bytes_to_megabytes⟩=\frac{\langle\text{vector\_dim}\rangle \times \langle\text{length\_matrix\_size}\rangle \times \langle\text{right\_matrix\_size}\rangle \times \langle\text{dtype\_bit}\rangle}{\langle\text{bits\_to\_bytes}\rangle \times \langle\text{bytes\_to\_megabytes}\rangle} =⟨bits_to_bytes⟩×⟨bytes_to_megabytes⟩⟨vector_dim⟩×⟨length_matrix_size⟩×⟨right_matrix_size⟩×⟨dtype_bit⟩​==4096×3000×1×328×10242 MB=47 MB= \frac{4096 \times 3000 \times 1 \times 32}{8 \times 1024^2}\text{ MB} = \text{47 MB}=8×102424096×3000×1×32​ MB=47 MB1024×2 is used here to calculate the number of megabytes.

This is negligible in comparison to managing a separate database, and multiplication of matrices of this size takes just a few milliseconds even on a CPU. Since we already extracted article titles and contents when creating embeddings, we can skip the overhead of scraping article content at query time. As a result, embedding search completes in just a few milliseconds.

When relying on cached articles, we must regularly update the cache to reflect any changes in the knowledge base. We achieve this through a nightly cron job that re-scrapes and re-embeds the relevant articles at 3:00am daily before relaunching the bot. This ensures employees always have access to up-to-date information when they log in the next morning.

- 

Confluence keyword search. In parallel, we perform a classic keyword-based search within Confluence. While this step takes a few seconds and is generally less precise than embedding-based search, it can occasionally retrieve relevant information when embeddings miss the mark — particularly when a user’s query closely matches specific keywords in an article. Similar to embedding search, we retrieve at most top-k3 relevant articles. However, because Confluence search only returns results with exact keyword matches, it may yield fewer than k3 articles).

As soon as these two searches complete, we end up with k1 + k2 + k3 potentially relevant documents. However, duplicates and irrelevant results can still be present because we simply select top-k most relevant articles without verifying their actual relevance.

### Intelligent filtering with an LLMIntelligent filtering with an LLM

Feeding too many irrelevant articles to an LLM can degrade performance — it’s like finding a needle in a haystack, as demonstrated in a recent paper at ICML 2024. However, retrieving too few articles risks missing the single piece of information that holds the key to the right answer. To maintain the optimal balance, we introduce an additional filtering step.

We make another LLM call, instructing it to determine whether each retrieved article may contain relevant information for the user’s question. We deliberately soften this filtering procedure because including an irrelevant article is still less harmful than omitting a relevant one. Any article flagged as having potential relevance is passed to the final generation stage.

Like the previous classification steps, this process is blazingly fast because it requires only a single output token (“0” or “1”). The filtering typically takes around 0.5 seconds per article and is highly parallelizable. Depending on the size of the target retrieved article, this entire step averages 1–2 seconds in total.

### Crafting the “perfect” promptCrafting the “perfect” prompt

We found that a meticulously tuned system prompt plays a pivotal role in generating high-quality responses. Even using the largest available LLM (Llama-405B at the time of implementation) didn’t yield as much improvement as carefully crafting the prompt with extensive attention to detail. Through precise prompt engineering, we can:

- Minimize hallucinations: By clearly instructing the model to ground its answers in the provided articles, we reduce the risk of fabricated or misleading content.

- Integrate hyperlinks and references: Employees can jump directly to suggested resources and explore the articles used in generating the response for deeper insights.

- Indicate the LLM’s knowledge limits: If no relevant documents are available or if a question requires human HR intervention, the model promptly alerts the user.

### Minimizing wait time for employeesMinimizing wait time for employees

Even though the system involves multiple AI tasks — contextualization, topic routing, location tagging, retrieving and filtering articles and final response generation — we’ve carefully orchestrated each step to prioritize speed:

- Low-latency LLM calls: We use a slightly smaller, more optimized model (Llama-3.3-70b) instead of the massive Llama-405b, striking a balance between performance and speed.

- Parallelization: Nearly all retrieval and filtering steps run in parallel, with each sub-step optimized to minimize latency.

- Smart caching: We cache embeddings in RAM and update them once daily, eliminating the need to re-scrape and re-embed content in real time.

As a result, employees typically see the first token of the HR Assistant’s response within 4–5 seconds, with the full response generated within 7–10 seconds — far quicker than waiting for a busy HR professional’s reply.

# How Studio supercharges this workflowHow Studio supercharges this workflow

Throughout the entire process, Studio serves as the backbone for our LLM-driven features. Here’s why:

- Guided choice feature: We rely on this to enforce single-token outputs (“0” or “1”) for classification and filtering calls, ensuring consistent and fast responses.

- Flexible model hosting: Whether we need smaller, more agile models or want to experiment with the latest big LLM, Studio supports quick model swaps and scalable deployments.

- Prompt iteration and testing: The platform’s integrated environment allows data scientists, ML engineers and even non-technical stakeholders to refine prompts, test them live and evaluate model outputs — shortening our development cycle.

### Taking HR to the next levelTaking HR to the next level

Our AI-driven HR Assistant showcases how combining advanced retrieval strategies, state-of-the-art language models and a robust development platform like Nebius AI Studio can revolutionize day-to-day HR operations. Key benefits include:

- Faster response times: Employees receive nearly instant answers to routine HR queries, boosting overall satisfaction.

- Scalability and consistency: The AI efficiently handles repetitive questions, freeing the HR department to focus on strategic matters.

- Expert escalations: Sensitive topics (salary, performance reviews, job offers) or situations where the AI’s knowledge is insufficient get routed directly to human HR staff, ensuring a personal touch where it matters most.

To quantify this impact, let’s explore how much time the assistant has saved our HR department. The graph below illustrates the number of questions the assistant processed each given month:

This leaves us with approximately 156 processed requests per month. Given that each request typically requires approximately five minutes of an HR specialist’s time, this equates to ~780 minutes per month or ~13 hours — more than 1.5 workdays saved per HR specialist. And if your company is larger than Nebius, these savings will most likely grow even higher!

If your HR team is juggling countless requests or your organization spans multiple regions with diverse policies, consider implementing a similar AI-powered HR assistant. By leveraging Nebius AI Studio’s end-to-end capabilities — from generative AI to text embedding models — you can significantly reduce the administrative burden on your HR team while improving the employee experience.

# ConclusionConclusion

AI isn’t just about efficiency — it’s about creating seamless, context-aware experiences for employees. With the right platform and methodology, you can provide quick, accurate and empathetic responses while ensuring that critical human interactions are preserved for sensitive matters. Our HR Assistant at Nebius demonstrates that the future of HR is already here — and it’s powered by AI.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius

Sign up​
Docs​

Akim Tsvigun
Senior ML Solutions Architect at Nebius

## See also

### 

Creating images with Flux: Your prompt guide

With this complete prompt guide, you will learn practical tips for creating exceptional images with Flux on Nebius AI Studio. I will share clear, actionable insights from experience to help bring your AI art game to the next level. With Nebius AI Studio’s prices starting at $0.0013 per image, you can experiment with crystal-clear visuals up to 2000×2000 pixels without breaking the bank.

January 31, 2025
7 mins to read

### 

Transforming ideas into images: Introducing text-to-image generation on Nebius AI Studio

From concept art to product visuals, text-to-image AI is revolutionizing creative workflows, reducing hours of design work to mere minutes. Today, we’re excited to launch Nebius AI Studio’s text-to-image service, delivering premium, production-ready image generation at a fraction of typical costs.

January 22, 2025
4 mins to read

### 

Nebius AI Studio expands with vision models, new language models, embeddings and LoRA

As the holiday season approaches and we all juggle year-end projects, we’re excited to bring you a gift of expanded capabilities on Nebius AI Studio. These updates — including advanced vision models, a broader range of language models, powerful embeddings and LoRA hosting — are designed to help you jumpstart the new year with stronger, more versatile AI tools.

December 17, 2024
2 mins to read

Sign in to save this post
Sign In
