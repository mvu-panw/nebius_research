# Build a multi-agent AI customer support system with the Google ADK, A2A and Nebius AI Studio

Source: https://nebius.com/blog/posts/build-multi-agent-ai-customer-support-system

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

# IntroductionIntroduction

Ever reached out to an online store with a simple question, like tracking a delayed order or asking about a refund, only to be left waiting for hours or met with a generic response?

What if there were an assistant that understands urgency, knows company-specific details and can process and respond to customer queries accurately while operating 24/7?

Sounds innovative, right? That’s exactly what AI agents bring to customer support. There’s no doubt that artificial intelligence is transforming various industries, and AI agents powered by large foundation models are at the core of this transformation.

In this article, you’ll learn how to build a multi-agent system that understands customer queries and intelligently routes them for resolution. We’ll do this by using an open-source Agent Development Kit (ADK) and the Agent-to-Agent (A2A) protocol. By the end of this article, you will have built a multi-agent customer support system with a frontend UI for a demo online store, powered by top open-source models from Nebius AI Studio.

Here is a sneak peek of the final result you’ll build in this tutorial — you can also check the source code here:

Streamlit Demo UI. Click to expand

# What is ADK?What is ADK?

AI agents have gained significant prominence recently, as shown by the increasing number of frameworks built to support their development. Among these, one is an ADK, or Agent Development Kit.

ADK is a modular framework developed by Google for building production-ready AI agents. It is designed to make agent development feel more like traditional software engineering. This makes it easier to scale, test and integrate agents into real-world systems.

### Key features of ADKKey features of ADK

- 

Flexible and modular architecture: ADK is designed to support a variety of agentic workflows, whether you’re building a simple task-based agent or a complex multi-agent system. Its modular structure makes it easy to plug in new capabilities as needed.

- 

Model agnostic: You can use ADK with any large language model. While it works seamlessly with Gemini models, it also supports other open-source and proprietary models.

- 

Deployment agnostic: ADK gives you the freedom to deploy agents locally, on the cloud or within your existing infrastructure, depending on your use case and scalability needs.

- 

Framework compatible: The toolkit integrates easily with other agent development tools and frameworks, allowing you to extend functionality without being locked into a single ecosystem.

- 

Developer-friendly: ADK follows familiar software engineering principles. It provides reusable components, clean abstractions and a structure that helps developers quickly build, test and maintain AI agents.

# What is the A2A protocol?What is the A2A protocol?

The Agent-to-Agent (A2A) Protocol is an open standard, which enables AI agents to communicate, collaborate and delegate tasks to each other. It gives agents a shared language for working together regardless of how they were built or which framework they use.

A2A simplifies the creation of systems where multiple agents can solve complex problems as a team. Each agent publishes a public description of its capabilities, called an Agent Card, and follows standard patterns for sending messages, handling tasks and streaming updates. This makes it easy for developers to connect agents like LEGO blocks and focus on what each agent does rather than how they connect.

### A2A sample use caseA2A sample use case

To understand how A2A simplifies communication between different agents, let’s take a sample use case where a company is automating its hiring process by using AI agents. Behind the scenes, several tasks are handled by different remote agents, such as:

- An HR agent who collects documents and manages paperwork.

- An IT agent that sets up accounts and assigns equipment to the employee.

- A Finance agent who registers the new hire in the payroll system.

With A2A, a host agent or onboarding coordinator agent starts the process and delegates tasks to each specialized remote agent. These agents operate independently, complete their responsibilities and report back with updates.

Since they all follow the same protocol, each agent knows what to do and how to communicate, resulting in an automated onboarding experience for both the employee and the company.

# Project overview: Customer query routing and resolution agents with the ADK and A2A protocolProject overview: Customer query routing and resolution agents with the ADK and A2A protocol

This project builds a multi-agent customer query routing and resolution system. In simple terms, it is a system that receives a customer message, understands the intent or emotion behind it and routes it to the right agent for resolution. That could mean answering a question, providing support or escalating the issue when necessary.

Here’s how the system works, step by step:

- Takes a customer query (a text message) as input.

- Calls three separate remote agents:

- Intake agent: Analyzes the sentiment of the user’s message by classifying it as positive, neutral or negative.

- Resolution agent: Answers the query by searching a predefined knowledge base by using the Retrieval-Augmented Generation (RAG) technique.

- Escalation agent: Handles angry or frustrated users by simulating an escalation to a human support team.

- Uses a coordinator agent as a host agent to orchestrate the entire workflow. The coordinator agent first calls the intake agent to assess a customer’s tone, then routes the original query to the appropriate agent. It routes to the resolution agent when the tone is positive and to the escalation agent when the tone is negative.

To make things more concrete, here’s a high-level visual representation of the entire multi-agent workflow.

Architecture of the multi-agent customer query routing and resolution system. Click to expand

This entire process is made possible by the A2A protocol, which provides a standardized framework for agent collaboration. It allows agents to discover each other’s capabilities by publishing an Agent Card, a metadata file that describes their skills, at a standard /.well-known/agent-card.json endpoint.

A2A defines a consistent communication format by using a strict JSON-RPC protocol. This ensures that messages sent by one agent are always understood by another, no matter how the agent was built.

For example, when a user types, “I’m very unhappy; your product is broken, ‘ here’s how A2A facilitates the collaboration:

- Discovery: The coordinator agent checks the intake agent’s AgentCard at its /.well-known/agent-card.json endpoint to confirm it has the “classify sentiment” skill.

- Communication: It sends the user’s message in a standardized JSON-RPC request. The intake agent processes it and returns a “negative” sentiment response in the same format.

- Collaboration: Now, understanding the user is angry, the coordinator agent checks the escalation agent’s capabilities, sends the original message and completes the resolution through agent-to-agent coordination.

# Model integrationModel integration

Our multi-agent system uses Nebius-hosted open-source text and embedding models, each chosen for its specific role:

- Intake and Escalation Agents — Meta-Llama-3.1-8B-Instruct for fast, accurate sentiment analysis and escalation handling, optimized for short, instruction-based prompts.

- Resolution Agent — Qwen3-30B-A3B for reliable function-calling and high-recall answers when querying the knowledge base in Retrieval-Augmented Generation (RAG) pipelines.

- Embedding Model — Qwen3-Embedding-8B delivers high-quality vector embeddings for efficient and relevant document retrieval, powering the resolution agent’s RAG capabilities.

By pairing the right model with each agent’s task, we achieve higher accuracy, faster response times and cost-efficient AI-powered support automation.

# PrerequisitesPrerequisites

To follow along with this tutorial, make sure you have the following in place:

### 1. Nebius AI Studio API access1. Nebius AI Studio API access

Sign up to AI Studio, create an account and generate your API key.

You will receive free credits that allow you to run large language models (LLMs) for this project.

### 2. Clone the project repository2. Clone the project repository

This tutorial is based on code available in a GitHub repository. Start by cloning the project and navigating to the correct directory:

git clone https://github.com/Astrodevil/ADK-Agent-Examples.git
cd ADK-Agent-Examples/a2a_customer_routing

You’ll be working with Python files like agent.py and tools.py, so we recommend opening the project in your favorite code editor (such as VS Code or PyCharm).

### 3. Install required dependencies3. Install required dependencies

Make sure you have Python 3.10+ installed. Then install all dependencies by using:

pip install -r requirements.txt

### 4. Set up environment variables4. Set up environment variables

Copy the example environment file and add your AI Studio API key:

cp .env.example .env

Then open the newly created .env file and replace the placeholder with your actual API key.

# Step 1: Setting up tools and the knowledge baseStep 1: Setting up tools and the knowledge base

Before diving into the code, let’s briefly understand the structure of the project.

After cloning the repository, your project should look like this:

.
├── a2a_customer_routing/
│ ├── knowledge_base/
│ │ └── swiftcart_kb.json # A JSON file with Q&A for the Resolution Agent
│ │
│ ├── multi_agent/ 
│ │ ├── __init__.py 
│ │ ├── agent.py # Defines the agents using ADK and A2A servers
│ │ ├── run_agents.py # Main entry point to start all agent servers 
│ │ └── tools.py # Defines the tools agents can use
│ │
│ └── streamlit_app.py # The Streamlit user interface
│
├── README.md 
└── requirements.txt 

This layout will give you a sense of how each module works as we go forward.

💡 Heads up: For brevity, only the essential code snippets are included in this tutorial. To explore the full implementation, check out the complete code on GitHub.

Now, let’s start by setting up tools for the agents.

AI agents rely on tools to perform tasks, retrieve information and interact with their environment. We define these tools in a2a_customer_routing/multi_agent/tools.py. This file includes three main capabilities:

- Knowledge retrieval

- Sentiment classification

- Escalation

### Knowledge base initialization and RAG pipelineKnowledge base initialization and RAG pipeline

At the core of the query resolution system is a class called KB. It loads a JSON file of FAQs, splits them into chunks, embeds them by using AI Studio and builds a vector index — creating a simple Retrieval-Augmented Generation (RAG) pipeline.

# Load and parse FAQ JSON into Document objects
kb_path = Path(__file__).parent.parent / "knowledge_base" / "swiftcart_kb.json"
data = json.loads(kb_path.read_text())
docs = [ Document(text=f"Q: {faq['question']}\nA: {faq['answer']}") 
 for faqs in data.values() for faq in faqs ]

# Split text into nodes suitable for semantic search
nodes = SentenceSplitter(chunk_size=512, chunk_overlap=20) \
 .get_nodes_from_documents(docs)

# Build vector index with AI Studio embeddings
self.index = VectorStoreIndex(
 nodes,
 embed_model=NebiusEmbedding(
 model_name="Qwen/Qwen3-Embedding-8B",
 api_key=os.getenv("NEBIUS_API_KEY")
 )
)

# Wrap the index in a query engine backed by Meta's Llama 3.1 8B Instruct model
self.query_engine = self.index.as_query_engine(
 llm=NebiusLLM(
 model="meta-llama/Meta-Llama-3.1-8B-Instruct",
 api_key=os.getenv("NEBIUS_API_KEY")
 ),
 response_mode="tree_summarize",
 similarity_top_k=3
)

Here’s what happens under the hood:

To make the knowledge base searchable for customer queries, the system first uses a SentenceSplitter to break each FAQ entry into overlapping 512-token chunks.

Each chunk is then embedded into a high-dimensional vector by using the Qwen3-Embedding-8B model from AI Studio.

These vectors are stored in VectorStoreIndex, enabling efficient similarity search. When a user submits a query, the system retrieves the top-K most relevant chunks from the index.

Finally, the retrieved chunks are passed into Meta’s Llama‑3.1‑8B‑Instruct model, which generates a concise, context-aware answer grounded in the source material.

The JSON file used here is a mock dataset for demonstration purposes. In real-world deployments, your knowledge base could be populated from:

- Internal helpdesk systems (e.g., Zendesk, Freshdesk)

- CMS platforms (e.g., Notion, Confluence)

- API-based knowledge repositories

- Live documents and manuals

### Query resolution toolQuery resolution tool

The resolve_query_fn(question: str) function sends the user’s question to the RAG engine. If the system finds relevant content and the LLM generates a meaningful answer, the response is prefixed with KB_ANSWER. Otherwise, it falls back to NO_KB_INFO.

This prevents the system from making up answers when the knowledge base lacks relevant information.

def resolve_query_fn(question: str) -> str:
 resp = kb.query_engine.query(question.strip())
 if resp.source_nodes and resp.response.strip():
 return f"KB_ANSWER: {resp.response.strip()}"
 return "NO_KB_INFO: No information found in knowledge base for this question"

### Sentiment classification toolSentiment classification tool

To classify a user’s message, we use the classify_fn(message: str) function.

It uses a straightforward prompt, along with the Meta-Llama-3.1-8B-Instruct model (via AI Studio), to classify the sentiment as positive, neutral or negative.

def classify_fn(message: str) -> str:
 prompt = (
 "Analyze the sentiment of the following user message. "
 "Classify it as one of positive, neutral or negative. "
 "Return only the single word.\n\n"
 f'User Message: "{message.strip()}"\n'
 "Classification:"
 )
 resp = completion(
 model="nebius/meta-llama/Meta-Llama-3.1-8B-Instruct",
 messages=[{"role": "user", "content": prompt}],
 api_key=os.getenv("NEBIUS_API_KEY"),
 max_tokens=5,
 temperature=0.0
 )
 sentiment = resp.choices[0].message.content.strip().lower()
 return sentiment if sentiment in ("positive", "neutral", "negative") else "neutral"

### Escalation toolEscalation tool

When a user sends a frustrated or negative message, the system uses the escalate_fn() tool to simulate escalating the case to human support.

This function logs the event and returns a user-friendly response.

In a real-world setup, it could trigger workflows like creating support tickets or notifying your team via Slack or email.

def escalate_fn(message: str) -> str:
 logger.info(f"[ESCALATION] Forwarding to human support: {message.strip()}")
 return "Your message has been escalated to human support. We will contact you shortly."

# Step 2: Creating the remote agents by using ADKStep 2: Creating the remote agents by using ADK

Now that our agent capabilities are defined as tools, we can create the agents themselves in a2a_customer_routing/multi_agent/agent.py. This is done by using the ADK’s LlmAgent class. It allows us to instantiate an agent by declaratively providing four key components: a name, an LLM model, a set of tools and a clear instruction prompt that governs its behavior. We will define the:

- Intake Agent: This agent receives incoming user messages and classifies the sentiment by using the classify_fn tool.

- Resolution Agent: This agent queries the knowledge base by using the resolve_query_fn tool and ensures that it only returns meaningful answers.

- Escalation Agent: Handles cases that require human intervention. It uses the escalate_fn tool to simulate a handoff, returning a polite response to the user.

These agents need LLMs to function; therefore, we will use LiteLLM as an abstraction to connect with LLMs hosted on AI Studio. The agents are powered by:

- Meta-Llama-3.1‑8B-Instruct, for intake and escalation agents.

- Qwen3‑30B‑A3B, a more powerful 30B model for the resolution agent.

# In multi_agent/agent.py
# For the full code, see the file on GitHub.

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .tools import resolve_query_fn, classify_fn, escalate_fn

def create_llm_model(model_name: str):
 """Factory function to create LLM models with consistent configuration."""
 api_key = os.getenv("NEBIUS_API_KEY")
 return LiteLlm(model=model_name, api_key=api_key, temperature=0.1)
 
llama_8b = create_llm_model("nebius/meta-llama/Meta-Llama-3.1-8B-Instruct")
qwen = create_llm_model("nebius/Qwen/Qwen3-30B-A3B")

# Sentiment Classifier
intake_agent = LlmAgent(
 name="intake_agent",
 model=llama_8b,
 instruction="Use the classify_fn tool. Return ONLY the classification result...",
 tools=[classify_fn]
)

# Answers from Knowledge Base
resolution_agent = LlmAgent(
 name="resolution_agent",
 model=qwen,
 instruction="Use resolve_query_fn to answer the user's question from the knowledge base...",
 tools=[resolve_query_fn]
)

# Human Handoff
escalation_agent = LlmAgent(
 name="escalation_agent",
 model=llama_8b,
 instruction="Use escalate_fn to forward the user's message to human support...",
 tools=[escalate_fn]
)

# Step 3: Enabling communication with the A2A server wrapperStep 3: Enabling communication with the A2A server wrapper

To expose our remote agents over the network, we need to wrap them in an A2A server. ADK provides an official A2aAgentExecutor that seamlessly bridges the A2A protocol with the ADK runtime.

This integration significantly simplifies our server setup. We just need to create a function that takes our ADK agent and an Agent Card, wires them up by using A2aAgentExecutor and wraps them in A2AStarletteApplication from the A2A SDK.

# In multi_agent/agent.py

from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor, A2aAgentExecutorConfig
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler

def create_agent_a2a_server(agent: LlmAgent, agent_card: AgentCard):
 # The ADK Runner handles session state and agent execution
 runner = Runner(
 app_name=agent.name, agent=agent, artifact_service=InMemoryArtifactService(),
 session_service=InMemorySessionService(), memory_service=InMemoryMemoryService()
 )
 
 # Use the official A2A Agent Executor from the ADK
 config = A2aAgentExecutorConfig()
 executor = A2aAgentExecutor(runner=runner, config=config)
 
 # Standard A2A request handler
 request_handler = DefaultRequestHandler(
 agent_executor=executor, task_store=InMemoryTaskStore()
 )
 
 # Return the final, runnable Starlette application
 return A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)

# Step 4:  Implementing the Coordinator Agent and its A2A client toolStep 4:  Implementing the Coordinator Agent and its A2A client tool

# In multi_agent/agent.py

from a2a.client import ClientConfig, ClientFactory, create_text_message_object
from a2a.types import AgentCard, Task
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

class A2AToolClient:
 async def create_task(self, agent_url: str, message: str) -> str:
 async with httpx.AsyncClient(...) as httpx_client:
 # 1. A2A discovery: fetch agent_card
 agent_card_response = await httpx_client.get(f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}")
 agent_card = AgentCard(**agent_card_response.json())

 # 2. Use the official client factory
 factory = ClientFactory(ClientConfig(httpx_client=httpx_client))
 client = factory.create(agent_card)
 
 # 3. Create a standard message object and send
 message_obj = create_text_message_object(content=message)
 
 # 4. Process the response stream for the final text artifact
 async for response in client.send_message(message_obj):
 if isinstance(response, tuple) and len(response) > 0:
 task: Task = response[0]
 if task.artifacts:
 try:
 text_response = task.artifacts[0].parts[0].root.text
 if text_response:
 return text_response.strip()
 except (AttributeError, IndexError):
 pass # Ignore intermediate tasks
 return "Agent did not return a valid response."

# Instantiate the client to be used as a tool
coordinator_a2a_client = A2AToolClient()

# Define the Coordinator Agent
def create_coordinator_agent_with_registered_agents():
 return LlmAgent(
 name="support_coordinator",
 # The prompt is updated to be more explicit for better reliability
 instruction="""...
3. **Finalize and Respond:** The tool used in the previous step will return the final answer. Your final job is to output that exact text as your own final answer...
""",
 tools=[coordinator_a2a_client.create_task]
 )

# Step 5: System orchestration and executionStep 5: System orchestration and execution

The run_agents.py script serves as the main entry point for running the entire multi-agent system. It handles the orchestration and startup sequence, launching each agent as an independent background Uvicorn server by using Python’s threading and asyncio.

### Key components:Key components:

- run_agent_in_background(): Launches each agent server in its own dedicated thread. This enables all agents to run concurrently without blocking each other.

- wait_for_agents(): Polls each agent’s /.well-known/agent-card.json endpoint until it receives a successful response. This acts as a health check, guaranteeing that an agent is fully operational before the system proceeds.

- start_all_agents(): Orchestrates the entire startup sequence in the correct order:

- Starts the three remote “specialist” agents (Intake, Resolution and Escalation), each bound to a unique local port (10020–10022).

- Waits for all three specialist agents to pass their health checks, ensuring they are ready to receive requests.

- Instantiates the Coordinator Agent. Only after its dependencies are confirmed to be live is the coordinator created.

- Starts the Coordinator Agent on port 10023 and confirms that it is also live. At this point, the entire system is ready.

# In multi_agent/run_agents.py

from . import agent as agent_module
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

def start_all_agents():
 """Start all support agents and the coordinator in the correct order."""
 
 # 1. Define the specialist agents to start first
 support_agents_to_start = {
 "Intake": (agent_module.create_intake_agent_server, 10020),
 "Resolution": (agent_module.create_resolution_agent_server, 10021),
 "Escalation": (agent_module.create_escalation_agent_server, 10022),
 }

 # Start each support agent in a background thread
 threads = {
 name: run_agent_in_background(create_fn, port, name)
 for name, (create_fn, port) in support_agents_to_start.items()
 }

 # 2. Wait until all specialist agents are healthy
 support_agent_urls = [f"http://127.0.0.1:{port}" for _, port in support_agents_to_start.values()]
 wait_for_agents(support_agent_urls)

 # 3. Create the Coordinator Agent instance
 agent_module.coordinator_agent = agent_module.create_coordinator_agent_with_registered_agents()
 
 # 4. Start the Coordinator Agent in a background thread
 threads["Coordinator"] = run_agent_in_background(
 agent_module.create_coordinator_agent_server, 10023, "Coordinator"
 )

 # Confirm the coordinator is live before finishing
 wait_for_agents(["http://127.0.0.1:10023"])

 logger.info("\n✅ All A2A agents are running and orchestrated!")

To execute the system, run the script as a module from the project root.

python -m a2a_customer_routing.multi_agent.run_agents

The agent server will start:

Click to expand

# Step 6: Client-side interactionStep 6: Client-side interaction

With the multi-agent backend running, we need a user-friendly way to interact with it. To achieve this, we will use Streamlit to build a chat interface that communicates directly with our Coordinator Agent by using the A2A protocol.

A key technical challenge is that Streamlit is a synchronous framework, while the modern a2a-sdk client is asynchronous (async/await). To integrate them safely, our UI code uses a robust pattern that runs the asynchronous A2A communication in a separate background thread. This prevents event loop conflicts and ensures that the UI remains responsive.

The core logic is split into two functions:

- An async function, query_coordinator_async, which uses the official ClientFactory from the a2a-sdk to handle the A2A communication. It discovers the agent, creates a client, sends the message and processes the stream of responses to find the final text artifact.

- A synchronous wrapper, query_coordinator, which is called by the main Streamlit components. This function uses a helper to manage the background thread, making the async call safe to run from the synchronous UI code.

# In streamlit_app.py

import asyncio
import threading
from a2a.client import ClientFactory, create_text_message_object

# Helper to run async code from a sync environment like Streamlit
def run_async_in_thread(coro):
 # ... (implementation that runs the coroutine in a new thread) ...
 return result

# The async function that performs the actual A2A call
async def query_coordinator_async(message: str) -> str:
 async with httpx.AsyncClient(...) as httpx_client:
 # It uses the same ClientFactory pattern as the agent tool
 # to fetch the agent card, create a client and send a message.
 # ... (full implementation is in the GitHub repo) ...
 async for response in client.send_message(message_obj):
 # Parses the stream of task updates for the final text artifact
 # ...
 return final_response

# The wrapper function called by the Streamlit UI
def query_coordinator(message: str) -> str:
 return run_async_in_thread(query_coordinator_async(message))

# --- Streamlit UI logic ---
if prompt := st.chat_input("Ask me anything..."):
 # ...
 with st.spinner("Thinking..."):
 response = query_coordinator(prompt)
 st.markdown(response)
 # ...

Launch the UI in a separate terminal:

Click to expand

# Real-world use casesReal-world use cases

While our demo focuses on a powerful multi-agent customer support system, the same architecture can power a variety of additional scenarios:

- Customer support with escalation fallback — Automatically resolve common queries while routing complex or high-priority issues to human agents.

- Automated onboarding workflows — Guide new customers or employees through setup, collecting data and answering questions in real time.

- Internal helpdesk automation — Handle IT, HR and finance requests without manual triage.

- API-triggered agent orchestration — Coordinate multiple backend services (e.g., order tracking, refund processing, account updates) through AI agents.

- Multi-language support bots — Detect language and sentiment, then route queries to region-specific agents or translators.

# ConclusionConclusion

The multi-agent customer query routing and resolution system demonstrates how ADK and the A2A protocol serve as complementary technologies for building AI agents. The ADK provides a high‑level framework for creating agents with complex reasoning abilities, while A2A enables those agents to communicate and collaborate.

Clone the repo, grab your Nebius AI Studio API key and run it locally in minutes.

Try AI Studio: Deploy open-source models like Llama 3 and Qwen, with blazing-fast inference and zero-retention infrastructure.

Throughout this tutorial, we have engineered a complete multi-agent system, showcasing the following:

- We utilized ADK to create remote agents by providing instruction prompts and tools.

- We used AI Studio to access powerful LLMs for different agents, choosing a smaller model for the Intake Agent and a more powerful one for the Resolution Agent, thereby optimizing both performance and cost.

- We employed the A2A protocol to expose our agents over a standardized interface, by using the A2aAgentExecutor ADK to bridge the A2A server and the ADK runtime.

- We built a Coordinator Agent that orchestrates the workflow, routing tasks among agents based on sentiment and query type.

This project serves as a solid base for developing advanced agentic systems. By combining a model provider like AI Studio, a robust framework like ADK and a standard communication layer like the A2A protocol, you can build real‑world AI solutions.

## Explore AI Studio, ADK and A2A

AI Studio docs​
A2A Quickstart notebook​
A2A GitHub repo​
ADK Agent examples repo​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- 

Introduction

- 

What is ADK?

- Key features of ADK

- 

What is the A2A protocol?

- A2A sample use case

- 

Project overview: Customer query routing and resolution agents with the ADK and A2A protocol

- 

Model integration

- 

Prerequisites

- 1. Nebius AI Studio API access

- 2. Clone the project repository

- 3. Install required dependencies

- 4. Set up environment variables

- 

Step 1: Setting up tools and the knowledge base

- Knowledge base initialization and RAG pipeline

- Query resolution tool

- Sentiment classification tool

- Escalation tool

- 

Step 2: Creating the remote agents by using ADK

- 

Step 3: Enabling communication with the A2A server wrapper

- 

Step 4:  Implementing the Coordinator Agent and its A2A client tool

- 

Step 5: System orchestration and execution

- 

Step 6: Client-side interaction

- 

Real-world use cases

- 

Conclusion

## See also

### 

Setting up a RAG-powered content generation with Nebius AI Studio and Qdrant

Learn how to build a smart, scalable content generator by using Nebius AI’s Llama 3.3-70B and Qdrant’s vector search. This RAG-based system lets you upload brand-specific documents and get custom social posts, article drafts and more, rooted in your actual company data.

September 23, 2025
11 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

How we streamlined HR operations with an AI assistant (and why you should too)

Repetitive employee queries can overwhelm HR departments and reduce time for strategic tasks. At Nebius, we implemented an AI Assistant powered by Nebius AI Studio that automates over 150 monthly queries. In this article, we explore how NLP and RAG help Studio drive such process efficiency.

February 12, 2025
13 mins to read

Sign in to save this post
Sign In
