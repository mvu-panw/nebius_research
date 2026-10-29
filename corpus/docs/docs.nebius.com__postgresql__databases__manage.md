# Creating, modifying and deleting databases in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/databases/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating, modifying and deleting databases in Managed Service for PostgreSQL®

To work with a database in a Managed Service for PostgreSQL cluster, you need to [connect](https://docs.nebius.com/postgresql/databases/connect.md) to it.

Once you connect to the cluster, all [PostgreSQL commands](https://www.postgresql.org/docs/current/sql-commands.html) are available for you to execute. For example, you can perform these basic operations:

* [Create databases](#how-to-create-databases)
* [Modify databases](#how-to-modify-databases)
* [Delete databases](#how-to-delete-databases)

## How to create databases

To create a database, run the [CREATE DATABASE](https://www.postgresql.org/docs/current/sql-createdatabase.html) command:

```sql theme={null}
CREATE DATABASE <name>;
```

Every cluster has at least one default database, which you specified when [creating the cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters). Use the `\l` command to list all databases in the cluster.

When a new database is created, you don't automatically switch to it. Use the `\c <name>` command to connect to the database you just created.

## How to modify databases

To make changes to a database, run the [ALTER DATABASE](https://www.postgresql.org/docs/current/sql-alterdatabase.html) command:

```sql theme={null}
ALTER DATABASE <name> <changes>;
```

For example, you can rename the database:

```sql theme={null}
ALTER DATABASE db_test RENAME TO old_testdb;
```

Note that you can't rename the current database. Connect to another database, first.

## How to delete databases

> [!WARNING]
>
> Do not delete the default database, as this may cause the service to malfunction.

To delete a database, run the [DROP DATABASE](https://www.postgresql.org/docs/current/sql-dropdatabase.html) command. This operation cannot be undone.

```sql theme={null}
DROP DATABASE <name>;
```

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
