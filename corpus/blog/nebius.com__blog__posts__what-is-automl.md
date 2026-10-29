# What is AutoML? Understanding automated machine learning

Source: https://nebius.com/blog/posts/what-is-automl

Skip to main content

Automated machine learning, also known as AutoML or automated ML, takes the grind out of developing a machine learning model. It’s a friend to data scientists, analysts, and developers everywhere as it can automate time-consuming, iterative tasks, giving teams an opportunity to build ML models with high scale, efficiency and productivity — all while sustaining model quality.

This article will take you deep into the world of automated machine learning to find out how AutoML works, how it provides faster, more accurate outputs than a hand-coded algorithm, and why it’s revolutionising machine learning by making development more user-friendly and opening the field to non-experts.

## What is automated machine learning (AutoML)?What is automated machine learning (AutoML)?

Automated machine learning or AutoML is the process of automating the end-to-end process of building machine learning models. This includes tasks such as data preprocessing, feature engineering, model selection and hyperparameter tuning.

The goal of automations here is the democratization of machine learning. By providing a user-friendly interface for training and deploying models, AutoML allows accessibility for a wider range of people, including those with little or no experience in data science.

AutoML reduces manual labor and simplifies routine tasks, while providing faster and more accurate outputs than a hand-coded algorithm. This improved accessibility also allows non-experts in your organization to participate in the process of creating and deploying machine learning models.

## How does the AutoML process work?How does the AutoML process work?

An AutoML platform is typically an open source library that simplifies tasks in the machine learning process, including:

- 

Raw data processing.

- 

Feature engineering.

- 

Model selection.

- 

Hyperparameter optimization.

- 

Deployment of a practical ML model.

AutoML creates many training pipelines in parallel that try different algorithms and parameters for you. Iterations are made through ML algorithms paired with feature selections, and model scoring allows you to track an optimization metric or metrics. The process ends once it hits the exit criteria defined in your experiments.

You can run, design and automate your ML training experiments following these steps:

- 

Identify the ML problem to be solved: classification, forecasting, regression, computer vision or natural language processing (NLP).

- 

Choose whether you want a code-first experience or a no-code experience (also termed a studio web experience). If you prefer a code-first experience, you should consider solutions such as the Azure Machine Learning SDKv2 or the Azure Machine Learning CLIv2.

- 

Specify the source of the labeled training data.

- 

Configure the automated machine learning parameters that determine how many iterations over different models, hyperparameter settings and advanced preprocessing. Determine what metrics to look at when choosing the best model.

- 

Job submission.

- 

Review the job results.

Monitoring and analysis of logged job information provides valuable evaluation metrics gathered during the job. The job model inspection produces a Python object (.pkl) file that can be used in analysis and when determining feature importance.

### OutputsOutputs

Supervised machine learning models create outputs by making predictions based on the input data you select. During training sessions, the model learns the relationship between the input data and the correct outputs, and uses those learnings to make new predictions.

### InputsInputs

The quality of input data is vital for machine learning models because it directly affects the accuracy and performance of the model. If the data is of poor quality, the model will learn misleading or incorrect relationships between the input and output, and you will not get the results you need.

### HyperparametersHyperparameters

Hyperparameters are settings or parameters that govern model behavior. Hyperparameters include the:

- 

Learning rate.

- 

Number of hidden layers in a neural network.

- 

Regularization strength.

These parameters can have a significant impact on your model’s performance, and the optimization of hyperparameters often turns out to be a time-consuming and challenging task that requires considerable expertise and experience.

AutoML systems optimize hyperparameter search by automatically finding the best combination of hyperparameters for a given machine learning model. This is achieved by running model training sessions on the data using different combinations of hyperparameters, then running an evaluation on the performance of each combination.

### Why is AutoML important?Why is AutoML important?

AutoML represents a milestone in machine learning and artificial intelligence (AI).

AI and ML have faced 'black box' criticism because machine learning algorithms can pose challenges for reverse engineering. Although they improve AI efficiency and processing power, it can be difficult to track how the algorithm delivered a particular output. In turn, this makes it hard to choose the correct model for a given problem, and it can be difficult to predict a result if a model is a mysterious black box.

But AutoML makes machine learning less of a black box by improving accessibility and making it easier for non-experts to develop AI machine learning models, and by fine-tuning the end-to-end pipeline through meta learning.

As developing machine learning models requires technical skills and deep learning knowledge, this can be a barrier for those who have the domain knowledge to identify problems that could be solved with machine learning, but lack the technical skills to build AI models themselves. For those looking to bridge this skills gap, an AI and Machine Learning bootcamp can provide the foundational training needed to get started.

AutoML helps in the democratization of machine learning by making it more widely accessible, which promises benefits such as driving innovation in AI and complex problem-solving. On a wider scale, AutoML also represents a step toward artificial general intelligence, which is the hypothetical AI of a machine that has the ability to understand or learn any intellectual task that a human being can.

## Pros and cons of AutoMLPros and cons of AutoML

AutoML is an exciting field and promises to level the playing field by allowing more people to develop and build machine learning models.

But before you even touch an algorithm, it’s worth weighing up the benefits and challenges to make sure it’s the correct solution for your business.

### ProsPros

- 

Efficiency: AutoML speeds up and simplifies the machine learning process and reduces training time of ML models.

- 

Cost savings: Having a faster, more efficient machine learning process means a company can save money by devoting less of its budget to maintaining that process.

- 

Accessibility: Having a simpler process allows companies to save money on training staff or hiring experts. It also makes machine learning a viable possibility for a wider range of companies.

- 

Performance: An AutoML algorithm tends to be more efficient than hand-coded models.

### ConsCons

- Not a replacement for human knowledge: Like most automation, AutoML is designed to efficiently perform rote tasks, freeing up human employees such as data scientists to focus on other jobs.

But even though tasks such as monitoring, analysis and problem detection are faster when automated, human supervision is still required to assess and supervise the model. AutoML should help, not replace, a data scientist and other experts.

- Support: As AutoML is a relatively new field, you may encounter tools that are not fully developed.

### Different ways to use AutoMLDifferent ways to use AutoML

AutoML shares use cases with traditional machine learning, and ways it’s commonly used include:

- 

Improving accuracy of finance fraud detection models.

- 

Analyzing data sets for healthcare research and development.

- 

Developing image recognition for facial recognition technology.

- 

Data labeling, where you can automate labeled data to generate image models.

- 

Optimization of model performance by specifying model algorithms and tuning hyperparameters.

- 

Web service deployment.

- 

Large scale deployments, for example by using Azure Machine Learning MLOps and ML Pipelines capabilities.

- 

Risk assessment in banking and insurance.

- 

Cybersecurity risk assessment and monitoring.

- 

Customer support, including ways to automate sentiment analysis for chatbots.

- 

Adapting to malware and spam cyberthreats.

- 

Improving quality testing in agriculture.

- 

Improving engagement rates in marketing.

- 

To drive a recommendation engine in entertainment.

- 

Help improve profits and reduce waste in retail.

Support for computer vision tasks allows you to automate the generation of models trained on image data for scenarios such as:

- 

Multi-class image classification.

- 

Multi-label image classification.

- 

Object detection.

- 

Instance segmentation.

## Natural language processing: NLPNatural language processing: NLP

Support for natural language processing (NLP) in AutoML tasks allows you to automate the generation of models trained on text data for both a text classification and named entity recognition scenario.

The authoring of a AutoML trained NLP is supported via solutions such as the Azure Machine Learning Python SDK, and the resulting experimentation jobs, models and outputs can be collected, reviewed and used to guide future development.

NLP capability supports:

- 

End-to-end deep neural network NLP training with the latest pre-trained BERT models.

- 

Seamless integration with data labeling solutions.

- 

Using labeled data for generating NLP models.

- 

Multi-lingual support with 104 languages.

- 

Distributed training with Horovod.

### ClassificationClassification

In AutoML, classification is a type of supervised learning in which models learn to use training data and apply those learnings to new data.

You can choose the featurization that best suits the classification task in hand, such as deep neural network text featurizers.

The goal of classification models is to predict which categories new data fall into based on learnings from its training data. Common uses of classification models in the real-world include fraud detection, handwriting recognition and object detection.

### RegressionRegression

Similar to classification, regression tasks are a common supervised learning task you’ll encounter when exploring AutoML. There are solutions available on the market that include featurization specific to regression problems.

Whereas in classification, where predicted output values are always categorical, regression models predict numerical output values based on independent predictors. The objective in this exercise is to establish a relationship estimation among those independent predictor variables, by estimating how one variable impacts the others.

One practical use of regression could be using a model for automobile price prediction, based on common features such as gas, mileage and safety rating.

### Time-series forecastingTime-series forecasting

Forecasting is essential for all businesses. Whether it’s in revenue, inventory, sales or customer demand, you can use AutoML to combine techniques and approaches to get a high-quality, recommended time-series forecast.

Automated time-series forecast experiments are treated as multivariate regression problems, where past time-series values are 'pivoted' to become more dimensions for the regressor, together with other predictors.

This alternative approach, unlike the more familiar classical time-series methods, naturally incorporates multiple contextual variables and their relationship to one another during training.

AutoML learns a single, but often internally branched, model for all items in the dataset and prediction horizons. The result is that there is a significantly increased volume of data available to estimate a model parameter or parameters, making it possible to generalize to unseen series.

Advanced forecasting configurations include a wide variety of features, including:

- 

Holiday detection and featurization.

- 

Time-series learners and deep neural network or DNN learners.

- 

Multiple models support through grouping.

- 

Rolling origin cross-validation.

- 

Configurable lags.

- 

Rolling window aggregate features.

## Training, validation, and test dataTraining, validation, and test data

As well as providing the training data that is needed to train models, when using AutoML you can specify what type of model validation to perform. This model validation takes place during training, when automated ML uses validation data to tune model hyperparameters based on the applied algorithm to find the combination that best fits the training data. The same validation data is used for each iteration of tuning, which introduces model evaluation bias since the model continues to improve and fit to the validation data.

To help confirm that this bias isn’t applied to the final model, during final model evaluation AutoML supports the use of test data to evaluate the recommended model that emerged from your experiments. This happens by default at the end of your experiment.

## Feature engineeringFeature engineering

Feature engineering is the process of using domain knowledge of the data to create features that help an ML algorithm to learn better.

For example, some solutions enable scaling and normalization techniques to be applied during feature engineering, and these techniques are referred to as featurization.

For automated machine learning experiments, featurization is applied automatically — but customization is also possible based on your data. As part of this process, AutoML can also be used to help prevent over-fitting and imbalanced data in your models.

Additional feature engineering techniques, such as encoding and transforms, are also available.

It’s worth noting that AutoML featurization steps (for example, feature normalization) become part of the underlying model. When using the model for predictions, the same featurization steps applied during training are applied to your input data automatically.

## Ensemble modelsEnsemble models

AutoML supports ensemble models, which improve machine learning results and predictive performance by combining multiple models, rather than using single models.

AutoML uses both voting ensemble and stacking ensemble methods for model combination:

- 

Voting method: Predicts based on the weighted average of predicted class probabilities for classification tasks, or predicted regression targets for regression tasks.

- 

Stacking method: Combines heterogeneous models and trains a meta-model based on the output from the individual models. The current default meta-models are Logistic Regression for classification tasks and ElasticNet for regression or forecasting tasks.

The Caruana ensemble selection algorithm with sorted ensemble initialization decides which models to use within the ensemble.

At a high level, this algorithm initializes the ensemble with up to five models with the best individual scores, and verifies that these models are within a 5% threshold of the best score to avoid a poor initial ensemble.

Then, for each ensemble iteration, a new model is added to the existing ensemble and the resulting score is calculated. If a new model improved the existing ensemble score, an ensemble update takes place to include the new model.

## ConclusionConclusion

As this article has given you a deep dive into AutoML, you’re now ready to get started with automated machine learning tools and benefit from how they:

- 

Improve model performance.

- 

Enhance accessibility through user-friendly interfaces.

- 

Offer end-to-end solutions for the entire machine learning lifecycle.

AutoML democratizes the machine learning model development process and empowers its users, and it’s time for you to discover how it can give your business a head start.

## FAQ

What are the main benefits of AutoML?

AutoML models automate resource-intensive iterative tasks, giving you time to focus on more complex or rewarding jobs. AutoML can automate the end-to-end machine learning process and machine learning pipeline, and resulting ML models can save a developer considerable time and resources and provide insight for future developments.

Is AutoML easy to use?

AutoML is intuitive and straightforward to use. ML professionals and developers in a multitude of industries use AutoML to automate ML solutions without extensive programming knowledge. A series of simple machine learning tools helps to make it easy to optimise and automate a machine learning model and accelerate development.

Where can I use AutoML?

AutoML platforms can be built in-house or acquired from a third-party vendor and accessed through open source repositories such as GitHub. They allow developers to build ML models with high efficiency and productivity, all while sustaining model quality. AutoML also allows users to easily apply data science best practices.

How does AutoML train models?

Machine learning tools can train ML and AI models for complex problems such as image recognition tasks, including object detection and classification. You can also use learning models to automate natural language processing tasks — such as sentiment analysis and entity recognition — while models can also be trained for structured data such as tabular data from a database.

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

Entropy in machine learning — applications, examples, alternatives

Entropy is a machine learning term borrowed from thermodynamics that measures randomness or disorder in any system. Why measure disorder? Mathematics uses entropy to measure this chaos — or, more specifically, the probability of chaos.

September 17, 2024
10 mins to read

### 

What is a feature in machine learning?

Features are essential to understanding data patterns and training machine learning models. Learn about their importance and generation techniques.

September 17, 2024
8 mins to read

### 

Open-source vs proprietary software

In this post, we’re comparing open-source and proprietary software, with a detailed focus on definitions, differences, key advantages and business models.

August 28, 2024
10 mins to read

Sign in to save this post
Sign In
