# Nebius AI Cloud services

Source: https://docs.nebius.com/overview/services

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius AI Cloud services

The resources you create in Nebius AI Cloud belong to *Nebius AI Cloud services*.

## List of services

### Compute

* ***Compute – virtual machines*** (all [regions](https://docs.nebius.com/overview/regions.md))

  Compute allows you to create and manage virtual machines (VMs). They are like your local machine, but in the cloud. You can connect to them and use their GPUs and other computing resources in your ML/AI workloads. Grouping VMs with GPUs into GPU clusters enables fast InfiniBand™ interconnection.

  ***[Documentation](https://docs.nebius.com/compute/index.md)***

* ***Managed Service for Soperator*** (all [regions](https://docs.nebius.com/overview/regions.md) except for `us-north1` and `uk-south2`)

  Managed Service for Soperator provides Slurm-based clusters for distributed ML/AI training. Soperator is an open-source Kubernetes operator from Nebius that combines features from Slurm and Kubernetes. This allows you to efficiently manage both your ML workloads and the underlying infrastructure.

  ***[Documentation](https://docs.nebius.com/slurm-soperator/index.md)***

* ***Managed Service for Kubernetes®*** (all [regions](https://docs.nebius.com/overview/regions.md))

  With Kubernetes, you can efficiently manage and scale your containerized ML/AI applications and ensure they are portable and fault-tolerant. Managed Service for Kubernetes offered by Nebius AI Cloud provides a streamlined experience of deploying and managing clusters powered by Kubernetes.

  ***[Documentation](https://docs.nebius.com/kubernetes/index.md)***

### Storage

In Nebius AI Cloud, you can store data in VM volumes, Amazon S3-like buckets, registries for Docker and Helm artifacts, and PostgreSQL® databases.

* ***Compute – disks and shared filesystems*** (all [regions](https://docs.nebius.com/overview/regions.md))

  Virtual machines in Compute use volumes that are also part of the Compute service. Disks are block storage volumes. Each of them is used on one running VM at a time as a boot disk or an additional (secondary) disk. Shared filesystems are file storage volumes that can be shared by multiple VMs. The POSIX compliance guarantees and consistency semantics of shared filesystems are described in the [shared filesystem documentation](https://docs.nebius.com/compute/storage/types.md#posix-compliance-and-consistency-guarantees-for-filesystems).

  ***[Documentation](https://docs.nebius.com/compute/storage/types.md)***

* ***Object Storage*** (all [regions](https://docs.nebius.com/overview/regions.md))

  Most ML/AI workloads involve large files, such as datasets and artifacts of trained models. To store, access and share them efficiently, you can use Object Storage, an Amazon S3-like storage service offered by Nebius AI Cloud.

  ***[Documentation](https://docs.nebius.com/object-storage/index.md)***

* ***Managed Service for PostgreSQL®*** (all [regions](https://docs.nebius.com/overview/regions.md) except for `eu-north2`\*, `eu-south1`, `us-north1` and `uk-south2`)

  Database systems such as PostgreSQL are an important part of MLOps: you can set up your ML tools to ingest data from databases, as well as store metadata and other artifacts in them. Managed Service for PostgreSQL in Nebius AI Cloud offers an easy way to deploy and work with fully managed PostgreSQL databases.

  ***[Documentation](https://docs.nebius.com/postgresql/index.md)***

* ***Container Registry*** (all [regions](https://docs.nebius.com/overview/regions.md))

  Container Registry is your best choice to safely store your application containerized into Docker images and Helm charts, and access them easily in workloads that you run in Nebius AI Cloud.

  ***[Documentation](https://docs.nebius.com/container-registry/index.md)***

### AI services

* ***Serverless AI*** (all [regions](https://docs.nebius.com/overview/regions.md) except for `eu-north2`\*)

  Serverless AI is a service for running containerized AI workloads as interactive Devlabs for coding, jobs that run to completion, or endpoints that serve users. By deploying your workloads in Serverless AI, you can focus on them without worrying about the infrastructure: the service handles resource provisioning and lifecycle, and usage-based, per-second billing.

  ***[Documentation](https://docs.nebius.com/serverless/overview.md)***

* ***Managed Service for MLflow*** (`eu-north1`, `me-west1`, `us-central1`, `uk-south1` and `eu-west2` [regions](https://docs.nebius.com/overview/regions.md))

  MLflow is a highly available platform for managing a lifecycle of machine learning experiments. You can track them, organize models into detailed versions, compare metrics and deploy customized models. Managed MLflow in Nebius AI Cloud enables you to access model artifacts, training results and tuned hyperparameters in a single interface. As a result, you can reproduce ML experiments and deploy the best performing models.

  ***[Documentation](https://docs.nebius.com/mlflow/index.md)***

* ***Applications*** (`eu-north1` and `us-central1`)

  Deploy third-party software on Managed Service for Kubernetes® clusters from the Applications marketplace.

  ***[Documentation](https://docs.nebius.com/applications/index.md)***

### Observability

* ***Monitoring*** ([in preview](#service-and-application-stages); all [regions](https://docs.nebius.com/overview/regions.md))

  Monitoring collects and visualizes resource metrics, and allows you to set custom alerts that are triggered when these metrics cross the specified thresholds.

  ***[Documentation](https://docs.nebius.com/observability/monitoring.md)***

* ***Logging*** ([in preview](#service-and-application-stages); all [regions](https://docs.nebius.com/overview/regions.md))

  Logging collects, stores and provides logs for your Nebius AI Cloud services. It allows you to view all logs in one place and debug issues faster.

  ***[Documentation](https://docs.nebius.com/observability/logging.md)***

### Network

* ***Virtual Networks*** (all [regions](https://docs.nebius.com/overview/regions.md))

  The service provides networking infrastructure, so you can create Nebius AI Cloud resources within it. Virtual Networks enables routing, segmentation, IP addressing and private DNS for your resources in the tenant.

  ***[Documentation](https://docs.nebius.com/vpc/index.md)***

* ***Nebius Tunnels*** ([in preview](#service-and-application-stages); all [regions](https://docs.nebius.com/overview/regions.md))

  Nebius Tunnels lets you expose local HTTP and TCP services to the internet through an outbound agent connection, without opening inbound firewall ports.

  ***[Documentation](https://docs.nebius.com/tunnels/index.md)***

### Management

* ***Identity and Access Management*** (all [regions](https://docs.nebius.com/overview/regions.md))

  Identity and Access Management helps you centrally manage user and service account access to your Nebius AI Cloud resources. It ensures that only users and service accounts with specific permissions can interact with your resources.

  ***[Documentation](https://docs.nebius.com/iam/index.md)***

### Security

* ***Audit Logs*** (all [regions](https://docs.nebius.com/overview/regions.md))

  With the Audit Logs, you can see who did what and when with your resources, to ensure security, compliance and accountability.

  ***[Documentation](https://docs.nebius.com/audit-logs/index.md)***

* ***Key Management Service*** (all [regions](https://docs.nebius.com/overview/regions.md))

  The service issues and stores cryptographic keys that you can use to protect your applications. Key Management Service allows you to perform such operations as data encryption, decryption, signing hashes or generating data keys for envelope encryption.

  ***[Documentation](https://docs.nebius.com/kms/index.md)***

* ***SecretStash*** (all [regions](https://docs.nebius.com/overview/regions.md))

  The service stores sensitive data as secrets in an encrypted form. For instance, you can store API keys, tokens and certificates securely. This allows you to avoid hardcoding sensitive data, and still allows you to reuse that data in scripts, pipelines and applications.

  ***[Documentation](https://docs.nebius.com/mysterybox/index.md)***

## Service and application stages

Each Nebius AI Cloud service or application is either in preview or generally available.

### Preview

Services and applications *in preview* are intended for testing and feedback. They come without guaranteed service levels, and you may encounter issues and bugs when using them. It is not recommended to use services and applications in preview for production purposes.

Nebius AI Cloud provides services and applications in preview free of charge. In some cases, access to a service or an application in preview might be limited.

A service or an application in preview can be different from its final, generally available version, and is not guaranteed to become generally available at all. Most services and applications in preview become paid after becoming generally available, but you will never be retrospectively charged for using a service or an application while it was free of charge in preview.

Parts of services and applications, such as their individual features, can also be in preview.

### General availability

*Generally available* services and applications are ready to use in production environments. They are fully supported by Nebius AI Cloud and usually covered by service level agreements (SLAs). Usually, you are charged for using generally available services and applications.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
