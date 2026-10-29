# Connecting to databases in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/databases/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Connecting to databases in Managed Service for PostgreSQL®

To work with a database in a Managed Service for PostgreSQL cluster, you need to connect to it.

## Prerequisites

1. [Create a cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters) and securely store the password you specified during creation.

2. To connect to a database, install `psql`, a PostgreSQL command line client:

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

3. To secure connections to databases, install the Nebius AI Cloud certificate:
   ```bash theme={null}
   mkdir -p ~/.postgresql \
   curl "https://storage.eu-north1.nebius.cloud/msp-certs/ca.pem" \
      -o ~/.postgresql/root.crt \
   chmod 0600 ~/.postgresql/root.crt
   ```
   This command creates the `.postgresql` folder, downloads the certificate into it and then sets the access rights to the certificate file.

## How to connect to a database

Go to the web console and get the connection command with all data filled in for your cluster:

**Web console**

1. In the sidebar, go to  **PostgreSQL**.
2. Click your cluster.
3. Click **How to connect**.
4. Copy the connection command from the window that opens.

Enter this command in the terminal. You will be asked for the password you specified when [creating the cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters).

### Details of the connection command

The connection command that you copy from the web console looks like this:

```bash theme={null}
psql "host=<cluster_endpoint> \
  port=5432 \
  sslmode=verify-full \
  dbname=<DB_name> \
  user=<username>"
```

It contains the following parameters:

* `<DB_name>`: Default database name that you specified when creating the cluster. If you created another database in this cluster, you can use its name instead.

* `<username>`: The username you specified when creating the cluster.

  > [!NOTE]
  >
  > Once you create other databases and [users](https://docs.nebius.com/postgresql/databases/users.md#create-a-new-user), you can use their names instead.

* `<cluster_endpoint>`: Depends on where you are connecting from:

  * To connect from the internet, use the public cluster endpoint. You can connect from the internet only if you enabled public access to the cluster when you created it.
  * To connect from other Nebius AI Cloud resources, use the private cluster endpoint.

To get the endpoints:

**Web console**

1. In the sidebar, go to  **PostgreSQL**.
2. Click your cluster.
3. Click **Copy endpoint URL** and select **Public RW endpoint URL** to copy the public cluster endpoint, or **Private RW endpoint URL** to copy the private cluster endpoint.

**CLI**

Get the URLs from cluster data:

```bash theme={null}
nebius msp postgresql v1alpha1 cluster get-by-name \
  --name <cluster_name> \
  --format jsonpath='{.status.connection_endpoints.public_read_write}'

nebius msp postgresql v1alpha1 cluster get-by-name \
  --name <cluster_name> \
  --format jsonpath='{.status.connection_endpoints.private_read_write}'
```

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
