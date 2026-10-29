# How to enable or disable health checks in a Managed Service for Kubernetes® cluster

Source: https://docs.nebius.com/kubernetes/maintenance/enable-disable-health-checks

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to enable or disable health checks in a Managed Service for Kubernetes® cluster

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to enable health checks

[Health checks](https://docs.nebius.com/kubernetes/maintenance/health-checks.md) are enabled by default in Managed Service for Kubernetes clusters created on December 1, 2025, or later. If you created your cluster before this date and you want to enable the health checks, [contact technical support](https://console.nebius.com/support/create-ticket). Alternatively, [create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and [move your workloads](https://docs.nebius.com/kubernetes/node-groups/moving-workload.md) there.

## How to disable health checks

Disabling a health check means adding an auto-repair condition with the trigger turned off to the node group. The condition type and status depend on the issue type to which the health check is applied.

### How to stop processing I/O issues of a Network SSD NRD boot disk

If you want to prevent Managed Kubernetes from deleting a node when a Network SSD Non-replicated boot disk reports [input/output (I/O) issues](https://docs.nebius.com/kubernetes/maintenance/health-checks.md#i%2Fo-issues-of-a-network-ssd-nrd-boot-disk), disable a health check for the `NebiusBootDiskIOError` condition:

**CLI**

```bash theme={null}
nebius mk8s node-group update --id <node_group_ID> \
   --auto-repair-conditions '[{"type":"NebiusBootDiskIOError","status":"TRUE","disabled":true}]'
```

**Go SDK**

```go theme={null}
ioIssuesNodeGroup, err := sdk.Services().MK8S().V1().
    NodeGroup().Get(
        ctx,
        &mk8s.GetNodeGroupRequest{
            Id: "<node_group_ID>",
        },
    )
if err != nil {
    return err
}
ioIssuesSpec := ioIssuesNodeGroup.GetSpec()
if ioIssuesSpec == nil {
    return errors.New("node group spec is missing")
}
ioIssuesSpec.AutoRepair = &mk8s.NodeGroupAutoRepairSpec{
    Conditions: []*mk8s.NodeAutoRepairCondition{
        {
            Type:   "NebiusBootDiskIOError",
            Status: mk8s.ConditionStatus_TRUE,
            Trigger: &mk8s.NodeAutoRepairCondition_Disabled{
                Disabled: true,
            },
        },
    },
}
ioIssuesOperation, err := sdk.Services().MK8S().V1().
    NodeGroup().Update(
        ctx,
        &mk8s.UpdateNodeGroupRequest{
            Metadata: ioIssuesNodeGroup.GetMetadata(),
            Spec:     ioIssuesSpec,
        },
    )
if err != nil {
    return err
}
if _, err = ioIssuesOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group = await node_group_service.get(
    GetNodeGroupRequest(id="<node_group_ID>"),
)
if node_group.spec is None:
    raise ValueError("node group spec is missing")
node_group.spec.auto_repair = NodeGroupAutoRepairSpec(
    conditions=[
        NodeAutoRepairCondition(
            type="NebiusBootDiskIOError",
            status=ConditionStatus.TRUE,
            disabled=True,
        ),
    ],
)
operation = await node_group_service.update(
    UpdateNodeGroupRequest(
        metadata=node_group.metadata,
        spec=node_group.spec,
    ),
)
await operation.wait()
```

**JavaScript SDK**

```ts theme={null}
const ioIssuesService = new NodeGroupService(sdk);
const ioIssuesNodeGroup = await ioIssuesService.get(
  GetNodeGroupRequest.create({
    id: "<node_group_ID>",
  }),
);
if (!ioIssuesNodeGroup.spec) {
  throw new Error("node group spec is missing");
}
ioIssuesNodeGroup.spec.autoRepair = NodeGroupAutoRepairSpec.create({
  conditions: [
    NodeAutoRepairCondition.create({
      type: "NebiusBootDiskIOError",
      status: ConditionStatus.TRUE,
      trigger: {
        $case: "disabled",
        disabled: true,
      },
    }),
  ],
});
const ioIssuesOperation = await ioIssuesService.update(
  UpdateNodeGroupRequest.create({
    metadata: ioIssuesNodeGroup.metadata,
    spec: ioIssuesNodeGroup.spec,
  }),
).result;
await ioIssuesOperation.wait();
```

### False or unknown status of a node

If you want to prevent Managed Kubernetes from deleting a node when it reports a [false or unknown status](https://docs.nebius.com/kubernetes/maintenance/health-checks.md#false-or-unknown-status-of-a-node), disable a health check:

1. Disable the health check for the `Unknown` status of the node:

   **CLI**

   ```bash theme={null}
   nebius mk8s node-group update --id <node_group_ID> \
      --auto-repair-conditions '[{"type":"Ready","status":"UNKNOWN","disabled":true}]'
   ```

   **Go SDK**

   ```go theme={null}
   unknownStatusNodeGroup, err := sdk.Services().MK8S().V1().
       NodeGroup().Get(
           ctx,
           &mk8s.GetNodeGroupRequest{
               Id: "<node_group_ID>",
           },
       )
   if err != nil {
       return err
   }
   unknownStatusSpec := unknownStatusNodeGroup.GetSpec()
   if unknownStatusSpec == nil {
       return errors.New("node group spec is missing")
   }
   unknownStatusSpec.AutoRepair = &mk8s.NodeGroupAutoRepairSpec{
       Conditions: []*mk8s.NodeAutoRepairCondition{
           {
               Type:   "Ready",
               Status: mk8s.ConditionStatus_UNKNOWN,
               Trigger: &mk8s.NodeAutoRepairCondition_Disabled{
                   Disabled: true,
               },
           },
       },
   }
   unknownStatusOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Update(
           ctx,
           &mk8s.UpdateNodeGroupRequest{
               Metadata: unknownStatusNodeGroup.GetMetadata(),
               Spec:     unknownStatusSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = unknownStatusOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   **Python SDK**

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group = await node_group_service.get(
       GetNodeGroupRequest(id="<node_group_ID>"),
   )
   if node_group.spec is None:
       raise ValueError("node group spec is missing")
   node_group.spec.auto_repair = NodeGroupAutoRepairSpec(
       conditions=[
           NodeAutoRepairCondition(
               type="Ready",
               status=ConditionStatus.UNKNOWN,
               disabled=True,
           ),
       ],
   )
   operation = await node_group_service.update(
       UpdateNodeGroupRequest(
           metadata=node_group.metadata,
           spec=node_group.spec,
       ),
   )
   await operation.wait()
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const unknownStatusService = new NodeGroupService(sdk);
   const unknownStatusNodeGroup = await unknownStatusService.get(
     GetNodeGroupRequest.create({
       id: "<node_group_ID>",
     }),
   );
   if (!unknownStatusNodeGroup.spec) {
     throw new Error("node group spec is missing");
   }
   unknownStatusNodeGroup.spec.autoRepair =
     NodeGroupAutoRepairSpec.create({
       conditions: [
         NodeAutoRepairCondition.create({
           type: "Ready",
           status: ConditionStatus.UNKNOWN,
           trigger: {
             $case: "disabled",
             disabled: true,
           },
         }),
       ],
     });
   const unknownStatusOperation = await unknownStatusService.update(
     UpdateNodeGroupRequest.create({
       metadata: unknownStatusNodeGroup.metadata,
       spec: unknownStatusNodeGroup.spec,
     }),
   ).result;
   await unknownStatusOperation.wait();
   ```

2. Disable the health check for the `False` status of the node:

   **CLI**

   ```bash theme={null}
   nebius mk8s node-group update --id <node_group_ID> \
      --auto-repair-conditions '[{"type":"Ready","status":"FALSE","disabled":true}]'
   ```

   **Go SDK**

   ```go theme={null}
   falseStatusNodeGroup, err := sdk.Services().MK8S().V1().
       NodeGroup().Get(
           ctx,
           &mk8s.GetNodeGroupRequest{
               Id: "<node_group_ID>",
           },
       )
   if err != nil {
       return err
   }
   falseStatusSpec := falseStatusNodeGroup.GetSpec()
   if falseStatusSpec == nil {
       return errors.New("node group spec is missing")
   }
   falseStatusSpec.AutoRepair = &mk8s.NodeGroupAutoRepairSpec{
       Conditions: []*mk8s.NodeAutoRepairCondition{
           {
               Type:   "Ready",
               Status: mk8s.ConditionStatus_FALSE,
               Trigger: &mk8s.NodeAutoRepairCondition_Disabled{
                   Disabled: true,
               },
           },
       },
   }
   falseStatusOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Update(
           ctx,
           &mk8s.UpdateNodeGroupRequest{
               Metadata: falseStatusNodeGroup.GetMetadata(),
               Spec:     falseStatusSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = falseStatusOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   **Python SDK**

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group = await node_group_service.get(
       GetNodeGroupRequest(id="<node_group_ID>"),
   )
   if node_group.spec is None:
       raise ValueError("node group spec is missing")
   node_group.spec.auto_repair = NodeGroupAutoRepairSpec(
       conditions=[
           NodeAutoRepairCondition(
               type="Ready",
               status=ConditionStatus.FALSE,
               disabled=True,
           ),
       ],
   )
   operation = await node_group_service.update(
       UpdateNodeGroupRequest(
           metadata=node_group.metadata,
           spec=node_group.spec,
       ),
   )
   await operation.wait()
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const falseStatusService = new NodeGroupService(sdk);
   const falseStatusNodeGroup = await falseStatusService.get(
     GetNodeGroupRequest.create({
       id: "<node_group_ID>",
     }),
   );
   if (!falseStatusNodeGroup.spec) {
     throw new Error("node group spec is missing");
   }
   falseStatusNodeGroup.spec.autoRepair =
     NodeGroupAutoRepairSpec.create({
       conditions: [
         NodeAutoRepairCondition.create({
           type: "Ready",
           status: ConditionStatus.FALSE,
           trigger: {
             $case: "disabled",
             disabled: true,
           },
         }),
       ],
     });
   const falseStatusOperation = await falseStatusService.update(
     UpdateNodeGroupRequest.create({
       metadata: falseStatusNodeGroup.metadata,
       spec: falseStatusNodeGroup.spec,
     }),
   ).result;
   await falseStatusOperation.wait();
   ```

### How to stop processing issues with GPUs on a node

If you want to prevent Managed Kubernetes from cordoning, draining and stopping a node when the service detects [issues with GPUs](https://docs.nebius.com/kubernetes/maintenance/health-checks.md#issues-with-gpus-on-a-node) on it, disable a health check for the `NebiusGPUError` condition:

**CLI**

```bash theme={null}
nebius mk8s node-group update --id <node_group_ID> \
   --auto-repair-conditions '[{"type":"NebiusGPUError","status":"TRUE","disabled":true}]'
```

**Go SDK**

```go theme={null}
gpuIssuesNodeGroup, err := sdk.Services().MK8S().V1().
    NodeGroup().Get(
        ctx,
        &mk8s.GetNodeGroupRequest{
            Id: "<node_group_ID>",
        },
    )
if err != nil {
    return err
}
gpuIssuesSpec := gpuIssuesNodeGroup.GetSpec()
if gpuIssuesSpec == nil {
    return errors.New("node group spec is missing")
}
gpuIssuesSpec.AutoRepair = &mk8s.NodeGroupAutoRepairSpec{
    Conditions: []*mk8s.NodeAutoRepairCondition{
        {
            Type:   "NebiusGPUError",
            Status: mk8s.ConditionStatus_TRUE,
            Trigger: &mk8s.NodeAutoRepairCondition_Disabled{
                Disabled: true,
            },
        },
    },
}
gpuIssuesOperation, err := sdk.Services().MK8S().V1().
    NodeGroup().Update(
        ctx,
        &mk8s.UpdateNodeGroupRequest{
            Metadata: gpuIssuesNodeGroup.GetMetadata(),
            Spec:     gpuIssuesSpec,
        },
    )
if err != nil {
    return err
}
if _, err = gpuIssuesOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group = await node_group_service.get(
    GetNodeGroupRequest(id="<node_group_ID>"),
)
if node_group.spec is None:
    raise ValueError("node group spec is missing")
node_group.spec.auto_repair = NodeGroupAutoRepairSpec(
    conditions=[
        NodeAutoRepairCondition(
            type="NebiusGPUError",
            status=ConditionStatus.TRUE,
            disabled=True,
        ),
    ],
)
operation = await node_group_service.update(
    UpdateNodeGroupRequest(
        metadata=node_group.metadata,
        spec=node_group.spec,
    ),
)
await operation.wait()
```

**JavaScript SDK**

```ts theme={null}
const gpuIssuesService = new NodeGroupService(sdk);
const gpuIssuesNodeGroup = await gpuIssuesService.get(
  GetNodeGroupRequest.create({
    id: "<node_group_ID>",
  }),
);
if (!gpuIssuesNodeGroup.spec) {
  throw new Error("node group spec is missing");
}
gpuIssuesNodeGroup.spec.autoRepair = NodeGroupAutoRepairSpec.create({
  conditions: [
    NodeAutoRepairCondition.create({
      type: "NebiusGPUError",
      status: ConditionStatus.TRUE,
      trigger: {
        $case: "disabled",
        disabled: true,
      },
    }),
  ],
});
const gpuIssuesOperation = await gpuIssuesService.update(
  UpdateNodeGroupRequest.create({
    metadata: gpuIssuesNodeGroup.metadata,
    spec: gpuIssuesNodeGroup.spec,
  }),
).result;
await gpuIssuesOperation.wait();
```
