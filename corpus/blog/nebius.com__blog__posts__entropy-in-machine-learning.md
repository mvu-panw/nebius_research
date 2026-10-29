# Entropy in machine learning — applications, examples, alternatives

Source: https://nebius.com/blog/posts/entropy-in-machine-learning

Skip to main content

Entropy is a machine learning term borrowed from thermodynamics that measures randomness or disorder in any system. Why measure disorder? Consider a real-life system like your office desk. The number of ways you can organize the items on your desk is limited, but the number of ways to mess it up is unlimited! Mathematics uses entropy to measure this chaos — or, more specifically, the probability of chaos.

Claude E. Shannon introduced the concept of entropy to data science in his famous 1948 paper, the Mathematical Theory of Communication. He defined entropy as the expected surprise of a random event. For example, let’s say you purchase a lottery ticket. If you don’t win the lottery, you’ll not be surprised because the chance of that happening is very low. But if you did win the lottery — you would be AMAZED. Entropy can give you a mathematical number on how surprised you’ll be!

In other words, entropy measures the unexpectedness in any system. The higher the entropy, the more randomness in your system. This article explores the mathematical basis behind entropy and its usage in machine learning. We also look at scenarios where entropy may not be the best fit and suggest alternatives.

## What is entropy in machine learning?What is entropy in machine learning?

Entropy is an important concept in supervised machine-learning techniques. Supervised learning models (algorithms) analyze large pre-labeled data sets and use the information learned to label new data. For example, you may label many financial transactions as fraudulent or genuine and train the model. Then, when you give the model a new transaction not found in its dataset, the model can accurately predict if it is fraudulent. The labels (like “fraudulent” and “genuine”) are also called class labels.

Entropy is the quantitative assessment of the unpredictability of the distribution of your class labels. You can use it to understand how evenly or unevenly your data points are distributed across different classes. The higher the entropy, the harder it will be for your supervised machine-learning algorithm to make accurate predictions.

Let’s look at a simple example to understand the concept further. Consider a dataset of customers who either purchased a product or didn’t. The entropy is high if there is a near-equal distribution of customers in both classes. Predicting whether the next customer will buy the item is hard — the probability is nearly equal.

However, if most customers purchase the product, entropy drops. The data is more organized, and it is easier to predict the outcome for the next customer.

Source

## Mathematical formula for entropyMathematical formula for entropy

Now that we have theoretically understood the concept, let’s look at the math behind it. In data science, you can calculate the entropy for every class label. It relates to the data distribution for that label.

Remember that entropy is a measure of surprise. It calculates your surprise if the machine learning algorithm classifies a new data point with that specific label. For example, going back to your customers, if most customers purchased the product, and your machine learning algorithm classified the next customer as “purchaser, ” you’ll be less surprised (low entropy). But if it classified the customer as “not purchasing, ” you’ll be more surprised (high entropy).

Entropy is thus inversely proportional to the probability of an event occurring. Shannon bases the formula on the logarithmic scale. For any data factor (individual label x):

Entropy(x)=p(x)⋅log2p(x),Entropy(x) = p(x)·log_2 p(x),Entropy(x)=p(x)⋅log2​p(x), where p(x)p(x)p(x) represents the probability of that classification outcome.

### Why is the log multiplied by the probability?Why is the log multiplied by the probability?

When p(x)=1p(x)=1p(x)=1, log2p(x)=0log_2 p(x)=0log2​p(x)=0 and when p(x)=0.5p(x) = 0.5p(x)=0.5, log2p(x)=1log_2 p(x)=1log2​p(x)=1.

Since probability is a value between 0 and 1, entropy should also be between 0 and 1. But as the value p(x)p(x)p(x) moves to 0, the value of log2p(x)log_2 p(x)log2​p(x) becomes greater than 1. (Cells with values 1.7 and 3.3 in the table below. Table shows approximate values.)

 | p(x)p(x)p(x)
 | −log2p(x)- log_2 p(x)−log2​p(x)
 | −p(x)⋅log2p(x)-p(x)·log_2 p(x)−p(x)⋅log2​p(x)

 | 1
 | 0
 | 0

 | 0.8
 | 0.32
 | 0.25

 | 0.5
 | 1
 | 0.5

 | 0.3
 | 1.7
 | 0.51

 | 0.1
 | 3.3
 | 0.33

However, we want it to move to 0 as well. If there is no possibility of an outcome, there is no possibility of surprise for that outcome. Multiplying by p (x) evens that out. (last column of the table)

### Net entropyNet entropy

You can calculate the total entropy in your data by summating individual values.

H(x)=∑x=0np(x)⋅log2p(x)H(x) = \sum_{x=0}^{n}p(x)·log_2 p(x)H(x)=x=0∑n​p(x)⋅log2​p(x) Machine learning algorithms often try to minimize net entropy to make the best possible prediction for new data.

Net entropy distribution curve. Source

## Entropy in machine learning modelsEntropy in machine learning models

Entropy helps machine learning models make accurate decisions about unknown data. It gives a mathematical basis for the model to classify data. The models can reduce entropy to mathematically co-relate different data points.

Let’s dive deep into decision trees to understand the practical applications better. They are the most common algorithms designed around the entropy concept.

### Decision tree overviewDecision tree overview

Decision trees combine the if-else programming paradigm with entropy to efficiently classify data. They split the dataset into smaller and smaller subsets based on entropy conditions.

Key components of a decision tree:

- 

Root node: The topmost node, representing the entire dataset, where the first split or decision occurs.

- 

Internal nodes: These nodes represent the decision points where the dataset is further split based on feature values.

- 

Branches: These are the possible outcomes of a decision at an internal node, leading to other nodes.

- 

Leaf nodes: The terminal nodes representing the final output or classification.

### Use of entropy in decision treesUse of entropy in decision trees

The tree tries to split the data at every node based on specific attributes so the classification is as neat as possible. The lower the entropy, the neater the split. The algorithm splits the data at every internal node based on the feature that minimizes entropy and maximizes information gain.

Information gain is computed as follows:

IG(n)=1−∑i=1Jp2(i)IG(n)=1 - \sum_{i=1}^{J} p^2 (i)IG(n)=1−i=1∑J​p2(i) Information gain represents the change or reduction in entropy. It compares the parent node’s entropy with the average entropy of all child nodes. High information gain indicates more reduction in entropy. Low information gain indicates less reduction in entropy.

### Example of entropy in machine learningExample of entropy in machine learning

Consider media algorithms trying to predict the movie genre by analyzing the movie poster. Initially, entropy is high as there is a mix of objects and landscapes in the images. But you can reduce entropy by zooming in on the central image object. A fighting animal indicates fantasy, a human holding sports equipment indicates a sports movie, and so on.

You train your decision tree on movie posters pre-labeled with their genre. The algorithm self-learns, trying to identify correlations between the image data and its corresponding label.

The first split is on the image at the center of the poster, as it reduces the entropy the most. The next level split categorizes the central image into human, animal, or object. The level after that tries to identify what the central image is doing. At every level, the algorithm tries to reduce the chaos or uncertainty that entropy creates and reach certainty or a definite answer to the question — “What is the movie genre based on its poster?”

## More applications of entropy in machine learningMore applications of entropy in machine learning

Beyond decision trees and information gain, entropy is the basis for several other important measures that help quantify relationships between data, probability distributions, or models.

### Mutual informationMutual information

Mutual information mathematically quantifies the relationship or dependency between two random variables. It measures how knowing one variable reduces the uncertainty (entropy) about the other.

For two variables, x and y:

I(x;y)=H(x)−H(x∣y)I(x;y)=H(x)-H(x|y)I(x;y)=H(x)−H(x∣y)

H(x)H(x)H(x) is the entropy of x, and H(x∣y)H(x|y)H(x∣y) represents the remaining uncertainty about x after knowing y. H(x∣y)H(x|y)H(x∣y) is also called conditional entropy. If knowing y completely determines x, the conditional entropy is zero because there’s no remaining uncertainty in x.

Consider a scenario where you’re trying to predict a student’s exam result x (pass or fail) based on their class attendance y. If y is greater than 90%, the student always passes. In this case, the conditional entropy will be close to zero because knowing y reduces nearly all the uncertainty about x.

A common use case of mutual information is in evaluating the quality of a clustering solution. Clustering algorithms try to find patterns in a dataset without any pre-labeling. You can check their output using mutual information. Data points within a cluster should have high mutual information, while the inter-cluster data should have low mutual information.

### Relative entropyRelative entropy

Relative entropy, or Kullback-Leibler (KL) divergence, measures the difference between two probability distributions of the same variable.

Probability distribution P and Q. Source

KL divergence quantifies how much one probability distribution (P) diverges from a second reference distribution (Q). It simply tells how much 'extra information' would be needed to describe the true distribution. A higher KL divergence indicates that the learned distribution won’t be able to represent the original data accurately.

For example, suppose you have a dataset of handwritten digits and want to generate new digits similar to those in the dataset. The true distribution of these digits is unknown and complex due to the variety of digits, styles, and handwriting. Some generative AI algorithms use KL divergence to learn a simpler, approximate distribution Q that can still generate similar digits.

### Cross entropyCross entropy

Entropy, specifically cross-entropy, has applications in model evaluation. It is used as the loss function that quantifies how well or poorly a model performs. It measures the discrepancy between the predicted values and the actual target values from the dataset. If the model predicts a probability that’s far from the true label, the cross-entropy value will be large, indicating a poor prediction. Unlike KL divergence, cross-entropy also penalizes incorrect predictions.

### Dimensionality reductionDimensionality reduction

Dimensionality reduction in machine learning refers to techniques that reduce the number of input variables (features) in a dataset while retaining as much important information as possible. For example, when analyzing facial images, you can look at everything from skin tone to eye shape, eye color, nose shape, scars, ear shape, etc. Or you can focus on two or three key features, such as eye color, hair color, and skin tone, to quickly categorize an image. Reducing the number of features decreases the computational complexity of the model, making it faster and more scalable.

Entropy plays a role in dimension reduction techniques like t-SNE (t-distributed Stochastic Neighbor Embedding) and UMAP (Uniform Manifold Approximation and Projection). t-SNE minimizes the KL divergence between the probability distributions of the high-dimensional data points and their lower-dimensional representations. UMAP uses cross-entropy for the same.

### Anomaly detectionAnomaly detection

Entropy can be used to detect anomalies in data. Anomalies often exhibit a higher degree of randomness or uncertainty as compared to normal data points. By calculating the entropy of each data point, one can identify those that deviate significantly from the expected distribution and potentially flag them as anomalies.

## Entropy alternativesEntropy alternatives

Entropy calculations depend on the accurate distribution of class labels and features. If the data is noisy or contains errors, the entropy-based splits may become less meaningful, leading to poor decision-making. Similarly, missing values can skew the entropy calculations.

In situations where the classes are highly imbalanced, entropy calculations become biased. A model might focus on the majority class, as the entropy-based split will be more heavily influenced by the dominant class, leading to poor generalization for minority classes.

In such scenarios, you may consider using entropy alternatives.

### Gini impurityGini impurity

Like entropy, Gini impurity measures the level of disorder in a dataset, but its calculation is simpler and computationally less expensive.

Gini impurity ranges between 0 and 0.5. A Gini impurity of 0 indicates perfect purity, meaning all instances belong to the same class. On the other hand, a Gini impurity of 0.5 represents maximum disorder, indicating a perfectly equal mix of classes.

Gini impurity is less sensitive to rare events (e.g., imbalanced datasets), making it more stable when dealing with noisy data. It is often preferred for classification tasks where computational efficiency is important, such as large-scale datasets or real-time applications.

### Balanced accuracyBalanced accuracy

Balanced accuracy is preferred over cross-entropy in assessing model performance when the number of examples in one class significantly outweighs those in another. In an imbalance scenario, if 90% of data belongs to a single class, a model can achieve 90% accuracy simply by always predicting the majority class, even though it may perform poorly on the minority.

Balanced accuracy computes the average of the true positive rates across all classes, providing a more nuanced understanding of the model’s performance.

### Hinge lossHinge loss

Hinge loss is an alternative loss function that quantifies the penalty of misclassification in binary classification tasks. (E.g., Classifying emails as spam or not spam). It may be better suited than cross-entropy for data with two classes as it maximizes the boundary between classes, which entropy does not do.

## ConclusionConclusion

Just like entropy, which measures chaos in thermodynamics, entropy in machine learning is a mathematical function that quantifies the randomness in a given dataset. ML models like decision trees use entropy in classification tasks. They attempt to minimize its value while analyzing data. The lower the entropy, the closer the model is to the final prediction.

Beyond classification, entropy also has applications in dimensionality reduction and anomaly detection. It helps you determine the relative correlation between data points. It can also be used as a loss function in model evaluation.

However, entropy is better suited for probabilistic data distribution and doesn’t work well with overly balanced or overly imbalanced datasets. You may have to choose different functions depending on your ML task. Mastering concepts like entropy, decision trees, and loss functions is crucial for anyone working in machine learning. If you’re looking to build a strong foundation in these core ML principles, a machine learning bootcamp can provide the structured, hands-on training you need to apply these concepts in real-world scenarios.

## FAQ

How does entropy prevent overfitting?

Entropy helps prevent overfitting by guiding the decision tree to make splits that reduce uncertainty the most. This encourages the creation of generalizable rules rather than rules that fit the training data too closely.

Can entropy be visualized in classifiers?

Entropy can be visualized indirectly by examining the decision tree itself. Nodes with higher entropy represent greater uncertainty, while nodes with lower entropy represent more confident decisions.

Is discretization needed for entropy with continuous features?

Yes, discretization is typically needed for entropy with continuous features. This involves converting continuous values into discrete bins, allowing entropy to be calculated more easily.

What role does joint entropy have in model interactions?

Joint entropy measures the uncertainty between two or more variables. In model interactions, entropy can help identify dependencies between features and guide the selection of appropriate model features.

What are entropy`s limits in decision trees?

Entropy can be limited by the complexity of the decision tree. If the tree becomes too deep or has too many branches, it can overfit the training data and perform poorly on unseen data.

How does entropy affect precision-recall balance?

Entropy does not directly affect precision-recall balance. However, the choice of impurity metric (entropy or Gini impurity) can influence the structure of the decision tree, which in turn can impact the balance between precision and recall.

Can entropy minimization cause bias?

Yes, entropy minimization can cause bias if the dataset is imbalanced. This is because entropy tends to favor splits that reduce the uncertainty for the majority class, potentially leading to biased predictions.

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

What is a feature in machine learning?

Features are essential to understanding data patterns and training machine learning models. Learn about their importance and generation techniques.

September 17, 2024
8 mins to read

### 

Open-source vs proprietary software

In this post, we’re comparing open-source and proprietary software, with a detailed focus on definitions, differences, key advantages and business models.

August 28, 2024
10 mins to read

### 

Unlocking the potential of few-shot learning

An end-to-end guide to understanding few-shot learning and its benefits against traditional supervised learning.

July 25, 2024
10 mins to read

Sign in to save this post
Sign In
