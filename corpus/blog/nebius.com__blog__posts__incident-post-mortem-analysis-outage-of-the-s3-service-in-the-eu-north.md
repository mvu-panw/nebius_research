# Incident post-mortem analysis: outage of the S3 service in the eu-north1 region

Source: https://nebius.com/blog/posts/incident-post-mortem-analysis-outage-of-the-s3-service-in-the-eu-north

Skip to main content

## Incident overviewIncident overview

On May 5th, 2025, we had an outage of the S3 service in the eu-north1 region triggered by a steady increase of migration traffic accompanied by unexpected behaviour of the program.

The YDB database used to store binary S3 data hit the maximum allocated CPU resources for the background processing because of a bug in the thread pool size automatic configuration system. CPU starvation triggered the overflow of the storage group (shard) buffer accumulating log of recent changes. The system categorized this situation as the emergency ‘out of space’ issue, eventually bringing the database to the inoperable state, and misguiding the SRE team.

## ImpactImpact

Clients using S3 object storage service in eu-north1 experienced full unavailability between 05.05.2025 15:30 and 17:00 UTC for both uploads and downloads. At 17:00 UTC the uploads were restored with the newly uploaded data downloadable and at 17:50 UTC the incident was mitigated having restored access to all data. There have been no data loss as part of the incident.

## TimelineTimeline

 | Time (UTC)
 | Event

 | 15:20
 | S3 background processes report problems with the binary objects database. The most common is [OUT_OF_SPACE] Cannot perform transaction: out of disk space at tablet.

 | 15:21
 | An alert about SLI upload time violations fires on the S3 side, S3 duty starts looking at the problem.

 | 15:31
 | The S3 traffic drops significantly, more S3 engineers join the investigation.

 | 15:33
 | More that 10% of data shards are not operational, impact on clients confirmed.

 | 15:35
 | Incident coordination channel is created, YDB duty team joins the investigation.

 | 16:40
 | S3 team starts manually switching the incoming traffic to write to another database.

 | 17:00
 | All public uploads are restored going into an alternate database.

 | 17:06
 | YDB team figured out the root cause related to the incorrect handling of the log chunks buffer overflow.

 | 17:35
 | Overflown storage groups had been rearranged manually by the YDB SRE team.

 | 17:45
 | The S3 team confirmed the primary YDB database is now operational.

 | 17:50
 | S3 storage reconfigured to read from the primary database, service restored.

## Root causeRoot cause

It’s hard to attribute the issue to a single ‘bug’ in the system code. There were several factors contributing to the problem, related to the hard limited buffer for the incoming changes over the physical disk.

- 

There is no backpressure on the buffer writing side.

- 

The buffer processing is a short-running background task executed in the batch pool. There are other tasks in this pool with the long execution time. Long running background tasks block execution of the short running ones when there’s not enough resources in a pool.

- 

Automatic allocation of resources to execution pools believes the pool does not consume CPU when no tasks are completed within a second, reducing number of resources to the default minimum.

- 

The buffer overflow triggers ‘Out of space’ error code on write attempts to all storage groups placed on a physical disk.

- 

The storage group ‘Out of space’ error never occurs for real space issues until all the disks in the cluster are full, as there’s a staged backpressure ensuring the upfront replacement of storage groups without downtime before running out of space on them.

- 

Reaction to the ‘Out of space’ error assumes emergency shutdown of the writing component waiting for disks to be added to the cluster.

## Incident triggerIncident trigger

The incident was triggered by the incorrect behavior of the thread pool automatic configuration system, caused by the approach to measure the CPU consumption in the pool.

## Why did finding root cause took so much time?Why did finding root cause took so much time?

The SRE team was misguided by the ‘out of space’ records in the log, trying to localize the non-existent problem with the disk space. Log chucks overflow on several disks was also detected quickly, but at first did not attract attention, since single disk failures normally do not affect the YDB database operation.

## Why didn’t we catch the issue on the testing installations?Why didn’t we catch the issue on the testing installations?

For the problem to arise, two factors had to coexist:

- There should be many large disks attached to a single YDB storage node. In fact, only configurations with HDD disk arrays allow to achieve the capacity volume to exceed the default batch pool resources involved in LSM compaction and defragmentation planning.

- There should be a long-running constant write workload of large objects. We had it here as part of the migration of the S3 data from another cluster.

## Post-incident action planPost-incident action plan

Immediate actions

These actions are being taken to prevent the similar incidents from happening in the future:

- Alerts for used log chunks.

- Switch off automatic pool size configuration, adjust pool sizes manually.

- Alerts for resource consumption in the batch pool.

Code changes

Fixes to be done in the system code to prevent similar incidents from happening:

- Refactor automatic pool configuration system to work correctly with long running tasks.

- Stop writing new user data to log before the limit reached, to avoid blocking of compaction.

- Remove returning the ‘out of space’ error for the write requests which cannot write to the log, delay execution of such requests.

- Split LSM compaction and defragmentation planning long-running tasks into fragments.

Nebius team

Contents

- Incident overview

- Impact

- Timeline

- Root cause

- Incident trigger

- Why did finding root cause took so much time?

- Why didn’t we catch the issue on the testing installations?

- Post-incident action plan

Sign in to save this post
Sign In
