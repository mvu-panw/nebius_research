# How to connect to virtual machines in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to connect to virtual machines in Nebius AI Cloud

Safe connection to the VM over SSH uses a key pair: you place the public key on the VM and store the private key on your device.

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## Set up the VM

To be able to connect to the VM, define specific information during the [VM creation](https://docs.nebius.com/compute/virtual-machines/manage.md).

### Generate a key pair

Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You will need the [contents of the public key](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md#getting-the-public-key) and the path to your private key in later steps.

### Configure the user data

User configuration helps to quickly create VMs with identical user data: it stores your username and the public key for the access to the VM.

**CLI**

Create a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:

```bash theme={null}
export USER_DATA=$(jq -Rrs '.' <<EOF
#cloud-config
users:
  - name: $USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - $(cat ~/.ssh/id_ed25519.pub)
EOF
)
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The above example sets the value of the machine's `USER` environment variable as the username for the VM.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

**Go SDK**

Define `userData` as a string in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:

```go theme={null}
publicKeyBytes, err := os.ReadFile(
    os.ExpandEnv("$HOME/.ssh/id_ed25519.pub"),
)
if err != nil {
    return err
}
publicKey := strings.TrimSpace(string(publicKeyBytes))
userData := "#cloud-config\nusers:\n" +
    "  - name: user\n" +
    "    sudo: ALL=(ALL) NOPASSWD:ALL\n" +
    "    shell: /bin/bash\n" +
    "    ssh_authorized_keys:\n" +
    "      - " + publicKey
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The example sets `user`; replace it with your username.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

Pass `userData` to `InstanceSpec.CloudInitUserData` when you create the VM.

**Python SDK**

Define `user_data` as a string in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:

```python theme={null}
public_key = (
    Path.home()
    .joinpath(".ssh/id_ed25519.pub")
    .read_text()
    .strip()
)
user_data = "\n".join(
    [
        "#cloud-config",
        "users:",
        "  - name: user",
        "    sudo: ALL=(ALL) NOPASSWD:ALL",
        "    shell: /bin/bash",
        "    ssh_authorized_keys:",
        f"      - {public_key}",
    ],
)
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The example sets `user`; replace it with your username.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

Pass `user_data` to `InstanceSpec.cloud_init_user_data` when you create the VM.

**JavaScript SDK**

Define `userData` as a string in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:

```ts theme={null}
const publicKey = readFileSync(
  `${process.env.HOME}/.ssh/id_ed25519.pub`,
  "utf8",
).trim();
const userData = [
  "#cloud-config",
  "users:",
  "  - name: user",
  "    sudo: ALL=(ALL) NOPASSWD:ALL",
  "    shell: /bin/bash",
  "    ssh_authorized_keys:",
  `      - ${publicKey}`,
].join("\n");
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The example sets `user`; replace it with your username.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

Pass `userData` to `InstanceSpec.cloudInitUserData` when you create the VM.

### Configure the VM

When you [create the VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), specify the user data, network settings and boot disk:

**CLI**

In the `nebius compute instance create` command, set the following parameters:

* `--cloud-init-user-data`: Pass the user data with your username and public key.
* `--network-interfaces`: To enable public access to the VM, include `"public_ip_address": {}` in the network interface specification.

  Alternatively, to enable public access to the VM, set `"public_ip_address": {"allocation_id": "<allocation_ID>"}` with an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) ID. This way the public IP address is preserved as an allocation object and you can reuse it for another VM after deleting this one.

> **How to create an allocation**
>
> 1. Get the default subnet's ID:
>
>    ```bash theme={null}
>    export SUBNET_ID=$(nebius vpc subnet list \
>      --format jsonpath='{.items[0].metadata.id}')
>    ```
>
> 2. Create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) by using the default subnet's ID:
>
>    ```bash theme={null}
>    export ALLOCATION_ID=$(nebius vpc allocation create \
>      --ipv4-public-subnet-id $SUBNET_ID \
>      --name allocation-name \
>      --format jsonpath='{.metadata.id}')
>    ```
>
> > [!NOTE]
> >
> > If an allocation with a public address has not been assigned to any resource for 30 days, Nebius AI Cloud can delete this allocation and release its address. If you want to preserve the address, assign its allocation to a Nebius AI Cloud resource.

Example:

```bash theme={null}
nebius compute instance create \
  --name inference-vm \
  --resources-platform <platform> \
  --resources-preset <preset> \
  --boot-disk-existing-disk-id <boot_disk_ID> \
  --boot-disk-attach-mode READ_WRITE \
  --cloud-init-user-data "$USER_DATA" \
  --network-interfaces '[{"name": "eth0", "subnet_id": "<subnet_ID>", "ip_address": {}, "public_ip_address": {"allocation_id": "<allocation_ID>"}}]'
```

**Go SDK**

1. Get the subnet ID:

   ```go theme={null}
   subnets, err := sdk.Services().VPC().V1().
       Subnet().List(
           ctx,
           &vpc.ListSubnetsRequest{},
       )
   if err != nil {
       return err
   }
   if len(subnets.GetItems()) == 0 {
       return errors.New("no subnets found")
   }
   subnetID := subnets.GetItems()[0].GetMetadata().GetId()
   ```

2. Create a public allocation:

   ```go theme={null}
   allocationOperation, err := sdk.Services().VPC().V1().
       Allocation().Create(
           ctx,
           &vpc.CreateAllocationRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "allocation-name",
               },
               Spec: &vpc.AllocationSpec{
                   IpSpec: &vpc.AllocationSpec_Ipv4Public{
                       Ipv4Public: &vpc.IPv4PublicAllocationSpec{
                           Pool: &vpc.IPv4PublicAllocationSpec_SubnetId{
                               SubnetId: subnetID,
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = allocationOperation.Wait(ctx); err != nil {
       return err
   }
   allocationID := allocationOperation.ResourceID()
   ```

3. Set the platform, preset, existing boot disk ID and cloud-init user data:

   ```go theme={null}
   publicAllocation := &compute.PublicIPAddress_AllocationId{
       AllocationId: allocationID,
   }
   instanceOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "inference-vm",
               },
               Spec: &compute.InstanceSpec{
                   Resources: &compute.ResourcesSpec{
                       Platform: "<platform>",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "<preset>",
                       },
                   },
                   BootDisk: &compute.AttachedDiskSpec{
                       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
                       Type: &compute.AttachedDiskSpec_ExistingDisk{
                           ExistingDisk: &compute.ExistingDisk{
                               Id: "<boot_disk_ID>",
                           },
                       },
                   },
                   CloudInitUserData: userData,
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       {
                           Name:      "eth0",
                           SubnetId:  subnetID,
                           IpAddress: &compute.IPAddress{},
                           PublicIpAddress: &compute.PublicIPAddress{
                               Allocation: publicAllocation,
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = instanceOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the subnet ID:

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnets = await subnet_service.list(ListSubnetsRequest())
   if not subnets.items:
       raise ValueError("no subnets found")
   subnet_id = subnets.items[0].metadata.id
   ```

2. Create a public allocation:

   ```python theme={null}
   allocation_service = AllocationServiceClient(sdk)
   allocation_operation = await allocation_service.create(
       CreateAllocationRequest(
           metadata=ResourceMetadata(name="allocation-name"),
           spec=AllocationSpec(
               ipv4_public=IPv4PublicAllocationSpec(
                   subnet_id=subnet_id,
               ),
           ),
       ),
   )
   await allocation_operation.wait()
   allocation_id = allocation_operation.resource_id
   ```

3. Set the platform, preset, existing boot disk ID and cloud-init user data:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   create_instance_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="inference-vm"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="<platform>",
                   preset="<preset>",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(id="<boot_disk_ID>"),
               ),
               cloud_init_user_data=user_data,
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(
                           allocation_id=allocation_id,
                       ),
                   ),
               ],
           ),
       ),
   )
   await create_instance_operation.wait()
   ```

**JavaScript SDK**

1. Get the subnet ID:

   ```ts theme={null}
   const subnetService = new SubnetService(sdk);
   const subnets = await subnetService.list(
     ListSubnetsRequest.create({}),
   );
   const subnetId = subnets.items[0]?.metadata?.id;
   if (!subnetId) {
     throw new Error("no subnets found");
   }
   ```

2. Create a public allocation:

   ```ts theme={null}
   const allocationService = new AllocationService(sdk);
   const allocationOperation = await allocationService.create(
     CreateAllocationRequest.create({
       metadata: ResourceMetadata.create({
         name: "allocation-name",
       }),
       spec: AllocationSpec.create({
         ipSpec: {
           $case: "ipv4Public",
           ipv4Public: IPv4PublicAllocationSpec.create({
             pool: {
               $case: "subnetId",
               subnetId,
             },
           }),
         },
       }),
     }),
   ).result;
   await allocationOperation.wait();
   const allocationId = allocationOperation.resourceId();
   ```

3. Set the platform, preset, existing boot disk ID and cloud-init user data:

   ```ts theme={null}
   const connectInstanceService = new InstanceService(sdk);
   const connectInstanceOperation = await connectInstanceService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "inference-vm",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "<platform>",
           size: {
             $case: "preset",
             preset: "<preset>",
           },
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: "<boot_disk_ID>",
             }),
           },
         }),
         cloudInitUserData: userData,
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({
               allocation: {
                 $case: "allocationId",
                 allocationId,
               },
             }),
           }),
         ],
       }),
     }),
   ).result;
   await connectInstanceOperation.wait();
   ```

For the full set of parameters and more examples, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md#examples).

## Connect to the VM by using SSH

> [!NOTE]
>
> **Requirements to connect to a private IP address or FQDN**
>
> To connect to a VM from another VM by using a [private IP address](https://docs.nebius.com/compute/virtual-machines/network.md#private-ip-addresses) or an [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md), both VMs must be in the same network. An FQDN resolves only from workloads in the network whose [DNS zone](https://docs.nebius.com/vpc/dns/overview.md) holds it. Within that network, the VM's hostname alone is enough.

1. Get your VM's IP address:

   **Connecting from the internet**

   To connect to the VM from the internet (if you have enabled public access to it), get its public IP address:

   **CLI**

   ```bash theme={null}
   export PUBLIC_IP_ADDRESS=$(nebius compute instance get-by-name \
     --name <VM_name> \
     --format json \
     | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
   ```

   **Go SDK**

   ```go theme={null}
   publicInstance, err := sdk.Services().Compute().V1().
       Instance().GetByName(
           ctx,
           &common.GetByNameRequest{
               Name: "<VM_name>",
           },
       )
   if err != nil {
       return err
   }
   publicAddress := publicInstance.GetStatus().
       GetNetworkInterfaces()[0].GetPublicIpAddress().GetAddress()
   publicIPAddress := strings.Split(publicAddress, "/")[0]
   if publicIPAddress == "" {
       return fmt.Errorf("public IP address is missing")
   }
   ```

   **Python SDK**

   ```python theme={null}
   public_ip_service = InstanceServiceClient(sdk)
   public_instance = await public_ip_service.get_by_name(
       GetByNameRequest(name="<VM_name>"),
   )
   public_address = (
       public_instance.status.network_interfaces[0]
       .public_ip_address.address
   )
   public_ip_address = public_address.split("/")[0]
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const publicIpInstanceService = new InstanceService(sdk);
   const publicIpInstance = await publicIpInstanceService.getByName(
     GetByNameRequest.create({
       name: "<VM_name>",
     }),
   );
   const publicAddress = publicIpInstance.status
     ?.networkInterfaces[0]?.publicIpAddress?.address;
   let publicIpAddress = publicAddress?.split("/")[0];
   ```

   **Connecting from another VM**

   To connect to the VM from another Compute VM, get the private IP address or FQDN of the VM that you connect to:

   **CLI**

   * Private IP address:

     ```bash theme={null}
     nebius compute instance get-by-name \
       --name <VM_name> \
       --format json \
       | jq -r '.status.network_interfaces[0].ip_address.address | split("/")[0]'
     ```

   * FQDN:

     ```bash theme={null}
     nebius compute instance get-by-name \
       --name <VM_name> \
       --format json \
       | jq -r '.status.network_interfaces[0].fqdn | split("/")[0]'
     ```

   **Go SDK**

   * Private IP address:

     ```go theme={null}
     privateInstance, err := sdk.Services().Compute().V1().
         Instance().GetByName(
             ctx,
             &common.GetByNameRequest{
                 Name: "<VM_name>",
             },
         )
     if err != nil {
         return err
     }
     privateAddress := privateInstance.GetStatus().
         GetNetworkInterfaces()[0].GetIpAddress().GetAddress()
     fmt.Println(strings.Split(privateAddress, "/")[0])
     ```

   * FQDN:

     ```go theme={null}
     fqdnInstance, err := sdk.Services().Compute().V1().
         Instance().GetByName(
             ctx,
             &common.GetByNameRequest{
                 Name: "<VM_name>",
             },
         )
     if err != nil {
         return err
     }
     fqdn := fqdnInstance.GetStatus().GetNetworkInterfaces()[0].GetFqdn()
     fmt.Println(strings.Split(fqdn, "/")[0])
     ```

   **Python SDK**

   * Private IP address:

     ```python theme={null}
     private_ip_service = InstanceServiceClient(sdk)
     private_instance = await private_ip_service.get_by_name(
         GetByNameRequest(name="<VM_name>"),
     )
     private_address = (
         private_instance.status.network_interfaces[0]
         .ip_address.address
     )
     print(private_address.split("/")[0])
     ```

   * FQDN:

     ```python theme={null}
     fqdn_service = InstanceServiceClient(sdk)
     fqdn_instance = await fqdn_service.get_by_name(
         GetByNameRequest(name="<VM_name>"),
     )
     fqdn = fqdn_instance.status.network_interfaces[0].fqdn
     print(fqdn.split("/")[0])
     ```

   **JavaScript SDK**

   * Private IP address:

     ```ts theme={null}
     const privateIpInstanceService = new InstanceService(sdk);
     const privateIpInstance = await privateIpInstanceService.getByName(
       GetByNameRequest.create({
         name: "<VM_name>",
       }),
     );
     const privateAddress = privateIpInstance.status
       ?.networkInterfaces[0]?.ipAddress?.address;
     console.log(privateAddress?.split("/")[0]);
     ```

   * FQDN:

     ```ts theme={null}
     const fqdnInstanceService = new InstanceService(sdk);
     const fqdnInstance = await fqdnInstanceService.getByName(
       GetByNameRequest.create({
         name: "<VM_name>",
       }),
     );
     const fqdn = fqdnInstance.status?.networkInterfaces[0]?.fqdn;
     console.log(fqdn?.split("/")[0]);
     ```

2. Connect to the VM:

   **Connecting from the internet**

   ```bash theme={null}
   ssh <username>@<public_IP_address>
   ```

   If your private key is stored in a custom location, specify the path to it with the `-i` parameter:

   ```bash theme={null}
   ssh -i ~/.ssh/<private_key_file> <username>@<public_IP_address>
   ```

   **Connecting from another VM**

   Use the received private address or FQDN:

   ```bash theme={null}
   ssh <username>@<private_address_or_FQDN>
   ```

   If your private key is stored in a custom location, specify the path to it with the `-i` parameter:

   ```bash theme={null}
   ssh -i ~/.ssh/<private_key_file> <username>@<private_address_or_FQDN>
   ```

## Shared access to the VM

To let the other users connect to your VM:

1. Ask them to [generate an SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md#generating-a-key-pair) and share the [contents of their public key](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md#getting-the-public-key) with you.

2. Connect to the VM under the name used when creating the VM:

   ```bash theme={null}
   ssh <username>@<public_IP_address>
   ```

3. Create a new user for VM access, named `newuser` in this example:

   ```bash theme={null}
   sudo useradd -m -d /home/newuser -s /bin/bash newuser
   ```

4. Switch to the new user:

   ```bash theme={null}
   sudo su - newuser
   ```

5. Create the `ssh` directory:

   ```bash theme={null}
   mkdir .ssh
   ```

6. In the directory, create the `authorized_keys` file:

   ```bash theme={null}
   cd .ssh
   touch authorized_keys
   ```

7. Add the new user's public key to the created file:

   ```bash theme={null}
   echo "<public_key>" > /home/newuser/.ssh/authorized_keys
   ```

8. Change the directory's access permissions:

   ```bash theme={null}
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

9. Exit the new user's shell:

   ```bash theme={null}
   exit
   ```

10. Restart the VM:

    ```bash theme={null}
    sudo reboot
    ```

11. Ask the other user to check the connection:

    ```bash theme={null}
    ssh newuser@<public_IP_address>
    ```

## Example

Example of getting the public IP address of the VM named `training-instance` and connecting to it from the internet:

**CLI**

```bash theme={null}
export PUBLIC_IP_ADDRESS=$(nebius compute instance get-by-name \
  --name training-instance \
  --format json \
  | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
ssh $USER@$PUBLIC_IP_ADDRESS
```

**Go SDK**

```go theme={null}
trainingInstance, err := sdk.Services().Compute().V1().
    Instance().GetByName(
        ctx,
        &common.GetByNameRequest{
            Name: "training-instance",
        },
    )
if err != nil {
    return err
}
trainingAddress := trainingInstance.GetStatus().
    GetNetworkInterfaces()[0].GetPublicIpAddress().GetAddress()
publicIPAddress = strings.Split(trainingAddress, "/")[0]
fmt.Printf("ssh user@%s\n", publicIPAddress)
```

**Python SDK**

```python theme={null}
training_ip_service = InstanceServiceClient(sdk)
training_instance = await training_ip_service.get_by_name(
    GetByNameRequest(name="training-instance"),
)
training_address = (
    training_instance.status.network_interfaces[0]
    .public_ip_address.address
)
public_ip_address = training_address.split("/")[0]
print(f"ssh user@{public_ip_address}")
```

**JavaScript SDK**

```ts theme={null}
const trainingInstanceService = new InstanceService(sdk);
const trainingInstance = await trainingInstanceService.getByName(
  GetByNameRequest.create({
    name: "training-instance",
  }),
);
const trainingAddress = trainingInstance.status
  ?.networkInterfaces[0]?.publicIpAddress?.address;
publicIpAddress = trainingAddress?.split("/")[0];
console.log(`ssh user@${publicIpAddress}`);
```
