# Machine learning experiments: approaches and best practices

Source: https://nebius.com/blog/posts/machine-learning-experiments

Skip to main content

In science, an experiment is a question to nature about a scientific theory. For example, Arthur Eddington’s famous 1919 experiment verified Einstein’s relativity theory by asking the question—does light bend due to the gravitational field produced by the sun? To answer the question, he recorded the perceived position of stars during a solar eclipse when the sun’s light was blocked. He then compared the measured star positions to their expected positions. Eddington’s readings showed that the sun’s gravitational field does indeed bend light, providing strong support for the relativity theory.

Similarly, machine learning experiments pose questions about models that data scientists try to answer by data measurements. The goal is to find and optimize the best model for a specific use case. The definition of best also changes for every use case. Some use cases demand models with high accuracy, while others prioritize speed or interpretability.

Machine learning experiments allow data scientists to ask questions, make hypotheses and collect data to prove (or disprove) different scenarios and models. This article explores different approaches and best practices for machine learning experimentation.

## What is a machine learning experiment?What is a machine learning experiment?

A machine learning experiment is essentially a structured process of testing machine learning models. In every experiment, a model runs over a dataset and makes predictions. You then validate the predictions against known outputs.

A loss function quantifies the difference between the model’s predicted values and the data’s actual values. You use it to calculate metrics like accuracy or error percentage.

You can run hundreds of experiments before selecting a production model. Between experiments, you make small changes in model parameters or data configurations. Results and changes are systematically tracked so that data drives the final decision-making process.

## Machine learning experiment approachesMachine learning experiment approaches

During the experimentation phase, you are free to explore both models and data. Depending on your goals, you can run the following types of experiments.

### 1. Model selection.1. Model selection.

The dataset remains the same. You change models between experiments.

You use a standardized or open-source dataset to trial different models for your use case. You run different models, such as logistic regression, SVM, random forests and neural networks, over the same dataset. All of them are evaluated using consistent metrics like accuracy, precision and recall.

To compare two specific models, you can randomly divide up one large dataset between the two models or divide the data based on specific attributes. For example, in fraud detection, you may divide the data based on the payment method used—credit card transactions going to one model and direct debits to another.

### 2. Feature engineering.2. Feature engineering.

The model remains the same. You change data features between experiments.

Feature engineering involves transforming raw data into features that better represent the underlying patterns and improve model performance. You create new features or transform existing ones between experiments.

Examples of transformation include:

- Scaling features to a specific range

- Standardizing feature values

- Applying logarithmic or square root functions on features

- Creating new features by raising existing features to powers

You can also filter features between experiments. For example, evaluate different feature subsets to select the best-performing combination.

### 3. Hyperparameter tuning3. Hyperparameter tuning

The model remains the same. You change hyperparameters between experiments.

Hyperparameters are settings that determine the neural network structure and the learning process of the model. These parameters are not learned from the data but are set before training. Examples include learning rate, number of hidden layers and batch size.

You can take various approaches to hyperparameter tuning:

- Grid search—exhaustively explore a predefined set of hyperparameter values.

- Random search—sample random hyperparameter values from a specified distribution.

- Bayesian optimization—building a probabilistic model of the loss function to explore various hyperparameters intelligently.

- Hyperband—eliminate 50% underperforming hyperparameters between experiments.

- Genetic algorithms—”evolve” the populations of hyperparameter configurations, by choosing high-performing configurations over time.

Each approach has its pros and cons. Grid search and Bayesian require more computational resources but are more thorough. Random search and hyperband are less intensive and faster but may miss out on specific critical parameters.

### 4. Data augmentation4. Data augmentation

The model remains the same. You change the dataset between experiments.

Data augmentation is the process of artificially increasing the size and diversity of a dataset. You transform the data without changing its label (original output value).

For example, in image recognition, you may crop images, flip them horizontally or add noise to images before running the next experiment. You aim to improve the model’s capabilities by exposing it to more data.

## Example of an ML experimentExample of an ML experiment

Consider a bank trying to develop a machine learning model to detect fraudulent transactions. The goal is to minimize the number of false positives (legitimate transactions flagged as fraud) and false negatives (fraudulent transactions not detected).

The bank’s data engineering team collects historical transaction data, including features like transaction amount, location, time and user information. The dataset is labeled, and every transaction is marked as either ‘fraudulent’ or ‘legitimate.’

Some experiments the team may conduct include:

- Try different models like random forest or gradient boosting on the data.

- Create a new feature that measures the time difference between transactions and trying models on that feature.

- Use external fraud reports to enhance the data before trying the model.

- Tweak the model’s parameters like tree depth (for decision tree model)

## Best practices in machine learning experimentationBest practices in machine learning experimentation

The main challenge in machine learning experimentation is systematically tracking the metadata across hundreds of experiments. You have to keep detailed records of model parameter values, data features, metrics and other details like code and environment configurations you use to run the experiment. Your goal should be to record enough information so anyone in your team can reproduce the results if needed.

If you are just starting out or self-tracking, you can use a simple spreadsheet to record key differences between experiments. The spreadsheet acts as a summary of one batch of experiments that you run over a short period.

Having said that, it is best to use experiment tracking tools to store data and generate usable reports in the long term.

Some other best practices include:

- Establish a baseline. It is important to clearly define objectives before starting experimentation. If you are exploring models, you should know the metric values to aim for. If you are trying to optimize a single model, it is better to establish a baseline model as a reference point. That way, you can quickly identify whether changes are improving performance.

- Maintain consistency. It is important to maintain consistency in the factors that remain the same between experiments. Your experiment conditions also include the code version, operating system and other server configurations in which your model runs. You should aim to create reproducible environments that you can set up and use consistently over time. Version control is critical to reduce human error and allow the option to rollback.

- Implement automation. Having an established MLOps pipeline greatly improves the speed and efficiency of your experimentation. Automate routine tasks like data ingestion, pre-processing and deployment. Automation also supports collaboration between team members so they do not repeat work or overwrite each other’s changes.

## ConclusionConclusion

Machine learning experimentation is an iterative process. Like a scientist, you must hypothesize and collect data diligently to support your viewpoint. Review the results regularly and learn from failures. Continuous improvement and adaptation are key to developing effective models.

## Explore Nebius AI

Log in​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Shweta Shetty
Technology writer and editor at Nebius AI

## See also

### 

What is epoch in machine learning? Understanding its role and importance

What is an epoch in machine learning? Learn how epochs, batch size, stochastic descent gradient and iterations influence neural networks in deep learning.

July 23, 2024
10 mins to read

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

### 

In-house AI R&D: Nebius’ secret ingredient for truly AI‑centric cloud

It wouldn’t be possible for us to build a machine-learning platform without advancing in the field ourselves.

July 29, 2024
9 mins to read

Sign in to save this post
Sign In
