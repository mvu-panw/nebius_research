# Replicating data to Managed Service for PostgreSQL® from an external PostgreSQL cluster

Source: https://docs.nebius.com/postgresql/replication/from-external

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Replicating data to Managed Service for PostgreSQL® from an external PostgreSQL cluster

Managed Service for PostgreSQL supports logical replication, enabling you to replicate data from external PostgreSQL instances into your Nebius AI Cloud cluster. This feature facilitates data migration, synchronization, and integration between different PostgreSQL databases. See the PostgreSQL documentation for more information about [logical replication](https://www.postgresql.org/docs/16/logical-replication.html) and the associated [restrictions](https://www.postgresql.org/docs/16/logical-replication-restrictions.html).

> [!NOTE]
>
> Instead of using replication, you can [move data](https://docs.nebius.com/postgresql/data-transfers/migrate-data.md) from or to a Managed PostgreSQL cluster.

## Prerequisites

* The external PostgreSQL cluster should be running version 10 or higher.
* The Managed PostgreSQL cluster must be able to connect to the external PostgreSQL cluster. Ensure that incoming connections are allowed for the external PostgreSQL cluster from the internet.

## Configure the replication source

Set up the external PostgreSQL cluster:

1. Enable logical replication by setting `wal_level = logical` in the `postgresql.conf` file.

2. Create a user with replication privileges:

   ```sql theme={null}
   CREATE ROLE <replicator_username> WITH REPLICATION LOGIN PASSWORD '<password>';
   ```

3. Create a publication for the tables you wish to replicate:

   ```sql theme={null}
   CREATE PUBLICATION <publication_name> FOR TABLE <source_table>;
   ```

## Configure the replication target

Set up the Managed PostgreSQL cluster:

1. In your Managed PostgreSQL cluster, create the table that will receive the replicated data. Ensure that the table schema matches the source table.

2. Establish a subscription to the external publication:

   ```sql theme={null}
   CREATE SUBSCRIPTION <subscription_name>
   CONNECTION 'host=<external_host> port=5432 user=<replicator_username> dbname=<source_db_name> password=<password>'
   PUBLICATION <publication_name>;
   ```

   Upon successful creation, PostgreSQL will synchronize the data from the external source to the Managed PostgreSQL cluster.

3. Check that the data has been replicated correctly:

   ```sql theme={null}
   SELECT * FROM <target_table>;
   ```

## Monitoring and maintenance

* Use the `pg_stat_subscription` view to monitor the status of your subscription:

  ```sql theme={null}
  SELECT * FROM pg_stat_subscription;
  ```

* If you alter the schema of the replicated tables, ensure that corresponding changes are made on both the publisher and subscriber to prevent replication errors.

* Regularly monitor replication slots on the external PostgreSQL instance to prevent issues related to disk space, as logical replication slots retain WAL files until they are consumed by all subscribers.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
