# How Positronic Robotics is creating a smart cleaning robot with Nebius Technologies

Source: https://nebius.com/customer-stories/positronic-robotics

Skip to main content

## Cleaning as a global problemCleaning as a global problem

Every year, people around the world spend up to 800 billion person-hours cleaning. It’s one of the most disliked chores, and businesses constantly struggle with labor shortages and high turnover rates. Automating cleaning isn’t just a nice-to-have — it’s quickly becoming a necessity. Hardware is getting cheaper and more self-operating arms and mobile robotic platforms are now available, making it possible for engineers to build solutions at the intersection of robotics and machine learning without massive investments.

Positronic Robotics is a startup that creates AI-based robot control systems, turning them into intelligent next-generation workers — specifically, cleaners. The company trains ML models and develops tools that allow robots to handle cleaning tasks more effectively than humans. At first, these robots will serve as assistants to human cleaners, gradually gaining autonomy.

## ContentsContents

Smart cleaning with AI

Approaches and technologies

Using Nebius AI Cloud for model training

Plans for the future

# Positronic Robotics: smart cleaning with AIPositronic Robotics: smart cleaning with AI

In most hotels, bathrooms account for over 40% of cleaning time. Consider that’s usually the least appealing task for housekeeping staff and you have the perfect starting point for Positronic Robotics’ ambitious journey toward fully automated cleaning.

Bathrooms may not be glamorous, but they’re perfect testing grounds. Each one is relatively isolated, allowing the robot to work on one task while a human cleaner focuses on the rest of the room. Like eating an elephant one bite at a time, robots start with cleaning toilets, then move on to washing basins, mirrors, shower areas and so on. By beginning in places with consistent cleaning routines and high labor costs — like hotels — Positronic Robotics will refine its technology before moving on to commercial cleaning and, ultimately, household applications.

With a smarter approach to humans teaching AI in a controlled setting, slowly increasing the complexity of tasks over time, each new property added to the system accelerates training and broadens its scope. This collaborative model is a win-win for everyone: cleaners offload their least appealing tasks while robots learn directly from them in real hotel environments

# Approaches and technologiesApproaches and technologies

Engineers at Positronic are building a fully end-to-end, Gen 3 robotics system based on machine learning, focusing on an imitation learning approach that trains robots to perform tasks by picking up from human demonstrations.

For reference:

- 

Gen 1 (Open Loop): Follows pre-set commands without environment feedback, often operating in fenced areas for safety.

- 

Gen 2 (Closed Loop): Uses sensors and mapping to adjust actions in real time, but relies heavily on predefined algorithms.

- 

Gen 3 (AI-driven): Employs neural networks to process sensor data directly and adapt quickly to changing conditions.

# How does it work?How does it work?

To train the robot, people demonstrate how to perform tasks — like wiping a sink — over and over, and the model learns by observing these actions. As it sees more examples, the robot becomes capable of cleaning a range of objects in diverse environments with different kinds of contaminants. A high-level planning system, powered via a modern VLM like GPT-4o, then decides how to switch between tasks and tools.

At the core of the robot’s control system is the Action Chunking Transformer (ACT), which merges features from a visual encoder and robot states with a transformer encoder-decoder model to predict the next steps. Beyond simply anticipating the next position, ACT predicts an entire Action Chunk, which helps mitigate the compound error effect. This approach is inspired by psychological theories on action chunking, which describe how sequences of actions are grouped together to improve efficiency. By structuring movements in this way, the robot can execute tasks more smoothly and with greater precision. Additionally, ACT is trained as a Conditional Variational Autoencoder (CVAE) to capture the variability in human data, such as pauses during demonstrations.

Unlike in the original ACT paper, instead of relying directly on robot joint states, Positronic represents automated movements in a Cartesian space, which allows the same policy to be used for different robotic arms. This approach improves flexibility, ensures consistency across various hardware setups and allows demonstrations to be decoupled from specific hardware configurations. For modeling rotation, engineers use a specialized method that enhances stability and accuracy, avoiding the limitations of traditional quaternion-based representations.

In the midst of development, Positronic tackles all sorts of challenges. Increasing movement speed is a big priority, so that robots perform cleaning tasks at least as quickly as humans. The team also developed specialized cleaning attachments that both machines and people can use, making it easier to teach the robot. To mention another important achievement, Positronic recently trained the robot to maintain full surface contact while applying the necessary pressure to not just to glide over surfaces but to scrub off stubborn stains.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

# Using Nebius AI Cloud for model trainingUsing Nebius AI Cloud for model training

Computing: Positronic uses several virtual machines hosted on Nebius’ infrastructure through the Compute Cloud service to train its models. The startup relies on NVIDIA H100 GPUs for model training. Each training session takes place in a containerized environment on Nebius servers and is optimized through distributed parallel computing. Data is transferred to the servers and runs in containers with minimal manual configuration. A single server is dedicated to one training cycle, which lasts about 12 to 16 hours.

Data organization: The storage and management of training data also utilizes Nebius’ services. Currently, researchers use around one terabyte of data for ongoing training, but this volume is expected to grow significantly. During training sessions, data is collected via VR tools and sensors, then processed and prepared for use in the models.

Flexibility and automation: Training processes are automated with scripts that manage the start and end of each task. After training is complete, the server automatically shuts down to conserve resources. The company is exploring the possibility of running simulators in a virtual environment on Nebius servers for parallel model training in the future.

# Plans for the futurePlans for the future

Right now, engineers at Positronic Robotics are focused on scaling up the data collection process. To achieve this goal, they plan on equipping cleaning staff with specialized tools, enabling the model to learn from a wide array of real-life examples and scenarios.

Another important next step will be the integration of simulators to accelerate model validation and virtual-environment training. This will allow multiple robots to be trained in parallel, improving their performance metrics and testing the resilience of their solutions under various conditions.

Looking ahead, Positronic is also exploring the possibility of running these simulators on Nebius servers, creating a virtual environment for parallel model training at a much larger scale.

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

Chatfuel

Using Nebius Token Factory to leverage a cascade of Llama-405B models along with a custom SDK, leading AI-powered customer engagement automation platform Chatfuel achieved significant efficiency gains with much better response quality and interaction speed for its AI chatbot agents.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
