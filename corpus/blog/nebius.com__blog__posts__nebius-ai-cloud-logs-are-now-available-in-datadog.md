# Nebius Cloud Logs are now available in Datadog: Trace AI incidents across every layer

Source: https://nebius.com/blog/posts/nebius-ai-cloud-logs-are-now-available-in-datadog

Skip to main content

Debugging a production AI service usually means playing detective across half a dozen tools, and the trail goes cold every time you switch consoles. That’s why we’re announcing a new integration with Datadog to close that gap. Logs from core Nebius AI Cloud services now stream straight into Datadog Log Management. So if your team’s already on Datadog, you can investigate your Nebius workloads alongside the rest of your stack, in the tool you already live in — and Nebius AI Cloud Observability remains available, of course.

The integration covers Nebius Cloud Compute, Managed Service for Kubernetes, Applications, Managed Service for PostgreSQL, Managed Service for MLflow and Kubernetes control-plane events. In other words, Datadog shows the full path an incident can take through an AI stack, not just the surface where it first shows up, saving teams time during incidents.

## The challenge: AI incidents cross layers, but investigation gets splitThe challenge: AI incidents cross layers, but investigation gets split

A production AI incident rarely announces where it started. An inference endpoint slows down. A deployment rolls out cleanly, then traffic errors climb. A model job behaves differently after a configuration change. The cause might be in the application or compute layer, or in a service like Kubernetes, PostgreSQL, or MLflow.

When those signals live in separate tools, you lose valuable time reconstructing context instead of fixing the issue: switching consoles, comparing timestamps, copying identifiers and rebuilding the story by hand. AI workloads need to show up in the operating workflow your team already uses for search, alerting, investigation and incident response.

## The solution: every layer visible in DatadogThe solution: every layer visible in Datadog

The new Datadog integration with Nebius AI Cloud streams logs from your Nebius tenant directly into Datadog Log Management. Instead of treating Nebius as a separate investigation path, you can bring your Nebius workload logs into the same Datadog environment you use for the rest of your infrastructure and applications: application logs, Kubernetes events, PostgreSQL logs, MLflow logs and Kubernetes control plane activity.

With the integration, your team can now work more efficiently:

- Investigate an inference or application issue without moving Nebius logs into a separate workflow

- Correlate Kubernetes events, control plane activity and service logs alongside the rest of the Datadog environment

- Bring in PostgreSQL and MLflow logs when a workload issue may involve data services or ML lifecycle context

- Apply existing Datadog practices for dashboards, alerts, on-call workflows and incident response to act on Nebius logs

During live investigations, that’s the difference between chasing a problem across four consoles and following it from symptom to root cause in one. Instead of losing those first critical minutes of an incident reassembling context across separate tools, you get a full view of your Nebius AI Cloud logs right inside Datadog, alongside the rest of your tooling logs.

## Observe the way that works for youObserve the way that works for you

If your team already lives in Datadog, you can route Nebius logs into the platform you already use. If you prefer to operate from Nebius directly, we still have Nebius AI Cloud Observability built into the product. This integration is another path to observability, not a replacement.

## Get started todayGet started today

Nebius AI Cloud is available now in the Datadog Integrations Catalog. Simply configure the parent Nebius Cloud integration, then use service-specific tiles for Compute, Kubernetes, Applications, PostgreSQL and MLflow.

Want to learn more? Here are the key resources to get your integration set up today!

- Datadog documentation on Nebius

- Nebius on Datadog Integration Catalog

- Datadog’s blog on the integration

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

David Schulman
Senior Director of Partner Marketing

Contents

- The challenge: AI incidents cross layers, but investigation gets split

- The solution: every layer visible in Datadog

- Observe the way that works for you

- Get started today

## See also

### 

Nebius and LangChain partner to power production-grade AI agents on open models

Nebius and LangChain have partnered to integrate Nebius Token Factory with LangChain’s Deep Agents. The integration, combined with LangChain’s existing Tavily integration, gives teams building on LangChain a direct path to run agent workloads on production-grade AI infrastructure with open-source models, dedicated endpoints, real-time search and full control over cost and data.

May 13, 2026
6 mins to read

### 

Game on! UFB and Nebius power the future of robotics

We are thrilled to announce that Nebius is the official technology partner for Season 1 of Ultimate Fighting Bots (UFB)’s Humanoid Sports League — the world’s first multi-format competition platform for physical AI. The two companies will pioneer the use robots by coupling UFB’s growing platform for humanoids with Nebius’s cloud solution for physical AI.

May 13, 2026
9 mins to read

### 

Introducing the Nebius Agents Blueprint: open architecture for production-ready AI agents

Today we’re introducing the Nebius Agents Blueprint, an open reference architecture for building, operating, and continuously improving AI agents in production. This post covers the six-component composable stack — inference, orchestration, retrieval, grounding, observability, and simulation — and the case study behind it: a compliance audit agent that achieved 72% lower cost and 20% higher precision over a GPT-based prototype by improving the system, not the model.

June 10, 2026
6 mins to read

Sign in to save this post
Sign In
