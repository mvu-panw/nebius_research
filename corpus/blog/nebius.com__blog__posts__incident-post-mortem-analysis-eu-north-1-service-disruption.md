# Incident post-mortem analysis: eu-north-1 service disruption on February 26, 2026

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-eu-north-1-service-disruption

Skip to main content

On February 26, 2026, a power infrastructure fault in the eu-north-1 region caused a brief interruption of power to a subset of compute hosts. This resulted in simultaneous host restarts and temporary unavailability of some customer workloads. While core systems began recovering automatically, additional recovery constraints in compute and storage layers extended the time required to fully restore normal operation for all affected resources.

## ImpactImpact

A subset of customers with resources in eu-north-1 experienced:

- Failures and automatic restarts of virtual machines;

- Temporary inability to start certain virtual machines;

- In some cases, temporary loss of access to attached storage volumes during recovery;

- One managed database workload experienced approximately 6 minutes of partial unavailability, followed by a degraded state before stabilizing.

The impact was limited to resources located in eu-north-1. Other regions were not affected.

## Timeline (CET)Timeline (CET)

2026-02-26 15:16 — A short circuit occurred in cabling supplying cooling infrastructure in eu-north-1. A high fault current (recorded above 10kA at protection level) triggered UPS overcurrent protection. The UPS output breaker opened due to the high current before the transfer to external bypass mode was completed. This resulted in a brief interruption of power to a subset of compute hosts.

2026-02-26 15:16–15:20 — Affected hosts rebooted. Customer-facing symptoms began, including virtual machine restarts and service unavailability.

2026-02-26 15:40 — The incident was formally declared and coordinated response initiated.

2026-02-26 ~16:00–18:00 — Initial triage confirmed the power infrastructure event as the triggering cause. Large-scale host recovery and virtual machine restarts were underway. Recovery throughput was slower than expected under mass-restart conditions.

2026-02-26 19:25 — Storage attachment conflicts were identified as a contributing factor preventing some virtual machines from starting.

2026-02-26 23:00–02:00 (Feb 27) — Corrective operational actions were applied to resolve storage attachment conflicts and accelerate recovery.

2026-02-27 02:30 — The majority of customer-facing impact had been mitigated; remaining isolated cases were being handled individually.

2026-02-27 06:37 — Data center inspection confirmed the root electrical cause: a short circuit in cabling supplying cooling systems, which resulted in high overcurrent and triggered UPS protection.

2026-02-27 09:49 — UPS operation in eu-north-1 was restored to normal mode after inspection and validation.

2026-02-27 13:34 — All identified customer-facing impact in eu-north-1 was resolved.

## Root causeRoot cause

The incident was triggered by a short circuit in cabling supplying cooling components in the eu-north-1 region. The fault generated a high overcurrent condition (recorded above 10kA), which activated UPS protection mechanisms.

During the protection sequence, the UPS output breaker opened due to the high current before the transfer to external bypass mode was completed.

Switching a UPS to bypass mode should normally occur without interrupting the load. In this incident, the power interruption occurred due to the output breaker opening during the fault condition, rather than the bypass transfer itself.

This resulted in a brief interruption of power to a subset of compute hosts and caused their simultaneous restart.

Recovery time was extended by two contributing factors:

- Throughput limitations in compute control-plane recovery operations during mass virtual machine restarts.

- Storage attachment state inconsistencies after host reboots, which required corrective operational actions before certain virtual machines could successfully start or regain full disk access.

## Incident response outcomesIncident response outcomes

This incident demonstrated that while power protection mechanisms operated as designed to prevent hardware damage, a region-level restart scenario creates complex cross-layer recovery conditions.

We identified that large-scale simultaneous restarts require higher recovery throughput capacity in compute control-plane components. We also confirmed that storage state persistence across host reboots can lead to attachment conflicts that must be explicitly reconciled during recovery.

## Post-incident action planPost-incident action plan

We are implementing the following improvements:

- 

Review and refine electrical protection selectivity and configuration in eu-north-1 to reduce the likelihood of similar region-level power interruptions.

- 

Improve compute recovery throughput and behavior under mass-restart scenarios.

- 

Refine storage state handling after host reboots to prevent stale attachment conflicts.

- 

Enhance monitoring and alerting across power, compute and storage layers to enable faster understanding of the incident scope and specific failure details during cross-layer incidents.

We are committed to improving platform resilience, observability and recovery characteristics and appreciate our customers’ patience during this event.

Nebius team

Contents

- Incident overview

- Impact

- Timeline (CET)

- Root cause

- Incident response outcomes

- Post-incident action plan

Sign in to save this post
Sign In
