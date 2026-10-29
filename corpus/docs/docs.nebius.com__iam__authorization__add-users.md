# How to invite users to a tenant

Source: https://docs.nebius.com/iam/authorization/add-users

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to invite users to a tenant

You can add users in one of the following ways:

* If you have created a [federation](https://docs.nebius.com/iam/overview.md#federations) and configured single sign-on, you can create user accounts in your application in one of the [supported identity providers](https://docs.nebius.com/iam/federations/saml-sso.md).

  Then, users can sign in to Nebius AI Cloud by using the federation ID.

* If you do not have a federation or you want to use an alternative method, you can send invitations to users from Nebius AI Cloud. In this case, users receive their invitations via email. Once the user accepts the invitation, they can [sign in by using any available method](https://docs.nebius.com/iam/log-in.md#how-to-sign-in-to-the-web-console), including the federation ID.

  By default, an invitation is valid for three days. When you create invitations by using the CLI, you can customize this period with the `--expires-in` parameter.

## Sending an invitation

To send an invitation, do the following:

1. Create it:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.
   2. On the **Users** tab, click **Invite user**.
   3. In the window that opens, specify the **Email** of the user whom you would like to invite.
   4. (Optional) From the **Groups** list, select the groups you want to add the user to. You can skip the next step to add the user to a group if you set group membership when you create the invitation.
   5. Click **Invite user**.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius iam invitation create --parent-id <tenant_ID> --email <user_email> --expires-in 24h 
   ```

   In the command, specify:

   * `--email`: Email of the user whom you would like to invite.
   * `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
   * `--expires-in` (optional): How long the invitation remains valid after creation. If omitted, the invitation is valid for three days.

   **Terraform**

   1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

   2. Create the following configuration file:

      ```hcl theme={null}
      resource "nebius_iam_v1_invitation" "<invitation_name>" {
        parent_id = "<tenant_ID>"
        email     = "<user_email>"
      }
      ```

      In the file, specify:

      * `email`: Email of the user whom you would like to invite.
      * `parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md).

   3. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   4. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

   **Go SDK**

   Run the following code:

   ```go theme={null}
   invitationOperation, err := sdk.Services().IAM().V1().
       Invitation().Create(
           ctx,
           &iam.CreateInvitationRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<tenant_ID>",
               },
               Spec: &iam.InvitationSpec{
                   Contact: &iam.InvitationSpec_Email{
                       Email: "<user_email>",
                   },
               },
               ExpiresIn: durationpb.New(24 * time.Hour),
           },
       )
   if err != nil {
       return err
   }
   if _, err = invitationOperation.Wait(ctx); err != nil {
       return err
   }
   invitationID := invitationOperation.ResourceID()
   ```

   In the code, set the following parameters:

   * `Metadata.ParentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).
   * `Spec.Contact` (`&iam.InvitationSpec_Email{Email: ...}`): Email of the user whom you would like to invite.
   * `ExpiresIn`: How long the invitation remains valid after creation. The code sets it to 24 hours.

   **Python SDK**

   Run the following code:

   ```python theme={null}
   invitation_service = InvitationServiceClient(sdk)
   invitation_operation = await invitation_service.create(
       CreateInvitationRequest(
           metadata=ResourceMetadata(parent_id="<tenant_ID>"),
           spec=InvitationSpec(email="<user_email>"),
           expires_in=timedelta(hours=24),
       ),
   )
   await invitation_operation.wait()
   invitation_id = invitation_operation.resource_id
   ```

   In the code, set the following parameters:

   * `metadata.parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).
   * `spec` (`InvitationSpec(email=...)`): Email of the user whom you would like to invite.
   * `expires_in`: How long the invitation remains valid after creation. The code sets it to 24 hours.

   **JavaScript SDK**

   Run the following code:

   ```ts theme={null}
   const createInvitationService = new InvitationService(sdk);
   const invitationOperation = await createInvitationService.create(
     CreateInvitationRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<tenant_ID>",
       }),
       spec: InvitationSpec.create({
         contact: {$case: "email", email: "<user_email>"},
       }),
       expiresIn: {seconds: 86400},
     }),
   ).result;
   await invitationOperation.wait();
   const invitationId = invitationOperation.resourceId();
   ```

   In the code, set the following parameters:

   * `metadata.parentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).
   * `spec` (`InvitationSpec.create({contact: {$case: "email", email: ...}})`): Email of the user whom you would like to invite.
   * `expiresIn`: How long the invitation remains valid after creation. The code sets it to 24 hours.

   The invitation to the tenant is sent to the specified email.

2. Add the user to the required group. You can do it at any time, even before the user accepts their invitation.

   **Web console**

   Only do this if the user wasn't added to a group during invitation in the previous step.

   1. In the sidebar, go to  **Administration** → **IAM**.

   2. On the **Users** tab, find the user. To find a user with a pending invitation, filter the list by **Status** and select `Invited`.

      To find a user with an expired invitation, filter the list by **Status** and select `Expired`. Next to the user, click  → **Resend invitation**. The user will reappear in the list of invited users.

   3. Next to the user, click  → **Add user to group**.

   4. In the window that opens, select the groups you want to add the user to.

   5. Click **Close**.

   **CLI**

   1. Get a list of groups, so you can choose the group for the user and copy the group ID:

      ```bash theme={null}
      nebius iam group list --parent-id <tenant_ID>
      ```

      Save the `metadata.id` value for the required group.

   2. Get the ID of the invited user:

      ```bash theme={null}
      nebius iam invitation list --parent-id <tenant_ID>
      ```

      Save the `status.tenant_user_account_id` value for the required user.

   3. Assign the group to the user:

      ```bash theme={null}
      nebius iam group-membership create \
        --parent-id group-*** \
        --member-id tenantuseraccount-***
      ```

      Specify the group and user ID that you saved earlier.

   **Terraform**

   1. In the directory with the already created Terraform manifest, add the following configuration file:

      ```hcl theme={null}
      resource "nebius_iam_v1_group_membership" "<group_membership_name>" {
        parent_id = data.nebius_iam_v1_group.<group_name>.id
        member_id = nebius_iam_v1_invitation.<invitation_name>.status.tenant_user_account_id
      }

      data "nebius_iam_v1_group" "<group_name>" {
        parent_id = "<tenant_ID>"
        name      = "<group_name>"
      }
      ```

      The file contains the following:

      * Resource that adds a group to the user. In the resource, specify the names of the group and invitation resources.
      * Data source that you use to get the group ID. In the data source, specify the tenant ID and the name of the group to which you want to add the user.

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

   **Go SDK**

   1. Get a list of groups, so you can choose the group for the user and copy the group ID:

      ```go theme={null}
      listedGroups, err := sdk.Services().IAM().V1().Group().List(
          ctx,
          &iam.ListGroupsRequest{ParentId: "<tenant_ID>"},
      )
      if err != nil {
          return err
      }
      fmt.Println(listedGroups)
      ```

      The response returns the groups in `Items`, with each item's ID available at `Metadata.GetId()`.

   2. Get the ID of the invited user:

      ```go theme={null}
      listedInvitations, err := sdk.Services().IAM().V1().
          Invitation().List(
          ctx,
          &iam.ListInvitationsRequest{ParentId: "<tenant_ID>"},
      )
      if err != nil {
          return err
      }
      fmt.Println(listedInvitations)
      ```

      The response returns the invitations in `Items`, with each item's user ID available at `Status.GetTenantUserAccountId()`.

   3. Assign the group to the user:

      ```go theme={null}
      membershipOperation, err := sdk.Services().IAM().V1().
          GroupMembership().Create(
              ctx,
              &iam.CreateGroupMembershipRequest{
                  Metadata: &common.ResourceMetadata{
                      ParentId: "<group_ID>",
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

      Set `Metadata.ParentId` to the group ID and `Spec.MemberId` to the user ID that you saved earlier.

   **Python SDK**

   1. Get a list of groups, so you can choose the group for the user and copy the group ID:

      ```python theme={null}
      group_service = GroupServiceClient(sdk)
      listed_groups = await group_service.list(
          ListGroupsRequest(parent_id="<tenant_ID>"),
      )
      print(listed_groups)
      ```

      The response returns the groups in `items`, with each item's ID available at `metadata.id`.

   2. Get the ID of the invited user:

      ```python theme={null}
      invitation_service = InvitationServiceClient(sdk)
      listed_invitations = await invitation_service.list(
          ListInvitationsRequest(parent_id="<tenant_ID>"),
      )
      print(listed_invitations)
      ```

      The response returns the invitations in `items`, with each item's user ID available at `status.tenant_user_account_id`.

   3. Assign the group to the user:

      ```python theme={null}
      membership_service = GroupMembershipServiceClient(sdk)
      membership_operation = await membership_service.create(
          CreateGroupMembershipRequest(
              metadata=ResourceMetadata(parent_id="<group_ID>"),
              spec=GroupMembershipSpec(member_id="<service_account_ID>"),
          ),
      )
      await membership_operation.wait()
      ```

      Set `metadata.parent_id` to the group ID and `spec.member_id` to the user ID that you saved earlier.

   **JavaScript SDK**

   1. Get a list of groups, so you can choose the group for the user and copy the group ID:

      ```ts theme={null}
      const groupService = new GroupService(sdk);
      const listedGroups = await groupService.list(
        ListGroupsRequest.create({parentId: "<tenant_ID>"}),
      );
      console.log(listedGroups);
      ```

      The response returns the groups in `items`, with each item's ID available at `metadata.id`.

   2. Get the ID of the invited user:

      ```ts theme={null}
      const listInvitationService = new InvitationService(sdk);
      const listedInvitations = await listInvitationService.list(
        ListInvitationsRequest.create({parentId: "<tenant_ID>"}),
      );
      console.log(listedInvitations);
      ```

      The response returns the invitations in `items`, with each item's user ID available at `status.tenantUserAccountId`.

   3. Assign the group to the user:

      ```ts theme={null}
      const membershipService = new GroupMembershipService(sdk);
      const membershipOperation = await membershipService.create(
        CreateGroupMembershipRequest.create({
          metadata: ResourceMetadata.create({
            parentId: "<group_ID>",
          }),
          spec: GroupMembershipSpec.create({
            memberId: "<service_account_ID>",
          }),
        }),
      ).result;
      await membershipOperation.wait();
      ```

      Set `metadata.parentId` to the group ID and `spec.memberId` to the user ID that you saved earlier.

The user is added to the specified group. Now, the user has access to the tenant and they can manage resources within it.

## Checking invitation status

After you send an invitation, you can check its status.

**Web console**

On the **Users** tab in the [web console](https://console.nebius.com/iam/users), the **Status** column shows whether a user is `Active`, `Invited`, `Expired` or `Blocked`. You can filter the list by **Status**.

For a user with the `Invited` status, you can see how many days are left before the invitation expires.

For a user with the `Expired` status, you can only resend or delete the invitation. You can't **Add user to group** until you [resend the invitation](#resending-an-invitation).

**CLI**

Get a list of invitations in the tenant:

```bash theme={null}
nebius iam invitation list --parent-id <tenant_ID>
```

For each invitation, the response returns:

* `metadata.id`: Invitation ID
* `status.state`: Invitation state, such as `PENDING`, `ACCEPTED` or `EXPIRED`
* `status.expires_at`: Date and time when the invitation expires

Save the `metadata.id` value for the required invitation. You need it to update, resend or delete the invitation.

**Go SDK**

Get a list of invitations in the tenant:

```go theme={null}
listedInvitations, err := sdk.Services().IAM().V1().
    Invitation().List(
    ctx,
    &iam.ListInvitationsRequest{ParentId: "<tenant_ID>"},
)
if err != nil {
    return err
}
fmt.Println(listedInvitations)
```

The response returns the invitations in `Items`. For each item, the response returns:

* `Metadata.GetId()`: Invitation ID
* `Status.GetState()`: Invitation state, such as `PENDING`, `ACCEPTED` or `EXPIRED`
* `Status.GetExpiresAt()`: Date and time when the invitation expires

Save the ID of the required invitation. You need it to update, resend or delete the invitation.

**Python SDK**

Get a list of invitations in the tenant:

```python theme={null}
invitation_service = InvitationServiceClient(sdk)
listed_invitations = await invitation_service.list(
    ListInvitationsRequest(parent_id="<tenant_ID>"),
)
print(listed_invitations)
```

The response returns the invitations in `items`. For each item, the response returns:

* `metadata.id`: Invitation ID
* `status.state`: Invitation state, such as `PENDING`, `ACCEPTED` or `EXPIRED`
* `status.expires_at`: Date and time when the invitation expires

Save the `metadata.id` value for the required invitation. You need it to update, resend or delete the invitation.

**JavaScript SDK**

Get a list of invitations in the tenant:

```ts theme={null}
const listInvitationService = new InvitationService(sdk);
const listedInvitations = await listInvitationService.list(
  ListInvitationsRequest.create({parentId: "<tenant_ID>"}),
);
console.log(listedInvitations);
```

The response returns the invitations in `items`. For each item, the response returns:

* `metadata.id`: Invitation ID
* `status.state`: Invitation state
* `status.expiresAt`: Date and time when the invitation expires

Save the ID of the required invitation. You need it to update, resend or delete the invitation.

## Updating an invitation

If you sent an invitation to a wrong email address, you can change the address instead of creating a new invitation. To notify the new recipient, [resend the invitation](#resending-an-invitation) afterward.

**Web console**

You can't change the email address of an invitation in the web console directly.

Delete the invitation, then send a new one to the correct address.

**CLI**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Change the email address:

   ```bash theme={null}
   nebius iam invitation update <invitation_ID> \
     --patch \
     --email <new_user_email>
   ```

   In the command, specify:

   * `<invitation_ID>`: ID of the invitation that you saved earlier
   * `--email`: New email of the user whom you would like to invite
   * `--patch`: Updates only the parameters that you specify and keeps the rest of the invitation unchanged

**Go SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Change the email address:

   ```go theme={null}
   invitationForUpdate, err := sdk.Services().IAM().
       V1().Invitation().Get(
           ctx,
           &iam.GetInvitationRequest{Id: "<invitation_ID>"},
       )
   if err != nil {
       return err
   }
   invitationForUpdate.GetSpec().Contact =
       &iam.InvitationSpec_Email{Email: "<new_user_email>"}
   updateInvitationOperation, err := sdk.Services().IAM().
       V1().Invitation().Update(
           ctx,
           &iam.UpdateInvitationRequest{
               Metadata: invitationForUpdate.GetMetadata(),
               Spec:     invitationForUpdate.GetSpec(),
           },
       )
   if err != nil {
       return err
   }
   if _, err = updateInvitationOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   In the code, set the following parameters:

   * `GetInvitationRequest.Id`: ID of the invitation that you saved earlier
   * `Spec.Contact` (`&iam.InvitationSpec_Email{Email: ...}`): New email of the user whom you would like to invite

   The code gets the invitation before updating it, so that the parameters you don't change keep their values.

**Python SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Change the email address:

   ```python theme={null}
   invitation_service = InvitationServiceClient(sdk)
   invitation = await invitation_service.get(
       GetInvitationRequest(id="<invitation_ID>"),
   )
   if invitation.metadata is None or invitation.spec is None:
       raise ValueError("invitation resource is incomplete")
   invitation.spec.email = "<new_user_email>"
   update_invitation_operation = await invitation_service.update(
       UpdateInvitationRequest(
           metadata=invitation.metadata,
           spec=invitation.spec,
       ),
   )
   await update_invitation_operation.wait()
   ```

   In the code, set the following parameters:

   * `GetInvitationRequest.id`: ID of the invitation that you saved earlier
   * `invitation.spec.email`: New email of the user whom you would like to invite

   The code gets the invitation before updating it, so that the parameters you don't change keep their values.

**JavaScript SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Change the email address:

   ```ts theme={null}
   const updateInvitationService = new InvitationService(sdk);
   const invitationForUpdate = await updateInvitationService.get(
     GetInvitationRequest.create({id: "<invitation_ID>"}),
   );
   if (!invitationForUpdate.metadata ||
       !invitationForUpdate.spec) {
     throw new Error("invitation resource is incomplete");
   }
   invitationForUpdate.spec.contact = {
     $case: "email",
     email: "<new_user_email>",
   };
   const updateInvitationOperation =
     await updateInvitationService.update(
       UpdateInvitationRequest.create({
         metadata: invitationForUpdate.metadata,
         spec: invitationForUpdate.spec,
       }),
     ).result;
   await updateInvitationOperation.wait();
   ```

   In the code, set the following parameters:

   * `GetInvitationRequest.id`: ID of the invitation that you saved earlier
   * `spec.contact` (`{$case: "email", email: ...}`): New email of the user whom you would like to invite

   The code gets the invitation before updating it, so that the parameters you don't change keep their values.

## Resending an invitation

If the invitation expired or the user didn't receive the email, you can send the invitation again.

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.

2. On the **Users** tab, find the user.

   To find a user with an expired invitation, filter the list by **Status** and select `Expired`.

3. Next to the user, click  → **Resend invitation**.

   The user will reappear in the list of invited users.

**CLI**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Resend the invitation:

   ```bash theme={null}
   nebius iam invitation resend <invitation_ID>
   ```

   Specify the invitation ID that you saved earlier.

**Go SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Resend the invitation:

   ```go theme={null}
   resendInvitation, err := sdk.Services().IAM().V1().
       Invitation().Resend(
           ctx,
           &iam.ResendInvitationRequest{Id: "<invitation_ID>"},
       )
   if err != nil {
       return err
   }
   if _, err = resendInvitation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set `ResendInvitationRequest.Id` to the invitation ID that you saved earlier.

**Python SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Resend the invitation:

   ```python theme={null}
   invitation_service = InvitationServiceClient(sdk)
   resend_invitation = await invitation_service.resend(
       ResendInvitationRequest(id="<invitation_ID>"),
   )
   await resend_invitation.wait()
   ```

   Set `ResendInvitationRequest.id` to the invitation ID that you saved earlier.

**JavaScript SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Resend the invitation:

   ```ts theme={null}
   const resendInvitationService = new InvitationService(sdk);
   const resendInvitation = await resendInvitationService.resend(
     ResendInvitationRequest.create({id: "<invitation_ID>"}),
   ).result;
   await resendInvitation.wait();
   ```

   Set `ResendInvitationRequest.id` to the invitation ID that you saved earlier.

## Deleting an invitation

Deleting an invitation cancels it, so the user can no longer accept it. To invite the user later, [send a new invitation](#sending-an-invitation).

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.

2. On the **Users** tab, find the user.

   To find a user with a pending invitation, filter the list by **Status** and select `Invited`.

3. Next to the user, click  → **Delete invitation**.

**CLI**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Delete the invitation:

   ```bash theme={null}
   nebius iam invitation delete <invitation_ID>
   ```

   Specify the invitation ID that you saved earlier.

**Go SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Delete the invitation:

   ```go theme={null}
   deleteInvitation, err := sdk.Services().IAM().V1().
       Invitation().Delete(
           ctx,
           &iam.DeleteInvitationRequest{Id: "<invitation_ID>"},
       )
   if err != nil {
       return err
   }
   if _, err = deleteInvitation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set `DeleteInvitationRequest.Id` to the invitation ID that you saved earlier.

**Python SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Delete the invitation:

   ```python theme={null}
   invitation_service = InvitationServiceClient(sdk)
   delete_invitation = await invitation_service.delete(
       DeleteInvitationRequest(id="<invitation_ID>"),
   )
   await delete_invitation.wait()
   ```

   Set `DeleteInvitationRequest.id` to the invitation ID that you saved earlier.

**JavaScript SDK**

1. Get the ID of the invitation, as described in [Checking invitation status](#checking-invitation-status).
2. Delete the invitation:

   ```ts theme={null}
   const deleteInvitationService = new InvitationService(sdk);
   const deleteInvitation = await deleteInvitationService.delete(
     DeleteInvitationRequest.create({id: "<invitation_ID>"}),
   ).result;
   await deleteInvitation.wait();
   ```

   Set `DeleteInvitationRequest.id` to the invitation ID that you saved earlier.
