# Getting started with Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Managed Service for PostgreSQL®

Modern AI and ML workloads operate with sizable datasets. Managed Service for PostgreSQL allows you to apply its flexibility and dataset management capabilities to enhance the performance of your projects in Nebius AI Cloud.

This guide will get you started with Managed Service for PostgreSQL. You will:

* Install and configure CLIs to work with Managed Service for PostgreSQL
* Create your first cluster
* Connect to the cluster
* Perform basic operations with a PostgreSQL database

> [!TIP]
>
> If you want to move data from an external PostgreSQL cluster to a Managed PostgreSQL cluster, use [migration](https://docs.nebius.com/postgresql/data-transfers/migrate-data.md) or [replication](https://docs.nebius.com/postgresql/replication/from-external.md).

## Prepare your environment

Before moving on with this guide, make sure you have the `postgresql` package installed. You will need it to [connect to your cluster](#connect-to-your-cluster) and [test a database within it](#perform-operations-with-a-test-database).

### Install postgresql package

**macOS**

1. Ensure you have [Homebrew](https://brew.sh) installed.

2. Run the command to install PostgreSQL CLI:

   ```sh theme={null}
   brew install libpq
   ```

**Ubuntu**

Run the command to install PostgreSQL CLI:

```sh theme={null}
sudo apt update && sudo apt install -y postgresql-client
```

### (Optional) Install the Nebius AI Cloud CLI or provider for Terraform

If you want to manage clusters and other Nebius AI Cloud resources in the command line or using Terraform, install and configure one of these tools:

* [Nebius AI Cloud CLI](https://docs.nebius.com/cli/install.md)
* [Nebius AI Cloud provider for Terraform](https://docs.nebius.com/terraform-provider/install.md)

## Create a cluster

**Web console**

1. In the sidebar, go to  **PostgreSQL**.

2. Click  **Create cluster**.

3. On the page that opens:

   1. Specify the **Name** for your cluster. Do not use spaces in cluster names.

   2. Write a short **Description** of your cluster. For example, `My first Managed Service for PostgreSQL cluster`.

   3. In the **Username** field, type the username.

   4. In the **Password** field, come up with a secure password. Such a password must contain at least:

      * 8 characters
      * One lowercase character
      * One uppercase character
      * One special character

   5. Keep all the other settings with their default values — they will be more than enough for the purposes of this guide.

   6. Click **Create cluster**.

On the **Managed Service for PostgreSQL®** page, you will see your cluster with the `Provisioning` status.

Please wait until its status changes to `Running` before trying to perform any operations on your new cluster.

**CLI**

1. Prepare environment variables:

   1. Come up with a name for your Managed Service for PostgreSQL cluster:

      ```bash theme={null}
      export CLUSTER_NAME=<new_PostgreSQL_cluster_name>
      ```

      Do not use spaces in your cluster names.

   2. Copy the network ID from the [Network](https://console.nebius.com/network) section of the web console and save it to an environment variable:

      ```bash theme={null}
      export NETWORK_ID=<network_ID>
      ```

   3. Set the credentials for your Managed Service for PostgreSQL database: database name, your username and database password:

      ```bash theme={null}
      export BOOTSTRAP_DB_NAME=<PostgreSQL_database_name>
      export BOOTSTRAP_USER_NAME=<username>
      export BOOTSTRAP_USER_PASSWORD=<database_password>
      ```

2. Run the command to create a cluster:

   ```bash theme={null}
   nebius msp postgresql v1alpha1 cluster create \
     --name $CLUSTER_NAME \
     --description "My first PostgreSQL cluster" \
     --network-id $NETWORK_ID \
     --bootstrap-db-name $BOOTSTRAP_DB_NAME \
     --bootstrap-user-name $BOOTSTRAP_USER_NAME \
     --bootstrap-user-password $BOOTSTRAP_USER_PASSWORD \
     --config-version 16 \
     --config-template-disk-type network-ssd \
     --config-template-disk-size-gibibytes 96 \
     --config-template-resources-platform cpu-e2 \
     --config-template-resources-preset 2vcpu-8gb \
     --config-template-hosts-count 1 \
     --config-public-access
   ```

3. Wait for the operation to complete.

**Terraform**

The configuration below assumes that the [project](https://docs.nebius.com/iam/overview.md#projects) is stored in the [`project_id` input variable](https://developer.hashicorp.com/terraform/language/values/variables).

For more information about how to get the network ID, see the [instructions](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

```hcl theme={null}
resource "nebius_msp_postgresql_v1alpha1_cluster" "example_cluster" {
  parent_id   = var.project_id
  description = "My first Managed PostgreSQL cluster"
  name        = "postgres_cluster_example"
  network_id  = "<network_ID>"

  bootstrap = {
    db_name       = "<your_postgresql_db_name>"
    user_name     = "<your_username>"
    user_password = "<your_database_password>"
  }

  config = {
    template = {
      resources = {
        platform = "cpu-e2"
        preset   = "2vcpu-8gb"
      }
      disk = {
        size_gibibytes = 96
        type           = "network-ssd"
      }
      hosts = {
        count = 1
      }
    }
    version = "16"

    public_access = true
  }
}
```

For details about the `nebius_msp_postgresql_v1alpha1_cluster` Terraform resource, see the [provider reference](https://docs.nebius.com/terraform-provider/reference/resources/msp_postgresql_v1alpha1_cluster.md).

## Connect to your cluster

1. Open your cluster's page.

2. Under the cluster name, click **How to connect**.

3. Follow the instructions in the dialog window.

4. To check the connection, list all the databases on your cluster with the command:

   ```sh theme={null}
   \l
   ```

   You should see the following output:

   > **Output**
   >
   > ```sh theme={null}
   >                                 List of databases
   >     Name    |  Owner   | Encoding | Collate | Ctype |        Access privileges
   > ------------+----------+----------+---------+-------+----------------------------------
   >  postgres   | postgres | UTF8     | C       | C     | =Tc/postgres                    +
   >             |          |          |         |       | postgres=CTc/postgres           +
   >             |          |          |         |       | cnpg_pooler_pgbouncer=c/postgres
   >  template0  | postgres | UTF8     | C       | C     | =c/postgres                     +
   >             |          |          |         |       | postgres=CTc/postgres
   >  template1  | postgres | UTF8     | C       | C     | =c/postgres                     +
   >             |          |          |         |       | postgres=CTc/postgres
   > ```

## Perform operations with a test database

In this guide, we'll use the `dellstore2` dataset. It contains a fictional store database with products, orders, inventory and customer information.

1. Download the [dellstore2-normal-1.0.tar.gz](https://www.postgresql.org/ftp/projects/pgFoundry/dbsamples/dellstore2/dellstore2-normal-1.0/) file from the PostgreSQL website.

2. Extract the file into a folder.

3. From the folder to which you extracted the file, connect to your Managed Service for PostgreSQL cluster with the Nebius AI Cloud CLI and create a database on your cluster:

   ```sql theme={null}
   CREATE DATABASE dellstore;
   ```

4. Upload the dataset from the file onto your cluster:

   ```sh theme={null}
   \i dellstore2-normal-1.0.sql;
   ```

5. Check if the objects were created successfully:

   ```sh theme={null}
   \d
   ```

   You should see the following output:

   > **Output**
   >
   > ```sh theme={null}
   >                     List of relations
   >  Schema |           Name           |   Type   |      Owner
   > --------+--------------------------+----------+-----------------
   >  public | categories               | table    | <your_username>
   >  public | categories_category_seq  | sequence | <your_username>
   >  public | cust_hist                | table    | <your_username>
   >  public | customers                | table    | <your_username>
   >  public | customers_customerid_seq | sequence | <your_username>
   >  public | inventory                | table    | <your_username>
   >  public | items                    | table    | <your_username>
   >  public | orderlines               | table    | <your_username>
   >  public | orders                   | table    | <your_username>
   >  public | orders_orderid_seq       | sequence | <your_username>
   >  public | products                 | table    | <your_username>
   >  public | products_prod_id_seq     | sequence | <your_username>
   >  public | reorder                  | table    | <your_username>
   > (13 rows)
   > ```

6. Write a row into the `products` table:

   ```sql theme={null}
   INSERT INTO products(
       prod_id,
       category,
       title,
       actor,
       price,
       special,
       common_prod_id
   )
   VALUES (
       10001,
       42,
       'FUTURE INTELLIGENCE',
       'FORD PREFECT',
       42.42,
       0,
       1978
   );
   ```

7. Query the database to see that your row was written correctly:

   ```sql theme={null}
   SELECT * FROM products WHERE prod_id = 10001;
   ```

   You should get the following output:

   ```sh theme={null}
    prod_id | category |        title        |    actor     | price | special | common_prod_id
   ---------+----------+---------------------+--------------+-------+---------+----------------
      10001 |       42 | FUTURE INTELLIGENCE | FORD PREFECT | 42.42 |       0 |           1978
   (1 row)
   ```

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
