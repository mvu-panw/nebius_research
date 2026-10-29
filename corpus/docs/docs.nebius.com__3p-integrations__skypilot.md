# Managing AI workloads on Compute virtual machines with SkyPilot

Source: https://docs.nebius.com/3p-integrations/skypilot

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing AI workloads on Compute virtual machines with SkyPilot

Nebius AI Cloud supports integration with [SkyPilot](https://docs.skypilot.co/en/latest/docs/index.html), an open-source framework for running AI workloads on different cloud infrastructures. SkyPilot can create clusters of Compute virtual machines (VMs) and run workloads on them based on task definitions like this:

```yaml theme={null}
resources:
  infra: nebius
  accelerators: H100:1

run: |
  nvidia-smi
```

In this tutorial, you will deploy and use the Managed SkyPilot API Server in the Nebius AI Cloud console to manage your SkyPilot workloads.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram)
* [Compute disks](https://docs.nebius.com/compute/resources/pricing.md#disks)
* [Object Storage buckets](https://docs.nebius.com/object-storage/resources/pricing.md)

## Prerequisites

1. Deploy the Managed SkyPilot API Server:

   1. In the Nebius AI Cloud console, go to  **AI orchestration** → **SkyPilot**.
   2. Enter a name for the application or keep the default one.
   3. Select a **Platform** and a **Preset** (vCPUs and RAM) for the API server VM.
   4. Click **Deploy application**.

2. Install `uv`, a Python package manager, on your local machine:

   ```bash theme={null}
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install the SkyPilot CLI:

   ```bash theme={null}
   uv tool install --with pip "skypilot[nebius]"
   ```

4. Connect to the managed API server. On the application page, click **How to connect** and copy the login command. Run the command in your terminal:

   ```bash theme={null}
   sky api login -e "<your_server_endpoint>"
   ```

   Replace `<your_server_endpoint>` with the public endpoint URL from your deployed application.

5. Verify that SkyPilot can access your project:

   ```bash theme={null}
   sky check nebius
   ```

   If the check is successful, the output contains the following:

   ```text theme={null}
   Checking credentials to enable infra 'nebius'...
     Nebius: enabled
   ```

6. Clone the [Nebius ML Cookbook](https://github.com/nebius/ml-cookbook) repository and go to the `skypilot` directory:

   ```bash theme={null}
   git clone https://github.com/nebius/ml-cookbook.git
   cd ml-cookbook/skypilot
   ```

   The ML Cookbook contains example task definitions used in this tutorial.

7. If you want to test mounting Object Storage buckets to VMs, [create a bucket](https://docs.nebius.com/object-storage/buckets/manage.md).

## Steps

1. Run SkyPilot tasks from the Nebius ML Cookbook:

   * [GPU check](#run-a-gpu-check)
   * [Object Storage check](#run-an-object-storage-check)
   * [InfiniBand™ check](#run-an-infiniband-check)
   * [Training task](#run-a-training-task)

   You can choose to run some or all of these tasks, depending on your use cases.

2. Work with the VMs managed by SkyPilot as part of the tasks:

   * [Monitor SkyPilot clusters and VMs](#monitor-the-skypilot-clusters-and-vms)
   * [Connect to the VMs](#connect-to-the-vms)

If you face issues when you launch tasks or work with the VMs, see the [troubleshooting section](#troubleshoot-issues).

### Run tasks

#### Run a GPU check

The GPU check in this tutorial creates a VM with one NVIDIA® H100 GPU and runs the [NVIDIA System Management Interface](https://docs.nvidia.com/deploy/nvidia-smi/index.html) (`nvidia-smi`) on it. `nvidia-smi` outputs the list of GPUs available on the VM and the list of processes running on the GPUs.

1. Launch the task:

   ```bash theme={null}
   sky launch -c basic-job examples/basic-job.yaml
   ```

2. When SkyPilot displays which resources it is going to create and asks you to confirm the launch, enter `Y` and press **Enter**.

If the launch is successful, the output contains the list of GPUs and processes running on them returned by `nvidia-smi`:

> **Output example**
>
> ```text theme={null}
> ⚙︎ Launching on Nebius eu-north1.
> └── Instance is up.
> ✓ Cluster launched: basic-job.  View logs: sky api logs -l sky-2025-02-27-11-36-07-257438/provision.log
> ⚙︎ Syncing files.
> ✓ Setup detached.
> ⚙︎ Job submitted, ID: 1
> ├── Waiting for task resources on 1 node.
> └── Job started. Streaming logs... (Ctrl-C to exit log streaming; job will not be killed)
> ...
> (task, pid=7059) +-----------------------------------------------------------------------------------------+
> (task, pid=7059) | NVIDIA-SMI 550.127.08             Driver Version: 550.127.08     CUDA Version: 12.4     |
> (task, pid=7059) |-----------------------------------------+------------------------+----------------------+
> (task, pid=7059) | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
> (task, pid=7059) | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
> (task, pid=7059) |                                         |                        |               MIG M. |
> (task, pid=7059) |=========================================+========================+======================|
> (task, pid=7059) |   0  NVIDIA H100 80GB HBM3          On  |   00000000:8D:00.0 Off |                    0 |
> (task, pid=7059) | N/A   29C    P0             70W /  700W |       1MiB /  81559MiB |      0%      Default |
> (task, pid=7059) |                                         |                        |             Disabled |
> (task, pid=7059) +-----------------------------------------+------------------------+----------------------+
> ✓ Job finished (status: SUCCEEDED).
> ```

#### Run an Object Storage check

The [Object Storage](https://docs.nebius.com/object-storage/index.md) check creates a VM and mounts a bucket from your project to it.

1. In `examples/test-cloud-bucket.yaml`, find `source: nebius://my-nebius-bucket` under `file_mounts` and replace `my-nebius-bucket` with the name of your bucket.

2. Launch the task:

   ```bash theme={null}
   sky launch -c test-cloud-bucket examples/test-cloud-bucket.yaml
   ```

3. When SkyPilot displays which resources it is going to create and asks you to confirm the launch, enter `Y` and press **Enter**.

If the launch is successful, the output contains the list of objects in the bucket:

> **Output example**
>
> ```text theme={null}
> ⚙︎ Launching on Nebius eu-north1.
> └── Instance is up.
> ✓ Cluster launched: test-cloud-bucket.  View logs: sky api logs -l sky-2025-03-25-13-42-18-045624/provision.log
> ⚙︎ Syncing files.
>   Mounting (to 1 node): nebius://another-example-bucket -> /my_data
> ✓ Storage mounted.  View logs: sky api logs -l sky-2025-03-25-13-42-18-045624/storage_mounts.log
> ✓ Setup detached.
> ⚙︎ Job submitted, ID: 1
> ├── Waiting for task resources on 1 node.
> └── Job started. Streaming logs... (Ctrl-C to exit log streaming; job will not be killed)
> (setup pid=3963) Setup will be executed on every `sky launch` command on all nodes
> (task, pid=3963) Run will be executed on every `sky exec` command on all nodes
> (task, pid=3963) Do we have data?
> (task, pid=3963) total 4
> (task, pid=3963) drwxr-xr-x 2 ubuntu ubuntu 4096 Mar 25 12:44 lorem-ipsum
> ✓ Job finished (status: SUCCEEDED).
> ```

#### Run an InfiniBand check

The InfiniBand check creates a cluster of two VMs with 8 NVIDIA® H100 GPUs each, connected with InfiniBand, and runs the `ib_send_bw` test from [perftest](https://github.com/linux-rdma/perftest). The test measures bandwidth when sending data between GPUs on different VMs.

1. Launch the task:

   ```bash theme={null}
   sky launch -c infiniband-test examples/infiniband-test.yaml
   ```

2. When SkyPilot displays which resources it is going to create and asks you to confirm the launch, enter `Y` and press **Enter**.

If the launch is successful, the output contains the results of the test:

> **Output example**
>
> ```text theme={null}
> ⚙︎ Launching on Nebius eu-north1.
> └── Instances are up.
> ✓ Cluster launched: infiniband-test.  View logs: sky api logs -l sky-2025-02-27-09-15-19-016219/provision.log
> ✓ Setup detached.
> ⚙︎ Job submitted, ID: 14
> ├── Waiting for task resources on 2 nodes.
> └── Job started. Streaming logs... (Ctrl-C to exit log streaming; job will not be killed)
> ...
> (worker1, rank=1, pid=33870, ip=192.168.0.15) ---------------------------------------------------------------------------------------
> (worker1, rank=1, pid=33870, ip=192.168.0.15)                     Send BW Test
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Dual-port       : OFF            Device         : mlx5_0
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Number of qps   : 1              Transport type : IB
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Connection type : RC             Using SRQ      : OFF
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  PCIe relax order: ON
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  ibv_wr* API     : ON
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  TX depth        : 128
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  CQ Moderation   : 1
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Mtu             : 4096[B]
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Link type       : IB
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Max inline data : 0[B]
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  rdma_cm QPs       : OFF
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  Data ex. method : Ethernet
> (worker1, rank=1, pid=33870, ip=192.168.0.15) ---------------------------------------------------------------------------------------
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  local address: LID 0x1334 QPN 0x0131 PSN 0xcdddde
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  remote address: LID 0x132f QPN 0x0131 PSN 0x90f79b
> (worker1, rank=1, pid=33870, ip=192.168.0.15) ---------------------------------------------------------------------------------------
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  #bytes     #iterations    BW peak[Gb/sec]    BW average[Gb/sec]   MsgRate[Mpps]
> (worker1, rank=1, pid=33870, ip=192.168.0.15)  65536      1000             361.82             361.67               0.689839
> (worker1, rank=1, pid=33870, ip=192.168.0.15) ---------------------------------------------------------------------------------------
> ✓ Job finished (status: SUCCEEDED).
> ```

#### Run a training task

The training task adapts a [tutorial](https://pytorch.org/tutorials/intermediate/ddp_series_minGPT.html) from the PyTorch documentation and its [implementation](https://docs.skypilot.co/en/latest/getting-started/tutorial.html) from the SkyPilot documentation. It creates a cluster of two VMs with 8 NVIDIA® H100 GPUs each, connected with InfiniBand. Then, it uses PyTorch to train a GPT-like model with [Distributed Data Parallel](https://pytorch.org/docs/stable/index.html) on the VMs.

1. Launch the task:

   ```bash theme={null}
   sky launch distributed-training examples/distributed-training-container.yaml
   ```

2. When SkyPilot displays which resources it is going to create and asks you to confirm the launch, enter `Y` and press **Enter**.

If the launch is successful, the output contains training logs:

> **Output example**
>
> ```text theme={null}
> ⚙︎ Launching on Nebius eu-north1.
> └── Instances are up.
> ✓ Cluster launched: distributed-training.  View logs: sky api logs -l sky-2025-02-27-11-27-07-706257/provision.log
> ⚙︎ Syncing files.
> ✓ Setup detached.
> ⚙︎ Job submitted, ID: 1
> ├── Waiting for task resources on 2 nodes.
> └── Job started. Streaming logs... (Ctrl-C to exit log streaming; job will not be killed)
> ...
> ...
> (task, pid=8591) [GPU4] Epoch 10 | Iter 0 | Eval Loss 1.94895
> (task, pid=8591) [GPU7] Epoch 10 | Iter 0 | Eval Loss 1.93593
> (task, pid=8591) [GPU6] Epoch 10 | Iter 0 | Eval Loss 1.95961
> (task, pid=8591) I0227 16:33:56.668000 20640 site-packages/torch/distributed/elastic/agent/server/api.py:879] [default] worker group successfully finished. Waiting 300 seconds for other agents to finish.
> (task, pid=8591) I0227 16:33:56.669000 20640 site-packages/torch/distributed/elastic/agent/server/api.py:932] Local worker group finished (WorkerState.SUCCEEDED). Waiting 300 seconds for other agents to finish
> (task, pid=8591) I0227 16:33:56.670000 20640 site-packages/torch/distributed/elastic/agent/server/api.py:946] Done waiting for other agents. Elapsed: 0.0005085468292236328 seconds
> ✓ Job finished (status: SUCCEEDED).
> ```

> [!NOTE]
>
> The training task also has a single VM (non-distributed) version. To launch it, run `sky launch ai-training examples/ai-training.yaml`.

### Work with the VMs managed by SkyPilot

After you created a cluster and launched a task on it, you can use SkyPilot and Nebius AI Cloud tools to monitor the cluster and connect to its VMs.

#### Monitor the SkyPilot clusters and VMs

To see the statuses of the SkyPilot clusters, run the following command:

```bash theme={null}
sky status
```

You can also [monitor individual VMs](https://docs.nebius.com/compute/monitoring/virtual-machines.md) in the Nebius AI Cloud web console. The VMs' names have the cluster name as the prefix.

#### Connect to the VMs

SkyPilot sets up SSH access to VMs in clusters automatically.

* To connect to the main ("head") VM of the cluster, run `ssh <cluster_name>`. For example:

  ```bash theme={null}
  ssh distributed-training
  ```

* To connect to other VMs ("workers"), run `ssh <cluster_name>-worker<index>`. For example:

  ```bash theme={null}
  ssh distributed-training-worker1
  ```

For more details, see the [SkyPilot documentation](https://docs.skypilot.co/en/latest/running-jobs/distributed-jobs.html#ssh-into-worker-nodes).

### Troubleshoot issues

#### Unavailable resources

When you run `sky launch`, you might get the following error:

```text theme={null}
sky.exceptions.ResourcesUnavailableError: Failed to provision all possible launchable resources. Relax the task's resource requirements: 2x Nebius({'H100': 8})
To keep retrying until the cluster is up, use the `--retry-until-up` flag.
Reasons for provision failures (for details, please check the log above):
Resource                       Reason
Nebius(gpu-h100-sxm_8gpu-      Failed to acquire resources in all zones in
128vcpu-1600gb, {'H100': 8})   eu-north1 for {Nebius({'H100': 8})}.
```

It means that the resources that you specified in the task definition exceed your [Compute quotas](https://docs.nebius.com/compute/resources/quotas-limits.md). For details on how to view and manage quotas, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

#### Connection errors

If SkyPilot commands fail with connection errors, make sure the Managed SkyPilot API Server is running. Check the application status in the Nebius AI Cloud console under  **AI orchestration** → **SkyPilot**. If the server is running, verify your connection by running `sky api login` again with the correct endpoint URL.

#### Authentication errors

If you get authentication errors when running SkyPilot commands, verify that you are connected to the managed API server by running `sky api login` again with the correct endpoint URL.

#### Other issues

If you face problems that are not covered by this tutorial, you can create issues in relevant GitHub repositories:

* [Nebius ML Cookbook](https://github.com/nebius/ml-cookbook/issues)
* [SkyPilot](https://github.com/skypilot-org/skypilot/issues)

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources, so Nebius AI Cloud doesn't charge for them:

* Delete VMs and GPU clusters that SkyPilot created for all tasks in this tutorial:

  ```bash theme={null}
  sky down basic-job test-cloud-bucket infiniband-test distributed-training ai-training
  ```

* [Delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) the bucket that you used in the [Object Storage task](#run-an-object-storage-check).

* If you no longer need the Managed SkyPilot API Server, delete it in the Nebius AI Cloud console. Go to  **AI orchestration** → **SkyPilot**, open the application, go to the **Settings** tab and click **Delete application**.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
