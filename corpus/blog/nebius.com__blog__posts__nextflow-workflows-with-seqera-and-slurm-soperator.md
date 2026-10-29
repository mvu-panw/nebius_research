# Running Nextflow workflows with Seqera Platform and Slurm on Nebius AI Cloud

Source: https://nebius.com/blog/posts/nextflow-workflows-with-seqera-and-slurm-soperator

Skip to main content

# IntroductionIntroduction

As an example, we will be performing protein structure prediction using the Chai-1 molecular structure prediction method via the nf-chai POC workflow to predict folding of sequences in the Critical Assessment of Techniques for Protein Structure Prediction (CASP15) competition.

We’ll dive into:

- 

Seqera Platform, an orchestrator for Nextflow, enabling easy deployment of scalable and reproducible scientific workflows using software containers across all major cloud environments and HPC environments.

- 

Soperator, a Kubernetes operator that manages Slurm clusters dynamically, bringing Kubernetes' scalability to HPC workloads.

# Why combine Seqera platform and Soperator?Why combine Seqera platform and Soperator?

### Seqera — the best place to run NextflowSeqera — the best place to run Nextflow

Seqera Platform, developed by the creators of Nextflow, accelerates scientific development by integrating data, code, computing, and environments, empowering researchers to develop, deploy, and scale bioinformatics pipelines faster. Key features include:

- Centralized pipeline management and monitoring

- Multi-cloud workflow execution capabilities

- Built-in versioning and configuration management

- Reproducible workflow environments

- Simplified deployment across diverse compute environments

### Soperator — Slurm operator for KubernetesSoperator — Slurm operator for Kubernetes

Soperator brings modern cloud capabilities to HPC workloads:

- Automated Slurm cluster provisioning in Kubernetes

- Easy scaling of Slurm worker nodes to help manage costs

- Native Docker support for containerized workflows

- Advanced GPU health monitoring and failure recovery

- Shared filesystem across cluster nodes

### Why this combination?Why this combination?

The integration of Seqera and Soperator creates a powerful environment particularly suited for bioinformatics workflows:

- Seamless orchestration: Seqera manages workflow logic, while Soperator handles infrastructure

- Full containerization: Unlike traditional Slurm deployments, Soperator-based Slurm provides native Docker support

- High availability: Kubernetes' self-healing capabilities ensure workflow reliability

# Implementation guideImplementation guide

### PrerequisitesPrerequisites

- Nebius AI Cloud account

- Seqera Platform account

- Basic familiarity with Nextflow and Slurm

### Using Soperator to provision a Slurm clusterUsing Soperator to provision a Slurm cluster

Soperator, Slurm operator for Kubernetes, bridges the gap between modern cloud-native capabilities of K8s and Slurm’s high-performance scheduling, creating a dynamic, scalable HPC solution. Designed to simplify the deployment of Slurm clusters, Soperator offers key features including shared root filesystems, automated health checks, and easy scaling. These ensure automated resource management while maintaining a familiar Slurm user experience.

How we developed Soperator — a Kubernetes operator by Nebius for Slurm

Installation overview

While setting up Soperator is fairly straightfoward, it does require some familiarity with Infrastructure as code (IaC) tools, such Terraform. Below is the summary of the steps you’d need to perform in order to install Soperator on Nebius AI Cloud platform. The detailed step-by-step guide can be found in this GitHub repository.

- Install Terraform, kubectl, and Nebius’ CLI.

- Define cluster parameters (e.g., compute resources and storage options) in configuration files.

- Use Terraform to configure and deploy your Kubernetes and Slurm clusters.

Aternatively, if you do not wish to follow the above steps, Nebius provides managed Soperator deployments.

Once installed, you can connect with your Slurm cluster via SSH:

$ ssh root@<slurm cluster ip> 

Here we can see all nodes available in the Slurm cluster (3 in our test cluster):

$ root@login-0:~# sinfo
PARTITION AVAIL TIMELIMIT NODES STATE NODELIST
main* up infinite 3 idle worker-[0-2] 

Configuring the cluster

- Creating new Linux users:

$ createuser <username> 

This process happens on the shared root filesystem, so you only need to run it once on the login node — the user will be immediately available on all nodes.

- Installing software packages

$ apt install cowsay

Just like with user creation, you only need to run this command once on the login node.

- Since it’s a Slurm cluster, you can submit regular Slurm jobs with sbatch and srun commands.

Later on in this blog post we will use Seqera to submit Nextflow pipelines with 1000s of containerized Slurm jobs to the cluster for us.

- Finally, we will install Java, Nextflow and apptainer on the cluster, since we will require these tools to run Nextflow via Seqera.

apt update
apt install default-jdk
curl -s https://get.nextflow.io | bash
apt install -y ./apptainer_1.3.5_amd64.deb

Resource monitoring

This deployment also comes with pre-built dashboards out of the box to monitor e.g.

- Hardware system metrics (GPU/CPU/RAM/etc utilization)

Click to expand

- Kubernetes metrics (node availability, pod states. etc)

Click to expand

- Slurm metrics (worker node states, number of jobs and their status over time, etc).

Click to expand

### Setting up a Slurm compute environment on SeqeraSetting up a Slurm compute environment on Seqera

Now that our Slurm cluster on Nebius is operational and has all necessary tools installed, we can set up access to the Slurm cluster in our Seqera Platform workspace via a compute environment (CE). For detailed information on how to get started with Seqera, please visit this guide. For working with SSH-based Slurm clusters, we recommend setting up managed identities in Seqera to preserve user identity and provide improved security. A detailed walkthrough on how to setup managed identities can be found here.

💡 You will need to be the owner of the organization on Seqera to follow the setup guide for managed identities.

Once managed identities are configured, we can create a Slurm compute environment (CE) in our workspace by going to “Compute Environments” —> “Add compute environment” and selecting “Slurm Workload Manager” as the platform and “Managed identity cluster” for credentials. The information for the managed identities will be prefilled for us based on the IP and port information entered under managed identities at the organization level. We specify the work directory where Nextflow will write all temporary work files and specify the head and compute queue names. The head queue will be where our main Nextflow job will run and submit compute jobs to the Slurm scheduler for us. We finish setting up the CE by clicking “Add”, which will create the compute environment and bring us back to the main CE page.

Click to expand

Click to expand

### Testing the compute environmentTesting the compute environment

We are now ready to launch Nextflow pipelines on our Soperator Slurm cluster via Seqera. Note that pipeline submission on Seqera can be made via the GUI interface, Seqera Platform API, CLI, or our Python wrapper around the CLI called seqerakit. In this blog post, we will perform all actions via the graphical user interface on seqera.io for simplicity. As a first test, we will run a small test using the nextflow-io/hello pipeline to make sure our setup is working. In our Launchpad, we click on “Add pipeline”, select our Slurm CE as the compute environment, and add this as the pipeline to launch and hit the “Launch” button. This will launch a run of the hello Nextflow pipeline on our Slurm CE. If we go to the run page for this submission, we should see the run kick-off and finish very quickly with 4 succeeding tasks. Great, we are ready to launch real workloads with Nextflow pipelines on our Slurm cluster now.

Click to expand

### Running nf-chai on Slurm via Seqera PlatformRunning nf-chai on Slurm via Seqera Platform

To showcase compute usage with Seqera and Nextflow on Slurm, we will run a POC pipeline, nf-chai, which implements the state of the art Chai-1 model for molecular structure prediction. Note that this represents a very simple, one process pipeline, which parallelizes running Chai-1 structure prediction in a containerized environment, without any other processes in the pipeline. Nextflow enables you to build data analysis pipelines that can enable data flow through much more complex workflows while providing high scalability. An example of a more complex pipeline for running multiple structure prediction algorithms is the nf-core/proteinfold pipeline, which is showcased on Seqera here: Protein structure prediction with Seqera. To run Nextflow pipelines on our Slurm cluster, we will use Apptainer as our container engine, as this allows us to easily share apptainer images between nodes.

To efficiently run nf-chai on our Slurm cluster, we will perform two more steps directly on the Slurm cluster. First, we will pre-download the apptainer image to a specified location using the following command:

# This will download the apptainer image in the current directory
apptainer pull community.wave.seqera.io-library-gcc_linux-64_python_cuda_pip_chai_lab-44cb323409492b49.img docker://community.wave.seqera.io/library/gcc_linux-64_python_cuda_pip_chai_lab:44cb323409492b49

Next, we will pre-download the reference weights used by Chai-1, to make them available to all workflow tasks. If we don’t do this beforehand, each task would waste time downloading files to the task work directory, instead of symlinking them in, ultimately slowing down our workflow execution. The weights for Chai-1 can be pre-downloaded using the following python command created by a community member on the Chai-1 Github issue board. Make sure to set export CHAI_DOWNLOADS_DIR=[chai1_weights_target_dir] to the directory where you want to store the weights and that you have the chai_lab package installed in your python environment.

from chai_lab.utils.paths import chai1_component, downloads_path
import chai_lab.utils.paths as paths
from transformers import EsmTokenizer, EsmModel 

components = ["feature_embedding", "token_embedder", "trunk", "diffusion_module", "confidence_head"]

#download model weights
for component in components:
chai1_component(component + ".pt")

#download cached rdkit conformers
paths.cached_conformers.get_path()

#download ESM tokenizer and model
esm_cache_folder = downloads_path.joinpath("esm")
model_name = "facebook/esm2_t36_3B_UR50D"
tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=esm_cache_folder)
model = EsmModel.from_pretrained(model_name, cache_dir=esm_cache_folder)

Now we are ready to configure and launch nf-chai. Let’s head back to Seqera and add nf-chai as a pipeline from here. For the purposes of this blog post, we will be running release 0.2.1. We need to configure a couple of parameters for a successful execution:

- Define where we want to store our results (outdir)

- Point to our pre-downloaded weights dir on the cluster (weights_dir)

- Add cluster configuration option to the Nextflow config block (Advanced settings):

process {
clusterOptions = '--gres=gpu:1'  
}

- Add the apptainer cache dir environment variable to the pre-run script block (“Advanced settings”). This is the location where we downloaded the apptainer image previously.

NXF_APPTAINER_CACHEDIR = [folder where apptainer images are stored]

 - type: 'blog-yfm-block'

column: 'left'

resetPaddings: true

paddingBottom: s

text: |

- type: 'blog-yfm-block'

column: 'left'

resetPaddings: true

paddingBottom: m

text: |

Click to expand

For input data, we use the CASP15 competition dataset here as an example set of protein sequences to predict using nf-chai. We downloaded the data from CASP15 to our cluster with:

wget https://predictioncenter.org/download_area/CASP15/sequences/casp15.seq.txt

We prepared sequences for prediction by Chai-1 by adding entity type protein| to the fasta IDs and filtered out sequences longer than 2047 amino acids, as Chai-1 cannot currently handle predictions above this size. We run nf-chai using our Soperator Slurm cluster with 3 worker nodes. Please note that we are running Chai-1 in single sequence mode without multiple-sequence alignment (MSAs) for demonstration purposes here, and prediction quality will likely be lower compared to using Chai-1 with MSAs. We define our input and output data locations for the pipeline run and can finally launch nf-chai. We can now monitor the pipeline starting and jobs going from submitted to running to succeeded status. If we want to, we can also check job status on the Slurm cluster directly with squeue but, we generally don’t need to do this because Seqera will record and report run statistics for us.

Click to expand

Our nf-chai pipeline run successfully predicted the structures of 84 protein sequences using 24 GPUs in parallel at any given point. We have made all of the results (Chai-1 produces 5 predictions per sequence = 420 structure predictions) available in this Github repository for you to download and explore.

3D rendering of protein structure prediction results for target T1105 of CASP15 predicted with Chai-1 via nf-chai

# ConclusionConclusion

Combining Nebius’ Soperator with Seqera Platform for deploying your Nextflow pipelines provides great benefits. Soperator-based Slurm provides you with simplified scaling and cluster management experience. Additionally, it is packed with all the necessary drivers and components, making it GPU-ready out of the box. Slurm executor provides a familiar and friendly interface for executing Nextflow workflows and allows easy configuration of compute environments with Seqera. Seqera enables visibility for data processing operations within organizations and facilitates configuration, deployment and optimization of pipelines for execution on Soperator, ensuring stability and reproducibility of your Nextflow runs.

## Explore Nebius

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Kim
Cloud Solutions Consultant

Florian Wünnemann
Bioinformatics Engineer at Seqera

Contents

- 

Introduction

- 

Why combine Seqera platform and Soperator?

- Seqera — the best place to run Nextflow

- Soperator — Slurm operator for Kubernetes

- Why this combination?

- 

Implementation guide

- Prerequisites

- Using Soperator to provision a Slurm cluster

- Setting up a Slurm compute environment on Seqera

- Testing the compute environment

- Running nf-chai on Slurm via Seqera Platform

- 

Conclusion

## See also

### 

Explaining Soperator, Nebius’ open-source Kubernetes operator for Slurm

We’ve built an open-source Kubernetes operator that runs and manages Slurm clusters as Kubernetes resources. From this article, you’ll find out how the community tackled this task previously and the details of the architecture of our solution, which we named Soperator.

September 24, 2024
10 mins to read

### 

Slurm vs Kubernetes: Which to choose for model training

Scaling your machine learning workloads will eventually require resource orchestration. This article compares the most popular options today — Slurm and Kubernetes, covering their design origins, ML adaptations and other factors to consider.

May 29, 2024
13 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
