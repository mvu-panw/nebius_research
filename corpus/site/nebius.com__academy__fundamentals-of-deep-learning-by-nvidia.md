# Fundamentals of Deep Learning — NVIDIA open-source course on Nebius Academy

Source: https://nebius.com/academy/fundamentals-of-deep-learning-by-nvidia

Skip to main content

## For engineers starting deep learning

Python basics and some Pandas are enough. No prior deep learning required.

## Self-paced, hands-on

Six modules, each with a Jupyter notebook you run yourself. About 6 hours end to end.

## 100% free and open source

The course is free on Nebius Academy, and every notebook is public on GitHub.

## Get a credential

Earn a Credly digital badge when you complete the course.

## Start with working code

Every module opens a notebook that already runs, and you build on it from there. You train your first image classifier in module one, then a convolutional network that reads American Sign Language letters, then apply data augmentation so it generalizes. In module five you take a pre-trained model and turn it into an automatic doggy door, then use transfer learning so the door opens for one specific dog.

The final module moves from images to text: you train a model on sequential data and see how the same ideas carry over to natural language processing.
Start the course for free

## Created by NVIDIA, hosted on Nebius Academy

Fundamentals of Deep Learning' is the first open-source from the NVIDIA DLI open-source catalogue to be hosted on Nebius Academy. The curriculum and notebooks are the work of NVIDIA and are published under an open licence. Nebius Academy hosts the course, adds the learning path and awards the badge.

The course is one part of a wider collaboration between Nebius Academy and NVIDIA: courses co-developed by Nebius and NVIDIA engineers, more titles from NVIDIA open-source catalog, and hands-on workshops at Berlin. See all joint initiatives.

## What you’ll be able to do

By the end of the course you can:

## Train a network

Build and train neural networks in PyTorch on real image datasets.

## Classify images with CNNs

Apply convolutional architectures to image classification.

## Get more from less data

Use data augmentation and transfer learning to improve accuracy on small datasets.

## Control overfitting

Manage the bias-variance trade-off and apply techniques to address overfitting.

## Run predictions on new data

Save a trained model and use it on images it has never seen.

## Curriculum

01 · An introduction to deep learning

- What deep learning is and how it differs from writing rules by hand

- Load and prepare the MNIST handwritten-digit dataset in PyTorch

- Build, train, and evaluate your first image classifier

02 · How a neural network trains

- What happens in a training loop: loss, gradients, optimizer steps, epochs

- Train a network on the American Sign Language alphabet dataset

- Read training and validation curves and recognize overfitting when it happens

03 · Convolutional neural networks

- Why convolution and pooling suit image data

- Rebuild the sign-language model as a CNN, layer by layer

- Compare its accuracy and generalization with the dense network from module 02

04 · Data augmentation and deployment

- Augment training images so the model sees more variation than the dataset holds

- Retrain and measure the gain in validation accuracy

- Save the trained model and run inference on images it has never seen

05 · Pre-trained models

- Use a model pre-trained on ImageNet without training anything yourself

- Build an automatic doggy door that only opens for dogs

- Apply transfer learning so the door opens for one specific dog, from a handful of photos

06 · Advanced architectures

- How sequential data such as text differs from images

- Turn text into inputs a network can learn from

- Train a model on sequences and see how the same ideas extend to natural language processing

## Every module ends in a notebook you run yourself

The course links to the notebooks on GitHub. Pick the setup that fits you; all three are documented in the repository.

## NVIDIA Brev

One-click launchable with CUDA, Python, and all dependencies pre-installed. An NVIDIA T4 or L4 is enough for every lab. Ready in about 2 minutes. Brev bills GPU time by the hour, so stop the instance when you finish a session.

Launch on Brev

## Local machine

Clone the repository and install the requirements. Needs Python 3.9+, PyTorch 2.4.1 or newer, and an NVIDIA GPU with CUDA 11.8+ (CPU works, but the later notebooks are slow).

Clone the repo

## Docker, if you would rather not manage dependencies

The repository ships a Dockerfile with every library pinned. Build it, run JupyterLab with GPU passthrough, and skip the environment setup. You still need an NVIDIA GPU on the host.

Read the setup guide

## Make your learning rewarding

## Earn a digital badge

Receive a Credly digital badge when you complete the course on Nebius Academy.

## Challenge your skills with Nebius Certification

We invite you to challenge your skills. Explore a wide range of Nebius certifications, validate your knowledge, and earn an official Nebius certificate.

Explore Nebius Certification

## Start with working code

Six modules, six notebooks, one badge. Free on Nebius Academy.
Start the course for freeView the source on GitHub

## FAQ

Is the course free?

Yes. The course is free to take on Nebius Academy, and the materials are open source on GitHub.

What do I need to know before I start?

Python basics (functions, loops, dictionaries, lists), some familiarity with Pandas, and an idea of what a regression line is. No prior deep learning experience.

Do I need my own GPU?

No. NVIDIA Brev gives you a pre-configured GPU environment from the repository; a T4 or L4 is sufficient. Brev is a paid service billed by the hour, and charges continue while the instance is running, so stop it when you finish a session. You can also run locally or in Docker if you have an NVIDIA GPU.

Which framework does the course use?

PyTorch 2.4 or newer. The open-source release replaced the TensorFlow/Keras version used in earlier NVIDIA DLI workshops.

Do I get a credential?

Yes. Completing the course on Nebius Academy earns a Credly digital badge.

How is this different from the NVIDIA DLI workshop of the same name?

Same curriculum, self-paced instead of instructor-led, and free. The instructor-led version is still offered by NVIDIA DLI for organizations.

Can I use the materials for my team or university?

Yes, under the licenses in the repository (Apache 2.0 for code, CC BY 4.0 for teaching material). NVIDIA names, logos, and trademarks are excluded.

For a guided program, write to academy@nebius.com. Nebius Academy runs programs for companies and universities, and we can advise on which courses fit.

Fundamentals of Deep Learning is created by NVIDIA and hosted on Nebius Academy.

Course code is licensed under the Apache License 2.0; documentation, notebook text, and NVIDIA-created educational media under Creative Commons Attribution 4.0 International. See the repository for full license terms and third-party notices.
