# NVIDIA Blueprint for virtual screening in Nebius AI Cloud

Source: https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# NVIDIA Blueprint for virtual screening in Nebius AI Cloud

Nebius AI Cloud offers NVIDIA Blueprint for virtual screening as a Kubernetes application. The application is available in the `eu-north1` and `us-central1` [regions](https://docs.nebius.com/overview/regions.md).

## About the Blueprint

[NVIDIA Blueprints](https://build.nvidia.com/blueprints) are pretrained end-to-end reference AI workflows designed for common enterprise use cases. The [NVIDIA Blueprint for generative virtual screening](https://github.com/NVIDIA-BioNeMo-blueprints/generative-virtual-screening) guides researchers through an AI-driven pipeline that designs optimized small molecules efficiently. It orchestrates a suite of GPU-accelerated NIM microservices (including OpenFold2, MSA-Search, GenMol and DiffDock) to predict protein structures, generate drug-like molecules and model their docking without predefined binding pockets. This workflow significantly accelerates hit identification and lead optimization, enabling smarter, faster drug discovery cycles.

Within the deployment, we also deploy JupyterHub along with the Python notebook sample to make experimentation with the Blueprint more accessible.

For more information about deploying the Blueprint and connecting to it, see [Deploying NVIDIA Blueprint for virtual screening in Nebius AI Cloud](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/deploy.md).

## Terms and conditions

This application is provided under a bring-your-own-license model. By deploying this application, you represent and warrant that you hold, and will maintain throughout the use of the application, a valid and sufficient NVIDIA AI Enterprise License. Use of the application without such license is strictly prohibited. If you do not currently possess the required license, please refer to [How to get licenses for NVIDIA Blueprint for virtual screening](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/licenses.md) for available options.

## Getting started

To use NVIDIA Blueprint for virtual screening, [get the licenses](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/licenses.md) and [deploy it](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/deploy.md). After that, you can access it via [JupyterHub](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/deploy.md#how-to-access-the-blueprint-via-jupyterhub) to run the sample notebook.
