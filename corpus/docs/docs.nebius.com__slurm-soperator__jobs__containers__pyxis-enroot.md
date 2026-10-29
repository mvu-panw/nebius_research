# Running jobs in containers by using Enroot and Pyxis

Source: https://docs.nebius.com/slurm-soperator/jobs/containers/pyxis-enroot

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running jobs in containers by using Enroot and Pyxis

Soperator clusters support Enroot and Pyxis to run jobs in containers:

* [Enroot](https://github.com/nvidia/enroot) is a simple container runtime. It was created by NVIDIA® specifically for machine learning and high-performance computing. Enroot supports Docker images and can execute the same containers, but works better with Slurm. It allows you to pull the images from container registries, such as [Docker Hub](https://hub.docker.com/), [NVIDIA NGC](https://catalog.ngc.nvidia.com/containers) (`nvcr.io`) or [Container Registry](https://docs.nebius.com/container-registry/index.md) by Nebius.
* [Pyxis](https://github.com/NVIDIA/pyxis) is a plug-in for Slurm, which uses Enroot to allow cluster users to run containerized jobs by using the `srun` command with additional `--container-***` parameters.

You can run a Slurm job within a container created from an image that is stored either [in a registry](#how-to-run-a-job-for-a-container-registry-image) or [locally](#how-to-run-a-job-for-a-local-image).

## How to run a job for a container registry image

1. Create the following job called `test.sbatch`:

   ```bash theme={null}
   #!/bin/bash

   #SBATCH -J test
   #SBATCH --output=log.out
   #SBATCH --error=log.out
   #SBATCH --gpus=1

   srun --container-image="nvcr.io#nvidia/tensorflow:23.02-tf1-py3" \
      python -c "import tensorflow as tf; print (tf.__version__)"
   ```

   This job pulls a TensorFlow image from the NVIDIA container registry, starts a container and executes a simple Python script within it.

   Use the `--container-image="<your.container.registry#repository/container:tag>"` parameter for the `srun` command, to specify a container image.

   In Soperator clusters, a container image is first pulled from the registry, then saved to the cluster's shared filesystem. Next, all worker nodes can use this image to start the container, without repeated downloads of the same data from the registry.

   You can disable this default behavior and add the `--container-image-save=""` parameter with an empty value to the `srun` command. In this parameter, you can also set the path where the image is stored in the filesystem: `--container-image-save="<path/to/image>"`.

   For more information about other parameters available for `srun`, see [Pyxis documentation](https://github.com/NVIDIA/pyxis/wiki/Usage).

2. Run the job:

   ```bash theme={null}
   sbatch test.sbatch
   ```

### How to authenticate in a container registry

Docker Hub and NVIDIA NGC container registries are configured by default, and you do not need to authenticate to pull public container images from them.

If you need to pull images from another registry, or to pull private container images, configure credentials in the `~/.config/enroot/.credentials` file:

```bash theme={null}
machine <container_registry_endpoint> login <login> password <password>
```

The password requirements depend on the image:

* To pull a private container image, the password is required. For more information about the login and password, consult the documentation of the selected container registry.
* To pull a public container image from a registry other than Docker Hub or NVIDIA NGC, you can use an arbitrary string instead of a password.

The endpoint for Container Registry by Nebius is `cr.<region_ID>.nebius.cloud`, where `<region_ID>` is the ID of a [Nebius AI Cloud region](https://docs.nebius.com/overview/regions.md); for example, `cr.eu-north1.nebius.cloud`.

For more information, see [Container Registry documentation](https://docs.nebius.com/container-registry/registries/manage.md) and [Enroot documentation](https://github.com/NVIDIA/enroot/blob/master/doc/cmd/import.md#description).

## How to run a job for a local image

> [!WARNING]
>
> You can only use images in the [squashfs](https://www.kernel.org/doc/Documentation/filesystems/squashfs.txt) format (`.sqsh`, `.sqshfs`, `.squashfs`). You can get the images by using the [enroot import](https://github.com/NVIDIA/enroot/blob/master/doc/cmd/import.md) command. Alternatively, they can be saved when you pull the image from the registry by using `--container-image-save="<path>/image.sqshfs"`.

To run a job in a container with a local image, do the following:

1. Create the following job called `test.sbatch`:

   ```bash theme={null}
   #!/bin/bash

   #SBATCH -J test
   #SBATCH --output=log.out
   #SBATCH --error=log.out
   #SBATCH --gpus=1

   srun --container-image="./tensorflow.sqsh" \
      python -c "import tensorflow as tf; print (tf.__version__)"
   ```

   This job starts a container with a local image, then executes a simple Python script within the container.

   Use the `--container-image="<full/path/to/image>"` parameter for the `srun` command, to specify the container image.

   For more information about other parameters available for `srun`, see [Pyxis documentation](https://github.com/NVIDIA/pyxis/wiki/Usage).

2. Run the job:

   ```bash theme={null}
   sbatch test.sbatch
   ```
