# AI model hosting options

Source: https://nebius.com/blog/posts/ai-model-hosting-options

Skip to main content

Once your AI model is trained and ready, you must host or “deploy” it. AI model hosting is the process of making your AI model accessible to other users or applications. Typically, the model exposes an API (application programming interface) that authorized users and software systems can use to communicate with your model via code.

As a simplistic overview, you can picture the hosted AI model running on a remote server (hosting environment) and awaiting input. An external application performs an “API call” and sends input data to the model. The model processes the input and returns any predictions or new data generated as output back to the external application.

Of course, in practice, things get a LOT more complicated. You typically have large AI workloads running in a distributed environment spanning hundreds (if not thousands) of servers. There are several technology layers between your model and the underlying server hardware.

AI hosting options are based on who owns and manages the different technology layers. Before making a choice, you must consider factors like performance, cost, security, the technologies you’ll have to work with, and your team’s technical capabilities.

This article explores the technologies to consider when hosting, the options available, and the criteria for choosing the best solution.

## Technology layers in AI model hostingTechnology layers in AI model hosting

AI model hosting options require you to consider who manages which layer in your AI deployment stack. Let’s consider these layers.

### ComputeCompute

This layer includes specialized hardware needed to speed up AI processing. CPUs handle general-purpose tasks but also require GPUs for parallel processing and matrix calculations. Specialized hardware such as TPUs (Tensor Processing Units) and FPGAs (Field-Programmable Gate Arrays) are modern advances for generative AI models. You also need high-performance network infrastructure like RDMA (Remote Direct Memory Access) and ROCE (RDMA Over Converged Ethernet) for fast data transfer between computing nodes in a distributed environment.

### StorageStorage

This layer stores interim model output, the data the model works with, model metadata, and more. Block storage, file storage, object storage, etc., are a must. You may also need high-performance file systems like Lustre, designed to work with large-scale AI compute clusters.

### Compute unitCompute unit

These are technologies necessary for running the AI model on the hardware. They act as an intermediary and manage the hardware resources for the model.

Containers are lightweight, portable units that package the application and its dependencies. They ensure consistency across environments. VMs are virtual machines that create several server instances on the same hardware. You may also use the bare metal option with a light operating system and no virtualization. Typically, you may have several containers running across several VMs.

### OrchestrationOrchestration

Technologies in this layer let you scale, start, and stop underlying infrastructure based on workload demand. They can withstand hardware failures and network outages.

Kubernetes is an open-source platform for managing containerized workloads. Ray and JARK are emerging frameworks designed for distributed computing.

### Environment & toolsEnvironment & tools

This is the layer data scientists are most familiar with. It includes all frameworks, software libraries, and tools needed to build and run your AI models.

### DeploymentDeployment

Deployment is the technical term for hosting. The topmost layer in the image shows some managed deployment options. You can choose the self-managed route and purchase and organize everything you need for each layer. Or you can go the managed route and let third parties manage some of (or all) the layers for you. You could even go 'serverless', letting others manage your server for you while you just focus on your model. Cloud technologies give a lot of flexibility in this regard.

## Summary of AI model hosting optionsSummary of AI model hosting options

 | Option
 | Description

 | Self-managed on-prem
 | You purchase, configure, and manage all the hardware and software layers in the AI model deployment stack.

 | Self-managed cloud
 | You lease some infrastructure from a cloud provider. The cloud provider manages the hardware layers (1, 2 in the diagram above), but you set up and manage all the other software configurations yourself.

 | Serverless
 | You lease server infrastructure from a cloud provider. The cloud provider manages layers 1, 2 and 3, so you can run the model without thinking about the underlying server environment. You manage layers 4 and above yourself.

 | Managed cloud
 | You lease some infrastructure from a cloud provider. The cloud provider manages the hardware layers. The cloud provider or another third party manages some of the software layers. You can pick and choose what you manage and what others manage for you.

 | AI PaaS
 | AI Platform as a Service gives you fully managed layers from 1 to 5. You only focus on the model.

Depending on your chosen solution, you need to work with different tools and technologies. You get different degrees of flexibility, convenience, and control from each.

## Self-managed on-prem AI model hostingSelf-managed on-prem AI model hosting

On-prem AI model hosting requires you to first invest in server hardware. You typically have to find a vendor partner in the AI hardware space (like an NVIDIA vendor partner) who will suggest the best solutions for your use case. You can select different computing, storage, and networking solutions (e.g., NVIDIA GPUs with IBM storage) or pick a turnkey AI data center like NVIDIA AI for Enterprise.

Next, you must install the operating system, container technologies, relevant machine learning libraries, etc. You also have to configure web servers, such as NGINX or Apache, to serve requests to the model.

This approach provides full control over the hardware configurations and security, but it also comes with responsibilities for infrastructure maintenance. It is expensive to get started and typically out-of-reach for start-ups and small organizations. It also limits flexibility and capacity. For example, you are limited in running your model in a specific location, which may increase latency for users in other locations. You also cannot scale up or down quickly and are limited to your pre-purchased capacity.

## Self-managed cloudSelf-managed cloud

You can lease server infrastructure from cloud providers. You only pay for the time your workload runs. You do not have to pay for idle resources or pay upfront fees, making this a more cost-effective option.

Public cloud providers like AWS, Azure, and GCP offer a range of server instances — you can pick and choose the GPU/CPU/network combination necessary to get started.

However, public cloud providers have many services and don’t cater specifically to AI workloads. Cloud tech support and services are available only for premium clients. Most importantly, cost estimation is challenging to predict. The public cloud provider may lock you into using various services — bloating your bill without realizing it. You need specific public cloud expertise to navigate and choose the best solutions for your use case.

Instead, consider looking for an AI cloud provider that provides customized service. You will get customized consultation from the start, predictable billing, and full support throughout your project.

## ServerlessServerless

All three public cloud providers offer “serverless” capabilities. You can run your workloads on their servers without worrying about underlying server configuration. This is done through serverless functions like Lambda for AWS or Azure Functions for Microsoft.

However, running AI through serverless requires complex coding skills. You must integrate with several other services, including storage and API Gateway. You also have to tackle the “cold start” problem. When a serverless function hasn’t been used for a while, the cloud provider shuts down the server instance that runs the function to save resources. The next time the function is triggered, the underlying cloud technology restarts the server, loads your function, and initializes all its dependencies — causing a 7–10-second delay. The delay can be a deal-breaker for most enterprise AI use cases.

Serverless is not a practical solution for most enterprise use cases. It is suited for experimentation and early prototyping.

## Managed cloudManaged cloud

Managed cloud is a game changer for most AI teams. Hosting your AI model requires Ops expertise, but AI teams have more development experience. Trying to ramp up on Kubernetes, databases and other deployment layer tech can take away time and energy from AI development.

Managed cloud solves this problem for AI teams. The managed service handles all configurations, scaling, and maintenance of the infrastructure layer so you don’t have to. For example, you may choose managed Kubernetes or managed SQL data. You pay for hour based usage, the same as for hardware layers.

Managed cloud gives you convenience and flexibility at lower cost.

## AI PaaSAI PaaS

AI Platform as a Service gives you an all in one AI platform with your favorite frameworks and tools ready to go. With AI PaaS, the network, storage, orchestration, and compute is handled for you. You just have to focus on training and developing your model. Typically, a few clicks in a UI based console are enough to host the model and move it to production. Most platforms also autogenerate the API’s you need.

AI platforms may be slightly less flexible in terms of the software you have to use. However, the returns in terms of productivity and cost-efficiency are very high. Your team can focus on their core tasks without getting distracted by cluster scaling, resource management, networking, etc.

## Criteria for choosing the best AI model hosting optionCriteria for choosing the best AI model hosting option

When choosing between the different options consider the following criteria.

### Inference typeInference type

Do you plan to run your AI workloads in batches or expect real-time input? In batch mode, input data is collected over time and then sent to the hosted AI model to generate predictions. In real-time mode, your model has to process incoming data with minimal latency and provide immediate responses. Batch mode requires hosting options that can scale quickly when the workload runs and then remain idle for a period without adding to your costs. Real-time mode requires hosting options that can process at high speed and provide load balancing, caching etc. to meet performance criteria. Self-managed on-prem is inefficient for batch processing. It can work in real-time if your input comes from a specific geographic area. Managed cloud or AI PaaS are preferable for both as they provide autoscaling at low latency and low cost.

### Cost considerationsCost considerations

When budgeting, you have to consider both initial costs and ongoing costs. On-prem infrastructure typically has a high initial investment with average ROI of 3–5 years. However, you do require operational specialists on the team for ongoing maintenance.

In contrast, cloud infrastructure shifts capex to opex. Your monthly bills can be estimated upfront for increased predictability. Managed cloud and AI PaaS also lets you manage with your existing team so you don’t have the expenses of hiring specialists.

### SecuritySecurity

AI projects in heavily regulated industries must meet compliance considerations. There are rules around where your data resides and who can access it. On-prem may be preferred if your data must sit in specific geographic locations on hardware fully controlled by you. Private cloud is another option — you can lease cloud infrastructure so that more layers are in your control. However, cost tends to be higher. Managed cloud and AI PaaS provide a happy medium for most industries. These providers can meet stringent requirements without adding to your bill, as long as they meet security criteria in managing their hardware. You will have to check your vendors security policies to determine this.

### CustomizabilityCustomizability

You want hosting options that are fully customizable to your project needs. You should be able to configure (or request configurations from providers) for every layer of your deployment stack. You don’t want to be locked into a tech stack you are uncomfortable with.

## FAQ

Where can I host an AI model?

You can host an AI model on several platforms, including on-premises servers, cloud services like Nebius cloud, or AI platform as a service. Each option offers different levels of control, scalability, and cost depending on your requirements.

What is the best hosting for AI?

The best AI hosting option depends on your needs. For flexibility with full control, and easy scalability, managed cloud services like Nebius are best. If you have the budget you may consider investing in on-prem infrastructure.

How much does it cost to host an AI?

The cost to host an AI model varies based on factors like model complexity, usage, and infrastructure. Cloud platforms often charge based on compute, storage, and data transfer per hour. Prices can range from a few dollars monthly to thousands for large-scale models.

How do I publish an AI model?

To publish an AI model, first, train and export it. Then, choose a hosting platform (e.g., Nebius, AWS, or an on-prem server). Create APIs or endpoints to interact with the model and deploy it. Ensure it is scalable and secure, depending on the intended usage and application.

## Explore Nebius

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

Choosing storage for deep learning: a comprehensive guide

Drawing from Nebius’ and our clients’ extensive experience, this guide and research aims to help engineers choose the most fitting storage solutions for deep learning.

August 15, 2024
7 mins to read

### 

On Kubernetes significance for ML/AI engineers

K8s has become the tool of choice for machine learning teams large and small. What are its properties that have made it today’s industry standard?

November 14, 2023
7 mins to read

### 

ModelOps: mastering AI model lifecycle

Model operationalization (ModelOps) is an ideology that aims to streamline the development and deployment process for AI applications. Let’s get deeper into the topic, understand differences between ModelOps and MLOps, and explore ModelOps use cases.

May 1, 2024
7 mins to read

Sign in to save this post
Sign In
