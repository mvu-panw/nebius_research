# Apache Flink cluster — Nebius applications

Source: https://nebius.com/applications/flink-cluster

Skip to main content

# Apache Flink cluster
by Apache
Orchestration

Apache Flink is a framework and distributed processing engine for stateful computations over unbounded and bounded data streams. This Helm chart deploys a Flink 1.20 session cluster — one JobManager plus N TaskManagers — on top of Managed Kubernetes, using upstream apache/flink container images straight from the Apache project. The JobManager Web UI is exposed through a secure tunnel and protected by HTTP Basic Auth, so the cluster overview is reachable from your browser without exposing the cluster directly to the internet. Job submission stays on the cluster-internal RPC port (<release>-jobmanager:6123), reachable from any pod in the namespace.Deploy on Nebius
Free

Deployment methods1
Setup timefrom 15 minutesDeploy (opens in a new tab)
Sign-in required to deploy. Free to browse and read docs.

Vendor:Apache

Additional links
- Apache Flink website (opens in a new tab)
- Apache Flink documentation (opens in a new tab)
- Apache Flink on Docker Hub (opens in a new tab)
- Apache Flink on GitHub (opens in a new tab)

Licenses
- Apache Flink Helm chartApache License 2.0
- Apache FlinkApache License 2.0
- nginx (auth proxy)BSD 2-Clause

## Key features

### Upstream Apache images

Container images come straight from docker.io/apache/flink — not a third-party rebuild.

### JobManager + TaskManager topology

Submit streaming and batch jobs over the standalone protocol on port 6123 from any pod in the namespace; the JobManager coordinates a fleet of long-running TaskManagers.

### Web UI behind Basic Auth

JobManager Web UI exposed through a secure HTTP/2 tunnel with HTTP Basic Auth — set or generate a password at install time.

### Stateful fault tolerance

Checkpoints and savepoints give resilient stateful jobs out of the box; configure your storage backend via Helm overrides.

## Pricing

Additional Nebius infrastructure costs may apply. Use the Nebius Pricing Page (opens in a new tab) to estimate your infrastructure costs.

Self-managed

### Apache Flink cluster on Kubernetes

Deploy a long-running Apache Flink session cluster (JobManager + TaskManagers) on Kubernetes, with the JobManager Web UI exposed through a secure tunnel and protected by HTTP Basic Auth.
Free
Charged for resources

Setup time15+ minutes
ScalingAuto
MaintenanceSelf-managed (cluster)Deploy (opens in a new tab)
White-glove

### Deploy with a solutions architect
Some applications are easier with a hand on the wheel. Talk to an architect who has deployed this in production.
- Architecture review & sizing
- Hands-on deploy session
- 30 days of follow-up supportTalk to an expert 

## Security & compliance

### Run Apache Flink cluster on infrastructure built for AI workloads
Reliable AI infrastructure backed by top-tier NVIDIA GPUs, purpose-built for demanding inference workloads. Multiple deployment methods — virtual machines for full hardware control, Kubernetes for scalable cluster deployments, and managed serverless applications for teams that want inference running without infrastructure overhead.Learn about Nebius AI Cloud 

### Security & compliance, out of the box
Nebius meets a broad set of security and compliance standards. Fine-grained IAM controls, audit logs, and encrypted storage are available out of the box — so teams can meet security requirements without additional tooling.Explore the Trust center 
SOC 2 Type II with HIPAASOC 3ISO/IEC 27001ISO/IEC 27799ISO 22301ISO/IEC 27701ISO/IEC 27018ISO/IEC 27032NIS 2DORACSA STAR Level 1

## Support

### Application support
Provided by Apache. See the documentation and project links above.

### Infrastructure support
Provided by Nebius for the underlying cloud infrastructure.

## More applications from Orchestration

### AI Orchestration
by Union.ai
OrchestrationDevelopment

The AI development layer of your tech stack.
On request

### Anyscale
by Anyscale
Orchestration

Launch and manage Ray clusters of any size using resources of your preferred cloud provider.
Free

### Apache Spark cluster
by Apache
Orchestration

A long-running Apache Spark standalone cluster on Kubernetes with secure Web UI access.
Free

### Argo CD
by Argo Project
OrchestrationInfrastructure

GitOps tool for declarative, automated Kubernetes app deployment and sync.
Free

### ClearML Agent
by ClearML
Orchestration

A ClearML Agent for scaling AI/ML workflows on multiple GPU machines.
Free

### +13 more apps in Orchestration
Pipelines, schedulers, and workflow engines.Browse all
