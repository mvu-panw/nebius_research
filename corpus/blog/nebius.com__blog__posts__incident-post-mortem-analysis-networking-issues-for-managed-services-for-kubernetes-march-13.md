# Incident post-mortem analysis: networking issues for Managed Services for Kubernetes on March 13, 2025

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-networking-issues-for-managed-services-for-kubernetes-march-13

Skip to main content

## Incident overviewIncident overview

On March 13, 2025, a release of one of the control plane components of the VPC service in the eu-west1 region caused massive networking issues for clients' pods of Managed Services for Kubernetes.

There was a bug in the processing of the network configuration data that caused the malfunctioning of the IP alias (prefix delegation) mechanism of virtual machines' network interfaces. This mechanism is necessary for the proper functioning of the Managed Services for Kubernetes pod network. While the root cause bug was introduced to production with a much earlier release, the release on March 13 had a new feature that triggered the bug. Due to this complication, the initial rollback was ineffective and the incident mitigation took longer.

The eu-north1 region was not affected by this incident.

## ImpactImpact

Practically every pod of Managed Services for Kubernetes running in eu-west1 experienced the loss of connectivity for at least some time between 13:36 and 18:11 UTC.

## TimelineTimeline

 | Time (UTC)
 | Event

 | 13:36
 | Start of the canary deployment to eu-west1.

 | 14:35
 | Start of the deployment to all other nodes in eu-west1.

 | 15:13
 | The Nebius team becomes aware of the issue.

 | 15:30
 | On-call engineers initiate the rollback of the release.

 | 15:32
 | The incident response team is assembled. Full-scale incident response procedures are initiated.

 | 16:00
 | It becomes clear that the rollback didn’t help and the root cause is more complex.

 | 16:20
 | The team establishes that the issue is related to IP aliases, but the bigger picture remains unclear.

 | 16:41
 | The team finds out that a manual restart of the component on one problematic node at a time resolves the issue on this particular node. The team initiates the restart of the component on all the affected nodes, but one node at a time.

 | 17:36
 | The actual root cause is found. The team works on a plan to speed up the mitigation.

 | 17:57
 | The team is now sure that just restarting the component will fix the issue, so the parallel restart is initiated.

 | 18:11
 | Impact fully mitigated.

## Root causeRoot cause

Bug description

There is a host component of the VPC control plane. One of its functions is to send, receive and process BGP messages, announce and withdraw routes. Due to the bug, this component partially ignored route distinguishers in the announcements. As a result, some IP alias announcements that should be treated differently were merged into a single instance. That merge, in turn, resulted in one withdrawal cancelling two different announcements simultaneously.

Incident trigger

This bug was unknown to the development team and was in the code for quite some time. The release that triggered this incident introduced a change in route distinguishers values that was required for a new feature. Due to this change, the above-mentioned bug now actually manifested itself. Two different announcements were merged in one and a sequence of two announcements and one withdrawal resulted in no active routes known to the data plane. Packets for these routes were then not processed.

This only affected network connectivity for pods of Managed Services for Kubernetes, as only their update messages were changed by the triggering release.

Why did the rollback not help?

The combination of the bug and the change in route distinguishers made the simple rollback ineffective, as it led to the same sequence of update messages — but with reversed route distinguishers.

Why did we not catch the issue on the testing installation or on canaries?

It required two factors to reproduce the issue.

- 

An IP alias must exist at the time of release that changed route distinguishers.

- 

A node with a virtual machine that sends packets to an IP alias must be updated before the node with the virtual machine that receives them.

There were end-to-end (e2e) tests with permanent virtual machines on testing installation which met the first condition, but the second condition was not met. Similar reasoning applies to canaries in the eu-west1 region; in addition, our permanent e2e virtual machines do not reside on canary nodes. Both testing and canary e2e issues will be addressed in the list of action items.

Another reason that significantly contributed to the response time is the insufficient alerting on technical metrics deviating from their normal values. Two metrics that were sensitive in this particular case are the number of routes and the number of drops.

## Post-incident action planPost-incident action plan

We acknowledge the severity of this incident and are committed to addressing the root causes to improve system reliability and resilience. On top of measures directly addressing the bug itself, below is a list of key action items we are already working on or plan to begin in the near future.

Service observability and alerting

- Add alert on diverged number of routes.

- Add alert on the number of drops in data plane.

Incident response capabilities of the VPC service

- Develop a method to reset endpoints without requiring a restart of the host VPC component.

Testing and deployment procedures

- Move VPC’s persistent e2e test virtual machines to canary hosts.

- Add persistent e2e tests for Managed Services for Kubernetes.

- Increase the frequency of e2e tests.

- Introduce the new deployment stage: non-critical internal services will be the first to receive updates.

Contents

- Incident overview

- Impact

- Timeline

- Root cause

- Post-incident action plan

Sign in to save this post
Sign In
