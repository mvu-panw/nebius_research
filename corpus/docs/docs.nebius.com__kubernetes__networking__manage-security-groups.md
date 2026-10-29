# How to attach security groups to a node group in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/networking/manage-security-groups

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to attach security groups to a node group in Managed Service for Kubernetes®

Attach network security groups to Managed Kubernetes node groups to control traffic to and from your cluster's nodes.

## Prerequisites

Before attaching security groups to a node group, you need to create them. See [Managing security groups](https://docs.nebius.com/vpc/security-groups/manage.md) for instructions on creating groups and defining rules.

> [!WARNING]
>
> If you use your own security groups to restrict egress traffic, make sure that the cluster can still access the resources it needs. For example, blocking outbound internet access can break functionality that depends on it, such as pulling images from external registries.

Set up the interface that you are going to use:

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to attach security groups to a node group

**Web console**

To attach a security group to a node group:

1. In the [web console](https://console.nebius.com), go to  **Compute** → **Kubernetes**.
2. Open the page of the cluster with the node group where you want to attach a security group.
3. Switch to the **Node groups** tab and open the page of the required node group.
4. On the node group page, switch to the **Security groups** tab and click **Attach security groups**.
5. In the window that opens, select one or multiple security groups and click **Attach security groups**.

**CLI**

To attach security groups when creating a node group, use the `--template-network-interfaces` parameter:

```bash theme={null}
nebius mk8s node-group create \
  --parent-id <cluster_ID> \
  --name <node_group_name> \
  --fixed-node-count 1 \
  --template-resources-platform <platform> \
  --template-resources-preset <preset> \
  --template-network-interfaces "[{\"subnet_id\": \"<subnet_ID>\", \"security_groups\": [{\"id\": \"<security_group_ID_1>\"}, {\"id\": \"<security_group_ID_2>\"}]}]"
```

To get the security group ID, run `nebius vpc security-group list`.

**Go SDK**

Use `SecurityGroups` in `Spec.Template.NetworkInterfaces` to assign security groups when creating a node group:

```go theme={null}
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
                    FixedNodeCount: 1,
                },
                Template: &mk8s.NodeTemplate{
                    Resources: &mk8s.ResourcesSpec{
                        Platform: "<platform>",
                        Size: &mk8s.ResourcesSpec_Preset{
                            Preset: "<preset>",
                        },
                    },
                    NetworkInterfaces:
                        []*mk8s.NetworkInterfaceTemplate{
                        {
                            SubnetId: "<subnet_ID>",
                            SecurityGroups: []*mk8s.SecurityGroup{
                                {Id: "<security_group_ID_1>"},
                                {Id: "<security_group_ID_2>"},
                            },
                        },
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

**Python SDK**

Use `security_groups` in `spec.template.network_interfaces` to assign security groups when creating a node group:

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group_operation = await node_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id="<cluster_ID>",
            name="<node_group_name>",
        ),
        spec=NodeGroupSpec(
            fixed_node_count=1,
            template=NodeTemplate(
                resources=ResourcesSpec(
                    platform="<platform>",
                    preset="<preset>",
                ),
                network_interfaces=[
                    NetworkInterfaceTemplate(
                        subnet_id="<subnet_ID>",
                        security_groups=[
                            SecurityGroup(id="<security_group_ID_1>"),
                            SecurityGroup(id="<security_group_ID_2>"),
                        ],
                    ),
                ],
            ),
        ),
    ),
)
await node_group_operation.wait()
```

**JavaScript SDK**

Use `securityGroups` in `spec.template.networkInterfaces` to assign security groups when creating a node group:

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
        fixedNodeCount: 1,
      },
      template: NodeTemplate.create({
        resources: ResourcesSpec.create({
          platform: "<platform>",
          size: {
            $case: "preset",
            preset: "<preset>",
          },
        }),
        networkInterfaces: [
          NetworkInterfaceTemplate.create({
            subnetId: "<subnet_ID>",
            securityGroups: [
              SecurityGroup.create({ id: "<security_group_ID_1>" }),
              SecurityGroup.create({ id: "<security_group_ID_2>" }),
            ],
          }),
        ],
      }),
    }),
  }),
).result;
await nodeGroupOperation.wait();
```

## How to update security groups on an existing node group

**Web console**

To change or delete the attached security group from a node group:

1. In the [web console](https://console.nebius.com), go to  **Compute** → **Kubernetes**.
2. Open the page of the cluster with the node group where you want to change a security group.
3. Switch to the **Node groups** tab and open the page of the required node group.
4. On the node group page, switch to the **Security groups** tab.

   * To attach a different security group:

     1. Click **Attach security groups**.
     2. In the window that opens, select one or multiple security groups, and click **Attach security groups**.

   * To detach a security group:

     1. Click  next to the security group you want to detach and select **Detach**.
     2. In the window that opens, enter the name of the security group and click **Detach security group**.

**CLI**

Run the following command:

```bash theme={null}
nebius mk8s node-group update \
  --template-network-interfaces "[{\"subnet_id\": \"<subnet_ID>\", \"security_groups\": [{\"id\": \"<security_group_ID_1>\"}, {\"id\": \"<security_group_ID_2>\"}]}]" \
  <node_group_ID>
```

To get the security group ID, run `nebius vpc security-group list`.

**Go SDK**

```go theme={null}
nodeGroup, err := sdk.Services().MK8S().V1().
    NodeGroup().Get(
        ctx,
        &mk8s.GetNodeGroupRequest{
            Id: "<node_group_ID>",
        },
    )
if err != nil {
    return err
}
nodeGroupSpec := nodeGroup.GetSpec()
if nodeGroupSpec == nil || nodeGroupSpec.GetTemplate() == nil {
    return errors.New("node group template is missing")
}
nodeGroupSpec.GetTemplate().NetworkInterfaces =
    []*mk8s.NetworkInterfaceTemplate{
        {
            SubnetId: "<subnet_ID>",
            SecurityGroups: []*mk8s.SecurityGroup{
                {Id: "<security_group_ID_1>"},
                {Id: "<security_group_ID_2>"},
            },
        },
    }
nodeGroupOperation, err = sdk.Services().MK8S().V1().
    NodeGroup().Update(
        ctx,
        &mk8s.UpdateNodeGroupRequest{
            Metadata: nodeGroup.GetMetadata(),
            Spec:     nodeGroupSpec,
        },
    )
if err != nil {
    return err
}
if _, err = nodeGroupOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group = await node_group_service.get(
    GetNodeGroupRequest(id="<node_group_ID>"),
)
if node_group.spec is None or node_group.spec.template is None:
    raise ValueError("node group template is missing")
node_group.spec.template.network_interfaces = [
    NetworkInterfaceTemplate(
        subnet_id="<subnet_ID>",
        security_groups=[
            SecurityGroup(id="<security_group_ID_1>"),
            SecurityGroup(id="<security_group_ID_2>"),
        ],
    ),
]
node_group_operation = await node_group_service.update(
    UpdateNodeGroupRequest(
        metadata=node_group.metadata,
        spec=node_group.spec,
    ),
)
await node_group_operation.wait()
```

**JavaScript SDK**

```ts theme={null}
const nodeGroupUpdateService = new NodeGroupService(sdk);
const nodeGroup = await nodeGroupUpdateService.get(
  GetNodeGroupRequest.create({
    id: "<node_group_ID>",
  }),
);
if (!nodeGroup.spec?.template) {
  throw new Error("node group template is missing");
}
nodeGroup.spec.template.networkInterfaces = [
  NetworkInterfaceTemplate.create({
    subnetId: "<subnet_ID>",
    securityGroups: [
      SecurityGroup.create({ id: "<security_group_ID_1>" }),
      SecurityGroup.create({ id: "<security_group_ID_2>" }),
    ],
  }),
];
const nodeGroupUpdateOperation = await nodeGroupUpdateService.update(
  UpdateNodeGroupRequest.create({
    metadata: nodeGroup.metadata,
    spec: nodeGroup.spec,
  }),
).result;
await nodeGroupUpdateOperation.wait();
```

The update replaces the whole network interface list, so include every subnet and security group that the node group must keep.
