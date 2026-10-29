# How Unum partnered with Nebius to preserve knowledge in compact models

Source: https://nebius.com/customer-stories/unum

Skip to main content

## Partnership that makes us proudPartnership that makes us proud

In our field, effective partnerships that harness complementary strengths can drive significant breakthroughs. Such is the case with the collaboration between Nebius AI and Unum, an AI research lab known for developing compact and efficient AI models.

Unum specializes in training multimodal models that enhance perception and search capabilities. These models are hybrid, incorporating various transformers. Often, they start with pre-trained weights from individual components and undergo extensive fine-tuning on custom datasets. This process makes it challenging to determine the training duration for the entire model, as it involves training each component separately before the hybrid.

## ContentsContents

Models and architectures

Technical challenges

Data quality

Benchmarking the models

Going forward

## Models and architectures

To date, Unum has trained and open-sourced four models in partnership with us, all available on Hugging Face for everyone to experiment with:

- UForm-Gen2, a scaled-down version of the UForm-Gen, which was already among the industry’s smallest multimodal generative models.

- UForm-Gen2-dpo, implementing the same idea, this time using the direct preference optimization (DPO) paradigm.

- UForm-VL-English in two versions, which are small and large multimodal encoders that help to understand and search visual and textual content.

The company specializes in training multimodal models that enhance perception and search capabilities. These models are hybrid, incorporating various transformers. Often, they start with pre-trained weights from individual components and undergo extensive fine-tuning on custom datasets. This process makes it challenging to determine the training duration for the entire model, as it involves training each component separately before the hybrid.

For instance, Unum’s first collaborative model with Nebius, the UForm-Gen2, utilized Unum’s visual encoder, a text encoder and a decoder from Qwen by Alibaba Cloud. Training this hybrid model took approximately one day on eight NVIDIA H100s. However, preparing the individual components took considerably longer: five days for the visual encoder, two additional days to retrain the Qwen component and extra time for the text encoder. Therefore, the complete end-to-end training process extends well beyond a single day and does not include the time required for data sourcing, compilation, cleaning and organization.

A key feature in a multimodal setup is the use of contrastive loss, which is crucial for aligning various vector spaces, whether in encoders or decoders. Unum’s approach is somewhat similar to OpenAI’s CLIP model, frequently used in multimodal tasks. However, Unum’s models are smaller and more data-efficient, allowing faster training and improved performance in search tasks. Among other companies, Salesforce is also exploring similar technologies with their ALBEF model, but Unum aims to surpass both Salesforce and OpenAI in efficiency.

Unum finds the entire realm of multimodal search and chat intriguing because it represents a step towards more sophisticated artificial intelligence. Humans do not rely solely on text; we integrate text with visual, auditory and tactile inputs. Thus, adopting a multimodal approach is essential for both the industry and for advancing research.

## Technical challenges

The biggest challenge Unum faces is the speed of data loading. Sometimes, the fluctuating metrics suggest that the model is not converging. This typically indicates problems with either the data or, more frequently in Unum’s case, the model’s size. When you develop some of the smallest multimodal transformers in the industry, ‘I/O to computing power’ ratios become an ever-growing concern. Data access here includes loading and on-the-fly decoding of images and videos, a highly I/O-intensive task, ruling out anything related to storage virtualization like remote disks or S3-compatible object storage.

Traditional methods often struggle to contain so much knowledge within such a compact model. There aren’t many solutions to this; perhaps one option is to simply build a larger model. As known, larger models are generally easier to train than smaller ones, especially if you expect the same quality from a small model as from a large one. Building a larger model might seem like a straightforward solution, larger models are generally easier to train and can deliver similar quality without the constraints of smaller models.

OpenAI addressed some of these challenges by using vast amounts of training data. Although they likely use more advanced methods now, they haven’t released any new models recently. In contrast, Unum’s approach is highly data-efficient and less demanding in terms of computational resources, which makes their models both cost-effective and capable of running on a wide range of devices, including mobile phones, IoT devices and smart watches.

Ideally, Unum’s data should be stored on local disks to maximize GPU utilization, which is why they maintain their own on-premise solution with high-speed SSDs. Unum has not fully integrated this system with Nebius infrastructure; instead, they have divided workloads, conducting some experiments on Nebius and others in different cloud and on-premise environments.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Data quality

Unum demonstrated an importance of data quality a year ago with their first public models, achieving superior search performance using a smaller but higher-quality dataset compared to the original CLIP’s training on 400 million low-quality image-text pairs. Unum’s model, trained on 4, 9 and 25 million high-quality samples, outperformed CLIP’s search quality.

Unum sources data from public datasets, which is then extensively augmented and enhanced. While they do not make their datasets public, they invest considerable time and effort in their improvement. The company releases only the final checkpoints of their models, not the intermediate ones. This contrasts with some teams that release semi-finished checkpoints, which may be less polished. For Unum, only the checkpoints that significantly contribute to industry standards are released, typically after numerous rounds of refinement.

## Benchmarking the models

Currently, there are only a few benchmarks suitable for the multimodal domain. Unum utilizes different evaluation methods for their embeddings and generative models, each serving distinct purposes.

- For embeddings, Unum measures retrieval effectiveness by building a search pipeline on datasets like the publicly available MS COCO, which they have also translated into various languages to assess search quality across linguistic barriers.

- Another commonly used benchmark is zero-shot image classification, where a model untrained on specific classification tasks must categorize images into predefined classes. This benchmark often employs the ImageNet dataset, but Unum avoids using it if the dataset has been included in training, as it would unfairly skew the results.

- The generative benchmarks, focusing on captioning and visual question answering (VQA), present even greater challenges. Captioning requires describing what is depicted in an image, while VQA involves answering questions based on an image. Despite the existence of benchmarks like CLIPScore, which measures how well a caption corresponds to an image, these can be unreliable if the model outperforms or differs significantly in style from the benchmark’s baseline, CLIP.

Unum also extensively uses various VQA datasets to evaluate their models. However, the company doesn’t restrict releases based on achieving specific scores. Instead, Unum prioritizes overall improvements in model performance, even if certain benchmarks show a decline.

## Going forward

Unum is now turning its focus towards enhancing video capabilities, ideally in collaboration with Nebius. Although dealing with the V100-equipped machines was challenging, they are actively exploring video search and video question answering.

Moreover, Unum is exploring the potential for privacy-preserving chat applications that operate entirely on a user’s device, addressing privacy concerns and compliance with NDAs. This capability is particularly valuable in sensitive environments like financial institutions, where data privacy is crucial.

Applications for mobile devices and IoT are especially relevant for Unum, given the necessity of training smaller models for such platforms. Several European and American publishers have adopted Unum’s search libraries for mobile devices, and some are implementing features similar to Google Photos, allowing for on-device text-based searches that preserve user privacy.

As Unum’s engineers look to the future, they recognize the challenges ahead but remain optimistic about overcoming them. The outlook is promising, especially with strong partnerships and continuous innovation in data management and model deployment.

## Nebius services used

### Compute Cloud

Providing secure and scalable computing capacity for hosting and testing your projects. GPU-accelerated instances use top-of-line NVIDIA GPUs.

Learn more​
Docs​

### Object Storage

Secure, scalable and cost-effective cloud object storage. Store, easily access, share and manage large amounts of unstructured data.

Learn more​
Docs​

## More exciting stories

## 

Recraft

Recraft, recently funded in a round led by Khosla Ventures and former GitHub CEO Nat Friedman, is the first generative AI model built for designers. Featuring 20 billion parameters, the model was trained from scratch on Nebius.
Read the story

## 

Dubformer

Dubformer is a secure AI dubbing and end-to-end localization solution that guarantees broadcast quality in over 70 languages. The company manages two of its most resource-intensive tasks on Nebius: ML itself and the deployment of models.
Read the story

## 

Krisp

Krisp’s work with us lies in the field of Accent Localization, an AI-powered real-time voice conversion technology that removes the accent from call center agent speech resulting in US-native speech.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
