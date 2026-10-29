# [Security Advisory] eMudhra intermediate certificates compromise

Source: https://nebius.com/blog/posts/emudhra-intermediate-certificates-compromise

Skip to main content

## What happenedWhat happened

The private keys of eight eMudhra intermediate certificate authorities (CAs) have been compromised. A flaw in key generation makes it possible to recover these keys from publicly available certificates. An attacker could use them to create fraudulent certificates and impersonate legitimate websites or services to applications that still trust the affected CAs. Details are available on the incident information page.

## Nebius responseNebius response

### Compute instancesCompute instances

The latest versions of Nebius Compute virtual machine images no longer trust the compromised certificate chains.

Please re-create your instances using the latest VM image to ensure protection.

### Managed KubernetesManaged Kubernetes

New Managed Kubernetes node groups will use the updated worker node version that doesn’t contain compromised CA certificates.

Nebius Managed Kubernetes supports only Ubuntu nodes. Mitigations suggested below are based on the Canonical recommendations.

For existing clusters, choose and apply the mitigation that best fits how your node groups are configured and used:

- 

Recommended approach — upgrade node groups. See instructions in Approach 1: upgrade node groups section.

- 

Mitigation for older infrastructure versions — cloud-init user data. See instructions in Approach 2: cloud-init user data.

- 

Temporary mitigation — DaemonSet. See instructions in Approach 3: temporary DaemonSet.

IMPORTANT: Customers are responsible for reviewing their workloads and implementing appropriate mitigation measures.

### Soperator clustersSoperator clusters

We updated the certificate trust bundle in Soperator clusters’ JailFS to the latest available version, preventing workloads on worker and login nodes from trusting the affected CAs.

In parallel, we are updating the images used by Soperator itself. Applying these updates requires downtime, so upgrades will be scheduled with customer consent. You can request a priority upgrade, and we will do our best to accommodate your request.

### Managed PostgreSQLManaged PostgreSQL

Newly created clusters will include all required fixes. All existing clusters will be updated during the scheduled maintenance windows on October 29 and November 3, 2026. Alternatively, you can create a new cluster and restore data from a backup or contact Customer support.

### Managed SkyPilotManaged SkyPilot

Newly created clusters will include all required fixes. For existing clusters, the underlying components will be updated during the scheduled maintenance windows on October 29 and November 3, 2026. To upgrade SkyPilot, click “Update” in the Console UI.

### Managed MLflowManaged MLflow

Newly created clusters will include all required fixes. For existing clusters, the underlying components will be updated during the scheduled maintenance windows on October 29 and November 3, 2026. To upgrade the MLflow version on existing clusters, re-create them or contact Customer support.

### Serverless Devlabs, Endpoints and JobsServerless Devlabs, Endpoints and Jobs

Mitigations are included in the latest versions of Nebius-managed Serverless images. Please stop and restart existing Endpoints and Devlabs to apply the updates. Jobs are short-lived, and newly created Jobs include the fixes.

Some third-party template images are still awaiting fixes and will be updated as soon as upstream providers release them.

## Nebius Token FactoryNebius Token Factory

We updated the affected certificate trust stores and software dependencies for all user-facing components of the Token Factory infrastructure. Internal components and inference engines will be updated within the next week.

## TavilyTavily

Tavily’s public endpoints use certificates that are not affected by the eMudhra CA incident, so no customer configuration changes are required to use Tavily’s hosted APIs. Mitigations have already been applied to Tavily’s Search API. Updates to the remaining internal components are in progress, with some dependent on fixed releases from upstream vendors.

Note

We have not identified evidence of unauthorized access to Nebius, Token Factory or Tavily systems or customer data related to this incident.

We strongly recommend applying these mitigations as soon as possible.

Nebius team

Contents

- 

What happened

- 

Nebius response

- Compute instances

- Managed Kubernetes

- Soperator clusters

- Managed PostgreSQL

- Managed SkyPilot

- Managed MLflow

- Serverless Devlabs, Endpoints and Jobs

- 

Nebius Token Factory

- 

Tavily

Sign in to save this post
Sign In
