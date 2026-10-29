# How to stop and start Compute virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/stop-start

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to stop and start Compute virtual machines

To proceed with [maintenance](https://docs.nebius.com/compute/virtual-machines/maintenance.md), stop and start virtual machines [manually](#how-to-stop-and-start-vms-manually) or [automatically](#how-to-stop-and-start-vms-automatically-by-using-autohealing). If you need to keep your VMs running, [contact the support team](https://console.nebius.com/support/create-ticket) and consult them about the possibility of rescheduling maintenance of the affected VMs.

> [!WARNING]
>
> Do not stop your VM by using Linux commands, such as `shutdown` or `halt`. Compute considers this as a failure, reboots the VM automatically and continues charging for this VM. Use Nebius AI Cloud interfaces instead and follow the instructions below.

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

## How to stop and start VMs manually

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. On the **Standalone VMs** tab, find VMs with the maintenance label.

   > **Example**
   >
   > ![maintenance-label](https://mintcdn.com/nebius-ai-cloud/3vrg63wLg56IgavR/_assets/compute/maintenance-label-for-one-vm.png?fit=max\&auto=format\&n=3vrg63wLg56IgavR\&q=85\&s=7e0e5645e6e70a1b07b0b31fb768ffb9)

3. Click  → **Stop** for these VMs.

4. In the window that opens, confirm stopping the VM.

5. When the VM status changes to **Stopped**, click  → **Start**.

6. In the window that opens, confirm starting the VM.

**CLI**

1. Check whether maintenance is scheduled for a VM:

   ```bash theme={null}
   nebius compute instance get --id <VM_ID>
   ```

   If the output contains the `status.maintenance_event_id` parameter, this means that you need to stop and start this VM.

2. Stop the VM:

   ```bash theme={null}
   nebius compute instance stop --id <VM_ID>
   ```

3. Start the VM:

   ```bash theme={null}
   nebius compute instance start --id <VM_ID>
   ```

**Go SDK**

1. Check whether maintenance is scheduled for a VM:

   ```go theme={null}
   instance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   fmt.Println(instance)
   ```

   If the response contains a maintenance event ID in the VM status, stop and start this VM.

2. Stop the VM:

   ```go theme={null}
   stopInstanceOperation, err := sdk.Services().Compute().V1().
       Instance().Stop(
           ctx,
           &compute.StopInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = stopInstanceOperation.Wait(ctx); err != nil {
       return err
   }
   ```

3. Start the VM:

   ```go theme={null}
   startOperation, err := sdk.Services().Compute().V1().
       Instance().Start(
           ctx,
           &compute.StartInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = startOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Check whether maintenance is scheduled for a VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   print(instance)
   ```

   If the response contains a maintenance event ID in the VM status, stop and start this VM.

2. Stop the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   stop_instance_operation = await instance_service.stop(
       StopInstanceRequest(id="<VM_ID>"),
   )
   await stop_instance_operation.wait()
   ```

3. Start the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   start_instance_operation = await instance_service.start(
       StartInstanceRequest(id="<VM_ID>"),
   )
   await start_instance_operation.wait()
   ```

**JavaScript SDK**

1. Check whether maintenance is scheduled for a VM:

   ```ts theme={null}
   const getInstanceService = new InstanceService(sdk);
   const instance = await getInstanceService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   console.log(instance);
   ```

   If the response contains a maintenance event ID in the VM status, stop and start this VM.

2. Stop the VM:

   ```ts theme={null}
   const stopInstanceService = new InstanceService(sdk);
   const stopInstanceOperation = await stopInstanceService.stop(
     StopInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await stopInstanceOperation.wait();
   ```

3. Start the VM:

   ```ts theme={null}
   const startInstanceService = new InstanceService(sdk);
   const startInstanceOperation = await startInstanceService.start(
     StartInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await startInstanceOperation.wait();
   ```

## How to stop and start VMs automatically by using autohealing

You can create a VM with the autohealing function. It allows a VM to automatically stop and start each time maintenance is scheduled. As a result, the applications on this VM are highly available.

> [!WARNING]
>
> Use autohealing only if the automatic VM shutdown is safe for the workloads on this VM. If you cannot stop the VM at any time, it is better to manage the VM [manually](#how-to-stop-and-start-vms-manually).

To create a VM that stops and starts automatically during maintenance events:

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#create-a-service-account).

3. Add it to the default `viewers` group:

   **CLI**

   1. Get the ID of the `viewers` group:

      ```bash theme={null}
      nebius iam group get-by-name --name viewers \
        --parent-id <tenant_ID> \
        --format jsonpath='{.metadata.id}'
      ```

      In the command, specify your [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).

   2. Get the ID of the service account:

      ```bash theme={null}
      nebius iam service-account get-by-name \
        --name <service_account_name> \
        --format jsonpath='{.metadata.id}'
      ```

   3. Add the service account to the `viewers` group:

      ```bash theme={null}
      nebius iam group-membership create \
        --parent-id <viewers_group_ID> \
        --member-id <service_account_ID>
      ```

   **Go SDK**

   1. Get the ID of the `viewers` group:

      ```go theme={null}
      viewersGroup, err := sdk.Services().IAM().V1().
          Group().GetByName(
              ctx,
              &iam.GetGroupByNameRequest{
                  ParentId: "<tenant_ID>",
                  Name:     "viewers",
              },
          )
      if err != nil {
          return err
      }
      viewersID := viewersGroup.GetMetadata().GetId()
      if viewersID == "" {
          return errors.New("viewers group ID is missing")
      }
      ```

      In the code, specify your [tenant ID](https://docs.nebius.com/iam/get-tenants.md).

   2. Get the ID of the service account:

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
      if serviceAccountID == "" {
          return errors.New("service account ID is missing")
      }
      ```

      In the code, specify the service account name.

   3. Add the service account to the `viewers` group:

      ```go theme={null}
      membershipOperation, err := sdk.Services().IAM().V1().
          GroupMembership().Create(
              ctx,
              &iam.CreateGroupMembershipRequest{
                  Metadata: &common.ResourceMetadata{
                      ParentId: "<viewers_group_ID>",
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

      In the code, specify the IDs of the `viewers` group and the service account.

   **Python SDK**

   1. Get the ID of the `viewers` group:

      ```python theme={null}
      group_service = GroupServiceClient(sdk)
      viewers_group = await group_service.get_by_name(
          GetGroupByNameRequest(
              parent_id="<tenant_ID>",
              name="viewers",
          ),
      )
      viewers_id = viewers_group.metadata.id
      ```

      In the code, specify your [tenant ID](https://docs.nebius.com/iam/get-tenants.md).

   2. Get the ID of the service account:

      ```python theme={null}
      service_account_service = ServiceAccountServiceClient(sdk)
      service_account = await service_account_service.get_by_name(
          GetServiceAccountByNameRequest(name="<service_account_name>"),
      )
      service_account_id = service_account.metadata.id
      ```

      In the code, specify the service account name.

   3. Add the service account to the `viewers` group:

      ```python theme={null}
      membership_service = GroupMembershipServiceClient(sdk)
      membership_operation = await membership_service.create(
          CreateGroupMembershipRequest(
              metadata=ResourceMetadata(parent_id="<viewers_group_ID>"),
              spec=GroupMembershipSpec(member_id="<service_account_ID>"),
          ),
      )
      await membership_operation.wait()
      ```

      In the code, specify the IDs of the `viewers` group and the service account.

   **JavaScript SDK**

   1. Get the ID of the `viewers` group:

      ```ts theme={null}
      const groupService = new GroupService(sdk);
      const viewersGroup = await groupService.getByName(
        GetGroupByNameRequest.create({
          parentId: "<tenant_ID>",
          name: "viewers",
        }),
      );
      const viewersId = viewersGroup.metadata?.id;
      if (!viewersId) {
        throw new Error("viewers group ID is missing");
      }
      ```

      In the code, specify your [tenant ID](https://docs.nebius.com/iam/get-tenants.md).

   2. Get the ID of the service account:

      ```ts theme={null}
      const saService = new ServiceAccountService(sdk);
      const serviceAccount = await saService.getByName(
        GetServiceAccountByNameRequest.create({
          name: "<service_account_name>",
        }),
      );
      const serviceAccountId = serviceAccount.metadata?.id;
      if (!serviceAccountId) {
        throw new Error("service account ID is missing");
      }
      ```

      In the code, specify the service account name.

   3. Add the service account to the `viewers` group:

      ```ts theme={null}
      const membershipService = new GroupMembershipService(sdk);
      const membershipOperation = await membershipService.create(
        CreateGroupMembershipRequest.create({
          metadata: ResourceMetadata.create({
            parentId: "<viewers_group_ID>",
          }),
          spec: GroupMembershipSpec.create({
            memberId: "<service_account_ID>",
          }),
        }),
      ).result;
      await membershipOperation.wait();
      ```

      In the code, specify the IDs of the `viewers` group and the service account.

4. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md). In its configuration, specify the following:

   * [Settings that allow connections](https://docs.nebius.com/compute/virtual-machines/connect.md#set-up-the-vm) to this VM.
   * Created service account:

     **CLI**

     ```bash theme={null}
     nebius compute instance create \
       ... \
       --service-account-id <service_account_ID>
     ```

     **Go SDK**

     ```go theme={null}
     fsAttachMode := compute.AttachedFilesystemSpec_READ_WRITE
     existingFS := &compute.ExistingFilesystem{
         Id: filesystemID,
     }
     fsType := &compute.AttachedFilesystemSpec_ExistingFilesystem{
         ExistingFilesystem: existingFS,
     }
     instanceOperation, err := sdk.Services().Compute().V1().
         Instance().Create(
             ctx,
             &compute.CreateInstanceRequest{
                 Metadata: &common.ResourceMetadata{
                     Name: "vm",
                 },
                 Spec: &compute.InstanceSpec{
                     ServiceAccountId: "<service_account_ID>",
                     Resources: &compute.ResourcesSpec{
                         Platform: "cpu-e2",
                         Size: &compute.ResourcesSpec_Preset{
                             Preset: "2vcpu-8gb",
                         },
                     },
                     BootDisk: &compute.AttachedDiskSpec{
                         AttachMode: compute.AttachedDiskSpec_READ_WRITE,
                         Type: &compute.AttachedDiskSpec_ExistingDisk{
                             ExistingDisk: &compute.ExistingDisk{
                                 Id: bootDiskID,
                             },
                         },
                     },
                     Filesystems: []*compute.AttachedFilesystemSpec{
                         {
                             AttachMode: fsAttachMode,
                             MountTag:   "filesystem-1",
                             Type:       fsType,
                         },
                     },
                     NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                         {
                             Name:           "eth0",
                             SubnetId:       subnetID,
                             IpAddress:      &compute.IPAddress{},
                             PublicIpAddress: &compute.PublicIPAddress{},
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

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     create_instance_operation = await instance_service.create(
         CreateInstanceRequest(
             metadata=ResourceMetadata(name="vm"),
             spec=InstanceSpec(
                 service_account_id="<service_account_ID>",
                 resources=ResourcesSpec(
                     platform="cpu-e2",
                     preset="2vcpu-8gb",
                 ),
                 boot_disk=AttachedDiskSpec(
                     attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                     existing_disk=ExistingDisk(id=boot_disk_id),
                 ),
                 filesystems=[
                     AttachedFilesystemSpec(
                         attach_mode=(
                             AttachedFilesystemSpec.AttachMode.READ_WRITE
                         ),
                         existing_filesystem=ExistingFilesystem(
                             id=filesystem_id,
                         ),
                         mount_tag="filesystem-1",
                     ),
                 ],
                 network_interfaces=[
                     NetworkInterfaceSpec(
                         name="eth0",
                         subnet_id=subnet_id,
                         ip_address=IPAddress(),
                         public_ip_address=PublicIPAddress(),
                     ),
                 ],
             ),
         ),
     )
     await create_instance_operation.wait()
     ```

     **JavaScript SDK**

     ```ts theme={null}
     const createInstanceService = new InstanceService(sdk);
     const createInstanceOperation = await createInstanceService.create(
       CreateInstanceRequest.create({
         metadata: ResourceMetadata.create({
           name: "vm",
         }),
         spec: InstanceSpec.create({
           serviceAccountId: "<service_account_ID>",
           resources: ResourcesSpec.create({
             platform: "cpu-e2",
             size: {
               $case: "preset",
               preset: "2vcpu-8gb",
             },
           }),
           bootDisk: AttachedDiskSpec.create({
             attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
             type: {
               $case: "existingDisk",
               existingDisk: ExistingDisk.create({
                 id: bootDiskId,
               }),
             },
           }),
           filesystems: [
             AttachedFilesystemSpec.create({
               attachMode: AttachedFilesystemSpec_AttachMode.READ_WRITE,
               mountTag: "filesystem-1",
               type: {
                 $case: "existingFilesystem",
                 existingFilesystem: ExistingFilesystem.create({
                   id: filesystemId,
                 }),
               },
             }),
           ],
           networkInterfaces: [
             NetworkInterfaceSpec.create({
               name: "eth0",
               subnetId: subnetId,
               ipAddress: IPAddress.create({}),
               publicIpAddress: PublicIPAddress.create({}),
             }),
           ],
         }),
       }),
     ).result;
     await createInstanceOperation.wait();
     ```

5. [Connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

6. Install `jq` on the VM:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

7. Go to the `/usr/local/bin/` directory:

   ```bash theme={null}
   cd /usr/local/bin/
   ```

8. Create the `vm_maintenance.sh` file:

   ```bash theme={null}
   sudo nano vm_maintenance.sh
   ```

9. Add the following Bash script to the file:

   ```bash theme={null}
   #!/bin/bash

   INSTANCE_ID_FILE="/mnt/cloud-metadata/instance-id"
   CHECK_INTERVAL=600 # 10 minutes in seconds

   # Check if the Nebius AI Cloud CLI is installed
   check_nebius_installed() {
       if ! command -v nebius &> /dev/null; then
           echo "$(date) - Nebius utility not found, exiting..."
           exit 1
       fi
   }

   get_instance_id() {
       if [[ -f "$INSTANCE_ID_FILE" ]]; then
           cat "$INSTANCE_ID_FILE"
       else
           echo "File with the virtual machine ID is not found"
           exit 1
       fi
   }

   # Handle a maintenance event
   handle_maintenance_event() {
       # Add custom actions before stopping the virtual machine
       echo "$(date) - Custom actions before stopping the virtual machine"
       sudo shutdown -h +1 "Restarting virtual machine due to maintenance"
   }

   check_nebius_installed

   # main loop
   while true; do
       INSTANCE_ID=$(get_instance_id)
       if [[ -z "$INSTANCE_ID" ]]; then
           echo "Virtual machine ID is empty"
           exit 1
       fi

       RESPONSE=$(nebius compute instance get --id "$INSTANCE_ID" --format json)
       if echo "$RESPONSE" | jq -e '.status.maintenance_event_id' >/dev/null; then
           echo "$(date) - Maintenance event detected"
           handle_maintenance_event
       else
           echo "$(date) - No maintenance event detected"
       fi

       sleep "$CHECK_INTERVAL"
   done
   ```

10. Make the file executable:

    ```bash theme={null}
    sudo chmod +x /usr/local/bin/vm_maintenance.sh
    ```

11. To make the script run continuously and restart it when the VM fails or reboots, add a `systemd` unit to the script:

    ```bash theme={null}
    sudo bash -c 'cat > /etc/systemd/system/vm_maintenance.service << EOF
    [Unit]
    Description=VM Maintenance Event Handler
    After=network.target

    [Service]
    ExecStart=/usr/local/bin/vm_maintenance.sh
    Restart=always
    User=root
    Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    WorkingDirectory=/usr/local/bin
    StandardOutput=append:/var/log/vm_maintenance.log
    StandardError=append:/var/log/vm_maintenance.log

    [Install]
    WantedBy=multi-user.target
    EOF'
    ```

12. Start the service created with the `systemd` unit, and let it restart in case of the VM reboot:

    ```bash theme={null}
    sudo systemctl daemon-reload
    sudo systemctl start vm_maintenance
    sudo systemctl enable vm_maintenance
    sudo systemctl status vm_maintenance
    ```

    The output example is the following:

    ```text theme={null}
    Created symlink /etc/systemd/system/multi-user.target.wants/vm_maintenance.service → /etc/systemd/system/vm_maintenance.service.
    ● vm_maintenance.service - VM Maintenance Event Handler
         Loaded: loaded (/etc/systemd/system/vm_maintenance.service; enabled; vendor preset: enabled)
         Active: active (running) since Fri 2025-04-25 10:19:19 UTC; 214ms ago
       Main PID: 28530 (vm_maintenance.)
          Tasks: 6 (limit: 19056)
         Memory: 24.3M
            CPU: 25ms
         CGroup: /system.slice/vm_maintenance.service
                 ├─28530 /bin/bash /usr/local/bin/vm_maintenance.sh
                 └─28535 nebius compute instance get --id computeinstance-*** --format json

    Apr 25 10:19:19 computeinstance-*** systemd[1]: Started VM Maintenance Event Handler.
    ```

Now, the script runs continuously, and the VM stops and starts during maintenance events.
