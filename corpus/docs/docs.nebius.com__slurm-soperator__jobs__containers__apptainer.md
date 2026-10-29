# Running jobs in containers by using Apptainer

Source: https://docs.nebius.com/slurm-soperator/jobs/containers/apptainer

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running jobs in containers by using Apptainer

Soperator clusters allow you to run jobs in containers by using [Apptainer](https://apptainer.org/). Apptainer is a secure and portable container runtime compatible with Slurm. It is designed for high-performance computing (HPC) and scientific computing. Apptainer was formerly known as Singularity and supports the same `.sif` container image format.

> [!NOTE]
>
> Apptainer may provide lower performance than other [supported tools for running jobs in containers](https://docs.nebius.com/slurm-soperator/jobs/containers/index.md). We recommend using container runtimes that Soperator has performance optimizations for, such as Enroot.

To run a containerized job by using Apptainer:

1. [Connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) to a login node of your Soperator cluster.

2. Install Apptainer:

   ```bash theme={null}
   sudo add-apt-repository -y ppa:apptainer/ppa
   sudo apt update
   sudo apt install -y apptainer
   ```

3. Verify that the installation was successful by checking the Apptainer version:

   ```bash theme={null}
   apptainer --version
   ```

   Expected output:

   ```bash theme={null}
   apptainer version 1.3.4
   ```

4. Use `srun` to pull a container image and convert it to the `.sif` format:

   ```bash theme={null}
   srun apptainer pull cuda_image.sif docker://nvidia/cuda:12.4.1-cudnn-devel-rockylinux8
   ```

   The `pull` command can download or convert a container from the specified URL. In particular, you can pull an image from Docker Hub or another container registry. For more information, see the [Apptainer documentation](https://apptainer.org/docs/user/main/cli/apptainer_pull.html).

5. Create the `apptainer_job.sh` script with the following contents:

   ```bash theme={null}
   #!/bin/bash
   #SBATCH --job-name=apptainer_job
   #SBATCH --gres=gpu:8
   #SBATCH --output=output.log
   #SBATCH --error=error.log
   apptainer exec --nv cuda_image.sif nvidia-smi
   ```

   This script uses the following parameters:

   * `--gres=gpu:8` requests 8 GPUs for the job.
   * `--nv` enables NVIDIA® GPU support inside the container.

   This script runs the [nvidia-smi monitoring utility by NVIDIA](https://docs.nvidia.com/deploy/nvidia-smi/index.html) to print information on GPU visibility inside the container.

   To run custom workloads, replace `cuda_image.sif` with a different container image. Also, replace `nvidia-smi` with the required application or command. For example:

   ```bash theme={null}
   apptainer exec --nv my_custom_image.sif python train.py
   ```

   Ensure that `my_custom_image.sif` contains Python and all other dependencies of `train.py`.

6. Run the job:

   ```bash theme={null}
   sbatch apptainer_job.sh
   ```

   The output contains the following confirmation:

   ```bash theme={null}
   Submitted batch job <job_ID>
   ```

7. When the job completes, check the logs. The `output.log` file contains the list of all 8 GPUs that are available for usage inside the container:

   ```bash theme={null}
   cat output.log
   Wed Apr 16 13:55:48 2025
   +-----------------------------------------------------------------------------------------+
   | NVIDIA-SMI 550.54.15              Driver Version: 550.54.15      CUDA Version: 12.4     |
   |-----------------------------------------+------------------------+----------------------+
   | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
   | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
   |                                         |                        |               MIG M. |
   |=========================================+========================+======================|
   |   0  NVIDIA H100 80GB HBM3          On  |   00000000:8D:00.0 Off |                    0 |
   | N/A   29C    P0             73W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   1  NVIDIA H100 80GB HBM3          On  |   00000000:91:00.0 Off |                    0 |
   | N/A   27C    P0             67W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   2  NVIDIA H100 80GB HBM3          On  |   00000000:95:00.0 Off |                    0 |
   | N/A   29C    P0             67W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   3  NVIDIA H100 80GB HBM3          On  |   00000000:99:00.0 Off |                    0 |
   | N/A   27C    P0             71W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   4  NVIDIA H100 80GB HBM3          On  |   00000000:AB:00.0 Off |                    0 |
   | N/A   29C    P0             70W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   5  NVIDIA H100 80GB HBM3          On  |   00000000:AF:00.0 Off |                    0 |
   | N/A   27C    P0             70W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   6  NVIDIA H100 80GB HBM3          On  |   00000000:B3:00.0 Off |                    0 |
   | N/A   29C    P0             69W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+
   |   7  NVIDIA H100 80GB HBM3          On  |   00000000:B7:00.0 Off |                    0 |
   | N/A   26C    P0             68W /  700W |       0MiB /  81559MiB |      0%      Default |
   |                                         |                        |             Disabled |
   +-----------------------------------------+------------------------+----------------------+

   +-----------------------------------------------------------------------------------------+
   | Processes:                                                                              |
   |  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
   |        ID   ID                                                               Usage      |
   |=========================================================================================|
   |  No running processes found                                                             |
   +-----------------------------------------------------------------------------------------+
   ```
