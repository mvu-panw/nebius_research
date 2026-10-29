# How and why we built Managed PostgreSQL for AI workloads

Source: https://nebius.com/blog/posts/managed-postgresql-for-ai-workloads

Skip to main content

At Nebius, we offer a fully managed, one-click PostgreSQL solution. Since GA in 2025, it has grown to hundreds of production clusters and tens of tebibytes of data under management.

In this article, I’ll describe how it is implemented under the hood, the engineering decisions we made along the way, and how we optimize the solution for AI workloads.

## Deciding how to build Nebius Managed PostgreSQLDeciding how to build Nebius Managed PostgreSQL

When we designed the Nebius Managed PostgreSQL service, our aim was to recreate what worked best in general cloud services while combining this with the latest technologies and specializations for AI use cases.

Our Managed PostgreSQL service is used not only by our external customers, but also by many Nebius services. Our customers and internal teams expect the following as a minimum bar:

- High availability

- PITR

- Automated failover

- Periodic physical backups, compressed and encrypted

- Fast restores

- Connection pooling

- Extensive metrics coverage and logs

- Zero data loss with strict synchronous replication guarantees

Given these requirements, we chose to use Kubernetes alongside CloudNativePG (CNPG), the open-source Kubernetes operator for PostgreSQL. Despite CNPG being relatively new, it had three major points in its favor:

- Developed by the experienced EnterpriseDB team

- Provided most of the features from the list above out of the box

- Distributed as open-source under the Apache License 2.0

After a detailed comparison of each operator available at that time, we decided to move forward with CNPG.

Looking back over the last three years of development, it was the right decision: the CNPG operator has matured and is now the most popular Kubernetes operator for PostgreSQL.

## How clusters are organizedHow clusters are organized

We create a separate MK8s cluster for each cloud project. This allows multiple instances of Managed PostgreSQL (or even other Nebius cloud services such as Managed MLflow) to run inside the same Kubernetes cluster while ensuring all instances belong to a single customer. This approach avoids security and isolation issues.

To achieve fair resource utilization, each PostgreSQL instance is allocated to a separate compute node inside the MK8s cluster.

Let’s have a look at how our typical cluster is organized:

Let’s look at some of the features of our PostgreSQL and why they’re important for AI use cases.

## Persistent data storage for disaster mitigationPersistent data storage for disaster mitigation

Persistent data is stored on Nebius network SSD drives. This approach allows fast migration of cluster instances in case of sudden compute instance failures. These disks are also replicated, meaning that they are fault-tolerant by design and can survive physical device failures well.

## Backups for disaster recovery and experimentation velocityBackups for disaster recovery and experimentation velocity

We perform periodic physical backups for every cluster and continuously archive WAL segments to object storage. Customers can restore the entire cluster to any point in time within the recovery window (seven days by default) with a single click in the console.

Fast backup and restore options are important for disaster recovery, and they’re also necessary for experimentation velocity in AI use cases. Teams frequently test new datasets, embedding models, vector indexes, and application logic. A fast physical backup/restore mechanism allows them to create a snapshot before an experiment and quickly roll back to a known-good state afterwards. This enables safer and faster iteration on production-like data.

### From Barman to WAL-GFrom Barman to WAL-G

Initially, we used Barman for backups, as it comes as standard with the CNPG operator. But we encountered two limitations:

- 

Slow backup and restoration. By default, Barman uses pg_basebackup for backup creation. Since pg_basebackup is single-threaded, it caused significantly longer backup creation times on large clusters (1 TB+). Barman backup restore runs single-threaded too, which was another bottleneck. For example, for large clusters, a Barman backup could take more than a day to complete and 15+ hours to restore. This is too long for teams building AI applications that want to test a new embedding model or chunking strategy on a copy of production data.

- 

Precise control over resource utilization. We wanted to control which resources are allocated to a backup process and limit their impact on the running database, but CNPG offers only limited control over resources such as network and disk. Without this control, queries slow down as they compete for disk and network bandwidth.

We resolved both limitations by switching to WAL-G for backup creation and restoration. Today, 100% of our production clusters use WAL-G as a backup solution. With WAL-G, the same 1.5 TB cluster that took a day to back up and 20+ hours to restore can be backed up in 2 hours and restored in just an hour. Backups are running smoothly, and our SRE team sleeps soundly!

## Connection pooling for bursty AI workloadsConnection pooling for bursty AI workloads

AI workloads often create bursty and unpredictable database traffic: agents, workers, background jobs, embedding pipelines, RAG services, chat sessions, and evaluation tasks may all access PostgreSQL simultaneously. Some of these requests are short-lived metadata lookups, some perform vector similarity searches, some write conversation history or model outputs, and others run batch ingestion or indexing jobs.

Without a connection pooler, every AI worker or service replica may try to open its own direct database connections. During spikes, this can quickly create a connection storm, where PostgreSQL spends too much time managing client sessions instead of executing useful queries.

A connection pooler solves this by sitting between applications and PostgreSQL. Instead of allowing every application instance, worker, or AI agent to keep its own direct database connections, the pooler maintains a smaller, controlled set of connections to PostgreSQL and reuses them efficiently. This reduces connection churn, protects the database from traffic spikes, and helps keep PostgreSQL focused on executing queries rather than constantly creating, managing, and destroying sessions.

We serve all client connections via a connection pooler (PgBouncer). Customers can choose the preferred connection mode: session or statement pooling. We allocate connection pooler pods on the same nodes as the PostgreSQL pods to lower the round-trip time between the client and the PostgreSQL backend process. This approach also minimizes potential disruptions from compute node maintenance.

## Why we ship two vector extensionsWhy we ship two vector extensions

Two vector search extensions, pgvector and pgvectorscale, are available on every cluster out of the box. Which one is right depends on whether your index fits in RAM, and that answer tends to change as a dataset grows.

- 

pgvector provides two memory-optimized data structures with two index types: HNSW and IVFFlat. These are memory-oriented ANN structures and perform well when all the data fits into memory. It’s supported by many cloud providers, and it’s fast and easy to use.

- 

pgvectorscale is another ANN implementation, inspired by Microsoft DiskANN research. It’s designed specifically for lower RAM usage and huge SSD-backed datasets. Instead of trying to keep massive ANN graphs mostly in RAM, it optimizes for disk and cache efficiency. As a tradeoff, it has worse throughput/recall performance. It uses pgvector structures as a base and optimizes storage for memory-limited environments.

## What the benchmarks showWhat the benchmarks show

We ran an open-source benchmark suite on Nebius and on a comparable AWS instance. We used VectorDBBench, which ships with standard datasets and benchmarks against different ANN engines. We ran on an 8 vCPU / 32 GB preset using OpenAI embeddings.

 | Machine
 | vCPU
 | Memory (GB)
 | Price

 | AWS db.m5.2xlarge
 | 8
 | 32
 | $0.712/hr

 | Nebius cpu-e2-8vcpu-32gb
 | 8
 | 32
 | $0.560/hr

The benchmark parameters were:

vectordbbench pgvectorhnsw --host <host> 
--db-name <db-name> --user-name <username> --password <password> 
--case-type 'Performance1536D500K' --ef-construction 200 --m 16 
--ef-search 40 --max-parallel-workers 7 --skip-load --skip-drop-old 
--num-concurrency 80 --concurrency-duration 600

Since AWS only has the vector extension installed, we tested it exclusively. We used 80 simultaneous connections for 10 minutes on the OpenAI 500K dataset (Performance1536D500K in VectorDBBench). The results were 1,267 QPS on AWS and 1,122 on Nebius for the same recall of around 96%. While the performance is comparable, Nebius comes in 3–4 times cheaper.

## How we engineer for AI workloads in everything we doHow we engineer for AI workloads in everything we do

At Nebius, we combine the best of general cloud engineering with specialized expertise that allows us to tailor every element of our platform for AI workloads. That’s true for our managed PostgreSQL service too.

Most of what makes this service work for AI workloads wasn’t originally built with AI workloads in mind. Cluster isolation, replicated SSDs, synchronous replication, and WAL-G are ordinary database engineering. AI workloads made them matter more: PITR becomes an experimentation tool when you retrain embeddings twice a week, and a pooler becomes essential when an agent fleet opens connections faster than the database can close them.

Spin up a Managed PostgreSQL cluster, load your own embeddings, and run the benchmark above. Get started now.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Daniil Zakhlystov

Evgeny Shavlyugin

Contents

- 

Deciding how to build Nebius Managed PostgreSQL

- 

How clusters are organized

- 

Persistent data storage for disaster mitigation

- 

Backups for disaster recovery and experimentation velocity

- From Barman to WAL-G

- 

Connection pooling for bursty AI workloads

- 

Why we ship two vector extensions

- 

What the benchmarks show

- 

How we engineer for AI workloads in everything we do

## See also

### 

What we built this quarter: Nebius Cloud Platform

The Q3 2026 release of Nebius AI Cloud is here. Cloud Interconnect opens a private, MACsec-encrypted path between Nebius and your own networks; spot pricing puts idle GPU capacity on the market at demand-set prices; and Serverless AI now runs Python jobs with no containers to build. Here’s what shipped, what changed, and why it matters.

October 1, 2026
12 mins to read

### 

In agentic RL, faster tokens are not enough

Faster model inference does not necessarily mean faster agentic RL training. In this article, we show how improvements to routing, sandbox execution and batch assembly reduced fixed-weight batch collection time by 66.9%, from 591.8 to 196.1 seconds for 256 trajectories.

September 28, 2026
22 mins to read

### 

Nebius and WEKA benchmark distributed KV cache for agentic inference on NVIDIA HGX B300

Nebius and WEKA benchmarked a distributed NVMe KV cache tier for agentic inference on NVIDIA HGX B300 in Nebius AI Cloud. Over eight hours on identical hardware, WEKA NeuralMesh with Augmented Memory Grid served 2.4× more requests than HBM-only, held a 93% cache hit rate against 40%, and kept median time to first token near one second. This post covers the results and the infrastructure underneath.

September 24, 2026
8 mins to read

Sign in to save this post
Sign In
