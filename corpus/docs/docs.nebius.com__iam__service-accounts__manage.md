# How to manage service accounts

Source: https://docs.nebius.com/iam/service-accounts/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage service accounts

In this guide, you will learn how to create a service account, grant it access rights and delete it.

## Prerequisites

> [!TIP]
>
> You do not need to complete any prerequisites if you create a service account in the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Install [jq](https://jqlang.github.io/jq/download/) to extract IDs and tokens from JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. [Get the tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2) and save it to an environment variable:

   ```bash theme={null}
   export TENANT_ID=<tenant_ID>
   ```

**Terraform**

[Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## Creating a service account

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.
2. Click **Create resource** → **Service account**.
3. In the window that opens, check the service account name and select the project.
4. Click **Create and continue**.

**CLI**

Create a service account and save its ID to an environment variable:

```bash theme={null}
export SA_ID=$(nebius iam service-account create \
  --name <service_account_name> \
  --format jsonpath='{.metadata.id}')
```

**Terraform**

1. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_iam_v1_service_account" "<service_account_name>" {
     name        = "<service_account_name>"
     parent_id   = "<project_ID>"
     description = "My service account"
   }
   ```

   In the configuration, specify your [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).

2. Validate the configuration:

   Check that the configuration is correct:

   ```bash theme={null}
   terraform validate
   ```

3. If the configuration is valid, apply it:

   Apply the changes:

   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a service account and save its ID to a variable:

```go theme={null}
serviceAccountOperation, err := sdk.Services().IAM().V1().
    ServiceAccount().Create(
        ctx,
        &iam.CreateServiceAccountRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<service_account_name>",
            },
            Spec: &iam.ServiceAccountSpec{},
        },
    )
if err != nil {
    return err
}
if _, err = serviceAccountOperation.Wait(ctx); err != nil {
    return err
}
serviceAccountID := serviceAccountOperation.ResourceID()
```

**Python SDK**

Create a service account and save its ID to a variable:

```python theme={null}
service_account_service = ServiceAccountServiceClient(sdk)
service_account_operation = await service_account_service.create(
    CreateServiceAccountRequest(
        metadata=ResourceMetadata(name="<service_account_name>"),
        spec=ServiceAccountSpec(),
    ),
)
await service_account_operation.wait()
service_account_id = service_account_operation.resource_id
```

**JavaScript SDK**

Create a service account and save its ID to a variable:

```ts theme={null}
const serviceAccountCreateService =
  new ServiceAccountService(sdk);
const serviceAccountOperation =
  await serviceAccountCreateService.create(
    CreateServiceAccountRequest.create({
      metadata: ResourceMetadata.create({
        name: "<service_account_name>",
      }),
      spec: ServiceAccountSpec.create({}),
    }),
  ).result;
await serviceAccountOperation.wait();
let serviceAccountId =
  serviceAccountOperation.resourceId();
```

## Granting editor access to the service account

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

To grant access rights to the service account:

**Web console**

1. On the **Service accounts** tab, locate the required service account and click  → **Add to group**.

**CLI**

1. Get the ID of the default `editors` group:

   ```bash theme={null}
   nebius iam group get-by-name \
     --name editors --parent-id <tenant_ID> \
     --format jsonpath='{.metadata.id}'
   ```

   In the command, specify the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).

2. Add the service account to the `editors` group:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id <editors_group_ID> \
     --member-id <service_account_ID>
   ```

**Terraform**

1. Get and copy the ID of the default `editors` group:

   ```bash theme={null}
   nebius iam group get-by-name \
     --name editors --parent-id <tenant_ID> \
     --format jsonpath='{.metadata.id}'
   ```

   In the command, specify the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).

2. Add the `nebius_iam_v1_group_membership` resource to the configuration file. By using this resource, you add the service account to the `editors` group:

   ```hcl theme={null}
   resource "nebius_iam_v1_group_membership" "sa_editors" {
     parent_id = "<editors_group_ID>"
     member_id = nebius_iam_v1_service_account.<service_account_name>.id
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

**Go SDK**

1. Get the ID of the default `editors` group:

   ```go theme={null}
   editorsGroup, err := sdk.Services().IAM().V1().Group().
       GetByName(
       ctx,
       &iam.GetGroupByNameRequest{
           ParentId: "<tenant_ID>",
           Name:     "editors",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(editorsGroup.GetMetadata().GetId())
   ```

   In the code, set the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).

2. Add the service account to the `editors` group:

   ```go theme={null}
   membershipOperation, err := sdk.Services().IAM().V1().
       GroupMembership().Create(
           ctx,
           &iam.CreateGroupMembershipRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<editors_group_ID>",
               },
               Spec: &iam.GroupMembershipSpec{
                   MemberId: "<service_account_ID>",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = membershipOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the ID of the default `editors` group:

   ```python theme={null}
   group_service = GroupServiceClient(sdk)
   editors_group = await group_service.get_by_name(
       GetGroupByNameRequest(
           parent_id="<tenant_ID>",
           name="editors",
       ),
   )
   print(editors_group.metadata.id)
   ```

   In the code, set the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).

2. Add the service account to the `editors` group:

   ```python theme={null}
   membership_service = GroupMembershipServiceClient(sdk)
   membership_operation = await membership_service.create(
       CreateGroupMembershipRequest(
           metadata=ResourceMetadata(
               parent_id="<editors_group_ID>",
           ),
           spec=GroupMembershipSpec(
               member_id="<service_account_ID>",
           ),
       ),
   )
   await membership_operation.wait()
   ```

**JavaScript SDK**

1. Get the ID of the default `editors` group:

   ```ts theme={null}
   const groupService = new GroupService(sdk);
   const editorsGroup = await groupService.getByName(
     GetGroupByNameRequest.create({
       parentId: "<tenant_ID>",
       name: "editors",
     }),
   );
   console.log(editorsGroup.metadata?.id);
   ```

   In the code, set the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).

2. Add the service account to the `editors` group:

   ```ts theme={null}
   const membershipService = new GroupMembershipService(sdk);
   const membershipOperation = await membershipService.create(
     CreateGroupMembershipRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<editors_group_ID>",
       }),
       spec: GroupMembershipSpec.create({
         memberId: "<service_account_ID>",
       }),
     }),
   ).result;
   await membershipOperation.wait();
   ```

## Deleting a service account

> [!WARNING]
>
> Deleting a service account cannot be reversed.

If you no longer need a service account:

**Web console**

1. Delete all resources associated with the account.
2. On the **Service accounts** tab, find the required service account and click  → **Delete service account**.
3. In the window that opens, confirm the deletion.

**CLI**

1. Delete all resources associated with the account.

2. Get the service account ID and save it to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account get-by-name \
     --name <service_account_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Delete the service account:

   ```bash theme={null}
   nebius iam service-account delete --id $SA_ID
   ```

**Terraform**

1. Delete all resources associated with the account.
2. Remove the corresponding `nebius_iam_v1_service_account` resource from the configuration file.
3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Delete all resources associated with the account.

2. Get the service account ID and save it to a variable:

   ```go theme={null}
   serviceAccount, err := sdk.Services().IAM().V1().
       ServiceAccount().GetByName(
           ctx,
           &iam.GetServiceAccountByNameRequest{
               Name: "<service_account_name>",
           },
       )
   if err != nil {
       return err
   }
   lookedUpServiceAccountID := serviceAccount.GetMetadata().GetId()
   fmt.Println(lookedUpServiceAccountID)
   ```

3. Delete the service account:

   ```go theme={null}
   deleteServiceAccount, err := sdk.Services().IAM().V1().
       ServiceAccount().Delete(
           ctx,
           &iam.DeleteServiceAccountRequest{
               Id: "<service_account_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = deleteServiceAccount.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Delete all resources associated with the account.

2. Get the service account ID and save it to a variable:

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(name="<service_account_name>"),
   )
   service_account_id = service_account.metadata.id
   print(service_account_id)
   ```

3. Delete the service account:

   ```python theme={null}
   delete_service_account_service = (
       ServiceAccountServiceClient(sdk)
   )
   delete_service_account = await delete_service_account_service.delete(
       DeleteServiceAccountRequest(id="<service_account_ID>"),
   )
   await delete_service_account.wait()
   ```

**JavaScript SDK**

1. Delete all resources associated with the account.

2. Get the service account ID and save it to a variable:

   ```ts theme={null}
   const serviceAccountLookupService =
     new ServiceAccountService(sdk);
   const serviceAccount =
     await serviceAccountLookupService.getByName(
       GetServiceAccountByNameRequest.create({
         name: "<service_account_name>",
       }),
     );
   const lookedUpServiceAccountId = serviceAccount.metadata?.id;
   if (!lookedUpServiceAccountId) {
     throw new Error("service account ID is missing");
   }
   console.log(lookedUpServiceAccountId);
   ```

3. Delete the service account:

   ```ts theme={null}
   const deleteServiceAccountService =
     new ServiceAccountService(sdk);
   const deleteServiceAccount =
     await deleteServiceAccountService.delete(
       DeleteServiceAccountRequest.create({
         id: "<service_account_ID>",
       }),
     ).result;
   await deleteServiceAccount.wait();
   ```
