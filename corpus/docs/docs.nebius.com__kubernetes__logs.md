# Logs in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Logs in Managed Service for Kubernetes®

Managed Service for Kubernetes provides logs about clusters and node groups. Use these logs for troubleshooting and tracking actions on Managed Kubernetes resources. All logs are available on the  [Observability → Logs](https://console.nebius.com/observability/logs) page of the web console. Audit and control plane logs are also available on the **Logs** tab of a cluster page.

The service supports three types of logs:

* **Audit logs**: Contain metadata about operations that modify a cluster. For example, who and when created or deleted a Pod.

  Disabled by default; you can [enable them](#how-to-enable-audit-logs).

* **Control plane logs**: Show actions recorded by [control plane components](https://docs.nebius.com/kubernetes/components.md#control-plane-components) of a cluster. For example, you can learn about the cluster scaling, Pod scheduling or node availability.

  The control plane logs are collected from the following components:

  * API server ([kube-apiserver](https://kubernetes.io/docs/concepts/overview/kubernetes-api/))
  * Scheduler ([kube-scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/))
  * [Cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md)
  * Controller manager ([kube-controller-manager](https://kubernetes.io/docs/concepts/architecture/controller/))
  * Cloud controller manager

  In addition, Kubernetes generates node events. They provide information about Kubernetes resources, for example, state changes, node errors, Pod errors or scheduling failures.

  The control plane logs are enabled by default; you cannot disable them.

* **journald logs**: Show entries recorded by systemd services running on cluster nodes.

  Disabled by default; you can [enable them](#how-to-enable-journald-logs).

## Prerequisites

If you use the web console, you don't need to complete any prerequisites.

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to enable audit logs

Audit logs in Managed Kubernetes are disabled by default. To enable them for a cluster, specify the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters):

**CLI**

```bash theme={null}
nebius mk8s cluster update --id <cluster_ID> --control-plane-audit-logs
```

**Go SDK**

```go theme={null}
clusterForLogs, err := sdk.Services().MK8S().V1().
    Cluster().Get(
        ctx,
        &mk8s.GetClusterRequest{
            Id: "<cluster_ID>",
        },
    )
if err != nil {
    return err
}
clusterForLogsSpec := clusterForLogs.GetSpec()
if clusterForLogsSpec == nil ||
    clusterForLogsSpec.GetControlPlane() == nil {
    return fmt.Errorf("cluster control plane spec is missing")
}
clusterForLogsSpec.ControlPlane.AuditLogs = &mk8s.AuditLogsSpec{}
logsOperation, err := sdk.Services().MK8S().V1().
    Cluster().Update(
        ctx,
        &mk8s.UpdateClusterRequest{
            Metadata: clusterForLogs.GetMetadata(),
            Spec:     clusterForLogsSpec,
        },
    )
if err != nil {
    return err
}
if _, err = logsOperation.Wait(ctx); err != nil {
    return err
}
```

The code reads the current cluster spec, sets `Spec.ControlPlane.AuditLogs` and sends the spec back, so the other cluster parameters keep their current values.

**Python SDK**

```python theme={null}
logs_cluster_service = ClusterServiceClient(sdk)
cluster_for_logs = await logs_cluster_service.get(
    GetClusterRequest(id="<cluster_ID>"),
)
if cluster_for_logs.spec is None:
    raise ValueError("cluster spec is missing")
if cluster_for_logs.spec.control_plane is None:
    raise ValueError("cluster control plane spec is missing")
cluster_for_logs.spec.control_plane.audit_logs = AuditLogsSpec()
logs_operation = await logs_cluster_service.update(
    UpdateClusterRequest(
        metadata=cluster_for_logs.metadata,
        spec=cluster_for_logs.spec,
    ),
)
await logs_operation.wait()
```

The code reads the current cluster spec, sets `spec.control_plane.audit_logs` and sends the spec back, so the other cluster parameters keep their current values.

**JavaScript SDK**

```ts theme={null}
const logsClusterService = new ClusterService(sdk);
const clusterForLogs = await logsClusterService.get(
  GetClusterRequest.create({
    id: "<cluster_ID>",
  }),
);
if (!clusterForLogs.spec?.controlPlane) {
  throw new Error("cluster control plane spec is missing");
}
clusterForLogs.spec.controlPlane.auditLogs = AuditLogsSpec.create({});
const logsOperation = await logsClusterService.update(
  UpdateClusterRequest.create({
    metadata: clusterForLogs.metadata,
    spec: clusterForLogs.spec,
  }),
).result;
await logsOperation.wait();
```

The code reads the current cluster spec, sets `spec.controlPlane.auditLogs` and sends the spec back, so the other cluster parameters keep their current values.

## How to view audit and control plane logs

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.
2. Open the page of the required cluster and then go to the **Logs** tab.
3. In the **Bucket** field, select **Managed Kubernetes audit logs** or **Managed Kubernetes control planes**.
4. (Optional) To check logs for a specific control plane component, select it in the **Component** field.
5. Apply the required period.

## How to enable journald logs

The monitoring agent installed on cluster nodes can collect [journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) logs from systemd services and forward them to Observability Logs.

To configure journald log collection, set instance metadata labels when you create or update a node group. The settings apply to all nodes in the group.

> [!WARNING]
>
> Updating instance metadata labels recreates all nodes in the group. Enable journald logs when you [create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups) to avoid this update. For an existing group, configure its [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#deployment-strategy-and-quotas) to create replacement nodes before removing existing ones.

**CLI**

To enable journald log collection for a new node group, add the labels when you [create the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

```bash theme={null}
nebius mk8s node-group create \
  --parent-id <cluster_ID> \
  --name <node_group_name> \
  --fixed-node-count <number_of_nodes> \
  --template-resources-platform <platform_ID> \
  --template-resources-preset <preset_name> \
  --template-instance-metadata-labels "nebius.o11y.systemd-logs-collection.enabled=true,nebius.o11y.systemd-logs-collection.units=kubelet.service;containerd.service"
```

The `--template-instance-metadata-labels` parameter accepts the following labels, separated by commas:

* `nebius.o11y.systemd-logs-collection.enabled=true`: Enables journald log collection.
* `nebius.o11y.systemd-logs-collection.units=<systemd_units>`: Specifies the systemd units to collect logs from. Separate multiple units with semicolons, for example, `sshd.service;containerd.service`. If you omit this label, logs from all units are collected.

To enable journald log collection for an existing node group, update its instance metadata labels. The `--template-instance-metadata-labels` parameter replaces all existing instance metadata labels, so include the labels you want to keep as `<existing_labels>` in the command:

```bash theme={null}
nebius mk8s node-group update \
  --id <node_group_ID> \
  --template-instance-metadata-labels "<existing_labels>,nebius.o11y.systemd-logs-collection.enabled=true"
```

**Go SDK**

To enable journald log collection for a new node group, add the labels when you [create the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

```go theme={null}
instanceLabels := map[string]string{
    "nebius.o11y.systemd-logs-collection.enabled": "true",
    "nebius.o11y.systemd-logs-collection.units":
        "kubelet.service;containerd.service",
}
nodeGroupOperation, err := sdk.Services().MK8S().V1().
    NodeGroup().Create(
        ctx,
        &mk8s.CreateNodeGroupRequest{
            Metadata: &common.ResourceMetadata{
                ParentId: "<cluster_ID>",
                Name:     "<node_group_name>",
            },
            Spec: &mk8s.NodeGroupSpec{
                Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                    FixedNodeCount: <number_of_nodes>,
                },
                Template: &mk8s.NodeTemplate{
                    Resources: &mk8s.ResourcesSpec{
                        Platform: "<platform_ID>",
                        Size: &mk8s.ResourcesSpec_Preset{
                            Preset: "<preset_name>",
                        },
                    },
                    InstanceMetadata:
                        &mk8s.InstanceMetadataTemplate{
                        Labels: instanceLabels,
                    },
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = nodeGroupOperation.Wait(ctx); err != nil {
    return err
}
```

The `Spec.Template.InstanceMetadata.Labels` map accepts the following labels:

* `nebius.o11y.systemd-logs-collection.enabled`: Enables journald log collection. Set it to `"true"`.
* `nebius.o11y.systemd-logs-collection.units`: Specifies the systemd units to collect logs from. Separate multiple units with semicolons, for example, `"sshd.service;containerd.service"`. If you omit this label, logs from all units are collected.

To enable journald log collection for an existing node group, update its instance metadata labels:

```go theme={null}
nodeGroupService := sdk.Services().MK8S().V1().NodeGroup()
nodeGroup, err := nodeGroupService.Get(
    ctx,
    &mk8s.GetNodeGroupRequest{
        Id: "<node_group_ID>",
    },
)
if err != nil {
    return err
}
nodeTemplate := nodeGroup.GetSpec().GetTemplate()
if nodeTemplate == nil {
    return errors.New("node group template is missing")
}
instanceMetadata := nodeTemplate.GetInstanceMetadata()
if instanceMetadata == nil {
    instanceMetadata = &mk8s.InstanceMetadataTemplate{}
    nodeTemplate.InstanceMetadata = instanceMetadata
}
if instanceMetadata.Labels == nil {
    instanceMetadata.Labels = map[string]string{}
}
journaldLabel := "nebius.o11y.systemd-logs-collection.enabled"
instanceMetadata.Labels[journaldLabel] = "true"
updateOperation, err := nodeGroupService.Update(
    ctx,
    &mk8s.UpdateNodeGroupRequest{
        Metadata: nodeGroup.GetMetadata(),
        Spec:     nodeGroup.GetSpec(),
    },
)
if err != nil {
    return err
}
if _, err = updateOperation.Wait(ctx); err != nil {
    return err
}
```

The code reads the current node group specification, adds the journald label to `Spec.Template.InstanceMetadata.Labels` and sends the specification back, so the other instance metadata labels and node group parameters keep their current values.

**Python SDK**

To enable journald log collection for a new node group, add the labels when you [create the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group_operation = await node_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id="<cluster_ID>",
            name="<node_group_name>",
        ),
        spec=NodeGroupSpec(
            fixed_node_count=<number_of_nodes>,
            template=NodeTemplate(
                resources=ResourcesSpec(
                    platform="<platform_ID>",
                    preset="<preset_name>",
                ),
                instance_metadata=InstanceMetadataTemplate(
                    labels={
                        "nebius.o11y.systemd-logs-collection.enabled":
                            "true",
                        "nebius.o11y.systemd-logs-collection.units":
                            "kubelet.service;containerd.service",
                    },
                ),
            ),
        ),
    ),
)
await node_group_operation.wait()
```

The `spec.template.instance_metadata.labels` dictionary accepts the following labels:

* `nebius.o11y.systemd-logs-collection.enabled`: Enables journald log collection. Set it to `"true"`.
* `nebius.o11y.systemd-logs-collection.units`: Specifies the systemd units to collect logs from. Separate multiple units with semicolons, for example, `"sshd.service;containerd.service"`. If you omit this label, logs from all units are collected.

To enable journald log collection for an existing node group, update its instance metadata labels:

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group = await node_group_service.get(
    GetNodeGroupRequest(id="<node_group_ID>"),
)
labels = node_group.spec.template.instance_metadata.labels
labels["nebius.o11y.systemd-logs-collection.enabled"] = "true"
update_operation = await node_group_service.update(
    UpdateNodeGroupRequest(
        metadata=node_group.metadata,
        spec=node_group.spec,
    ),
)
await update_operation.wait()
```

The code reads the current node group specification, adds the journald label to `spec.template.instance_metadata.labels` and sends the specification back, so the other instance metadata labels and node group parameters keep their current values.

**JavaScript SDK**

To enable journald log collection for a new node group, add the labels when you [create the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

```ts theme={null}
const nodeGroupService = new NodeGroupService(sdk);
const nodeGroupOperation = await nodeGroupService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: "<cluster_ID>",
      name: "<node_group_name>",
    }),
    spec: NodeGroupSpec.create({
      size: {
        $case: "fixedNodeCount",
        fixedNodeCount: <number_of_nodes>,
      },
      template: NodeTemplate.create({
        resources: ResourcesSpec.create({
          platform: "<platform_ID>",
          size: {
            $case: "preset",
            preset: "<preset_name>",
          },
        }),
        instanceMetadata: InstanceMetadataTemplate.create({
          labels: {
            "nebius.o11y.systemd-logs-collection.enabled":
              "true",
            "nebius.o11y.systemd-logs-collection.units":
              "kubelet.service;containerd.service",
          },
        }),
      }),
    }),
  }),
).result;
await nodeGroupOperation.wait();
```

The `spec.template.instanceMetadata.labels` object accepts the following labels:

* `nebius.o11y.systemd-logs-collection.enabled`: Enables journald log collection. Set it to `"true"`.
* `nebius.o11y.systemd-logs-collection.units`: Specifies the systemd units to collect logs from. Separate multiple units with semicolons, for example, `"sshd.service;containerd.service"`. If you omit this label, logs from all units are collected.

To enable journald log collection for an existing node group, update its instance metadata labels:

```ts theme={null}
const updateNodeGroupService = new NodeGroupService(sdk);
const nodeGroup = await updateNodeGroupService.get(
  GetNodeGroupRequest.create({
    id: "<node_group_ID>",
  }),
);
if (!nodeGroup.spec?.template) {
  throw new Error("node group template is missing");
}
const nodeTemplate = nodeGroup.spec.template;
nodeTemplate.instanceMetadata = InstanceMetadataTemplate.create({
  ...nodeTemplate.instanceMetadata,
  labels: {
    ...nodeTemplate.instanceMetadata?.labels,
    "nebius.o11y.systemd-logs-collection.enabled": "true",
  },
});
const updateOperation = await updateNodeGroupService.update(
  UpdateNodeGroupRequest.create({
    metadata: nodeGroup.metadata,
    spec: nodeGroup.spec,
  }),
).result;
await updateOperation.wait();
```

The code reads the current node group specification, adds the journald label to `spec.template.instanceMetadata.labels` and sends the specification back, so the other instance metadata labels and node group parameters keep their current values.

## How to view journald logs

**Web console**

1. In the web console, go to  [Observability → Logs](https://console.nebius.com/observability/logs).
2. In the **Bucket** field, select **User logs**.
3. To show only the logs of your cluster, enter the following query:

   ```
   {__bucket__="default", mk8s_cluster_id="<cluster_ID>"}
   ```

   The `__bucket__` label is required. For more information about the query syntax, see [LogQL implementation by Nebius AI Cloud](https://docs.nebius.com/observability/logs/query-language.md).

**CLI**

Get the journald logs of your cluster for the last hour:

```bash theme={null}
nebius logging query '{mk8s_cluster_id="<cluster_ID>"}' \
  --bucket default \
  --since 1h
```

The command contains the following parameters:

* `--bucket`: The log bucket. The `default` bucket stores user logs, including journald logs.
* `--since` (optional): The period to get logs for, counting back from the current time. The default value is `1h`.

For more information about querying logs, see [How to query logs with Nebius AI Cloud CLI](https://docs.nebius.com/observability/logs/nebius-cli.md).

## See also

* [Logs in Nebius AI Cloud](https://docs.nebius.com/observability/logging.md)
