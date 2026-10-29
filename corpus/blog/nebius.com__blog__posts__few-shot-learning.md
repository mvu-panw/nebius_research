# Unlocking the potential of few-shot learning

Source: https://nebius.com/blog/posts/few-shot-learning

Skip to main content

Modern deep-learning models require extensive datasets for adequate training and understanding. However, obtaining such rich datasets is expensive and not always possible. Few-shot learning (FSL) allows models to understand new information using limited data samples.

FSL introduces meta-learning, which teaches models how to learn. The approach uses a support set to extract information for a new domain and adapt itself to it. This allows developers to extend the models’ capabilities as required and find applications in new areas.

## What is few-shot learning?What is few-shot learning?

Few-shot learning (FSL) is a modern paradigm in machine learning that allows artificial intelligence models to understand new information using very few data samples. This approach tackles the data hunger problems of traditional models by utilizing their existing knowledge to adapt quickly to new, unseen data. This form of learning is called meta-learning, which essentially means learning to learn.

The human brain can quickly grasp new information if it already has some background information or basis built for it. For example, if we see a new species of a bird, the brain has little trouble understanding its features since it already knows what a bird is. We only need to connect additional dots, such as the feather colors and overall shape. FSL works similarly: a pre-trained model has already captured features for various birds, and FSL helps connect the dots for a new species by using just a few training examples.

FSL is often explained as N-way-K-shot learning. N refers to the number of new additional classes the model will learn, and K is the number of data samples available for each class. A higher N would result in increased computation, while a smaller K would lead to poor results as the model has insufficient information to grasp. Overall, FSL is ideal for scenarios where data collection is challenging. It provides a resourceful and cost-effective method for expanding existing AI models and building new applications.

### Important terms related to few-shot learningImportant terms related to few-shot learning

Before diving into more technical details about FSL, let’s discuss some terms important for understanding the procedure.

- Support set: The support set is the training set for the FSL method. It contains a small number of samples for each new category to be learned. The model is expected to generalize over these samples and apply its learning in unseen scenarios.

- Query set: The query set is the test set for FSL. It can contain multiple samples for the same categories as the support set. However, the sample data in the query set does not overlap with the support set. The model is evaluated on this data after it has learned the support set information.

- N-way-K-shot learning: This learning technique defines the number of novel classes and the sample size of each class in a support set. For example, a 4-Way-4-Shot learning means 4 new categories, each having 4 data samples.

- One-shot learning: This subset of FSL uses only 1 training example per category.

- Zero-shot learning: Zero-shot learning allows a model to infer classes it has never seen before (no explicit training). It uses certain auxiliary information, such as text descriptions, to define the data, and the model must use its existing knowledge to classify information accurately.

## Why few-shot learning?Why few-shot learning?

Modern deep-learning models contain billions of parameters; training them from scratch is costly. It requires expensive hardware equipment, an extensive dataset, and several hours (sometimes days) to complete the training. In many cases, the unavailability of labeled datasets becomes a bottleneck for training.

Few-shot learning addresses these limitations of traditional supervised learning. It allows pre-trained models to extract new knowledge from limited data. Models can generalize to new information, predict new categories, and adapt to different data distributions (domain shift). FSL provides a cost-effective method for repurposing large-scale models and adapting them to new downstream tasks. The models learn rare categories using very few training samples, providing amazing results.

## How does few-shot learning work?How does few-shot learning work?

Due to its unique functionality, the few-shot learning algorithm works differently from traditional machine learning. While conventional models train themselves to predict classes for data points directly, FSL learns to compare two data points and conclude whether they belong to the same class. One data point belongs to the support set, while the other belongs to the query set.

Suppose we have a support set containing 3 classes and 5 samples for each class, making it a 3-way-5-shot learning problem. The training procedure uses a similarity function, such as the Euclidean distance, to calculate a similarity score between the support and query image. The algorithm trains itself to maximize the score between similar images and minimize dissimilar data points. During inference, the query image is compared with every image in the support set and is classified based on the similarity score.

Specialized networks like the Siamese network are purpose-built for FSL applications. The architecture uses two parallel-running neural networks to generate embeddings for input images and compare the output. The comparison is drawn using pairwise similarity, which compares pairs of data points, or triplet loss, which compares an anchor image to a positive (similar) and negative (dissimilar) example. Let’s look at the Siamese network in detail.

### Siamese networkSiamese network

A Siamese network consists of multiple (usually two or three) subnetworks running in parallel. This architecture is trained to act as a similarity function and generate a similarity score between inputs each branch receives. The neural networks act as feature extractors, creating embeddings for the input images. The embeddings are compared afterward for the similarity score. The backpropagation tweaks the model weights to generate embeddings that are either similar or different from each other, depending on the training samples. There are two key approaches to training a Siamese Network. Let’s look at each in detail.

#### 1. Pairwise similarity1. Pairwise similarity

This method uses two networks, usually pre-trained convolutional neural networks (CNNs), to process two images in parallel. The images are converted to an encoded representation, which is then flattened and concatenated together. The final embedding is a joint representation of both the input images. The final form is passed to a fully connected layer, calculating the similarity score as output. The ground truths for the network are 1 if the image is the same and 0 otherwise. The backpropagation algorithm tweaks the Siamese branches to bring the predictions closer to the labels.

The following code snippet uses Tensorflow to calculate pairwise cosine similarity for 2 input images.

import tensorflow as tf

def preprocess_image(image_path):
"""
Preprocesses an image for similarity calculation.

Args:
image_path: Path to the image file.

Returns:
A preprocessed image tensor.
"""
# Load image and convert to float32
image = tf.io.read_file(image_path)
image = tf.image.decode_image(image, channels=3) # Assuming RGB images
image = tf.cast(image, tf.float32)

# Resize image
image = tf.image.resize(image, (200, 200))

# Normalize image
image = image / 255.0 # Normalize pixel values to [0, 1]

return image

def pairwise_cosine_similarity(images):
"""
Calculates pairwise cosine similarity for a list of image paths.

Args:
images: A list of image paths.

Returns:
A tensor of shape [num_images, num_images] containing pairwise cosine similarities.
"""
# Preprocess images
preprocessed_images = [preprocess_image(path) for path in images]

# Flatten the images
flat_image1 = tf.reshape(preprocessed_images[0], [-1])
flat_image2 = tf.reshape(preprocessed_images[1], [-1])

# Calculate cosine similarity using vectorized operations
image_norm1 = tf.nn.l2_normalize(flat_image1, axis=0)
image_norm2 = tf.nn.l2_normalize(flat_image2, axis=0)

return tf.reduce_sum(tf.multiply(image_norm1, image_norm2))

# place the image paths in the list below
image_paths = ["image1.jpg", "image2.jpg"]
similarity_matrix = pairwise_cosine_similarity(image_paths)
print("Image Similarity:", similarity_matrix)

#### 2. Triplet loss2. Triplet loss

The triplet loss uses a slightly different approach by using three network branches. The approach starts with obtaining an anchor image from any given class. Next, we sample an image from the same class and another from a different image. These images are passed through the same neural network for transformation. In this scenario, the anchor image acts as the ground truth and a loss is calculated between the anchor and the other two samples. The loss is calculated as the square of the Euclidean distance between the two embeddings. The final loss is calculated as the max between zero or the difference between the two losses plus a margin value. Mathematically, it is written as:

Triplet Loss=max(0,∣∣f(ia)−f(i−)∣∣22−∣∣f(ia)−f(i+)∣∣22+α)\text{Triplet Loss} = max(0, ||f(i_a)-f(i_-)||^2 {}_2-||f(i_a)-f(i_+)||^2 {}_2 + \alpha)Triplet Loss=max(0,∣∣f(ia​)−f(i−​)∣∣22​−∣∣f(ia​)−f(i+​)∣∣22​+α)

Here,

- IaI_aIa​ represents the anchor image

- I−I_{-}I−​ represents the dissimilar sample

- I+I_{+}I+​ represents the matching image

- α\alphaα is the margin

The training aims to bring the positive image closer to the anchor in the latent embedding space and vice versa for the negative sample.

The following code snippet calculates the triplet loss between an anchor, a positive, and a negative image. It uses matrix operations and Euclidean distance to estimate how close or far apart the images are.

import tensorflow as tf

# Function to load and preprocess an image
def load_and_preprocess_image(image_path, target_size=(224, 224)):
image = tf.io.read_file(image_path)
image = tf.image.decode_image(image, channels=3)
image = tf.image.resize(image, target_size)
image = image / 255.0 # Normalize to [0, 1]
return image

# Function to compute Euclidean distance
def euclidean_distance(a, b):
return tf.sqrt(tf.reduce_sum(tf.square(a - b), axis=-1))

# Triplet loss function
def triplet_loss(anchor, positive, negative, margin=1.0):
# Flatten the images to 1D vectors
flat_anchor = tf.reshape(anchor, [-1])
flat_positive = tf.reshape(positive, [-1])
flat_negative = tf.reshape(negative, [-1])

# Compute the distances
pos_dist = euclidean_distance(flat_anchor, flat_positive)
neg_dist = euclidean_distance(flat_anchor, flat_negative)

# Compute the triplet loss
loss = tf.maximum(0.0, pos_dist - neg_dist + margin)

return loss

# Paths to the images
anchor_path = "anchor.jpg
positive_path = "positive.jpg"
negative_path = "negative.jpeg"

# Load and preprocess the images
anchor_image = load_and_preprocess_image(anchor_path)
positive_image = load_and_preprocess_image(positive_path)
negative_image = load_and_preprocess_image(negative_path)

# Compute the triplet loss
loss = triplet_loss(anchor_image, positive_image, negative_image)

print("Triplet Loss:")
print(loss.numpy())

## Applications of few-shot learningApplications of few-shot learning

FSL has gained massive popularity as it allows ML engineers to include new classes in models without any extensive dataset or training. It has developed applications for image classification, object detection, and semantic segmentation. Let’s look at these in detail.

### Image classificationImage classification

Since FSL’s basic principle is comparing data points, it can be used for image classification. The query image, taken from the query set, is compared against the target image from the support set. The similarity score between the two determines whether they belong to the same class.

However, Zhang et al. proposed a more advanced method of image classification using FSL and Earth Mover’s Distance (EMD). The paper proposes a network constructed using two CNNs. Each CNN extracts features from the image, which are used for comparison. The authors propose a novel technique that divides each image into segments and compares the localities using optimal matching. They use the EMD to generate structural similarity, and the algorithm updates the segment weights by modifying their brightness.

### Object detectionObject detection

The object detection problem uses ML to detect and localize various objects in images. Training a general-purpose object detection model is costly, and an FSL approach is a great way to use existing models for new problems. Perez-Rua et al. propose an incremental few-shot detection approach to add new classes to a base learner.

The authors use CentreNet as the base learner and employ a meta-learning strategy, forming the OpeN-ended Centre nEt (ONCE). The architecture includes a class-generic feature extractor and a class-specific code generator. The former extracts generic features from an input image, while the latter predicts class codes from a set of input support images. The two components are convolved to represent the object detection result as a heat map.

Additionally, the approach only requires a single pass of a sample to register a new class and does not require access to previous data. Overall, the FSL approach is efficient and maintains data privacy.

### Semantic segmentationSemantic segmentation

Semantic segmentation breaks an image into pixels and classifies each pixel individually. As each pixel has its own label, the overall image becomes a segmented map that precisely identifies each object or element in the frame. Few-shot learning approaches allow semantic segmentation tasks to identify new objects using a few training samples.

Liu et al. propose a network that uses part-aware prototypes to extract details from the query image set. The model uses a CNN backbone network for feature extraction from support and query images. It then uses a Prototype Generation Network to create a set of part-aware prototypes that identify and pool features from different parts of the image. The approach also includes unlabeled data in the prototype generation network to better model intra-class variation. Finally, a part-aware mask generation network uses the query image feature to predict a segmentation mask.

### RoboticsRobotics

The modern robotics industry teaches robots to mimic human actions like walking, jumping, or general tasks like picking up objects. Teaching robots new procedures can be conducted using FSL. They can be shown a few examples of a certain task and taught to generalize the action in different environments and conditions. FSL helps with generalized path planning or arm movements from demonstrations.

Wu et al. propose a novel approach to facilitate imitation learning in robots. Their approach builds a unique computational model that allows a robot to learn invariant feature points from a provided movement. Simply put, a robot can learn a certain arm movement from an example and recognize the points involved. It can then generalize that movement and can perform a different but similar movement by recognizing similar points between the two paths. It is a single-shot approach, as the robot only requires a single example to capture all its needed features.

### Natural language processing (NLP)Natural language processing (NLP)

NLP is becoming increasingly popular with the advent of LLMs however, text data labeling is a big challenge. Few-shot learning allows easy training of models for tasks like text classification. Modern approaches use embedding networks to generate latent representations of the text. The embeddings are then matched with a query text using metric learning approaches. They also utilize task clustering to combine multiple metrics for target tasks.

## Meta-learning algorithmsMeta-learning algorithms

Meta-learning algorithms can be further classified as data-level, parameter-level, metric-learning, and gradient-based meta-learning. Each algorithm approaches the meta-learning paradigm differently and aims to improve the outcomes. Let’s discuss the algorithms in detail.

### Data-levelData-level

Data-level meta-learning uses different techniques to overcome data limitations in FSL. Some key techniques include expanding the dataset, data augmentation, or adding unlabeled samples. A meta-learning algorithm can underfit or overfit the limited data so the before-mentioned techniques are necessary.

Data augmentation involves rotating, cropping, or adding noise to the existing images and making the new ones part of the support set. This allows the algorithm to pick up variations in the image details. Adding unlabeled images creates a semi-supervised learning environment, which can also improve results.

Moreover, generative models like Generative Adversarial Networks (GAN) are used to generate new data samples. Since the synthesized data comes from the same distribution, it is made part of the support set and aids with the model learning.

### Parameter-levelParameter-level

Another method for tackling overfitting is by optimizing the model parameters to learn just the key features from the few data samples. Parameter-level FSL uses meta-learning to intelligently focus on the key features and update parameters accordingly. This is achieved by constraining the parameter space using regularization techniques.

Moreover, approaches like Model-Agnostic Meta-Learning (MAML) use knowledge from previous tasks in the same domain. They use parameters from a different task as a starting point to optimize the parameter route during meta-learning.

### Metric learningMetric learning

The metric learning approach uses distance measures to compare two data points and generate a similarity score. Practically, we can use CNNs to generate image embeddings. The embeddings can be passed to a distance function like Euclidean distance, Jacobian distance, or Earth Mover’s distance to calculate the similarity between the embeddings. The similarity score helps determine whether the two samples fall in the same class.

A popular algorithm under metric learning is the Siamese network, which uses two or more networks to generate data embeddings and a similarity score.

### Gradient-based meta-learningGradient-based meta-learning

Gradient-based meta-learning is based on a student-teacher model. The teacher is the base learner, which contains all the necessary knowledge for a specific task. It is trained on the support set in episodes to make predictions on the query set. The classification loss derived from the teacher model is then used to train the student model, making it proficient in the classification task.

## Algorithms for few-shot image classificationAlgorithms for few-shot image classification

Various algorithms meta-learning have been built for few-shot image classification. Let’s discuss four key algorithms in detail.

- The Model-Agnostic Meta-Learning (MAML) is a learning approach that can be applied to any learning model trained with gradient descent. The gradient-based meta-learning approach optimizes the parameter initialization to give the learner a good starting point. The approach achieves optimal fast learning on a new task with only a few gradient steps, avoiding overfitting. Initially, a base neural network is trained till a few gradient steps to obtain a set of parameters. The algorithm samples a set of image classification tasks, and each task is trained sequentially, with the parameters updated after each task. When the training run is complete, the fine-tuned model is evaluated on the query set images, and the initial model parameters are updated.

- Matching networks consist of a classifier, such as a CNN, for image classification tasks. The CNN is used to generate embeddings for a query image and a set of support images. The image embeddings are then compared using an attention kernel consisting of a cosine distance function followed by a softmax operation. The calculated cross-entropy loss is backpropagated towards the classifier. The final predicted class for any given query image is the weighted sum of the support set labels, the weights being the similarity score between the query and support image.

- Prototypical networks work similarly to matching networks, but instead of using individual image samples, they create class prototypes. They still use a CNN architecture to generate embeddings, but the embeddings for the support set are averaged together for each class. The final singular embedding represents the entire class in the embedding space, and the final goal is to move the query image closer to its targeted class. The network classifies images by using a relevant metric like Euclidean distance to find the closest matching class prototype.

- Relation networks consist of an embedding module and a relation module, both of which have a neural network architecture. The embedding module encodes the input support and query images to the embedding space. The embeddings are then concatenated and passed to the relation module neural network, which acts as the distance function. The module predicts a distance score between the two embeddings, which allows classifying the unlabeled query image.

## ConclusionConclusion

Few-shot learning allows machine learning models to adapt to new domains without extensive retraining or fine-tuning. The approach uses a few sample data points, known as the support set, and learns their key features to make predictions on unseen examples. The approach is called meta-learning and often relies on distance metrics to calculate the similarity between different data samples. The similarity scores help place unseen data within the available classes.

It is an efficient approach that allows fast adaptation and repurposing of existing models for new downstream tasks. It has found various applications in practical use cases especially for image classification and object detection. Developers can easily extend an existing classifier to include new classes and use the same model in various situations.

## FAQ

What is the difference between one-shot learning and few-shot learning?

One-shot learning uses only a single training example to learn a new class, whereas a few-shot uses a few more, usually 4 or 5.

What is the difference between few-shot and active learning?

Few-shot learning aims to train models with few examples per class, which is useful in data-scarce scenarios. Active learning involves models querying human annotators for the most informative data points to minimize labeling efforts and improve performance.

Is few-shot learning supervised or unsupervised?

Few-shot learning is supervised as the support set contains labeled data.

What is the main challenge of few-shot learning?

The main challenge of few-shot learning is to adequately teach a model about new categories of information using very few data points.

## Explore Nebius AI

Get started​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

What is epoch in machine learning? Understanding its role and importance

What is an epoch in machine learning? Learn how epochs, batch size, stochastic descent gradient and iterations influence neural networks in deep learning.

July 23, 2024
10 mins to read

### 

Fundamentals of LoRA and low‑rank fine-tuning

In the next installment of our series of deep technical articles on AI research, let’s switch our attention to the famous LoRA, a low-rank adaptation technique.

May 13, 2024
11 mins to read

### 

Data preparation for LLMs: techniques, tools and our established pipeline

Let’s explore methods and technologies for maximizing efficiency in data collection and preparation for training large models. I will outline the pipeline in detail and discuss our own chosen workload for dataprep.

June 27, 2024
16 mins to read

Sign in to save this post
Sign In
