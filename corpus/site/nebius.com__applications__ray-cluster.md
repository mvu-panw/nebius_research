# Ray Cluster — Nebius applications

Source: https://nebius.com/applications/ray-cluster

Skip to main content

# Ray Cluster
by Ray
OrchestrationInfrastructure

During installation, you can select the number and parameters of worker groups, configure autoscaling, and set up the head node. Alternatively, you may provide your own configuration in YAML format. Optionally, you can install the KubeRay Operator, which is required for Ray Cluster to function properly. You may also optionally install the Kubernetes Prometheus Stack, which integrates with the KubeRay Operator and Ray Cluster for monitoring and observability. By default, the installation parameters enable autoscaling and set the number of worker replicas to 0. This means that as soon as a task is submitted, Ray Cluster will automatically create a worker. Once the task is finished, the worker will be deleted after a short grace period if it is not used anymore. Ray Cluster autoscaling and Managed Service for Kubernetes cluster work together, so if no suitable node is available, the Kubernetes cluster autoscaler can provision one.Deploy on Nebius
Free

Deployment methods1
Setup timefrom 20 minutesDeploy Ray Cluster (opens in a new tab)
Sign-in required to deploy. Free to browse and read docs.

Vendor:Ray

Additional links
- Ray website (opens in a new tab)
- Ray documentation (opens in a new tab)
- Ray GitHub (opens in a new tab)
- KubeRay on GitHub (opens in a new tab)

Licenses
- Ray Cluster Helm chartApache License 2.0
- KubeRay OperatorApache License 2.0
- RayApache License 2.0
- kube-prometheus-stack (optional dependency)Apache License 2.0

## Key features

### Flexible cluster configuration

Configure head and worker groups or provide custom YAML.

### Autoscaling support

Scales Ray workers with workload demand and integrates with Kubernetes autoscaling.

### Node group targeting

Supports node selectors and custom resources for precise scheduling.

### Optional monitoring stack

Can integrate kube-prometheus-stack with Grafana dashboards.

## Pricing

Additional Nebius infrastructure costs may apply. Use the Nebius Pricing Page (opens in a new tab) to estimate your infrastructure costs.

Self-managed

### Ray Cluster on Kubernetes

Deploy Ray clusters on Kubernetes with configurable worker groups and autoscaling.
Free
Charged for resources

Setup time20+ minutes
ScalingAuto
MaintenanceSelf-managed (cluster)Deploy (opens in a new tab)
White-glove

### Deploy with a solutions architect
Some applications are easier with a hand on the wheel. Talk to an architect who has deployed this in production.
- Architecture review & sizing
- Hands-on deploy session
- 30 days of follow-up supportTalk to an expert 

## Security & compliance

### Run Ray Cluster on infrastructure built for AI workloads
Reliable AI infrastructure backed by top-tier NVIDIA GPUs, purpose-built for demanding inference workloads. Multiple deployment methods — virtual machines for full hardware control, Kubernetes for scalable cluster deployments, and managed serverless applications for teams that want inference running without infrastructure overhead.Learn about Nebius AI Cloud 

### Security & compliance, out of the box
Nebius meets a broad set of security and compliance standards. Fine-grained IAM controls, audit logs, and encrypted storage are available out of the box — so teams can meet security requirements without additional tooling.Explore the Trust center 
SOC 2 Type II with HIPAASOC 3ISO/IEC 27001ISO/IEC 27799ISO 22301ISO/IEC 27701ISO/IEC 27018ISO/IEC 27032NIS 2DORACSA STAR Level 1

## Support

### Application support
Provided by Ray. See the documentation and project links above.

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

### Apache Flink cluster
by Apache
Orchestration

A long-running Apache Flink session cluster on Kubernetes with secure Web UI access.
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

### +13 more apps in Orchestration
Pipelines, schedulers, and workflow engines.Browse all
