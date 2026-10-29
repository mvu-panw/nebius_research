# Running jobs in containers in Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/jobs/containers

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running jobs in containers in Soperator clusters

Soperator enables you to run jobs in containers. Containers allow you to run applications across different cloud providers, in a portable and consistent way. You can create a container image once and then run it in different cloud services. In addition, many widespread solutions are already available in container registries.

Soperator clusters allow you to run jobs in containers by using the following tools:

* [Enroot and Pyxis](https://docs.nebius.com/slurm-soperator/jobs/containers/pyxis-enroot.md)
* [Apptainer](https://docs.nebius.com/slurm-soperator/jobs/containers/apptainer.md)
* [Docker](https://docs.nebius.com/slurm-soperator/jobs/containers/docker.md)

For the best performance, we recommend using Enroot and Pyxis, because Soperator includes performance optimizations for them.
