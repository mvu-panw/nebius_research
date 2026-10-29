# Users and user privileges in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/databases/users

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Users and user privileges in Managed Service for PostgreSQL®

When you [create a cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters) in Managed Service for PostgreSQL, you set names for a default database and a default user (also called bootstrap user). After that, [connect](https://docs.nebius.com/postgresql/databases/connect.md) to the cluster as the bootstrap user and [create other users](#create-a-new-user).

> [!NOTE]
>
> Do not routinely work with the cluster as the bootstrap user. Create other users with the necessary privileges and leave the bootstrap user as a fallback in case of emergency.

## Bootstrap user privileges

The bootstrap user is not a superuser but has administrative privileges. It has the `msp_admin` and `msp_superuser` roles defined in Managed Service for PostgreSQL.

* `msp_admin` gives the following privileges:

  * `pg_monitor` and `pg_signal_backend` [predefined roles](https://www.postgresql.org/docs/current/predefined-roles.html).
  * Subscription for logical replication (`CREATE | DROP | ALTER SUBSCRIPTION`).
  * Ability to enable [extensions](https://docs.nebius.com/postgresql/databases/extensions.md) (`CREATE EXTENSION`).
  * Extension-specific functions: `pg_stat_reset()` and `pg_stat_statements_reset()` from the [pg\_stat\_statements](https://www.postgresql.org/docs/16/pgstatstatements.html) extension.

* `msp_superuser` enables you to bypass ownership verification when you grant and revoke privileges.

When you connect as the bootstrap user and create new users, you can grant them the `msp_admin` role but not the `msp_superuser` role.

## How to manage users

### Create a new user

1. [Connect](https://docs.nebius.com/postgresql/databases/connect.md) to the cluster via psql as a user with administrative privileges (for example, the bootstrap user).

2. Create a new user with privileges to connect to a `<test_db>` database. Execute the following SQL statements:

   ```sql theme={null}
   CREATE USER <db_user> PASSWORD '<password>';
   GRANT CONNECT ON DATABASE <test_db> TO <db_user>;
   ```

   `<db_user>` can connect to the `<test_db>` database and work with the data.

   The following usernames are reserved, do not specify them: `admin`, `repl`, `monitor`, `postgres`, `public` and `none`.

3. (Optional) If you need to grant them additional privileges for the database:

   1. Connect to the cluster as the user that owns the `<test_db>` database. Usually, the database owner is the user who created it.

      Alternatively, connect as the bootstrap user to bypass the database ownership check.

   2. Execute the following SQL statement:

      ```sql theme={null}
      GRANT ALL PRIVILEGES ON DATABASE <test_db> TO <db_user>;
      ```

See more details on user roles and privileges in the [PostgreSQL documentation](https://www.postgresql.org/docs/16/user-manag.html).

### Create a new user with administrative privileges

To create a user with administrative privileges, connect as the bootstrap user and execute the following SQL statements:

```sql theme={null}
CREATE USER <new_admin> CREATEDB CREATEROLE PASSWORD '<password>';
GRANT msp_admin TO <new_admin>;
```

`<new_admin>` can create databases, create users and grant them privileges. The `msp_admin` role lets them bypass checks when interacting with data.

You cannot grant the `msp_superuser` role. You can grant any [predefined roles](https://www.postgresql.org/docs/current/predefined-roles.html) except for the following:

* `role_pg_read_server_files`
* `role_pg_write_server_files`
* `role_pg_execute_server_program`
* `role_pg_read_all_data`
* `role_pg_write_all_data`

The following usernames are reserved, do not specify them: `admin`, `repl`, `monitor`, `postgres`, `public` and `none`.

### Manage the bootstrap user

> [!WARNING]
>
> Change the password for the bootstrap user only via Nebius AI Cloud interfaces (web console, CLI and provider for Terraform). Don't change it by using SQL statements, as the password will eventually be reset to the one created via Nebius AI Cloud interfaces.

**Web console**

To change the password of the bootstrap user:

1. In the sidebar, go to  **PostgreSQL**.
2. Click your cluster and go to **Settings**.
3. In the **Database** section, enter the new password.
4. Click **Update cluster**.

**CLI**

To change the password of the bootstrap user, run the following command:

```bash theme={null}
nebius msp postgresql v1alpha1 cluster update \
   --id <cluster_ID> \
   --parent-id <project_ID> \
   --bootstrap-user-password <new_password>
```

**Terraform**

To change the password of the bootstrap user:

1. In your Terraform configuration (`main.tf`), change the value of `bootstrap.user_password` within the `nebius_msp_postgresql_v1alpha1_cluster` [resource](https://docs.nebius.com/terraform-provider/reference/resources/msp_postgresql_v1alpha1_cluster.md#nested-schema-for):

   ```terraform theme={null}
   resource "nebius_msp_postgresql_v1alpha1_cluster" "<cluster_name>" {
     ...
     bootstrap = {
       db_name       = "<default_db_name>"
       user_name     = "<bootstrap_username>"
       user_password = "<new_password>"
     }
     ...
   }
   ```

2. Update the configuration:

   ```bash theme={null}
   terraform apply
   ```

### Delete a user

> [!WARNING]
>
> Do not delete the bootstrap user, as this may cause the service to malfunction.

To delete a user, connect to the cluster as a user with administrative privileges and execute the following SQL statement:

```sql theme={null}
DROP USER <username>;
```

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
