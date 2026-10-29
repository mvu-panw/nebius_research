# Monitoring clusters in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/monitoring

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring clusters in Managed Service for PostgreSQL®

You can monitor Managed Service for PostgreSQL cluster state on the dashboard in the Nebius AI Cloud [web console](https://console.nebius.com). There are two ways to find the required dashboard:

* Go to  **Observability** → [Metrics](https://console.nebius.com/observability/metrics) and select the resource you would like to review.
* Go to the page of the cluster you would like to review and switch to the **Metrics** tab.

Use the dashboards to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/postgresql/resources/quotas-limits.md) increases and quickly identify anomalies. In case of issues with your clusters, dashboards also help the Nebius support team investigate the issues.

Data for the dashboards is collected automatically.

The cluster usage data becomes available 5–10 minutes after the cluster is created.

## Dashboard filters

Select a group:

* `pgbouncer` to monitor the connection pool.
* `postgres` to monitor the database operations.

To check Managed PostgreSQL hosts health separately, select them from the **Pod** list.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## Cluster monitoring metrics

### Resource usage

* **Total service CPU usage**

  Amount of vCPU that a cluster consumed.

* **Total service memory usage**

  Amount of consumed RAM in GiB, with work memory and cache.

* **Total disk IO usage**

  Disk read/write rate, in bytes per second.

* **Total service network usage**

  Network receive/transmit rate, in bytes per second.

* **Total service disk usage**

  Percentage of consumed storage.

* **Last base backup**

  Time since the last successful backup.

* **CPU usage**

  Amount of vCPU consumed per container, including the limit.

* **Throttling containers in %**

  Percentage of CPU periods containers went throttling.

* **Throttling containers in seconds**

  Percentage of CPU seconds containers went throttling.

* **Memory usage**

  Amount of memory that containers used in a dedicated period, including work memory and cache. Measured in bytes.

* **Network RX/TX**

  Average speed of data received/sent over the network per container, in bytes per second.

* **Disk IO**

  Average IOPS of the cluster's disks per container, in operations per second.

* **Disk used space**

  Amount of disk space consumed per container, including the limit.

* **Disk inodes used**

  Number of used [inodes](https://www.kernel.org/doc/html/latest/filesystems/ext4/inodes.html) with files metadata per container, including the limit. A lack of inodes leads to an overall lack of disk space, especially if you generate many small files like [Write-Ahead Log (WAL)](https://www.postgresql.org/docs/current/wal-intro.html) segments or temporary tablespaces.

### Replication

* **Current instance roles**

  Roles that hosts in a cluster are performing now: primary (handling read/write operations) or replica (replicating data and serving read-only queries).

* **Instance roles**

  Roles that hosts in a cluster performed during the dedicated period.

* **Instance status**

  Hosts statuses during the dedicated period: up or down.

* **Replication lag**

  Delay between the primary database and its replicas, in seconds.

* **WAL size**

  Size of WAL files in bytes per host.

* **WAL count**

  Number of WAL files per host.

* **WAL archiver**

  Number of archived WAL files per host.

### Database performance

* **Database size**

  Amount of disk space that a database consumed.

* **Transaction rate**

  Number of transactions committed or rolled back from each host per second.

* **Longest transaction**

  A pair of committed and rolled-back transactions that took the longest to complete for each host.

### Connection pooler

* **Pooler query rate**

  Number of queries passed through the pooler to the server per second.

* **Pooler query duration**

  Time used to process queries through the pooler.

* **Pooler servers used**

  Number of used server (pooler to PostgreSQL) connections.

* **Pooler clients used**

  Number of used client (client to pooler) connections.

* **Pooler clients active**

  Number of clients that are assigned a server connection and can process queries.

* **Pooler clients waiting**

  Number of clients that have sent queries but are not yet assigned a server connection.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
