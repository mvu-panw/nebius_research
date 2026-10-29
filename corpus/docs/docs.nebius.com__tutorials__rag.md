# Building a RAG electronics store chatbot with JupyterLab, Serverless AI and Managed Service for PostgreSQL®

Source: https://docs.nebius.com/tutorials/rag

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Building a RAG electronics store chatbot with JupyterLab, Serverless AI and Managed Service for PostgreSQL®

This tutorial walks you through building a Retrieval-Augmented Generation (RAG) chatbot that answers questions by using your own documents. You will use [Managed Service for PostgreSQL](https://docs.nebius.com/postgresql/index.md) with the pgvector extension to store and search text embeddings, a [Serverless AI Devlab](https://docs.nebius.com/serverless/quickstart/devlabs.md) with JupyterLab to prepare the knowledge base and run retrieval logic, and a [Serverless AI](https://docs.nebius.com/serverless/index.md) LLM endpoint (vLLM with an OpenAI-compatible API) for inference. You will deploy the Qwen3-0.6B model for generation. You run the full RAG pipeline from the notebook and call the endpoint for generation. By the end, you will have a working example of an electronics store assistant that uses product catalogs and policies to answer customer questions.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute](https://docs.nebius.com/compute/resources/pricing.md) resources used by Serverless AI: a Devlab with JupyterLab and an endpoint
* [Managed Service for PostgreSQL cluster](https://docs.nebius.com/postgresql/resources/pricing.md)

## Prerequisites

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* Create resources in a project in a [region](https://docs.nebius.com/overview/regions.md) where [Serverless AI](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region) and [Managed Service for PostgreSQL](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region) are available, for example `eu-north1`, `eu-west1` or `us-central1`.
* In the [web console](https://console.nebius.com), go to  **Administration** → **Limits** and make sure that you have at least one **NVIDIA® Hopper® H200 for regular VMs without reservations** and one virtual machine under **Compute**, and one allocation under **Virtual Networks** in the region that you use. [Increase quotas](https://docs.nebius.com/overview/quotas.md#change-quotas) if needed.

## Steps

### Create a Managed Service for PostgreSQL cluster

1. In the [web console](https://console.nebius.com), go to  **Managed Service for PostgreSQL**.

2. Click **Create cluster** and configure the cluster:

   * Enter a name.
   * In **Access**, select **Public and private** so that JupyterLab can connect to the cluster from the internet.
   * In **Resources**, choose a preset (for example, `4 vCPUs – 16 GiB RAM`) and set the storage size.
   * In **Database**, set the database name, username and password. For example: database `rag-example`, user `rag_example_user` and a strong password.

3. Click **Create cluster** and wait until it is ready.

4. Open the cluster page. On **Cluster overview**, click **Copy endpoint URL** and select **Public RW endpoint URL** to copy the connection host. In the **General** block you can copy **Bootstrap database** and **Username** if needed. You will need the endpoint host, database name, username and password in the notebook.

Managed Service for PostgreSQL clusters have the [pgvector extension](https://docs.nebius.com/postgresql/databases/extensions.md#pgvector) available. You will enable it in the notebook.

### Create a JupyterLab Devlab

1. Create a Devlab from the JupyterLab template:

   1. In the [web console](https://console.nebius.com), go to  **Serverless AI** → **Devlabs**.
   2. Click  **Create Devlab**.
   3. Under **Devlab settings**, choose **Template** and select **JupyterLab**.
   4. Review the prefilled Devlab settings. The console generates the Jupyter token automatically. Copy and save the token securely.
   5. Click **Create Devlab** and wait until the Devlab is running.

2. Open the Devlab UI:

   1. On the Devlab page, click the web UI link to connect to JupyterLab. Enter the token if prompted.
   2. Open a new notebook. You will run all the code below in this notebook.

### Prepare the knowledge base in JupyterLab

1. In JupyterLab, open a terminal and install dependencies:

   ```bash theme={null}
   pip install psycopg2-binary sentence_transformers
   ```

2. Create three Markdown files in the notebook's working directory: `laptop_catalog.md`, `headphones_catalog.md`, and `return_policy.md`. Use sections separated by `## ` headers. Full example contents:

   > **laptop\_catalog.md**
   >
   > ```markdown theme={null}
   > ## Dell Inspiron 15
   > - Type: Laptop
   > - Price: $849.99
   > - RAM: 16GB DDR4
   > - Storage: 512GB SSD
   > - CPU: Intel Core i7-1255U
   > - Display: 15.6" FHD
   > - Battery Life: Up to 8 hours
   > - Return Policy: 14 days unopened, 7 days if opened (10% restocking fee)
   >
   > ## Lenovo IdeaPad Slim 5
   > - Type: Laptop
   > - Price: $699.99
   > - RAM: 8GB DDR4
   > - Storage: 256GB SSD
   > - CPU: AMD Ryzen 5 5500U
   > - Display: 14" FHD
   > - Battery Life: Up to 10 hours
   > - Return Policy: 14 days unopened only
   >
   > ## Apple MacBook Air M2
   > - Type: Laptop
   > - Price: $1,199.00
   > - RAM: 8GB Unified Memory
   > - Storage: 512GB SSD
   > - CPU: Apple M2
   > - Display: 13.6" Retina
   > - Battery Life: Up to 18 hours
   > - Return Policy: 7 days unopened only
   > ```

   > **headphones\_catalog.md**
   >
   > ```markdown theme={null}
   > ## Sony WH-1000XM5
   > - Type: Headphones
   > - Price: $399.99
   > - Type: Over-Ear
   > - Features: Noise Cancelling, Wireless, 30-hour Battery Life
   > - Return Policy: 14 days with packaging
   >
   > ## Apple AirPods Pro (2nd Gen)
   > - Type: Headphones
   > - Price: $249.00
   > - Type: In-Ear
   > - Features: Active Noise Cancellation, Transparency Mode, Wireless Charging
   > - Return Policy: 7 days unopened
   >
   > ## JBL Tune 510BT
   > - Type: Headphones
   > - Price: $49.95
   > - Type: On-Ear
   > - Features: Wireless, 40-hour Battery, Fast Charging
   > - Return Policy: 30 days (opened or unopened)
   > ```

   > **return\_policy.md**
   >
   > ```markdown theme={null}
   > ## General Return Rules:
   > - Proof of purchase is required for all returns.
   > - All returns must be initiated within the stated return window.
   >
   > ## Return Electronics (Laptops, Phones, Tablets):
   > - Unopened: Return within 14 days for full refund.
   > - Opened: Return within 7 days with 10% restocking fee.
   >
   > ## Return Accessories (Headphones, Chargers, Cases):
   > - Varies by product. See specific item entry.
   > - Generally:
   >   - High-end headphones: 14 days with packaging.
   >   - Budget headphones: 30 days regardless of packaging.
   >
   > ## Return Refund Timeline:
   > - Refunds are processed within 5 business days after return approval.
   >
   > ## Non-Returnable Items:
   > - Software licenses, gift cards, and opened hygiene products.
   > ```

3. In the notebook, run the following in order:

   1. Connect to the database and create the table.

      Replace `<host>`, `<dbname>`, `<user>` and `<password>` with your Managed Service for PostgreSQL cluster connection details: use **Public RW endpoint URL** as the hostname and the **Bootstrap database**, **Username** and password from the **General** block.

      The `all-MiniLM-L6-v2` model produces 384-dimensional vectors. If you use another model, change `vector(384)` in the table definition.

      ```python theme={null}
      import psycopg2

      conn = psycopg2.connect(
          dbname="<dbname>",
          user="<user>",
          password="<password>",
          host="<host>",
          port=5432,
          sslmode="require"
      )
      cur = conn.cursor()

      cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
      conn.commit()

      cur.execute("""
          CREATE TABLE IF NOT EXISTS documents (
              id SERIAL PRIMARY KEY,
              content TEXT,
              embedding vector(384)
          )
      """)
      conn.commit()
      ```

   2. Load the embedding model and define helpers.

      ```python theme={null}
      from sentence_transformers import SentenceTransformer

      model = SentenceTransformer('all-MiniLM-L6-v2')

      def get_embedding(text):
          return model.encode(text).tolist()

      def add_document(content):
          embedding = get_embedding(content)
          cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (content, embedding))

      def chunk_text(text):
          raw_chunks = text.split("## ")
          return ["## " + chunk.strip() for chunk in raw_chunks if chunk.strip()]

      def get_chunks_from_docs(*filenames):
          for filename in filenames:
              with open(filename, 'r', encoding='utf-8') as f:
                  text = f.read()
                  for chunk in chunk_text(text):
                      add_document(chunk)
              conn.commit()
      ```

   3. Ingest the documents:

      ```python theme={null}
      get_chunks_from_docs('laptop_catalog.md', 'headphones_catalog.md', 'return_policy.md')
      ```

   4. Define retrieval and prompt building:

      ```python theme={null}
      def search_documents(query, limit=5):
          query_embedding = get_embedding(query)
          cur.execute("""
              SELECT content, embedding <=> %s::vector AS distance
              FROM documents
              ORDER BY distance
              LIMIT %s
          """, (query_embedding, limit))
          return [f"{i}. {content}" for i, (content, _) in enumerate(cur.fetchall(), 1)]

      def build_prompt(query, retrieved_chunks):
          context = "\n\n".join(retrieved_chunks)
          return f"""Answer the following question based on the context below.

      Context:
      {context}

      Question: {query}

      Answer:"""
      ```

   Your knowledge base is now ready for RAG queries.

### Deploy a serverless LLM endpoint

The endpoint exposes an OpenAI-compatible API that you will call from your JupyterLab notebook.

1. In the [web console](https://console.nebius.com), go to  **Serverless AI** → **Endpoints** and click  **Create endpoint**.

2. Under **Endpoint settings** → **Image path**, enter `vllm/vllm-openai:latest`.

3. Under **Ports**, set the container port to `8000`.

4. Under **Entrypoint command**, specify the following value:

   ```bash theme={null}
   python3 -m vllm.entrypoints.openai.api_server --model Qwen/Qwen3-0.6B --host 0.0.0.0 --port 8000
   ```

5. Under **Computing resources**, choose **With GPU**, then select a platform (for example, `NVIDIA® H200 NVLink`) and a preset (for example, `1 GPU — 16 vCPUs — 200 GiB RAM`).

6. Click **Create** and wait until the endpoint status is `Running`. It may take five minutes.

7. Open the endpoint. In the **Network** section, copy the value of a public endpoint in the `http://<IP_address>:8000` format.

### Call the LLM from the notebook

1. Add the following code to your JupyterLab notebook to call the deployed endpoint. Replace `<ENDPOINT_IP>` with the endpoint address from [Deploy a serverless LLM endpoint](#deploy-a-serverless-llm-endpoint).

   ```python theme={null}
   import requests
   import re

   API_BASE = "http://<ENDPOINT_IP>"
   MODEL_ID = "Qwen/Qwen3-0.6B"

   def ask_llm(prompt):
       response = requests.post(
           f"{API_BASE}/v1/chat/completions",
           headers={
               "Content-Type": "application/json"
           },
           json={
               "model": MODEL_ID,
               "messages": [
                   {
                       "role": "system",
                       "content": "You are a helpful store assistant. Answer based only on the provided information."
                   },
                   {
                       "role": "user",
                       "content": prompt
                   }
               ],
               "max_tokens": 2560,
               "temperature": 0.6
           }
       )
       data = response.json()
       raw_text = data["choices"][0]["message"]["content"]
       # Optional: remove reasoning traces if present
       clean_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()
       return clean_text
   ```

2. Run a RAG query:

   ```python theme={null}
   query = input("Your question: ")
   results = search_documents(query)
   answer = ask_llm(build_prompt(query, results))
   print(answer)
   ```

The pipeline retrieves relevant document chunks from Managed Service for PostgreSQL and sends the constructed prompt to your serverless endpoint for generation.

> **Example**
>
> Your question: What laptop and headphones should I buy with a budget of 1000 USD?
>
> Answer: The laptop to buy is the Sony WH-1000XM5, and the headphones are the JBL Tune 510BT. Both products are within the 1000 USD budget.

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources so Nebius AI Cloud doesn't charge for them:

* **JupyterLab Devlab**: In the [web console](https://console.nebius.com), go to  **Serverless AI** → **Devlabs**, open the Devlab and delete it.
* **Serverless AI endpoint**: In the [web console](https://console.nebius.com), go to  **Serverless AI** → **Endpoints**. Open the endpoint, stop it if it is running, and then delete it.
* **Managed Service for PostgreSQL cluster**: Follow the [instructions](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-delete-clusters).

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
