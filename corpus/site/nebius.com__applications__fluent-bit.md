# Fluent Bit — Nebius applications

Source: https://nebius.com/applications/fluent-bit

Skip to main content

# Fluent Bit
by Fluent Inc.
Observability

Deploys the upstream fluent/fluent-bit Helm chart from the CNCF Fluent project. Fluent Bit is a fast, lightweight log processor and forwarder designed for cloud-native environments. By default this product runs as a DaemonSet (one pod per node) that picks up container logs from each node’s kubelet and ships them to the configured outputs. The plugin ecosystem supports inputs from systemd, kubernetes events, syslog, and outputs to Loki, Elasticsearch, Kafka, S3, Splunk, and more.Deploy on Nebius
Free

Deployment methods1
Setup timefrom 10 minutesDeploy Fluent Bit (opens in a new tab)
Sign-in required to deploy. Free to browse and read docs.

Vendor:Fluent Inc.

Additional links
- Fluent Bit website (opens in a new tab)
- Fluent Bit documentation (opens in a new tab)
- Fluent Bit on GitHub (opens in a new tab)
- fluent/helm-charts (opens in a new tab)

Licenses
- Fluent Bit Helm chartApache License 2.0
- Fluent BitApache License 2.0

## Key features

### Upstream CNCF chart

Vendored from fluent/fluent-bit — the canonical chart maintained by the CNCF Fluent project.

### DaemonSet log collection

One pod per node by default; tails container logs from /var/log/containers/* and the journald socket.

### Plugin ecosystem

Configurable via config.inputs / config.outputs Helm values — Loki, Elasticsearch, Kafka, S3, Splunk, and many more outputs available out of the box.

### Prometheus-ready

Built-in metrics endpoint on port 2020; optional ServiceMonitor integrates with the Prometheus Operator.

## Pricing

Additional Nebius infrastructure costs may apply. Use the Nebius Pricing Page (opens in a new tab) to estimate your infrastructure costs.

Self-managed

### Fluent Bit on Kubernetes

Deploy the upstream Fluent Bit chart from CNCF Fluent project to forward container logs from your Kubernetes cluster.
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

### Run Fluent Bit on infrastructure built for AI workloads
Reliable AI infrastructure backed by top-tier NVIDIA GPUs, purpose-built for demanding inference workloads. Multiple deployment methods — virtual machines for full hardware control, Kubernetes for scalable cluster deployments, and managed serverless applications for teams that want inference running without infrastructure overhead.Learn about Nebius AI Cloud 

### Security & compliance, out of the box
Nebius meets a broad set of security and compliance standards. Fine-grained IAM controls, audit logs, and encrypted storage are available out of the box — so teams can meet security requirements without additional tooling.Explore the Trust center 
SOC 2 Type II with HIPAASOC 3ISO/IEC 27001ISO/IEC 27799ISO 22301ISO/IEC 27701ISO/IEC 27018ISO/IEC 27032NIS 2DORACSA STAR Level 1

## Support

### Application support
Provided by Fluent Inc. See the documentation and project links above.

### Infrastructure support
Provided by Nebius for the underlying cloud infrastructure.

## More applications from Observability

### Dynatrace Observability
by Dynatrace
ObservabilityData

Full-stack observability for GenAI and agentic AI workloads.
On request

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

### Grafana solution by Nebius
by Grafana Labs
Observability

A ready-to-use solution to work with Nebius Monitoring and Logging services.
Free

### +7 more apps in Observability
Monitoring, tracing, and evaluation tools.Browse all
