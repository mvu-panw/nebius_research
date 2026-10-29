# How to run Meta Llama 3.1 405B with Nebius AI Studio API

Source: https://nebius.com/blog/posts/run-meta-llama-405b-in-ai-studio

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

Top open-source models usually require major compute resources to operate. As a result, integrating an LLM like Llama 3.1 405B into an app will have several pain points.

You may also encounter a steep learning curve in understanding how to operate LLMs and optimize performance.

Nebius AI Studio allows developers to use top open-source models without facing these difficulties. The platform provides an API to run such models. With it, you get the following benefits:

- 

Integration: The platform offers APIs and tools that make integrating AI capabilities into existing applications and business use cases easier.

- 

Accessibility: Studio provides a user-friendly playground where you can test various models. This lowers the barrier to entry for using advanced AI models and enables developers with varying levels of expertise to access powerful models.

- 

Performance: It also helps you do the heavy lifting to optimize model performance. These include features like quantization, flash attention, and continuous batching.

From this guide, you’ll learn how to integrate Llama 3.1 405B into your applications using an API.

### PrerequisitesPrerequisites

To follow along with this blog post, you should have a basic understanding of large language models and their real-world use cases. Before getting started, please ensure you have completed the following steps:

#### 1. Sign up for Nebius AI Studio1. Sign up for Nebius AI Studio

- Visit Studio to create an account.

#### 2. Get access to API2. Get access to API

- In Studio, click on your profile picture in the top right corner.

- Select API Keys from the dropdown menu.

- Click Create API Key to generate your key to access the API.

#### 3. Set Up Your API Key3. Set Up Your API Key

It’s recommended to store your API key in an environment variable for security reasons. Here’s how to do that:

On macOS/Linux:

Open your terminal and run the following command:

export NEBIUS_API_KEY="your_nebius_api_key"

On Windows:

Open your Command Prompt and run the following command:

set NEBIUS_API_KEY="your_nebius_api_key"

Make sure to replace "your_nebius_api_key" with your actual API key.

#### 4. Install the OpenAI SDK4. Install the OpenAI SDK

Depending on the programming language you’re using, install the appropriate SDK to interact with Nebius AI’s API.

For Python:

Open your terminal and run:

pip install openai

For JavaScript:

If you’re using Node.js, run the following command in your terminal:

npm install openai

### Understanding Llama 3.1 405BUnderstanding Llama 3.1 405B

With the Llama 3.1 model, Meta has set a new standard in using large-scale models for language-based AI applications. Llama 3.1 405B is designed to handle large-scale natural language processing (NLP) tasks. As the name suggests, this model comes with 405 billion parameters, which outscales previous versions in both complexity and performance.

#### Key featuresKey features

- 

Large parameter count: With 405 billion parameters, Llama 3.1 ranks among the largest models for NLP.

- 

Pretraining on diverse data: Trained on a wide range of multilingual data, Llama 3.1 has a strong ability to understand different languages and retain knowledge.

- 

Scalability: Although large, Llama 3.1 is optimized for efficiency on distributed systems. This makes it suitable for applications that demand computational power.

- 

Open source: Developers can freely access and build on the model.

### API overviewAPI overview

The Nebius AI Studio API allows you to interact with various advanced models via an OpenAI-compatible interface. This API simplifies the process of building AI-powered applications by offering flexibility across different development environments. If you’re familiar with OpenAI’s API, you can use Studio with minimal changes to your code.

#### API access methodsAPI access methods

- 

Python SDK: Using the Open AI package for an easy setup, you can efficiently interact with the service. This method allows Python developers to quickly make API requests and integrate them into Python-based applications.

- 

cURL: Ideal for users who prefer command-line tools, the service supports cURL for making API calls. This method is perfect for quick testing, automation scripts, or when working in environments that don’t require full-fledged SDKs.

- 

JavaScript SDK: For web-based developments, JavaScript SDK provides a straightforward way to integrate available models directly into your applications.

#### Token limitsToken limits

Studio applies rate limits based on the model you’re using. Essentially, this means that it restricts the units of text that can be processed by the API within a given time frame, depending on the model. Here’s the breakdown:

- 

Meta-Llama-3.1-405B-Instruct: This specific model allows up to 100,000 tokens to be processed per minute.

- 

All other models: The limit is higher for the rest of the available models; you get up to 200,000 tokens per minute.

These limits prevent system overload and ensure resources are efficiently distributed. Despite these optimizations, models on Nebius AI Studio maintain 99% of the original quality. This means that you get identical output with improved performance.

### How to make API calls to LLMHow to make API calls to LLM

You can run an LLM with the Studio API in four simple steps. Here’s how it works:

- 

Initialise the API Client: This is where you set things up. You load the required library (in this case, Python’s OpenAI SDK) and input your API key. This key acts as a password, giving you access to Nebius AI’s models. Essentially, you’re telling your program, “This is the service I want to use, and here’s the access key.”

- 

Create a request: In this step, you decide what you want the model to do. You specify the model (like “Meta-Llama-3.1”) and provide input text or prompts. You can also customise parameters like max_tokens (how long the response should be) or temperature (how creative or random the model should be in its response).

- 

Send the API request: Now you’re ready to send the request to Nebius AI. This is done by making a POST request to the API endpoint (e.g., /v1/chat/completions), where you include the model, the input message, and your API key. It’s like sending a question or task to the model.

- 

Receive and process the response: After the request is sent, the API returns a response from the model. This could be an answer to your prompt, a piece of text, or any other completion task. You can then use this response in your application, whether it’s part of a chatbot, a content generator, or a research tool.

We will see how these steps work in practice by exploring the various API access methods and how they add flexibility to your development lifecycle.

### Accessing API with PythonAccessing API with Python

If you want to integrate Llama 3.1 405B into your data science pipelines, get started with Python to access the API. Here is how:

#### Step 1: Initialise the API clientStep 1: Initialise the API client

This step sets up the connection to Nebius AI’s models. Import the required libraries and pass in your API key using the environment variable.

import os
from openai import OpenAI

# Initialise the API client
client = OpenAI(
　base_url="<https://api.studio.nebius.ai/v1/>",
　api_key=os.environ.get("NEBIUS_API_KEY"),
)

#### Step 2: Create a requestStep 2: Create a request

In this step, you’re specifying which AI model you want to use and what input (prompt) you want to send. In this case, you’re running the Llama 3.1 405B model. You’ll also customise options like temperature to control the creativity of the model’s responses.

# Create the request with your prompt
completion = client.chat.completions.create(
　model="meta-llama/Meta-Llama-3.1-405B-Instruct",
　　messages=[
　　{
　　　"role": "user",
　　　"content": """What is an API?"""
　　}
　],
　temperature=0.6
)

#### Step 3: Send the RequestStep 3: Send the Request

This part is already handled when you call the .create() method on the client. Behind the scenes, this sends a request to the Nebius API and waits for a response.

#### Step 4: Receive and process the responseStep 4: Receive and process the response

Once the model processes your request, it will return a response. You can print this response or use it in your application.

# Print the response from the model
print(completion.to_json())

### Accessing API with JavaScriptAccessing API with JavaScript

The JavaScript SDK is perfect for embedding LLama 3.1 in a real-time web app. Here is how:

#### Step 1: Initialise the API clientStep 1: Initialise the API client

In this step, you set up the API client by importing the OpenAI JavaScript SDK and configuring it with your API key. The baseURL is set to Nebius AI’s endpoint.

// Import the OpenAI SDK
const OpenAI = require('openai');

// Initialise the API client with the API key and base URL
const client = new OpenAI({
　baseURL: '<https://api.studio.nebius.ai/v1/>',
　apiKey: process.env.NEBIUS_API_KEY, // Use your environment variable
});

#### Step 2: Create a requestStep 2: Create a request

Here, you define the task you want to perform, such as specifying the model and providing an input message. You can also set parameters like temperature to control the randomness of the output.

client.chat.completions.create({
　"temperature": 0.6, // Adjusts creativity of the model’s response
　"model": "meta-llama/Meta-Llama-3.1-405B-Instruct", // Model for instruction tasks
　"messages": [
　　{
　　　"role": "user", // The role of the message sender (in this case,the user)
　　　"content": "What is an API?" // The prompt or input message
　　}
　]
})

#### Step 3: Send the API RequestStep 3: Send the API Request

Now, you send the request to Nebius AI’s API, which is handled via the SDK’s chat.completions.create() method. This sends a POST request to Nebius AI’s endpoint, and the API processes your input.

#### Step 4: Receive and process the responseStep 4: Receive and process the response

Once the request is sent, you handle the response by logging it to the console or using it in your application logic.

.then((completion) => console.log(completion)) // Handle the response

### Using API via cURLUsing API via cURL

The cURL command is perfect for quick API testing or integrating API calls into shell-based automation scripts. Here is how:

#### Step 1: Initialise the cURL CommandStep 1: Initialise the cURL Command

Start by constructing your cURL command to interact with the API. You will be making a POST request to the appropriate endpoint. This command points to the API’s chat completions endpoint.

curl '<https://api.studio.nebius.ai/v1/chat/completions>' \

#### Step 2: Set request method and headersStep 2: Set request method and headers

Next, specify the request method and include the necessary headers. This includes specifying that you’re sending JSON data and providing your API key for authorisation.

-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: */*' \
-H 'Authorization: Bearer $NEBIUS_API_KEY' \

#### Step 3: Compose the request dataStep 3: Compose the request data

Prepare the JSON payload containing the model’s parameters, such as the temperature, model name, and input message.

--data-binary ’{"temperature":0.6,"model":"meta-llama/Meta-Llama-3.1-405B-Instruct","messages":[{"role":"user","content":"What is an API?"}]}’

### PerformancePerformance

Nebius AI Studio lets you interact with various open-source models for NLP tasks. These models are optimized for high throughput and scalability. Studio’s optimization of these models offers the following:

- 

Scalability: Optimised models use fewer computational resources, which enables them to run efficiently across diverse hardware environments.

- 

Reduced latency: Models respond faster by reducing the number of computations required; this is beneficial for real-time applications as it improves response time.

- 

Higher throughput: These optimisations allow models to process more input sequences per second; this is particularly beneficial for large-scale tasks.

### Real-world use cases for running Llama 3.1Real-world use cases for running Llama 3.1

Running Llama 3.1 with Studio helps you develop real-world AI applications efficiently. The platform’s ability to handle large-scale language models makes it ideal for NLP tasks that require high performance and scalability. Below are some key use cases:

- 

Large-scale chatbot deployments. The service’s quick response times and ability to handle concurrent requests make it perfect for powering chatbots like customer support, virtual assistants, and conversational agents. With Studio, businesses can deploy chatbots capable of handling large amounts of interaction.

- 

Content generation. Looking to automate content creation? Llama 3.1 can generate human-like text for tasks such as content marketing, blog posts, or social media caption posts. Nebius’ infrastructure allows you to use Llama 3.1 for this use case.

- 

Translation models. Llama 3.1 handles translation tasks accurately; this can be useful for international businesses looking to bridge language barriers in communication or documentation.

### ConclusionConclusion

Llama 3.1 405B shows the latest advancements of open-source models. Thanks to cloud platforms, developers and businesses can easily build with these innovations through an API. Nebius AI Studio is one such platform that provides easy access for developers and businesses to create powerful AI-driven solutions within their applications.

Llama 3.1 is proof that the future of AI is open source, and it only gets better from here. As more advanced open-source models are developed, you can confidently experiment and build upon these models with Studio.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius

Sign up​
Docs​

Nebius team

## See also

### 

Introducing Nebius AI Studio: Achieve fast, flexible inference today

Our new platform not only allows application builders to use generative AI without significant effort but does so at a fraction of the cost. Our goal is to democratize access to cutting-edge AI technologies, enabling businesses of all sizes to innovate and compete in the AI space.

September 30, 2024
4 mins to read

### 

Tips and tricks for performing large model checkpointing

There are various aspects to optimize when training large models. It often lasts weeks and involves managing billions of rows of data, with checkpoints of such models weighing terabytes in some cases. Let’s explore how to handle large model checkpointing.

March 11, 2024
9 mins to read

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

Sign in to save this post
Sign In
