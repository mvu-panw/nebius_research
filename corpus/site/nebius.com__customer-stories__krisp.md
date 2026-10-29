# Krisp’s advancements in real-time voice AI

Source: https://nebius.com/customer-stories/krisp

Skip to main content

## Technology and client baseTechnology and client base

Krisp’s work with us lies in the field of Accent Localization, an AI-powered realtime voice conversion technology that removes the accent from call center agent speech resulting in US-native speech. The goal is to improve the clarity and comprehension in human-to-human communication, when the agent — located, say, in India — talks to a US-based customer.

Krisp is a leading AI-powered noise cancellation technology company that enhances voice communication by eliminating background noises and voices in real-time. Founded in 2017, the company has revolutionized the way professionals and businesses communicate by providing crystal-clear audio for remote meetings, calls, and recordings. As a high-growth startup, Krisp continues to innovate and recently shipped products based on in-house developed on-device Speech-to-Text and Accent Localization technologies.

## ContentsContents

AI models

Data handling and storage

Model evaluation

Key highlights of working with Nebius AI

Lessons learned and future directions

## AI models

Krisp uses a mix of modern transformers, convolutional networks, and conformer networks to train and inference their Accent Localization (AL) models. Their research and engineering teams put a special focus on efficiency and high quality resulting in compact AI models, as their solution generally must run on low-powered PCs and thin clients typical for call center environments. This sets them apart from large language models (LLMs) that are typically trained and run on high-powered GPUs in cloud.

However, before building those efficient on-device models, Krisp’s team has to train a much larger foundational voice conversion model. This is where the need for powerful GPUs emerged.

After a competitive evaluation, Nebius AI was selected as a preferred vendor given our reliable, high performant AI-centric cloud solutions.

The foundational model takes about two weeks to train on a single NVIDIA H100 GPU. Often, Krisp had to train tens of different versions of this model through various experiments to select an optimal one with highest possible quality. Next, they would train a real-time version of the AL model, with much stricter requirements on the CPU footprint and latency.

Finding the right balance between model size, performance and quality was a challenge that pushed the team to focus on making their algorithms more efficient, rather than just making the models bigger.

## Data handling and storage

Large, high-quality datasets are critical in Krisp’s training process. They work with fairly large datasets, usually around 2 to 2.5 terabytes in size. The team uses a combination of datasets from different sources — data acquired from the third party service companies, data synthesized in-house, data carefully cleaned from publicly available sources.

Additionally, to make its algorithms more robust, Krisp uses various data augmentation techniques to feed the models during the training process. For example, they make sure their accent localization technology can work well in a highly noisy, busy call centers where agents might be sitting close together.

Preparing all this data on the fly during the training requires a lot of high performance storage, to ensure maximum GPU utilization and lower time to results. Here, Nebius accommodate this need by providing direct attached high-speed SSDs to move large amounts of data between the GPUs.

## Model evaluation

Evaluating the quality of accent localization models is not a straightforward process. Krisp used a combination of objective metrics and subjective testing to ensure high-quality output. They look at things like how natural the speech sounds, whether the pronunciation is correct, and how accurately the words and sounds are reproduced.

Krisp’s engineers have developed their own ways to measure how natural the speech sounds, as there aren’t widely accepted industry standards for this. They also check that words aren’t distorted in the output speech, which is crucial for maintaining the meaning and intent. Among others, they use metrics like word error rate (WER) by comparing the transcription of the converted speech to the original and phoneme error rate (PER) for assessing pronunciation accuracy.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Key highlights of working with Nebius AI

- 

As mentioned, Krisp’s work with Nebius AI targeted training of their foundational voice AI models for accent localization. The secondary goal was get acquainted with the capabilities and performance of their H100 GPUs. They found that a single H100 GPU completed the training process 50–80% faster than the A100 GPU they were familiar with.

- 

Krisp found the Nebius infrastructure to be very stable, with only one planned downtime during an intense 3-month collaboration, which was communicated well in advance.

- 

They were also impressed with the quality of support and onboarding with one of our cloud solutions architects, noting that they were able to transfer data and start training within a day of an initial discussion.

- 

They ask for VM option with greater CPU power for H100s, and we will consider that.

- 

They expressed high satisfaction from our collaboration, given that they met their tight product research and development timeline, plus valuable insights into working with H100 GPUs, highlighting areas where they could improve their training processes for the future.

## Lessons learned and future directions

Working with Nebius AI, Krisp have made significant progress in developing real-time, on-device AI solutions, particularly in the area of accent localization. It also gave Krisp valuable insights into using advanced GPU systems and cloud infrastructure. They learned a lot about what H100 GPUs can do and identified ways they could improve training processes to make better use of this hardware.

Krisp’s challenge here is switching to more complex distributed training setups. The team, while knowing its own infrastructure well, sees a need to develop better ways of using a distributed GPU cluster to really benefit from cloud systems like Nebius AI has.

Looking ahead, Krisp plans to continue optimizing their real-time models based on the foundational models developed on our platform. They’re thinking about supporting more accent types in the near future, which will require new foundational models and provide further collaboration opportunities.

## Nebius services used

### Compute Cloud

Providing secure and scalable computing capacity for hosting and testing your projects. GPU-accelerated instances use top-of-line NVIDIA GPUs.

Learn more​
Docs​

### Virtual Private Cloud

Providing a private and secure connection between Nebius resources in your virtual network and the Internet.

Learn more​

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

Unum

In our field, effective partnerships that harness complementary strengths can drive significant breakthroughs. Such is the case with the collaboration between Nebius and Unum, an AI research lab known for developing compact and efficient AI models.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
