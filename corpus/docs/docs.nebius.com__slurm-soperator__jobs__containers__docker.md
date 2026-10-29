# Running jobs in containers by using Docker

Source: https://docs.nebius.com/slurm-soperator/jobs/containers/docker

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running jobs in containers by using Docker

Soperator clusters allow you to use Docker Engine to run jobs in containers.

## Limitations

When using Docker Engine with Slurm, consider the following limitations:

* **Docker Engine doesn't respect Slurm resource allocations.** Docker may use all resources of a node, regardless of the settings that you specify in `sbatch`. We recommend using [Enroot](https://docs.nebius.com/slurm-soperator/jobs/containers/pyxis-enroot.md) or [other supported container runtimes](https://docs.nebius.com/slurm-soperator/jobs/containers/index.md) to run Docker containers. If you want to use Docker Engine, use the `-N` and `--exclusive` settings to allocate entire nodes to Slurm jobs.
* **Docker containers aren't managed as part of the Slurm job lifecycle.** If a job is canceled, fails or times out, containers started with `srun docker run` continue running. Stop them manually or adjust your job script to stop the containers when the job receives the `SIGTERM` or `SIGKILL` signals.
* **Performance may be degraded without local disks.** If no local disk is available, Docker uses the [VFS storage driver](https://docs.docker.com/engine/storage/drivers/vfs-driver/), which leads to significantly lower performance.

## How to run a Docker container in a Slurm job

1. [Connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) to a login node of your Soperator cluster.

2. Create a batch script that runs your workload in a container.

   For example, create the `test_nccl.sh` script with the following contents:

   ```bash theme={null}
   #!/bin/bash

   #SBATCH -J docker-all-reduce
   #SBATCH -N 2
   #SBATCH --exclusive
   #SBATCH --output=output.log

   srun docker run --device=/dev/infiniband nvidia/cuda:12.8.0-runtime-ubuntu24.04 bash -c '
     echo "Installing additional dependencies..."
     apt update -y && apt install -y wget rdma-core ibverbs-utils

     echo "Installing NCCL tests..."
     wget -P /tmp https://github.com/nebius/slurm-deb-packages/releases/download/nccl_tests_12.8.0/nccl-tests-perf.tar.gz
     tar -xvzf /tmp/nccl-tests-perf.tar.gz -C /usr/bin && rm -rf /tmp/nccl-tests-perf.tar.gz

     echo "Starting all_reduce_perf..."
     /usr/bin/all_reduce_perf -b 512M -e 8G -f 2 -g 8
   '
   ```

   This script pulls a Docker image with Ubuntu and CUDA® toolkit from NVIDIA®, then installs [NVIDIA Collective Communications Library (NCCL) tests](https://github.com/NVIDIA/nccl-tests) and their dependencies, and runs NCCL tests in a Docker container. The script uses the following parameters:

   * `#SBATCH -N` specifies how many nodes to allocate.
   * `#SBATCH --exclusive` specifies that no other jobs may be scheduled on these nodes until this job is completed.
   * `--device=/dev/infiniband` parameter for `docker` allows access to InfiniBand™ from inside Docker containers.

   If your workload needs access to the shared filesystem, you can add the `-v` parameter to make paths from the shared filesystem visible from inside the container:

   ```bash theme={null}
   srun docker run -v </path/in/shared/filesystem>:</container/path> <other_parameters> <docker_image> <command>
   ```

3. Start the job:

   ```bash theme={null}
   sbatch test_nccl.sh
   ```

   The output contains the job ID:

   ```bash theme={null}
   Submitted batch job <job_ID>
   ```

4. When the job is completed, review the contents of `output.log`. The output contains the logs of the container starting up and installing dependencies, followed by the results of NCCL tests. For example:

   ```bash theme={null}
   ==========
   == CUDA ==
   ==========

   CUDA Version 12.8.0
   ...
   Installing additional dependencies...
   Get:3 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64  Packages [1607 kB]
   ...
   Starting all_reduce_perf...
   # nThread 1 nGpus 8 minBytes 536870912 maxBytes 8589934592 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
   #
   # Using devices
   #  Rank  0 Group  0 Pid      1 on 1ae1d8baa190 device  0 [0x8d] NVIDIA H100 80GB HBM3
   #  Rank  1 Group  0 Pid      1 on 1ae1d8baa190 device  1 [0x91] NVIDIA H100 80GB HBM3
   #  Rank  2 Group  0 Pid      1 on 1ae1d8baa190 device  2 [0x95] NVIDIA H100 80GB HBM3
   #  Rank  3 Group  0 Pid      1 on 1ae1d8baa190 device  3 [0x99] NVIDIA H100 80GB HBM3
   #  Rank  4 Group  0 Pid      1 on 1ae1d8baa190 device  4 [0xab] NVIDIA H100 80GB HBM3
   #  Rank  5 Group  0 Pid      1 on 1ae1d8baa190 device  5 [0xaf] NVIDIA H100 80GB HBM3
   #  Rank  6 Group  0 Pid      1 on 1ae1d8baa190 device  6 [0xb3] NVIDIA H100 80GB HBM3
   #  Rank  7 Group  0 Pid      1 on 1ae1d8baa190 device  7 [0xb7] NVIDIA H100 80GB HBM3
   #
   #                                                              out-of-place                       in-place
   #       size         count      type   redop    root     time   algbw   busbw #wrong     time   algbw   busbw #wrong
   #        (B)    (elements)                               (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)
      536870912     134217728     float     sum      -1   2145.0  250.29  438.01      0   2146.1  250.16  437.78      0
     1073741824     268435456     float     sum      -1   4036.8  265.99  465.47      0   4041.8  265.66  464.90      0
     2147483648     536870912     float     sum      -1   7917.9  271.22  474.63      0   7921.6  271.09  474.41      0
     4294967296    1073741824     float     sum      -1    15729  273.06  477.85      0    15710  273.40  478.45      0
     8589934592    2147483648     float     sum      -1    31257  274.81  480.93      0    31278  274.63  480.60      0
   # Out of bounds values : 0 OK
   # Avg bus bandwidth    : 467.303
   ```

## How to run a Docker container in an interactive mode

1. [Connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) to a login node of your Soperator cluster.

2. To run an interactive session on a node and prevent any other allocations on this node, use [salloc](https://slurm.schedmd.com/salloc.html):

   ```bash theme={null}
   salloc --exclusive
   ```

   This command allocates a worker node to a new job and opens a terminal on this node.

   Output example:

   ```bash theme={null}
   salloc: Granted job allocation <job_ID>
   <username>@worker-<number>:~$
   ```

3. Start a Docker container on a worker node:

   ```bash theme={null}
   docker run --rm <other_parameters> <docker_image> <command>
   ```

   The `--rm` parameter ensures that the container is automatically deleted when it exits.

   If your workload needs access to the shared filesystem, use the `-v` parameter to make paths from the shared filesystem visible from inside the container:

   ```bash theme={null}
   docker run --rm -v </shared/filesystem/path>:</container/path> <other_parameters> <docker_image> <command>
   ```

   For multi-node GPU workloads, use the `--device=/dev/infiniband` parameter for `docker` that allows access to InfiniBand from inside Docker containers.

4. After you finish the interactive session and exit, you can see the confirmation that the node is no longer allocated:

   ```bash theme={null}
   exit
   salloc: Relinquishing job allocation <job_ID>
   salloc: Job allocation <job_ID> has been revoked.
   <username>@login-0:~$
   ```

## How to get information about your Docker containers

To list all containers, including the ones that are already finished, [connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-worker-nodes) to a worker node and run the following command:

```bash theme={null}
docker ps -a
```

For more details on Docker commands and parameters, see the [Docker documentation](https://docs.docker.com/reference/cli/docker/container/).

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
