# From game modder to world modeler: How Jua is building a digital twin of Earth

Source: https://nebius.com/customer-stories/jua

Skip to main content

## Long story shortLong story short

Jua is building a foundation model to simulate the physics of Earth, starting with weather forecasting for energy markets. After struggling with unreliable infrastructure across three AI-first cloud providers, Jua moved to Nebius for higher throughput and stable clusters. With Nebius, Jua trained and refined EPT-2, now delivering hourly global updates, 6x higher resolution, and forecasting performance that beats leading AI and traditional weather models.

Jua is a Zurich-based AI company building foundation models for the physical world. It sells advanced weather forecasting to the energy sector today, while working toward a broader universal world model that can simulate physical systems such as weather, oceans, wildfire behavior, and more.

## ContentsContents

The seed of an idea

Building the research machine

The road to Nebius

Geospatial reasoning system, Athena

Compute, the competitive advantage

In a growing lab in Zurich, Marvin Gabler and his team are building a foundation model that simulates the physics of the entire planet. His company Jua sells weather prediction to the energy sector today, but the long-term goal is what Gabler calls a Universal World Model: a system that can simulate any physical process governed by the laws of nature. Ocean currents, material stress, agricultural yield, wildfire behavior. Anything physics touches.

It started with a kid who couldn’t stop tinkering. Gabler spent most of his childhood in Germany modding games, building plugins, and constructing virtual worlds. The obsession with simulation never went away. It just got more serious.

## The seed of an idea

Gabler grew up in an entrepreneurial household in Germany. Practical, hands-on, no patience for theory without execution. While studying biotech and computer science at university, he founded and sold his first company, an e-commerce business. After that he joined Q.met, his family’s weather data company, as head of research where he built out Europe’s largest weather YouTube channel, worked directly with energy and insurance clients, and started the research that would eventually become Jua.

The global energy grid was shifting quickly toward renewables, and with that shift came a massive new dependency on better understanding weather. Wind, solar, and hydro were scaling rapidly, but the forecasting infrastructure behind them hadn’t changed in decades. Government-backed numerical weather models refreshed a few times a day. Every vendor in the market was surfacing variants of the same data. Pricing was volatile, critical infrastructure was unpredictable, and traders were navigating billion-dollar markets with tools that couldn’t keep pace with the speed of transacting.

GPT-2 had recently shown what scaling laws could do for language. Gabler believed the same logic applied to physics. With the right data, enough compute, and a team that understood both domains, you could collapse fifty years of atmospheric science into a single model and push well beyond what numerical methods could ever deliver.

“There were two other companies attempting this, both well-funded. I built deep relationships with both of them but realized they weren’t going to solve the problem I saw clearly. So I decided to do it myself”. Like many founders, he learned to code out of necessity, hiring a full-time engineer wasn’t an option.

## Building the research machine

To build what is now Jua’s Earth Physics Transformer (EPT-2), Gabler needed a team that could operate like an elite research lab at startup speed. He bypassed the usual hiring pools entirely, instead going through the author lists of the world’s leading papers in physics-informed machine learning. He built a shortlist of twenty PhD-level researchers from around the world and picked up the phone. These were industry experts with the specific blend of deep physics intuition and production ML engineering needed to simulate the Earth at scale. At some point every founder becomes a salesperson and Gabler was selling both the vision of what could be built, and how they were going to create real value that didn’t yet exist.

“Convincing the first one took time. After that, each became easier. People want to work on hard problems, and I was upfront that this was a race. Great talent brings in more great talent. When DeepMind released GraphCast in November 2023, it set an important open benchmark for the field. It pushed the team to go further and faster”.

Building a world model is computationally brutal. Unlike text-based AI, Jua’s models ingest mostly heterogeneous raw data. This includes disparate satellite feeds, geographic projections from sources that don’t align, and unconventional signals like car windshield wiper telemetry to track localized precipitation. Training runs stretch to months. A single cluster failure during one of those runs means incredibly expensive rework and lost time in a market where being first earns years of trust. Utilities that embed a forecasting model into their trading infrastructure rarely switch for a marginal improvement. Getting there first matters.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## The road to Nebius

In the early days, Jua ran heavy training loads across three major AI-first cloud providers. The experience was sometimes frustrating. Unreliable throughput and mid-run failures turned long training cycles into expensive dead ends. Nebius AI Cloud outperformed on every internal benchmark Jua’s engineering team designed. This included consistently higher throughput and ultra-stable clusters. “Utilizing high-speed InfiniBand, Nebius felt like a single stable supercomputer”, Gabler says. “That changed everything for us”.

The stability reshaped the team’s daily work. Engineers stopped watching dashboards and started focusing on the actual research: ingesting higher-quality data, refining model architecture, and expanding what EPT-2 can simulate. When a new satellite launches or a market regime shifts, Jua now runs tight fine-tuning cycles knowing the infrastructure will hold.

EPT-2 is now state-of-the-art globally, outperforming leading AI weather models and traditional numerical baselines across all forecast horizons on RMSE. Jua delivers hourly global updates, breaking the 4 times daily refresh cycle that every other system, including those from the world’s largest AI labs, still follows. EPT-2 runs at 6x higher temporal and spatial resolution than comparable AI models, and predicts variables that other systems cannot, including localized phenomena critical to energy markets. That’s what dedicated endpoints on Nebius can do.

## Geospatial reasoning system, Athena

Benchmarks:

Jua’s agentic intelligence layer, Athena, is a geospatial reasoning system built on top of EPT-2. It turns raw physics predictions into trading decisions, reading market context, modeling what participants are likely to do, and surfacing the most profitable position.

“We realized early that this is about human nature more than mother nature”, Gabler says. “Traders need a system that understands how the physical world moves markets”.

Jua now serves major utilities across four continents, including some of Europe’s largest energy companies, as well as commodity traders and hedge funds. The sales cycle, which once required months of proof-of-concept work, has compressed to as little as two weeks. Athena fits into existing workflows and delivers continuous, high-resolution insight into how the physical world will affect open positions.

## Compute, the competitive advantage

The downstream impact on all of this work is measurable every day. In European energy markets, where trading happens in tight intraday windows, Jua’s higher resolution is a real edge. Jua’s forecasts have an estimated $1.5 million profit and loss impact per gigawatt annually, translating to hundreds of millions for large portfolios. Gabler even tracks how many hours of productive decision-making Jua gives back to traders each week to create clarity and stickiness.

As Jua looks toward 2026, the infrastructure demands will grow with the ambition of his growing team. Thousands of the latest GPU’s running on Nebius AI cloud determines how fast Gabler’s team can push the boundary of what the model can simulate.

“I’ve been trying to simulate the world since I was a kid modding games in my bedroom”, he says. “Now I have the team and the infrastructure to actually do it”.

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

## 

Jua

Jua is building a foundation AI model for weather simulation, creating a real-time digital twin of the Earth. Using Nebius AI Cloud, the team trains large-scale physics-based models to deliver fast, high-resolution forecasts, enabling energy traders to make better decisions in highly volatile, weather-driven markets.
Read the story

- 
- 

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
