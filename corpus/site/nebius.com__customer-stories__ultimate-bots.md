# The dance crew, the robot and the AI Cloud: How Ultimate Bots built physical AI on Nebius

Source: https://nebius.com/customer-stories/ultimate-bots

Skip to main content

## Long story shortLong story short

A crew of TURF dancers from Oakland came into the Ultimate Bots lab in early 2026 with a vision: teach a humanoid robot to dance TURF and welcome robots into a culture two decades in the making. Short for Taking Up Room on the Floor, TURF is a dance style invented in Oakland, and it isn’t the kind of choreography you typically find in a research dataset. Using Ultimate Bots Studio, the crew filmed their own movement, uploaded it and within minutes a humanoid was performing their dance.

Ultimate Bots is a San Francisco–based company building the premier spectator sport of the AI era. It produces live shows where humanoid robots fight, dance and perform, and it builds the software stack that lets anyone create motions for them. Its initial consumer product for creatives, Studio, runs as a serverless workflow on Nebius AI Cloud and is built on top of NVIDIA’s Sonic foundation model for humanoid locomotion.

## ContentsContents

The league and the accessibility thesis

The Ultimate Bots Studio app

Under the hood — Nebius Serverless

The foundation — NVIDIA Sonic

What is next

TURF dance was born on the streets of Oakland in the early 2000s. It’s a style of contortion, gliding and storytelling that came out of the hyphy era and has, in the years since, become one of California’s defining contributions to street dance. TURF, Inc is the Oakland entertainment company that represents the broader TURF community and it has spent two decades pushing the form forward by running tournaments, mentoring young dancers and using dance as a tool for healing, restorative justice and community.

Earlier this spring, Ultimate Bots invited a TURF crew into its San Francisco lab. The dancers arrived with a clear vision: teach a humanoid robot to dance TURF and welcome robots into a culture that had been built on Oakland’s dance floors for the better part of twenty years.

Using Ultimate Bots Studio, each crew member filmed their own choreography — moves like the wave, the dimestop and general floor work — uploaded the video, then watched a humanoid mirror their moves on screen within minutes. The motion the dancers uploaded was clean enough for a real robot to replicate within minutes. By the end of the session, the bot was running through a TURF routine that had been on the dance floor an hour earlier.

This was the first time a humanoid robot was invited into a dance culture and taught a community-invented style by the community itself, on a tool any creator can easily use.

## The league and the accessibility thesis

Ultimate Bots is the robot sports league where teams program and pilot humanoid robots, competing across disciplines, like fighting, dancing and soon more. They’ve performed shows for audiences in San Francisco, Los Angeles and Las Vegas, and captivated millions of people online via the TED Talks main stage, and on the pages of The New York Times, Bloomberg, Forbes and San Francisco Chronicle.

The company is built around a thesis of accessibility that humanoid robotics needs to become a creative medium for anyone, the same way music software, video editing and game engines became accessible to anyone.

“Every transformative technology, including the internet and the smartphone, had a moment where it stopped belonging to the labs and started belonging to creators,” says Xenia Bulatov, Commissioner of Ultimate Bots. “That’s when the field actually became big. Humanoid robotics is in that moment right now and we want to build the tool that lets a dance crew in Oakland choreograph a robot in parallel with a research team in Zurich or a high-schooler in London, all on Nebius AI Cloud.”

The accessibility thesis cuts three ways inside Ultimate Bots. It’s about making it easier for people to experience robotics via their live shows, to train robot moves via the Studio web application and to program humanoids and compete against other teams within their sports league. The TURF collaboration was the proof that the second leg works for the audience that is not robotics or AI native: the creators and artists.

“The most striking thing about the TURF collaboration wasn’t what we did for them,” Bulatov says. “It was that they showed up wanting to welcome robots into their culture. That’s the moment a technology actually becomes a medium — when communities decide on their own terms to bring it in. And Studio has to be good enough to deserve the invitation.”

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## The Ultimate Bots Studio app

Studio is a browser-based creative tool that allows anyone with a phone to record and upload a sequence of human movement. Studio then produces a motion file that a real humanoid robot can perform. At Ultimate Bots dance competition events, the teams use Studio to train humanoids how to dance.

The audience includes the people who define what humanoid motion looks like culturally. It isn’t only roboticists. It’s choreographers, dancers, designers, kids with phones and creators like TURF dancers.

For the TURF crew, the workflow was four steps and a few minutes:

- Film the choreography on a phone.

- Upload to Studio via a browser.

- Wait for the motion to retarget on the humanoid and render in simulation.

- Export and run on the real humanoid robot.

Studio makes creating a multi-step physical-AI pipeline feel like uploading to YouTube or TikTok. And it is built on Nebius.

## Under the hood — Nebius Serverless

When a Studio user uploads a video, the browser hands the file to Nebius Object Storage and triggers a Nebius Serverless job. The job runs pose extraction, retargeting against the humanoid’s joint configuration and physical validation. A playable motion file is returned. End-to-end runtime is on the order of minutes from upload to deployable result.

The architectural decision under all of that is a deliberate one: Studio runs serverless rather than on a managed cluster. For a small engineering team shipping a consumer product, the difference is measurable.

“Serverless Jobs and Endpoints are the biggest single benefit,” says Patrick Rose, lead engineer at Ultimate Bots. “It’s the reduction in mental overhead. No control plane, no Kubernetes, no queueing logic to tune. For a startup where the engineers wear many hats, that’s the whole difference between shipping a product in two minutes instead of spending two weeks down a DevOps rabbit hole. We use the API to fire off the right amount of compute in minutes and move on to the next thing.”

The economics are similarly cooperative with how a small team actually works.

“On another hyperscaler we’ve burned thousands of dollars on products after forgetting to adjust spot requests for a day,” Rose says. " Nebius' CLI lets me start and stop instances confidently without remembering to check a dashboard, and the docs are short enough that you actually read them. For a consumer-facing physical AI product, that’s the difference between a viable cost structure and a quietly leaking one.”

This level of efficiency makes Studio a responsive tool for the creators to use real-time, rather than a research tool that creators wait on. When the TURF crew was in the lab iterating between takes, the iteration loop was bounded by the dancers, not by infrastructure.

## The foundation — NVIDIA Sonic

Studio sits on top of a recent breakthrough out of NVIDIA: the SONIC foundation model for humanoid locomotion.

SONIC is a learned controller for bipedal humanoids. Given a sequence of poses, a piece of choreography or a fighting combination, SONIC produces the joint-level commands that move the robot from one frame to the next while keeping it upright and within safe operating envelopes. It is the closest thing the field of humanoid motion has to a base model, a piece of trained intelligence the rest of the stack can be built on.

Before SONIC, every team working on humanoid motion was assembling controllers from scratch, often per-move and per-robot. SONIC’s open release works for an entire class of motions and lets teams ship products at the layer the user actually touches.

“SONIC is what turned this from a research project into a product,” Rose says. “You hand it motion, it plays it out. That’s what makes Studio feel like a creative tool instead of a control-theory exercise.”

The architecture sits on three layers: NVIDIA SONIC as the base, Nebius Serverless in the middle, Ultimate Bots' Studio surface on top. All TURF dancers need to do is upload a video and tap the upload button. It’s designed to be that easy.

## What is next

When Ultimate Bots set out to build Studio, the bet was that humanoid motion could feel like a creative tool that’s fast enough for a dancer to iterate with, simple enough for a creator who’s never read a research paper and good enough that a culture would invite it in. The TURF collaboration is what that looks like when the bet pays off.

The upload-to-deploy loop, the engineering team that didn’t have to babysit clusters, the foundation model that handled what a small team should never rebuild — are all in service of a seamless user experience. A dancer can show up at the UFB lab in the morning and walk out with a sophisticated robot dance in an hour. Now that this part of the robot ability has advanced, the Ultimate Bots team has begun expanding the tool stack even further. Stay tuned.

🤖 Studio is open

Upload your video and watch a humanoid perform your dance

## More exciting stories

## 

Voxel51

Voxel51 develops FiftyOne, an open-source platform that helps physical AI teams understand, curate, and evaluate multimodal datasets. Together with Nebius and NVIDIA, the company built a production synthetic data pipeline that enables teams to generate synthetic scene variations at scale and review them in FiftyOne.
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
