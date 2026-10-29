# Bucket policies in Object Storage

Source: https://docs.nebius.com/object-storage/buckets/bucket-policy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Bucket policies in Object Storage

A *bucket policy* enables you to configure fine-grained access to objects within a bucket. In particular, you can allow access to objects with certain [prefixes or keys](https://docs.nebius.com/object-storage/overview.md#keys-prefixes-and-object-hierarchy) for a certain [IAM group](https://docs.nebius.com/iam/authorization/groups/index.md). In a policy, you specify what permissions the group obtains and what objects it can access.

## How to configure a bucket policy

Before you begin, make sure that you have a bucket. If you do not have one, [create a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets).

**CLI**

To configure a list of rules in a bucket policy, run the following command:

```bash theme={null}
nebius storage bucket update \
  --id <bucket_ID> \
  --bucket-policy-rules "[{\"paths\": [\"<paths>\"], \"roles\": [\"<list_of_roles>\"], \"group_id\": \"<group_ID>\"}]"
```

> [!WARNING]
>
> In the command, specify all the rules that the bucket should have. If you add a new rule to a list of existing rules, specify the existing rules as well. Otherwise, they will be deleted.

The `--bucket-policy-rules` parameter contains a list of rules for a bucket policy. Every rule has the following parameters:

* `paths`: Paths to objects that the rule applies to. Each path is either a full object key or a prefix ending with a single `*` wildcard character. If you use `*`, the rule provides access to all objects. A path may also contain one or more `?` placeholders. Each `?` character matches a single character at that position in the string.

  Examples of supported paths:

  * `prefix_1/key_1`: Rule applies to the object with the set prefix and key.
  * `prefix_1/*`: Rule applies to any object with the `prefix_1` prefix.
  * `allowed?/*`: Rule applies to objects with prefixes like `allowed1/`, `allowed2/` or `allowedA/`. A single `?` matches exactly one character, so neither `allowed/` nor `allowed10/` matches.
  * `key_1`: Rule applies to the object with the `key_1` key.
  * `*`: Rule applies to all objects in a bucket.

  You can use the `*` symbol only at the end of the path and only once in a path. For example, you can specify `prefix_1/*`, but you cannot use `prefix*1` or `pre*fix*`.

* `roles`: [Object Storage roles](https://docs.nebius.com/iam/authorization/roles.md#object-storage) granted to the specified IAM group to access objects in a bucket. You can grant read-only roles or editor roles.

* `group_id`: ID of the IAM group to which the rule applies.

  To get the group ID, go to the  [Administration → IAM](https://console.nebius.com/iam/groups) page in the web console. The list of groups and their IDs is displayed on the **Groups** tab.

**Terraform**

To configure a list of rules in a bucket policy, use the `bucket_policy` parameter in a bucket configuration:

```hcl theme={null}
resource nebius_storage_v1_bucket "<bucket_name>" {
  bucket_policy = {
    rules = [
      {
        paths      = [<paths>]
        roles      = [<list_of_roles>]
        group_id = "<group_ID>"
      }
    ]
  }
  ...
}
```

The `rules` parameter contains a list of rules for the bucket policy. Every rule has the following parameters:

* `paths`: Paths to objects that the rule applies to. Each path is either a full object key or a prefix ending with a single `*` wildcard character. If you use `*`, the rule provides access to all objects. A path may also contain one or more `?` placeholders. Each `?` character matches a single character at that position in the string.

  Examples of supported paths:

  * `prefix_1/key_1`: Rule applies to the object with the set prefix and key.
  * `prefix_1/*`: Rule applies to any object with the `prefix_1` prefix.
  * `allowed?/*`: Rule applies to objects with prefixes like `allowed1/`, `allowed2/` or `allowedA/`. A single `?` matches exactly one character, so neither `allowed/` nor `allowed10/` matches.
  * `key_1`: Rule applies to the object with the `key_1` key.
  * `*`: Rule applies to all objects in a bucket.

  You can use the `*` symbol only at the end of the path and only once in a path. For example, you can specify `prefix_1/*`, but you cannot use `prefix*1` or `pre*fix*`.

* `roles`: [Object Storage roles](https://docs.nebius.com/iam/authorization/roles.md#object-storage) granted to the specified IAM group to access objects in a bucket. You can grant read-only roles or editor roles.

* `group_id`: ID of the IAM group to which the rule applies.

  To get the group ID, go to the  [Administration → IAM](https://console.nebius.com/iam/groups) page in the web console. The list of groups and their IDs is displayed on the **Groups** tab.

Rules within a single policy don't conflict with each other. All of them apply with an equal priority.

For more information about how to configure a bucket policy, see [Examples](#examples).

### Anonymous access

Anonymous access allows you to access a bucket without authentication. For instance, you can use a `curl` command without any authentication data.

To configure anonymous access:

* Instead of the `group_id` parameter, specify `"anonymous": {}` in a CLI command or `anonymous = {}` in Terraform configuration.
* Only use the `storage.viewer`, `storage.object-viewer` and `storage.object-lister` roles in the rule, as anonymous access only works for read-only permissions.

For more information, see the examples below.

### Examples

**CLI**

* Allow access to all objects in a bucket:

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"*\"], \"roles\": [\"storage.viewer\"], \"group_id\": \"group-e00***\"}]"
  ```

  The `storage.viewer` role enables one to view buckets, to list and download objects.

* Allow full read access (including multipart uploads) to objects with the `allowed1` and `allowed2` prefixes:

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"allowed1/*\", \"allowed2/*\"], \"roles\": [\"storage.viewer\"], \"group_id\": \"group-e00***\"}]"
  ```

* Allow partial read access (without multipart uploads) to objects with the `allowed1` and `allowed2` prefixes:

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"allowed1/*\", \"allowed2/*\"], \"roles\": [\"storage.object-lister\", \"storage.object-viewer\"], \"group_id\": \"group-e00***\"}]"
  ```

* Allow access to objects with prefixes like `allowed1/`, `allowed2/`, `allowedA/` and so on, using a placeholder:

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"allowed?/*\"], \"roles\": [\"storage.object-lister\", \"storage.object-viewer\"], \"group_id\": \"group-e00***\"}]"
  ```

* Allow access to the object with the `allowed_key` key:

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"allowed_key\"], \"roles\": [\"storage.viewer\"], \"group_id\": \"group-e00***\"}]"
  ```

* Allow anonymous access to all objects in a bucket:

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"*\"], \"roles\": [\"storage.viewer\"], \"anonymous\": {} }]"
  ```

* Apply two rules simultaneously:

  * Assign the `storage.viewer` role to the `prefix_1/key_1` object.
  * Assign the `storage.editor` role to objects with the `prefix_2` prefix.

  ```bash theme={null}
  nebius storage bucket update \
    --id storagebucket-e00*** \
    --bucket-policy-rules "[{\"paths\": [\"prefix_1/key_1\"], \"roles\": [\"storage.viewer\"], \"group_id\": \"group-e00***\"},
      {\"paths\": [\"prefix_2/*\"], \"roles\": [\"storage.editor\"], \"group_id\": \"group-e00***\"}]"
  ```

**Terraform**

* Allow access to all objects in a bucket:

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths    = ["*"]
          roles    = ["storage.viewer"]
          group_id = "group-e00***"
        }
      ]
    }
    ...
  }
  ```

* Allow full read access (including multipart uploads) to objects with the `allowed1` and `allowed2` prefixes:

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths    = ["allowed1/*", "allowed2/*"]
          roles    = ["storage.viewer"]
          group_id = "group-e00***"
        }
      ]
    }
    ...
  }
  ```

* Allow partial read access (without multipart uploads) to objects with the `allowed1` and `allowed2` prefixes:

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths    = ["allowed1/*", "allowed2/*"]
          roles    = ["storage.object-lister", "storage.object-viewer"]
          group_id = "group-e00***"
        }
      ]
    }
    ...
  }
  ```

* Allow access to objects with prefixes like `allowed1/`, `allowed2/`, `allowedA/` and so on, using a placeholder. A single `?` matches exactly one character, so neither `allowed/` nor `allowed10/` matches this rule:

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths    = ["allowed?/*"]
          roles    = ["storage.viewer"]
          group_id = "group-e00***"
        }
      ]
    }
    ...
  }
  ```

* Allow access to the object with the `allowed_key` key:

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths    = ["allowed_key"]
          roles    = ["storage.viewer"]
          group_id = "group-e00***"
        }
      ]
    }
    ...
  }
  ```

* Allow anonymous access to all objects in a bucket:

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths     = ["*"]
          roles     = ["storage.viewer"]
          anonymous = {}
        }
      ]
    }
    ...
  }
  ```

* Apply two rules simultaneously:

  * Assign the `storage.viewer` role to the `prefix_1/key_1` object.
  * Assign the `storage.editor` role to objects with the `prefix_2` prefix.

  ```hcl theme={null}
  resource nebius_storage_v1_bucket "bucket1" {
    bucket_policy = {
      rules = [
        {
          paths    = ["prefix_1/key_1"]
          roles    = ["storage.viewer"]
          group_id = "group-e00***"
        },
        {
          paths    = ["prefix_2/*"]
          roles    = ["storage.editor"]
          group_id = "group-e00***"
        }
      ]
    }
    ...
  }
  ```

## How to delete all bucket policy rules

If you specify an empty list of rules for a bucket policy, no policy applies.

**CLI**

To delete all rules, run the following command:

```bash theme={null}
nebius storage bucket update \
  --id storagebucket-e00*** \
  --bucket-policy-rules '[]'
```

**Terraform**

To delete all rules, delete the `bucket_policy` parameter from the Terraform configuration.

## Limitations

* The IAM group and the bucket must be in the same tenant.
* The maximum number of rules per bucket is 10.
* The maximum number of paths per rule is 10.
* The maximum path length is 1024 symbols (the same as the maximum length of an object key).

## Access permits and bucket policies

If you have assigned a bucket policy or an [access permit](https://docs.nebius.com/iam/authorization/groups.md#custom-groups) to a bucket, both of them grant access to the bucket and its objects. For example:

> * If a bucket policy grants the `storage.object-lister` role and an access permit grants the `storage.object-viewer` role to the same IAM group, both of the roles apply to the group. As a result, members of this group can both list objects and view them.
>
> * If a bucket policy grants the `storage.viewer` role and an access permit grants the `storage.editor` role to the same IAM group, members of this group have editor rights as a result although they still have rights of the `storage.viewer` role.
