# xAID: Training a foundation model for AI-assisted medical imaging

Source: https://nebius.com/customer-stories/xaid

Skip to main content

## PremisePremise

xAID is building the ultimate AI assistant for medical imaging. Trained on a unique dataset of real-world chest and abdominal CT scans, xAID’s large-scale 3D transformer model is built to identify emergency pathologies and non-acute conditions with millimetric precision. With training cycles lasting over five days on noisy clinical data, xAID relies on Nebius AI Cloud for uninterrupted, high-performance computing at scale and expert MLOps support — enhancing training stability and efficiency so xAID can focus on improving patient outcomes.

xAID brings medical and technology experts together to address a critical need for accurate diagnostic support in Emergency Departments amid a global radiologist shortage. By expanding diagnostic capabilities with state-of-the-art AI, xAID empowers healthcare professionals to focus on complex, high-priority cases while supporting early detection with opportunistic screenings.

## ContentsContents

Generalizing a unique, real-world dataset: operating globally

Telling the signal from the noise: training on noisy classification data

Managing high-resolution input under memory limits

Enhancing training efficiency for diagnostic precision

Building a 3D Swin Transformer, the ideal model architecture for medical imaging

Next steps: towards a smarter, more comprehensive AI assistant

Imagine you’re getting a CT scan at the Emergency Department for Covid-19 symptoms, but a calcium buildup in your coronary artery is missed by radiologists. Wouldn’t you want a silent threat like this to be identified as early as possible — ideally, while you’re already in the hospital?

This firsthand experience inspired one of xAID’s cofounders to address diagnostic bottlenecks with cutting-edge AI capabilities. The company is developing a foundation model not only to help identify the critical conditions that send patients to emergency departments, but also to flag related, non-acute pathologies that might otherwise go undetected — amplifying the reach of radiologists amid a global shortage.

Powered by Nebius, xAID’s AI assistant is trained on real-world chest and abdominal CT scans with up to 256³ input image resolution. With five days per epoch training on noisy clinical data, xAID relied on Nebius AI Cloud for consistent, high-performance computing, eliminating the risk of unexpected interruptions or infrastructure bottlenecks.

In this case study, we’ll explore xAID’s strategies to tackle key challenges when training on noisy clinical data, their 3D transformer model architecture, and the next steps to increase an already high diagnostic accuracy of 0.86 macro F1 on most clinically relevant pathologies.

## Generalizing a unique, real-world dataset: operating globally

xAID’s competitive edge stems from a rare asset: a broad dataset including over 1 million training scans from the CIS region, Latin America and Europe, valued in the tens of millions of dollars.

To ensure global scalability, xAID’s model is fine-tuned using clinical reports and incorporating scans from devices made by the five leading CT manufacturers. This approach helps the model generalize across diverse populations and imaging standards.

With a global vision in mind, xAID currently operates across the EU, Latin America and the CIS region, with plans to enter the US in 2026 and the Asia-Pacific region in 2027, positioning the company for worldwide coverage.

## Telling the signal from the noise: training on noisy classification data

When comparing with test and validation datasets manually classified by their in-house radiology team, xAID found a significant number of errors in the automatically labeled training data. The challenge was clear: how to ensure diagnostic precision when the model is training on inconsistent data?

xAID solved it from two angles:

- 

Smarter annotation: Although model performance would strongly improve if medical specialists annotated the entire training dataset, this approach would be too costly and time-consuming. By developing an in-house annotation platform, xAID enabled their radiology team to correct labels faster and at scale.

- 

More data: Noisy labels make training unstable, meaning the model’s learning process can be inconsistent, risking convergence failure and slow accuracy improvements. As a solution, xAID compensates with data volume — adding more examples to dilute mislabeled cases so the model learns more robust patterns.

The strategy worked, pushing training time to five days per cycle on three NVIDIA H100 GPUs. That’s why Nebius AI Cloud’s reliable, high-performance infrastructure was crucial, ensuring uninterrupted runs and accelerating xAID’s path to bringing life-saving technology to market.

## Managing high-resolution input under memory limits

Working with 256³-resolution CT images, even after 2x downsampling, put significant pressure on the 80 GB memory limits of the H100 GPUs. How do you train on such large volumes, already scaled up to handle labeling errors, without exceeding hardware constraints? Hint: xAID’s answer involved a smarter way to handle gradients.

Instead of feeding the model all training data at once, the dataset was split into large batches. Each time the model processes a batch, it makes predictions and adjusts its parameters as it learns to identify patterns on the data. These adjustments are made by computing gradients.

Here’s the challenge: xAID’s model has nearly 580 million parameters. Updating them after every batch would be inefficient and memory-heavy. Instead, xAID accumulated gradients across several batches to perform a single update later, allowing for larger batch sizes within memory limits.

With noisy labels and large batches, GPU utilization can fluctuate, but xAID’s strategy kept it within a 70-90% range to make every GPU hour count.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Enhancing training efficiency for diagnostic precision

While gradient accumulation solved the memory challenge, it introduced another one: slower training. Optimizing model architecture was critical for xAID to maintain processing speed without sacrificing model accuracy:

- 

Patch size calibration: The model processes CT scans in smaller 3D patches, embedded as tokens like words in Natural Language Processing (NLP). Patch size is a delicate trade-off: too small, and token count grows cubically with volumetric datasets, slowing computation. Too large, and the model risks missing tiny tissue lesions — an imperative to catch early-stage pathological changes, including nodules just a few millimeters wide.

- 

Pre-training with anatomical information: For the model to start learning, xAID provides anatomical priors so the encoder can start processing input, improving stability from early stages.

- 

Auxiliary multi-head attention: This module helps the model focus on multiple parts of the image at once, stabilizing training and speeding up convergence even when labels are noisy.

These choices show that processing speed isn’t just about raw compute, but it reflects smart, AI-native design, made possible by Nebius’ vertically integrated stack, purpose-built for AI workloads.

## Building a 3D Swin Transformer, the ideal model architecture for medical imaging

A foundation model, capable of generalizing across organs and pathologies, is essential considering current approaches in medical imaging are mostly outdated and limited in scope.

Most AI models deployed today are trained to detect a narrow set of pathologies, typically 5 to 7 for screenings like X-rays or mammograms. For more complex exams like abdominal or chest CT scans, the number of relevant medical conditions can be 10x higher, often exceeding 70 distinct conditions.

In pre-training experiments to compare different ML techniques, xAID observed transformer models performed consistently better than alternatives. Transformers break down images into patches and use attention mechanisms to dynamically focus on the most relevant parts of the input, making them well-suited for analyzing medical scans.

To maximize model accuracy while balancing computational efficiency, xAID adopted the Swin transformer, which introduces a shifted window mechanism. Instead of computing attention across the entire image, Swin groups patches into windows and computes attention locally, significantly reducing computational load. These windows are then shifted around in subsequent layers to allow the model to understand the image more broadly, but without the cost of full global attention.

This design is especially effective for CT scans, since body structures span across slices. The shifted window enables the model to learn both local and global contexts, identifying subtle patterns while maintaining scalability.

## Next steps: towards a smarter, more comprehensive AI assistant

xAID’s foundation model is trained to identify medical conditions with high precision, achieving a 0.8 macro-average F1 score — ranging from 0 to 1, this metric considers correct predictions against false positives and false negatives.

For the five acute conditions most relevant to emergency care, the model performs even better, reaching 0.86. These include inflammation of the gallbladder (Cholecystitis), appendix (Appendicitis) and pancreas (Pancreatitis), as well as intestinal complications like Diverticulitis and Intestinal Ischemia.

Looking ahead, xAID is focused on two crucial goals: improving classification accuracy beyond 0.95 and expanding the model coverage to include an even broader list of pathologies.

Besides increasing the volume of data, the team is focused on improving its quality by expanding physician-labeled datasets to reduce noise. To support radiologists across a wider range of pathologies, xAID will prioritize the most clinically urgent conditions, where faster, more accurate diagnostics can make a life-saving difference.

## More exciting stories

## 

vLLM

Using Nebius’ infrastructure, vLLM — a leading open-source LLM inference framework — is testing and optimizing their inference capabilities in different conditions, enabling high-performance, low-cost model serving in production environments.
Read the story

## 

SGLang

SGLang, a pioneering LLM inference framework, teamed up with Nebius AI Cloud to supercharge DeepSeek R1’s performance for real-world use. The SGLang team achieved a 2× boost in throughput and markedly lower latency on one node.
Read the story

## 

London Institute for Mathematical Sciences

How well can LLMs abstract problem-solving rules and how to test such ability? Research by the London Institute for Mathematical Sciences, conducted using our infrastructure, helps to understand the causes of LLM imperfections.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
