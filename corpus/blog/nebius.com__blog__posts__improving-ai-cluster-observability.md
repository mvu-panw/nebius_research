# Improving AI cluster observability: New metrics, Grafana dashboards and advanced logging

Source: https://nebius.com/blog/posts/improving-ai-cluster-observability

Skip to main content

In the past weeks, we have made several significant observability-related improvements to the Nebius AI Cloud. Among them: advanced monitoring metrics in our web console and API, out-of-the-box Grafana dashboards, as well as monitoring and logging features, allowing customers to upload their custom metrics and logs to our cloud.

# AI cluster observability is keyAI cluster observability is key

AI infrastructure is a complex system with tightly interconnected hardware and software layers working together to create a stable and highly performant environment for AI workloads. These systems are enabled to deliver outstanding compute performance, though they also suffer from increased failure rates due to their scale and enormous loads.

Although many AI clusters are hosted in the cloud, their overall complexity creates numerous challenges that operational teams must overcome to ensure smooth and consistent performance. Bringing deep visibility into an AI cluster’s state provides significant benefits for infrastructure admins and ML engineers. Here are some notable advantages of having an extended observability system in place:

- 

Increased efficiency: Tracking performance metrics across the cluster components helps detect deviations and bottlenecks and eliminate them to ensure maximum utilization of resources.

- 

Improved reliability: Since accelerator failures are inevitable, proactive monitoring and logging help detect issues at early stages and encourage admins to re-allocate resources to minimize the outage losses.

- 

Quick troubleshooting: Extended system logs and actual performance data allow operational teams to track the initial cause of an issue and reduce the investigation time needed.

All of these advantages result in extracting maximum value from reserved compute hours and delivering better outcomes for your AI project.

# Observability in Nebius AI CloudObservability in Nebius AI Cloud

Unlike general-purpose cloud environments, AI-focused clouds require more granular and workload-specific data, to help developers make the model development process more transparent and predictable.

In this domain, our AI Cloud has two main services: Monitoring and Logging. The first focuses on collecting and visualizing performance metrics; the second one, on storing information about system events.

Below, we reveal additional information about recent changes in these two services:

- 

Detailed Monitoring metrics added to the UI and API.

- 

Pre-configured Grafana dashboards are now available for everyone.

- 

We added new Monitoring and Logging functionality — including the ability to upload custom metrics and logs.

# AI-specific metrics in dashboardsAI-specific metrics in dashboards

Last quarter, we deployed the Monitoring service across all our cloud services. It collects system performance data and delivers it through a public API and visualizes it on the web console dashboards. One of the goals that we were pursuing was to collect performance metrics from every component of an AI cluster, from compute to networking and storage.

Figure 1. Power usage metrics on the Compute monitoring dashboard

Since AI workloads are more complex and sophisticated than conventional computing tasks, we need to provide more granular visibility even on the infrastructure level. For example, we show not only the temperature but also provide information about possible reasons for throttling. Additionally, you can track network data.

Figure 2. Network metrics on the Compute monitoring dashboard

All monitoring metrics in Nebius AI Cloud are available for every user by default—you don’t need to buy or install additional third-party applications or services.

The latest feature we’ve developed so far to extend your AI monitoring capabilities is the ability to stream your custom monitoring data in our cloud. It ingests and securely stores your data, which you can then visualize on Grafana dashboards together with the original performance metrics from Nebius AI Cloud. For more info, see our docs.

# Pre-configured Grafana dashboardsPre-configured Grafana dashboards

Grafana is the de facto standard for visualizing performance metrics and logs. Most of our customers use Grafana for cloud monitoring on a daily basis. To make this experience more convenient, we created pre-configured dashboards for Grafana that allow our customers to receive service logs and performance data—without extra effort.

Figure 3. Nebius performance dashboard for compute

There are two options for using these dashboards: you can deploy the Grafana image with pre-configured dashboards to your Kubernetes cluster from our Application space or you can add them to your Grafana via Grafana Marketplace, then connect our endpoints as a data source.

Figure 4. Nebius’ Shared Filesystem dashboard on Grafana Marketplace

For more info about the installation process, see our documentation on metrics and logs.

# Detailed and flexible loggingDetailed and flexible logging

Logging on Nebius AI Cloud is available for our managed services and Kubernetes applications. This functionality allows you to control events, pinpoint performance issues and accelerate the troubleshooting process for the launched managed applications.

A new feature of the Logging service is the ability to upload and store customer logs in our cloud. This allows you to stream and securely store custom logs from your application right to the Nebius AI Cloud environment. Uploaded logs will be available in a readable format and ready to be visualized in Grafana. This will make things easier if you need to deploy and start your new application quickly.

For those who need information about the cloud platform as a whole, we recently launched Audit Logs, a new service that collects and stores security-related events.

# What’s nextWhat’s next

These changes in observability are some of many steps we plan to take in making our cloud more transparent and convenient for our customers. Delivering deeper insights about your AI cloud environment will make training and inference experience more predictable and less costly, reducing idle compute capacity and minimizing risks of wasting resources due to unoptimized infrastructure.

We know there is more work to do to deliver ultimate observability for AI teams, but these recent changes will definitely make your operations more convenient and effective. We are committed to continuing our efforts to polish and enhance this side of the platform.

Feel free to contact our experts if you need more information about our AI Cloud and its observability features.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Valeria Shchennikova
Product Manager at Nebius

Andrey Kuyukov
Product Marketing Manager at Nebius

Contents

- AI cluster observability is key

- Observability in Nebius AI Cloud

- AI-specific metrics in dashboards

- Pre-configured Grafana dashboards

- Detailed and flexible logging

- What’s next

## See also

### 

Meet Audit Logs in Nebius AI Cloud

Audit Logs is a new feature, now available in preview in Nebius AI Cloud. With Audit Logs, our customers can improve their accountability and security and ensure compliance with regulatory requirements.

April 15, 2025
2 mins to read

### 

Q1 2025: Nebius AI Cloud updates

The end of the quarter is a great time to reflect and share a kind of changelog with you, highlighting what’s improved in Nebius AI Cloud over the past three months. This quarter, we launched new regions, released new services for MLOps and enhanced our existing product lineup to minimize your infrastructure concerns even further.

April 9, 2025
7 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
