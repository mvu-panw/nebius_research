# Running NVIDIA NIM and NVIDIA Blueprint in Nebius AI Cloud

Source: https://nebius.com/blog/posts/running-nvidia-nim-and-blueprint-on-nebius-ai-cloud

Skip to main content

For healthcare and life sciences AI teams, quickly setting up the full AI stack is critical. Teams can achieve this goal with NVIDIA NIM™, a set of portable, high-performance microservices that deliver fast, secure and easy deployment of AI model inference.

In Nebius AI Cloud, NVIDIA Enterprise licensing is already built in. This licensing provides access to NVIDIA AI Enterprise, a cloud-native suite of software tools, libraries and frameworks designed to deliver optimized performance, robust security and stability for production AI deployments. It also includes NVIDIA NIM, which empowers research teams to rapidly and securely run biological AI models, enabling them to concentrate fully on scientific discovery.

In this blog, we will take a look at how teams can deploy the four NVIDIA NIMs available now in the platform with a few clicks, how they can be consumed via their API and how they can fit into larger scientific workflows. It also covers NVIDIA Blueprint for virtual screening in drug discovery, which turns folding, molecule generation and docking into a ready workflow shortly after deployment.

# What are NVIDIA NIM microservices and why do they matter?What are NVIDIA NIM microservices and why do they matter?

NVIDIA NIM, part of the NVIDIA AI Enterprise software suite, is a set of easy-to-use microservices designed for secure, reliable deployment of high-performance AI model inferencing. These prebuilt containers support a broad spectrum of AI models — from open-source community models to NVIDIA AI foundation models, as well as custom AI models. NIM microservices are deployed with a single command for easy integration into enterprise-grade AI applications using standard APIs and just a few lines of code. In healthcare and life sciences, this translates to workflows such as structure prediction, molecule generation and sequence modeling, where these packaged services remove the need for custom infrastructure.

NIM microservices are critical for health and life sciences organizations, but it can take a lot of effort when teams deploy them on their own; it means handling container builds, CUDA versions, dependency management and model-specific environment configurations.

A therapeutic discovery AI team at a biotech startup folds proteins, explores chemical space around a lead compound or evaluates docking scores at scale. They usually have AI and scientific expertise, but most of the time that doesn’t include infrastructure. Configuring the models can take days, and pulling in the right licenses is another hurdle. This slows down experiments and increases cost.

In Nebius AI Cloud, all the above are taken care of. The selected NIM is automatically deployed with the correct GPU configuration and exposes a predictable endpoint.

Nebius AI Cloud currently supports four NIM microservices from the NVIDIA BioNeMo family; Boltz-2, MolMIM, Evo2-40B and GenMol. Each covers a different part of digital biology and chemistry workflows.

The Enterprise license allows you to use the model both for research and in production environments, covers commercial use and includes access to NVIDIA Enterprise Support through the Nebius support team. You do not need to bring your own license or provide an API key. Everything is handled automatically as part of your deployment.

# Deploying NIM in Nebius AI CloudDeploying NIM in Nebius AI Cloud

Deploying a NIM in Nebius is simple. Go to the Nebius console, open the Applications section and choose a model. Click Deploy Application, select your region (for example eu-north1 or us-central1) and pick your GPU configuration.

After selecting a NIM, Nebius takes care of the rest. It pulls the right container image from the Nebius NVIDIA registry, configures the GPUs and exposes the API endpoint within a few minutes. The available GPU options are selected to meet each model’s minimum requirements. For example, you won’t see a single NVIDIA H100 GPU option for Evo2-40B because it requires more memory. However, selecting a larger configuration should generally yield smoother runs and faster inference.

Here’s what the deployment looks like in the console:

Once your NIM is deployed, the connection details are shared back, including your public endpoint and the credentials you created during setup. You can use this information to send API requests directly to your deployed model. The URL format looks like this:

https://<username>:<password>@<endpoint>/<path>

- <username> and <password> are the credentials you set during deployment.

- <endpoint> is the exposed service URL.

- <path> is the API resource you want to call, such as /generate or /embedding.

Please note that each NIM has its own way of handling requests and returning results. You’ll see the specific format for your model once you deploy it. For more details and examples, refer to the Nebius documentation.

# Example of working with a NIM via Jupyter notebookExample of working with a NIM via Jupyter notebook

Now that MolMIM is up and running, let’s open a Jupyter notebook and actually play with it. This is where you get to see the model generate and optimize molecules step by step.

You can run the notebook in two ways: either locally on your machine, or inside a container or VM running in Nebius. Both options work the same, as long as your notebook can reach the MolMIM endpoint.

If you head to NVIDIA’s digital-biology-examples repository, you’ll find the MolMIM notebook.

We’re going to use that exact notebook, just with one small adjustment so it connects to your Nebius deployment instead of a local Docker container.

In the section that defines the NIM connection, look for this part:

nim_host = "localhost"
port = "8000"
sampling_url = f"http://{nim_host}:{port}/sampling"
hidden_url = f"http://{nim_host}:{port}/hidden"
decode_url = f"http://{nim_host}:{port}/decode"

Replace it with:

# Nebius MolMIM endpoint (basic auth in URL)
nim_host = "<host>" # update this to the app endpoint without http://, https:// and forward slashes
username = "<username>" # update this to username that is set on deployment
password = "<password>" # update this to password that is set on deployment
NIM_url = f"https://{username}:{password}@{nim_host}"
sampling_url = f"{NIM_url}/sampling"
hidden_url = f"{NIM_url}/hidden"
decode_url = f"{NIM_url}/decode"

# Optional: check if your NIM is ready
!curl {NIM_url}/v1/health/ready

That’s all you need to change. The rest of the notebook stays exactly as NVIDIA wrote it. Once you run it, the notebook will connect to your deployed MolMIM NIM and start generating molecules around your seed compound.

# NVIDIA Blueprint for virtual screening in drug discoveryNVIDIA Blueprint for virtual screening in drug discovery

Once you get comfortable deploying and using NIM microservices with Nebius AI Cloud, you might want to see how these models can work together in a larger workflow. NVIDIA Blueprints make that possible. They are comprehensive reference workflows built with NVIDIA AI Enterprise libraries, SDKs and microservices. Each blueprint includes reference code, deployment tools, customization guides and a reference architecture to speed up deployment of AI solutions.

For AI teams in healthcare and life sciences, the NVIDIA Blueprint for virtual screening in drug discovery is the one to look at. It is a containerized workflow that folds proteins, generates small molecules and docks them. The entire workflow runs on GPUs and ships with an interactive JupyterHub environment so you can poke at it right after deployment. The Blueprint uses four NIM microservices under the hood: MSA-Search, OpenFold2, GenMol and DiffDock. You start with a sequence and end with a ranked list of candidate binders.

The idea behind it is simple. Drug discovery is a long process of narrowing down an enormous chemical space, and this Blueprint speeds that up by combining several GPU microservices into one automated workflow. It starts with MSA-Search, which finds homologous sequences and provides evolutionary context for OpenFold2, the model that predicts the 3D protein structure. Once the structure is ready, GenMol designs new small molecules that could bind to it and DiffDock evaluates how those molecules might fit.

Everything is linked through a single notebook, so you can run the full workflow in one place, tweak parameters and rerun without dealing with setup or infrastructure.

### LicensingLicensing

The Blueprint uses a bring-your-own-license model, which means you’ll need a valid NVIDIA Enterprise license to deploy it. If you need help obtaining a valid license, check the Nebius licensing guide for detailed instructions and available options.

# Deploying NVIDIA Blueprint in NebiusDeploying NVIDIA Blueprint in Nebius

You can deploy the NVIDIA Blueprint for virtual screening directly from the Nebius AI Cloud web console. The setup usually takes around two to three hours, because the application downloads large MSA databases and model files during installation.

This application can only be installed on an existing Managed Service for Kubernetes cluster. Before installation, make sure your cluster is prepared:

- 

Create a Managed Kubernetes cluster with the public endpoint enabled.

- 

Create a node group with at least four NVIDIA GPUs.

- 

Install the NVIDIA GPU Operator and NVIDIA Device Plugin on the cluster.

Once your cluster is ready, open the Applications section in the Nebius console. Under Applications for Managed Service for Kubernetes, find NVIDIA Blueprint for virtual screening and click Deploy. Make sure you select the cluster you prepared.

You’ll be asked to configure the following settings:

- 

Application name and Namespace: choose unique identifiers for your deployment.

- 

NGC API key: generate one from the NGC Console.

- 

If you don’t already have a key:

- 

Go to the NVIDIA NGC website.

- 

Sign in or create an account.

- 

Visit build.nvidia.com and click Generate API Key.

- 

Copy the key and paste it in the deployment configuration.

- 

Disk size: choose at least 2 TB. The Blueprint downloads large datasets, so pick a size that fits your workflow.

- 

JupyterHub admin password: click Generate to create a secure password, copy it and confirm that you saved it.

- 

JupyterHub accessibility: select a way to access the JupyterHub cluster:

- ClusterIP for access by port forwarding.

- LoadBalancer for internet access via IP or port forwarding.

Click Deploy Application when you’re done.

Nebius will now install all required components, download the MSA databases, pull model containers and bring up JupyterHub. When the status changes to Deployed, the application is ready. You can then follow the connection instructions in the console to open JupyterHub and start using the environment.

### Running the workflowRunning the workflow

Open JupyterHub and sign in with the credentials you set during deployment. Launch the sample notebook and follow the steps it provides. It walks you through the full workflow and should run without any changes. You will see outputs and visuals as it runs, and all intermediate files are saved to persistent storage.

Everything in the Blueprint is a microservice, which makes it easy to experiment. You can tune GenMol’s generation parameters, try different scoring functions, or insert your own scripts in the notebook. You stay inside the same Nebius cluster the whole time, so there is no juggling of environments.

# Cleaning upCleaning up

When you are done, you can clean up resources directly from the console.

Delete the Blueprint deployment, remove any NIM microservices you launched for testing and stop your workspaces if you are not using them. Your results stay saved in object storage if you want to come back later.

# Wrapping UpWrapping Up

With NVIDIA NIM and NVIDIA Blueprint for virtual screening running in Nebius AI Cloud, you can start from a protein sequence and end up with docked molecules, all without worrying about infrastructure or setup.

If you just want to try a single model, deploy Boltz-2 or MolMIM and start playing with the endpoint. If you want to see the whole process in action, deploy the NVIDIA Blueprint for virtual screening, open JupyterHub and watch it fold proteins, generate molecules and rank potential binders right in your browser.

We’re still adding new models and workflows, but everything you’ve read here is already live in Nebius AI Cloud eu-north1 and us-central1 (our data centers in Finland and Kansas City).

So go ahead — deploy a NIM, open a notebook and see what happens when GPUs, models and biology start working together in the same cloud.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- 

What are NVIDIA NIM microservices and why do they matter?

- 

Deploying NIM in Nebius AI Cloud

- 

Example of working with a NIM via Jupyter notebook

- 

NVIDIA Blueprint for virtual screening in drug discovery

- Licensing

- 

Deploying NVIDIA Blueprint in Nebius

- Running the workflow

- 

Cleaning up

- 

Wrapping Up

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Visibility that drives elasticity: Introducing Capacity Blocks and Capacity Dashboard

Today, we’re expanding Nebius AI Cloud’s elasticity even further with the introduction of Capacity Blocks and Capacity Dashboard — two new capabilities that bring additional clarity to GPU capacity management and give users full confidence in the compute they rely on.

December 17, 2025
4 mins to read

### 

Nebius AI Cloud “Aether 3.1” release: Next-gen compute for AI operations at scale

The Nebius AI Cloud 3.1 release continues the evolution of our platform into a transparent, orchestrated, developer-first environment — where performance is accessible, capacity is visible and control feels effortless. Across new platforms based on NVIDIA Blackwell Ultra, smarter capacity management and an improved experience for both developers and platform operators, every enhancement moves us closer to that goal.

December 17, 2025
5 mins to read

Sign in to save this post
Sign In
