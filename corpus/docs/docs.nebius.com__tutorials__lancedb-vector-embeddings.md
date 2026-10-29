# Using LanceDB and Object Storage to generate, persist and query vector embeddings

Source: https://docs.nebius.com/tutorials/lancedb-vector-embeddings

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Using LanceDB and Object Storage to generate, persist and query vector embeddings

Vector embeddings turn text, images and other unstructured data into numerical vectors that you can search by similarity, which is the basis for semantic search and retrieval-augmented generation (RAG). This tutorial shows you how to use [LanceDB](https://lancedb.com/) with [Object Storage](https://docs.nebius.com/object-storage.md) as a persistent vector store. LanceDB writes tables directly to an [Object Storage](https://docs.nebius.com/object-storage.md) bucket, each containing vector embeddings alongside structured metadata, with no separate database server to run or manage. Object Storage exposes an [S3-compatible API](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md), so LanceDB connects to it with no additional drivers. This tutorial uses the **Enhanced Throughput** storage class because it is well suited for streaming embeddings or model weights at scale and for latency-sensitive queries. By the end of this tutorial, you will have LanceDB reading and writing vector data to an Object Storage bucket in Nebius AI Cloud and will have run a nearest-neighbor similarity search against that data.

## Costs

Nebius AI Cloud charges for the following resources used in this tutorial:

* [Object Storage](https://docs.nebius.com/object-storage/resources/pricing.md): storage consumed by LanceDB files written to your bucket.

## Prerequisites

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
* Create resources in a project in one of the available [regions](https://docs.nebius.com/overview/regions.md), such as `eu-north1`.
* Python 3.9 or later installed locally or a running [JupyterLab® Devlab](https://docs.nebius.com/serverless/quickstart/devlabs.md).

## Steps

### Create an Object Storage bucket

1. In the [web console](https://console.nebius.com), go to  **Object Storage** and click **Create bucket**.

2. Enter a name for the bucket, for example `lancedb-data`.

3. Select **Enhanced Throughput** for the storage class.

   > [!NOTE]
   >
   > You can use the Standard storage class instead, but Enhanced Throughput works better for this workflow. For a comparison, see [Storage classes in Object Storage](https://docs.nebius.com/object-storage/storage-classes.md).

4. Click **Create bucket**.

### Create a service account and grant it access to the bucket

LanceDB needs credentials to read and write objects. Create a dedicated [service account](https://docs.nebius.com/iam/service-accounts/manage.md), put it in its own [group](https://docs.nebius.com/iam/authorization/groups/members.md) and grant that group access to the bucket you created.

1. Create a service account:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account create \
     --name lancedb-sa \
     --format jsonpath='{.metadata.id}')
   ```

2. Create a group for the service account and add the account to it:

   ```bash theme={null}
   export PROJECT_ID=$(nebius config get parent-id)
   export TENANT_ID=$(nebius iam project get $PROJECT_ID \
     --format jsonpath='{.metadata.parent_id}')
   export GROUP_ID=$(nebius iam group create \
     --name lancedb-access --parent-id $TENANT_ID \
     --format jsonpath='{.metadata.id}')
   nebius iam group-membership create \
     --parent-id $GROUP_ID \
     --member-id $SA_ID
   ```

3. Look up the bucket ID and grant the group read and write access scoped to the bucket:

   ```bash theme={null}
   export BUCKET_ID=$(nebius storage bucket get-by-name \
     --name lancedb-data \
     --format jsonpath='{.metadata.id}')
   nebius storage bucket update --id $BUCKET_ID \
     --bucket-policy-rules "[{\"paths\":[\"*\"],\"roles\":[\"storage.editor\"],\"group_id\":\"$GROUP_ID\"}]"
   ```

   The `storage.editor` role in this [bucket policy](https://docs.nebius.com/object-storage/buckets/bucket-policy.md) lets the service account read and write objects in this bucket only.

4. Create an [access key](https://docs.nebius.com/iam/service-accounts/access-keys.md) and save the credentials:

   ```bash theme={null}
   export ACCESS_KEY_ID=$(nebius iam v2 access-key create \
     --account-service-account-id $SA_ID \
     --description 'LanceDB' \
     --format jsonpath='{.metadata.id}')
   export AWS_ACCESS_KEY_ID=$(nebius iam v2 access-key get \
     --id $ACCESS_KEY_ID \
     --format jsonpath='{.status.aws_access_key_id}')
   export AWS_SECRET_ACCESS_KEY=$(nebius iam v2 access-key get \
     --id $ACCESS_KEY_ID \
     --format jsonpath='{.status.secret}')
   ```

   Save the values of `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` somewhere secure — the secret is shown only once.

### Install LanceDB

Install LanceDB dependencies for your platform of choice:

**Python**

```bash theme={null}
pip install lancedb pandas
```

**TypeScript**

```bash theme={null}
npm install @lancedb/lancedb
```

### Connect LanceDB to Object Storage

Open a script or notebook and connect LanceDB to your bucket. The endpoint follows the pattern `https://storage.<region_ID>.nebius.cloud`. Replace `<bucket_name>`, `<region_ID>`, `<access_key_ID>` and `<secret_access_key>` with your values.

**Python**

```python theme={null}
import lancedb

db = lancedb.connect(
    "s3://<bucket_name>/lancedb",
    storage_options={
        "region": "<region_ID>",
        "endpoint": "https://storage.<region_ID>.nebius.cloud",
        "aws_access_key_id": "<access_key_ID>",
        "aws_secret_access_key": "<secret_access_key>",
    },
)
```

**TypeScript**

```typescript theme={null}
import * as lancedb from "@lancedb/lancedb";

const db = await lancedb.connect("s3://<bucket_name>/lancedb", {
  storageOptions: {
    region: "<region_ID>",
    endpoint: "https://storage.<region_ID>.nebius.cloud",
    awsAccessKeyId: "<access_key_ID>",
    awsSecretAccessKey: "<secret_access_key>",
  },
});
```

> [!NOTE]
>
> You can supply credentials via environment variables instead of `storage_options`. If `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` and `AWS_ENDPOINT` are set in your shell, you can call `lancedb.connect("s3://<bucket_name>/lancedb")` with no additional options.

### Create a table and insert vectors

Create a table with a vector column and a metadata column, then insert a few rows. In this tutorial, random vectors are used to keep the example self-contained.

> [!TIP]
>
> In a real application you would generate embeddings using a model deployed via [Serverless AI](https://docs.nebius.com/serverless/overview.md) or running locally with [SentenceTransformers](https://sbert.net). For a Serverless AI example, see the tutorial on [Building a RAG electronics store chatbot](https://docs.nebius.com/tutorials/rag.md).

**Python**

```python theme={null}
import numpy as np

data = [
    {"id": 1, "text": "Nebius Object Storage", "vector": np.random.rand(128).tolist()},
    {"id": 2, "text": "LanceDB vector database", "vector": np.random.rand(128).tolist()},
    {"id": 3, "text": "Serverless AI embeddings", "vector": np.random.rand(128).tolist()},
]

table = db.create_table("documents", data=data)
print(f"Table created with {table.count_rows()} rows.")
```

**TypeScript**

```typescript theme={null}
const data = [
  { id: 1, text: "Nebius Object Storage", vector: Array.from({ length: 128 }, Math.random) },
  { id: 2, text: "LanceDB vector database", vector: Array.from({ length: 128 }, Math.random) },
  { id: 3, text: "Serverless AI embeddings", vector: Array.from({ length: 128 }, Math.random) },
];

const table = await db.createTable("documents", data);
console.log(`Table created with ${await table.countRows()} rows.`);
```

LanceDB writes the table as Lance files under `s3://<bucket_name>/lancedb/documents.lance/`. You can verify this in the [web console](https://console.nebius.com) under **Object Storage** → your bucket.

### Run a similarity search

Query the table for the rows nearest to a query vector:

**Python**

```python theme={null}
query_vector = np.random.rand(128).tolist()

results = (
    table.search(query_vector)
         .limit(2)
         .select(["id", "text", "_distance"])
         .to_pandas()
)
print(results)
```

**TypeScript**

```typescript theme={null}
const queryVector = Array.from({ length: 128 }, Math.random);

const results = await table
  .search(queryVector)
  .limit(2)
  .select(["id", "text", "_distance"])
  .toArray();

console.log(results);
```

The output shows the two nearest rows along with their `_distance` score. Because the data in this example is random, the distances have no semantic meaning — in a real application, vectors would come from an embedding model and low distances would indicate semantic similarity.

### Reconnect to an existing table

LanceDB tables persist in Object Storage. To reopen a table in a later session, reconnect with the same credentials and call `open_table`:

**Python**

```python theme={null}
db = lancedb.connect(
    "s3://<bucket_name>/lancedb",
    storage_options={
        "region": "<region_ID>",
        "endpoint": "https://storage.<region_ID>.nebius.cloud",
        "aws_access_key_id": "<access_key_ID>",
        "aws_secret_access_key": "<secret_access_key>",
    },
)
table = db.open_table("documents")
print(table.count_rows())
```

**TypeScript**

```typescript theme={null}
const db = await lancedb.connect("s3://<bucket_name>/lancedb", {
  storageOptions: {
    region: "<region_ID>",
    endpoint: "https://storage.<region_ID>.nebius.cloud",
    awsAccessKeyId: "<access_key_ID>",
    awsSecretAccessKey: "<secret_access_key>",
  },
});
const table = await db.openTable("documents");
console.log(await table.countRows());
```

## How to delete the created resources

Object Storage is a chargeable resource. If you no longer need the data, [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) the bucket to stop incurring charges.

## See also

* [LanceDB storage configuration](https://docs.lancedb.com/storage/configuration)
* [Object Storage overview](https://docs.nebius.com/object-storage.md)
* [Amazon S3 API Compatibility Reference](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md)
* [Serverless AI](https://docs.nebius.com/serverless/overview.md) — use Nebius-hosted embedding models to generate vectors for your LanceDB tables

***

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
