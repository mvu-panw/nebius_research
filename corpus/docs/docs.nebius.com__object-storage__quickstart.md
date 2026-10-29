# How to get started with Object Storage: Create your first bucket

Source: https://docs.nebius.com/object-storage/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to get started with Object Storage: Create your first bucket

Most ML/AI workloads involve large files, such as datasets and artifacts of trained models. To efficiently store, access and share them, you can use Object Storage, a simple storage service offered by Nebius AI Cloud.

In this guide, you will learn how to start using Object Storage. You will set up your environment to work with Object Storage, create your first *bucket*, a data container and upload a test file.

For visual guidance on creating a bucket and uploading objects in the web console, watch the video below. If you prefer other interfaces or written instructions, follow the steps further down.

[YouTube video player](https://www.youtube.com/embed/Cx7BlL6PdKk)

Visit [Nebius Academy](https://academy.nebius.com/trainer/nebius-ai-cloud-onboarding/lesson/b532ba82-1b87-4d8c-ae82-f99afa32d04d) for video tutorials to help you get started with Nebius AI Cloud.

## Prepare your environment

Make sure that you meet the prerequisites for your preferred interface:

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Nebius AI Cloud CLI**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

In this guide, you will use the terminal in your environment, for example on your local machine, to run commands that create and manage Nebius AI Cloud resources. The commands use certain command line interfaces (CLIs) and tools that you need to install first. Here are all the installation commands in a single copy-and-paste block:

```bash Ubuntu theme={null}
sudo apt-get install unzip jq
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
curl -sSL https://artifacts.nebius.cloud/cli/install.sh | bash
nebius profile create
```

```bash macOS theme={null}
brew install jq
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
curl -sSL https://artifacts.nebius.cloud/cli/install.sh | bash
nebius profile create
```

These commands will install the following:

* **AWS CLI** ([how to install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)) manages buckets and objects: Object Storage is compatible with Amazon S3. For Linux, the AWS CLI is distributed in a ZIP archive, so the commands also install the `unzip` package.
* **jq** ([how to install](https://jqlang.github.io/jq/download/)) parses JSON outputs from the Nebius AI Cloud CLI and extracts resource IDs for other commands.
* **Nebius AI Cloud CLI** ([how to install](https://docs.nebius.com/cli/install.md)) manages all Nebius AI Cloud resources. In this guide, the CLI is used to create access-related resources. It can also be used for creating and modifying Object Storage buckets, but not for uploading objects.

The last command, `nebius profile create`, will guide you through several prompts. After you complete the prompts, your browser will open the Nebius AI Cloud web console sign-in screen. Sign in to the web console to complete the initialization. If you have access to multiple tenants, the CLI will prompt you to choose a tenant ID. After that, save your project ID in the CLI configuration.

If the project ID hasn't been configured during the `nebius profile create` flow, [get the project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) and save it in the CLI configuration:

```bash theme={null}
nebius config set parent-id <project_ID>
```

## Configure access, credentials and AWS CLI settings

> [!NOTE]
>
> If you are using the [web console](https://console.nebius.com), you can skip this step and proceed to [creating a bucket](#create-a-bucket-and-upload-a-file-to-it).

1. Create a service account and save its ID to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account create \
     --name object-storage-sa \
     --format jsonpath='{.metadata.id}')
   ```

2. Grant edit access to the service account:

   1. Get the tenant ID:

      ```bash theme={null}
      export PROJECT_ID=$(nebius config get parent-id)
      export TENANT_ID=$(nebius iam project get $PROJECT_ID --format jsonpath='{.metadata.parent_id}')
      ```

   2. Get the ID of the default `editors` group:

      ```bash theme={null}
      export EDITORS_GROUP_ID=$(nebius iam group get-by-name \
        --name editors --parent-id $TENANT_ID \
        --format jsonpath='{.metadata.id}')
      ```

   3. Add the service account to `editors` group:

      ```bash theme={null}
      nebius iam group-membership create \
        --parent-id $EDITORS_GROUP_ID \
        --member-id $SA_ID
      ```

3. Create an [access key](https://docs.nebius.com/iam/service-accounts/access-keys.md) for the service account and get its AWS-like ID and contents:

   ```bash theme={null}
   export ACCESS_KEY_ID=$(nebius iam v2 access-key create \
     --account-service-account-id $SA_ID \
     --description 'AWS CLI' \
     --format json | jq -r '.metadata.id')
   export ACCESS_KEY_AWS_ID=$(nebius iam v2 access-key get \
     --id $ACCESS_KEY_ID \
     --format json | jq -r '.status.aws_access_key_id')
   export SECRET_ACCESS_KEY=$(nebius iam v2 access-key get \
     --id $ACCESS_KEY_ID \
     --format json | jq -r '.status.secret')
   ```

4. Add the key to the AWS CLI configuration:

   ```bash theme={null}
   aws configure set aws_access_key_id $ACCESS_KEY_AWS_ID
   aws configure set aws_secret_access_key $SECRET_ACCESS_KEY
   ```

5. Depending on your project [region](https://docs.nebius.com/overview/regions.md), add the Nebius AI Cloud region ID and the Object Storage endpoint URL to the AWS CLI configuration:

   ```bash theme={null}
   aws configure set region <region_ID>
   aws configure set endpoint_url https://storage.<region_ID>.nebius.cloud
   ```

   For example, run the following commands for a project in `eu-north1`:

   ```bash theme={null}
   aws configure set region eu-north1
   aws configure set endpoint_url https://storage.eu-north1.nebius.cloud
   ```

## Create a bucket and upload a file to it

In Object Storage, a bucket is a container for *objects*. An object, in turn, is a file together with its metadata such as the file name (it is called *object key* in Object Storage terms). You can use the [web console](https://console.nebius.com) or the AWS CLI to create buckets and upload objects.

**Web console**

1. Create a bucket:
   1. In the sidebar, go to  **Storage** → **Object Storage**.

   2. Click **Create resource** → **Bucket**.

   3. (Optional) Specify the bucket name.

      The bucket name must be unique across the region. For more information, see [Naming](https://docs.nebius.com/object-storage/overview.md#naming).

   4. Set the [bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters).

   5. Click **Create bucket**.
2. Upload a file:

   1. Click  **Add** → **Object**.
   2. In the window that opens, select the file to upload.
   3. Click **Upload**.
3. Check that the **Objects** tab shows the new object.

**AWS CLI**

1. Create a bucket:

   ```bash theme={null}
   aws s3 mb s3://quickstart-bucket
   ```

2. Upload an object:

   ```bash theme={null}
   echo 'Hello world!' > test.txt
   aws s3 cp test.txt s3://quickstart-bucket/test.txt
   ```

3. To make sure that the object has been uploaded, list the objects in the bucket:

   ```bash theme={null}
   aws s3 ls s3://quickstart-bucket
   ```
