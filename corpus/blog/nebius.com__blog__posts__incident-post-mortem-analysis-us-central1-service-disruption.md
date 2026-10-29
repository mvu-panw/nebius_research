# Incident post-mortem analysis: us-central1 service disruption on September 3, 2025

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-us-central1-service-disruption

Skip to main content

## Incident overviewIncident overview

Nebius experienced a service disruption in the us-central1 region on September 3, 2025 from 16:30 to 18:15 UTC due to routing configuration conflicts that developed between network domains supporting inter-datacenter connectivity.

The incident resulted from the interaction of two independent network changes: routing policy optimization that created a latent vulnerability, followed by security infrastructure extension that triggered routing recomputation and activated a persistent routing loop. This disruption affected multiple customer-facing services and exposed cross-regional service dependencies that amplified the impact beyond the affected region.

Connectivity was restored after targeted network remediation and routing policy adjustments. Other regions remained available.

## ImpactImpact

- Duration: 1 hour 45 minutes (16:30 — 18:15 UTC).

- Geographic scope: Primarily us-central1 region.

- Service architecture impact: Customers experienced inconsistent service quality depending on where they were routed. Our system continued to send users to both working and non-working regional centers, meaning some customers could access services while others couldn’t, based simply on which endpoint they were directed to.

#### Customer-visible effectsCustomer-visible effects

Public API:

- Operations targeting public API endpoint in us-central1 region experienced failures or timeouts; public API endpoints in other regions (e.g., eu-north1) remained available but could not access us-central1 resources.

Console:

- The us-central console failed to communicate with service dependencies in eu-north1, which prevented customers from viewing resources.

- The eu-north1 console remained available but could not display or manage us-central1 resources.

- Quotas in us-central1 could not be listed or changed.

Virtual machine management:

- Creation of new instances in us-central1 failed.

Tenant management:

- New tenant registration was completely unavailable during the disruption; affected tenants were eventually registered after connectivity was restored.

Developer tools:

- SDKs, CLI, Terraform Provider and API Gateway usage targeting us-central1 experienced failures; tooling targeting other regions remained available but with limited us-central1 resource visibility.

## TimelineTimeline

 | Time  (UTC)
 | Event

 | 10:34 — 14:00
 | Routing policy optimization completed on network edge; latent routing vulnerability introduced between network domains. No immediate impact observed.

 | 14:00 — 16:30
 | Network remained stable; routing conflict potential masked by redundancy.

 | 16:30
 | New Firewall nodes onboarding triggered routing recomputation; persistent routing loop activated. First customer‑visible symptoms in us‑central1.

 | 16:30 +
 | Service disruption began affecting us-central1 region.

 | 16:50
 | Incident declared; initial scope confirmed and communications initiated.

 | 17:06
 | Status page updated to reflect ongoing incident.

 | 17:10
 | Triage localized the issue to routing instabilities in inter-datacenter path.

 | 17:22
 | Engineering analysis confirmed persistent routing loop between network domains.

 | 17:27
 | Initial rollback attempts executed without restoring service.

 | 17:30 — 18:15
 | Mitigation actions (routing policy adjustments and targeted network remediation) applied.

 | 18:15
 | Routing loop eliminated; regional connectivity restored; Console functionality recovered.

 | 18:30
 | All known customer-visible impacts resolved.

 | 18:33
 | Incident fully mitigated.

## Root causeRoot cause

A sequence of network changes created conditions for a persistent routing loop between the Backbone and Data Center network domains supporting us-central1 operations. A prior routing policy optimization had introduced a latent configuration that allowed cross-domain routing conflicts.

Although these changes were tested, the issue was not observed because not all production factors were represented in the reduced-scale lab environment. Protection mechanisms intended to prevent such routing behavior were present but did not work under these specific circumstances.

During a subsequent security infrastructure extension, routing recomputation caused different network devices to prefer opposite domain paths for the same network prefixes, completing the routing loop.

This resulted in unstable control‑plane behavior, misleading diagnostics, and incorrect next‑hop resolution on the inter‑facility path supporting us‑central1.

Service architecture vulnerability: the network partition exposed critical cross-regional service dependencies that significantly amplified the incident impact. Several us-central1 services maintained dependencies on eu-north1, transforming a network connectivity issue into broader service unavailability. Additionally, our geo-IP load balancing system continued directing customers to both regional endpoints without awareness of the network partition, resulting in inconsistent service experiences.

## Incident response outcomesIncident response outcomes

This incident highlighted several critical areas for improvement in our network and service architecture:

Network infrastructure lessons:

- 

Routing policy validation: network safeguards were insufficient to prevent cross-domain routing conflicts, allowing the formation of persistent routing loops

- 

Latent issue detection: network redundancy successfully maintained service during normal operations but masked critical routing vulnerabilities until triggered by subsequent changes

- 

Network monitoring: routing instability detection took approximately 20 minutes, indicating gaps in real-time network health visibility

Service architecture lessons:

- 

Cross-regional dependencies: multiple us-central1 services retained dependencies on eu-north1 infrastructure, creating service architecture vulnerabilities that amplified network incidents

- 

Load balancing resilience: customer‑facing experiences lacked sufficient failover; users were not automatically redirected to a healthy Console during the partition.

- 

Regional service isolation: varying service impacts demonstrated the critical need for independent regional operation capabilities during network partitions

- 

Tenant registration architecture: cross-region quorum requirements created unnecessary single points of failure for customer onboarding processes

## Post-incident action planPost-incident action plan

We are implementing comprehensive improvements to prevent similar incidents and reduce customer impact.

Network infrastructure improvements:

- Implement stricter split-horizon controls between routing domains to prevent cross-domain routing cycles.

- Enhance cross-region connectivity alerting to detect and alert on inter-facility loss.

- Deploy automated pre-deployment routing policy validation and network simulation tools.

- Enhance routing stability monitoring with automated churn detection and alerting for unusual routing patterns.

Service architecture improvements:

- Enable geo-DNS failover for Console to automatically redirect users to healthy regional endpoints during network partitions.

- Reduce cross-regional service dependencies, enabling tenant creation and core operations without single control-plane path reliance.

- Regionalize shared Console dependencies to eliminate single-region dependencies for user-facing experiences.

- Improve tenant registration to operate without all-regions quorum requirement.

We sincerely apologize for the service disruption and any inconvenience this caused. Reliability remains our highest priority, and we are committed to implementing these comprehensive improvements to prevent similar incidents.

Nebius team

Contents

- 

Incident overview

- 

Impact

- Customer-visible effects

- 

Timeline

- 

Root cause

- 

Incident response outcomes

- 

Post-incident action plan

Sign in to save this post
Sign In
