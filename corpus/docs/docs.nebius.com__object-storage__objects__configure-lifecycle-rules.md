# How to configure lifecycle rules in Object Storage

Source: https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to configure lifecycle rules in Object Storage

You can configure the following [lifecycle rules](https://docs.nebius.com/object-storage/objects/lifecycles.md):

* [Expiration lifecycle rules](#how-to-configure-expiration-lifecycle-rules) if you want to delete unnecessary objects and versions.
* [Transition lifecycle rules](#how-to-configure-transition-lifecycle-rules) if you want to change a [storage class](https://docs.nebius.com/object-storage/storage-classes.md) of objects.

We recommend using Nebius AI Cloud interfaces: the [web console](https://console.nebius.com), the [Nebius AI Cloud CLI](https://docs.nebius.com/cli/index.md) or the [provider for Terraform](https://docs.nebius.com/terraform-provider/index.md). The AWS CLI is supported but with limited availability of features.

## How to configure expiration lifecycle rules

> [!WARNING]
>
> When you configure expiration rules, make sure that only the required objects and versions fall under these rules. Otherwise, you can unintentionally delete objects that must be preserved.

**Web console**

In the web console, you can only add lifecycle rules to existing buckets. You cannot create a bucket with a lifecycle rule.

To add an expiration lifecycle rule to a bucket:

1. In the web console, go to  **Storage** → **Object Storage**.

2. Open the page of the required bucket.

3. Go to the **Lifecycle rules** tab.

4. Click  **Add rule**.

5. (Optional) On the page that opens, specify the rule name. It helps identify the rule in a list of lifecycle rules.

6. Specify which objects the rule applies to:

   * **Object key prefix**: The rule applies to objects whose names begin with a specified prefix. For instance, if you set the `expiring/` prefix, the rule applies to the `expiring/test.txt` object and doesn't apply to the `test.txt` object.

   * **Minimum size, bytes**: The rule applies to objects larger than the specified size.

   * **Maximum size, bytes**: The rule applies to objects smaller than the specified size.

     If you set both a minimum and maximum size, make sure that the maximum size is greater than or equal to the minimum one.

   * **Tags**: The rule applies to objects with the specified tags.

     A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

7. Set the actions that the lifecycle rule should perform:

   * **Expiration**: Delete objects and versions several days after the object upload or on a certain date. For example, you can delete objects five days after their upload.
   * **Non-current version expiration**: If you [enabled versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) in your bucket, you can delete all versions except for the current one. To make them expire several days after the object upload, specify the required number of days.
   * **Abort of incomplete multipart upload**: Remove multipart uploads that fail and remain stale. If they take longer than the specified number of days, Object Storage aborts multipart uploads and deletes all the data uploaded.

8. Click **Add rule**.

**Nebius AI Cloud CLI**

When you update the settings of a bucket, make sure to list all lifecycle rules, even the ones that you do not change. If you do not include some rules, Object Storage will delete them.

When you reconfigure a rule, specify only the parameters that you want to change. For example, if you earlier set a filter of objects in a rule and you want to change an expiration condition, specify only the condition, and the rule name or ID. You do not need to set the filter again as it will be preserved.

To create an expiration lifecycle rule:

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. If you update the settings of an existing bucket, get a list of its lifecycle rules:
   ```bash theme={null}
   nebius storage bucket get-by-name --name <bucket_name>
   ```
   The rules are specified in the `spec.lifecycle_configuration.rules` parameter. If you want to preserve them when adding a new rule, duplicate those rules in the `update` command.
3. To configure a new lifecycle rule, run one of the following commands:

   * Create a bucket with a lifecycle rule:

     ```bash theme={null}
     nebius storage bucket create --name <bucket_name> \
       --lifecycle-configuration-rules '[
       {
          "id": "<rule_ID>",
          "status": "enabled",
          <rule_conditions>
       },
       {
         <rules_created_earlier>
       },
       ...
     ]'
     ```

   * Add a rule to an existing bucket:

     ```bash theme={null}
     nebius storage bucket update --id <bucket_ID> \
       --lifecycle-configuration-rules '[
       {
          "id": "<rule_ID>",
          "status": "enabled",
          <rule_conditions>
       },
       {
         <rules_created_earlier>
       },
       ...
     ]'
     ```

     In the `--id` parameter, specify the bucket ID. To get it, run `nebius storage bucket get-by-name --name <bucket_name>`.

   Every rule contains the following parameters:

   * `id`: Rule ID (string). Helps identify the rule in the list of lifecycle rules.
   * `status`: Whether the rule is enabled or disabled. Use the `disabled` status to turn the rule off but preserve it in the list.

   To set the rule conditions, use the examples below and insert them into the command instead of `<rule_conditions>`. You can combine and adapt these examples to your needs.

   * To delete objects five days after their upload, specify:

     ```json theme={null}
     "expiration": {
        "days": 5
     }
     ```

   * To delete objects whose names begin with a certain prefix, specify:

     ```json theme={null}
     "filter": {
        "prefix": "expiring/"
     },
     "expiration": {
        "days": 5
     }
     ```

     For instance, if you set the `expiring/` prefix, the `expiring/test.txt` object will be deleted five days after the upload, and the `test.txt` object will not.

   * To delete objects that exceed 5120 bytes:

     ```json theme={null}
     "filter": {
        "object_size_greater_than_bytes": 5120
     },
     "expiration": {
        "days": 5
     }
     ```

     The service applies the rule five days after the object upload.

   * To delete objects that are less than 128 bytes:

     ```json theme={null}
     "filter": {
        "object_size_less_than_bytes": 128
     },
     "expiration": {
        "days": 5
     }
     ```

   * To delete objects with certain tags, specify:

     ```json theme={null}
     "filter": {
         "tags": [
            {"key": "key1", "value": "value1"},
            {"key": "key2", "value": "value2"}
         ]
     },
     "expiration": {
        "days": 5
     }
     ```

     A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

   * If you [enabled versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) in your bucket, you can delete outdated versions. These are often all the versions except for the current one. To make them expire five days after they are no longer current:

     ```json theme={null}
     "noncurrent_version_expiration": {
        "noncurrent_days": 5
     }
     ```

   * To delete all versions except for the last three:

     ```json theme={null}
     "noncurrent_version_expiration": {
        "noncurrent_days": 5,
        "newer_noncurrent_versions": 3
     }
     ```

     The versions will expire five days after they are no longer current.

   * If you ran multipart uploads for large objects and they failed and remained stale, abort these uploads and delete all the data uploaded. For example, to delete stale multipart uploads seven days after you initiated them (that is, after executing the `CreateMultipartUpload` method):

     ```json theme={null}
     "abort_incomplete_multipart_upload": {
        "days_after_initiation": 7
     }
     ```

**Terraform**

To create an expiration lifecycle rule:

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

2. Create a bucket with expiration lifecycle rules by using the following configuration file:

   ```hcl theme={null}
   resource "nebius_storage_v1_bucket" "<bucket_name>" {
     name                  = "<bucket_name>"
     parent_id             = "<project_ID>"
     default_storage_class = "<STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT>"
     versioning_policy     = "ENABLED"
     lifecycle_configuration = {
       rules = [
         {
           id     = "<rule_ID>"
           status = "ENABLED"
           <rule_conditions>
         }
       ]
     }
   }
   ```

   The file contains the following parameters:

   * `name`: Bucket name.
   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `default_storage_class`: Default storage class. It applies to objects if a storage class isn't set for them explicitly during the upload.
   * `versioning_policy`: Enables versioning of objects in the bucket. For more information, see [Object versioning in a bucket](https://docs.nebius.com/object-storage/buckets/versioning.md).
   * `lifecycle_configuration.rules`: List of lifecycle rules. Every rule contains the following parameters:

     * `id`: Rule ID (string). Helps identify the rule in the list of lifecycle rules.
     * `status`: Whether the rule is enabled or disabled. Use the `DISABLED` status to turn the rule off but preserve it in the list.

     To set the rule conditions, use the examples below and insert them into the configuration file instead of `<rule_conditions>`. You can combine and adapt these examples to your needs.

     * To delete objects five days after their upload, specify:

       ```hcl theme={null}
       expiration = {
         days = 5
       }
       ```

     * To delete objects whose names begin with a certain prefix, specify:

       ```hcl theme={null}
       expiration = {
         days = 5
       }
       filter = {
         prefix = "expiring/"
       }
       ```

       For instance, if you set the `expiring/` prefix, the `expiring/test.txt` object will be deleted five days after the upload, and the `test.txt` object will not.

     * To delete objects that exceed 5120 bytes:

       ```hcl theme={null}
       expiration = {
         days = 5
       }
       filter = {
         object_size_greater_than_bytes = 5120
       }
       ```

       The service applies the rule five days after the object upload.

     * To delete objects that are less than 128 bytes:

       ```hcl theme={null}
       expiration = {
         days = 5
       }
       filter = {
         object_size_less_than_bytes = 128
       }
       ```

     * To delete objects with certain tags, specify:

       ```hcl theme={null}
       expiration = {
         days = 5
       }
       filter = {
         tags = [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
       }
       ```

       A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

     * If you enabled versioning in your bucket, you can delete outdated versions. These are often all the versions except for the current one. To make them expire five days after they are no longer current:

       ```hcl theme={null}
       noncurrent_version_expiration = {
         noncurrent_days = 5
       }
       ```

     * To delete all the versions except for the last three:

       ```hcl theme={null}
       noncurrent_version_expiration = {
         noncurrent_days           = 5
         newer_noncurrent_versions = 3
       }
       ```

       The versions will expire five days after they are no longer current.

     * If you ran multipart uploads for large objects and they failed and remained stale, abort these uploads and delete all the data uploaded. For example, to delete stale multipart uploads seven days after you initiated them (that is, after executing the `CreateMultipartUpload` method):

       ```hcl theme={null}
       abort_incomplete_multipart_upload = {
         days_after_initiation = 7
       }
       ```

3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**AWS CLI**

When you update the lifecycle configuration of a bucket, make sure to list all lifecycle rules and their configuration details, even the ones that you don't change. If you don't include some of them, the service will remove and replace them with the last lifecycle configuration.

To create an expiration lifecycle rule:

1. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI.

2. If you update the lifecycle configuration of an existing bucket, get its current lifecycle configuration:

   ```bash theme={null}
   aws s3api get-bucket-lifecycle-configuration --bucket <bucket_name>
   ```

   The rules are specified in the `Rules` parameter. If you want to preserve them when adding a new rule, duplicate those rules in the new JSON file that you apply to the bucket.

3. To configure a new lifecycle rule, create the `lifecycle.json` file with lifecycle rules:

   ```json theme={null}
   {
     "Rules": [
       {
         "ID": "<rule_ID>",
         "Status": "Enabled",
         "Filter": {
         },
         <rule_conditions>
       },
       {
         <rules_created_earlier>
       },
       ...
     ]
   }
   ```

4. Apply the lifecycle configuration to the bucket:

   ```bash theme={null}
   aws s3api put-bucket-lifecycle-configuration \
     --bucket <bucket_name> \
     --lifecycle-configuration file://lifecycle.json
   ```

   Every rule contains the following parameters:

   * `ID`: Rule ID (string). Helps identify the rule in the list of lifecycle rules.
   * `Status`: Whether the rule is enabled or disabled. Use the `Disabled` status to turn the rule off but preserve it in the list.

   To set the rule conditions, use the examples below and insert them into the JSON file instead of `<rule_conditions>`. You can combine and adapt these examples to your needs.

   * To delete objects five days after their upload, specify:

     ```json theme={null}
     "Expiration": {
       "Days": 5
     }
     ```

   * To delete objects whose names begin with a certain prefix, specify:

     ```json theme={null}
     "Filter": {
       "Prefix": "expiring/"
     },
     "Expiration": {
       "Days": 5
     }
     ```

     For instance, if you set the `expiring/` prefix, the `expiring/test.txt` object will be deleted five days after the upload, and the `test.txt` object will not.

   * To delete objects that exceed 5120 bytes:

     ```json theme={null}
     "Filter": {
       "ObjectSizeGreaterThan": 5120
     },
     "Expiration": {
       "Days": 5
     }
     ```

     The service applies the rule five days after the object upload.

   * To delete objects that are less than 128 bytes:

     ```json theme={null}
     "Filter": {
       "ObjectSizeLessThan": 128
     },
     "Expiration": {
       "Days": 5
     }
     ```

   * To delete objects with a certain tag, specify:

     ```json theme={null}
     "Filter": {
       "Tag": { "Key": "key1", "Value": "value1"}
     },
     "Expiration": {
       "Days": 5
     }
     ```

     A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

     If you want to set several tags, specify:

     ```json theme={null}
     "Filter": {
       "And": {
         "Tags": [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
       }
     },
     "Expiration": {
       "Days": 5
     }
     ```

   * If you enabled versioning in your bucket, you can delete outdated versions. These are often all the versions except for the current one. To make them expire five days after they are no longer current:

     ```json theme={null}
     "Filter": {
     },
     "NoncurrentVersionExpiration": {
       "NoncurrentDays": 5
     }
     ```

   * To delete all versions except for the last three:

     ```json theme={null}
     "Filter": {
     },
     "NoncurrentVersionExpiration": {
       "NoncurrentDays": 5,
       "NewerNoncurrentVersions": 3
     }
     ```

     The versions will expire five days after they are no longer current.

   * If you ran multipart uploads for large objects and they failed and remained stale, abort these uploads and delete all the data uploaded. For example, to delete stale multipart uploads seven days after you initiated them:

     ```json theme={null}
     "Filter": {
     },
     "AbortIncompleteMultipartUpload": {
       "DaysAfterInitiation": 7
     }
     ```

## How to configure transition lifecycle rules

> [!NOTE]
>
> Before you configure a transition rule, check your [quotas](https://docs.nebius.com/object-storage/resources/quotas-limits.md) in the project. Make sure that they are sufficient for switching a storage class.

**Web console**

In the web console, you can only add lifecycle rules to existing buckets. You cannot create a bucket with a lifecycle rule.

To add a transition lifecycle rule to a bucket:

1. In the web console, go to  **Storage** → **Object Storage**.

2. Open the page of the required bucket.

3. Go to the **Lifecycle rules** tab.

4. Click  **Add rule**.

5. (Optional) On the page that opens, specify the rule name. It helps identify the rule in a list of lifecycle rules.

6. Specify which objects the rule applies to:

   * **Object key prefix**: The rule applies to objects whose names begin with a specified prefix. For instance, if you set the `expiring/` prefix, the rule applies to the `expiring/test.txt` object and doesn't apply to the `test.txt` object.

   * **Minimum size, bytes**: The rule applies to objects larger than the specified size.

   * **Maximum size, bytes**: The rule applies to objects smaller than the specified size.

     If you set both a minimum and maximum size, make sure that the maximum size is greater than or equal to the minimum one.

   * **Tags**: The rule applies to objects with the specified tags.

     A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

7. To create a transition lifecycle rule, enable the **Modify storage class** action.

8. Select the rule type:

   * **Upload**: Set the number of days after the object upload. When this period expires, the storage class of the object changes.

   * **Last access**: Set the number of days after the [last access](https://docs.nebius.com/object-storage/objects/lifecycles.md#last-access-lifecycle-rules) to the object. When this period expires, the storage class changes.

     > [!TIP]
     >
     > You can set [filters](#optional-filters-for-last-access-lifecycle-rules) to define what actions are considered the last access to the object. These filters apply to all last-access lifecycle rules.

   * **Date**: Set a specific date when you need to switch the storage class.

9. Select a new storage class that the lifecycle rule applies to.

10. Click **Add rule**.

**Nebius AI Cloud CLI**

When you update the settings of a bucket, make sure to list all lifecycle rules, even the ones that you do not change. If you do not include some rules, Object Storage will delete them.

When you reconfigure a rule, specify only the parameters that you want to change. For example, if you earlier set a filter of objects in a rule and you want to change an expiration condition, specify only the condition, and the rule name or ID. You do not need to set the filter again as it will be preserved.

To create a transition lifecycle rule:

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. If you update the settings of an existing bucket, get a list of its lifecycle rules:
   ```bash theme={null}
   nebius storage bucket get-by-name --name <bucket_name>
   ```
   The rules are specified in the `spec.lifecycle_configuration.rules` parameter. If you want to preserve them when adding a new rule, duplicate those rules in the `update` command.
3. To configure a new transition lifecycle rule, run one of the following commands:

   * Create a bucket with a lifecycle rule:

     ```bash theme={null}
     nebius storage bucket create --name <bucket_name> \
       --default-storage-class <standard|enhanced_throughput|intelligent> \
       --lifecycle-configuration-rules '[
       {
         "id": "<rule_ID>",
         "status": "enabled",
         "transition": {
           "storage_class": "<standard|enhanced_throughput|intelligent>",
           "days": <number_of_days>
         },
         "filter": { <filters> }
       },
       {
         <rules_created_earlier>
       },
       ...
       ]'
     ```

   * Add a rule to an existing bucket:

     ```bash theme={null}
     nebius storage bucket update --id <bucket_ID> \
       --lifecycle-configuration-rules '[
       {
         "id": "<rule_ID>",
         "status": "enabled",
         "transition": {
           "storage_class": "<standard|enhanced_throughput|intelligent>",
           "days": <number_of_days>
         },
         "filter": { <filters> }
       },
       {
         <rules_created_earlier>
       },
       ...
       ]'
     ```

   The commands contain the following parameters:

   * `--name`: Bucket name.
   * `--id`: Bucket ID. To get it, run `nebius storage bucket get-by-name --name <bucket_name>`.
   * `--default-storage-class`: Default storage class. It applies to objects if a storage class isn't explicitly set for them during the upload.
   * `--lifecycle-configuration-rules`: List of lifecycle rules. Every rule contains the following parameters:

     * `id`: Rule ID (string). Helps identify the rule in the list of lifecycle rules.

     * `status`: Whether the rule is enabled or disabled. Use the `disabled` status to turn the rule off but preserve it in the list.

     * `transition`: Conditions for a transition lifecycle rule. To change a storage class, set the `storage_class` parameter. Use either the `days` or `days_since_last_access` parameter:

       * `storage_class`: New storage class.
       * `days`: The rule applies the specified number of days after the object upload.
       * `days_since_last_access`: The rule applies the specified number of days after the object hasn't been accessed.

         The service considers an object to be accessed if its data was retrieved or copied by using [S3 methods](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html), such as `GetObject`, `HeadObject`, `GetObjectTagging`, `CopyObject` or `UploadPartCopy`. You can configure the rule to refer only to some of these methods by using [last access filters](#optional-filters-for-last-access-lifecycle-rules).

     * `filter` (optional): Filters of objects. By using them, you can apply a rule to certain objects only. You can combine the filters if needed. The available filters are the following:

       * To transition objects whose names begin with a certain prefix, specify:

         ```json theme={null}
         "filter": {
            "prefix": "expiring/"
         }
         ```

         For instance, if you set the `expiring/` prefix, the storage class of the `expiring/test.txt` object will be switched. However, this will not happen to the `test.txt` object.

       * To transition objects that exceed 5120 bytes:

         ```json theme={null}
         "filter": {
            "object_size_greater_than_bytes": 5120
         }
         ```

       * To transition objects that are less than 128 bytes:

         ```json theme={null}
         "filter": {
            "object_size_less_than_bytes": 128
         }
         ```

       * To transition objects with certain tags, specify:

         ```json theme={null}
         "filter": {
            "tags": [
               {"key": "key1", "value": "value1"},
               {"key": "key2", "value": "value2"}
            ]
         }
         ```

         A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

**Terraform**

To create a transition lifecycle rule:

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

2. Create a bucket with transition lifecycle rules by using the following configuration file:

   ```hcl theme={null}
   resource "nebius_storage_v1_bucket" "<bucket_name>" {
     name                  = "<bucket_name>"
     parent_id             = "<project_ID>"
     default_storage_class = "<STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT>"
     versioning_policy     = "ENABLED"
     lifecycle_configuration = {
       rules = [
         {
           id     = "<rule_ID>"
           status = "ENABLED"
           transition = {
             storage_class          = "<STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT>"
             days                   = <number_of_days>
             days_since_last_access = <number_of_days>
           }
           filter = { <filters> }
         }
       ]
     }
   }
   ```

   The file contains the following parameters:

   * `name`: Bucket name.
   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `default_storage_class`: Default storage class. It applies to objects if a storage class isn't explicitly set for them during the upload.
   * `versioning_policy`: Enables versioning of objects in the bucket. For more information, see [Object versioning in a bucket](https://docs.nebius.com/object-storage/buckets/versioning.md).
   * `lifecycle_configuration.rules`: List of lifecycle rules. Every rule contains the following parameters:

     * `id`: Rule ID (string). Helps identify the rule in the list of lifecycle rules.

     * `status`: Whether the rule is enabled or disabled. Use the `DISABLED` status to turn the rule off but preserve it in the list.

     * `transition`: Conditions for a transition lifecycle rule. To change a storage class, set the `storage_class` parameter. Use either the `days` or `days_since_last_access` parameter:

       * `storage_class`: New storage class.
       * `days`: The rule applies the specified number of days after the object upload.
       * `days_since_last_access`: The rule applies the specified number of days after the object hasn't been accessed.

         The service considers an object to be accessed if its data was retrieved or copied by using [S3 methods](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html), such as `GetObject`, `HeadObject`, `GetObjectTagging`, `CopyObject` or `UploadPartCopy`. You can configure the rule to refer only to some of these methods by using [last access filters](#optional-filters-for-last-access-lifecycle-rules).

     * `filter` (optional): Filters of objects. By using them, you can apply a rule to certain objects only. You can combine the filters if needed. The available filters are the following:

       * To transition objects whose names begin with a certain prefix, specify:

         ```hcl theme={null}
         filter = {
           prefix = "expiring/"
         }
         ```

         For instance, if you set the `expiring/` prefix, the storage class of the `expiring/test.txt` object will be switched. However, this will not happen to the `test.txt` object.

       * To transition objects that exceed 5120 bytes:

         ```hcl theme={null}
         filter = {
           object_size_greater_than_bytes = 5120
         }
         ```

       * To transition objects that are less than 128 bytes:

         ```hcl theme={null}
         filter = {
           object_size_less_than_bytes = 128
         }
         ```

       * To transition objects with certain tags, specify:

         ```hcl theme={null}
         filter = {
           tags = [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
         }
         ```

         A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**AWS CLI**

When you update the lifecycle configuration of a bucket, make sure to list all lifecycle rules and their configuration details, even the ones that you don't change. If you don't include some of them, the service will remove and replace them with the last lifecycle configuration.

The AWS CLI only supports transition lifecycle rules that set a number of days after the object upload. If you want to set the last access time of the object or the date of the storage class switch, use the Nebius AI Cloud interfaces.

Although the AWS CLI allows multiple transition actions in a single rule, Object Storage only supports one transition action per rule. If you need multiple transition actions, create multiple rules.

To create a transition lifecycle rule:

1. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI.

2. If you update the lifecycle configuration of an existing bucket, get its current lifecycle configuration:

   ```bash theme={null}
   aws s3api get-bucket-lifecycle-configuration --bucket <bucket_name>
   ```

   The rules are specified in the `Rules` parameter. If you want to preserve them when adding a new rule, duplicate those rules in the new JSON file that you apply to the bucket.

3. To configure a new transition lifecycle rule, create the `lifecycle.json` file with lifecycle rules:

   ```json theme={null}
   {
     "Rules": [
       {
         "ID": "<rule_ID>",
         "Status": "Enabled",
         "Filter": {},
         "Transitions": [
           {
             "StorageClass": "<STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT>",
             "Days": <number_of_days>
           }
         ]
       },
       {
         <rules_created_earlier>
       },
       ...
     ]
   }
   ```

   If the `Filter` element is left empty, the rule applies to all objects in the bucket.

4. Apply the lifecycle configuration to the bucket:

   ```bash theme={null}
   aws s3api put-bucket-lifecycle-configuration \
     --bucket <bucket_name> \
     --lifecycle-configuration file://lifecycle.json
   ```

   Every rule contains the following parameters:

   * `ID`: Rule ID (string). Helps identify the rule in the list of lifecycle rules.

   * `Status`: Whether the rule is enabled or disabled. Use the `Disabled` status to turn the rule off but preserve it in the list.

   * `Transitions`: Conditions for a transition lifecycle rule. To change a storage class, set the `StorageClass` parameter. To define when the rule applies after the object upload, set the `Days` parameter.

     * `StorageClass`: New storage class.
     * `Days`: The rule applies the specified number of days after the object upload.

   * `Filter` (optional): Filters of objects. By using them, you can apply a rule to certain objects only. A `Filter` can contain exactly one of `Prefix`, `ObjectSizeGreaterThan`, `ObjectSizeLessThan` or `And`. To combine multiple conditions, use `And`.

     * To transition objects whose names begin with a certain prefix, specify:

       ```json theme={null}
       "Filter": {
         "Prefix": "expiring/"
       }
       ```

       For instance, if you set the `expiring/` prefix, the storage class of the `expiring/test.txt` object will be switched. However, this will not happen to the `test.txt` object.

     * To transition objects that exceed 5120 bytes, specify:

       ```json theme={null}
       "Filter": {
         "ObjectSizeGreaterThan": 5120
       }
       ```

     * To transition objects that are less than 128 bytes, specify:

       ```json theme={null}
       "Filter": {
         "ObjectSizeLessThan": 128
       }
       ```

     * To transition objects with a certain tag, specify:

       ```json theme={null}
       "Filter": {
         "Tag": { "Key": "key1", "Value": "value1"}
       }
       ```

       A *tag* represents a key-value pair that you add to existing objects or when you upload objects. For more information, see [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html).

       If you want to set several tags, specify:

       ```json theme={null}
       "Filter": {
         "And": {
           "Tags": [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
         }
       }
       ```

### (Optional) Filters for last-access lifecycle rules

You can filter actions that Object Storage considers or ignores when it determines the timestamp of the object's last access. In the filters, specify S3 methods and user agents (such as `rclone`) that should be included or excluded.

Filters apply to all last-access lifecycle rules. You configure them at the bucket level.

By default, no filters apply. All S3 methods (GetObject, HeadObject, GetObjectTagging, CopyObject and UploadPartCopy.) and user agents are included.

**Web console**

1. In the web console, go to  **Storage** → **Object Storage**.

2. Open the page of the required bucket.

3. Go to the **Settings** tab.

4. In the **Filters for last-access lifecycle rules** section, click  **Add filter**.

5. In the **Filter type** field, select one of the following:

   * `Include`: Consider only the methods and user agents listed in the filter.
   * `Exclude`: Ignore the methods and user agents listed.

6. Specify the S3 methods and user agents for the filter. Among the S3 methods, you can set `GetObject`, `HeadObject`, `GetObjectTagging`, `CopyObject` and `UploadPartCopy`.

   If you don't specify methods or user agents, Object Storage considers all of them.

7. Click **Add filter**.

   The new filter appears in the list of filters for last-access lifecycle rules.

8. Click **Save changes** to confirm.

**Nebius AI Cloud CLI**

When you create or update a bucket, set the filters by using the `--lifecycle-configuration-last-access-filter-conditions` parameter.

* Create a bucket with a lifecycle rule:

  ```bash theme={null}
  nebius storage bucket create --name <bucket_name> \
    --default-storage-class <standard|enhanced_throughput|intelligent> \
    --lifecycle-configuration-rules '[...]' \
    --lifecycle-configuration-last-access-filter-conditions '[
    {
      "type": "<include|exclude>",
      "methods": ["<S3_methods>"],
      "user_agents": ["<user_agents>"]
    },
    {
      <other_conditions>
    },
    ...
    ]'
  ```

* Add a rule to an existing bucket:

  ```bash theme={null}
  nebius storage bucket update --id <bucket_ID> \
    --lifecycle-configuration-rules '[...]' \
    --lifecycle-configuration-last-access-filter-conditions '[
    {
      "type": "<include|exclude>",
      "methods": ["<S3_methods>"],
      "user_agents": ["<user_agents>"]
    },
    {
      <other_conditions>
    },
    ...
    ]'
  ```

Apply the filtering parameter only if you use the [transition.days\_since\_last\_access](#how-to-configure-transition-lifecycle-rules) parameter.

For example, the service can consider an object to be accessed only if the `GetObject` and `CopyObject` methods were executed by using the `rclone` user agent. Alternatively, the service can ignore the `GetObject` and `UploadPartCopy` methods.

Every filter contains the following fields:

* `type`: Whether listed S3 methods and user agents should be considered to determine if the object is accessed. Possible values are the following:

  * `INCLUDE`: Consider only the methods and user agents listed in the filter.
  * `EXCLUDE`: Ignore the methods and user agents listed.

* `methods`: List of S3 methods, such as `"GET_OBJECT"`, `"HEAD_OBJECT"`, `"GET_OBJECT_TAGGING"`, `"COPY_OBJECT"` and `"UPLOAD_PART_COPY"`.

  If you do not specify the `methods` parameter, Object Storage considers all methods.

* `user_agents`: List of substrings that user agents (clients addressing an object) can contain. For instance, if you specify `rclone`, only the user agents with the `rclone` substring trigger the countdown of days for the rule to apply.

  If you do not specify the `user_agents` parameter, Object Storage considers all user agents.

Specify at least `methods` or `user_agents`. You can use both of them as well, but you cannot use a filter with the `type` parameter only.

**Terraform**

When you create or update a bucket, set the filters by using the `last_access_filter.conditions` parameter.

```hcl theme={null}
resource "nebius_storage_v1_bucket" "<bucket_name>" {
  ...
  lifecycle_configuration = {
    rules = [...]
    last_access_filter = [
      {
        conditions = [
          {
            type        = "<INCLUDE|EXCLUDE>"
            methods     = ["<S3_methods>"]
            user_agents = ["<user_agents>"]
          },
          {
            <other_conditions>
          },
          ...
        ]
      }
    ]
  }
}
```

Apply the filtering parameter only if you use the [transition.days\_since\_last\_access](#how-to-configure-transition-lifecycle-rules) parameter.

For example, the service can consider an object to be accessed only if the `GetObject` and `CopyObject` methods were executed by using the `rclone` user agent. Alternatively, the service can ignore the `GetObject` and `UploadPartCopy` methods.

Every filter contains the following fields:

* `type`: Whether listed S3 methods and user agents should be considered to determine if the object is accessed. Possible values are the following:

  * `INCLUDE`: Consider only the methods and user agents listed in the filter.
  * `EXCLUDE`: Ignore the methods and user agents listed.

* `methods`: List of S3 methods, such as `"GET_OBJECT"`, `"HEAD_OBJECT"`, `"GET_OBJECT_TAGGING"`, `"COPY_OBJECT"` and `"UPLOAD_PART_COPY"`.

  If you do not specify the `methods` parameter, Object Storage considers all methods.

* `user_agents`: List of substrings that user agents (clients addressing an object) can contain. For instance, if you specify `rclone`, only the user agents with the `rclone` substring trigger the countdown of days for the rule to apply.

  If you do not specify the `user_agents` parameter, Object Storage considers all user agents.

Specify at least `methods` or `user_agents`. You can use both of them as well, but you cannot use a filter with the `type` parameter only.

### Examples of transition lifecycle rules

Below are examples of how to create a bucket with a transition lifecycle rule that triggers if an object wasn't accessed for a long time.

* Switch a storage class to Standard if the object hasn't been accessed in seven days. For the access, don't consider the `GetObject` and `CopyObject` methods that were made by using `rclone`.

  **Nebius AI Cloud CLI**

  To set such a rule, run the following command:

  ```bash theme={null}
  nebius storage bucket create --name my-bucket \
     --default-storage-class enhanced_throughput \
     --lifecycle-configuration-rules '[
        {
           "id": "switch-to-standard-in-7-days",
           "status": "enabled",
           "transition": {
              "days_since_last_access": 7,
              "storage_class": "standard"
           }
        }
     ]' \
     --lifecycle-configuration-last-access-filter-conditions '[
        {
           "type": "exclude",
           "methods": ["get_object", "copy_object"],
           "user_agents": ["rclone"]
        }
     ]'
  ```

  **Terraform**

  To set such a rule, apply the following configuration:

  ```hcl theme={null}
  resource "nebius_storage_v1_bucket" "my-bucket" {
    name                  = "my-bucket"
    parent_id             = "project-e***"
    default_storage_class = "ENHANCED_THROUGHPUT"
    versioning_policy     = "ENABLED"
    lifecycle_configuration = {
      rules = [
        {
          id     = "switch-to-standard-in-7-days"
          status = "ENABLED"
          transition = {
            days_since_last_access = 7
            storage_class          = "STANDARD"
          }
        }
      ]
      last_access_filter = [
        {
          conditions = [
            {
              type        = "EXCLUDE"
              methods     = ["GET_OBJECT", "COPY_OBJECT"]
              user_agents = ["rclone"]
            }
          ]
        }
      ]
    }
  }
  ```

* Switch a storage class to Standard if the object hasn't been accessed in three days. For the access, consider only the `GetObjectTagging` method.

  **Nebius AI Cloud CLI**

  To set such a rule, run the following command:

  ```bash theme={null}
  nebius storage bucket create --name my-bucket \
     --default-storage-class enhanced_throughput \
     --lifecycle-configuration-rules '[
        {
           "id": "switch-to-standard-in-3-days",
           "status": "enabled",
           "transition": {
              "days_since_last_access": 3,
              "storage_class": "standard"
           }
        }
     ]' \
     --lifecycle-configuration-last-access-filter-conditions '[
        {
           "type": "include",
           "methods": ["get_object_tagging"]
        }
     ]'
  ```

  **Terraform**

  To set such a rule, apply the following configuration:

  ```hcl theme={null}
  resource "nebius_storage_v1_bucket" "my-bucket" {
    name                  = "my-bucket"
    parent_id             = "project-e***"
    default_storage_class = "ENHANCED_THROUGHPUT"
    versioning_policy     = "ENABLED"
    lifecycle_configuration = {
      rules = [
        {
          id     = "switch-to-standard-in-3-days"
          status = "ENABLED"
          transition = {
            days_since_last_access = 3
            storage_class          = "STANDARD"
          }
        }
      ]
      last_access_filter = [
        {
          conditions = [
            {
              type    = "INCLUDE"
              methods = ["GET_OBJECT_TAGGING"]
            }
          ]
        }
      ]
    }
  }
  ```
