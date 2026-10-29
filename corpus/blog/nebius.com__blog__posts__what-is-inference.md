# What is inference?

Source: https://nebius.com/blog/posts/what-is-inference

Skip to main content

Machine learning model inference refers to using a trained ML model in a real-world scenario. During inference, the model is passed to real-world data, producing an output that can be utilized in a practical application.

The operationalized model needs to be robust to different data distributions. For this, it undergoes a lengthy development lifecycle. This article will discuss the different stages of model development and explain how model inference is implemented.

## Machine learning training and inferenceMachine learning training and inference

Training and inference are both part of the machine learning project lifecycle. During the training phase, the model learns to understand the intricate patterns present in an elaborate dataset. The type of data set and its target variable depend on the task. For example, for a cat classification problem, the dataset would contain pictures, and the target variable would indicate whether the image contains a cat or not. ML training includes data collection, preparation, feature engineering, and model training and testing. It includes all the steps required to prepare an AI model for real-world use.

The inference stage comes after the training is complete. It involves packaging the model and deploying it on a specialized server. The model accepts real-world data and predicts various business use cases during inference. Since the model processes previously unseen data, inference tests the model’s robustness in practical scenarios.

## Machine learning development lifecycleMachine learning development lifecycle

The machine learning development lifecycle consists of various data preparation and model training steps. Let’s discuss these steps in detail.

### Data preparationData preparation

Every machine learning project starts with data collection and processing. The data required for ML training is obtained from various sources and must be cleaned and standardized before it is used for training. The preparation stage can involve joining data from various sources to create a single view, removing NULL values and outliers, and creating an automated extract, transform, and load (ETL) pipeline for seamless training.

Moreover, some advanced data transformation steps may involve data aggregation or feature engineering as part of the automated pipeline. Depending on the processing complication and problem specifications, all these steps may be performed in an SQL workflow or Python notebooks.

### Pre-trainingPre-training

Once data is prepared, the next step is to train the model for the specific task. Small models are trained directly for downstream tasks using the conventional train, validation, and test splits in the dataset.

However, large-scale models such as large language models (LLMs) undergo a pre-training phase first. Pre-training involves training the model on a massive generalized dataset without any distinct end goal. The purpose of pre-training is to teach the model basic information across various subjects. For example, if the model is built to predict animal images, then the dataset will cover images of all animal types. The model will learn to understand the different features present in the dataset and gain a generalized understanding of animals.

The pre-trained model is often referred to as a “foundation model” and is fine-tuned by data scientists for various downstream tasks.

### Fine-tuningFine-tuning

The fine-tuning stage completes the training process by specializing the model for a specific task. During fine-tuning, data scientists take the foundational model and train on a relatively smaller dataset with a particular target variable. The intuition here is that since the model already has a general understanding of the data, it requires only minor training to be ready for a specific task.

Continuing our previous example, suppose an ML engineer wants to train a model for detecting monkeys in an image. The fine-tuning process will involve using a labeled dataset for monkeys and continuing to train the foundation model using its existing weights. Depending on the requirement, the process may train the entire model or some specific layers. Another important distinction of fine-tuning is that it attaches the task-specific head to the model. Since the model in the example is trained for object detection, the model head will output the bounding box coordinates.

## Deployment phase: Machine learning inferenceDeployment phase: Machine learning inference

When the model is fine-tuned for the intended task, it is deployed to a specialized server. During production, the model processes real-world information and generates results. This process is called machine learning inference, and the model infers unseen information and uses its existing knowledge to make accurate predictions.

The model inference architecture covers the entire pipeline from data collection to running predictions and storing the results. Let’s understand the infrastructure components in detail.

### Inference architectureInference architecture

A machine learning production environment can be divided into three main components as follows:

### Data sourcesData sources

Even during inference, the model pipeline collects data from multiple sources as required. Depending on its nature, the required data may be collected in a conventional relational database (RDBMS) or a data lake. Structured data is stored in the RDBMS, while unstructured information like images and text is stored in a data lake. In either case, the stored information is used for batch predictions, i.e., the collected data is processed simultaneously to get multiple prediction values. Batch processing is popular in sales forecasting applications, where data collected over several months or years is used to predict future sales.

In modern, fast-paced applications, the data source is a real-time stream that collects information from a running application and delivers it to the hosted model. Such applications make predictions on the fly and use them to take real-time action.

### Model host systemModel host system

The host system is a high-performing server where the final model is deployed. The environment is often equipped with a high-power GPU for faster processing and seamlessly connects with the data sources.

The scripts deployed on the host system are responsible for loading data from the sources, performing necessary processing and structuring, and passing the processed data to the model. The model then infers the available information and provides its output.

### Data destinationData destination

The predictions from the model are sent towards their respective destinations via another pipeline. The destination can be an RDBMS or data lake where another team fetches the stored predicted values. They can also be transmitted to another application or dashboard in real time to display results immediately.

All the components mentioned for machine learning inference are often present on the same platform. The platform architecture allows seamless connections between the various modules and offers additional features like feature and model versioning.

### Model inference challengesModel inference challenges

While model inferencing is critical to the machine learning development lifecycle, deployment carries various challenges.

- Team collaboration: Often, the teams responsible for setting up the inference architecture and model deployment are unfamiliar with machine learning conventions. They may be familiar with a programming language different from the model’s. Moreover, robust deployment would require strict collaboration with the development team to understand any edge cases and create a scalable environment.

- Model drift: Machine learning modeling is an iterative process. The inference architecture must include drift monitoring to test when the model requires retraining.

- Costly hardware: Machine learning inference requires high-end CPUs and GPUs to handle real-time data streams and ensure fast processing. The required hardware can be costly and impact the product’s return on investment (ROI).

- Scalability: The host system must be scalable to accommodate a growing user base. Scalability for an ML project is different from that of a conventional software product since it has to accommodate the growing processing requirements of the model itself. The processing needs can be challenging to anticipate and accommodate beforehand.

- Model interpretability: Interpreting model results is a growing concern when producing the solution. Understanding the model’s logic can be challenging and raise concerns with customers or stakeholders.

## ConclusionConclusion

Machine learning inference is the process of using a fully trained model to make predictions on real-world unseen information. It is the last step in the machine learning development cycle, also called “productionizing the model.”

The development life cycle involves data gathering, processing, model pre-training, and finally, fine-tuning on task-specific scenarios. The final trained model is deployed on a specialized host environment for inference. The deployment architecture includes connections to data sources, a GPU-enabled host machine for faster processing, and connections to the data’s destination or dashboards.

The inference process has certain challenges, such as collaboration between IT teams and data scientists, costly hardware, and scalability. However, despite the challenges, machine learning applications are imperative to generating actionable insights and guiding business owners.

## FAQ

What is the difference between model training and model inference?

Model training uses supervised or unsupervised learning to teach the model data patterns. Model inference uses the trained model to make predictions in real-world scenarios.

What is the purpose of model inference?

Model inference applies a trained machine learning model to new, unseen data in a real-world environment, generating predictions or insights.

What is model inference time?

Model inference time is the time it takes for the model to process the input data and generate an output.

## Explore Nebius AI

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

Spark vs. Hadoop in data engineering

Spark has recently been gaining popularity over Hadoop for ML/AI use cases. Is Hadoop becoming obsolete? Do these technologies compete or complement each other? This blog post answers all your questions about Spark and Hadoop.

September 19, 2024
8 mins to read

### 

What is AutoML? Understanding automated machine learning

Explore our comprehensive guide to automated machine learning (AutoML) and find out why it’s changing data science and making machine learning available to everyone.

September 19, 2024
9 mins to read

### 

Entropy in machine learning — applications, examples, alternatives

Entropy is a machine learning term borrowed from thermodynamics that measures randomness or disorder in any system. Why measure disorder? Mathematics uses entropy to measure this chaos — or, more specifically, the probability of chaos.

September 17, 2024
10 mins to read

Sign in to save this post
Sign In
