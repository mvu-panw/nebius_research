# CUDA initialization error on virtual machines in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/cuda-init-error

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# CUDA initialization error on virtual machines in Nebius AI Cloud

On Compute virtual machines with GPUs, CUDA may fail to initialize in rare cases, which may lead to problems when running GPU workloads. This can happen due to various reasons, including issues with NVIDIA Fabric Manager initialization. You can resolve this issue by restarting the NVIDIA Fabric Manager service, the GPUs on the VM or the entire VM.

## Issue

On virtual machines with GPUs, CUDA may fail to initialize in rare cases, leading to errors when you run your workloads and tests. This can occur on any VM with GPUs, regardless of the specific platform, number of GPUs or boot disk image.

> For example, executing PyTorch code may result in the following error:
>
> ```text theme={null}
> ERROR: The NVIDIA Driver is present, but CUDA failed to initialize.  
> GPU functionality will not be available.
> [[ System not yet initialized (error 802) ]]
>
> /usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:129: UserWarning: 
> CUDA initialization: Unexpected error from cudaGetDeviceCount(). Did you run some cuda functions
> before calling NumCudaDevices() that might have already set an error? 
> Error 802: system not yet initialized (Triggered internally at 
> /opt/pytorch/pytorch/c10/cuda/CUDAFunctions.cpp:109.)
> return torch._C._cuda_getDeviceCount() > 0
> ```

## Possible cause

One possible cause of CUDA initialization failures is an issue with the [NVIDIA Fabric Manager](https://docs.nvidia.com/datacenter/tesla/fabric-manager-user-guide/index.html), a component that provides NVLink and NVSwitch support for multi-GPU VMs. In rare cases, its service, `nvidia-fabricmanager`, does not initialize on VM startup because of a race condition or other timing issues. This can cause initialization issues for CUDA and GPUs on the VM. However, CUDA initialization failures can also occur due to other reasons.

> **How to check nvidia-fabricmanager**
>
> 1. [Connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md).
> 2. Run the following command:
>
>    ```bash theme={null}
>    sudo systemctl status nvidia-fabricmanager
>    ```
>
>    If the service is not running, the `Active` line in the output indicates that:
>
>    ```text theme={null}
>    ○ nvidia-fabricmanager.service - NVIDIA fabric manager service
>         Loaded: loaded (/lib/systemd/system/nvidia-fabricmanager.service; enabled; ven>
>         Active: inactive (dead) since Fri 2025-05-23 07:37:49 UTC; 27s ago
>       Main PID: 3240 (code=exited, status=0/SUCCESS)
>            CPU: 787ms
>    ```

## Solutions

You can solve the issue on your existing VM without having to create a new VM. Try the following steps in order:

1. Start the NVIDIA Fabric Manager service:

   1. [Connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md).

   2. Run the following command:

      ```bash theme={null}
      sudo systemctl start nvidia-fabricmanager
      ```

   3. Check whether starting the service worked. To do this, you can try running your workload or get diagnostic information about the GPUs on the VM. For example, use the [NVIDIA System Management Interface](https://docs.nvidia.com/deploy/nvidia-smi/index.html) (`nvidia-smi`) to get the fabric states and statuses of the GPUs:

      ```bash theme={null}
      nvidia-smi -q | grep -A 2 'Fabric'
      ```

      In the output, all the GPUs should be in the `Completed` fabric state and the `Success` status:

      ```bash theme={null}
      Fabric
          State                             : Completed
          Status                            : Success
      --
      Fabric
          State                             : Completed 
          Status                            : Success
      ...
      ```

   If this step has not worked, stay connected to the VM and proceed to the next step.

2. Restart the GPUs on the VM:

   > [!WARNING]
   >
   > If your VM is a [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/index.md) node (that is, its name starts with `mk8snodegroup`), skip this step and proceed to the next step.

   1. Stop the services and workloads that use the GPUs. For example, if you are not running any workloads on the VM, you only need to stop the monitoring services:

      ```bash theme={null}
      sudo systemctl stop nebius_observability_agent
      sudo systemctl stop nvidia-dcgm.service
      ```

   2. Run the `nvidia-smi` command that restarts GPUs:

      ```bash theme={null}
      sudo nvidia-smi -r
      ```

      This may take several minutes. You should see the following output:

      ```text theme={null}
      GPU 00000000:8D:00.0 was successfully reset.
      GPU 00000000:91:00.0 was successfully reset.
      GPU 00000000:95:00.0 was successfully reset.
      GPU 00000000:99:00.0 was successfully reset.
      GPU 00000000:AB:00.0 was successfully reset.
      GPU 00000000:AF:00.0 was successfully reset.
      GPU 00000000:B3:00.0 was successfully reset.
      GPU 00000000:B7:00.0 was successfully reset.

      Note: The operation has successfully reset all GPUs and NVSwitches. If the services, such as
      nvidia-fabricmanager, which manage or monitor NVSwitches are running, they might have been
      affected by this operation. Please refer respective service status or logs for details.
      All done.
      ```

   3. Start the stopped workloads and services again. For example, to start the monitoring services, run the following command:

      ```bash theme={null}
      sudo systemctl start nvidia-dcgm.service
      sudo systemctl start nebius_observability_agent
      ```

   4. Check whether restarting the GPUs worked. For example, you can run your workload or use `nvidia-smi`:

      ```bash theme={null}
      nvidia-smi -q | grep -A 2 'Fabric'
      ```

      If the step has not worked, e.g. there are GPUs that are not in the `Completed` fabric state and the `Success` status, proceed to the next step.

3. [Restart the VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md).

   After that, [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md) and then check whether restarting the VM worked. For example, you can run your workload or use `nvidia-smi`:

   ```bash theme={null}
   nvidia-smi -q | grep -A 2 'Fabric'
   ```

   If the step has not worked, e.g. there are GPUs that are not in the `Completed` fabric state and the `Success` status, [contact support](https://console.nebius.com/support/create-ticket).
