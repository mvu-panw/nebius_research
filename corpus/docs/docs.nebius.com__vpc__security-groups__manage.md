# Managing security groups and security rules

Source: https://docs.nebius.com/vpc/security-groups/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing security groups and security rules

To set up a firewall for your [Compute](https://docs.nebius.com/compute/index.md) virtual machines (VMs), you can create [security groups](https://docs.nebius.com/vpc/security-groups/overview.md) with security rules that control ingress and egress traffic at the packet level, and then add the VMs' network interfaces to the security groups.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. [Get the ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) where you want to manage security groups and security rules.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Install [jq](https://jqlang.github.io/jq/) to modify the VM specification returned by the Nebius AI Cloud CLI when you [add a VM to a security group](#adding-vms-to-security-groups):

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. [Get the ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) where you want to manage security groups and security rules.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Get the ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) where you want to manage security groups and security rules.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Get the ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) where you want to manage security groups and security rules.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Get the ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) where you want to manage security groups and security rules.

## Creating security groups

**Web console**

To create a security group:

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Open the network where you want to create a security group.
3. Click **Create** and select **Security group**.
4. In the window that opens, enter the security group name and click **Create security group**.

**CLI**

To create a security group, run `nebius vpc security-group create`:

```bash theme={null}
nebius vpc security-group create \
  --name <name> \
  --network-id <network_ID>
```

The command contains the following parameters:

* `--name`: Name of the security group.
* `--network-id`: ID of the network for the security group. You can only add VMs within this network to a security group. For instructions, see [How to get a network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

For more details, see the [command reference](https://docs.nebius.com/cli/reference/vpc/security-group/create.md).

**Go SDK**

Run the following code:

```go theme={null}
securityGroupService := sdk.Services().VPC().V1().
    SecurityGroup()
securityGroupOperation, err := securityGroupService.Create(
    ctx,
    &vpc.CreateSecurityGroupRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<name>",
            ParentId: "<project_ID>",
        },
        Spec: &vpc.SecurityGroupSpec{
            NetworkId: "<network_ID>",
        },
    },
)
if err != nil {
    return err
}
if _, err = securityGroupOperation.Wait(ctx); err != nil {
    return err
}
securityGroupID := securityGroupOperation.ResourceID()
fmt.Println(securityGroupOperation)
```

In the code, set the following parameters:

* `Metadata.Name`: Name of the security group.
* `Metadata.ParentId`: ID of the project.
* `Spec.NetworkId`: ID of the network for the security group. You can only add VMs within this network to a security group.

The code saves the security group ID to `securityGroupID`.

**Python SDK**

Run the following code:

```python theme={null}
security_group_service = SecurityGroupServiceClient(sdk)
security_group_operation = await security_group_service.create(
    CreateSecurityGroupRequest(
        metadata=ResourceMetadata(
            name="<name>",
            parent_id="<project_ID>",
        ),
        spec=SecurityGroupSpec(
            network_id="<network_ID>",
        ),
    ),
)
await security_group_operation.wait()
security_group_id = security_group_operation.resource_id
print(security_group_operation)
```

In the code, set the following parameters:

* `name`: Name of the security group.
* `parent_id`: ID of the project.
* `network_id`: ID of the network for the security group. You can only add VMs within this network to a security group.

The code saves the security group ID to `security_group_id`.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const securityGroupService = new SecurityGroupService(sdk);
const securityGroupOperation = await securityGroupService.create(
  CreateSecurityGroupRequest.create({
    metadata: {
      name: "<name>",
      parentId: "<project_ID>",
    },
    spec: {
      networkId: "<network_ID>",
    },
  }),
).result;
await securityGroupOperation.wait();
const securityGroupId = securityGroupOperation.resourceId();
console.log(securityGroupOperation);
```

In the code, set the following parameters:

* `name`: Name of the security group.
* `parentId`: ID of the project.
* `networkId`: ID of the network for the security group. You can only add VMs within this network to a security group.

The code saves the security group ID to `securityGroupId`.

Security groups are created empty. After creating a security group, [create security rules in it](#adding-security-rules-to-security-groups) and then [add VMs to it](#adding-vms-to-security-groups).

## Adding security rules to security groups

**Web console**

To add a rule to an existing security group:

1. In the sidebar, go to  **Networking** → **Virtual Networks**.

2. Switch to the **Security groups** tab.

3. Open the security group that you want to add a rule to and click  **Create security rule**.

4. In the window that opens, enter the rule name and specify the following parameters:

   * **Direction**: **Ingress** or **Egress**.

   * **Action**: **Allow** or **Deny**.

   * **Source/Destination security group**: Security group as the source (if **Direction** is set to **Ingress**) or as the destination (if **Direction** is set to **Egress**).

   * **Source/Destination CIDR blocks**: List of up to eight CIDR blocks that define the range of IP addresses for the source (if **Direction** is set to **Ingress**) or the destination traffic (if **Direction** is set to **Egress**).

     If you specify both the security group and CIDR blocks, the security rule applies to the VMs' network interfaces that are added to the specified security group *and* are assigned an IP address from one of the specified CIDR blocks. For more information, see [Security groups as sources or destinations in security rules](https://docs.nebius.com/vpc/security-groups/overview.md#security-groups-as-sources-or-destinations-in-security-rules).

     Traffic to and from `169.254.0.0/16` (`169.254.0.0`–`169.254.255.255`) isn't evaluated by security groups. These IP addresses are reserved for internal Nebius use.

   * **Destination ports**: List of up to eight ports to which the rule applies.

   * **Protocol**: `TCP`, `UDP`, `ICMP` or `Any`.

     > [!NOTE]
     >
     > Only `TCP` and `UDP` support port filtering. Selecting `Any` or `ICMP` hides the **Ports** section.

5. (Optional) Under **Advanced settings**, specify:

   * **Type**: **Stateful** or **Stateless**. If a rule that allows traffic is stateful, it also allows the response traffic within the same connection. For more information, see [Security rule types: stateful and stateless](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-types-stateful-and-stateless).
   * **Priority**: From 1 to 1000. Rules with lower priority are applied first; if priorities are equal, the deny rule wins. For more information, see [Security rule priorities](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-priorities).

6. Click **Create rule**.

**CLI**

To add a security rule to a security group, run `nebius vpc security-rule create`. For example, to create an egress security rule, run the following command:

```bash theme={null}
nebius vpc security-rule create \
  --parent-id <security_group_ID> \
  --name <name> \
  --access <allow|deny> \
  --egress-destination-cidrs "<CIDR_block_1>,<CIDR_block_2>,..." \
  --egress-destination-ports "<CIDR_port_1>,<CIDR_port_2>,..." \
  --egress-destination-security-group-id <destination_security_group_ID> \
  --protocol <tcp|udp|icmp|any> \
  --type <stateful|stateless> \
  --priority <priority_from_1_to_1000>
```

To get a security group ID, run `nebius vpc security-group list`. The output contains the ID in the `.metadata.id` parameter.

Traffic to and from `169.254.0.0/16` (`169.254.0.0`–`169.254.255.255`) isn't evaluated by security groups. These IP addresses are reserved for internal Nebius use.

For more details, see:

* [Command reference](https://docs.nebius.com/cli/reference/vpc/security-rule/create.md)
* `--egress-destination-security-group-id` (and `--ingress-source-security-group-id`): [Security groups as sources or destinations in security rules](https://docs.nebius.com/vpc/security-groups/overview.md#security-groups-as-sources-or-destinations-in-security-rules)
* `--type`: [Security rule types: stateful and stateless](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-types-stateful-and-stateless)
* `--priority`: [Security rule priorities](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-priorities)

**Go SDK**

For example, to create an egress security rule, run the following code:

```go theme={null}
ruleCIDRs := strings.Split("<CIDR_block_1>,<CIDR_block_2>,...", ",")
var rulePorts []int32
for _, port := range strings.Split("<CIDR_port_1>,<CIDR_port_2>,...", ",") {
    value, err := strconv.ParseInt(port, 10, 32)
    if err != nil {
        return err
    }
    rulePorts = append(rulePorts, int32(value))
}
securityRuleService := sdk.Services().VPC().V1().
    SecurityRule()
securityRuleOperation, err := securityRuleService.Create(
    ctx,
    &vpc.CreateSecurityRuleRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<name>",
            ParentId: "<security_group_ID>",
        },
        Spec: &vpc.SecurityRuleSpec{
            Access: vpc.RuleAccessAction_ALLOW,
            Protocol: vpc.RuleProtocol_TCP,
            Type: vpc.RuleType_STATEFUL,
            Priority: <priority_from_1_to_1000>,
            Match: &vpc.SecurityRuleSpec_Egress{
                Egress: &vpc.RuleEgress{
                    DestinationCidrs: ruleCIDRs,
                    DestinationPorts: rulePorts,
                    DestinationSecurityGroupId: "<destination_security_group_ID>",
                },
            },
        },
    },
)
if err != nil {
    return err
}
if _, err = securityRuleOperation.Wait(ctx); err != nil {
    return err
}
securityRuleID := securityRuleOperation.ResourceID()
fmt.Println(securityRuleOperation)
```

In the code, set the following parameters:

* `Metadata.Name`: Name of the security rule.
* `Metadata.ParentId`: ID of the security group.
* `Spec.Access`: Whether the rule allows or denies traffic. The example uses `vpc.RuleAccessAction_ALLOW`.
* `Spec.Protocol`: Protocol of the traffic. The example uses `vpc.RuleProtocol_TCP`.
* `Spec.Type`: [Security rule type](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-types-stateful-and-stateless). The example uses `vpc.RuleType_STATEFUL`.
* `Spec.Priority`: [Security rule priority](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-priorities), from `1` to `1000`.
* `DestinationCidrs` and `DestinationPorts` under `Spec.Match`: Destination CIDR blocks and ports. The code builds them from the comma-separated lists in `ruleCIDRs` and `rulePorts`.
* `DestinationSecurityGroupId` under `Spec.Match`: ID of the [destination security group](https://docs.nebius.com/vpc/security-groups/overview.md#security-groups-as-sources-or-destinations-in-security-rules).

The code saves the security rule ID to `securityRuleID`.

**Python SDK**

For example, to create an egress security rule, run the following code:

```python theme={null}
rule_cidrs = "<CIDR_block_1>,<CIDR_block_2>,...".split(",")
rule_ports = [
    int(port) for port in "<CIDR_port_1>,<CIDR_port_2>,...".split(",")
]
security_rule_service = SecurityRuleServiceClient(sdk)
security_rule_operation = await security_rule_service.create(
    CreateSecurityRuleRequest(
        metadata=ResourceMetadata(
            name="<name>",
            parent_id="<security_group_ID>",
        ),
        spec=SecurityRuleSpec(
            access=RuleAccessAction.ALLOW,
            protocol=RuleProtocol.TCP,
            type=RuleType.STATEFUL,
            priority=<priority_from_1_to_1000>,
            egress=RuleEgress(
                destination_cidrs=rule_cidrs,
                destination_ports=rule_ports,
                destination_security_group_id="<destination_security_group_ID>",
            ),
        ),
    ),
)
await security_rule_operation.wait()
security_rule_id = security_rule_operation.resource_id
print(security_rule_operation)
```

In the code, set the following parameters:

* `name`: Name of the security rule.
* `parent_id`: ID of the security group.
* `access`: Whether the rule allows or denies traffic. The example uses `RuleAccessAction.ALLOW`.
* `protocol`: Protocol of the traffic. The example uses `RuleProtocol.TCP`.
* `type`: [Security rule type](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-types-stateful-and-stateless). The example uses `RuleType.STATEFUL`.
* `priority`: [Security rule priority](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-priorities), from `1` to `1000`.
* `egress.destination_cidrs` and `egress.destination_ports`: Destination CIDR blocks and ports. The code builds them from the comma-separated lists in `rule_cidrs` and `rule_ports`.
* `egress.destination_security_group_id`: ID of the [destination security group](https://docs.nebius.com/vpc/security-groups/overview.md#security-groups-as-sources-or-destinations-in-security-rules).

The code saves the security rule ID to `security_rule_id`.

**JavaScript SDK**

For example, to create an egress security rule, run the following code:

```ts theme={null}
const ruleCidrs = "<CIDR_block_1>,<CIDR_block_2>,...".split(",");
const rulePorts = "<CIDR_port_1>,<CIDR_port_2>,...".split(",").map(Number);
const securityRuleService = new SecurityRuleService(sdk);
const securityRuleOperation = await securityRuleService.create(
  CreateSecurityRuleRequest.create({
    metadata: {
      name: "<name>",
      parentId: "<security_group_ID>",
    },
    spec: {
      access: RuleAccessAction.ALLOW,
      protocol: RuleProtocol.TCP,
      type: RuleType.STATEFUL,
      priority: <priority_from_1_to_1000>,
      match: {
        "$case": "egress",
        "egress": {
          destinationCidrs: ruleCidrs,
          destinationPorts: rulePorts,
          destinationSecurityGroupId: "<destination_security_group_ID>",
        },
      },
    },
  }),
).result;
await securityRuleOperation.wait();
const securityRuleId = securityRuleOperation.resourceId();
console.log(securityRuleOperation);
```

In the code, set the following parameters:

* `name`: Name of the security rule.
* `parentId`: ID of the security group.
* `access`: Whether the rule allows or denies traffic. The example uses `RuleAccessAction.ALLOW`.
* `protocol`: Protocol of the traffic. The example uses `RuleProtocol.TCP`.
* `type`: [Security rule type](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-types-stateful-and-stateless). The example uses `RuleType.STATEFUL`.
* `priority`: [Security rule priority](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-priorities), from `1` to `1000`.
* `destinationCidrs` and `destinationPorts` under `match`: Destination CIDR blocks and ports. The code builds them from the comma-separated lists in `ruleCidrs` and `rulePorts`.
* `destinationSecurityGroupId` under `match`: ID of the [destination security group](https://docs.nebius.com/vpc/security-groups/overview.md#security-groups-as-sources-or-destinations-in-security-rules).

The code saves the security rule ID to `securityRuleId`.

> [!NOTE]
>
> You can't change a security rule once it's created. To change a rule in a custom security group, [delete](#deleting-security-rules) it and create a new one. Security rules in default security groups can't be deleted.

## Deleting security rules

**Web console**

To delete a security rule from a security group:

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Switch to the **Security groups** tab.
3. Open the security group that you want to delete rules from.
4. Do one of the following:

   * To delete a single rule, click  next to the rule and select **Delete**.
   * To delete multiple rules at once, check the boxes next to the required rules and click **Delete** in the banner that appears.

**CLI**

To delete a security rule from a security group, run the `nebius vpc security-rule delete` command:

```bash theme={null}
nebius vpc security-rule delete <security_rule_ID>
```

To get the security rule ID, run `nebius vpc security-rule list --parent-id <security_group_ID>`.

For more details, see the [command reference](https://docs.nebius.com/cli/reference/vpc/security-rule/delete.md).

**Go SDK**

Run the following code:

```go theme={null}
deletedRuleService := sdk.Services().VPC().V1().
    SecurityRule()
deletedRuleOperation, err := deletedRuleService.Delete(
    ctx,
    &vpc.DeleteSecurityRuleRequest{
        Id: "<security_rule_ID>",
    },
)
if err != nil {
    return err
}
if _, err = deletedRuleOperation.Wait(ctx); err != nil {
    return err
}
```

Set `Id` to the ID of the security rule that you want to delete.

**Python SDK**

Run the following code:

```python theme={null}
deleted_rule_service = SecurityRuleServiceClient(sdk)
deleted_rule_operation = await deleted_rule_service.delete(
    DeleteSecurityRuleRequest(
        id="<security_rule_ID>",
    ),
)
await deleted_rule_operation.wait()
```

Set `id` to the ID of the security rule that you want to delete.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const deletedRuleService = new SecurityRuleService(sdk);
const deletedRuleOperation = await deletedRuleService.delete(
  DeleteSecurityRuleRequest.create({
    id: "<security_rule_ID>",
  }),
).result;
await deletedRuleOperation.wait();
```

Set `id` to the ID of the security rule that you want to delete.

If you delete all security rules from a security group, it denies all traffic to and from the VMs' network interfaces that are added to it. For more details, see [Security rule priorities](https://docs.nebius.com/vpc/security-groups/overview.md#security-rule-priorities).

## Adding VMs to security groups

A VM and the security groups that it's added to must be associated with the same network.

To add a VM's network interface to a security group, add the security group ID to the specification of the network interface when creating or modifying the VM. For example, to add an existing VM to a security group, perform the following steps:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. Open the VM that you want to add to a security group.

3. Click **Actions** → **Add to security groups**.

4. In the window that opens:

   * If you have only one network interface configured, select one or multiple security groups from the list.

   * If you have multiple network interfaces configured:

     1. Select the network interface that the security groups you want to add the VM to are associated with.
     2. Select one or multiple security groups from the list.

5. Click **Add VM to groups**.

**CLI**

Run the following command:

```bash theme={null}
nebius compute instance get --id <VM_ID> --format json | \
  jq --arg nic "<network_interface_name>" --arg sg "<security_group_ID>" \
    '.spec.network_interfaces |= map(if .name == $nic then .security_groups += [{id: $sg}] else . end) |
    {metadata: .metadata, spec: .spec}' | \
  nebius compute instance update -
```

In the command, specify the following values:

* `<VM_ID>`: ID of the VM.
* `<network_interface_name>`: Name of the VM's network interface, for example, `eth0`.
* `<security_group_ID>`: ID of the security group. To get it, run `nebius vpc security-group list`.

The command gets the VM specification, adds the security group to `security_groups` of the network interface, keeping the security groups that the interface already has, and then updates the VM with the full specification. The other network interfaces of the VM don't change.

For more details, see the reference for commands that create and modify VMs:

* [nebius compute instance create](https://docs.nebius.com/cli/reference/compute/instance/create.md)
* [nebius compute instance update](https://docs.nebius.com/cli/reference/compute/instance/update.md)
* [nebius compute instance edit](https://docs.nebius.com/cli/reference/compute/instance/edit.md)

**Go SDK**

Run the following code:

```go theme={null}
sgInstance, err := sdk.Services().Compute().V1().
    Instance().Get(
        ctx,
        &compute.GetInstanceRequest{
            Id: "<VM_ID>",
        },
    )
if err != nil {
    return err
}
if sgInstance.GetSpec() == nil {
    return errors.New("instance spec is missing")
}
interfaceFound := false
for _, networkInterface := range sgInstance.Spec.NetworkInterfaces {
    if networkInterface.GetName() == "<network_interface_name>" {
        networkInterface.SecurityGroups = append(
            networkInterface.SecurityGroups,
            &compute.SecurityGroup{Id: "<security_group_ID>"},
        )
        interfaceFound = true
    }
}
if !interfaceFound {
    return errors.New("network interface not found")
}
sgUpdateOperation, err := sdk.Services().Compute().V1().
    Instance().Update(
        ctx,
        &compute.UpdateInstanceRequest{
            Metadata: sgInstance.Metadata,
            Spec:     sgInstance.Spec,
        },
    )
if err != nil {
    return err
}
if _, err = sgUpdateOperation.Wait(ctx); err != nil {
    return err
}
fmt.Println(sgUpdateOperation)
```

In the code, specify the following values:

* `<VM_ID>`: ID of the VM.
* `<network_interface_name>`: Name of the VM's network interface, for example, `eth0`.
* `<security_group_ID>`: ID of the security group. When you [create a security group](#creating-security-groups), the code saves its ID to `securityGroupID`.

The code gets the VM, adds the security group to `SecurityGroups` of the network interface, keeping the security groups that the interface already has, and then updates the VM.

**Python SDK**

Run the following code:

```python theme={null}
sg_instance_service = InstanceServiceClient(sdk)
sg_instance = await sg_instance_service.get(
    GetInstanceRequest(id="<VM_ID>"),
)
if sg_instance.spec is None:
    raise ValueError("instance spec is missing")
network_interfaces = list(sg_instance.spec.network_interfaces)
interface_found = False
for network_interface in network_interfaces:
    if network_interface.name == "<network_interface_name>":
        network_interface.security_groups = [
            *network_interface.security_groups,
            SecurityGroup(id="<security_group_ID>"),
        ]
        interface_found = True
if not interface_found:
    raise ValueError("network interface not found")
sg_instance.spec.network_interfaces = network_interfaces
sg_update_operation = await sg_instance_service.update(
    UpdateInstanceRequest(
        metadata=sg_instance.metadata,
        spec=sg_instance.spec,
    ),
)
await sg_update_operation.wait()
print(sg_update_operation)
```

In the code, specify the following values:

* `<VM_ID>`: ID of the VM.
* `<network_interface_name>`: Name of the VM's network interface, for example, `eth0`.
* `<security_group_ID>`: ID of the security group. When you [create a security group](#creating-security-groups), the code saves its ID to `security_group_id`.

The code gets the VM, adds the security group to `security_groups` of the network interface, keeping the security groups that the interface already has, and then updates the VM.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const sgInstanceService = new InstanceService(sdk);
const sgInstance = await sgInstanceService.get(
  GetInstanceRequest.create({
    id: "<VM_ID>",
  }),
);
if (!sgInstance.spec) {
  throw new Error("instance spec is missing");
}
const sgInterface = (sgInstance.spec.networkInterfaces ?? []).find(
  (networkInterface) => networkInterface.name === "<network_interface_name>",
);
if (!sgInterface) {
  throw new Error("network interface not found");
}
sgInterface.securityGroups = [
  ...(sgInterface.securityGroups ?? []),
  SecurityGroup.create({ id: "<security_group_ID>" }),
];
const sgUpdateOperation = await sgInstanceService.update(
  UpdateInstanceRequest.create({
    metadata: sgInstance.metadata,
    spec: sgInstance.spec,
  }),
).result;
await sgUpdateOperation.wait();
console.log(sgUpdateOperation);
```

In the code, specify the following values:

* `<VM_ID>`: ID of the VM.
* `<network_interface_name>`: Name of the VM's network interface, for example, `eth0`.
* `<security_group_ID>`: ID of the security group. When you [create a security group](#creating-security-groups), the code saves its ID to `securityGroupId`.

The code gets the VM, adds the security group to `securityGroups` of the network interface, keeping the security groups that the interface already has, and then updates the VM.

If a VM's network interface isn't added to any security group, the [default security group](https://docs.nebius.com/vpc/security-groups/overview.md#default-security-groups) of the VM's network controls traffic to and from this network interface. You can achieve this by making the list of the network interface's security groups empty.

## Deleting security groups

> [!WARNING]
>
> You can only delete non-default security groups that don't have any associated VMs. Before deleting a security group, add any associated VMs to other security groups or revert these VMs to defaults. For more details, see [Adding VMs to security groups](#adding-vms-to-security-groups).

**Web console**

To delete a security group:

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Switch to the **Security groups** tab.
3. Click  next to the security group you want to delete and select **Delete**.
4. In the window that opens, enter the name of the security group and click **Delete security group**.

   > [!NOTE]
   >
   > If the security group has any rules in it, you will first need to [delete the rules](#deleting-security-rules).

**CLI**

To delete a security group, run `nebius vpc security-group delete`:

```bash theme={null}
nebius vpc security-group delete <security_group_ID>
```

To get the security group ID, run `nebius vpc security-group list`.

**Go SDK**

Run the following code:

```go theme={null}
deletedGroupService := sdk.Services().VPC().V1().
    SecurityGroup()
deletedGroupOperation, err := deletedGroupService.Delete(
    ctx,
    &vpc.DeleteSecurityGroupRequest{
        Id: "<security_group_ID>",
    },
)
if err != nil {
    return err
}
if _, err = deletedGroupOperation.Wait(ctx); err != nil {
    return err
}
```

Set `Id` to the ID of the security group that you want to delete.

**Python SDK**

Run the following code:

```python theme={null}
deleted_group_service = SecurityGroupServiceClient(sdk)
deleted_group_operation = await deleted_group_service.delete(
    DeleteSecurityGroupRequest(
        id="<security_group_ID>",
    ),
)
await deleted_group_operation.wait()
```

Set `id` to the ID of the security group that you want to delete.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const deletedGroupService = new SecurityGroupService(sdk);
const deletedGroupOperation = await deletedGroupService.delete(
  DeleteSecurityGroupRequest.create({
    id: "<security_group_ID>",
  }),
).result;
await deletedGroupOperation.wait();
```

Set `id` to the ID of the security group that you want to delete.
