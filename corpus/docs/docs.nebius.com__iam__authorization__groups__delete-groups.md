# How to delete groups

Source: https://docs.nebius.com/iam/authorization/groups/delete-groups

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to delete groups

You can delete any group, whether default or custom. After you delete a group, its users and service accounts will lose their access rights assigned within this group. Deleting a group is permanent and irreversible.

If you are part of the `admins` group and you delete it, you lose access rights of the `admin` role in the tenant. To recover access, [contact support](https://console.nebius.com/support/create-ticket).

To delete a group, do the following:

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM**.
2. On the **Groups** tab, in the line of the required group, click  → **Delete**.
3. In the window that opens, confirm the deletion.

**CLI**

1. Get the group ID:

   ```bash theme={null}
   nebius iam group list --parent-id <tenant_ID>
   ```

2. Delete the group:

   ```bash theme={null}
   nebius iam group delete --id <group_ID>
   ```

**Go SDK**

1. Get the group ID:

   ```go theme={null}
   groupService := sdk.Services().IAM().V1().Group()
   listedGroups, err := groupService.List(
       ctx,
       &iam.ListGroupsRequest{ParentId: "<tenant_ID>"},
   )
   if err != nil {
       return err
   }
   fmt.Println(listedGroups)
   ```

2. Delete the group:

   ```go theme={null}
   deleteSecretGroup, err := sdk.Services().IAM().V1().
       Group().Delete(
       ctx,
       &iam.DeleteGroupRequest{Id: "<group_ID>"},
   )
   if err != nil {
       return err
   }
   if _, err = deleteSecretGroup.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the group ID:

   ```python theme={null}
   group_service = GroupServiceClient(sdk)
   listed_groups = await group_service.list(
       ListGroupsRequest(parent_id="<tenant_ID>"),
   )
   print(listed_groups)
   ```

2. Delete the group:

   ```python theme={null}
   group_service = GroupServiceClient(sdk)
   delete_group = await group_service.delete(
       DeleteGroupRequest(id="<group_ID>"),
   )
   await delete_group.wait()
   ```

**JavaScript SDK**

1. Get the group ID:

   ```ts theme={null}
   const groupService =
     new GroupService(sdk);
   const listedGroups = await groupService.list(
     ListGroupsRequest.create({parentId: "<tenant_ID>"}),
   );
   console.log(listedGroups);
   ```

2. Delete the group:

   ```ts theme={null}
   const secretGroupDeleteService = new GroupService(sdk);
   const secretGroupDelete = await secretGroupDeleteService.delete(
     DeleteGroupRequest.create({id: "<group_ID>"}),
   ).result;
   await secretGroupDelete.wait();
   ```
