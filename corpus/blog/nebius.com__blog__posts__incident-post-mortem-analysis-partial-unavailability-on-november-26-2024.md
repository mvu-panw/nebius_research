# Incident post-mortem analysis: Partial unavailability on November 26, 2024

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-partial-unavailability-on-november-26-2024

Skip to main content

## Incident overviewIncident overview

A faulty release in the VM recovery sequence triggered a recovery operation causing 282 virtual machines (VMs) in the eu-north1 region to restart. 164 of these VMs experienced extended downtime requiring manual intervention to restore operation. This caused interruptions in customer workloads.

We sincerely apologize to all customers affected by this incident. We are committed to learning from this and are taking concrete steps to ensure it doesn’t happen again.

## ImpactImpact

- 282 VMs restarted. 196 of those could not successfully restart and got stuck.

- 32 VMs were restarted or deleted by users.

- 164 VMs failed to start and remained offline for approximately 2-3 hours.

## TimelineTimeline

 | Time (UTC+1)
 | Event

 | 13:48
 | Deployment of the new release to eu-north1. The chain of events leading to the incident started.

 | 13:48
 | Mass VM restart: 282 VMs affected.

 | 13:50
 | 86 VMs successfully restarted automatically.

 | 14:03
 | Alerts about the large number of stuck VMs were triggered and the issue was reported internally. First customer report received via Slack; the issue was classified as an incident.

 | 14:21
 | The team started analyzing the reasons of what was happening and how to approach mitigation of the impact without making it worse.

 | 15:00
 | Root cause identified and mitigation strategy determined.

 | 15:00 — 15:37
 | Researched ways to mitigate the incident without causing further issues and created a mitigation plan, while testing the solution on individual VMs. By this time, 32 VMs had been either recovered by users or deleted.

 | 15:37 — 16:39
 | 163 VMs recovered in batches.

 | 17:40
 | Verified successful startup of all affected VMs. Incident is resolved.

## Root causeRoot cause

To provide a clear understanding of the events that led to this incident, we will outline some internal processes that contributed to the issue.

The Compute API service encountered a problem where it incorrectly assumed certain VMs were not operational. This was caused by a flawed assumption about the order of event processing in the system responsible for tracking resource updates. As a result, the Compute API mistakenly identified some VMs as missing and initiated unnecessary recovery operations.

Another contributing factor was that by the time of the incident the systems were not optimized for the number of recovery operations causing VMs to become stuck.

## Mitigation actionsMitigation actions

We started by identifying the root cause of the incident and halting all automatic recovery operations to prevent any further impact.

Next, we categorized the affected VMs into two groups: those that had successfully restarted and those that were stuck and required manual intervention.

To resolve the issue, we developed and thoroughly tested mitigation procedures. These involved stopping the affected VMs to interrupt all stuck processes and then restarting them in controlled batches to ensure a successful restart

Finally, these mitigation procedures were successfully applied to all VMs requiring manual recovery, completing the process.

## Incident response outcomesIncident response outcomes

Our internal monitoring systems detected an issue when some VMs got stuck. This triggered immediate phone calls to the on-call engineers, and within 15 minutes, we assessed the impact, formally declared the incident, assembled the response team, and began mitigation efforts. Thanks to the team’s quick action, we identified the root cause within 35 minutes.

The recovery process followed a staged approach that proved effective but required manual intervention and close monitoring to ensure reliable recovery. This incident highlighted that we needed better automation of recovery procedures, which could significantly enhance response times in similar situations.

## Post-incident action planPost-incident action plan

Our post-incident action plan focuses on improving three key areas: pre-deployment validation, operations, and communications.

For pre-deployment validation, we will introduce additional testing for recovery scenarios and enforce stricter validation of VM state changes.

In operations, we plan to add rate limiting for recovery processes, enhance monitoring and anomaly detection in VM activities, and strengthen deployment procedures with additional safety checks.

In communications, we aim to ensure faster escalation for large-scale VM events, improve customer notifications and engagement, and refine internal communication protocols to streamline our incident response efforts.

Nebius team

Contents

- Incident overview

- Impact

- Timeline

- Root cause

- Mitigation actions

- Incident response outcomes

- Post-incident action plan

Sign in to save this post
Sign In
