# How to add accounts to groups

Source: https://docs.nebius.com/iam/authorization/groups/members

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to add accounts to groups

To grant users and service accounts access to tenant resources, add them to one of the [groups](https://docs.nebius.com/iam/authorization/groups/index.md).

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Install jq to extract IDs and tokens from JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

5. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM**.

6. If the group was created in a tenant, [get the tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2) and save it to an environment variable:

   ```bash theme={null}
   export TENANT_ID=<tenant_ID>
   ```

7. If the group was created in a project, [get the project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3) and save it to an environment variable:

   ```bash theme={null}
   export PROJECT_ID=<project_ID>
   ```

8. Get the relevant group ID and save it to an environment variable:

   ```bash theme={null}
   export GROUP_ID=$(nebius iam group get-by-name \
     --name <group_name> \
     --parent-id <$TENANT_ID|$PROJECT_ID> \
     --format jsonpath='{.metadata.id}')
   ```

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. If the group was created in a tenant, get the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).
4. If the group was created in a project, get the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
5. Get the relevant group ID:

   ```go theme={null}
   group, err := sdk.Services().IAM().V1().Group().GetByName(
       ctx,
       &iam.GetGroupByNameRequest{
           Name: "<group_name>",
           ParentId: "<tenant_ID|project_ID>",
       },
   )
   if err != nil {
       return err
   }
   groupID := group.GetMetadata().GetId()
   fmt.Println(groupID)
   ```

   Set the group's name in `Name` and its tenant or project ID in `ParentId`.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. If the group was created in a tenant, get the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).
4. If the group was created in a project, get the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
5. Get the relevant group ID:

   ```python theme={null}
   group_service = GroupServiceClient(sdk)
   group = await group_service.get_by_name(
       GetGroupByNameRequest(
           name="<group_name>",
           parent_id="<tenant_ID|project_ID>",
       ),
   )
   group_id = group.metadata.id
   print(group_id)
   ```

   Set the group's name in `name` and its tenant or project ID in `parent_id`.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. If the group was created in a tenant, get the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).
4. If the group was created in a project, get the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
5. Get the relevant group ID:

   ```ts theme={null}
   const groupService = new GroupService(sdk);
   const group = await groupService.getByName(
     GetGroupByNameRequest.create({
       name: "<group_name>",
       parentId: "<tenant_ID|project_ID>",
     }),
   );
   const groupId = group.metadata?.id;
   console.log(groupId);
   ```

   Set the group's name in `name` and its tenant or project ID in `parentId`.

## Adding a user account

**Web console**

To add a user to a group:

1. In the sidebar, go to  **Administration** → **IAM**.
2. On the **Groups** tab, click the group you want to add a user to.
3. Click **Add members**.
4. In the window that opens:
   * To add an existing tenant member, find the user and click  **Add** next to their name.
   * To invite a new user, type their full email address and click **Invite user**. The invitation is valid for three days, and you can track it on the **Users** tab. For more information, see [User invitations](https://docs.nebius.com/iam/authorization/add-users.md).

**CLI**

To add a user to a group via the Nebius AI Cloud CLI, you must have their email address.

1. Save a user email to an environment variable:

   ```bash theme={null}
   export USER_EMAIL=<user_email>
   ```

2. Get the user account ID and save it to an environment variable:

   ```bash theme={null}
   export USER_ID=$(nebius iam tenant-user-account-with-attributes list \
     --parent-id $TENANT_ID --all \
     --format json | jq -r --arg user_email "$USER_EMAIL" \
     '[.items[] | select(.attributes.email == $user_email)
     | .tenant_user_account.metadata.id] | first')
   ```

   With `--all`, the command returns the full list of user accounts instead of only the first page of results that may not contain the required user account.

3. To add the user account to the group, set up its membership:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id $GROUP_ID \
     --member-id $USER_ID
   ```

4. Check that the account has appeared in the group:

   ```bash theme={null}
   nebius iam group-membership list-members \
     --parent-id $GROUP_ID | grep "$USER_ID"
   ```

**Go SDK**

To add a user to a group, you must have their email address.

1. Get the user account ID:

   ```go theme={null}
   var userID string
   pageToken := ""
   for {
       userAccounts, err := sdk.Services().IAM().V1().
           TenantUserAccountWithAttributes().List(
               ctx,
               &iam.ListTenantUserAccountsWithAttributesRequest{
                   ParentId:  tenantID,
                   PageSize:  1000,
                   PageToken: pageToken,
               },
           )
       if err != nil {
           return err
       }
       for _, account := range userAccounts.GetItems() {
           if account.GetAttributes().GetEmail() == userEmail {
               userID = account.GetTenantUserAccount().
                   GetMetadata().GetId()
               break
           }
       }
       if userID != "" {
           break
       }
       pageToken = userAccounts.GetNextPageToken()
       if pageToken == "" {
           break
       }
   }
   if userID == "" {
       return fmt.Errorf("user not found: %s", userEmail)
   }
   fmt.Println(userID)
   ```

   The SDK has no parameter to fetch the full list of user accounts at once, so the code requests each subsequent page in a `for` loop by using the `PageToken` parameter until it finds an account whose `Attributes.Email` matches the required email address.

2. To add the user account to the group, set up its membership:

   ```go theme={null}
   membershipOp, err := sdk.Services().IAM().V1().
       GroupMembership().Create(
           ctx,
           &iam.CreateGroupMembershipRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<group_ID>",
               },
               Spec: &iam.GroupMembershipSpec{
                   MemberId: "<user_ID>",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = membershipOp.Wait(ctx); err != nil {
       return err
   }
   ```

   Set the group ID in `Metadata.ParentId` and the user account ID in `Spec.MemberId`.

3. Check that the account has appeared in the group:

   ```go theme={null}
   userMembershipLookupService := sdk.Services().IAM().V1().
       GroupMembership()
   userMemberships, err := userMembershipLookupService.ListMembers(
       ctx,
       &iam.ListGroupMembershipsRequest{ParentId: "<group_ID>"},
   )
   if err != nil {
       return err
   }
   found := false
   for _, membership := range userMemberships.GetMemberships() {
       if membership.GetSpec().GetMemberId() == "<user_ID>" {
           fmt.Println(membership)
           found = true
           break
       }
   }
   if !found {
       return fmt.Errorf(
           "user is not a group member: %s",
           "<user_ID>",
       )
   }
   ```

   The code lists the group's memberships and checks each membership's `Spec.MemberId` against the user account ID.

**Python SDK**

To add a user to a group, you must have their email address.

1. Get the user account ID:

   ```python theme={null}
   user_account_service = (
       TenantUserAccountWithAttributesServiceClient(sdk)
   )
   page_token = ""
   user_id = ""
   while True:
       user_accounts = await user_account_service.list(
           ListTenantUserAccountsWithAttributesRequest(
               parent_id=tenant_id,
               page_size=1000,
               page_token=page_token,
           ),
       )
       for item in user_accounts.items:
           if item.attributes.email == user_email:
               user_id = item.tenant_user_account.metadata.id
               break
       if user_id or not user_accounts.next_page_token:
           break
       page_token = user_accounts.next_page_token
   if not user_id:
       raise RuntimeError(f"user not found: {user_email}")
   print(user_id)
   ```

   The SDK has no parameter to fetch the full list of user accounts at once, so the code requests each subsequent page in a `while` loop by using the `page_token` parameter until it finds an account whose `attributes.email` matches the required email address.

2. To add the user account to the group, set up its membership:

   ```python theme={null}
   membership_service = GroupMembershipServiceClient(sdk)
   membership_operation = await membership_service.create(
       CreateGroupMembershipRequest(
           metadata=ResourceMetadata(parent_id="<group_ID>"),
           spec=GroupMembershipSpec(member_id="<user_ID>"),
       ),
   )
   await membership_operation.wait()
   ```

   Set the group ID in `metadata.parent_id` and the user account ID in `spec.member_id`.

3. Check that the account has appeared in the group:

   ```python theme={null}
   membership_service = GroupMembershipServiceClient(sdk)
   memberships = await membership_service.list_members(
       ListGroupMembershipsRequest(parent_id="<group_ID>"),
   )
   user_membership = next(
       (
           item for item in memberships.memberships
           if item.spec.member_id == "<user_ID>"
       ),
       None,
   )
   if user_membership is None:
       raise RuntimeError(
           "user is not a group member: " + "<user_ID>"
       )
   print(user_membership)
   ```

   The code lists the group's memberships and checks each membership's `spec.member_id` against the user account ID.

**JavaScript SDK**

To add a user to a group, you must have their email address.

1. Get the user account ID:

   ```ts theme={null}
   const userAccountService =
     new TenantUserAccountWithAttributesService(sdk);
   let userId = "";
   let pageToken = "";
   while (true) {
     const userAccounts = await userAccountService.list(
       ListTenantUserAccountsWithAttributesRequest.create({
         parentId: tenantId,
         pageSize: 1000,
         pageToken,
       }),
     ).result;
     userId = userAccounts.items.find(
       (item) =>
         item.attributesOptional?.$case === "attributes" &&
         item.attributesOptional.attributes.email === userEmail,
     )?.tenantUserAccount?.metadata?.id ?? "";
     if (userId || !userAccounts.nextPageToken) {
       break;
     }
     pageToken = userAccounts.nextPageToken;
   }
   if (!userId) {
     throw new Error(`user not found: ${userEmail}`);
   }
   console.log(userId);
   ```

   The SDK has no parameter to fetch the full list of user accounts at once, so the code requests each subsequent page in a `while` loop by using the `pageToken` parameter until it finds an account whose `attributes.email` matches the required email address.

2. To add the user account to the group, set up its membership:

   ```ts theme={null}
   const userMembershipService =
     new GroupMembershipService(sdk);
   const userMembershipOperation = await userMembershipService.create(
     CreateGroupMembershipRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<group_ID>",
       }),
       spec: GroupMembershipSpec.create({memberId: "<user_ID>"}),
     }),
   ).result;
   await userMembershipOperation.wait();
   ```

   Set the group ID in `metadata.parentId` and the user account ID in `spec.memberId`.

3. Check that the account has appeared in the group:

   ```ts theme={null}
   const userMembershipLookupService =
     new GroupMembershipService(sdk);
   const userMemberships = await userMembershipLookupService.listMembers(
     ListGroupMembershipsRequest.create({parentId: "<group_ID>"}),
   ).result;
   const userMembership = userMemberships.memberships.find(
     (item) => item.spec?.memberId === "<user_ID>",
   );
   if (!userMembership) {
     throw new Error(
       "user is not a group member: " + "<user_ID>",
     );
   }
   console.log(userMembership);
   ```

   The code lists the group's memberships and checks each membership's `spec.memberId` against the user account ID.

## Adding a service account

**Web console**

To add a service account to a group:

1. In the sidebar, go to  **Administration** → **IAM**.
2. On the **Groups** tab, click the group you want to add a service account to.
3. Click **Add members**.
4. In the window that opens, switch to the **Service accounts** tab.
5. Find the service account you want to add to the group and click  **Add** next to its name.

**CLI**

To add a service account to a group via the Nebius AI Cloud CLI, you must have its name.

1. Get the service account ID and save it to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account get-by-name \
     --name <service_account_name> \
     --format jsonpath='{.metadata.id}')
   ```

2. Set up the account membership in the group:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id $GROUP_ID \
     --member-id $SA_ID
   ```

3. Check that the account has appeared in the group:

   ```bash theme={null}
   nebius iam group-membership list-members \
     --parent-id $GROUP_ID | grep "$SA_ID"
   ```

If you don't know the name of the service account:

1. View all service accounts for your project:

   ```bash theme={null}
   nebius iam service-account list
   ```

2. Get the service account ID and save it to an environment variable. If the required service account does not appear as the first item in the previous command output, change the digit in `.items[0].metadata.id`:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account list \
     --format jsonpath='{.items[0].metadata.id}')
   ```

3. Set up the account membership in the group:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id $GROUP_ID \
     --member-id $SA_ID
   ```

4. Check that the new account has appeared in the group:

   ```bash theme={null}
   nebius iam group-membership list-members \
     --parent-id $GROUP_ID | grep "$SA_ID"
   ```

**Go SDK**

To add a service account to a group, you must have its name.

1. Get the service account ID:

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
   serviceAccountID := serviceAccount.GetMetadata().GetId()
   fmt.Println(serviceAccountID)
   ```

   Set the service account's name in `Name`.

2. Set up the account membership in the group:

   ```go theme={null}
   secondMembershipService := sdk.Services().IAM().V1().
       GroupMembership()
   secondMembershipOperation, err := secondMembershipService.Create(
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
   if _, err = secondMembershipOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set the group ID in `Metadata.ParentId` and the service account ID in `Spec.MemberId`.

3. Check that the account has appeared in the group:

   ```go theme={null}
   secondMembershipLookup := sdk.Services().IAM().V1().
       GroupMembership()
   secondMemberships, err := secondMembershipLookup.ListMembers(
       ctx,
       &iam.ListGroupMembershipsRequest{ParentId: "<group_ID>"},
   )
   if err != nil {
       return err
   }
   foundSecondServiceAccount := false
   for _, membership := range secondMemberships.GetMemberships() {
       if membership.GetSpec().GetMemberId() == "<service_account_ID>" {
           fmt.Println(membership)
           foundSecondServiceAccount = true
           break
       }
   }
   if !foundSecondServiceAccount {
       return fmt.Errorf(
           "second service account is not a group member: %s",
           "<service_account_ID>",
       )
   }
   ```

   The code lists the group's memberships and checks each membership's `Spec.MemberId` against the service account ID.

If you don't know the name of the service account:

1. List all service accounts:

   ```go theme={null}
   serviceAccountListService := sdk.Services().IAM().V1().
       ServiceAccount()
   allServiceAccounts, err := serviceAccountListService.List(
       ctx,
       &iam.ListServiceAccountRequest{},
   )
   if err != nil {
       return err
   }
   fmt.Println(allServiceAccounts)
   ```

2. Get the ID of the first service account in the list. If the required service account is not the first item, change the index in `GetItems()[0]`:

   ```go theme={null}
   listedServiceAccounts, err := sdk.Services().IAM().V1().
       ServiceAccount().List(
           ctx,
           &iam.ListServiceAccountRequest{},
       )
   if err != nil {
       return err
   }
   if len(listedServiceAccounts.GetItems()) == 0 {
       return fmt.Errorf("service account not found")
   }
   listedServiceAccountID := listedServiceAccounts.GetItems()[0].
       GetMetadata().GetId()
   if listedServiceAccountID == "" {
       return fmt.Errorf("service account ID is missing")
   }
   fmt.Println(listedServiceAccountID)
   ```

3. Set up the account membership in the group:

   ```go theme={null}
   serviceAccountMembershipService := sdk.Services().
       IAM().V1().GroupMembership()
   serviceAccountMembershipOperation, err :=
       serviceAccountMembershipService.Create(
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
   if _, err = serviceAccountMembershipOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set the group ID in `Metadata.ParentId` and the service account ID in `Spec.MemberId`.

4. Check that the new account has appeared in the group:

   ```go theme={null}
   serviceAccountMembershipLookup := sdk.Services().
       IAM().V1().GroupMembership()
   serviceAccountMemberships, err :=
       serviceAccountMembershipLookup.ListMembers(
           ctx,
           &iam.ListGroupMembershipsRequest{
               ParentId: "<group_ID>",
           },
       )
   if err != nil {
       return err
   }
   foundServiceAccount := false
   for _, membership := range serviceAccountMemberships.
       GetMemberships() {
       if membership.GetSpec().GetMemberId() == "<service_account_ID>" {
           fmt.Println(membership)
           foundServiceAccount = true
           break
       }
   }
   if !foundServiceAccount {
       return fmt.Errorf(
           "service account is not a group member: %s",
           "<service_account_ID>",
       )
   }
   ```

   The code lists the group's memberships and checks each membership's `Spec.MemberId` against the service account ID.

**Python SDK**

To add a service account to a group, you must have its name.

1. Get the service account ID:

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(name="<service_account_name>"),
   )
   service_account_id = service_account.metadata.id
   print(service_account_id)
   ```

   Set the service account's name in `name`.

2. Set up the account membership in the group:

   ```python theme={null}
   second_membership_service = (
       GroupMembershipServiceClient(sdk)
   )
   second_membership_operation = (
       await second_membership_service.create(
           CreateGroupMembershipRequest(
               metadata=ResourceMetadata(parent_id="<group_ID>"),
               spec=GroupMembershipSpec(
                   member_id="<service_account_ID>",
               ),
           ),
       )
   )
   await second_membership_operation.wait()
   ```

   Set the group ID in `metadata.parent_id` and the service account ID in `spec.member_id`.

3. Check that the account has appeared in the group:

   ```python theme={null}
   second_membership_lookup = GroupMembershipServiceClient(sdk)
   second_memberships = await second_membership_lookup.list_members(
       ListGroupMembershipsRequest(parent_id="<group_ID>"),
   )
   second_membership = next(
       (
           item for item in second_memberships.memberships
           if item.spec.member_id == "<service_account_ID>"
       ),
       None,
   )
   if second_membership is None:
       raise RuntimeError(
           "second service account is not a group member: " +
           "<service_account_ID>"
       )
   print(second_membership)
   ```

   The code lists the group's memberships and checks each membership's `spec.member_id` against the service account ID.

If you don't know the name of the service account:

1. List all service accounts:

   ```python theme={null}
   service_account_list_service = (
       ServiceAccountServiceClient(sdk)
   )
   service_accounts = await service_account_list_service.list(
       ListServiceAccountRequest(),
   )
   print(service_accounts)
   ```

2. Get the ID of the first service account in the list. If the required service account is not the first item, change the index in `items[0]`:

   ```python theme={null}
   service_account_list_service = (
       ServiceAccountServiceClient(sdk)
   )
   listed_service_accounts = (
       await service_account_list_service.list(
           ListServiceAccountRequest(),
       )
   )
   if not listed_service_accounts.items:
       raise RuntimeError("service account not found")
   service_account_id = listed_service_accounts.items[0].metadata.id
   print(service_account_id)
   ```

3. Set up the account membership in the group:

   ```python theme={null}
   service_account_membership_service = (
       GroupMembershipServiceClient(sdk)
   )
   service_account_membership_operation = (
       await service_account_membership_service.create(
           CreateGroupMembershipRequest(
               metadata=ResourceMetadata(parent_id="<group_ID>"),
               spec=GroupMembershipSpec(
                   member_id="<service_account_ID>",
               ),
           ),
       )
   )
   await service_account_membership_operation.wait()
   ```

   Set the group ID in `metadata.parent_id` and the service account ID in `spec.member_id`.

4. Check that the new account has appeared in the group:

   ```python theme={null}
   service_account_membership_lookup = (
       GroupMembershipServiceClient(sdk)
   )
   service_account_memberships = (
       await service_account_membership_lookup.list_members(
           ListGroupMembershipsRequest(parent_id="<group_ID>"),
       )
   )
   service_account_membership = next(
       (
           item for item in service_account_memberships.memberships
           if item.spec.member_id == "<service_account_ID>"
       ),
       None,
   )
   if service_account_membership is None:
       raise RuntimeError(
           "service account is not a group member: " +
           "<service_account_ID>"
       )
   print(service_account_membership)
   ```

   The code lists the group's memberships and checks each membership's `spec.member_id` against the service account ID.

**JavaScript SDK**

To add a service account to a group, you must have its name.

1. Get the service account ID:

   ```ts theme={null}
   const serviceAccountService =
     new ServiceAccountService(sdk);
   const serviceAccount = await serviceAccountService.getByName(
     GetServiceAccountByNameRequest.create({name: "<service_account_name>"}),
   );
   let serviceAccountId = serviceAccount.metadata?.id;
   if (!serviceAccountId) {
     throw new Error("service account ID is missing");
   }
   console.log(serviceAccountId);
   ```

   Set the service account's name in `name`.

2. Set up the account membership in the group:

   ```ts theme={null}
   const secondMembershipService =
     new GroupMembershipService(sdk);
   const secondMembershipOperation =
     await secondMembershipService.create(
       CreateGroupMembershipRequest.create({
         metadata: ResourceMetadata.create({
           parentId: "<group_ID>",
         }),
         spec: GroupMembershipSpec.create({
           memberId: "<service_account_ID>",
         }),
       }),
     ).result;
   await secondMembershipOperation.wait();
   ```

   Set the group ID in `metadata.parentId` and the service account ID in `spec.memberId`.

3. Check that the account has appeared in the group:

   ```ts theme={null}
   const secondMembershipLookup =
     new GroupMembershipService(sdk);
   const secondMemberships =
     await secondMembershipLookup.listMembers(
       ListGroupMembershipsRequest.create({
         parentId: "<group_ID>",
       }),
     ).result;
   const secondMembership = secondMemberships.memberships.find(
     (item) => item.spec?.memberId === "<service_account_ID>",
   );
   if (!secondMembership) {
     throw new Error(
       "second service account is not a group member: " +
       "<service_account_ID>",
     );
   }
   console.log(secondMembership);
   ```

   The code lists the group's memberships and checks each membership's `spec.memberId` against the service account ID.

If you don't know the name of the service account:

1. List all service accounts:

   ```ts theme={null}
   const serviceAccountListService =
     new ServiceAccountService(sdk);
   const allServiceAccounts = await serviceAccountListService.list(
     ListServiceAccountRequest.create({}),
   );
   console.log(allServiceAccounts);
   ```

2. Get the ID of the first service account in the list. If the required service account is not the first item, change the index in `items[0]`:

   ```ts theme={null}
   const getServiceAccountListService =
     new ServiceAccountService(sdk);
   const listedServiceAccounts =
     await getServiceAccountListService.list(
       ListServiceAccountRequest.create({}),
     );
   if (!listedServiceAccounts.items.length) {
     throw new Error("service account not found");
   }
   const listedServiceAccountId =
     listedServiceAccounts.items[0].metadata?.id;
   if (!listedServiceAccountId) {
     throw new Error("service account ID is missing");
   }
   console.log(listedServiceAccountId);
   ```

3. Set up the account membership in the group:

   ```ts theme={null}
   const serviceAccountMembershipService =
     new GroupMembershipService(sdk);
   const serviceAccountMembershipOperation =
     await serviceAccountMembershipService.create(
       CreateGroupMembershipRequest.create({
         metadata: ResourceMetadata.create({
           parentId: "<group_ID>",
         }),
         spec: GroupMembershipSpec.create({
           memberId: "<service_account_ID>",
         }),
       }),
     ).result;
   await serviceAccountMembershipOperation.wait();
   ```

   Set the group ID in `metadata.parentId` and the service account ID in `spec.memberId`.

4. Check that the new account has appeared in the group:

   ```ts theme={null}
   const serviceAccountMembershipLookup =
     new GroupMembershipService(sdk);
   const serviceAccountMemberships =
     await serviceAccountMembershipLookup.listMembers(
       ListGroupMembershipsRequest.create({
         parentId: "<group_ID>",
       }),
     ).result;
   const serviceAccountMembership =
     serviceAccountMemberships.memberships.find(
     (item) => item.spec?.memberId === "<service_account_ID>",
   );
   if (!serviceAccountMembership) {
     throw new Error(
       "service account is not a group member: " +
       "<service_account_ID>",
     );
   }
   console.log(serviceAccountMembership);
   ```

   The code lists the group's memberships and checks each membership's `spec.memberId` against the service account ID.
