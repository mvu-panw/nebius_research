# Capacity reservations for Managed Service for Kubernetes® node groups

Source: https://docs.nebius.com/kubernetes/node-groups/reservations

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Capacity reservations for Managed Service for Kubernetes® node groups

To make sure that GPU capacity is always available for your nodes (virtual machines, VMs), you can reserve GPUs. A *reservation* represents a [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md), and it reserves a specific number of GPUs that are allocated to your infrastructure. GPUs from a reservation remain available, even if a VM is stopped. Without reservations, GPU capacity is taken from a shared pool and returned when a VM is stopped (for example, by you or a [maintenance event](https://docs.nebius.com/kubernetes/maintenance/index.md)).

To start using reservations, send a request to your Nebius manager. In this request, specify how many GPUs you would like to reserve and for what period. If you are not in contact with a Nebius manager, you can ask [technical support](https://console.nebius.com/support/create-ticket) to connect you with one.

After reservations are ready, you can add them to your existing node groups or create new ones with reservations. You can also check your capacity block groups on the **Limits** page and get detailed information about them. For more information, see [List of capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md#list-of-capacity-block-groups).

> [!NOTE]
>
> GPUs allocated from reservations do not count towards [quotas on the number of GPUs](https://docs.nebius.com/compute/resources/quotas-limits.md#gpu-virtual-machines).

## How to add reservations to node groups

Node groups of a regular type with GPUs support reservations. [Preemptible node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md#preemptible-node-groups) and node groups without GPUs do not support reservations.

**Web console**

If you want to [create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#regular-node-groups), in the creation form, under **Computing resources**, select **With GPU** and a regular VM type. After that, specify the **Reservation usage** settings.

If you want to modify an existing node group, go to its **Settings** tab on the node group page. Next, update the **Reservation usage** settings.

The **Reservation usage** settings are only displayed if you have capacity block groups.

Available **Reservation usage** options:

* **With reservations**: Resources are allocated from reservations.

  In the **Reservation** section, you can configure the following options:

  * **Any (existing and future)** (default): Compute selects among your matching capacity block groups automatically.
  * **Specific capacity block groups**: Select one or more capacity block groups. Each option shows the capacity block group ID, reservation period and GPU usage. Make sure the selected groups have enough capacity and do not expire soon.
  * **Switch to PAYG**: Choose whether the VM can start after you create or restart it without active intervals in selected capacity block groups:

    * **When reservation is exhausted** (default): The VM can start as a pay-as-you-go VM when no capacity is available in the selected capacity block groups.
    * **Never**: The VM cannot start without available capacity in the selected capacity block groups.

    This does not affect the VM when it is running. If an interval in a selected capacity block group expires while the VM is running, the VM always continues as a pay-as-you-go VM, regardless of this setting.

  If you have capacity block groups in multiple regions, select a **Region** first.

* **Without reservations**: Resources are allocated from the common pool, and no reservations are used for the node group.

**CLI**

To configure reservations, use the `--template-reservation-policy-*` parameters when creating or updating a node group:

* Create a node group:

  ```bash theme={null}
  nebius mk8s node-group create \
    ... \
    --template-reservation-policy-policy <auto|forbid|strict> \
    --template-reservation-policy-reservation-ids <reservations>
  ```

* Update a node group:

  ```bash theme={null}
  nebius mk8s node-group update \
    --auto-approve \
    ... \
    --template-reservation-policy-policy <auto|forbid|strict> \
    --template-reservation-policy-reservation-ids <reservations>
  ```

Description of the parameters:

* `--template-reservation-policy-policy`: Policy for reservation usage. Supports the following values:

  * `auto`: Node group resources are allocated from reservations. If no reservations are currently available, the node group runs without them. In this case, resources for the node group are provided from the common pool.

    > [!NOTE]
    >
    > The `auto` value is default. If you don't have any reservations and you don't set the `--template-reservation-policy-policy` parameter, the `auto` value applies and the node group runs without reservations.

  * `forbid`: Node group resources are provided from the common pool, and no reservations are used.

  * `strict`: Node group resources are exclusively allocated from reservations. The node group doesn't run without the reservations.

* `--template-reservation-policy-reservation-ids` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation-ids` | **Behavior** |
| - | - | - |
| `auto` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, resources for all nodes in the node group are provided from the common pool, not from a reservation.If a reservation doesn't have enough capacity for the whole node group, it uses all the resources available in this reservation and also takes resources from the common pool. In other words, resources for some nodes are provided from the reservation, and resources for the rest of the nodes are provided from the common pool. |
| `auto` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), the same logic of the `auto` policy applies. |
| `forbid` | Not specified | Node group resources are provided from the common pool. No reservations are used. |
| `forbid` | Specified | Not supported. Applying this combination results in a validation error. |
| `strict` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, a request for creating or updating a node group fails. |
| `strict` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit, a request for creating or updating a node group fails. |

**Terraform**

To configure reservations in the node group, use the `reservation_policy` parameter of the node template:

```hcl theme={null}
resource "nebius_mk8s_v1_node_group" "my_node_group" {
  ...
  template = {
    ...
    reservation_policy = {
      policy          = "<AUTO|FORBID|STRICT>"
      reservation_ids = "<reservations>"
    }
  }
  ...
}
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the following values:

  * `AUTO`: Node group resources are allocated from reservations. If no reservations are currently available, the node group runs without them. In this case, resources for the node group are provided from the common pool.

    > [!NOTE]
    >
    > The `AUTO` value is default. If you don't have any reservations and you don't set the `policy` parameter, the `AUTO` value applies and the node group runs without reservations.

  * `FORBID`: Node group resources are provided from the common pool, and no reservations are used.

  * `STRICT`: Node group resources are exclusively allocated from reservations. The node group doesn't run without the reservations.

* `reservation_ids`: IDs of specific reservations (capacity block groups). You can use this parameter with the `AUTO` and `STRICT` reservation usages:

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation_ids` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, resources for all nodes in the node group are provided from the common pool, not from a reservation.If a reservation doesn't have enough capacity for the whole node group, it uses all the resources available in this reservation and also takes resources from the common pool. In other words, resources for some nodes are provided from the reservation, and resources for the rest of the nodes are provided from the common pool. |
| `AUTO` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), the same logic of the `AUTO` policy applies. |
| `FORBID` | Not specified | Node group resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. Applying this combination results in a validation error. |
| `STRICT` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, a request for creating or updating a node group fails. |
| `STRICT` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit, a request for creating or updating a node group fails. |

**Go SDK**

Use `ReservationPolicy` in `NodeTemplate` when creating or updating a node group:

* Create a node group:

  ```go theme={null}
  createReservationPolicy := &mk8s.ReservationPolicy{
      Policy: mk8s.ReservationPolicy_STRICT,
      ReservationIds: []string{
          "<reservation_ID>",
      },
  }
  createGroupOp, err := sdk.Services().MK8S().V1().
      NodeGroup().Create(
          ctx,
          &mk8s.CreateNodeGroupRequest{
              Metadata: &common.ResourceMetadata{
                  ParentId: "<cluster_ID>",
                  Name:     "<node_group_name>",
              },
              Spec: &mk8s.NodeGroupSpec{
                  Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                      FixedNodeCount: 2,
                  },
                  Template: &mk8s.NodeTemplate{
                      Resources: &mk8s.ResourcesSpec{
                          Platform: "<platform_ID>",
                          Size: &mk8s.ResourcesSpec_Preset{
                              Preset: "<preset_name>",
                          },
                      },
                      ReservationPolicy: createReservationPolicy,
                  },
              },
          },
      )
  if err != nil {
      return fmt.Errorf("create node group: %w", err)
  }
  if _, err = createGroupOp.Wait(ctx); err != nil {
      return fmt.Errorf("wait for node group creation: %w", err)
  }
  ```

* Update a node group:

  ```go theme={null}
  updateReservationPolicy := &mk8s.ReservationPolicy{
      Policy: mk8s.ReservationPolicy_STRICT,
      ReservationIds: []string{
          "<reservation_ID>",
      },
  }
  groupForPolicy, err := sdk.Services().MK8S().V1().
      NodeGroup().Get(
          ctx,
          &mk8s.GetNodeGroupRequest{Id: "<node_group_ID>"},
      )
  if err != nil {
      return fmt.Errorf("get node group: %w", err)
  }
  spec := groupForPolicy.GetSpec()
  if spec == nil {
      return fmt.Errorf("node group spec is missing")
  }
  template := spec.GetTemplate()
  if template == nil {
      return fmt.Errorf("node group template is missing")
  }
  template.ReservationPolicy = updateReservationPolicy
  updatePolicyOp, err := sdk.Services().MK8S().V1().NodeGroup().
      Update(
          ctx,
          &mk8s.UpdateNodeGroupRequest{
              Metadata: groupForPolicy.GetMetadata(),
              Spec:     groupForPolicy.GetSpec(),
          },
      )
  if err != nil {
      return fmt.Errorf(
          "update node group reservation policy: %w", err,
      )
  }
  if _, err = updatePolicyOp.Wait(ctx); err != nil {
      return fmt.Errorf("wait for node group update: %w", err)
  }
  ```

Description of the parameters:

* `Policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `ReservationIds` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `Policy` | `ReservationIds` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, resources for all nodes in the node group are provided from the common pool, not from a reservation.If a reservation doesn't have enough capacity for the whole node group, it uses all the resources available in this reservation and also takes resources from the common pool. In other words, resources for some nodes are provided from the reservation, and resources for the rest of the nodes are provided from the common pool. |
| `AUTO` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), the same logic of the `AUTO` policy applies. |
| `FORBID` | Not specified | Node group resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. Applying this combination results in a validation error. |
| `STRICT` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, a request for creating or updating a node group fails. |
| `STRICT` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit, a request for creating or updating a node group fails. |

**Python SDK**

Use `reservation_policy` in `NodeTemplate` when creating or updating a node group:

* Create a node group:

  ```python theme={null}
  create_reservation_policy = ReservationPolicy(
      policy=ReservationPolicy.Policy.STRICT,
      reservation_ids=["<reservation_ID>"],
  )
  create_group_service = NodeGroupServiceClient(sdk)
  create_group_operation = await create_group_service.create(
      CreateNodeGroupRequest(
          metadata=ResourceMetadata(
              parent_id="<cluster_ID>",
              name="<node_group_name>",
          ),
          spec=NodeGroupSpec(
              fixed_node_count=2,
              template=NodeTemplate(
                  resources=ResourcesSpec(
                      platform="<platform_ID>",
                      preset="<preset_name>",
                  ),
                  reservation_policy=create_reservation_policy,
              ),
          ),
      ),
  )
  await create_group_operation.wait()
  ```

* Update a node group:

  ```python theme={null}
  update_reservation_policy = ReservationPolicy(
      policy=ReservationPolicy.Policy.STRICT,
      reservation_ids=["<reservation_ID>"],
  )
  policy_group_service = NodeGroupServiceClient(sdk)
  group_for_policy = await policy_group_service.get(
      GetNodeGroupRequest(id="<node_group_ID>"),
  )
  group_for_policy.spec.template.reservation_policy = (
      update_reservation_policy
  )
  policy_operation = await policy_group_service.update(
      UpdateNodeGroupRequest(
          metadata=group_for_policy.metadata,
          spec=group_for_policy.spec,
      ),
  )
  await policy_operation.wait()
  ```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `reservation_ids` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation_ids` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, resources for all nodes in the node group are provided from the common pool, not from a reservation.If a reservation doesn't have enough capacity for the whole node group, it uses all the resources available in this reservation and also takes resources from the common pool. In other words, resources for some nodes are provided from the reservation, and resources for the rest of the nodes are provided from the common pool. |
| `AUTO` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), the same logic of the `AUTO` policy applies. |
| `FORBID` | Not specified | Node group resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. Applying this combination results in a validation error. |
| `STRICT` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, a request for creating or updating a node group fails. |
| `STRICT` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit, a request for creating or updating a node group fails. |

**JavaScript SDK**

Use `reservationPolicy` in `NodeTemplate` when creating or updating a node group:

* Create a node group:

  ```ts theme={null}
  const createReservationPolicy = ReservationPolicy.create({
    policy: ReservationPolicy_Policy.STRICT,
    reservationIds: ["<reservation_ID>"],
  });
  const createGroupService = new NodeGroupService(sdk);
  const createGroupOperation = await createGroupService.create(
    CreateNodeGroupRequest.create({
      metadata: ResourceMetadata.create({
        parentId: "<cluster_ID>",
        name: "<node_group_name>",
      }),
      spec: NodeGroupSpec.create({
        size: {
          $case: "fixedNodeCount",
          fixedNodeCount: 2,
        },
        template: NodeTemplate.create({
          resources: ResourcesSpec.create({
            platform: "<platform_ID>",
            size: {
              $case: "preset",
              preset: "<preset_name>",
            },
          }),
          reservationPolicy: createReservationPolicy,
        }),
      }),
    }),
  ).result;
  await createGroupOperation.wait();
  ```

* Update a node group:

  ```ts theme={null}
  const updateReservationPolicy = ReservationPolicy.create({
    policy: ReservationPolicy_Policy.STRICT,
    reservationIds: ["<reservation_ID>"],
  });
  const policyGroupService = new NodeGroupService(sdk);
  const groupForPolicy = await policyGroupService.get(
    GetNodeGroupRequest.create({
      id: "<node_group_ID>",
    }),
  );
  if (!groupForPolicy.spec?.template) {
    throw new Error("node group template is missing");
  }
  groupForPolicy.spec.template.reservationPolicy =
    updateReservationPolicy;
  const policyOperation = await policyGroupService.update(
    UpdateNodeGroupRequest.create({
      metadata: groupForPolicy.metadata,
      spec: groupForPolicy.spec,
    }),
  ).result;
  await policyOperation.wait();
  ```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `reservationIds` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservationIds` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, resources for all nodes in the node group are provided from the common pool, not from a reservation.If a reservation doesn't have enough capacity for the whole node group, it uses all the resources available in this reservation and also takes resources from the common pool. In other words, resources for some nodes are provided from the reservation, and resources for the rest of the nodes are provided from the common pool. |
| `AUTO` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), the same logic of the `AUTO` policy applies. |
| `FORBID` | Not specified | Node group resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. Applying this combination results in a validation error. |
| `STRICT` | Not specified | Managed Kubernetes tries to launch a node group in any available and suitable reservation. If none is found, a request for creating or updating a node group fails. |
| `STRICT` | Specified | Managed Kubernetes tries to launch a node group in one of the specified reservations. If none of them fit, a request for creating or updating a node group fails. |

## What's next

To find information about reservations, check the pages of your VMs (nodes). The VM page and the list of VMs show what reservation policy you have configured and what reservations currently apply. For more information, see [How to find information about reservations for an already configured VM](https://docs.nebius.com/compute/virtual-machines/reservations.md#how-to-find-information-about-reservations-for-an-already-configured-vm).

For details about how billing works when you use reservations, see [Billing for reservations](https://docs.nebius.com/compute/virtual-machines/reservations.md#billing-for-reservations).

## See also

* [Capacity block groups in Nebius AI Cloud](https://docs.nebius.com/overview/limits/capacity-block-groups.md)
* [Capacity reservations for Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/reservations.md)
