# Building a RAG-powered content generation platform with Nebius AI and Qdrant

Source: https://nebius.com/blog/posts/building-a-rag-powered-content-generation-platform

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

Writer’s block is real, and content teams face this more than anybody else. It is not just hard to write “social media hits” every day, but also difficult to keep up with what’s trending and align it with your company’s messaging. This is where AI can help. While there seems to be an AI SaaS solution for everything, a content generator platform tailored to a company’s specific needs was missing…until now. In this article, you will learn how to build a content generator platform by using Nebius AI Studio and Qdrant. By the end, you will learn how to build one for yourself, and you can also use the platform locally by following the steps in the readme.

# PrerequisitesPrerequisites

To follow the tutorial end-to-end, here’s what you need:

- AI Studio API key — For content generation by using the Llama-3.3-70B-Instruct model and embedding by using the Qwen3-Embedding-8B model.

- Qdrant Cloud API key (you need to login to get your keys) — For vector storage and search.

- Working knowledge of React, Tailwind CSS and React Query for frontend and state management.

- Working knowledge of Node.js to build the backend.

Before we get into building the tool, here’s how it works:

### Feature setFeature set

- AI content generation: Generate social media posts, articles and demo concepts by using the Llama-3.3-70B-Instruct model.

- RAG pipeline: Context-aware content creation with uploaded documents.

- Vector search: Qdrant Cloud integration for semantic document search and context retrieval.

- Dashboard: React-based interface with content generation, data management, analytics and history tracking.

- Analytics and history: Complete generation tracking and performance metrics.

Here’s the workflow:

Click to expand

In the next section, we will see in detail how the application works.

# Understanding how the application worksUnderstanding how the application works

For this tool, we are using Retrieval Augmented Generation (RAG), which combines search and generation to output contextual responses.

When users upload company data or documents from the frontend, it hits the backend API that processes the content. This converts the text into vector embeddings by using the AI Studio API, and store those vectors in Qdrant Cloud which powers the semantic search.

Later, when a user wants content generated, the system queries Qdrant to fetch relevant context based on semantic similarity. That context is then passed to the Llama-3.3-70B-Instruct model by using the AI Studio API, which generates personalized content suggestions based on it.

Here’s a diagram to show how all this ties together:

Click to expand

# Why AI Studio and Qdrant?Why AI Studio and Qdrant?

Before jumping into the code, let’s understand why we choose these tools.

Nebius AI has pretty much everything you want if you’re building for production: crazy-fast throughput (we’re talking up to 10 million tokens per minute) and 400k+ TPM on most models, support for multiple models like DeepSeek, Qwen and Llama, and solid features like fine-tuning support tailored to enterprise use cases. This helps in generating fast and reliable content, without having to worry about infrastructure.

While Qdrant Cloud is a vector database built for semantic search, it helps in retrieving relevant context from the uploaded documents and links, and helps in generating contextually aware content.

# Building the RAG pipelineBuilding the RAG pipeline

For the RAG pipeline to work as expected, you need to upload context documents. These can be a link, or a DOCX, TXT or MD file. Once you do that from the frontend, as shown in the image below, the pipeline starts working and along with Nebius AI Studio, it embeds and generates contextually aware content.

Click to expand

In the next steps, we will see how the raw documents are turned into searchable vectors that help in generating social media posts, articles and demo ideas.

Each step will be illustrated with code examples, but if you want to see the entire code, you can find it on GitHub.

### Step 1: Document processing and chunkingStep 1: Document processing and chunking

To get content suggestions based on your company’s needs and goals, you need to upload relevant documents or links.

In the backend, these documents are broken into manageable chunks.

Here’s how our document service handles this:

// backend/src/services/documentService.js

async processDocuments(documents) {
 const chunks = [];

 for (const doc of documents) {
 const text = await this.extractText(doc);
 const documentChunks = this.chunkText(text, 1000, 200); // 1000 words with 200 overlap

 chunks.push(...documentChunks.map((chunk, index) => ({
 id: `{doc.id}_chunk_{index}`,
 text: chunk,
 metadata: {
 source: doc.fileName || doc.url,
 type: 'document',
 chunkIndex: index
 }
 })));
 }

 return chunks;
}

This creates overlapping chunks to maintain context, while keeping each piece manageable for the embedding model.

### Step 2: Vector embedding generationStep 2: Vector embedding generation

Next, we convert these text chunks into vector embeddings by using Nebius’ Embedding model: Qwen3-Embedding-8B. Vector embeddings are numerical representations of text that capture semantic meaning, allowing our system to understand the relationships between different pieces of content.

// backend/src/services/embeddingService.js

async processDocumentChunks(chunks) {
 const texts = chunks.map(chunk => chunk.text);

 const embeddings = await this.generateEmbeddings(texts);

 return embeddings.map((embedding, index) => ({
 id: chunks[index].id,
 vector: embedding,
 payload: {
 text: chunks[index].text,
 ...chunks[index].metadata,
 timestamp: new Date().toISOString()
 }
 }));
}

### Step 3: Storing vectors in Qdrant CloudStep 3: Storing vectors in Qdrant Cloud

Then, we store these vectors in Qdrant Cloud for fast semantic search with the code below:

// backend/src/services/qdrantService.js

async addPoints(points) {
 const pointsData = points.map(point => ({
 id: point.id,
 vector: point.vector,
 payload: point.payload
 }));

 await this.client.upsert(this.collectionName, {
 points: pointsData
 });

 console.log(`✅ Added ${points.length} points to Qdrant Cloud`);
}

Each vector is stored with its associated metadata (like the original text, source document and timestamp) in what Qdrant calls a “point.” This allows us to not only find similar vectors, but also retrieve the original context when needed for content generation.

# Content generation with context-aware AIContent generation with context-aware AI

To get the most relevant content and demo ideas, the context that we uploaded above is combined with AI Studio’s content generation capabilities.

Here’s how our content generation pipeline works:

### Step 1: Semantic search for relevant contextStep 1: Semantic search for relevant context

When a user requests content generation, we first search for relevant context. This is where the RAG starts working, instead of generating content from scratch, we find the most relevant information from the user’s uploaded documents and company data, to provide context-aware suggestions.

// backend/src/controllers/contentController.js

async generateSuggestions(req, res) {
 const { contentType, goals, customCompanyData } = req.body;

 // Create search query based on content type
 let searchQuery = '';

 switch (contentType) {
 case 'social_media_post':
 searchQuery = goals || 'social media content engagement';
 break;
 case 'article':
 searchQuery = goals || 'article content writing';
 break;
 default:
 searchQuery = goals || 'content generation';

 }

 // Search for relevant documents

 const queryEmbedding = await embeddingService.processQuery(searchQuery);
 const similarResults = await qdrantService.searchSimilar(queryEmbedding, 5, 0.5);

 const contextData = similarResults.map(result => ({
 text: result.payload.text,
 type: result.payload.type,
 source: result.payload.source,
 score: result.score
 }));
}

### Step 2: AI-powered content generationStep 2: AI-powered content generation

Now, we use Nebius’ Llama-3.3-70B-Instruct model to generate content with the retrieved context. This is where semantic search works with AI generation to create personalized content suggestions instead of suggesting generic content.

// backend/src/services/nebiusService.js

async generateContentSuggestions(companyData, contentType, goals, contextData = []) {
 let contextInfo = '';
 
 if (contextData && contextData.length > 0) {
 contextInfo = `\n\nRelevant Context from Uploaded Documents:\n`;

 contextData.forEach((doc, index) => {
 contextInfo += `\${index + 1}. Source: 
 \${doc.source || 'Document'}\n`;

 contextInfo += `   Content: \${doc.text.substring(0, 200)}
 \${doc.text.length > 200 ? '...' : ''}\n\n`;
 });

 }

 const prompt = `Based on the following company information and uploaded documents, suggest 3 ${contentType} ideas:

Company Data: ${JSON.stringify(companyData)}

Company Goals: \${goals}
\${contextInfo}

Please provide structured suggestions with titles, descriptions, and key points.`;

 return await this.generateText(prompt, 'meta-llama/Llama-3.3-70B-Instruct', 1500);

}

# Real-time search and retrievalReal-time search and retrieval

The search functionality is what makes our content contextual. Here’s how the semantic search works:

Vector similarity search

Unlike traditional keyword-based search, which looks for exact word matches, semantic search understands the meaning behind the text. When a user requests content generation, their query is converted into a vector and we find the most semantically similar documents in our database.

Here’s how our Qdrant service handles this:

// backend/src/services/qdrantService.js

async searchSimilar(vector, limit = 5, scoreThreshold = 0.7) {
 const searchResult = await this.client.search(this.collectionName, {
 vector: vector,
 limit: limit,
 score_threshold: scoreThreshold,
 with_payload: true
 });

 return searchResult;
}

The score_threshold parameter only returns results that are relevant (similarity score above 0.7), while the limit parameter keeps the context focused and manageable. This means if someone asks for “social media content about our new product, ‘ the system will find documents about product launches, marketing strategies or customer testimonials, even if those documents don’t contain the exact words ‘social media’ or ‘new product.’

# Putting it all togetherPutting it all together

To break it down, there are two main processes that are working in the background:

- Document upload: When users upload documents, the tool first extracts the text content, then breaks it into manageable chunks with overlapping sections to maintain context. These text chunks are then converted into vector embeddings by using Nebius’ Qwen3-Embedding-8B model and finally stored in Qdrant Cloud for fast semantic search.

- Content generation: When a user requests content generation, it starts by converting their query into a vector embedding, then performs a semantic search in Qdrant Cloud to find the most relevant documents. The retrieved context is then passed to AI Studio, which generates personalized content suggestions based on both the company data and the relevant document context.

The benefit of this architecture is that it scales well. As you add more documents, the system gets smarter about your company’s context, leading to better content suggestions over time.

# Wrapping upWrapping up

We just walked through how to build a content generation platform by using AI Studio and Qdrant Cloud. From uploading documents to generating contextual, company-specific content by using a RAG setup.

With AI Studio handling high-performance generation and Qdrant powering semantic search, you get a solid foundation that’s scalable, efficient and grounded in your actual data, without needing to worry about managing complex infra.

### What’s next?What’s next?

The application is built in a way that it is flexible and scalable. You can take it further by:

- Adding image generation for visual content

- Tracking content performance with basic analytics

- Building team workflows for review and approvals

- Creating industry-specific templates

- Hooking into social media APIs for real-time posting

Want to try this in your own stack? Fork the repo and start building with your company data by using AI Studio today.

## Explore Nebius Token Factory and Qdrant

Token Factory Docs​
Qdrant docs​
RAG best practices​
Vector DBs comparison​

## Explore Nebius AI Cloud

Learn more​
Sign up​
Docs​

Nebius team

Contents

- 

Prerequisites

- Feature set

- 

Understanding how the application works

- 

Why Nebius AI Studio and Qdrant?

- 

Building the RAG pipeline

- Step 1: Document processing and chunking

- Step 2: Vector embedding generation

- 

Putting it all together

- 

Wrapping up

- What’s next?

## See also

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

Agent 101: Launching production-grade agents at scale

To go from prototype to production, AI agents need more than just a good model. In this guide, we break down the four components that matter most: reliable LLMs, orchestration frameworks, evaluation tools, and memory systems. We cover how teams are using Nebius AI Studio with CrewAI, ADK, LangChain, and more to ship scalable, observability-friendly agent workflows, all powered by fast, cost-efficient inference.

July 10, 2025
10 mins to read

### 

Fault-tolerant training: How we build reliable clusters for distributed AI workloads

When starting a job, you expect it to run without interruptions. This expectation holds true across many domains, but it resonates especially deeply with machine learning engineers who launch large-scale pre-training jobs. Maintaining a stable training environment is crucial for delivering AI results on schedule and within budget constraints.

August 28, 2025
9 mins to read

Sign in to save this post
Sign In
