# Groups within Nebius AI Cloud tenants

Source: https://docs.nebius.com/iam/authorization/groups

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Groups within Nebius AI Cloud tenants

*Groups* in Nebius AI Cloud help you organize and authorize [users and service accounts](https://docs.nebius.com/iam/overview.md#accounts-and-members) to view and manage your tenant resources.

By default, new users and service accounts do not have access to any resources in a tenant. When you [add a user or service account to a group](https://docs.nebius.com/iam/authorization/groups/members.md), they receive a specific level of access to resources, as defined by the [roles](https://docs.nebius.com/iam/authorization/roles.md) that are assigned to the group.

Your tenant includes pre-created [default groups](#default-groups) that provide broad permissions through the [general roles](https://docs.nebius.com/iam/authorization/roles.md#general-roles) assigned to them. You can also create and configure [custom groups](#custom-groups) for more granular control over access. For instructions, see [Managing custom groups](https://docs.nebius.com/iam/authorization/groups/manage.md).

If you want to delete a group, see [How to delete groups](https://docs.nebius.com/iam/authorization/groups/delete-groups.md).

## Default groups

From least to most access, the default groups in a tenant are the following:

* `auditors` can view **certain types** of resources **without access to data**.
* `viewers` can view **most types** of resources (except some resources related to access management, security, etc.) and **access data** in them (e.g. download objects in buckets).
* `editors` can view **and manage** most types of resources and access data in them.
* `admins` can view and manage **all types** of resources and access data in them.

Each default group is assigned a corresponding tenant-wide [general role](https://docs.nebius.com/iam/authorization/roles.md#general-roles).

> [!WARNING]
>
> Default groups and general roles grant a wide range of permissions across all services. To follow the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege), create custom groups and assign roles with as few permissions as possible to these groups.

## Custom groups

Custom groups give you granular control over permissions. You can create custom groups in your tenant or in a specific project. To manage group permissions, you should then create access permits that assign roles for specific resources to the group. The access permits can assign roles to the resources at the following levels:

* **Tenant**: A tenant, all projects and all resources within it.

* **Project**: A project and all resources within it.

* **Individual resource**: A resource that supports access permits, and its child resources. For example:

  * If you create an access permit for a group, it also applies to its group memberships because they are its child resources.
  * If you create an access permit for an account, it does not apply to its access keys, because their parent is the project, not the account.

  The following resource types support access permits:

  * Identity and Access Management resources (see the list in the **Identity and Access Management** section in [Roles for Nebius AI Cloud groups](https://docs.nebius.com/iam/authorization/roles.md#general-roles))
  * Virtual machines ([Compute](https://docs.nebius.com/compute/index.md))
  * Buckets ([Object Storage](https://docs.nebius.com/object-storage/index.md))
  * Container registries ([Container Registry](https://docs.nebius.com/container-registry/index.md))
  * Secrets ([SecretStash](https://docs.nebius.com/mysterybox/index.md))

For instructions, see [Managing custom groups](https://docs.nebius.com/iam/authorization/groups/manage.md).

> [!TIP]
>
> If you need granular access rights to objects in a bucket, set up a [bucket policy](https://docs.nebius.com/object-storage/buckets/bucket-policy.md) in Object Storage. You can use it instead of an access permit or apply both of them.
