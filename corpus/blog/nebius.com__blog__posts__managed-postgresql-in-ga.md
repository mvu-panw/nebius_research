# Introducing general availability of Managed Service for PostgreSQL

Source: https://nebius.com/blog/posts/managed-postgresql-in-ga

Skip to main content

As Managed Service for PostgreSQL transitions from preview to general availability, effective today we are introducing service pricing and SLAs.

# PostgreSQL for AI workloadsPostgreSQL for AI workloads

PostgreSQL is a renowned database solution that has been around for about three decades. With the rise of generative AI, PostgreSQL became a demanding solution for storing data for ML model training and running AI applications. It can handle large datasets of structured and semi-structured data for training, store and index vector embeddings using extensions like pgvector for RAG-based systems and serve as a persistent storage for metadata in MLOps pipelines.

# A fully managed serviceA fully managed service

Managed Service for PostgreSQL handles all of the underlying infrastructure jobs and frees up your team from excessive administrative complexities, such as:

- Service deployment and maintenance

- Network configuration and compute provisioning

- High availability configuration and automatic backups

- System observability

# What’s changed in general availabilityWhat’s changed in general availability

General availability comes with some noticeable improvements that will elevate your productivity and ensure a better user experience.

### Granular monitoring dashboardGranular monitoring dashboard

Starting from the preview launch, our dashboard consisted of panels that display resource usage, such as CPU, RAM or storage. Today, you have access to more specific information about database performance, replication parameters and connection pooler performance. Having such a granular view provides developers with sufficient information about the database usage and allows them to make deliberate decisions about the application backend.

### Advanced backup managementAdvanced backup management

By providing PostgreSQL as a managed service, we ensure that your data is secured and, if necessary, can be easily restored. During the preview stage, restoring backups required involvement of the Nebius support team. Now, you can handle the database backups on your own: you can extend the retention period up to 30 days instead of default 7 days, set the time when a backup should be created (one checkpoint per day) and restore the database state from the list of available backups.

Figure 1. List of backups for all PostgreSQL clusters

At the same time, you have more granular access to the database backups within the established retention period — just contact our support team and request a snapshot version of a precise time frame.

### Public pricing and SLAsPublic pricing and SLAs

During the preview period, Nebius customers had free access to this service, to test and validate its performance. Now, with production-ready features, the service will be billed according to the following rates:

 | Server configuration
 | Preview (USD)
 | General availability (USD)

 | 2vcpu-8gb
 | 0.00
 | 0.14/h

 | 4vcpu-16gb
 | 0.00
 | 0.28/h

 | 8vcpu-32gb
 | 0.00
 | 0.56/h

 | 16vcpu-64gb
 | 0.00
 | 1.12/h

 | 32vcpu-128gb
 | 0.00
 | 2.24/h

 | 48vcpu-192gb
 | 0.00
 | 3.36/h

Learn more about the service pricing in the documentation. To read about service SLAs, see the link.

# Getting startedGetting started

All existing preview deployments will automatically transition to the paid service. We encourage customers to review their current usage and adjust their configurations based on their specific needs.

To create a Nebius account, simply sign up for the platform and follow these guidelines. You can start working with PostgreSQL through our web interface, CLI or Terraform — choose the tool you prefer and we’ll manage the infrastructure for you.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

Nebius extends immediate access to NVIDIA Hopper GPUs

Striving to simplify the user experience, we increased the amount of compute resources immediately available for every user that signs up to our cloud. You can now access 8 NVIDIA H200 GPUs, 16 NVIDIA H100 GPUs and 2 NVIDIA L40S GPUs via our console and start using them immediately.

February 4, 2025
2 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

PostgreSQL in the context of ML

Among the many database options available, PostgreSQL stands out as a tool of choice for ML engineers. This article explores why and how you can use PostgreSQL to increase efficiency and speed in ML development.

November 21, 2024
10 mins to read

Sign in to save this post
Sign In
