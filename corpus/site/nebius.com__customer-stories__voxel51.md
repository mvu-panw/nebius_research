# Closing the physical AI learning loop: How Voxel51 is making data quality the competitive edge

Source: https://nebius.com/customer-stories/voxel51

Skip to main content

## Long story shortLong story short

Voxel51, a Nebius technology partner, is the leading data platform used by physical AI teams to build intelligent systems. As physical AI systems have grown more capable, the limiting factor has shifted from algorithmic innovation to the quality, coverage, and observability of training data. The company’s flagship product, FiftyOne, combines open-source flexibility with enterprise-grade capabilities to help teams understand and analyze their multimodal data, a critical step for building models that perform well in the real world.

Voxel51 partnered with Nebius and NVIDIA to deliver a production synthetic data generation pipeline for a leading automotive manufacturer. The accelerated data flywheel enabled autonomous vehicle teams to generate and quality-check hundreds of realistic scene variations. The customer was able to curate data in FiftyOne, generate at scale on Nebius AI Cloud, and review results back in FiftyOne, reducing the time taken to create model-ready training data.

Founded in Ann Arbor, Michigan, by Jason Corso and Brian Moore, Voxel51 helps machine learning teams improve model performance by making it easier to visualize and prepare training datasets, annotate data, identify model edge cases, debug predictions, and streamline physical AI workflows.

The company’s tools are widely used across industries such as autonomous vehicles, robotics, healthcare, retail, and security, where high-quality visual data is critical for training reliable AI systems. Voxel51 combines an open-source developer ecosystem with enterprise offerings that support large-scale data curation, annotation, model evaluation, and workflow automation for production AI teams.

## ContentsContents

Data is the biggest determinant of success

FiftyOne: Built for data-centric systems from the ground up

A three-way partnership for data, cloud infrastructure and compute

Building the blueprint with a leading automotive manufacturer

The closed loop in action

From blueprint to broad deployment: Physical AI at the speed the market demands

## Data is the biggest determinant of success

Bad data is the biggest obstacle to AI success. Autonomous vehicle and robotics teams have spent years advancing model architectures, but real-world performance is still gated by a more fundamental problem: training data that is of poor quality, expensive to collect, difficult to scale, and never sufficient to cover the rare, high-stakes edge cases that determine whether a model will run reliably in a real-life setting.

Development teams routinely spend 30 to 40 percent of their time on data preparation, which also involves infrastructure and tooling integration rather than improving model behavior. This structural drag on progress occurs even when teams clear the infrastructure hurdle because higher quality data is typically the biggest blocker. For example, real-world autonomous vehicle programs need training coverage of scenarios that production driving footage is unlikely to provide in sufficient volume including unusual weather conditions, edge-case traffic signal states, atypical lighting, rare pedestrian behaviors, or construction zones. These scenarios are critical to define the safety boundary of an autonomous system, and they are the scenarios that real-world data collection will always struggle with.

Synthetic data has long been proposed as the solution to generate realistic variations of scenes that cameras rarely capture, helping close data gaps that real-world collection cannot. In practice, most synthetic data pipelines have failed to deliver real world results because of errors created by ‘long tail’ edge cases or hallucinated scene elements. The pipelines that do generate accurate, production-grade data have existed only inside the world’s largest research labs, inaccessible to most teams because of the infrastructure investment and integration complexity required. Therefore, most teams driving innovation in physical AI are searching to close the gap in their high quality training data feedback loop.

Voxel51 was founded to solve the limiting factor of training data quality, coverage, and observability, to accelerate visual and physical AI systems.

## FiftyOne: Built for data-centric systems from the ground up

The core insight behind FiftyOne is that before you can improve a dataset, you have to be able to see it. Most ML teams work with training data they cannot fully observe. Files live in object storage, annotations exist as JSON or XML, model evaluations produce aggregate metrics — but the actual content of the dataset, which scenes are underrepresented, which labels are inconsistent, which edge cases are absent, remains opaque. The result is what Brian Moore, CEO at Voxel51, describes directly: “Bad data is the biggest obstacle to AI success. Poor quality data, insufficient coverage, and errors cause physical AI models to underperform or fail. And teams struggle to pinpoint where and why without the right data understanding.”

FiftyOne is a platform giving ML teams the ability to visually explore datasets at scale, search by embedding similarity to find scenes clustering around known failure modes and to surface blind spots and edge cases. It has been designed for simple, end-to-end observability. Now, teams can quickly understand what is affecting model performance, audit annotation quality, and exactly what a model is and is not learning. FiftyOne makes datasets understandable and actionable, giving teams the tools to understand their multimodal data, identify and address data issues, and build reliable physical AI models at scale.

The platform’s open-source origins shaped its design philosophy. A developer-first approach emphasizing flexibility and customizability made FiftyOne the platform of choice for computer vision teams across autonomous vehicles, robotics, defense, healthcare, and manufacturing.

3K Stack + Discord Members

10K+ Stars on GitHub

4M+ Downloads of FiftyOne

100K+ Meetup Members

As physical AI has grown more demanding, FiftyOne has evolved to match — expanding from dataset visualization to a full intelligence layer that spans curation, annotation, synthetic data review, and model evaluation across the physical AI data lifecycle.

“Data is the biggest determinant of success in physical AI and computer vision. As AI systems become more capable, the limiting factor is no longer algorithmic innovation, but the quality, coverage, and observability of the data used to train models.”

— Brian Moore, CEO and co-founder, Voxel51

## A three-way partnership for data, cloud infrastructure and compute

Building a production-grade synthetic data pipeline typically requires best-of-breed capabilities from multiple companies. End-users need enterprise-grade data management for massive datasets, reliable cloud services, and large-scale GPU deployments. No single company has the full stack.

Voxel51, NVIDIA, and Nebius came together to design a complementary architecture unifying data intelligence, visualization, and compute. Voxel51’s FiftyOne platform provides teams the observability into their datasets, surfaces the scenes that matter most for model performance, and closes the review loop by surfacing generated outputs back to human reviewers. NVIDIA brings the Physical AI Data Factory Blueprint, an open reference architecture for massive data generation and evaluation along with Cosmos open world foundation models for physics-consistent synthetic video generation and OSMO for agentic orchestration across the pipeline. Nebius supports the whole solution with a purpose-built, high-performance compute backbone, combining NVIDIA RTX PRO 6000 Blackwell Server Edition GPUs, high-throughput object storage, and managed Kubernetes.

The resulting architecture is designed as a modular reference that any engineering team can adopt. Engineering teams can consume the stack as a managed service, and focus on the work that actually advances their models.

“Together, Voxel51 and Nebius give our users the data and model insights coupled with the compute infrastructure for running complex tasks such as agentic workflows, auto-labeling, and novel scene generation at the speed and scale their systems need”

— Brian Moore, CEO and co-founder, Voxel51

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Building the blueprint with a leading automotive manufacturer

The first production deployment came through the advanced engineering and research team of a leading automotive manufacturer. They faced a similar challenge to other autonomous vehicle teams, training on edge case scenarios that rarely appear in production data but are critical to safety on the road.

Real-world driving footage of routine intersections doesn’t uncover the rare scenarios created from an icy overpass at dusk with a cyclist in the breakdown lane, the construction zone with ambiguous traffic signals in morning fog, or the school crossing with a stopped bus and oncoming traffic. The team needed to build around safety first, but without complete real world data.

The team adopted a data generation workflow to accelerate automation and reduce pipeline complexity. Their engineers use FiftyOne’s embedding search and visual dataset exploration to identify which scenes have the most impact on model performance and safety. A data agent automated much of this discovery process, surfacing the scenes worth augmenting before a human ever has to review them. Once a scene is identified as worth augmenting, it moves into the generation pipeline automatically. This ‘agentic data’ approach reflects the direction of physical AI development today.

## The closed loop in action

The pipeline that the three companies built together closes a loop that physical AI teams have been trying to close for years: the ability to identify what training data is missing, generate high-quality variations of the missing scenarios, and review the outputs.

Within FiftyOne, raw driving footage enters the platform, where the team uses visual dataset exploration and embedding search to identify scenes that matter most for model performance. The data agent automates scene discovery, flagging underrepresented scenarios and queuing them for augmentation. Once a scene is selected, it moves into the NVIDIA Physical AI Data Factory Blueprint, which orchestrates the generation and augmentation pipeline running reliably on Nebius infrastructure.

Inside the pipeline, NVIDIA Cosmos Reason or Qwen3-VL auto-labels the source footage and generates a response describing the scene. The team specifies the augmentations they want — different weather conditions, lighting changes, traffic signal states, time of day — and the NVIDIA Nemotron Nano model jitters those prompts to introduce variation across the generated batch, ensuring outputs don’t all look identical. Cosmos Transfer then runs multiple passes to produce the synthetic video. The entire process is orchestrated through NVIDIA OSMO.

Before any output reaches a training set, it passes through Cosmos Evaluator, which scores each generated clip across multiple axes: hallucination detection, traffic signal validity, and scene coherence. Only outputs that clear this quality bar are surfaced back in FiftyOne for human review. The result is a fully closed loop: curate in FiftyOne, generate at scale on Nebius with NVIDIA GPUs, and review in FiftyOne.

## From blueprint to broad deployment: Physical AI at the speed the market demands

Historically, the infrastructure barrier included standing up a generation pipeline of sufficient quality that requires simultaneous expertise in large-scale GPU orchestration, computer vision tooling, model selection, quality grading, and data management.

With the Voxel51, NVIDIA, and Nebius stack now available as a repeatable reference architecture, teams now have a blueprint and a concrete reference deployment to build from. The deployment with the automotive manufacturer validated that synthetic data pipelines are now more accessible for a variety of use cases and organizations of all sizes.

As a next step, Voxel51 and Nebius are working on enhancing the ‘agentic data’ architecture that was implemented.

## More exciting stories

## 

Ultimate Bots

Ultimate Bots is building a robot sports league and software for humanoid robots. Its browser-based Studio makes humanoid robotics accessible to creators by turning recorded movement into deployable robot motion in minutes. Powered by Nebius Serverless and NVIDIA’s SONIC foundation model, Studio now supports more than 500 creative workflows each month.
Read the story

## 

Jua

Jua is building a foundation AI model for weather simulation, creating a real-time digital twin of the Earth. Using Nebius AI Cloud, the team trains large-scale physics-based models to deliver fast, high-resolution forecasts, enabling energy traders to make better decisions in highly volatile, weather-driven markets.
Read the story

## 

RoboForce

RoboForce builds Robo-Labor for dirty, dangerous and repetitive industrial work across solar, data centers, shipping, mining, manufacturing and logistics. With Nebius AI Cloud, NVIDIA Blackwell infrastructure, scalable storage and expert support, RoboForce reduced AI setup pipeline time by 70% and cut iteration cycles from months to days.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
