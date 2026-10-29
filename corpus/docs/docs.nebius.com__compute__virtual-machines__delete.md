# Deleting a Compute virtual machine

Source: https://docs.nebius.com/compute/virtual-machines/delete

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deleting a Compute virtual machine

If [standalone disks](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks) or filesystems are attached to your virtual machine (VM), Compute doesn't automatically delete them. To stop being charged for volumes you no longer need, [delete](https://docs.nebius.com/compute/storage/manage.md#how-to-delete-a-volume) these volumes separately.

If VM-managed disks are attached to your VM, they are deleted along with the VM automatically. Charges for these disks stop immediately.

To delete a VM:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**. On the **Standalone VMs** tab, click the virtual machine you want to delete.
2. On the VM page, go to the **Settings** tab.
3. Click **Delete virtual machine**.
4. In the window that opens, confirm the deletion.

**CLI**

1. Get the ID of the virtual machine you want to delete:

   ```bash theme={null}
   nebius compute instance list
   ```

2. Delete the virtual machine:

   ```bash theme={null}
   nebius compute instance delete <VM_ID>
   ```

**Terraform**

1. Remove the corresponding `nebius_compute_v1_instance` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the virtual machine you want to delete:

   ```go theme={null}
   instances, err := sdk.Services().Compute().V1().
       Instance().List(
           ctx,
           &compute.ListInstancesRequest{},
       )
   if err != nil {
       return err
   }
   fmt.Println(instances)
   ```

2. Delete the virtual machine:

   ```go theme={null}
   deleteFinalOperation, err := sdk.Services().Compute().V1().
       Instance().Delete(
           ctx,
           &compute.DeleteInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = deleteFinalOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the ID of the virtual machine you want to delete:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instances = await instance_service.list(ListInstancesRequest())
   print(instances)
   ```

2. Delete the virtual machine:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   delete_final_operation = await instance_service.delete(
       DeleteInstanceRequest(id="<VM_ID>"),
   )
   await delete_final_operation.wait()
   ```

**JavaScript SDK**

1. Get the ID of the virtual machine you want to delete:

   ```ts theme={null}
   const manageListInstanceService = new InstanceService(sdk);
   const listedInstances = await manageListInstanceService.list(
     ListInstancesRequest.create({}),
   );
   console.log(listedInstances);
   ```

2. Delete the virtual machine:

   ```ts theme={null}
   const finalVmDeleteService = new InstanceService(sdk);
   const deleteFinalVmOperation =
     await finalVmDeleteService.delete(
       DeleteInstanceRequest.create({
         id: "<VM_ID>",
       }),
     ).result;
   await deleteFinalVmOperation.wait();
   ```
