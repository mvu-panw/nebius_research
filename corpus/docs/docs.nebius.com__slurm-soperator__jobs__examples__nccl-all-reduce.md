# Running the all-reduce NCCL performance test in Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/jobs/examples/nccl-all-reduce

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running the all-reduce NCCL performance test in Soperator clusters

Soperator includes pre-built [NVIDIA® Collective Communications Library (NCCL) tests](https://github.com/NVIDIA/nccl-tests) that you can use to validate collective communication between GPUs over the available high-performance network and assess network performance in your cluster.

NCCL used in these benchmarks enables communication over NVLink for single-node runs, and over a combination of NVLink and InfiniBand™ for multi-node runs.

There are two versions of NCCL tests included in Soperator: a single-node version (`all_reduce_perf`) and a multi-node version with the `_mpi` suffix (`all_reduce_perf_mpi`). In this article, you will run the `all_reduce_perf_mpi` NCCL test on multiple nodes. The all-reduce operation is important for synchronizing gradients during multi-GPU training, which makes `all_reduce_perf_mpi` useful for evaluating both network and compute resources.

## How to run the test

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md).

2. Create an output directory for Slurm logs:

   ```bash theme={null}
   mkdir -p results
   ```

3. Create an sbatch script for your platform and save it as `nccl_all_reduce.sbatch`:

   **8 × NVIDIA H100/H200**

   ```bash title="nccl_all_reduce.sbatch" theme={null}
   #!/bin/bash

   #SBATCH --job-name=nccl_all_reduce
   #SBATCH --time=30:00
   #SBATCH --output=results/%x-%j.out
   #SBATCH --error=results/%x-%j.out
   #SBATCH --nodes=8
   #SBATCH --gpus-per-node=8
   #SBATCH --ntasks-per-node=8
   #SBATCH --cpus-per-task=16
   #SBATCH --mem=0

   echo "Job ID: ${SLURM_JOB_ID}"
   echo "Start time: $(date -u '+%Y-%m-%d %H:%M:%SZ')"

   export UCX_NET_DEVICES=mlx5_0:1,mlx5_1:1,mlx5_2:1,mlx5_3:1,mlx5_4:1,mlx5_5:1,mlx5_6:1,mlx5_7:1

   export NCCL_IB_QPS_PER_CONNECTION=2
   export NCCL_NVLS_ENABLE=1
   export NCCL_BUFFSIZE=8388608

   srun --mpi=pmix all_reduce_perf_mpi -b 512M -e 16G -f 2 -g 1
   ```

   **8 × NVIDIA B200**

   ```bash title="nccl_all_reduce.sbatch" theme={null}
   #!/bin/bash

   #SBATCH --job-name=nccl_all_reduce
   #SBATCH --time=30:00
   #SBATCH --output=results/%x-%j.out
   #SBATCH --error=results/%x-%j.out
   #SBATCH --nodes=8
   #SBATCH --gpus-per-node=8
   #SBATCH --ntasks-per-node=8
   #SBATCH --cpus-per-task=20
   #SBATCH --mem=0

   echo "Job ID: ${SLURM_JOB_ID}"
   echo "Start time: $(date -u '+%Y-%m-%d %H:%M:%SZ')"

   export UCX_NET_DEVICES=mlx5_4:1,mlx5_5:1,mlx5_6:1,mlx5_7:1,mlx5_8:1,mlx5_9:1,mlx5_10:1,mlx5_11:1

   export NCCL_IB_QPS_PER_CONNECTION=2
   export NCCL_NVLS_ENABLE=1
   export NCCL_BUFFSIZE=8388608

   srun --mpi=pmix all_reduce_perf_mpi -b 512M -e 16G -f 2 -g 1
   ```

   **8 × NVIDIA B300**

   ```bash title="nccl_all_reduce.sbatch" theme={null}
   #!/bin/bash

   #SBATCH --job-name=nccl_all_reduce
   #SBATCH --time=30:00
   #SBATCH --output=results/%x-%j.out
   #SBATCH --error=results/%x-%j.out
   #SBATCH --nodes=8
   #SBATCH --gpus-per-node=8
   #SBATCH --ntasks-per-node=8
   #SBATCH --cpus-per-task=24
   #SBATCH --mem=0

   echo "Job ID: ${SLURM_JOB_ID}"
   echo "Start time: $(date -u '+%Y-%m-%d %H:%M:%SZ')"

   export UCX_NET_DEVICES=mlx5_4:1,mlx5_5:1,mlx5_6:1,mlx5_7:1,mlx5_8:1,mlx5_9:1,mlx5_10:1,mlx5_11:1

   export NCCL_IB_QPS_PER_CONNECTION=2
   export NCCL_NVLS_ENABLE=1
   export NCCL_BUFFSIZE=8388608

   srun --mpi=pmix all_reduce_perf_mpi -b 512M -e 16G -f 2 -g 1
   ```

4. Submit the job:

   ```bash theme={null}
   sbatch nccl_all_reduce.sbatch
   ```

   The examples above assume the job is run on 8 nodes using the `#SBATCH --nodes` directive. To run on a different number of nodes, override this value using the command-line argument when submitting the job: `sbatch --nodes=<node_count> nccl_all_reduce.sbatch`. Slurm uses the command-line value when both are present.
   For more details about running and configuring jobs, see [Running Slurm batch jobs](https://docs.nebius.com/slurm-soperator/jobs/index.md).

## Script structure and configuration

The example scripts include three sections:

1. Slurm configuration parameters
2. Environment variables for NCCL tuning
3. Launch command for the parallel NCCL testing

### Slurm configuration parameters

This section defines job parameters using `#SBATCH` directives. These directives configure job submission options.

For more details, see [Job configuration](https://docs.nebius.com/slurm-soperator/jobs/index.md#job-configuration) and the [SBATCH documentation](https://slurm.schedmd.com/sbatch.html).

* `--job-name`: Job name shown in the `squeue` and `sacct` output.
* `--time`: Job time limit (30 minutes in these examples).
* `--output`, `--error`: File names for the job output and error. You can use pattern substitution, for example: `%x` (job name) and `%j` (job ID).
* `--nodes`: Number of Slurm worker nodes used for the test. You can override this with `sbatch --nodes=<node_count>`.
* `--gpus-per-node`: Number of GPUs per node. The examples use all available GPUs for each platform (for example, 8 GPUs on 8xH200 nodes).
* `--ntasks-per-node`: Number of parallel processes per node. This example uses one process per GPU, so the value matches the number of GPUs (for example, 8). Some ML frameworks instead launch one process per node and handle parallelism internally; if you want to test how such frameworks would work, set this value to `1`.
* `--cpus-per-task`: Number of CPUs per process. In these examples, all CPUs are evenly divided across processes (total cores ÷ number of GPUs). This helps ensure consistent performance and avoids interference from cluster defaults. For one-process-per-node setups, set the value to the total number of CPUs per node. For CPU counts for each platform, see [presets](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).
* `--mem`: Amount of system memory per node. The examples use all available memory (`--mem=0`) to avoid unintended limitations from cluster defaults. You can also set a specific memory amount using units, for example: `--mem=4G`.

### Environment variables for NCCL tuning

This section defines environment variables for NCCL and related parallel libraries.

For more details, see the [NCCL environment variables documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html).

* `UCX_NET_DEVICES`: Comma-separated list of high-speed network interfaces used by the [Unified Communication X](https://openucx.org/documentation/) (UCX) library. UCX is commonly used as a transport layer in [Message Passing Interface](https://www.mpi-forum.org/) (MPI) implementations and other libraries (for example, [NVIDIA Inference Xfer Library](https://github.com/ai-dynamo/nixl) — NIXL).
  Use platform-specific values of 8 specific InfiniBand ports to achieve maximum bandwidth. Otherwise, use an Ethernet interface with IP connectivity across all worker nodes, for example: `UCX_NET_DEVICES=eth0`.
* NCCL tuning variables:

  * `NCCL_IB_QPS_PER_CONNECTION=2`: Sets the number of InfiniBand queue pairs per connection to 2 (instead of the default 1).
    Using more queue pairs may improve throughput by increasing routing entropy.
  * `NCCL_NVLS_ENABLE=1`: Enables NVLink SHARP support, allowing the NVSwitch to offload part of the computation work. This option is typically enabled by default, but may be disabled in some container images.
  * `NCCL_BUFFSIZE=8388608`: Sets the size of the internal NCCL communication buffer to 8 MB. A larger buffer can help improve performance in some scenarios by allowing more data to be processed in each communication step.

### Launch command configuration

This section uses the `srun` command to start the application in parallel across multiple nodes and processes, and defines arguments for both `srun` and NCCL tests.

* `srun --mpi=pmix`: Selects the [Process Management Interface for Exascale](https://pmix.org/) (PMIx) used to exchange rank information between Slurm's launcher (`srun`) and the MPI library (in the case of `all_reduce_perf_mpi`, [Open MPI](https://docs.open-mpi.org/)).
* `all_reduce_perf_mpi`: Runs the NCCL benchmark for the all-reduce operation, built with support for multi-node execution. NCCL also provides similar benchmarks for other collective operations like AllGather and ReduceScatter.

After the executable name, the following [NCCL test arguments](https://github.com/NVIDIA/nccl-tests#arguments) are used:

* `-b 512M`: Sets the minimum message size, meaning the test begins with messages of 512 MB.
* `-e 16G`: Defines the maximum message size, so the test will go up to 16 GB.
* `-f 2`: Specifies the multiplication factor, so each step doubles the message size (for example, 512 MB → 1 GB → 2 GB, etc.).
* `-g 1`: Indicates that each thread will use 1 GPU.
* `-t 1`: Sets the number of threads per process to 1.

## How to validate the results

When the job finishes, it saves both the standard output and standard error to a file named `results/nccl_all_reduce-<job_ID>.out`. A successful run should:

* Complete without errors
* Show `# Out of bounds values : 0 OK`
* Show increasing bus bandwidth (`busbw`) as the collective message size grows. In most cases, `busbw` will reach a stable peak bandwidth at larger collective operation sizes.

### Example output

This example was generated on a cluster of 8 virtual machines, each equipped with 8 NVIDIA H200 GPUs:

```text theme={null}
#  Rank  0 Group  0 Pid 121061 on   worker-0 device  0 [0000:8d:00] NVIDIA H200
...
#  Rank 63 Group  0 Pid  89331 on  worker-13 device  7 [0000:b7:00] NVIDIA H200
#
#                                                              out-of-place                       in-place
#       size         count      type   redop    root     time   algbw   busbw #wrong     time   algbw   busbw #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)
   536870912     134217728     float     sum      -1   3489.1  153.87  302.94      0   3343.1  160.59  316.16      0
  1073741824     268435456     float     sum      -1   6060.2  177.18  348.82      0   6061.9  177.13  348.72      0
  2147483648     536870912     float     sum      -1    11523  186.36  366.89      0    11799  182.00  358.32      0
  4294967296    1073741824     float     sum      -1    22312  192.49  378.97      0    22410  191.65  377.31      0
  8589934592    2147483648     float     sum      -1    44596  192.62  379.22      0    44542  192.85  379.67      0
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 355.703
#
```

> [!NOTE]
>
> The values above are provided for illustrative purposes. Actual results may vary depending on factors such as hardware or system configuration.

The result file begins with a header that includes metadata about the run, such as the NCCL tests version, NCCL library version, the list of GPUs used and the rank assigned to each GPU on every allocated worker node. This is followed by multiple lines, with one line per collective message size.

Each line contains several fields describing the test configuration and results for that message size, including:

* Size of the exchange (in bytes)
* Element count (based on the data type)
* Data type (for example, floating point)
* Reduction operation (for example sum)
* Rank-related information

For each message size, the test runs in two modes:

* Out-of-place, where input and output buffers are separate
* In-place, where input and output share the same buffer

For each iteration of the test, three metrics are reported:

* **Time:** The duration of a single collective operation iteration, measured in microseconds (μs).
* **Algorithm bandwidth** (`algbw`): The size of the input array for collective operation divided by time. Shows how fast one iteration completes based on the data size.
* **Bus bandwidth** (`busbw`): The algorithm bandwidth corrected for the number of communicating ranks to better estimate the peak hardware bandwidth. Due to this correction and the large speed difference of NVLink and InfiniBand, the final bus bandwidth value may not accurately reflect true hardware bandwidth. For example, in some scenarios, such as two-node runs that involve both NVLink and InfiniBand, the `busbw` value can overestimate the load on InfiniBand.

`Avg bus bandwidth` is the average of all `busbw` values reported across the different message sizes. When interpreting or comparing this average, consider the range of message sizes used in the test (defined by the `-b`, `-e` and `-f 2` arguments, and visible in the `size` column). Smaller message sizes typically result in lower bus bandwidth, while larger sizes reach higher bandwidth. As a result, the average can vary significantly depending on the size range included in the test.

For more details about the test and understanding its results, see [NCCL tests documentation](https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md).

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
