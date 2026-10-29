# Working with your Managed Service for PostgreSQL® cluster

Source: https://docs.nebius.com/postgresql/clusters/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Working with your Managed Service for PostgreSQL® cluster

In Managed Service for PostgreSQL, databases are organized into collections called *clusters*. You can [create](#how-to-create-clusters), [modify](#how-to-modify-clusters) or [delete](#how-to-delete-clusters) clusters.

> [!TIP]
>
> If you want to move data from an external PostgreSQL cluster to a Managed PostgreSQL cluster, use [migration](https://docs.nebius.com/postgresql/data-transfers/migrate-data.md) or [replication](https://docs.nebius.com/postgresql/replication/from-external.md).

## How to create clusters

**Web console**

1. In the sidebar, go to  **PostgreSQL**.

2. Click  **Create cluster**.

3. On the page that opens, enter the cluster name and an optional description.

4. (Optional) Select one of the pooling modes:

   * **Transaction**: A connection is allocated from a connection pool for every transaction. Once the transaction is completed, the connection returns to the pool.

     The transaction mode is suitable for a large number of idle connections. Additionally, this mode allows you to allocate a smaller pooling size in comparison with the session mode.

     However, the transaction mode offers a limited support of PostgreSQL features; not all PostgreSQL clients are compatible with this mode.

   * **Session** (set by default): A connection is allocated from a connection pool for every client session. Once the session is terminated, the connection returns to the pool.

     More PostgreSQL clients support the session mode, over the transaction mode. Moreover, the session mode does not limit the number of PostgreSQL features that you can use.

     However, a database has to consume more resources to maintain long-lasting connections. You may need to increase the pooling size.

5. (Optional) In the **Pooling size** field, specify the number of connections allowed in a pool for a single database.

6. In the **Access** field, select whether the cluster should have a public IP address and access through the internet.

7. In the **Resources** section, configure the cluster resources:

   1. Select the number of vCPUs and RAM to allocate to the cluster.
   2. Specify the storage capacity.

8. Set the number of the cluster hosts.

9. In the **Database** section, specify the parameters for the connection to the database:

   1. Enter the database name.

   2. Enter the username.

      The following usernames are reserved; do not specify them: `admin`, `repl`, `monitor`, `postgres`, `public` and `none`.

   3. Enter the password. It must contain at least:

      * 8 characters
      * One lowercase character
      * One uppercase character
      * One special character

10. (Optional) In the **Backup settings** section, configure the cluster backup:

    1. Schedule the backup. The backup is created every day at the selected time.
    2. Specify how long, in days, every backup and [write-ahead logs (WALs)](https://www.postgresql.org/docs/current/wal-intro.html) should be kept.

11. (Optional) Configure PostgreSQL additional parameters.

    > **Supported PostgreSQL parameters**
    >
    > * [Autovacuum work mem](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM)
    > * [Autovacuum vacuum cost delay](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY)
    > * [Autovacuum vacuum cost limit](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT)
    > * [Autovacuum naptime](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME)
    > * [Autovacuum vacuum scale factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR)
    > * [Autovacuum analyze scale factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR)
    > * [Statement timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-STATEMENT-TIMEOUT)
    > * [Idle in transaction session timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)
    > * [Search path](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-SEARCH-PATH)
    > * [Default transaction read-only](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY)
    > * [Maximum connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS)
    > * [Shared buffers](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-SHARED-BUFFERS)

12. Click **Create cluster**.

The cluster will have the `Provisioning` status while it is being created. Before you perform any operations, wait for the `Running` status.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Create a cluster:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster create \
       --name <cluster_name> \
       --description "<description>" \
       --network-id <network_ID> \
       --config-version 16 \
       --config-pooler-config-pooling-mode <transaction|session> \
       --config-pooler-config-max-pool-size <pooling_size> \
       --config-public-access=<true|false> \
       --config-template-resources-platform cpu-e2 \
       --config-template-resources-preset <preset> \
       --config-template-disk-type network-ssd \
       --config-template-disk-size-gibibytes <storage_size> \
       --config-template-hosts-count <number_of_hosts> \
       --bootstrap-db-name <database_name> \
       --bootstrap-user-name <username> \
       --bootstrap-user-password <password> \
       --backup-backup-window-start "<HH:MM:SS>" \
       --backup-retention-policy <number_of_days>d \
       <PostgreSQL_parameters>
   ```

   This command contains the following parameters:

   * `--name`: The cluster name.

   * `--description`: The cluster description.

   * `--network-id`: The [network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

   * `--config-version`: The PostgreSQL version. The service currently supports only version 16.

   * `--config-pooler-config-pooling-mode`: The mode of how to allocate connections from the database connection pool. Managed PostgreSQL supports the following options:

     * **Transaction**: A connection is allocated from a connection pool for every transaction. Once the transaction is completed, the connection returns to the pool.

       The transaction mode is suitable for a large number of idle connections. Additionally, this mode allows you to allocate a smaller pooling size in comparison with the session mode.

       However, the transaction mode offers a limited support of PostgreSQL features; not all PostgreSQL clients are compatible with this mode.

     * **Session** (set by default): A connection is allocated from a connection pool for every client session. Once the session is terminated, the connection returns to the pool.

       More PostgreSQL clients support the session mode, over the transaction mode. Moreover, the session mode does not limit the number of PostgreSQL features that you can use.

       However, a database has to consume more resources to maintain long-lasting connections. You may need to increase the pooling size.

   * `--config-pooler-config-max-pool-size`: The number of connections allowed in a pool for a single database.

   * `--config-public-access`: If `true`, the cluster has both a public and a private IP address, and the cluster is accessible through the internet.

   * `--config-template-resources-platform`: The resource platform for the database hosts. Managed PostgreSQL currently supports only the `cpu-e2` platform.

   * `--config-template-resources-preset`: The resource preset. Specify one of the [presets available for](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-non-gpu-platforms) `cpu-e2`.

   * `--config-template-disk-type`: The disk type for the database hosts. Managed PostgreSQL currently supports only `network-ssd` disks.

   * `--config-template-disk-size-gibibytes`: The number of gibibytes in the cluster storage.

   * `--config-template-hosts-count`: The number of the cluster hosts.

   * `--bootstrap-db-name`: The database name.

   * `--bootstrap-user-name`: The username of the database user.

     The following usernames are reserved; do not specify them: `admin`, `repl`, `monitor`, `postgres`, `public` and `none`.

   * `--bootstrap-user-password`: The password for this user. The password must contain at least:

     * 8 characters
     * One lowercase character
     * One uppercase character
     * One special character

   * `--backup-backup-window-start`: The backup schedule, in the `HH:MM:SS` format. The backup is created every day at the selected time.

   * `--backup-retention-policy`: How long, in days, every backup and [write-ahead logs (WALs)](https://www.postgresql.org/docs/current/wal-intro.html) should be kept. For example, `7d` or `30d`.

   To configure the database, you can also use PostgreSQL parameters.

   > **Supported PostgreSQL parameters**
   >
   > * [--config-postgresql-config-16-autovacuum-work-mem](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM): From `-1` to `2147483647` (in kilobytes).
   > * [--config-postgresql-config-16-autovacuum-vacuum-cost-delay](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY): From `-1` to `100` (in milliseconds).
   > * [--config-postgresql-config-16-autovacuum-vacuum-cost-limit](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT): From `-1` to `10000`.
   > * [--config-postgresql-config-16-autovacuum-naptime](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME): From `1` to `2147483` (in seconds).
   > * [--config-postgresql-config-16-autovacuum-vacuum-scale-factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR): From `0` to `100`.
   > * [--config-postgresql-config-16-autovacuum-analyze-scale-factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR): From `0` to `100`.
   > * [--config-postgresql-config-16-statement-timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-STATEMENT-TIMEOUT): From `0` to `2147483647` (in milliseconds).
   > * [--config-postgresql-config-16-idle-in-transaction-session-timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT): From `0` to `2147483647` (in milliseconds).
   > * [--config-postgresql-config-16-search-path](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-SEARCH-PATH)
   > * [--config-postgresql-config-16-default-transaction-read-only](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY)
   > * [--config-postgresql-config-16-max-connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS): From `100` to `12800`.
   > * [--config-postgresql-config-16-shared-buffers](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-SHARED-BUFFERS): From `128` to `8589934584` (in kilobytes).

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

2. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_msp_postgresql_v1alpha1_cluster" "<cluster_name>" {
     name        = "<cluster_name>"
     description = "<cluster_description>"
     parent_id   = "<project_ID>"
     network_id  = "<network_ID>"

     config = {
       version = "16"
       pooler_config = {
         pooling_mode  = "<TRANSACTION|SESSION>"
         max_pool_size = <pooling_size>
       }
       public_access = <true|false>
       template = {
         resources = {
           platform = "cpu-e2"
           preset   = "<preset>"
         }
         disk = {
           type           = "network-ssd"
           size_gibibytes = <storage_volume>
         }
         hosts = {
           count = <number_of_hosts>
         }
       }
       postgresql_config_16 = {
         <PostgreSQL_parameters>
       }
     }

     bootstrap = {
       db_name       = "<database_name>"
       user_name     = "<username>"
       user_password = "<password>"
     }

     backup = {
       backup_window_start = "HH:MM:SS"
       retention_policy    = "<number_of_days>d"
     }
   }
   ```

   The file contains the following parameters:

   * `name`: The cluster name.

   * `description`: The cluster description.

   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).

   * `network_id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

   * `config`: The cluster configuration parameters:

     * `version`: The PostgreSQL version. The service currently supports only version 16.

     * `pooler_config.pooling_mode`: The mode of how to allocate connections from the database connection pool. Managed PostgreSQL supports the following options:

       * **Transaction**: A connection is allocated from a connection pool for every transaction. Once the transaction is completed, the connection returns to the pool.

         The transaction mode is suitable for a large number of idle connections. Additionally, this mode allows you to allocate a smaller pooling size in comparison with the session mode.

         However, the transaction mode offers a limited support of PostgreSQL features; not all PostgreSQL clients are compatible with this mode.

       * **Session** (set by default): A connection is allocated from a connection pool for every client session. Once the session is terminated, the connection returns to the pool.

         More PostgreSQL clients support the session mode, over the transaction mode. Moreover, the session mode does not limit the number of PostgreSQL features that you can use.

         However, a database has to consume more resources to maintain long-lasting connections. You may need to increase the pooling size.

     * `pooler_config.max_pool_size`: The number of connections allowed in a pool for a single database.

     * `public_access`: If `true`, the cluster has both a public and a private IP address, and the cluster is accessible through the internet.

     * `template.resources.platform`: The resource platform for the database hosts. Managed PostgreSQL currently supports only the `cpu-e2` platform.

     * `template.resources.preset`: The resource preset. Specify one of the [presets available for](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-non-gpu-platforms) `cpu-e2`.

     * `template.disk.type`: The disk type for the database hosts. Managed PostgreSQL currently supports only `network-ssd` disks.

     * `template.disk.size_gibibytes`: The number of gibibytes in the cluster storage.

     * `template.hosts.count`: The number of the cluster hosts.

     * `postgresql_config_16`: Additional PostgreSQL parameters for the database configuration.

       > **Supported PostgreSQL parameters**
       >
       > ```hcl theme={null}
       > postgresql_config_16 = {
       >   autovacuum_work_mem                 = <in_kilobytes>
       >   autovacuum_vacuum_cost_delay        = <in_milliseconds>
       >   autovacuum_vacuum_cost_limit        = <>
       >   autovacuum_naptime                  = <in_seconds>
       >   autovacuum_vacuum_scale_factor      = <>
       >   autovacuum_analyze_scale_factor     = <>
       >   statement_timeout                   = <in_milliseconds>
       >   idle_in_transaction_session_timeout = <in_milliseconds>
       >   search_path                         = "<>"
       >   default_transaction_read_only       = <true|false>
       >   max_connections                     = <>
       >   shared_buffers                      = <in_kilobytes>
       > }
       > ```
       >
       > Supported PostgreSQL parameters:
       >
       > * [autovacuum\_work\_mem](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM): From `-1` to `2147483647`.
       > * [autovacuum\_vacuum\_cost\_delay](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY): From `-1` to `100`.
       > * [autovacuum\_vacuum\_cost\_limit](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT): From `-1` to `10000`.
       > * [autovacuum\_naptime](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME): From `1` to `2147483`.
       > * [autovacuum\_vacuum\_scale\_factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR): From `0` to `100`.
       > * [autovacuum\_analyze\_scale\_factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR): From `0` to `100`.
       > * [statement\_timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-STATEMENT-TIMEOUT): From `0` to `2147483647`.
       > * [idle\_in\_transaction\_session\_timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT): From `0` to `2147483647`.
       > * [search\_path](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-SEARCH-PATH)
       > * [default\_transaction\_read\_only](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY)
       > * [max\_connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS): From `100` to `12800`.
       > * [shared\_buffers](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-SHARED-BUFFERS): From `128` to `8589934584`.

   * `bootstrap.db_name`: The database name.

   * `bootstrap.user_name`: The username of the database user.

     The following usernames are reserved; do not specify them: `admin`, `repl`, `monitor`, `postgres`, `public` and `none`.

   * `bootstrap.user_password`:  The password for this user. The password must contain at least:

     * 8 characters
     * One lowercase character
     * One uppercase character
     * One special character

   * `backup.backup_window_start`: The backup schedule, in the `HH:MM:SS` format. The backup is created every day at the specified time.

   * `backup.retention_policy`: How long, in days, every backup and [write-ahead logs (WALs)](https://www.postgresql.org/docs/current/wal-intro.html) should be kept. For example, `7d` or `30d`.

3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

### How to restore clusters from backups

Managed PostgreSQL creates daily backups for each cluster, and you can create a new cluster from a backup. For more details and instructions, see [Backups in Managed Service for PostgreSQL®](https://docs.nebius.com/postgresql/backups.md).

## How to modify clusters

**Web console**

1. In the sidebar, go to  **PostgreSQL**.

2. Open the page of the required cluster and then go to the **Settings** tab.

3. Change the database pooling mode. Managed PostgreSQL supports the following options:

   * **Transaction**: A connection is allocated from a connection pool for every transaction. Once the transaction is completed, the connection returns to the pool.

     The transaction mode is suitable for a large number of idle connections. Additionally, this mode allows you to allocate a smaller pooling size in comparison with the session mode.

     However, the transaction mode offers a limited support of PostgreSQL features; not all PostgreSQL clients are compatible with this mode.

   * **Session** (set by default): A connection is allocated from a connection pool for every client session. Once the session is terminated, the connection returns to the pool.

     More PostgreSQL clients support the session mode, over the transaction mode. Moreover, the session mode does not limit the number of PostgreSQL features that you can use.

     However, a database has to consume more resources to maintain long-lasting connections. You may need to increase the pooling size.

4. In the **Access** field, select whether the cluster should have a public IP address and access through the internet.

5. In the **Resource preset** field, change the number of vCPUs and RAM that should be allocated to the cluster.

6. In the **Disk size** field, increase the size of the cluster storage disk. You cannot decrease the disk size. Managed PostgreSQL resizes the cluster disks without recreating the cluster.

7. Change the number of hosts in the cluster.

8. In the **Database** section, change the password of the database user. The password must contain at least:

   * 8 characters
   * One lowercase character
   * One uppercase character
   * One special character

9. Configure PostgreSQL additional parameters.

   > **Supported PostgreSQL parameters**
   >
   > * [Autovacuum work mem](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM)
   > * [Autovacuum vacuum cost delay](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY)
   > * [Autovacuum vacuum cost limit](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT)
   > * [Autovacuum naptime](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME)
   > * [Autovacuum vacuum scale factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR)
   > * [Autovacuum analyze scale factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR)
   > * [Statement timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-STATEMENT-TIMEOUT)
   > * [Idle in transaction session timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)
   > * [Search path](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-SEARCH-PATH)
   > * [Default transaction read-only](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY)
   > * [Maximum connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS)
   > * [Shared buffers](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-SHARED-BUFFERS)

**CLI**

1. Get the ID of the cluster via its name:

   ```bash theme={null}
   export PG_CLUSTER_ID=$(nebius msp postgresql v1alpha1 cluster \
     get-by-name --name <cluster_name> --format jsonpath='{.metadata.id}')
   ```

   Alternatively, you can use the listing command: `nebius msp postgresql v1alpha1 cluster list`.

2. Update the cluster settings:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster update \
     --id $PG_CLUSTER_ID \
     --config-pooler-config-pooling-mode <transaction|session> \
     --config-pooler-config-max-pool-size <pooling_size> \
     --config-public-access=<true|false> \
     --config-template-resources-preset <preset> \
     --config-template-disk-size-gibibytes <new_disk_size> \
     --config-template-hosts-count <number_of_hosts> \
     --bootstrap-user-password <password> \
     <PostgreSQL_parameters>
   ```

   The command contains the following parameters:

   * `--config-pooler-config-pooling-mode`: The mode of how to allocate connections from the database connection pool. Managed PostgreSQL supports the following options:

     * **Transaction**: A connection is allocated from a connection pool for every transaction. Once the transaction is completed, the connection returns to the pool.

       The transaction mode is suitable for a large number of idle connections. Additionally, this mode allows you to allocate a smaller pooling size in comparison with the session mode.

       However, the transaction mode offers a limited support of PostgreSQL features; not all PostgreSQL clients are compatible with this mode.

     * **Session** (set by default): A connection is allocated from a connection pool for every client session. Once the session is terminated, the connection returns to the pool.

       More PostgreSQL clients support the session mode, over the transaction mode. Moreover, the session mode does not limit the number of PostgreSQL features that you can use.

       However, a database has to consume more resources to maintain long-lasting connections. You may need to increase the pooling size.

   * `--config-pooler-config-max-pool-size`: The number of connections allowed in a pool for a single database.

   * `--config-public-access`: If `true`, the cluster has both a public and a private IP address, and the cluster is accessible through the internet.

   * `--config-template-resources-preset`: The resource preset. Specify one of the [presets available for](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-non-gpu-platforms) `cpu-e2`.

   * `--config-template-disk-size-gibibytes`: The cluster storage disk size, in gibibytes. You can only increase the disk size, not decrease it. Managed PostgreSQL resizes the cluster disks without recreating the cluster.

   * `--config-template-hosts-count`: The number of the cluster hosts.

   * `--bootstrap-user-password`: The password for this user. The password must contain at least:

     * 8 characters
     * One lowercase character
     * One uppercase character
     * One special character

   To configure the database, you can additionally use PostgreSQL parameters.

   > **Supported PostgreSQL parameters**
   >
   > * [--config-postgresql-config-16-autovacuum-work-mem](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM): From `-1` to `2147483647` (in kilobytes).
   > * [--config-postgresql-config-16-autovacuum-vacuum-cost-delay](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY): From `-1` to `100` (in milliseconds).
   > * [--config-postgresql-config-16-autovacuum-vacuum-cost-limit](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT): From `-1` to `10000`.
   > * [--config-postgresql-config-16-autovacuum-naptime](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME): From `1` to `2147483` (in seconds).
   > * [--config-postgresql-config-16-autovacuum-vacuum-scale-factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR): From `0` to `100`.
   > * [--config-postgresql-config-16-autovacuum-analyze-scale-factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR): From `0` to `100`.
   > * [--config-postgresql-config-16-statement-timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-STATEMENT-TIMEOUT): From `0` to `2147483647` (in milliseconds).
   > * [--config-postgresql-config-16-idle-in-transaction-session-timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT): From `0` to `2147483647` (in milliseconds).
   > * [--config-postgresql-config-16-search-path](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-SEARCH-PATH)
   > * [--config-postgresql-config-16-default-transaction-read-only](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY)
   > * [--config-postgresql-config-16-max-connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS): From `100` to `12800`.
   > * [--config-postgresql-config-16-shared-buffers](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-SHARED-BUFFERS): From `128` to `8589934584` (in kilobytes).

   Only the parameters from the command above can be changed. To perform a full cluster update, add `--full` to the command. This will update all parameters with the default values or the values specified in the `--full` command.

**Terraform**

1. Modify the manifest with the deployed infrastructure:

   ```hcl theme={null}
   resource "nebius_msp_postgresql_v1alpha1_cluster" "<cluster_name>" {
     name        = "<cluster_name>"

     config = {
       pooler_config = {
         pooling_mode  = "<TRANSACTION|SESSION>"
         max_pool_size = <pooling_size>
       }
       public_access = <true|false>
       template = {
         resources = {
           preset   = "<preset>"
           ...
         }
         disk = {
           type           = "network-ssd"
           size_gibibytes = <new_disk_size>
         }
         hosts = {
           count = <number_of_hosts>
         }
         postgresql_config_16 = {
           <PostgreSQL_parameters>
         }
         ...
       }
       postgresql_config_16 = {
         <PostgreSQL_parameters>
       }
       ...
     }

     bootstrap = {
       user_password = "<password>"
       ...
     }
     ...
   }
   ```

   You can change the following parameters:

   * `name`: The cluster name.

   * `config`: The cluster configuration parameters:

     * `pooler_config.pooling_mode`: The mode of how to allocate connections from the database connection pool. Managed PostgreSQL supports the following options:

       * **Transaction**: A connection is allocated from a connection pool for every transaction. Once the transaction is completed, the connection returns to the pool.

         The transaction mode is suitable for a large number of idle connections. Additionally, this mode allows you to allocate a smaller pooling size in comparison with the session mode.

         However, the transaction mode offers a limited support of PostgreSQL features; not all PostgreSQL clients are compatible with this mode.

       * **Session** (set by default): A connection is allocated from a connection pool for every client session. Once the session is terminated, the connection returns to the pool.

         More PostgreSQL clients support the session mode, over the transaction mode. Moreover, the session mode does not limit the number of PostgreSQL features that you can use.

         However, a database has to consume more resources to maintain long-lasting connections. You may need to increase the pooling size.

     * `pooler_config.max_pool_size`: The number of connections allowed in a pool for a single database.

     * `public_access`: If `true`, the cluster has both a public and a private IP address, and the cluster is accessible through the internet.

     * `template.resources.preset`: The resource preset. Specify one of the [presets available for](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-non-gpu-platforms) `cpu-e2`.

     * `template.disk.size_gibibytes`: The cluster storage disk size, in gibibytes. You can only increase the disk size, not decrease it. Managed PostgreSQL resizes the cluster disks without recreating the cluster.

     * `template.hosts.count`: The number of the cluster hosts.

     * `postgresql_config_16`: Additional PostgreSQL parameters for the database configuration.

       > **Supported PostgreSQL parameters**
       >
       > ```hcl theme={null}
       > postgresql_config_16 = {
       >   autovacuum_work_mem                 = <in_kilobytes>
       >   autovacuum_vacuum_cost_delay        = <in_milliseconds>
       >   autovacuum_vacuum_cost_limit        = <>
       >   autovacuum_naptime                  = <in_seconds>
       >   autovacuum_vacuum_scale_factor      = <>
       >   autovacuum_analyze_scale_factor     = <>
       >   statement_timeout                   = <in_milliseconds>
       >   idle_in_transaction_session_timeout = <in_milliseconds>
       >   search_path                         = "<>"
       >   default_transaction_read_only       = <true|false>
       >   max_connections                     = <>
       >   shared_buffers                      = <in_kilobytes>
       > }
       > ```
       >
       > Supported PostgreSQL parameters:
       >
       > * [autovacuum\_work\_mem](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-AUTOVACUUM-WORK-MEM): From `-1` to `2147483647`.
       > * [autovacuum\_vacuum\_cost\_delay](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY): From `-1` to `100`.
       > * [autovacuum\_vacuum\_cost\_limit](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT): From `-1` to `10000`.
       > * [autovacuum\_naptime](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME): From `1` to `2147483`.
       > * [autovacuum\_vacuum\_scale\_factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR): From `0` to `100`.
       > * [autovacuum\_analyze\_scale\_factor](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR): From `0` to `100`.
       > * [statement\_timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-STATEMENT-TIMEOUT): From `0` to `2147483647`.
       > * [idle\_in\_transaction\_session\_timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT): From `0` to `2147483647`.
       > * [search\_path](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-SEARCH-PATH)
       > * [default\_transaction\_read\_only](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY)
       > * [max\_connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS): From `100` to `12800`.
       > * [shared\_buffers](https://www.postgresql.org/docs/16/runtime-config-resource.html#GUC-SHARED-BUFFERS): From `128` to `8589934584`.

   * `bootstrap.user_password`: The password for this user. The password must contain at least:

     * 8 characters
     * One lowercase character
     * One uppercase character
     * One special character

   > [!WARNING]
   >
   > If you change other settings, the cluster will be destroyed and then recreated with the new configuration.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

## How to delete clusters

**Web console**

1. In the sidebar, go to  **PostgreSQL**.

2. Click the cluster you want to delete.

3. On the **Settings** tab, click **Delete cluster**.

4. In the dialog window, enter the cluster name and click **Delete cluster**.

**CLI**

1. Copy the ID of the cluster you want to delete. Run the following command:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster list --page-size 10
   ```

   On the list of clusters, you'll get the cluster IDs under `metadata:id`.

2. Export the ID of the cluster to an environment variable:

   ```bash theme={null}
   export CLUSTER_ID_DELETION=<cluster_ID_from_clipboard>
   ```

3. Run the following command to delete your cluster:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster delete --id $CLUSTER_ID_DELETION
   ```

**Terraform**

1. Remove the corresponding `nebius_msp_postgresql_v1alpha1_cluster` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

> [!TIP]
>
> You can later [restore](https://docs.nebius.com/postgresql/backups.md#how-to-restore-a-cluster-from-a-backup) a deleted cluster from its backup. Managed PostgreSQL preserves backups of deleted clusters for the retention period configured in the [backup settings](https://docs.nebius.com/postgresql/backups.md#how-to-configure-automatic-backups).

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
