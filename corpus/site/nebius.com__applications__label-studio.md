# Label Studio — Nebius applications

Source: https://nebius.com/applications/label-studio

Skip to main content

# Label Studio
by HumanSignal
Data

Deploys the upstream heartex/label-studio Helm chart maintained by HumanSignal. Label Studio is an open-source data labeling tool for preparing training data for machine-learning pipelines — it supports bounding boxes, polygons, keypoints, named entity recognition, audio transcription, video frame annotation, and many other interfaces. The chart bundles a PostgreSQL backend by default; an optional Redis cache can be enabled for background-job queues. The Web UI is reachable through a Nebius Application Tunnel; the first user to sign up becomes the project administrator.Deploy on Nebius
Free

Deployment methods1
Setup timefrom 15 minutesDeploy Label Studio (opens in a new tab)
Sign-in required to deploy. Free to browse and read docs.

Vendor:HumanSignal

Additional links
- Label Studio website (opens in a new tab)
- Label Studio documentation (opens in a new tab)
- Label Studio on GitHub (opens in a new tab)
- Helm chart source (opens in a new tab)

Licenses
- Label Studio Helm chartApache License 2.0
- Label Studio (Community Edition)Apache License 2.0
- postgresql (dependency)PostgreSQL License
- redis (dependency, optional)BSD-3-Clause

## Key features

### Upstream chart from HumanSignal

Vendored from HumanSignal/charts heartex/label-studio — the canonical chart maintained by the Label Studio team.

### Multi-modal labeling interfaces

Built-in templates for images (bounding boxes, polygons, keypoints), text (NER, classification), audio (transcription, segmentation), and video (frame-by-frame annotation).

### Built-in user management

Sign-up / login flow handled by Label Studio itself — no extra auth proxy needed in front of the Application Tunnel.

### Bundled PostgreSQL

Single-replica PostgreSQL deployed via the official Bitnami subchart; an external Postgres can be wired in through global.pgConfig for production setups.

### Object storage integration

First-class support for source/target storage backed by S3-compatible object stores, Azure Blob, and GCS — configure through Label Studio after installation.

## Pricing

Additional Nebius infrastructure costs may apply. Use the Nebius Pricing Page (opens in a new tab) to estimate your infrastructure costs.

Self-managed

### Label Studio on Kubernetes

Deploy the upstream HumanSignal Label Studio chart with a bundled PostgreSQL backend; reach the Web UI through a Nebius Application Tunnel.
Free
Charged for resources

Setup time15+ minutes
ScalingManual
MaintenanceSelf-managed (cluster)Deploy (opens in a new tab)
White-glove

### Deploy with a solutions architect
Some applications are easier with a hand on the wheel. Talk to an architect who has deployed this in production.
- Architecture review & sizing
- Hands-on deploy session
- 30 days of follow-up supportTalk to an expert 

## Security & compliance

### Run Label Studio on infrastructure built for AI workloads
Reliable AI infrastructure backed by top-tier NVIDIA GPUs, purpose-built for demanding inference workloads. Multiple deployment methods — virtual machines for full hardware control, Kubernetes for scalable cluster deployments, and managed serverless applications for teams that want inference running without infrastructure overhead.Learn about Nebius AI Cloud 

### Security & compliance, out of the box
Nebius meets a broad set of security and compliance standards. Fine-grained IAM controls, audit logs, and encrypted storage are available out of the box — so teams can meet security requirements without additional tooling.Explore the Trust center 
SOC 2 Type II with HIPAASOC 3ISO/IEC 27001ISO/IEC 27799ISO 22301ISO/IEC 27701ISO/IEC 27018ISO/IEC 27032NIS 2DORACSA STAR Level 1

## Support

### Application support
Provided by HumanSignal. See the documentation and project links above.

### Infrastructure support
Provided by Nebius for the underlying cloud infrastructure.

## More applications from Data

### ClickHouse
by ClickHouse
Data

Fast, open source column oriented DBMS optimized for real time analytics.
Free

### Dynatrace Observability
by Dynatrace
ObservabilityData

Full-stack observability for GenAI and agentic AI workloads.
On request

### Milvus
by Milvus
Data

High-performance, cloud-native vector databases built for scale.
Free

### MLflow
by MLflow
Data

Manage your ML experiments.
Free

### Qdrant
by Qdrant
Data

High-performance, open-source vector database for efficient semantic search.
Free

### +3 more apps in Data
Databases, pipelines, and feature stores.Browse all
