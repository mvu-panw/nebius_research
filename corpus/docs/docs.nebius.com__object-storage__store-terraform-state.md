# How to store a Terraform state in an Object Storage bucket

Source: https://docs.nebius.com/object-storage/store-terraform-state

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to store a Terraform state in an Object Storage bucket

When you create Nebius AI Cloud infrastructure by using a [Terraform provider](https://docs.nebius.com/terraform-provider/index.md), you declare the desired infrastructure state in `.tf` files. Next, Terraform applies the changes and stores the current infrastructure state in a `.tfstate` file.

For shared environments or automated workflows, it is a good practice to store the `.tf` files under version control (for example, in a Git repository) and to store the `.tfstate` files in S3-compatible storage. As a result, several users or automation systems can access and update the same infrastructure state safely. Also, you can [lock the state](https://developer.hashicorp.com/terraform/language/state/locking) to prevent conflicting changes.

In Nebius AI Cloud, you can store the `.tfstate` file in an [Object Storage bucket](https://docs.nebius.com/object-storage/overview.md#buckets). The Terraform state is uploaded to the bucket and is updated automatically every time you make changes in your resources in configuration files.

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. [Create a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#create) to store the state.

   > [!NOTE]
   >
   > [Terraform](https://developer.hashicorp.com/terraform/language/backend/s3) recommends that you enable versioning for the bucket. However, storing multiple versions of objects in a bucket increases your [costs](https://docs.nebius.com/object-storage/resources/pricing.md).

3. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#create) that accesses the bucket.

4. [Create an access key](https://docs.nebius.com/iam/service-accounts/access-keys.md#create) for this service account and save the AWS-like ID and secret.

5. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

## How to store the Terraform state file

1. Create a working directory on your local machine. If you intend to use version control, store this directory in a repository.

2. In this directory, create the `terraform.tf` file with the following contents:

   ```hcl theme={null}
   terraform {
     required_providers {
       nebius = {
         source  = "nebius/nebius"
         version = ">= 0.6.8"
       }
     }

     backend "s3" {
       bucket  = "<your_bucket_name>"
       key     = "<path_to_store_tfstate>"
       region  = "eu-north1"

       access_key = "<AWS-like_key_ID>"
       secret_key = "<AWS-like_key_secret>"

       endpoints = {
         s3 = "https://storage.eu-north1.nebius.cloud"
       }

       # Lock the state from concurrent modifications
       use_lockfile = true

       # These settings stop Terraform from AWS-specific checks
       # that are not relevant for Nebius AI Cloud
       skip_credentials_validation = true
       skip_region_validation      = true
       skip_requesting_account_id  = true
       skip_metadata_api_check     = true
     }
   }
   ```

   In this file, specify the following parameters:

   * `bucket`: Bucket name.
   * `key`: Path where the state should be stored, relative to the bucket root.
   * `access_key` and `secret_key`: AWS-like ID and secret to access the bucket.

3. Prepare the [authentication file](https://docs.nebius.com/terraform-provider/authentication.md) `provider "nebius" {}`.

4. Create configuration files for the infrastructure that you need to deploy. To get acquainted with an example of such infrastructure and files, see [How to create resources by using the Nebius AI Cloud provider for Terraform](https://docs.nebius.com/terraform-provider/manage/create-resources.md).

5. Initialize Terraform in the working directory:
   ```bash theme={null}
   terraform init
   ```

6. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

7. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

Terraform creates the required infrastructure and stores its state in a `.tfstate` file that is placed in the bucket you specified.

After that, when you want to update the infrastructure and change its configuration files, use the same `terraform.tf` file. When you run `terraform apply`, Terraform pulls the latest remote state from the bucket and shows the plan of the changes.
