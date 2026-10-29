# Incident post-mortem analysis: us-central1 service disruption on August 19, 2026

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-us-central1-service-disruption-on-august-19

Skip to main content

## Incident overviewIncident overview

On August 19, 2026, a storm-related event affected the building of the data center facility hosting the us-central1 region, taking the facility’s building management system offline and shutting down the chilled-water cooling loop. With active cooling lost, the data halls overheated within roughly two hours, and servers, network switches and rack power systems began shutting down on thermal protection. This caused a region-wide disruption of us-central1 services: GPU and CPU compute, external network connectivity for virtual machines, object and block storage, Managed Kubernetes, Token Factory, managed platform services, and the regional API and console endpoints.

Cooling was restored and the data center thermally stabilized approximately six hours after the storm-related event. Restoring the platform took significantly longer than the facility recovery itself: a whole-region restart from a hard power loss required manual intervention in several recovery paths, and recovery of customer resources, primarily virtual machines with their disk attachments and Managed Kubernetes clusters, formed the longest part of the outage. Most services were restored during the evening of August 19 (UTC), and the incident was fully mitigated by the morning of August 20.

We apologize to all customers affected by this incident. This analysis describes what happened, why recovery took as long as it did, and what we are changing as a result.

## ImpactImpact

Customers with resources in us-central1 experienced the following effects. Other regions were not affected, with one narrow exception noted below.

- 

Compute (GPU and CPU virtual machines): a large share of compute hosts shut down on thermal protection or lost power when rack power systems tripped. Roughly one third of running virtual machines in the region were interrupted and required recovery. Most affected VMs were restored during the afternoon and evening of August 19 (UTC); a subset required additional manual recovery steps and was restored over the following hours. All reserved GPU capacity was confirmed restored by 08:38 UTC on August 20; restoration of the remaining on-demand node pool continued for several more days under the standard hardware repair process, so on-demand capacity in the region was reduced during that period.

- 

External network connectivity: virtual machines in the region lost external connectivity for approximately two hours (about 11:00-12:50 UTC), because all regional network gateway nodes lost power simultaneously. Internal connectivity was partially preserved on hosts that remained powered.

- 

Object storage (S3): requests to the regional S3 endpoint failed from about 10:40 UTC; the service was restored at 13:27 UTC. There was no data loss.

- 

Block storage and file storage: storage-backed operations failed or hung during the acute phase. After power was restored, a subset of disks was left with stale attachment state from the abrupt host shutdowns and could not be mounted or deleted until that state was manually reconciled; these cases were resolved over the following day.

- 

Managed Kubernetes: user cluster control planes became unavailable across the region. Recovery was significantly extended by a bug in the managed disks hot-plug functionality (see Root cause). Recovery required coordinated manual work; all customer clusters were reported healthy by 21:58 UTC on August 19.

- 

Token Factory (AI inference): models deployed in us-central1 were partially or fully unavailable from about 10:37 UTC. Inference capacity outside the region continued serving existing traffic, but depends on us-central1 for deployment and scaling operations, so provisioning of new endpoints and autoscaling were degraded there. Token Factory was fully recovered at 20:25 UTC.

- 

Managed platform services (including Managed PostgreSQL, Serverless and application services in the region) were unavailable during the main incident window and recovered by about 20:50 UTC.

- 

Console and API: the regional console and public API endpoints were unavailable. Global console traffic automatically failed over away from the region at 10:52 UTC; at 11:01 UTC, however, a health check incorrectly reported the region as recovered and a portion of console traffic was routed back to it for about seven minutes, until the region was manually removed from rotation (traffic fully stopped by 11:08 UTC).

- 

Monitoring and metrics: customer-facing metrics and logs for regional resources were unavailable or incomplete during the incident, and some metric data points from the acute phase could not be recovered.

The status page for the incident was opened at 10:43 UTC on August 19 and marked resolved at 08:16 UTC on August 20.

## TimelineTimeline

All times are in UTC, August 19-20, 2026.

 | Time (UTC)
 | Event

 | Aug 19, ~08:30
 | Storm-related event affected the data center building, taking the building management system offline. The chilled-water cooling loop shuts down, cutting off active cooling. The chain of events leading to the incident started.

 | ~09:15
 | Internal monitoring begins showing a temperature increase in the region. No alerting exists on this metric; it is identified in retrospect.

 | ~09:40
 | First equipment-level symptoms: InfiniBand fabric degradation and GPU over-temperature alerts begin to accumulate; the first customer reports are received shortly after 10:00.

 | 10:15
 | On-call engineers are paged on critical component temperature alerts.

 | 10:21
 | The incident is declared and coordinated response begins.

 | 10:27
 | The response team attempts to contact the facility operator; contact is established at 10:46. Our data center engineers head to the site.

 | ~10:40-11:00
 | The thermal cascade peaks: rack power systems trip on thermal overload, taking down multiple racks, including racks hosting regional control-plane and network gateway components. External VM connectivity in the region is fully lost by 11:00. Peak air inlet temperature reaches 58.5 °C.

 | 10:54
 | The root cause is confirmed on-site: the storm-related event disabled the building management system and the chiller loop. The facility operator’s engineers are on site and begin restoring cooling.

 | 11:15
 | The facility operator switches cooling to manual bypass mode; rack rear doors are opened to vent heat.

 | 11:45
 | First confirmed temperature drop.

 | 12:11-12:26
 | Rear-door cooling units are back online; tripped racks are re-energized, control-plane racks first.

 | 12:29-12:41
 | Direct customer notifications are sent.

 | 12:42
 | The regional infrastructure control plane is restored after manual intervention; platform recovery begins in stages.

 | 12:50
 | External VM connectivity is restored. Automatic mass recovery of interrupted virtual machines begins.

 | 13:27
 | Object storage service is restored.

 | 13:41-13:56
 | Block-storage host components are restarted to clear stale disk attachment state left by the abrupt power loss; VM recovery success improves, though many earlier one-shot recovery attempts have already failed and are not retried automatically.

 | ~14:25
 | VM recovery rate limits, designed to protect the platform during isolated failures, are manually raised for the region-scale recovery.

 | ~14:35-14:55
 | Data center temperature is confirmed stable; systematic node remediation begins.

 | ~14:50-16:03
 | Regional monitoring and metrics collection are progressively restored.

 | 15:43-16:05
 | The first recovery wave brings roughly half of Managed Kubernetes control planes back online. The remainder stay down: their control-plane instances either failed recovery or came back unhealthy.

 | 16:15-16:23
 | Around 140 Managed Kubernetes clusters are estimated unreachable; engineers begin starting the affected control-plane instances manually.

 | ~17:00
 | Manual starts restore a further quarter of the affected clusters; investigation continues into clusters that stay unhealthy after restart.

 | 18:11
 | 79 clusters still have an unreachable control plane, with control-plane data (etcd) unavailable.

 | 18:17
 | The root cause of the extended Managed Kubernetes outage is identified: a bug in Compute disk hot-plug that can leave a data disk unattached when an instance is recovered. A mitigation (controlled stop and start of affected control-plane instances) is tested on one cluster by 18:30.

 | 19:36-19:55
 | The mitigation is applied at scale: clusters with an unreachable control plane drop from 55 to 8.

 | 20:25
 | Token Factory is fully recovered.

 | 20:53
 | 104 customer virtual machines that were stopped by the incident are identified and started.

 | 21:58
 | All Managed Kubernetes clusters are reported healthy.

 | Aug 20, 08:38
 | Incident fully mitigated: all reserved GPU capacity in the region is confirmed restored; remaining individual node repairs continue under the standard hardware recovery process.

## Root causeRoot cause

The direct cause of the incident was a storm-related event at the data center building that simultaneously disabled the building management system and the chilled-water cooling plant. With active cooling lost, the data halls overheated within about two hours, and servers, network switches and rack power systems shut down on thermal protection. The facility operator restored cooling in manual bypass mode, and the thermal environment was stabilized about six hours after the storm-related event.

Two factors extended the customer-visible impact well beyond the facility recovery:

Detection depended on equipment-level symptoms. The storm-related event disabled the building management system, which is also the system that monitors the facility, so no facility-level alert reached either the facility operator or us. Our engineering team detected the anomaly via secondary equipment-level thermal indicators and proactively escalated to the facility operator to initiate manual bypass protocols. On our side, regional dashboards show the temperature rise starting around 09:15 UTC in retrospect, but no alerting existed on facility or room temperature trends; the first signals engineers acted on were component over-temperature alerts at 10:15 UTC. As a result, there was no practical window to shed heat load in a controlled way: by the time it was considered, about a quarter of the affected servers had already shut down.

A region-scale cold start required manual work in several recovery paths.

- 

The regional infrastructure control plane did not recover unattended after power was restored and required about two hours of manual restoration before dependent services could begin recovering.

- 

Automatic VM recovery is designed as a single attempt per instance and is rate-limited to protect the platform during isolated failures. The platform launched automatic recovery for roughly a third of all running instances in the region; about a third of these attempts succeeded, and the rest failed, mostly on storage-attachment errors caused by stale disk attachment state on abruptly powered-off hosts. Failed attempts were not retried automatically, and the rate limits had to be raised manually mid-recovery.

- 

A bug in the managed disks hot-plug functionality left some secondary data disks unattached after recovery. Managed Kubernetes cluster control planes store their state on such disks, so hundreds of recovered control-plane instances came back without their data disk, and their clusters stayed down until the bug was identified at 18:17 UTC and a controlled mass restart was applied. The bug has since been fixed and the fix deployed to all regions.

- 

Regional monitoring depended on components inside the affected region, which reduced responders' visibility during the acute phase and slowed recovery decisions.

## Incident response outcomesIncident response outcomes

The facility-level response was fast once the event was detected: the incident was declared within minutes of the paging alerts, the facility operator was engaged immediately, cooling was switched to manual mode within an hour of the incident declaration, and hardware was progressively re-energized as soon as the thermal environment allowed, with control-plane racks prioritized.

The platform-level response surfaced the following lessons:

Facility monitoring must be independent of the systems it monitors. A single storm-related event disabled both the cooling plant and the building management system that would have reported the failure, so neither the facility operator nor Nebius received a facility-level alert. This was the main detection gap; the action plan addresses both the operator-side and the Nebius-side part of it.

Environmental data must be covered by alerting. The temperature rise was visible on our dashboards from about 09:15 UTC, but no alert was configured on facility or room temperature trends; the alerts that fired an hour later reported component overheating, a consequence rather than the cause.

Region-scale recovery must be a rehearsed procedure. Improvements made after earlier incidents worked as intended: control-plane racks were re-energized first, network gateways were restored within about two hours of power returning, and object storage recovered automatically. Because the broader region-scale recovery program remains in progress and has not yet reached the stage of full-scale recovery drills, the restoration sequence across dependent layers was determined and coordinated manually during the incident. The incident also defined the next scope for this program: the longest part of the recovery was restoring customer resources (virtual machines, disk attachments, Managed Kubernetes control planes), and we are extending the drills to cover that layer.

Recovery automation must be designed for mass failure, not only for isolated failure. Single-attempt recovery, conservative rate limits, and the inability to distinguish incident-stopped instances from user-stopped ones required manual work at scale. Our goal is fast, predictable region recovery supported by both automation and rehearsed procedures.

Observability and traffic management must degrade gracefully with the region. Monitoring components had startup and data dependencies inside the affected region, which reduced our visibility during the acute phase and recovery. The regional health check used for global console traffic management reported the region healthy while it was not, briefly routing traffic back into it.

## Post-incident action planPost-incident action plan

Facility resilience

- 

Complete a joint resilience review with the facility operator, covering redundancy of the facility-management and monitoring systems, the ability of the cooling plant to keep operating if those systems fail, electrical protection of the cooling equipment, and on-site response coverage.

- 

Introduce facility-level environmental alerting (cooling plant state, room temperature trend) that pages our on-call engineers independently of the building management system and before workload-level symptoms appear.

- 

Establish a documented emergency escalation path with the facility operator, with an on-call contact tree and guaranteed response times.

- 

Define an emergency heat-load reduction procedure: explicit criteria, ownership and mechanics for shutting down or degrading workloads during a cooling loss.

Region-scale recovery

- 

Establish a formal, dependency-ordered region cold-start procedure with clearly defined ownership across each service layer.

- 

Implement a regular cadence of region-scale recovery drills, ensuring end-to-end validation across core platform components and customer workloads (VMs, storage attachments, and Managed Kubernetes clusters).

Recovery of customer resources

- 

Fix the disk-attachment bug that extended the Managed Kubernetes outage and deploy the fix to all production regions (completed).

- 

Improve the ways Compute users can configure recovery policies for their instances. Migrate all Managed Kubernetes control plane nodes to the improved recovery policy.

- 

Automate reconciliation of stale storage attachment state after abrupt host failures, so disks can be mounted and deleted without manual intervention.

Observability and traffic management

- 

Remove in-region dependencies from the monitoring stack startup and recovery paths, and extend cross-region monitoring so that we retain visibility into a region even when its local monitoring is degraded.

- 

Make regional health checks used for global traffic management reflect real service availability, so traffic fails over from an unhealthy region and does not return prematurely.

Nebius team

Contents

- Incident overview

- Impact

- Timeline

- Root cause

- Incident response outcomes

- Post-incident action plan

Sign in to save this post
Sign In
