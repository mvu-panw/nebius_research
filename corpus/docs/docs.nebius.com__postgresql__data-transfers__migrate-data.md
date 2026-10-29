# Migration from or to a Managed Service for PostgreSQL® cluster

Source: https://docs.nebius.com/postgresql/data-transfers/migrate-data

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Migration from or to a Managed Service for PostgreSQL® cluster

You can migrate tables and schemas from or to a Managed Service for PostgreSQL cluster. To do this, create a dump of the source cluster by using the [pg\_dump](https://www.postgresql.org/docs/current/app-pgdump.html) utility. Next, restore the dump in the target cluster by using the [pg\_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) utility.

> [!NOTE]
>
> Instead of using migration, you can [replicate data](https://docs.nebius.com/postgresql/replication/from-external.md) from an external cluster to a Managed PostgreSQL cluster.

## Steps

1. [Prepare a target cluster](#prepare-a-target-cluster).
2. [Migrate data](#migrate-data).

## Prerequisites

The migration is only possible if the following conditions are met:

* The PostgreSQL version in the source cluster is the same as in the target cluster. You can check the versions supported by Managed PostgreSQL on the cluster creation page in the [web console](https://console.nebius.com).

* The `pg_dump` and `pg_restore` utilities have the same version. You can install these utilities together with `psql`:

  **macOS**

  ```bash theme={null}
  brew install libpq
  echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
  ```

  After that, restart the terminal.

  **Ubuntu**

  ```bash theme={null}
  sudo apt update && sudo apt install postgresql-client
  ```

* The major version of the utilities must be greater than or equal to the PostgreSQL version in the target cluster. For example, if the cluster is created with version 16, the major version of the utilities can be 16 or 17.

## Prepare a target cluster

1. Create a target cluster with the same username as in the source cluster. For details on how to create a Managed Service for PostgreSQL cluster, see [How to create clusters](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters).

2. Make sure that the target cluster has at least the same list of installed PostgreSQL extensions as the source cluster does:

   1. Connect to the DB in the source cluster and then check what extensions are installed:

      ```sql theme={null}
      SELECT * FROM pg_available_extensions;
      ```

   2. [Enable these extensions](https://docs.nebius.com/postgresql/databases/extensions.md) on a target cluster.

3. To secure connections to databases, install the Nebius AI Cloud certificate:
   ```bash theme={null}
   mkdir -p ~/.postgresql \
   curl "https://storage.eu-north1.nebius.cloud/msp-certs/ca.pem" \
      -o ~/.postgresql/root.crt \
   chmod 0600 ~/.postgresql/root.crt
   ```
   This command creates the `.postgresql` folder, downloads the certificate into it and then sets the access rights to the certificate file.

## Migrate data

1. Switch the source DB to read-only mode:

   ```sql theme={null}
   ALTER USER <username> SET default_transaction_read_only = on;
   ```

   Run this statement for every DB user.

2. Create the source DB dump:

   ```bash theme={null}
   pg_dump --host=<source_host_address> \
      --port=<port> \
      --dbname=<DB_name> \
      --username=<username> \
      --jobs=<number_of_CPU_cores> \
      --format=d \
      --file=db_dump
   ```

   Specify the following parameters in the command:

   * `--host`: The IP address or FQDN of the primary host of the source cluster.
   * `--port`: The port to access the source cluster.
   * `--dbname`: The source DB name.
   * `--username`: The username in the source cluster.
   * `--jobs` (optional): To speed up the dump creation and activate a multithreaded mode, specify the number of vCPU cores on which dump creation threads run in parallel.

3. Restore the data from the dump to the target cluster:

   ```bash theme={null}
   pg_restore --host=<target_host_address> \
      --dbname=<DB_name> \
      --username=<username> \
      --port=5432 \
      --format=d \
      --verbose \
      --file=db_dump \
      --single-transaction \
      --no-privileges
   ```

   Specify the following parameters in the command:

   * `--host`: The IP address or FQDN of the primary host of the target cluster.
   * `--dbname`: The target DB name.
   * `--username`: The username in the target cluster.

     Must match the username in the source cluster.

     If you restore all the data from the source DB, specify the DB owner username. If you only restore a single schema, add the `--schema=<schema_name>` parameter. In this case, the DB owner rights are not required.

   If the specified user does not have rights to create or update the PostgreSQL extensions and this causes errors during restoration, remove the `--single-transaction` parameter from the command. The service ignores the errors in this case:

   ```text theme={null}
   pg_restore: warning: errors ignored on restore: 3
   ```

   However, make sure that these errors only apply to the extensions.

4. Connect to the target DB and check the integrity of the migrated data:

   * To check the list of tables, run `\dt`.
   * To check the list of schemas, run `\dn`.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
