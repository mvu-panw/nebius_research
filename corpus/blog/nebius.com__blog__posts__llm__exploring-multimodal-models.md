# Exploring multimodal models: integrating vision, text and audio

Source: https://nebius.com/blog/posts/llm/exploring-multimodal-models

Skip to main content

Humans experience the world via multiple modalities. We see, listen and feel multiple elements, and these inputs allow us to understand our environment better. Multimodal models replicate the same behavior by integrating various data inputs into the same feature space.

Multimodal machine learning models combine computer vision and natural language processing to understand diverse information. The features of the different modalities provide a deeper understanding of the task at hand. Powered with enhanced understanding, the models can mimic human-like interactions and yield improved results for downstream tasks.

## What are multimodal models?What are multimodal models?

Modern artificial intelligence systems can understand different data types simultaneously. These multimodal ML models can understand the interaction between multiple modalities, such as text, images and audio data. The data fusion capabilities allow them to understand different aspects of the problem and construct high-performing AI systems.

Multimodal systems deal with multiple modalities as both inputs and outputs. They can process multiple modalities as inputs to construct an output or process one modality and output another, such as in text-to-speech applications.

## The magic behind multimodal modelsThe magic behind multimodal models

Behind the scenes, multimodal models utilize transformers to process information. Transformers divide the diverse modalities into segments and analyze the relationships between different segments, paying more attention to the important parts.

Each input modality is first converted into embeddings, a vector structure understood by transformers. Images are converted to patches, while text is tokenized. The embeddings are combined into a unified representation space for processing. Data fusion can occur at either the very start of the training, mid-training (in the middle layers), or at the end once the transformer individually processes the embeddings. The selection of the optimal data fusion process depends on the type of task and is determined via experimentation.

## Multimodal learning in computer visionMultimodal learning in computer vision

The advent of multimodal architectures has brought various interesting applications in the computer vision space. Many of these applications take existing use cases and enhance them using multimodal reasoning. Some popular applications of multimodal AI include:

- Visual Question Answering

- Text-to-image Generation

- Natural Language for Visual Reasoning

These models process information from multiple modalities to understand vision and language in a human-like manner. This section will explore the applications in detail, discussing their architectures and use cases in practical situations. We will also discuss some popular multimodal models that implement the applications.

### Visual question answering (VQA)Visual question answering (VQA)

Conventional chatbots can process human inputs and correspond accordingly but are limited to textual information. Visual Question Answering (VQA) models can understand visual data in the context of text inputs. They can accept images and corresponding sentences to conduct human-like conversations.

As the name suggests, VQA models answer questions about a provided image. For example, the user may provide an image of a family picnic and ask the model to describe it. They can also ask follow-up questions like what each person is doing in the image or what time of day is represented.

Top VQA models, like LLaVA or the PALI, are based on the transformer architecture and utilize data fusion for enhanced understanding. These models also display capabilities like understanding tabular information and charts and deriving statistical analysis from just images.

### Text-to-image generationText-to-image generation

Generative artificial intelligence (GenAI) has been the highlight of the AI revolution, and one of its most popular applications is text-to-image generation. These models can generate entire images from scratch using text prompts as descriptions. Depending on the prompts, the generation models can create images with different art styles and unique visuals.

OpenAI’s DALL-E and StabilityAI’s Stable Diffusion are two of the most popular text-to-image generation models. DALL-E is a transformer-based deep learning network that uses its understanding of the data to generate raw pixels. Diffusion models, on the other hand, work similarly to generative adversarial networks (GANs).

They start by adding noise to the data and then gradually remove it, forming the required image step-by-step. The latest releases from both models display amazing results. However, DALL-E is closed, while stable diffusion is open-source; the former is known for its photorealistic accuracy, while stable diffusion’s results are more artistic and creative.

Text-to-image generation models have several use cases in the creative space. They are used to generate graphic designs, logos and general royalty-free images for different purposes. They are also fused into modern large language model (LLM)-based chatbots like GPT4 and MS Copilot for users to play around with.

### Natural Language for Visual ReasoningNatural Language for Visual Reasoning

NLVR is a multimodal machine learning task that evaluates the model’s visual understanding. These models learn to understand the different aspects of an input image, such as the colors, shapes and sizes of the objects present. The understanding is then evaluated against a description of the provided visual. The model tries to judge whether the image matches the provided description or not.

Microsoft’s BEiT-3 model is a popular model from the NLVR family. The general-purpose AI is a multiway transformer-based model that has achieved state-of-the-art (SOTA) results in both vision and language-related tasks. It has beaten previous works in tasks like Visual Question-Answering, Image Captioning and Visual Reasoning on popular datasets like COCO, NLVR2 and VQAv2.

## What is multimodal deep learning?What is multimodal deep learning?

Traditional deep-learning models have achieved amazing results but are limited by their ability to handle only a single modality. Simple architectures like convolutional neural networks (CNNs) are purpose-built for understanding particular data types and cannot capture multimodal contexts for deeper understanding.

Multimodal deep learning is the latest advancement in the AI space that allows models to work with multiple modalities. These models leverage data fusion to simultaneously process text, images and audio. This allows them to improve performance on basic machine-learning tasks like image classification and build advanced applications like text-to-image generators.

## How does multimodal learning work?How does multimodal learning work?

Deep learning multimodal architectures are composed of 3 distinct components. These are:

- Unimodal encoders

- Fusion network

- Classifier

The unimodal encoders are multiple standalone encoders built to process particular data types. For example, we will have two encoders for a text-to-image model, one for processing text and the other for images. The next step is to map the individual encodings onto a unified latent space using a fusion network. These networks are the backbone of multimodal processing and are often based on the transformer architectures. The last stage is a classifier, which is trained for downstream tasks, producing the final output.

### Encoding stageEncoding stage

Encodings are a vector representation of unstructured data like text or images. The encoding stage carries out feature extraction for the provided data. The features are stored as vectors and help the model learn data patterns.

The encoding stage involves multiple unimodal embeddings depending on the modalities involved. For example, for text, we may use popular models like Word2Vec or BERT, and for images, we may use OpenAI’s CLIP model. General models like Data2Vec can also be utilized to process text, video and audio data. Many of these models utilize attention mechanisms to generate informative data representation.

ML engineers often select embedding models based on their benchmark performance and the task at hand.

### Fusion moduleFusion module

Once embeddings are created, their knowledge must be combined into a unified space. The embeddings are passed onto the fusion module, where they are combined using the defined techniques. Simpler fusion techniques involve plain concatenation or a weighted sum of the embeddings to form a single unit. However, these techniques do not capture complex cross-modality relationships and are troubled by challenges like uneven dimensions.

Some advanced techniques use attention mechanisms to assign weightage to different parts of the embeddings. Other techniques involve multilayer perceptron (MLP) networks to learn non-linear transformations from the concatenated representations. The technique selection depends on the embedding, dimensionality, modality type and task.

The fusion itself can be performed at different stages. These include:

- Early fusion: This combines the modalities immediately after embedding creation.

- Intermediate fusion: This is a middle ground where features are extracted from each modality to some extent, and then the intermediate representations are fused before further processing. This offers more flexibility and can capture some interactions between modalities.

- Late fusion: This allows each modality to be processed by an independent dedicated network, and the final outputs are combined. It allows for finer feature extraction and better individual results.

### ClassificationClassification

The final step of the pipeline is a classification module that uses the fused modalities to make predictions or decisions. It includes a multi-layer neural network trained for a specific task. Depending on the class labels and type of prediction, the layer can include popular functions like sigmoid or softmax. The output of this layer is the final prediction that the model requires. In the case of a classifier, the output will be the class label seen during training.

## Significance of multimodal modelsSignificance of multimodal models

Multimodal models bring us closer to mimicking human behavior by understanding multiple inputs simultaneously. Their ability to process visual cues and textual cues in the same context allows for a holistic understanding of the world.

Multimodality is a significant leap in AI that enables machines to comprehend and respond to content in a way that resembles human perception. It improves AI robustness and performance for various practical applications.

### Enhanced understandingEnhanced understanding

Combining information from different sources provides a deeper understanding of the data. It gives the model multiple perspectives to train itself and make better judgment calls for downstream tasks.

### Improved robustnessImproved robustness

Having multiple sources means the model is more stable against data variations. Even if one modality displays ambiguity or drift, the model can refer to other sources for making accurate predictions.

## Applications of multimodal modelsApplications of multimodal models

The introduction of multimodality has given rise to various interesting practical applications. Some popular ones include:

- Image captioning

- Visual Question Answering (VQA)

- Language translation with visual context

Let’s discuss these further.

### Image CaptioningImage Captioning

Modern models can generate text descriptions of input images. These models learn to extract relevant features from images to form a visual understanding and map it to the relevant text tokens. The model generates textual information as an output that accurately describes the events seen in the image.

Such models form the basis for aiding applications for the visually impaired and for the automated generation of captions for social media posts.

### Visual Question Answering (VQA)Visual Question Answering (VQA)

A VQA model combines image understanding with natural language processing to converse regarding a visual input. It can hold full-length conversations and generate accurate responses regarding a reference image.

### Language Translation with Visual ContextLanguage Translation with Visual Context

Combining text input with visual context helps improve contextual accuracy for translation tasks. The additional contexts help in ambiguous situations where a unimodal input might not be sufficient for deciphering the translation.

## Multimodal learning challengesMultimodal learning challenges

Despite being a revolutionary approach, multimodal architecture accompanies certain unique challenges. Many of these challenges relate to capturing and combining information from the various modalities. Let’s understand these challenges in detail.

### RepresentationRepresentation

Multimodal architectures use diverse modalities, such as text, image, video and audio. These modalities have unique structures and require different algorithms to form vector representations.

The challenge arises when the different representations are combined for multimodal learning. Engineers must form representations such that their combination preserves the original characteristics while capturing cross-modal relationships. Having improper representations can lead to the model failing to generalize well and prioritizing one modality over the other.

Two popular approaches, joint and coordinated representations, are used to solve this. A joint representation maps all modalities to the same space. Joint representations are beneficial when the modalities are similar and present during the training and testing phase. Coordinated representations use a coordinated space to process embeddings separately but keep similar elements nearby.

### FusionFusion

The fusion modules combine the various modalities present in the model inputs. They aim to create a unified representation that helps make better decisions than unimodal approaches.

The challenge with fusion is choosing the optimal fusion technique. Techniques like concatenation are simpler to implement but do not capture complex relationships. Moreover, advanced techniques that utilize attention mechanisms apply higher weightage to appropriate portions but are challenging to implement.

### AlignmentAlignment

Some multimodal applications, like text-to-speech, require accurate data point alignment. During the fusion process, the relevant words must be aligned with the relevant speech segments for complete understanding.

Statistical models like the hidden Markov model can estimate the alignment between different modalities. Moreover, dynamic time warping can align modalities by compressing or dialing them against time.

## ConclusionConclusion

Introducing multimodal models has opened up various avenues for practical applications. While conventional ML models are limited by their unimodal understanding, the multimodal approach integrates information from various sources and grasps deeper contexts. These models can simultaneously understand images, audio and text and develop a human-like understanding for improved outcomes.

Multimodality has the potential for various exciting applications, like text-to-image generation, image captioning and Visual Question Answering (VQA). However, multimodal development accompanies various challenges, including creating a unified representation, selecting the optimal fusion technique and modality alignment.

The current state of multimodal models is impressive; however, they hold great potential for future developments. Currently, most models process two modalities, but they may include more in the future. Moreover, multimodality is a leap towards artificial general intelligence (AGI), and we might see its applications in humanoid robots that understand and feel the environment just like humans.

## FAQ

What are the implications of multimodal models for user privacy and data security?

Multimodal models hold the same data concerns as conventional AI. Model development must follow data regulation guidelines posted by authorities like HIPAA and GDPR. The data should be secured using state-of-the-art protocols, and similar protocols should be implemented during model deployment.

How do multimodal models enhance user experience in interactive systems?

Multimodal models process multiple data modalities like text and images simultaneously. This allows them to produce human-like interactions and enhance user experience.

What are the challenges in training multimodal models with limited data?

Limited data may result in insufficient model training, drastically impacting model performance. Additionally, an imbalance between the different modalities can cause the model to understand one better than the other.

How does the integration of multiple data types impact the performance of AI models?

Combining multiple data types gives the model a broader context and perspective, enhances its understanding capability and improves performance.

What role do multimodal models play in the advancement of autonomous systems?

Multimodality allows systems to utilize multiple data streams for a better understanding of the information. It significantly improves the system’s performance and reduces the need for human intervention.

How can multimodal models improve the accessibility of technology for users with disabilities?

Multimodal models power various applications for users with disabilities. They can generate image descriptions for the visually impaired, convert hand sign gestures to audio speech for the mute and perform speech-to-text for the deaf.

What are the future trends in the development of multimodal AI technologies?

Some key future trends include the inclusion of more modalities in a single model. Better unified representations and development of more efficient models for faster performance.

## Explore Nebius AI

Get started​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## Products and tools

Compute Cloud​
Managed K8s​
Managed databases​
Object Storage​

## See also

### 

Data governance and data security: what’s the difference?

Learn about data governance and security, their role in managing an organization’s data assets, and key differences in goal, scope, components, and relationship.

May 14, 2024
6 mins to read

### 

ModelOps: mastering AI model lifecycle

Model operationalization (ModelOps) is an ideology that aims to streamline the development and deployment process for AI applications. Let’s get deeper into the topic, understand differences between ModelOps and MLOps, and explore ModelOps use cases.

May 1, 2024
7 mins to read

### 

Nebius AI is now open to everyone

We’re excited to announce that our platform is now officially open to everybody. Whether you are a company or an individual engineer, access the GPU cloud console straight away and start running your machine learning experiments.

April 30, 2024
1 min to read

Sign in to save this post
Sign In
