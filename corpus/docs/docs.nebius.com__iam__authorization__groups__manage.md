# Managing custom groups

Source: https://docs.nebius.com/iam/authorization/groups/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing custom groups

In addition to [default groups](https://docs.nebius.com/iam/authorization/groups.md#default-groups) that come with your tenant when you sign up for Nebius AI Cloud, you can create and manage [custom groups](https://docs.nebius.com/iam/authorization/groups.md#custom-groups) in the tenant and its projects for granular control over permissions. To manage group permissions, create access permits that assign [roles](https://docs.nebius.com/iam/authorization/roles.md) for specific resources to the group.

## Prerequisites

The prerequisites for this guide depend on the interface that you use.

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Install [jq](https://jqlang.github.io/jq/download/) to extract IDs and tokens from JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Setting up custom groups

To create a group and set up its permissions, go through the following steps:

**Web console**

1. Create a group within your tenant or project:

   1. In the sidebar, go to  **Administration** → **IAM**.
   2. Click **Create entity** and select **Group**.
   3. In the window that opens, specify the group name and define its scope by selecting either your tenant or a specific project in the tenant.
   4. Click **Create** to finish creating the group.

2. Create an access permit for the group:

   1. Open the newly created group and switch to the **Access permits** tab.

   2. Click **Manage permits**.

   3. In the window that opens, select the resource that you want the group to have access to. If the resource is not listed, enter its ID in the **Resource** field and press `Enter`.

      Only specific resource types support access permits. For the list of supported resource types, see [Custom groups](https://docs.nebius.com/iam/authorization/groups.md#custom-groups).

      The available resources depend on the scope of the group:

      * A group created in a tenant can have permits for the tenant, any projects and resources within it.
      * A group created in a project can only have permits for this project and resources within it.

   4. Select [roles](https://docs.nebius.com/iam/authorization/roles.md) to assign to the group. These roles define the permissions of the group members.

   5. Click **Save changes** to apply your changes.

3. [Add members](https://docs.nebius.com/iam/authorization/groups/members.md) to the group.

**CLI**

1. Create a group within your tenant or project:

   ```bash theme={null}
   nebius iam group create \
     --parent-id <tenant_or_project_ID> \
     --name <custom_group_name>
   ```

   In the `--parent-id` parameter, you can specify either the [ID of your tenant](https://docs.nebius.com/iam/get-tenants.md#cli-2) or the [ID of the specific project](https://docs.nebius.com/iam/manage-projects.md#cli-3).

   From the output of this command, copy the group ID to use it in the next step.

2. Create an access permit for the group:

   ```bash theme={null}
   nebius iam access-permit create \
     --parent-id <group_ID> \
     --resource-id <resource_ID> \
     --role <auditor|viewer|editor|admin|dsr.admin|...>
   ```

   In this command, set the following parameters:

   * `--parent-id`: Group ID that you got on the previous step.

   * `--resource-id`: ID of the resource for which the permit is created. Only specific resource types support access permits. For the list of supported resource types, see [Custom groups](https://docs.nebius.com/iam/authorization/groups.md#custom-groups).

     The available resources depend on the scope of the group:

     * A group created in a tenant can have permits for the tenant, any projects and resources within it.
     * A group created in a project can only have permits for this project and resources within it.

   * `--role`: One of the [roles](https://docs.nebius.com/iam/authorization/roles.md) that provide a set of permissions.

**Go SDK**

1. Create a group within your tenant or project:

   ```go theme={null}
   createGroup, err := sdk.Services().IAM().V1().Group().
       Create(
       ctx,
       &iam.CreateGroupRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<tenant_or_project_ID>",
               Name:     "<custom_group_name>",
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = createGroup.Wait(ctx); err != nil {
       return err
   }
   ```

   In `Metadata.ParentId`, you can specify either the [ID of your tenant](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2) or the [ID of the specific project](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).

   From the response, get the group's resource ID with `createGroup.ResourceID()` to use it in the next step.

2. Create an access permit for the group:

   ```go theme={null}
   permitOperation, err := sdk.Services().IAM().V1().
       AccessPermit().Create(
           ctx,
           &iam.CreateAccessPermitRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<group_ID>",
               },
               Spec: &iam.AccessPermitSpec{
                   ResourceId: "<resource_ID>",
                   Role:       "<auditor|viewer|editor|admin|dsr.admin|...>",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = permitOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   In the code, set the following parameters:

   * `Metadata.ParentId`: Group ID that you got on the previous step.

   * `Spec.ResourceId`: ID of the resource for which the permit is created. Only specific resource types support access permits. For the list of supported resource types, see [Custom groups](https://docs.nebius.com/iam/authorization/groups.md#custom-groups).

     The available resources depend on the scope of the group:

     * A group created in a tenant can have permits for the tenant, any projects and resources within it.
     * A group created in a project can only have permits for this project and resources within it.

   * `Spec.Role`: One of the [roles](https://docs.nebius.com/iam/authorization/roles.md) that provide a set of permissions.

**Python SDK**

1. Create a group within your tenant or project:

   ```python theme={null}
   create_group_service = GroupServiceClient(sdk)
   create_group = await create_group_service.create(
       CreateGroupRequest(
           metadata=ResourceMetadata(
               parent_id="<tenant_or_project_ID>",
               name="<custom_group_name>",
           ),
       ),
   )
   await create_group.wait()
   ```

   In `parent_id`, you can specify either the [ID of your tenant](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2) or the [ID of the specific project](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).

   From the response, get the group's resource ID with `create_group.resource_id` to use it in the next step.

2. Create an access permit for the group:

   ```python theme={null}
   permit_service = AccessPermitServiceClient(sdk)
   permit_operation = await permit_service.create(
       CreateAccessPermitRequest(
           metadata=ResourceMetadata(parent_id="<group_ID>"),
           spec=AccessPermitSpec(
               resource_id="<resource_ID>",
               role="<auditor|viewer|editor|admin|dsr.admin|...>",
           ),
       ),
   )
   await permit_operation.wait()
   ```

   In the code, set the following parameters:

   * `parent_id`: Group ID that you got on the previous step.

   * `resource_id`: ID of the resource for which the permit is created. Only specific resource types support access permits. For the list of supported resource types, see [Custom groups](https://docs.nebius.com/iam/authorization/groups.md#custom-groups).

     The available resources depend on the scope of the group:

     * A group created in a tenant can have permits for the tenant, any projects and resources within it.
     * A group created in a project can only have permits for this project and resources within it.

   * `role`: One of the [roles](https://docs.nebius.com/iam/authorization/roles.md) that provide a set of permissions.

**JavaScript SDK**

1. Create a group within your tenant or project:

   ```ts theme={null}
   const createGroupService = new GroupService(sdk);
   const createGroup = await createGroupService.create(
     CreateGroupRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<tenant_or_project_ID>",
         name: "<custom_group_name>",
       }),
     }),
   ).result;
   await createGroup.wait();
   ```

   In `parentId`, you can specify either the [ID of your tenant](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2) or the [ID of the specific project](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).

   From the response, get the group's resource ID with `createGroup.resourceId()` to use it in the next step.

2. Create an access permit for the group:

   ```ts theme={null}
   const permitService = new AccessPermitService(sdk);
   const permitOperation = await permitService.create(
     CreateAccessPermitRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<group_ID>",
       }),
       spec: AccessPermitSpec.create({
         resourceId: "<resource_ID>",
         role: "<auditor|viewer|editor|admin|dsr.admin|...>",
       }),
     }),
   ).result;
   await permitOperation.wait();
   ```

   In the code, set the following parameters:

   * `parentId`: Group ID that you got on the previous step.

   * `resourceId`: ID of the resource for which the permit is created. Only specific resource types support access permits. For the list of supported resource types, see [Custom groups](https://docs.nebius.com/iam/authorization/groups.md#custom-groups).

     The available resources depend on the scope of the group:

     * A group created in a tenant can have permits for the tenant, any projects and resources within it.
     * A group created in a project can only have permits for this project and resources within it.

   * `role`: One of the [roles](https://docs.nebius.com/iam/authorization/roles.md) that provide a set of permissions.

### Examples

**CLI**

> **Project resources editors**
>
> In this example, you will create a group within a project that gives its members permissions to create, read, update or delete any resources in this project. However, the members of this group will not be able to manage groups and permissions. This set of permissions is provided by the `editor` role.
>
> Run the following command to create the group and an access permit, and save the group ID to an environment variable:
>
> ```bash theme={null}
> export PROJECT_EDITOR_GROUP_ID=$(nebius iam group create \
>   --parent-id <project_ID> \
>   --name my-project-editors \
>   --format jsonpath='{.metadata.id}')
>
> nebius iam access-permit create \
>   --parent-id $PROJECT_EDITOR_GROUP_ID \
>   --resource-id <project_ID> \
>   --role editor
> ```
>
> After the operation is completed, use the group ID in the `PROJECT_EDITOR_GROUP_ID` variable to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

> **Granular permissions within a tenant**
>
> In this example, you will create a group within a tenant that gives its members permissions to view all resources in the tenant but only manage one specific SecretStash secret. This set of permissions is provided by the `viewer` and `editor` roles for various resources.
>
> Run the following command to create the group and access permits, and save the group ID to an environment variable:
>
> ```bash theme={null}
> export SECRET_EDITOR_GROUP_ID=$(nebius iam group create \
>   --parent-id <tenant_ID> \
>   --name my-secret-editors \
>   --format jsonpath='{.metadata.id}')
>
> nebius iam access-permit create \
>   --parent-id $SECRET_EDITOR_GROUP_ID \
>   --resource-id <tenant_ID> \
>   --role viewer
>
> nebius iam access-permit create \
>   --parent-id $SECRET_EDITOR_GROUP_ID \
>   --resource-id <secret_ID> \
>   --role editor
> ```
>
> After the operation is completed, use the group ID in the `SECRET_EDITOR_GROUP_ID` variable to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

**Go SDK**

> **Project resources editors**
>
> In this example, you will create a group within a project that gives its members permissions to create, read, update or delete any resources in this project. However, the members of this group will not be able to manage groups and permissions. This set of permissions is provided by the `editor` role.
>
> Run the following code to create the group and an access permit. The code gets the new group's resource ID with `projectGroupOp.ResourceID()` and uses it as `Metadata.ParentId` for the access permit:
>
> ```go theme={null}
> projectGroupOp, err := sdk.Services().IAM().V1().Group().
>     Create(
>     ctx,
>     &iam.CreateGroupRequest{
>         Metadata: &common.ResourceMetadata{
>             ParentId: "<project_ID>",
>             Name:     "my-project-editors",
>         },
>     },
> )
> if err != nil {
>     return err
> }
> if _, err = projectGroupOp.Wait(ctx); err != nil {
>     return err
> }
> projectEditorGroupID := projectGroupOp.ResourceID()
> projectPermitOp, err := sdk.Services().IAM().V1().
>     AccessPermit().Create(
>         ctx,
>         &iam.CreateAccessPermitRequest{
>             Metadata: &common.ResourceMetadata{
>                 ParentId: projectEditorGroupID,
>             },
>             Spec: &iam.AccessPermitSpec{
>                 ResourceId: "<project_ID>",
>                 Role:       "editor",
>             },
>         },
>     )
> if err != nil {
>     return err
> }
> if _, err = projectPermitOp.Wait(ctx); err != nil {
>     return err
> }
> ```
>
> After the operation is completed, use the group's resource ID to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

> **Granular permissions within a tenant**
>
> In this example, you will create a group within a tenant that gives its members permissions to view all resources in the tenant but only manage one specific SecretStash secret. This set of permissions is provided by the `viewer` and `editor` roles for various resources.
>
> Run the following code to create the group and access permits. The code gets the new group's resource ID with `secretGroupOp.ResourceID()` and uses it as `Metadata.ParentId` for both access permits:
>
> ```go theme={null}
> secretGroupOp, err := sdk.Services().IAM().V1().Group().
>     Create(
>     ctx,
>     &iam.CreateGroupRequest{
>         Metadata: &common.ResourceMetadata{
>             ParentId: "<tenant_ID>",
>             Name:     "my-secret-editors",
>         },
>     },
> )
> if err != nil {
>     return err
> }
> if _, err = secretGroupOp.Wait(ctx); err != nil {
>     return err
> }
> secretEditorGroupID := secretGroupOp.ResourceID()
> tenantPermitOp, err := sdk.Services().IAM().V1().AccessPermit().
>     Create(ctx, &iam.CreateAccessPermitRequest{
>         Metadata: &common.ResourceMetadata{
>             ParentId: secretEditorGroupID,
>         },
>         Spec: &iam.AccessPermitSpec{
>             ResourceId: "<tenant_ID>",
>             Role:       "viewer",
>         },
>     })
> if err != nil {
>     return err
> }
> if _, err = tenantPermitOp.Wait(ctx); err != nil {
>     return err
> }
> secretPermitOp, err := sdk.Services().IAM().V1().AccessPermit().
>     Create(ctx, &iam.CreateAccessPermitRequest{
>         Metadata: &common.ResourceMetadata{
>             ParentId: secretEditorGroupID,
>         },
>         Spec: &iam.AccessPermitSpec{
>             ResourceId: "<secret_ID>",
>             Role:       "editor",
>         },
>     })
> if err != nil {
>     return err
> }
> if _, err = secretPermitOp.Wait(ctx); err != nil {
>     return err
> }
> ```
>
> After the operation is completed, use the group's resource ID to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

**Python SDK**

> **Project resources editors**
>
> In this example, you will create a group within a project that gives its members permissions to create, read, update or delete any resources in this project. However, the members of this group will not be able to manage groups and permissions. This set of permissions is provided by the `editor` role.
>
> Run the following code to create the group and an access permit. The code gets the new group's resource ID with `project_group_operation.resource_id` and uses it as `parent_id` for the access permit:
>
> ```python theme={null}
> project_group_service = GroupServiceClient(sdk)
> project_group_operation = await project_group_service.create(
>     CreateGroupRequest(
>         metadata=ResourceMetadata(
>             parent_id="<project_ID>",
>             name="my-project-editors",
>         ),
>     ),
> )
> await project_group_operation.wait()
> project_editor_group_id = project_group_operation.resource_id
> project_permit_service = AccessPermitServiceClient(sdk)
> project_permit_operation = await project_permit_service.create(
>     CreateAccessPermitRequest(
>         metadata=ResourceMetadata(
>             parent_id=project_editor_group_id,
>         ),
>         spec=AccessPermitSpec(
>             resource_id="<project_ID>",
>             role="editor",
>         ),
>     ),
> )
> await project_permit_operation.wait()
> ```
>
> After the operation is completed, use the group's resource ID to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

> **Granular permissions within a tenant**
>
> In this example, you will create a group within a tenant that gives its members permissions to view all resources in the tenant but only manage one specific SecretStash secret. This set of permissions is provided by the `viewer` and `editor` roles for various resources.
>
> Run the following code to create the group and access permits. The code gets the new group's resource ID with `secret_group_operation.resource_id` and uses it as `parent_id` for both access permits:
>
> ```python theme={null}
> secret_group_service = GroupServiceClient(sdk)
> secret_group_operation = await secret_group_service.create(
>     CreateGroupRequest(
>         metadata=ResourceMetadata(
>             parent_id="<tenant_ID>",
>             name="my-secret-editors",
>         ),
>     ),
> )
> await secret_group_operation.wait()
> secret_editor_group_id = secret_group_operation.resource_id
> secret_permit_service = AccessPermitServiceClient(sdk)
> tenant_permit = await secret_permit_service.create(
>     CreateAccessPermitRequest(
>         metadata=ResourceMetadata(
>             parent_id=secret_editor_group_id,
>         ),
>         spec=AccessPermitSpec(
>             resource_id="<tenant_ID>",
>             role="viewer",
>         ),
>     ),
> )
> await tenant_permit.wait()
> secret_permit = await secret_permit_service.create(
>     CreateAccessPermitRequest(
>         metadata=ResourceMetadata(
>             parent_id=secret_editor_group_id,
>         ),
>         spec=AccessPermitSpec(
>             resource_id="<secret_ID>",
>             role="editor",
>         ),
>     ),
> )
> await secret_permit.wait()
> ```
>
> After the operation is completed, use the group's resource ID to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

**JavaScript SDK**

> **Project resources editors**
>
> In this example, you will create a group within a project that gives its members permissions to create, read, update or delete any resources in this project. However, the members of this group will not be able to manage groups and permissions. This set of permissions is provided by the `editor` role.
>
> Run the following code to create the group and an access permit. The code gets the new group's resource ID with `projectGroupOperation.resourceId()` and uses it as `parentId` for the access permit:
>
> ```ts theme={null}
> const projectGroupService = new GroupService(sdk);
> const projectGroupOperation = await projectGroupService.create(
>   CreateGroupRequest.create({
>     metadata: ResourceMetadata.create({
>       parentId: "<project_ID>",
>       name: "my-project-editors",
>     }),
>   }),
> ).result;
> await projectGroupOperation.wait();
> const projectEditorGroupId = projectGroupOperation.resourceId();
> const projectPermitService = new AccessPermitService(sdk);
> const projectPermitOperation = await projectPermitService.create(
>   CreateAccessPermitRequest.create({
>     metadata: ResourceMetadata.create({
>       parentId: projectEditorGroupId,
>     }),
>     spec: AccessPermitSpec.create({
>       resourceId: "<project_ID>",
>       role: "editor",
>     }),
>   }),
> ).result;
> await projectPermitOperation.wait();
> ```
>
> After the operation is completed, use the group's resource ID to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

> **Granular permissions within a tenant**
>
> In this example, you will create a group within a tenant that gives its members permissions to view all resources in the tenant but only manage one specific SecretStash secret. This set of permissions is provided by the `viewer` and `editor` roles for various resources.
>
> Run the following code to create the group and access permits. The code gets the new group's resource ID with `secretGroupOperation.resourceId()` and uses it as `parentId` for both access permits:
>
> ```ts theme={null}
> const secretGroupService = new GroupService(sdk);
> const secretGroupOperation = await secretGroupService.create(
>   CreateGroupRequest.create({
>     metadata: ResourceMetadata.create({
>       parentId: "<tenant_ID>",
>       name: "my-secret-editors",
>     }),
>   }),
> ).result;
> await secretGroupOperation.wait();
> const secretEditorGroupId = secretGroupOperation.resourceId();
> const secretPermitService = new AccessPermitService(sdk);
> const tenantPermit = await secretPermitService.create(
>   CreateAccessPermitRequest.create({
>     metadata: ResourceMetadata.create({
>       parentId: secretEditorGroupId,
>     }),
>     spec: AccessPermitSpec.create({
>       resourceId: "<tenant_ID>",
>       role: "viewer",
>     }),
>   }),
> ).result;
> await tenantPermit.wait();
> const secretPermit = await secretPermitService.create(
>   CreateAccessPermitRequest.create({
>     metadata: ResourceMetadata.create({
>       parentId: secretEditorGroupId,
>     }),
>     spec: AccessPermitSpec.create({
>       resourceId: "<secret_ID>",
>       role: "editor",
>     }),
>   }),
> ).result;
> await secretPermit.wait();
> ```
>
> After the operation is completed, use the group's resource ID to [add members](https://docs.nebius.com/iam/authorization/groups/members.md) to this group.

## Revoking role assignments

To revoke the role that you previously assigned to a group:

**Web console**

Remove the access permit that assigned this role:

1. In the sidebar, go to  **Administration** → **IAM**.
2. Switch to the **Groups** tab and select the group you want to update.
3. On the group page, switch to the **Access permits** tab.
4. Click  → **Manage permits** next to the name of the resource.
5. In the window that opens, deselect individual permits or click **Delete permits** to remove all access permits from the group.

**CLI**

Delete the access permit that grants this role:

```bash theme={null}
nebius iam access-permit delete --id <access_permit_ID>
```

If you don't know the ID of the access permit, you can list all access permits for a group and find the one you need. Run the following command:

```bash theme={null}
nebius iam access-permit list --parent-id <group_ID>
```

Output example:

```yaml theme={null}
items:
  - metadata:
      created_at: "2025-05-14T11:28:31.685598Z"
      id: accesspermit-***
      parent_id: group-***
    spec:
      resource_id: tenant-***
      role: viewer
```

**Go SDK**

Delete the access permit that grants this role:

```go theme={null}
deleteAccessPermit, err := sdk.Services().IAM().V1().
    AccessPermit().Delete(
        ctx,
        &iam.DeleteAccessPermitRequest{
            Id: "<access_permit_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = deleteAccessPermit.Wait(ctx); err != nil {
    return err
}
```

Set `Id` to the ID of the access permit that you want to delete.

If you don't know the ID of the access permit, you can list all access permits for a group and find the one you need:

```go theme={null}
accessPermitListService := sdk.Services().IAM().V1().
    AccessPermit()
accessPermitsByGroup, err := accessPermitListService.List(
    ctx,
    &iam.ListAccessPermitRequest{
        ParentId: "<group_ID>",
    },
)
if err != nil {
    return err
}
fmt.Println(accessPermitsByGroup)
```

Set `ParentId` to the group's ID. The response returns the access permits in `Items`, with each item's ID available at `Metadata.GetId()`.

**Python SDK**

Delete the access permit that grants this role:

```python theme={null}
access_permit_service = AccessPermitServiceClient(sdk)
delete_access_permit = await access_permit_service.delete(
    DeleteAccessPermitRequest(id="<access_permit_ID>"),
)
await delete_access_permit.wait()
```

Set `id` to the ID of the access permit that you want to delete.

If you don't know the ID of the access permit, you can list all access permits for a group and find the one you need:

```python theme={null}
access_permit_service = AccessPermitServiceClient(sdk)
access_permits_by_group = await access_permit_service.list(
    ListAccessPermitRequest(parent_id="<group_ID>"),
)
print(access_permits_by_group)
```

Set `parent_id` to the group's ID. The response returns the access permits in `items`, with each item's ID available at `metadata.id`.

**JavaScript SDK**

Delete the access permit that grants this role:

```ts theme={null}
const deleteAccessPermitService =
  new AccessPermitService(sdk);
const deleteAccessPermit = await deleteAccessPermitService.delete(
  DeleteAccessPermitRequest.create({id: "<access_permit_ID>"}),
).result;
await deleteAccessPermit.wait();
```

Set `id` to the ID of the access permit that you want to delete.

If you don't know the ID of the access permit, you can list all access permits for a group and find the one you need:

```ts theme={null}
const accessPermitListService =
  new AccessPermitService(sdk);
const accessPermitsByGroup = await accessPermitListService.list(
  ListAccessPermitRequest.create({
    parentId: "<group_ID>",
  }),
);
console.log(accessPermitsByGroup);
```

Set `parentId` to the group's ID. The response returns the access permits in `items`, with each item's ID available at `metadata.id`.
