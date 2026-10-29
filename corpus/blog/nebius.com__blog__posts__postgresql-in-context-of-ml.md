# PostgreSQL in the context of ML

Source: https://nebius.com/blog/posts/postgresql-in-context-of-ml

Skip to main content

Data cleaning and transformation is a big part of an ML engineer’s job. The underlying database infrastructure can often make this work more challenging than it needs to be. Given the diverse architectural styles and solutions in the database world, ML engineers frequently fall into the trap of picking the “right” tool for the data task.

For example,

- 

InfluxDB or RRDtool for time-series data

- 

Elasticsearch for searching through transactions

- 

Neo4j for graph databases

- 

Redis for queuing

The list goes on. Multiple solutions increase project costs and complexity, making it impractical for smaller teams. While large teams may foot the bill, excessive tooling causes delays by adding to the learning curve.

That’s where PostgreSQL can help. It has a wide range of features that make it good enough for any ML project. Besides, it includes PGML, an open-source extension to train and deploy ML models directly within the Postgres database. You can run ML workloads without moving data between systems.

This article explores PostgreSQL features for ML tasks and different ways that ML engineers can start using PostgreSQL.

## Understanding databasesUnderstanding databases

Before getting started, let’s briefly review database technologies in general. Databases can be broadly categorized into SQL and NoSQL.

SQL, or relational databases, organize data into tables with rows and columns. You define relationships between tables through foreign keys, joins, and other constraints.

A SQL database strictly follows ACID properties. Consequent operations are always completed together. If a single operation fails in a set of operations, the entire set fails. This makes SQL databases extremely reliable.

However, reliability comes at the cost of flexibility and performance. Most SQL databases offer limited data types and enforce rules that require workarounds for real-world data. You also get redundant columns and tables with the same information duplicated across multiple tables. It can increase storage costs and impact performance at scale.

The NoSQL, or non-relational databases, emerged as an alternative solution. They do not impose rigid structures on data. However, the flexibility comes at the cost of reduced data integrity and reliability. They guarantee availability and eventual consistency. The database state can become inconsistent in unpredictable ways, resulting in strange bugs.

As the name suggests, PostgreSQL is a SQL database, but its unique design offers more flexibility and better performance than similar solutions.

## Introducing PostgreSQLIntroducing PostgreSQL

PostgreSQL is an open-source object-relational database system (ORDBMS). Like traditional relational databases, it imposes a tabular structure on data and uses familiar SQL for queries and operations. However, as an ORDBMS, it also allows you to define complex data types like arrays and other custom types that can store more than just integers and strings. You get more flexibility with less integrity trade-offs.

PostgreSQL’s long feature list gives you many NoSQL benefits even while meeting the SQL standard. For example, NoSQL databases like MongoDB let you store documents and allow rich query searches within document text. PostgreSQL also lets you store documents in JSON or BSON format. You get flexible data modeling and rich queries without sacrificing reliability and transactional integrity.

PostgreSQL’s flexibility and customizability make it very suitable for the diverse data transformation requirements of ML teams. Having been around for 35 years, it is a mature solution with an active developer community. It meets all required security standards, and best of all, it is free for anyone to install and use.

PostgreSQL is like an elephant-sized tool chest (pun intended!). It has several data tooling options that provide decent performance for almost all ML use cases.

## PostgreSQL features for ML engineersPostgreSQL features for ML engineers

We give several examples below of using PostgreSQL for ML workloads, but you can do much more. It is also important to note that there are several ways of accomplishing the task in PostgreSQL, and we have only suggested some approaches. You can ask questions about your requirements on Reddit or search for ideas in the PostgreSQL wiki.

### Time series analysisTime series analysis

ML engineers often have to analyze a data sequence recorded at specific intervals. PostgreSQL includes many features for time-stamped data.

For example, you can use:

- 

time_bucket function from the TimescaleDB extension to aggregate data into regular intervals

- 

window functions for running calculations over a set of table rows that are related to the current row

- 

date_trunc to truncate a timestamp into the bucket size you want

### Regression analysisRegression analysis

You can implement regression analysis directly in PostgreSQL using its statistical functions, such as regr_slope, regr_intercept, and regr_r2. You can also calculate regression models without exporting data to an external tool.

### Full-text searchFull-text search

PostgreSQL data types like tsvector and tsquery types allow you to efficiently perform complex searches on large text datasets. You can tokenize, normalize, and rank documents based on relevance. It is also convenient for hybrid search that combines relational and full-text search. For example, you can write queries for requests like, 'Give me all departments with employees that live within the USA and write emails or Slack messages containing the words machine learning.'

### Text classificationText classification

Building on full-text search, you can also implement basic text classification directly in the database. You can write custom functions in any programming language without recompiling PostgreSQL. For example, you could write a function classifying emails using a Naive Bayes classifier implemented within the database. This approach enables you to keep the classification logic close to your data.

### Image transformationImage transformation

PostgreSQL extension PostGIS adds support for geographic objects (raster data) that you can use to handle images. You can apply transformations like resizing, cropping, or format conversion using SQL queries.

### Storing ML modelsStoring ML models

You can also store and manage smaller machine-learning models, such as linear regression or decision trees, directly in the database. That way, models are easily accessible and version-controlled alongside the data they were trained on.

## How to use PostgreSQL for your ML projectsHow to use PostgreSQL for your ML projects

Given PostgreSQL’s flexibility, it can be part of a larger data pipeline where data is extracted, transformed, and loaded (ETL) from various sources into PostgreSQL, then analyzed and modeled using external ML frameworks. It has extensions integrating all ML tooling from Jupyter Notebooks to Apache Spark. Some more options include…

### Procedural languagesProcedural languages

PostgreSQL supports several procedural languages adapted from common ones like Python, R, and Perl. These languages allow you to write complex logic and integrate machine learning algorithms directly into the database.

For example, PL/Python lets you use familiar libraries like scikit-learn, TensorFlow, or PyTorch within PostgreSQL. You can create user-defined functions (UDFs) that call Python scripts for ML tasks. PL/R lets you write R scripts within PostgreSQL, giving you access to R’s extensive libraries directly in your SQL queries.

### Apache MADlibApache MADlib

Apache MADlib is an open-source library designed for PostgreSQL. You can install it as a PostgreSQL extension and access its functions directly in your SQL queries. MADlib supports a wide range of ML algorithms and provides tools for data preprocessing, such as normalization and feature extraction.

### PostgresMLPostgresML

PostgresML is an ML/AI platform built inside PostgreSQL. It is based on moving models to the database instead of constantly moving data to the models. You get capabilities like a GPU-accelerated inference engine, access to open-source models with version control, model training functionality, and a feature store within the database itself. You can sign up with the tool for managed solutions or install the open-source pgml package for self-managed deployment.

## Challenges in using PostgreSQL for MLChallenges in using PostgreSQL for ML

It is important to remember that ML is a relatively new use case for PostgreSQL. It was originally designed for transactional operations rather than the large-scale, parallel processing often required for machine learning. You must manually configure and tweak your PostgreSQL setup for optimum performance.

- Scaling. Running complex queries, like large joins or aggregations, creates performance bottlenecks. Horizontal scaling is the solution, but it requires adding more processing and storage nodes on the fly. This requires implementing partitioning and replication strategies that complicate infrastructure management. Tuning PostgreSQL for scale can be difficult without deep expertise.

ML data backups are also time-consuming and resource-intensive. Restoring large datasets after a failure incident can lead to extended downtime.

- Integration. ML pipelines often include distributed processing tools like Apache Spark. Integrating PostgreSQL in such environments introduces additional management overheads.

- Performance. As mentioned, PostgreSQL is good enough but not the most optimum tool for every ML task. Its performance may still lag behind that of specialized NoSQL databases for your specific requirement. Complex transformations can lead to long-running queries that slow your system down.

Similarly, training large models directly in PostgreSQL can be slow and resource-intensive. You may not be able to leverage the full power of GPU acceleration available in other environments.

## Managed PostgreSQL as a solutionManaged PostgreSQL as a solution

Managed Service for PostgreSQL by Nebius makes it easy for ML engineers to integrate PostgreSQL into their projects. You use the Nebius console to create your PostgreSQL clusters and send your SQL queries. The managed service does all the underlying work, such as:

- 

Database installation and resource allocation for initial setup.

- 

Configuration tuning optimized to cluster size.

- 

Automatic data backup and easy restoration when needed.

With managed PostgreSQL, you can add new servers or increase capacity in a few clicks. You can also visualize and monitor the status of your PostgreSQL cluster in the console.

## ConclusionConclusion

PostgreSQL is a feature-packed relational database that acts like an all-in-one solution for ML developers. It gives the flexibility and scalability of NoSQL along with SQL’s reliability and data integrity. It offers several options to integrate into your unique ML ecosystem. You can use it to bring your models to your data instead of moving data across several tools and databases to your ML model.

However, PostgreSQL creates new challenges in the scale and performance of ML workloads. Services like Nebius Managed PostgreSQL handle database provisioning details so you can focus on your ML tasks and get the most out of this database.

## Explore Nebius

Get started​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

We’re launching a new Nebius platform built from the ground up

We have developed a new version of Nebius platform that we believe will serve your needs even better. It is already being tested by our in-house LLM R&D team and a number of clients. Now, we are rolling it out to everyone.

October 16, 2024
4 mins to read

### 

Introducing Nebius AI Studio: Achieve fast, flexible inference today

Our new platform not only allows application builders to use generative AI without significant effort but does so at a fraction of the cost. Our goal is to democratize access to cutting-edge AI technologies, enabling businesses of all sizes to innovate and compete in the AI space.

September 30, 2024
4 mins to read

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

Sign in to save this post
Sign In
