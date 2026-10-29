# Managing pricing policies in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/manage-pricing-policy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing pricing policies in Nebius AI Cloud

This article explains how to view, create, edit and delete pricing policies for preemptible virtual machines (VMs) in the web console, CLI, Go SDK, Python SDK or JavaScript SDK.

For information about spot pricing and how pricing policies affect preemptible resources, see [Spot pricing and pricing policies](https://docs.nebius.com/signup-billing/pricing-policy.md).

## Prerequisites

Pricing policies are project-level resources.

**Web console**

Make sure that you're in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has one of the following roles within the project, depending on what you need to do:

* To view pricing policies: at least the `viewer` role.
* To create, edit or delete pricing policies: at least the `editor` role.

For more information about roles, see [Roles](https://docs.nebius.com/iam/authorization/roles.md).

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure that you're in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has one of the following roles within the project, depending on what you need to do:

   * To view pricing policies: at least the `viewer` role.
   * To create, edit or delete pricing policies: at least the `editor` role.

   For more information about roles, see [Roles](https://docs.nebius.com/iam/authorization/roles.md).

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure that you're in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has one of the following roles within the project, depending on what you need to do:

   * To view pricing policies: at least the `viewer` role.
   * To create, edit or delete pricing policies: at least the `editor` role.

   For more information about roles, see [Roles](https://docs.nebius.com/iam/authorization/roles.md).

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure that you're in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has one of the following roles within the project, depending on what you need to do:

   * To view pricing policies: at least the `viewer` role.
   * To create, edit or delete pricing policies: at least the `editor` role.

   For more information about roles, see [Roles](https://docs.nebius.com/iam/authorization/roles.md).

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure that you're in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has one of the following roles within the project, depending on what you need to do:

   * To view pricing policies: at least the `viewer` role.
   * To create, edit or delete pricing policies: at least the `editor` role.

   For more information about roles, see [Roles](https://docs.nebius.com/iam/authorization/roles.md).

## How to view pricing policies

**Web console**

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Pricing**.
2. Switch to the **Pricing policy** tab and find the policy that you need.

   If the policy status is **Blocked**, its max price is lower than the current spot price. Resources that use this policy can't start until the spot price decreases or until you [increase](#how-to-edit-a-pricing-policy) the max price.

**CLI**

To list pricing policies in a project, run:

```bash theme={null}
nebius billing pricing-policy list \
  --parent-id <project_ID>
```

To get a pricing policy by ID, run:

```bash theme={null}
nebius billing pricing-policy get \
  --id <pricing_policy_ID>
```

In the output, check `status.scheduling_state`. If the value is `SCHEDULING_STATE_BLOCKED`, the policy's max price is lower than the current spot price.

**Go SDK**

1. List pricing policies in a project:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   policies, err := pricingPolicyService.List(
       ctx,
       &billing.ListPricingPoliciesRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("list pricing policies: %w", err)
   }
   fmt.Println(policies)
   ```

   In the code, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `Metadata.Id` value of the required policy in the list output.

2. Get a pricing policy by ID:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   policy, err := pricingPolicyService.Get(
       ctx,
       &billing.GetPricingPolicyRequest{
           Id: "<pricing_policy_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("get pricing policy: %w", err)
   }
   fmt.Println(policy)
   ```

   In the code, set `Id` to the pricing policy ID that you copied.

   In the output, check `Status.SchedulingState`. If the value is `billing.PricingPolicyStatus_SCHEDULING_STATE_BLOCKED`, the policy's max price is lower than the current spot price.

**Python SDK**

1. List pricing policies in a project:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policies = await pricing_policy_service.list(
       ListPricingPoliciesRequest(
           parent_id="<project_ID>",
       ),
   )
   print(pricing_policies)
   ```

   In the code, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `metadata.id` value of the required policy in the list output.

2. Get a pricing policy by ID:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policy = await pricing_policy_service.get(
       GetPricingPolicyRequest(
           id="<pricing_policy_ID>",
       ),
   )
   print(pricing_policy)
   ```

   In the code, set `id` to the pricing policy ID that you copied.

   In the output, check `status.scheduling_state`. If the value is `SCHEDULING_STATE_BLOCKED`, the policy's max price is lower than the current spot price.

**JavaScript SDK**

1. List pricing policies in a project:

   ```ts theme={null}
   const listService = new PricingPolicyService(sdk);
   const pricingPolicies = await listService.list(
     ListPricingPoliciesRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(pricingPolicies);
   ```

   In the code, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `metadata.id` value of the required policy in the list output.

2. Get a pricing policy by ID:

   ```ts theme={null}
   const getService = new PricingPolicyService(sdk);
   const fetchedPricingPolicy = await getService.get(
     GetPricingPolicyRequest.create({
       id: "<pricing_policy_ID>",
     }),
   ).result;
   console.log(fetchedPricingPolicy);
   ```

   In the code, set `id` to the pricing policy ID that you copied.

   In the output, check `status.schedulingState`. If the value is `SCHEDULING_STATE_BLOCKED`, the policy's max price is lower than the current spot price.

## How to create a pricing policy

You can create a pricing policy before creating preemptible resources, or create it while configuring a new resource in the web console.

**Web console**

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Pricing**.

2. Switch to the **Pricing policy** tab and click  **Create pricing policy**.

3. Enter a policy name. It can only contain Latin letters and numbers, with no special characters.

4. Select the project where the policy will be available.

5. Select the GPU platform for the policy.

6. In **Max price**, enter the highest spot price per GPU hour at which preemptible resources can run on this platform.

   The web console shows the allowed price range. To let resources start while the current spot price stays unchanged, enter a value that is higher than or equal to the current spot price.

7. Click **Create pricing policy**.

**CLI**

1. Get the current spot price for the GPU platform:

   ```bash theme={null}
   nebius billing v1alpha1 calculator estimate \
     --resource-spec-compute-instance-spec-parent-id <project_ID> \
     --resource-spec-compute-instance-spec-resources-platform <platform_ID> \
     --resource-spec-compute-instance-spec-resources-preset <preset> \
     --resource-spec-compute-instance-spec-preemptible-on-preemption STOP
   ```

   Specify the [project](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) where you create the pricing policy, as well as the [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

   In the output, `hourly_cost.general.total.cost` is the current hourly spot price of a preemptible VM with the specified preset in the project's region:

   ```yaml theme={null}
   hourly_cost:
     general:
       total:
         cost: "2.5"
         cost_rounded: "2.5"
   ```

   To get the spot price per GPU hour, divide this value by the number of GPUs in the preset. For example, divide by 8 for `8gpu-128vcpu-1600gb`.

2. Create the pricing policy:

   ```bash theme={null}
   nebius billing pricing-policy create \
     --parent-id <project_ID> \
     --name <pricing_policy_name> \
     --compute-instance-spec-v1-platform <platform_ID> \
     --pricing-max-price-v1-max-price <max_price>
   ```

   In this command:

   * `--parent-id`: ID of the project where the pricing policy will be available.
   * `--name`: Pricing policy name. It can only contain Latin letters and numbers, with no special characters.
   * `--compute-instance-spec-v1-platform`: GPU platform ID, for example `gpu-h100-sxm`.
   * `--pricing-max-price-v1-max-price`: Maximum spot price per GPU hour in your billing currency. The value must be higher than or equal to the minimum price. If the value is lower than the current spot price, the policy is created with blocked scheduling.

**Go SDK**

1. Get the current spot price for the GPU platform:

   ```go theme={null}
   computeInstanceSpec := &compute.CreateInstanceRequest{
       Metadata: &common.ResourceMetadata{
           ParentId: "<project_ID>",
       },
       Spec: &compute.InstanceSpec{
           Resources: &compute.ResourcesSpec{
               Platform: "<platform_ID>",
               Size: &compute.ResourcesSpec_Preset{
                   Preset: "<preset>",
               },
           },
           Preemptible: &compute.PreemptibleSpec{
               OnPreemption: compute.PreemptibleSpec_STOP,
           },
       },
   }
   calculatorService := sdk.Services().Billing().V1Alpha1().
       Calculator()
   estimate, err := calculatorService.Estimate(
       ctx,
       &billing.EstimateRequest{
           ResourceSpec: &billing.ResourceSpec{
               ResourceSpec: &billing.ResourceSpec_ComputeInstanceSpec{
                   ComputeInstanceSpec: computeInstanceSpec,
               },
           },
       },
   )
   if err != nil {
       return fmt.Errorf("estimate spot price: %w", err)
   }
   spotPrice := estimate.GetHourlyCost().GetGeneral().
       GetTotal().GetCost()
   fmt.Println(spotPrice)
   ```

   Specify the [project](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) where you create the pricing policy, as well as the [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

   The code prints the current hourly spot price of a preemptible VM with the specified preset in the project's region. To get the spot price per GPU hour, divide this value by the number of GPUs in the preset. For example, divide by 8 for `8gpu-128vcpu-1600gb`.

2. Create the pricing policy:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   pricingPolicyOperation, err := pricingPolicyService.Create(
       ctx,
       &billing.CreatePricingPolicyRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name: "<pricing_policy_name>",
           },
           Spec: &billing.PricingPolicySpec{
               ComputeInstanceSpec: &billing.ComputeInstanceSpec{
                   Versions: &billing.ComputeInstanceSpec_V1{
                       V1: &billing.ComputeInstanceSpecV1{
                           Platform: "<platform_ID>",
                       },
                   },
               },
               Pricing: &billing.PricingMethod{
                   Versions: &billing.PricingMethod_MaxPriceV1{
                       MaxPriceV1: &billing.MaxPriceV1{
                           MaxPrice: "<max_price>",
                       },
                   },
               },
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create pricing policy: %w", err)
   }
   pricingPolicyOperation, err = pricingPolicyOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for pricing policy creation: %w", err)
   }
   fmt.Println(pricingPolicyOperation.ResourceID())
   ```

   In the code:

   * `Metadata.ParentId`: ID of the project where the pricing policy will be available.
   * `Metadata.Name`: Pricing policy name. It can only contain Latin letters and numbers, with no special characters.
   * `Spec.ComputeInstanceSpec.Versions.V1.Platform`: GPU platform ID, for example `gpu-h100-sxm`.
   * `Spec.Pricing.Versions.MaxPriceV1.MaxPrice`: Maximum spot price per GPU hour in your billing currency. The value must be higher than or equal to the minimum price. If the value is lower than the current spot price, the policy is created with blocked scheduling.

**Python SDK**

1. Get the current spot price for the GPU platform:

   ```python theme={null}
   compute_instance_spec = CreateInstanceRequest(
       metadata=ResourceMetadata(
           parent_id="<project_ID>",
       ),
       spec=InstanceSpec(
           resources=ResourcesSpec(
               platform="<platform_ID>",
               preset="<preset>",
           ),
           preemptible=PreemptibleSpec(
               on_preemption=(
                   PreemptibleSpec.PreemptionPolicy.STOP
               ),
           ),
       ),
   )
   calculator_service = CalculatorServiceClient(sdk)
   estimate = await calculator_service.estimate(
       EstimateRequest(
           resource_spec=ResourceSpec(
               compute_instance_spec=compute_instance_spec,
           ),
       ),
   )
   print(estimate.hourly_cost.general.total.cost)
   ```

   Specify the [project](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) where you create the pricing policy, as well as the [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

   The code prints the current hourly spot price of a preemptible VM with the specified preset in the project's region. To get the spot price per GPU hour, divide this value by the number of GPUs in the preset. For example, divide by 8 for `8gpu-128vcpu-1600gb`.

2. Create the pricing policy:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policy_operation = await pricing_policy_service.create(
       CreatePricingPolicyRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="<pricing_policy_name>",
           ),
           spec=PricingPolicySpec(
               compute_instance_spec=ComputeInstanceSpec(
                   v1=ComputeInstanceSpecV1(
                       platform="<platform_ID>",
                   ),
               ),
               pricing=PricingMethod(
                   max_price_v1=MaxPriceV1(
                       max_price="<max_price>",
                   ),
               ),
           ),
       ),
   )
   await pricing_policy_operation.wait()
   print(pricing_policy_operation.resource_id)
   ```

   In the code:

   * `metadata.parent_id`: ID of the project where the pricing policy will be available.
   * `metadata.name`: Pricing policy name. It can only contain Latin letters and numbers, with no special characters.
   * `spec.compute_instance_spec.v1.platform`: GPU platform ID, for example `gpu-h100-sxm`.
   * `spec.pricing.max_price_v1.max_price`: Maximum spot price per GPU hour in your billing currency. The value must be higher than or equal to the minimum price. If the value is lower than the current spot price, the policy is created with blocked scheduling.

**JavaScript SDK**

1. Get the current spot price for the GPU platform:

   ```ts theme={null}
   const computeInstanceSpec = CreateInstanceRequest.create({
     metadata: ResourceMetadata.create({
       parentId: "<project_ID>",
     }),
     spec: InstanceSpec.create({
       resources: ResourcesSpec.create({
         platform: "<platform_ID>",
         size: {
           $case: "preset",
           preset: "<preset>",
         },
       }),
       preemptible: PreemptibleSpec.create({
         onPreemption: PreemptibleSpec_PreemptionPolicy.STOP,
       }),
     }),
   });
   const calculatorService = new CalculatorService(sdk);
   const estimate = await calculatorService.estimate(
     EstimateRequest.create({
       resourceSpec: ResourceSpec.create({
         resourceSpec: {
           $case: "computeInstanceSpec",
           computeInstanceSpec,
         },
       }),
     }),
   ).result;
   console.log(
     estimate.hourlyCost?.costType?.general?.total?.cost,
   );
   ```

   Specify the [project](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) where you create the pricing policy, as well as the [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

   The code prints the current hourly spot price of a preemptible VM with the specified preset in the project's region. To get the spot price per GPU hour, divide this value by the number of GPUs in the preset. For example, divide by 8 for `8gpu-128vcpu-1600gb`.

2. Create the pricing policy:

   ```ts theme={null}
   const createService = new PricingPolicyService(sdk);
   const createPricingPolicyOp = await createService.create(
     CreatePricingPolicyRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<project_ID>",
         name: "<pricing_policy_name>",
       }),
       spec: PricingPolicySpec.create({
         computeInstanceSpec: ComputeInstanceSpec.create({
           versions: {
             $case: "v1",
             v1: ComputeInstanceSpecV1.create({
               platform: "<platform_ID>",
             }),
           },
         }),
         pricing: PricingMethod.create({
           versions: {
             $case: "maxPriceV1",
             maxPriceV1: MaxPriceV1.create({
               maxPrice: "<max_price>",
             }),
           },
         }),
       }),
     }),
   ).result;
   await createPricingPolicyOp.wait();
   console.log(createPricingPolicyOp.resourceId());
   ```

   In the code:

   * `metadata.parentId`: ID of the project where the pricing policy will be available.
   * `metadata.name`: Pricing policy name. It can only contain Latin letters and numbers, with no special characters.
   * `spec.computeInstanceSpec.versions.v1.platform`: GPU platform ID, for example `gpu-h100-sxm`.
   * `spec.pricing.versions.maxPriceV1.maxPrice`: Maximum spot price per GPU hour in your billing currency. The value must be higher than or equal to the minimum price. If the value is lower than the current spot price, the policy is created with blocked scheduling.

After the policy is created, you can select it when creating preemptible resources on the same platform.

## How to edit a pricing policy

> [!NOTE]
>
> To update the max price in a pricing policy, first stop all running resources that use that policy.

**Web console**

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Pricing**.
2. Switch to the **Pricing policy** tab.
3. Find the policy you want to edit and click  → **Edit**.
4. Rename the policy or adjust the max price. The policy name can only contain Latin letters and numbers, with no special characters.
5. Click **Save changes**.

**CLI**

1. Get the pricing policy ID by name. To do this, use [nebius billing pricing-policy get-by-name](https://docs.nebius.com/cli/reference/billing/pricing-policy/get-by-name.md) with the pricing policy name and the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   In the output, copy the `metadata.id` value.

2. To rename the pricing policy, run:

   ```bash theme={null}
   nebius billing pricing-policy update <pricing_policy_ID> \
     --name <new_pricing_policy_name>
   ```

   In this command:

   * `<pricing_policy_ID>`: ID of the pricing policy that you copied.
   * `--name`: New pricing policy name. It can only contain Latin letters and numbers, with no special characters.

3. To update the max price, run:

   ```bash theme={null}
   nebius billing pricing-policy update <pricing_policy_ID> \
     --pricing-max-price-v1-max-price <max_price>
   ```

   The max price can only be updated when there are no running VMs associated with that policy.

**Go SDK**

1. Get the pricing policy ID. To do this, list pricing policies in a project and find the required policy by name:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   policies, err := pricingPolicyService.List(
       ctx,
       &billing.ListPricingPoliciesRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("list pricing policies: %w", err)
   }
   fmt.Println(policies)
   ```

   In the code, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `Metadata.Id` value of the required policy in the list output.

2. Rename the pricing policy:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   policy, err := pricingPolicyService.Get(
       ctx,
       &billing.GetPricingPolicyRequest{
           Id: "<pricing_policy_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("get pricing policy: %w", err)
   }
   pricingPolicyOperation, err := pricingPolicyService.Update(
       ctx,
       &billing.UpdatePricingPolicyRequest{
           Metadata: &common.ResourceMetadata{
               Id: policy.GetMetadata().GetId(),
               ParentId: policy.GetMetadata().GetParentId(),
               Name: "<new_pricing_policy_name>",
           },
           Spec: policy.GetSpec(),
       },
   )
   if err != nil {
       return fmt.Errorf("rename pricing policy: %w", err)
   }
   pricingPolicyOperation, err = pricingPolicyOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for pricing policy rename: %w", err)
   }
   fmt.Println(pricingPolicyOperation)
   ```

   In the code:

   * `GetPricingPolicyRequest.Id`: The pricing policy ID that you copied.
   * `Metadata.Name`: New pricing policy name. It can only contain Latin letters and numbers, with no special characters.

3. Update the max price:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   policy, err := pricingPolicyService.Get(
       ctx,
       &billing.GetPricingPolicyRequest{
           Id: "<pricing_policy_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("get pricing policy: %w", err)
   }
   pricingPolicySpec := policy.GetSpec()
   pricingPolicySpec.Pricing = &billing.PricingMethod{
       Versions: &billing.PricingMethod_MaxPriceV1{
           MaxPriceV1: &billing.MaxPriceV1{
               MaxPrice: "<max_price>",
           },
       },
   }
   pricingPolicyOperation, err := pricingPolicyService.Update(
       ctx,
       &billing.UpdatePricingPolicyRequest{
           Metadata: &common.ResourceMetadata{
               Id: policy.GetMetadata().GetId(),
               ParentId: policy.GetMetadata().GetParentId(),
               Name: policy.GetMetadata().GetName(),
           },
           Spec: pricingPolicySpec,
       },
   )
   if err != nil {
       return fmt.Errorf("update pricing policy max price: %w", err)
   }
   pricingPolicyOperation, err = pricingPolicyOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for pricing policy update: %w", err)
   }
   fmt.Println(pricingPolicyOperation)
   ```

   The max price can only be updated when there are no running VMs associated with that policy.

**Python SDK**

1. Get the pricing policy ID. To do this, list pricing policies in a project and find the required policy by name:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policies = await pricing_policy_service.list(
       ListPricingPoliciesRequest(
           parent_id="<project_ID>",
       ),
   )
   print(pricing_policies)
   ```

   In the code, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `metadata.id` value of the required policy in the list output.

2. Rename the pricing policy:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policy = await pricing_policy_service.get(
       GetPricingPolicyRequest(
           id="<pricing_policy_ID>",
       ),
   )
   pricing_policy_operation = await pricing_policy_service.update(
       UpdatePricingPolicyRequest(
           metadata=ResourceMetadata(
               id=pricing_policy.metadata.id,
               parent_id=pricing_policy.metadata.parent_id,
               name="<new_pricing_policy_name>",
           ),
           spec=pricing_policy.spec,
       ),
   )
   await pricing_policy_operation.wait()
   print(pricing_policy_operation)
   ```

   In the code:

   * `GetPricingPolicyRequest.id`: The pricing policy ID that you copied.
   * `metadata.name`: New pricing policy name. It can only contain Latin letters and numbers, with no special characters.

3. Update the max price:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policy = await pricing_policy_service.get(
       GetPricingPolicyRequest(
           id="<pricing_policy_ID>",
       ),
   )
   pricing_policy.spec.pricing = PricingMethod(
       max_price_v1=MaxPriceV1(
           max_price="<max_price>",
       ),
   )
   pricing_policy_operation = await pricing_policy_service.update(
       UpdatePricingPolicyRequest(
           metadata=ResourceMetadata(
               id=pricing_policy.metadata.id,
               parent_id=pricing_policy.metadata.parent_id,
               name=pricing_policy.metadata.name,
           ),
           spec=pricing_policy.spec,
       ),
   )
   await pricing_policy_operation.wait()
   print(pricing_policy_operation)
   ```

   The max price can only be updated when there are no running VMs associated with that policy.

**JavaScript SDK**

1. Get the pricing policy ID. To do this, list pricing policies in a project and find the required policy by name:

   ```ts theme={null}
   const listService = new PricingPolicyService(sdk);
   const pricingPolicies = await listService.list(
     ListPricingPoliciesRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(pricingPolicies);
   ```

   In the code, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `metadata.id` value of the required policy in the list output.

2. Rename the pricing policy:

   ```ts theme={null}
   const renameService = new PricingPolicyService(sdk);
   const pricingPolicyToRename = await renameService.get(
     GetPricingPolicyRequest.create({
       id: "<pricing_policy_ID>",
     }),
   ).result;
   const renamePricingPolicyOp = await renameService.update(
     UpdatePricingPolicyRequest.create({
       metadata: ResourceMetadata.create({
         id: pricingPolicyToRename.metadata.id,
         parentId: pricingPolicyToRename.metadata.parentId,
         name: "<new_pricing_policy_name>",
       }),
       spec: pricingPolicyToRename.spec,
     }),
   ).result;
   await renamePricingPolicyOp.wait();
   console.log(renamePricingPolicyOp);
   ```

   In the code:

   * `GetPricingPolicyRequest.id`: The pricing policy ID that you copied.
   * `metadata.name`: New pricing policy name. It can only contain Latin letters and numbers, with no special characters.

3. Update the max price:

   ```ts theme={null}
   const updateService = new PricingPolicyService(sdk);
   const pricingPolicyToUpdate = await updateService.get(
     GetPricingPolicyRequest.create({
       id: "<pricing_policy_ID>",
     }),
   ).result;
   pricingPolicyToUpdate.spec.pricing = PricingMethod.create({
     versions: {
       $case: "maxPriceV1",
       maxPriceV1: MaxPriceV1.create({
         maxPrice: "<max_price>",
       }),
     },
   });
   const updatePricingPolicyOp = await updateService.update(
     UpdatePricingPolicyRequest.create({
       metadata: ResourceMetadata.create({
         id: pricingPolicyToUpdate.metadata.id,
         parentId: pricingPolicyToUpdate.metadata.parentId,
         name: pricingPolicyToUpdate.metadata.name,
       }),
       spec: pricingPolicyToUpdate.spec,
     }),
   ).result;
   await updatePricingPolicyOp.wait();
   console.log(updatePricingPolicyOp);
   ```

   The max price can only be updated when there are no running VMs associated with that policy.

## How to delete a pricing policy

> [!WARNING]
>
> Deleting a pricing policy can stop resources that use it. Stopped VMs keep their attached volumes, and the volumes continue to be charged until you delete them. For more information about stopping charges for unused resources, see [How to stop being charged](https://docs.nebius.com/signup-billing/billing-models/payg.md#how-to-stop-being-charged).

**Web console**

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Pricing**.

2. Switch to the **Pricing policy** tab.

3. Check the number of running resources that use the policy.

4. Find the policy you want to delete and click  → **Delete**.

   If the web console shows affected resources, review them and continue only if they can be stopped.

5. Enter the policy name and click **Delete policy**.

**CLI**

1. Get the pricing policy ID by name. To do this, use [nebius billing pricing-policy get-by-name](https://docs.nebius.com/cli/reference/billing/pricing-policy/get-by-name.md) with the pricing policy name and the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   In the output, copy the `metadata.id` value.

2. Delete the pricing policy:

   ```bash theme={null}
   nebius billing pricing-policy delete \
     --id <pricing_policy_ID>
   ```

**Go SDK**

1. Get the pricing policy ID. To do this, list pricing policies in a project and find the required policy by name:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   policies, err := pricingPolicyService.List(
       ctx,
       &billing.ListPricingPoliciesRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("list pricing policies: %w", err)
   }
   fmt.Println(policies)
   ```

   In the code, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `Metadata.Id` value of the required policy in the list output.

2. Delete the pricing policy:

   ```go theme={null}
   pricingPolicyService := sdk.Services().Billing().V1().
       PricingPolicy()
   pricingPolicyOperation, err := pricingPolicyService.Delete(
       ctx,
       &billing.DeletePricingPolicyRequest{
           Id: "<pricing_policy_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("delete pricing policy: %w", err)
   }
   pricingPolicyOperation, err = pricingPolicyOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for pricing policy deletion: %w", err)
   }
   fmt.Println(pricingPolicyOperation)
   ```

   In the code, set `DeletePricingPolicyRequest.Id` to the pricing policy ID that you copied.

**Python SDK**

1. Get the pricing policy ID. To do this, list pricing policies in a project and find the required policy by name:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policies = await pricing_policy_service.list(
       ListPricingPoliciesRequest(
           parent_id="<project_ID>",
       ),
   )
   print(pricing_policies)
   ```

   In the code, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `metadata.id` value of the required policy in the list output.

2. Delete the pricing policy:

   ```python theme={null}
   pricing_policy_service = PricingPolicyServiceClient(sdk)
   pricing_policy_operation = await pricing_policy_service.delete(
       DeletePricingPolicyRequest(
           id="<pricing_policy_ID>",
       ),
   )
   await pricing_policy_operation.wait()
   print(pricing_policy_operation)
   ```

   In the code, set `DeletePricingPolicyRequest.id` to the pricing policy ID that you copied.

**JavaScript SDK**

1. Get the pricing policy ID. To do this, list pricing policies in a project and find the required policy by name:

   ```ts theme={null}
   const listService = new PricingPolicyService(sdk);
   const pricingPolicies = await listService.list(
     ListPricingPoliciesRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(pricingPolicies);
   ```

   In the code, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   Copy the `metadata.id` value of the required policy in the list output.

2. Delete the pricing policy:

   ```ts theme={null}
   const deleteService = new PricingPolicyService(sdk);
   const deletePricingPolicyOp = await deleteService.delete(
     DeletePricingPolicyRequest.create({
       id: "<pricing_policy_ID>",
     }),
   ).result;
   await deletePricingPolicyOp.wait();
   console.log(deletePricingPolicyOp);
   ```

   In the code, set `DeletePricingPolicyRequest.id` to the pricing policy ID that you copied.

If a stopped resource was configured to use the deleted policy, select another pricing policy before starting it.
