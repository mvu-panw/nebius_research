# Incident post-mortem analysis: us-central1 service disruption on March 10, 2026

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-us-central1-service-disruption-on-march-10

Skip to main content

On March 10, 2026 we were performing power infrastructure maintenance scheduled by one of our providers. The maintenance had been planned around a significantly narrower and more controlled customer impact, primarily related to pre-announced workload shutdowns within the maintenance scope. During the provider-led work, unexpected power failures affected additional racks serving regional networking and shared platform control plane services, turning the maintenance into a broader data center power incident. The incident then continued in several unplanned episodes over multiple hours, including additional power interruptions while recovery was already in progress, which extended customer impact and complicated restoration of the platform.

## ImpactImpact

Customers in us-central1 experienced several customer-visible effects across multiple services.

- 15:18–17:04 UTC: region-wide loss of external VM connectivity in us-central1.

- 15:24–16:46 UTC: public S3 endpoint unavailable, with internal storage operability also impaired.

- During the main incident window: broad Managed Kubernetes degradation, including cluster/API inaccessibility and a large number of clusters entering a critical state.

- 20:54–21:06 UTC and 22:37–22:54 UTC: additional shorter networking impacts for subsets of already recovering services due to later power aftershocks.

## TimelineTimeline

- 15:18 UTC — During scheduled provider-led electrical maintenance, an unexpected power event affects multiple racks serving regional networking and platform services.

- 15:19 UTC — External monitoring begins detecting regional failures.

- 15:24 UTC — The incident is declared and coordinated response begins.

- 15:45 UTC — We confirm the disruption is tied to the ongoing maintenance and begin joint restoration work with onsite teams.

- 16:26 UTC — We determine that part of the shared regional control layer is still unavailable, preventing automatic restart of some networking and platform workloads after power returns to hosts.

- 17:04 UTC — Core regional networking recovers and the broadest external VM connectivity impact begins to ease.

- 17:49 UTC — Core networking service and monitoring are fully operational again; recovery continues for workloads and platform components that did not restart cleanly.

- 18:44 UTC — Remaining recovery work narrows to services and instances that require manual intervention.

- 19:21 UTC — A later phase of the scheduled electrical work proceeds under active incident monitoring.

- 19:53 UTC — A brief secondary power interruption during that work causes renewed impact for a subset of services.

- 20:06 UTC — Onsite teams confirm maintenance is still in progress and that further unplanned interruptions remain possible.

- 20:54 UTC — Another brief power interruption affects a smaller subset of recovering services.

- 21:06 UTC — Services affected by the 20:54 interruption recover.

- 21:57 UTC — The provider reports that the active feed-restoration phase is complete and stability checks continue.

- 22:37 UTC — A further short interruption affects another small subset of services.

- 22:54 UTC — Services affected by the late interruption recover.

- 23:05 UTC — Provider-led electrical work stops for the night and no further power interruptions are expected.

- 23:49 UTC — Remaining recovery is limited to a reduced set of instances and services that did not restart cleanly after the power events.

- 00:27 UTC on March 11 — Final residual recovery continues for a small number of instances.

- 00:50 UTC on March 11 — Customer impact is fully mitigated.

## Root causeRoot cause

The primary cause of this incident was that, during planned maintenance by our power infrastructure provider, the work did not remain within the announced maintenance profile. Instead of a single controlled event, it resulted in an initial multi-rack outage followed by several additional unplanned and unannounced power interruptions over the next several hours.

The initial outage occurred while the site was operating in a temporary power configuration that had been put in place to carry out the planned maintenance. The presence of UPS capacity reduced the impact in some parts of the site, but it was not sufficient to prevent this incident under the actual maintenance conditions. During the work, some affected loads were temporarily dependent on a UPS-backed path while feed-transfer activity was still in progress. After the UPS on the redundant feed was discharged, the subsequent stages of the power transfer did not proceed as planned: an electrical anomaly led to incorrect switching and failure of several rack ATS units, which de-energized the affected racks. A subsequent failure during feed switching caused an additional power outage in some other racks.

The overall duration was then increased by how those repeated outages interacted with the platform architecture and the way recovery was conducted. Customer-facing networking, virtual machine connectivity, Managed Kubernetes and several storage and control functions depend on shared regional networking and a Kubernetes-based runtime and control plane layer. Power returned to different parts of the site at different times, and later brief outages interrupted recovery while it was already underway. As a result, some hosts were back before the control services needed to restart their workloads were healthy again. In practice, this meant that some networking gateways, control-plane components and storage-backed workloads did not recover automatically and required additional manual reconciliation.

Process-wise, during the incident response we did not follow the most effective restoration algorithm for a failure of this shape: too much of the recovery was handled as parallel service-by-service restoration instead of a stricter region-level recovery sequence ordered by dependency and aimed at minimizing total restoration time.

## Post-incident action planPost-incident action plan

- 

Re-evaluate our communication standards and processes for how broadly we scope maintenance notifications in the future, especially when provider-led infrastructure work may carry uncertainty beyond the directly planned impact.

- 

Finalize a joint technical and process review with the facility power provider and require stronger planning quality for future electrical maintenance, including earlier notice, stable scope before approval, explicit risk assessment and validated execution steps.

- 

Adopt more conservative preparation standards for this class of maintenance: assume a wider potential blast radius, validate contingency and rollback options in advance, align customer communication earlier and staff the full maintenance and stabilization window.

- 

Introduce hard stop-and-review criteria for ongoing electrical work so that any unexpected interruption pauses further maintenance until the risk is reassessed and continuation is explicitly re-approved.

- 

Prepare and regularly run recovery drills for a counter-emergency regional recovery procedure for large-scale power incidents, with a dependency-ordered restoration sequence, clear service ownership and target recovery times aimed at predictable minimum-time recovery of all core platform services.

Nebius team

Contents

- Impact

- Timeline

- Root cause

- Post-incident action plan

Sign in to save this post
Sign In
