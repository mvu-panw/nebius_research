# What is prompt engineering?

Source: https://nebius.com/blog/posts/what-is-prompt-engineering

Skip to main content

Very few companies have the budget to train a new large language model (LLM) from scratch. Most data science teams work with commercial and open-source LLMs like GPT, LLaMA, Mistral, etc., as they build AI applications for their enterprise.

Customizing these LLMs for your use case requires significant prompt engineering. It is the process of “communicating” with the LLM so your users get the output they expect. Prompt engineering is also one of the ways to prevent unauthorized, false, or inappropriate LLM output from reaching the end user.

This article explores prompt engineering in detail, including beginner and advanced prompting strategies for ML/AI engineers.

## Prompt engineering explainedPrompt engineering explained

Prompt engineering is the process of creating and optimizing “prompts, ” the natural language inputs needed to use the LLM across a range of tasks. To understand prompt engineering, you first need to know how LLMs work.

Think of the autocomplete feature on your phone. As you type, it suggests the next word, generally based on the latest/frequent word combinations. For example, if you type “Hello sir” frequently, it suggests sir every time you type “Hello.” LLMs work on the same principle, just on a much (much!) larger scale. They make next-word predictions based on training data from millions of existing documents.

To make better outputs, they need detailed input. Prompt engineering gives the context the LLM needs to respond to your user and effectively complete tasks. It maps user input from your AI app (user domain) to the LLM’s document domain so the LLM makes better predictions. AI app developers often have to develop innovative prompts so their AI apps respond correctly to end users.

## Prompt engineering examplePrompt engineering example

Consider you are building an AI chatbot that troubleshoots IT problems in an organization called XYZ Inc. Let’s consider the following situation:

Bot: — Hello! How may I help you today?

User: — The printer stopped working during the meeting. I couldn’t print out store analysis reports for my manager.

Feeding this user prompt directly to the LLM will not be helpful. The LLM has no context about what the user expects from your app. It may get side-tracked or start discussing the reports instead of the printer.

That’s where prompt engineering comes in. The app code wraps the user’s prompt in a “script” before feeding it to the LLM. The script may include additional documents to better guide the LLM.

Example prompt engineering script:

You are an IT support specialist for XYZ Inc. The organization has four printers: A, B, C, and D. You are on a call with an XYZ employee. The employee says: “The printer stopped working during the meeting. I couldn’t print out store analysis reports for my manager.” How will you respond? Your first goal is to identify the printer that needs troubleshooting. Then, refer to the relevant printer manual and suggest a solution.

For this example, the two different prompts were given to GPT 4. As you can see, the response with prompt engineering is more focused and results in better outcomes.

 | User prompt
 | LLM prompt
 | LLM output
 | Prompt engineering?

 | The printer stopped working during the meeting. I couldn’t print out store analysis reports for my manager.
 | The printer stopped working during the meeting. I couldn’t print out store analysis reports for my manager.
 | That sounds frustrating, especially during an important meeting! A quick fix could involve checking if the printer is connected properly or restarting it to see if it resolves the issue. If this happens frequently, it might help to consider digital backups, like sharing the reports via email or cloud services, to avoid future disruptions. Would you like suggestions on troubleshooting common printer issues, or are you looking for ways to ensure smoother report deliveries in the future?
 | No.

 | The printer stopped working during the meeting. I couldn’t print out store analysis reports for my manager.
 | You are an IT support specialist for XYZ Inc. The organization has four printers: A, B, C, and D. You are on a call with an XYZ employee. The employee says: “The printer stopped working during the meeting. I couldn’t print out store analysis reports for my manager.” How will you respond? Your first goal is to identify the printer that needs troubleshooting.
 | I’m sorry to hear the printer wasn’t working during your meeting. Let’s get that sorted out! Can you tell me which printer you were trying to use — Printer A, B, C, or D? Once we know that, we can start troubleshooting.
 | Yes.

## Prompt engineering basicsPrompt engineering basics

Prompt engineering includes many principles and practices that guide prompt development. The term “engineering” indicates a structured approach to the generally creative field of writing a prompt. The structure is necessary to ensure consistency in quality and define measurable success parameters. Before diving into different strategies, let’s overview the basic prompt structure. Think of prompts as blueprints — clear, well-organized ones lead to better results, while vague or poorly structured ones might yield irrelevant or inaccurate outcomes.

### Prompt structurePrompt structure

Prompt engineering looks at the same prompt from different abstraction levels. At its most abstract, prompt components present the basic building blocks of any AI prompt. They give a broad framework you can apply to any AI system, regardless of the specific platform or model you’re using.

You can also break down a prompt into elements that define the specific instructions that guide the AI. Elements are more customized to the AI system you’re interacting with.

You can look at a prompt as a recipe at a more detailed level. Recipes combine elements in specific ways to achieve the desired outcome. This is where the structure of the prompt becomes more refined and intentional.

The prompt instance is the actual prompt given to the LLM. It contains real data, objectives, and context for the LLM.

### Prompt componentsPrompt components

The essential components of a prompt are summarized in the table below. Whenever you write any prompt, try defining it using these five components.

 | Component
 | Explanation
 | Example

 | Task
 | The task you want the AI to do. This is not part of the actual prompt but tells you what the prompt does.
 | Generate a summary.

 | Instruction
 | Clearly describe what you want the AI to do. It should be direct and specific to guide the model effectively.
 | Summarize the following text in three sentences.

 | Context
 | Provide context so the AI understands the background or subject matter and generates a more relevant response.
 | The text is a report on customer feedback for a retail store in 2023.

 | Parameters
 | Specify any rules, formats, or constraints for the response, including word limits, tone, or style.
 | Keep your response under 50 characters and in a professional tone.

 | Input data
 | Provide the text, question, or data you want the AI to process. Include as many examples or details as possible.
 | Customer feedback: 'The staff was helpful, but I had to wait too long for assistance.'

The final prompt:

Summarize the following text in three sentences. The text is a report on customer feedback for a retail store in 2023. Keep your response under 50 characters and in a professional tone. Customer feedback: ‘The staff was helpful, but I had to wait too long for assistance.’

## Prompt engineering techniques for beginnersPrompt engineering techniques for beginners

Prompt engineering techniques present specific approaches to prompting for different tasks. Depending on the context, you can keep your prompt short and sweet or write a lengthy paragraph with examples and details. Promptingguide.ai gives comprehensive explanations for each technique. We present a “prompt-engineering cheat sheet” below so you can quickly find the prompt strategy you need for your use case. These prompts are typically used with a single LLM.

 | Technique name
 | Explanation
 | Prompt example
 | Common use case

 | Zero-shot prompting
 | Ask the model to perform a task without providing any prior examples.
 | Translate this sentence to French: 'I am learning AI.'
 | Translation, classification, fact-finding.

 | Few-shot prompting
 | Provide a few examples before asking the model to perform the task.
 | I have translated these sentences into French: ‘Hello, world.’ -> ‘Bonjour, le monde.’ ‘I love AI.’ -> ‘J’adore l’IA.’ Now you translate: ‘This is awesome.’
 | Complex classification, summarization, writing.

 | Chain-of-Thought (CoT) prompting
 | Encouraging the model to break down reasoning into steps to improve complex task performance.
 | Solve: 12 + 3 * (4 — 2). First, calculate 4 — 2. Then, multiply the result by 3. Finally, add 12.
 | Mathematical reasoning, problem-solving.

 | Multimodal CoT
 | Use CoT techniques across multiple data types, like text and images, for comprehensive reasoning.
 | Analyze this image and explain the events in it using text.
 | Image-text reasoning, cross-data type tasks.

 | Self-Consistency
 | Run multiple CoT samples and select the most consistent answer.
 | Explain why the Earth revolves around the sun. Answer multiple times from different perspectives (astronomer, scientist, student).
 | Logical reasoning, improving reliability.

 | Tree of Thoughts (ToT) prompting
 | Structuring the model’s thought process as a tree, exploring multiple paths, and selecting the best one.
 | Imagine three different economists answering the question — What will be the price of fuel tomorrow? All three will write down 1 step of their thinking and then go on to the next step. If any economist realizes they’re wrong at any point, they leave.
 | Complex problem-solving, decision making.

 | Graph prompting
 | Structure prompts in a way that models relationships between concepts using graphs.
 | Map the relationship between machine learning, deep learning, and neural networks.
 | Concept mapping, relationship analysis.

 | Meta prompting
 | Create prompts that design or generate other prompts for different tasks.
 | Write a prompt that helps generate a summary of any news article.
 | Prompt generation, Task automation.

 | Generate Knowledge
 | Prompt the model to generate necessary knowledge before completing a task.
 | Explain the history of blockchain, then describe how it can be used in supply chain management.
 | Generating detailed explanations, knowledge retrieval.

 | Prompt Chaining
 | Use the output of one prompt as the input for the next to handle complex tasks.
 | Step 1: Summarize this text. Step 2: Extract keywords from the summary generated in step 1.
 | Task automation, multi-step processes.

 | Active Prompt
 | Prompts evolve during interaction to reach optimal outputs through feedback.
 | Ask: What are the latest trends in AI? Refine: Summarize the trends based on the last 3 years.
 | Interactive dialogue, evolving task refinement.

 | ReAct
 | Combine reasoning and action, where the model reasons through a task and takes action, refining its approach.
 | Plan how to build a website, then create the layout based on your reasoning.
 | Task planning, real-time decision making.

 | Reflexion
 | Instruct the model to reflect on past outputs and refine future responses based on previous iterations.
 | Reflect on the mistakes made in the previous explanation and improve the next one.
 | Learning from errors, iterative improvement.

## Advanced prompt engineering techniquesAdvanced prompt engineering techniques

Some prompt engineering techniques integrate LLMs with other technologies, additional LLMs, or intricate workflows to address more complex problems. This section highlights a few advanced methods, but it is not an exhaustive list; it is an introduction to the many possibilities in the field.

### RAG prompt engineeringRAG prompt engineering

Retrieval Augmented Generation (RAG) closes gaps in the LLM’s training data without re-training the entire model. For example, let’s say you want to develop a chatbot that answers questions about your organization’s HR policies. The LLM is generic and has obviously not been trained on your organization’s HR policy documents.

In this case, you can:

- 

Take the user’s prompt.

- 

Identify keywords and do a smart search on your knowledge source.

- 

Pull out relevant documents.

- 

Engineer a new prompt enhanced with relevant retrieved information for additional context. Pass the new prompt to the LLM.

You typically need smart search technologies like Amazon Kendra to set up RAG workflows in your organization.

RAG workflow (Source)

### Automatic prompt engineeringAutomatic prompt engineering

In automatic prompt engineering, one LLM generates the prompts, and another LLM (or human) evaluates the prompts before passing them on to a third LLM as input. The prompt-generating LLM is given an example user input/output data set to guide the prompt-generation process.

The workflow typically consists of 2 steps:

- 

The prompt-generating LLM generates a set of candidate prompts.

- 

A prompt evaluation function (another LLM or human in the loop) evaluates each candidate prompt and returns the prompt with the highest score.

The final prompt is used downstream with a third LLM or the existing ones.

### Program-aided language modelsProgram-aided language models

Program-Aided Language Models (PALM) combine LLMs with external programming logic or tools to enhance their performance on more complex, reasoning-based tasks. It integrates language models with structured code execution so the model can handle tasks that require precise calculations, algorithmic thinking, or detailed data manipulation.

Initially, the LLM is given input explaining how to convert the input to code. Then, the user is asked to do the same for a new problem and run the code. In the below figure, the LLM interacts with the Python interpreter to solve mathematical problems.

PALM in action (Source)

## ConclusionConclusion

Prompt engineering is the process of guiding LLMs to generate optimal outputs. With numerous strategies available, selecting the best approach depends on your use case, the specific LLM, and the tools or technologies at hand. As LLMs evolve, prompt engineering continues to adapt, with new techniques emerging regularly. Staying updated on the latest methods is crucial for selecting the most effective strategy for your needs.

## FAQ

Why does an LLM need prompts?

LLMs need prompts to understand what task or information the user seeks. Prompts define the input, guiding the model to produce relevant, coherent responses based on the user’s requirements, ensuring the interaction stays focused and purposeful.

What is role prompting in an LLM?

Role prompting involves instructing an LLM to adopt a specific persona or role, such as a teacher or a developer, to guide the response style. This helps in generating outputs tailored to that role, improving the context and relevance of answers.

What are the 4 S’s of prompt engineering?

The 4 S’s of prompt engineering are Specificity (precise instructions), Simplicity (concise prompts), Structure (logical format), and Strategy (choosing the best method for the task). These principles ensure optimal LLM outputs across various applications.

Is prompt engineering a skill?

Yes, prompt engineering is a skill that involves crafting effective prompts to guide LLMs toward desired outcomes. It requires understanding the model’s behavior, structuring inputs, and iterating on prompts to improve accuracy and relevance.

Is prompt engineering difficult?

Prompt engineering can be challenging for beginners, as it requires understanding how LLMs interpret instructions and generate responses. However, with practice and learning different techniques, creating effective prompts tailored to specific tasks becomes easier.

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

What is a context window in AI? Understanding its importance in LLMs

Explore the importance of context windows in AI and LLMs. Learn how context window size affects model performance, tokenization and natural language processing.

November 28, 2024
12 mins to read

Sign in to save this post
Sign In
