# Backups in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/backups

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Backups in Managed Service for PostgreSQL®

Managed Service for PostgreSQL protects the data that you store in your clusters and creates backups for them. The service supports two types of backups:

* Automatic backups that Managed Service for PostgreSQL creates daily based on the [cluster configuration](#how-to-configure-automatic-backups) that you set.
* Manual (or on-demand) backups that you [create](#how-to-create-a-backup). You can also [delete](#how-to-delete-a-manual-backup) them later.

Once a backup is created, you can [restore a cluster](#how-to-restore-a-cluster-from-a-backup) from it.

## How to configure automatic backups

When you [create a Managed PostgreSQL cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters), you can configure at what time of day the service creates automatic backups and how long it stores them.

> [!WARNING]
>
> You cannot change the backup settings after you create a cluster.

**Web console**

On the cluster creation page ( **PostgreSQL** → **Create cluster**), find **Backup settings**.

You can configure the following settings of automatic backups:

***Start of backup window***

The time when Managed PostgreSQL starts creating automatic backups. The service backs up clusters daily. The time is specified in UTC+00:00. Format: `HH:MM:SS`; e.g., `00:30:00`. Default value: `00:02:00`.

***Retention period***

The number of days Managed PostgreSQL stores an automatic backup after creating it. This is how far back you can restore the cluster. The retention period also applies to the cluster's [write ahead log](https://www.postgresql.org/docs/current/continuous-archiving.html) (WAL). Default and minimum value: `7d` (7 days). Maximum value: `30d` (30 days).

**CLI**

Add parameters of automatic backups to the cluster creation command:

```bash theme={null}
nebius msp postgresql v1alpha1 cluster create \
  --backup-backup-window-start '00:02:00' \
  --backup-retention-policy '7d' \
  <other_parameters>
```

`--backup-backup-window-start`

The time when Managed PostgreSQL starts creating automatic backups. The service backs up clusters daily. The time is specified in UTC+00:00. Format: `HH:MM:SS`; e.g., `00:30:00`. Default value: `00:02:00`.

`--backup-retention-policy`

The number of days Managed PostgreSQL stores an automatic backup after creating it. This is how far back you can restore the cluster. The retention period also applies to the cluster's [write ahead log](https://www.postgresql.org/docs/current/continuous-archiving.html) (WAL). Default and minimum value: `7d` (7 days). Maximum value: `30d` (30 days).

See the [full reference](https://docs.nebius.com/cli/reference/msp/postgresql/v1alpha1/cluster/create.md) for the command.

**Terraform**

Add parameters of automatic backups to the cluster resource:

```bash theme={null}
resource "nebius_msp_postgresql_v1alpha1_cluster" "<resource_name>" {
  backup = {
    backup_window_start = "00:02:00"
    retention_policy    = "7d"
  }

  <other_parameters>
}
```

`backup.backup_window_start`

The time when Managed PostgreSQL starts creating automatic backups. The service backs up clusters daily. The time is specified in UTC+00:00. Format: `HH:MM:SS`; e.g., `00:30:00`. Default value: `00:02:00`.

`backup.retention_policy`

The number of days Managed PostgreSQL stores an automatic backup after creating it. This is how far back you can restore the cluster. The retention period also applies to the cluster's [write ahead log](https://www.postgresql.org/docs/current/continuous-archiving.html) (WAL). Default and minimum value: `7d` (7 days). Maximum value: `30d` (30 days).

See the [full reference](https://docs.nebius.com/terraform-provider/reference/resources/msp_postgresql_v1alpha1_cluster.md) for the resource.

## How to create a backup

Before you begin, make sure that your Managed PostgreSQL cluster has the `Running` status.

To create a backup:

**Web console**

1. In the sidebar, go to  **PostgreSQL**.
2. Open the page of the required cluster and then go to the **Backups** tab.
3. Click  **Create backup**.

After that, a new backup appears in the list.

**CLI**

1. To get the ID of the required cluster, list the Managed PostgreSQL clusters:
   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster list
   ```
   The cluster ID is specified in the `metadata.id` parameter.
2. Create a backup:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 backup create --cluster-id <cluster_ID>
   ```

## How to restore a cluster from a backup

When you restore from a backup, you create a new Managed PostgreSQL cluster. In this new cluster, the target host disks must be at least as large as the source host disks. You can configure the rest of the settings differently from the source cluster.

You can restore from a backup not only existing clusters, but also deleted ones. After you delete a cluster, Managed PostgreSQL stores its backups for the [retention period](#how-to-configure-automatic-backups).

To restore a cluster from a backup:

**Web console**

1. In the sidebar, go to  **PostgreSQL**.

2. Switch to **Backups**. Alternatively, open the page of the required cluster and switch to **Backups**.

3. Launch restoration:

   * For an automatic backup, click **Restore**.
   * For a manual backup, click  → **Restore**.

4. In the form that opens, configure and create a new cluster that will be restored from the backup. For configuration details, see [Working with your Managed Service for PostgreSQL® cluster](https://docs.nebius.com/postgresql/clusters/manage.md).

   When you fill out the form for an automatic backup, you can specify an optional *recovery time*. This is the moment to which the cluster state should be returned.

   Managed PostgreSQL supports the [Point-in-Time Recovery](https://en.wikipedia.org/wiki/Point-in-time_recovery) (PITR) technology. This technology allows you to restore a cluster to any moment, from creation of the oldest backup to archiving the most recent [write-ahead log (WAL)](https://www.postgresql.org/docs/current/wal-intro.html).

   If you specify a desired time and receive the error that a WAL has not been archived yet, wait a while for the WAL to be archived. The archiving process takes some time, especially if the cluster does not have any workloads.

**CLI**

1. Get IDs of the backup and its source cluster. For example, you can:

   * List all Managed PostgreSQL backups in the project:

     ```bash theme={null}
     nebius msp postgresql v1alpha1 backup list
     ```

   * List all backups of the specified cluster:

     ```bash theme={null}
     nebius msp postgresql v1alpha1 backup list-by-cluster \
       --cluster-id <cluster_ID>
     ```

     To get the cluster ID, use [nebius msp postgresql v1alpha1 cluster list](https://docs.nebius.com/cli/reference/msp/postgresql/v1alpha1/cluster/list.md) or [nebius msp postgresql v1alpha1 cluster get-by-name](https://docs.nebius.com/cli/reference/msp/postgresql/v1alpha1/cluster/get-by-name.md).

   Both commands that list backups return outputs like the following:

   ```yaml theme={null}
   backups:
     - id: <backup_ID>
       source_cluster_id: <ID_of_source_cluster>
       ...
   ```

2. Restore the cluster:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster restore \
     --backup-id <backup_ID> \
     --source-cluster-id <ID_of_source_cluster> \
     --name <cluster_name> \
     --bootstrap-user-password *** \
     --network-id vpcnetwork-e*** \
     --recovery-time <yyyy-mm-dd>T<hh:mm:ss>Z
   ```

   The command contains the following parameters:

   * `--backup-id`: The ID of the backup that you got in the previous step.

   * `--source-cluster-id`: The ID of the source PostgreSQL cluster.

   * `--name`: The name of the new PostgreSQL cluster created from the backup.

   * `--bootstrap-user-password`: The PostgreSQL user password. It does not have to repeat the password of the source cluster.

     The password must contain at least:

     * 8 characters
     * One lowercase character
     * One uppercase character
     * One special character

   * `--network-id`: The [network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

   * `--recovery-time` (optional; for automatic backups only): The moment to which the cluster state should be returned.

     Managed PostgreSQL supports the [Point-in-Time Recovery](https://en.wikipedia.org/wiki/Point-in-time_recovery) (PITR) technology. This technology allows you to restore a cluster to any moment, from creation of the oldest backup to archiving the most recent [write-ahead log (WAL)](https://www.postgresql.org/docs/current/wal-intro.html).

     If you specify a desired time and receive the error that a WAL has not been archived yet, wait a while for the WAL to be archived. The archiving process takes some time, especially if the cluster does not have any workloads.

## How to delete a manual backup

You can only delete manual backups that you created. You cannot delete automatic backups.

Conversely, Managed PostgreSQL cannot delete manual backups, only automatic ones.

To delete a manual backup:

**Web console**

1. In the sidebar, go to  **PostgreSQL**.
2. Open the page of the required cluster and then go to the **Backups** tab.
3. In the row of the required manual backup, click  → **Delete**.

After that, the deletion confirmation is displayed. The backup is deleted in a few seconds.

**CLI**

1. To get the ID of the required cluster, list the Managed PostgreSQL clusters:
   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster list
   ```
   The cluster ID is specified in the `metadata.id` parameter.

2. To get the ID of the required manual backup, list the backups of the selected cluster:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 backup list-by-cluster \
     --cluster-id <cluster_ID>
   ```

   The backup ID is specified in the `id` parameter.

   Select only backups with the `on_demand: true` parameter. This means that they are manual.

3. Delete the backup:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 backup delete \
     --cluster-id <cluster_ID> --backup-id <backup_ID>
   ```

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
