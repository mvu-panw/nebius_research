# kube-state-metrics — Nebius applications

Source: https://nebius.com/applications/kube-state-metrics

Skip to main content

# kube-state-metrics
by Kubernetes SIGs
Observability

Deploys the upstream prometheus-community/kube-state-metrics chart from Kubernetes SIGs. kube-state-metrics is a simple service that listens to the Kubernetes API server and generates metrics about the state of the objects (Deployments, Pods, Nodes, Services, and more). It focuses on the overall state of the cluster rather than the health of individual components, and is designed to be scraped by Prometheus.Deploy on Nebius
Free

Deployment methods1
Setup timefrom 10 minutesDeploy kube-state-metrics (opens in a new tab)
Sign-in required to deploy. Free to browse and read docs.

Vendor:Kubernetes SIGs

Additional links
- kube-state-metrics on GitHub (opens in a new tab)
- prometheus-community Helm chart (opens in a new tab)
- Prometheus monitoring overview (opens in a new tab)

Licenses
- kube-state-metrics Helm chartApache License 2.0
- kube-state-metricsApache License 2.0

## Key features

### Upstream Kubernetes SIGs chart

Vendored from prometheus-community/kube-state-metrics — the canonical chart used across the Kubernetes ecosystem.

### Object state metrics

Exposes metrics derived from Kubernetes objects and their current state on /metrics (port 8080) and /metrics (telemetry on port 8081).

### Prometheus-ready endpoints

Optional ServiceMonitor integrates directly with the Prometheus Operator (set prometheus.monitor.enabled=true).

### Low-overhead observability

Tracks cluster state changes without instrumenting individual workloads.

## Pricing

Additional Nebius infrastructure costs may apply. Use the Nebius Pricing Page (opens in a new tab) to estimate your infrastructure costs.

Self-managed

### kube-state-metrics on Kubernetes

Deploy the upstream prometheus-community/kube-state-metrics chart to expose Kubernetes object state as Prometheus metrics.
Free
Charged for resources

Setup time10+ minutes
ScalingAuto
MaintenanceSelf-managed (cluster)Deploy (opens in a new tab)
White-glove

### Deploy with a solutions architect
Some applications are easier with a hand on the wheel. Talk to an architect who has deployed this in production.
- Architecture review & sizing
- Hands-on deploy session
- 30 days of follow-up supportTalk to an expert 

## Security & compliance

### Run kube-state-metrics on infrastructure built for AI workloads
Reliable AI infrastructure backed by top-tier NVIDIA GPUs, purpose-built for demanding inference workloads. Multiple deployment methods — virtual machines for full hardware control, Kubernetes for scalable cluster deployments, and managed serverless applications for teams that want inference running without infrastructure overhead.Learn about Nebius AI Cloud 

### Security & compliance, out of the box
Nebius meets a broad set of security and compliance standards. Fine-grained IAM controls, audit logs, and encrypted storage are available out of the box — so teams can meet security requirements without additional tooling.Explore the Trust center 
SOC 2 Type II with HIPAASOC 3ISO/IEC 27001ISO/IEC 27799ISO 22301ISO/IEC 27701ISO/IEC 27018ISO/IEC 27032NIS 2DORACSA STAR Level 1

## Support

### Application support
Provided by Kubernetes SIGs. See the documentation and project links above.

### Infrastructure support
Provided by Nebius for the underlying cloud infrastructure.

## More applications from Observability

### Dynatrace Observability
by Dynatrace
ObservabilityData

Full-stack observability for GenAI and agentic AI workloads.
On request

### Fluent Bit
by Fluent Inc.
Observability

Lightweight CNCF log processor and forwarder for Kubernetes.
Free

### Grafana
by Grafana Labs
Observability

Deploy a secure, Grafana instance in the cloud with no setup or maintenance.
Free

### Grafana and Prometheus
by Grafana Labs
Observability

Collect, monitor, and visualize metrics with Prometheus and Grafana.
Free

### Grafana Loki
by Grafana Labs
Observability

Scalable, highly available log aggregation.
Free

### +7 more apps in Observability
Monitoring, tracing, and evaluation tools.Browse all
