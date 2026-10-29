# InfiniBand in focus: bandwidth, speeds and high-performance networking

Source: https://nebius.com/blog/posts/what-is-infiniband

Skip to main content

This blog post aims to redress the balance by providing a deep understanding of what InfiniBand is, how it works and why it’s the fastest growing high-speed interconnect network (HSI) on the market. We’ll also flag the advantages of InfiniBand over traditional Ethernet networks, and throw light on the latest developments that will affect interconnect technology in the coming years.

## What is InfiniBand and how does it work?What is InfiniBand and how does it work?

InfiniBand is an open standard, high-speed, low-latency interconnect technology explicitly designed for use in high performance computing (HPC) and data centers. InfiniBand Architecture is an industry standard specification that’s widely used to interconnect storage devices, servers and embedded systems, and allows efficient communications between them.

With the rise of AI, InfiniBand has also become the go-to network interconnection technology for high-performance GPU servers. Unlike Ethernet, InfiniBand uses a two-layer architecture that separates the physical layer and data link layer from the network layer. This allows InfiniBand applications to exchange data across the network without putting pressure on the operating system, allowing for a fast communication link between servers and systems.

As the CPU is prevented from becoming overloaded, this architecture also gives InfiniBand the ability to provide critical features such as virtualization, Quality of Service (QoS) and remote direct memory access (RDMA).

### Key features and benefits of InfiniBandKey features and benefits of InfiniBand

InfiniBand offers many networking advantages, including:

- High bandwidth. At its highest specs, InfiniBand can deliver up to 400Gb/s throughput. This is significantly faster than traditional networking technologies.

- QoS. InfiniBand includes a range of QoS features that allow admins to prioritize traffic, allocate bandwidth and manage network resources.

- Virtualization. Users can create virtual lanes to isolate tasks and run multiple jobs on the network at the same time.

- Low Latency. While Ethernet latencies range from around 20 to 80 microseconds, InfiniBand clocks in at 3 to 5 microseconds, boosting the speed at which applications can access data.

- Low Power Consumption. Compared to Ethernet server adapter cards, InfiniBand’s copper and fiber cards only use around a third of the power.

### Understanding the InfiniBand architectureUnderstanding the InfiniBand architecture

Unlike other HSI solutions, InfiniBand uses a two-layer architecture that keeps the physical and data link layers separate from the network layer. The InfiniBand layered approach looks like this:

- Physical layer: High bandwidth serial links provide point-to-point connectivity between devices.

- Data link layer: The data link layer handles transmission and reception of data packets between devices.

- Network layer: Provides access to InfiniBand’s most powerful tools such as virtualization and QoS, and provides admins with switches for low latency, high bandwidth connectivity between devices.

Crucially, the network layer facilitates RDMA, allowing devices on the network to access each other’s memory directly. This maintains high speeds as data does not need to be copied between machines.

Switches in the InfiniBand Architecture maintain low latency and provide high-bandwidth connections between devices.

### Comparing InfiniBand with EthernetComparing InfiniBand with Ethernet

Although it’s inevitable that InfiniBand will be compared to traditional Ethernet, it isn’t a fair match. While Ethernet was developed to facilitate compatibility and connectivity between networked devices, InfiniBand was specifically designed for use in HPC environments.

Although 10 Gigabit Ethernet is a strong contender, the data-heavy requirements of new HPC workloads need the lower latency and higher bandwidth offered by NVIDIA’s product. Moreover, as traditional Ethernet does not currently have critical features such as QoS and RDMA, it does not offer the tools that today’s admins need to manage data-intensive workloads.

### RDMA in InfiniBand: enhancing data transfer performanceRDMA in InfiniBand: enhancing data transfer performance

InfiniBand networks are based on RDMA, enabling direct, high speed data transfer between the memory of two computers. RDMA data transfers do not involve the CPU or use intermediate software or hardware.

The advantages of this set up are that:

- data does not need to be copied

- data transfer tasks can be offloaded to network InfiniBand hardware, improving CPU utilization and reducing the load handled by individual processor cores

By removing the need for data to be copied between devices on a network, RDMA deftly handles HPC workloads and maintains low latency. When compared to other RDMA technologies, InfiniBand’s performance is impressive.

## InfiniBand applicationsInfiniBand applications

With its higher data transfer speeds and low latency, it’s no surprise that InfiniBand technology has had a profound impact. InfiniBand is widely used to shape a variety of HPC environments, including supercomputers, high performance storage systems, data centers and clusters. Rankings on the Top 500 website — which showcases the fastest supercomputers on the planet — show that over 70% of the featured systems are powered by InfiniBand technology.

InfiniBand technology has obvious applications in fields where large volumes of data need to be processed. This includes scientific research in fields such as biology and chemistry, financial modelling, meteorology and oil and gas exploration. Additionally, InfiniBand technology is well suited to database applications as its high-speed communication links allow quick access to large repositories of data. In environments where enhancing performance in parallel computing applications is essential, including data centers and clusters, InfiniBand offers huge advantages.

A good example of InfiniBand’s impact is in the world of physics. Distributed physics analysis techniques and parallel applications require a fast and efficient connection between compute nodes and I/O nodes. Researchers at CERN have documented success when using InfiniBand in high energy physics because of the significant reduction in CPU utilization and the increased file transfer speed.

InfiniBand in supercomputing: Powering the World’s Fastest Computers. As most of the supercomputers listed in the Top500 rankings are powered by InfiniBand technology, NVIDIA’s impact on branches of science such as physics, biology and meteorology runs deep. By offering parallelism and the ability to process large amounts of data, it’s likely that InfiniBand technology will play a vital supporting role in key scientific discoveries over the coming years.

InfiniBand in high-performance storage systems: Wherever high-performance storage systems are used, InfiniBand’s high speed and critical features allow for rapid data communication and address any issues of storage system latency. As well as running data-intensive applications, InfiniBand also accelerates query processing and transaction. This can greatly speed the use of a wide variety of software, including database applications.

InfiniBand in data centers and clusters: When used to connect servers and storage systems in a data center or in clusters, InfiniBand allows all devices to be used as a single entity. InfiniBand also frees network capacity, improving the performance of applications that rely on parallel computing. Additionally, InfiniBand provides a reliable way to interconnect virtualization platforms and create virtual servers, storage devices and so on.

InfiniBand in HPC workloads: As InfiniBand has the bandwidth and low latency to juggle multiple tasks, data-heavy HPC workloads running on NVIDIA’s technology will not overload your network. This is an advantage when running data-intensive applications such as databases that need quick access to sprawling repositories of data. In fields such as scientific research, financial modelling and oil and gas exploration, InfiniBand makes sure the movement of information never slows down.

## Explore InfiniBand productsExplore InfiniBand products

As demand for faster data transfers grows, InfiniBand network systems are a popular choice for data centers. High-speed connections, minimal latency and superior throughput make InfiniBand a strong choice in all HPC environments.

But to understand which NVIDIA solution best suits your needs, it’s important to consider the current product range:

1. NVIDIA InfiniBand switches are a vital component in an InfiniBand network system. They direct data between devices at the physical layer, ensuring data transmission at high speeds and with low latency. Current InfiniBand switches include:

- NVIDIA Quantum-X800 InfiniBand Switches 200Gb/s-per-lane serializer/deserializer, with 144 ports at 800Gb/s across 72 octal small form-factor pluggable cages.

- NVIDIA Quantum-2 InfiniBand Switch Family The Quantum-2 QM9700 switches offer 64 ports of 400Gb/s InfiniBand per port.

- NVIDIA Quantum InfiniBand Switch Family The QM8700 and QM8790 fixed-configuration switches provide up to 40 200Gb/s ports with 16Tb/s of non-blocking bandwidth, or 80 100Gb/s ports with full bidirectional bandwidth per port.

2. NVIDIA InfiniBand transceivers and cables. InfiniBand’s secret power is the strength of its transceivers and cables, which are designed to smooth the high-speed transfer of data between devices. InfiniBand cables and connectors use active copper technology to amplify signals within the wires, enhancing signal integrity and minimizing signal loss.

No matter how large the physical area your network covers, cables from InfiniBand transfer data reliably across long distances. The cables are available in a variety of different lengths and NVIDIA’s range is flexible enough to connect any environment where HPC is essential.

3. NVIDIA InfiniBand adapters act like network interface cards (NICs) and allow different devices to connect to an InfiniBand network. The adapters come in a variety of options, including:

- ConnectX-8: maximum total bandwidth of 800Gb/s, dual-port or single-port configurations, host interface PCIe Gen6, up to 48 lanes

- ConnectX-7: maximum total bandwidth of 400Gb/s across one, two or four ports, host interface PCIe Gen5, up to 32 lanes

- ConnectX-6: maximum total bandwidth of 200Gb/s with PCIe Gen 3.0 and Gen 4.0 support

- ConnectX-5: maximum total bandwidth of 100Gb/s with PCIe Gen4 support

The current range of adapters is enough to meet the growing demands of data center applications, with a variety of options to consider depending on the HPC environment you have in mind.

## What is the InfiniBand network?What is the InfiniBand network?

InfiniBand is an open standard, network interconnection technology that offers high bandwidth, low latency and high reliability. The technology was defined by the InfiniBand Trade Association (IBTA).

InfiniBand fabric consolidation is often deployed in a data center or HPC environment. This allows storage networking, clustering, communication and management fabrics to be managed over the same InfiniBand Architecture. InfiniBand is a reliable solution where large volumes of data are transferred or processed by a supercomputer cluster and more demand is being put on networking technologies.

### Cluster computing with InfiniBandCluster computing with InfiniBand

With the rise of AI and large models such as ChatGPT, InfiniBand is most often used in a supercomputer cluster or GPU server. The key to its success is InfiniBand’s low latency, which is vital in clustered computing as this can affect the overall performance on a task and the speed at which applications access data. Where the fast processing of tightly coupled requests is essential, InfiniBand’s minimal latency makes it a solid choice.

### The role of InfiniBand switchesThe role of InfiniBand switches

Unlike Ethernet, InfiniBand switches do not run any routing protocols. Instead, a subnet manager manages all network activities by calculating and distributing the entire network’s forwarding table. Traffic is then directed to the correct place.

The manager allows multiple subnets or paths to be created between interconnected nodes. It also works out the best route between nodes based on the requirements of any applications that are running. Different InfiniBand subnets allow for flexible and efficient traffic routing that avoids squandering valuable CPU capacity.

### How InfiniBand manages congestionHow InfiniBand manages congestion

InfiniBand uses a congestion management mechanism to facilitate a lossless network and reliable data transmission when running heavy workloads. Each InfiniBand network link has a predetermined buffer for storing the data packets to be transmitted.

Before transferring data, the sender checks the available credits at the receiver, indicating the amount of buffer space available for incoming data. The sender decides whether to initiate the transfer based on this credit value. If the receiver does not have enough credits, the sender will wait until the receiver reports that it has capacity. This approach prevents congestion by signaling the sender when the network approaches capacity, allowing data bottlenecks to be avoided before they occur.

## Comparison of networking technologiesComparison of networking technologies

Because of its high speed and low latency, InfiniBand offers significant advantages over Ethernet/fibre channel and Intel’s Omni-Path Architecture (OPA) for computer cluster interconnections. Even though Ethernet technology is available that supports lightning-fast port speeds, InfiniBand’s RDMA and congestion management features keep data moving during busy periods and offers faster performance overall.

It’s no surprise that the majority of Top500 supercomputers built since 2014 have used InfiniBand networking for high-performance cluster deployments. Many other AI and big data applications have adopted InfiniBand technology, with 62% of the first 100 entries in the Top500 using NVIDIA’s networking products.

## What’s 200G InfiniBand HDR?What’s 200G InfiniBand HDR?

InfiniBand technology supports a variety of signaling rates to increase link bandwidth, including single data rate (SDR), double data rate (DDR), quad data rate (QDR), fourteen data rate (FDR) and enhanced data rate (EDR).

In 2019 Mellanox Technologies introduced the 200G InfiniBand with high data rate (HDR) support, which offers ultra-low latency and high data throughput. The system also uses intelligent compute acceleration engines to ensure speeds remain high and that data is processed efficiently. Users can use standard Mellanox software drivers on the cloud, and it offers support for RDMA verbs and all InfiniBand-based Message Passing Interface (MPI) software such as Mellanox HPC-X, MVAPICH2, Platform MPI and Intel MPI.

In addition, the system’s hardware offload feature for MPI cluster communication improves performance, which has a positive impact on the efficiency of business applications. 200G InfiniBand also features network compute acceleration engines, which are most commonly used to improve application performance.

## What is an Ethernet network?What is an Ethernet network?

Ethernet is the technology most commonly used in a local area network (LAN) for transmitting and receiving data through cables in a wired network, or wireless technology in a wireless network. Development of the Ethernet standard was kicked off by Xerox between 1973 and 1974, before the company teamed up with Intel and the Digital Equipment Corporation (DEC) to issue an Ethernet standard in 1980.

Ethernet networks offer a wide variety of data transmission rates, some of which can rival InfiniBand for speed. Enhancements in Ethernet technology continue and future systems promise to offer the RDMA and QoS critical features that make InfiniBand so enticing. And as organizations such as the Ultra Ethernet Consortium (UEC) bring together tech companies to develop an Ethernet suited to HPC environments, the classic networking technology is far from dead.

## InfiniBand vs Ethernet: what’s the difference?InfiniBand vs Ethernet: what’s the difference?

While InfiniBand and Ethernet are both interconnection technologies, each has characteristics and differences that determine the application fields in which they’re deployed. The key differences are bandwidth and latency, where RDMA gives InfiniBand a distinct advantage over current Ethernet technology.

### Types of Ethernet networksTypes of Ethernet networks

Ethernet and IP technologies were originally designed to facilitate compatibility and connectivity, so they’ve become the beating heart of the Internet. Recent developments have also allowed Ethernet solutions to get progressively faster and keep the competition on its toes:

 | System
 | IEEE Standard
 | Data rate

 | Ethernet
 | 802.3
 | 10Mb/s

 | Fast Ethernet/100Base-T
 | 802.3u
 | 100Mb/s

 | Gigabit Ethernet/GigE
 | 802.3z
 | 1,000Mb/s

 | 10 Gigabit Ethernet
 | IEEE 802.3ae
 | 10Gb/s

But InfiniBand’s positioning is different in terms of bandwidth, delay, network reliability and networking mode. While Ethernet provides a reliable architecture for networked machines to communicate, InfiniBand actively addresses data transmission bottlenecks in high-traffic HPC environments.

To do this, InfiniBand uses switches to create closed channels between nodes for RDMA without CPU involvement. This offloads data movement tasks to the network adapters, in turn freeing the CPU for more important jobs and greatly reducing latency.

Moreover, as InfiniBand boasts advanced error detection and correction mechanisms as standard, this facilitates reliable data transmission and network reliability no matter how busy your environment is. Data center and HPC admins using NVIDIA’s technology are also given more control using InfiniBand’s built-in QoS features, which can be used to prioritize traffic and allow critical applications to receive optimal network resources.

## InfiniBand vs Omni-Path: advantages of InfiniBand over Omni-PathInfiniBand vs Omni-Path: advantages of InfiniBand over Omni-Path

Although faster solutions are available on the market, many data centers and HPC customers are still using 100Gb/s systems for their high-performance network structure. The key 100Gb/s solutions on the marketplace currently are InfiniBand and the Omni-Path Architecture (OPA), a high-performance communication system developed by Intel.

But while OPA offers impressive functionality, InfiniBand is more attractive in terms of overall equipment cost. InfiniBand clusters require fewer switches and cables when compared to OPA, which can greatly reduce a network’s operation and maintenance costs. InfiniBand tech is also more efficient in terms of power consumption, making it kinder to the environment.

## Deep dive into InfiniBand specificationsDeep dive into InfiniBand specifications

The InfiniBand Trade Association (IBTA) publishes specifications that allow us to understand the maximum bandwidth and latency of InfiniBand devices. An InfiniBand specification defines the requirements for hardware and software, including bandwidth, latency and power consumption.

### What is the IBTA?What is the IBTA?

The IBTA was founded in 1999. It develops and publishes specifications for InfiniBand technology. The organization’s goal is to maintain and further the InfiniBand Architecture specification. This includes defining hardware transport protocols for both reliable messaging (send/receive) and memory manipulation semantics without software intervention in the data movement path. The organization’s members include representatives from a variety of high-profile tech companies, including IBM, Mellanox Technologies, Intel, Sepaton and others.

### IBTA specifications: QDR, SDR and DDRIBTA specifications: QDR, SDR and DDR

Among the IBTA’s first published specifications were:

- SDR: maximum bandwidth of 10Gb/s

- DDR: maximum bandwidth of 20Gb/s

- QDR: maximum bandwidth of 40Gb/s

HDR was introduced in 2017. It has a maximum bandwidth of 200Gb/s and low latency, making it around five times faster than QDR. With the rapid growth in AI and other data-intensive tasks, HDR has become the standard for high-performance computing.

### The InfiniBand NDR specificationThe InfiniBand NDR specification

Looking to the future, a new specification called Next Data Rate (NDR) is under development. NDR is expected to deliver a maximum bandwidth of 400Gb/s. It will also employ PAM4 encoding to allow for longer distances between devices without any loss in signal quality.

### How InfiniBand enables low-latency and high-performance computingHow InfiniBand enables low-latency and high-performance computing

InfiniBand achieves low latency through hardware offloads. This executes functions of the router using the hardware directly, rather than depending on any intermediary software.

The key benefit of hardware offloading is increased performance and throughput, as the CPU is never put under pressure to make forwarding decisions. Acceleration mechanisms such as InfiniBand’s cut-through forwarding mode also improve latency. InfiniBand switches only fetch the header information of the data packet, immediately initiating the forwarding process when it determines the destination port. This eliminates the need to wait for the entire data packet to be received before forwarding.

RDMA technology and QoS can also be used to further reduce end-to-end transport latency and congestion control, meaning that InfiniBand never slows down in situations where Ethernet may struggle.

## Future trends and conclusionFuture trends and conclusion

A large number of advancements to InfiniBand’s networking solutions have been made in recent years, including brand new interfaces and technology to smooth connectivity.

In March this year NVIDIA announced the X800 series of networking switches, which claim to be the world’s first networking platforms capable of end-to-end 800Gb/s throughput. Based on what we’ve seen so far, other NVIDIA innovations in the coming years are likely to include faster data transfer speeds, lower latency and new applications in disciples such as machine learning.

But it isn’t game over for Ethernet yet, and parallel developments in Ethernet technology will pose a challenge to InfiniBand.

These Ethernet developments include:

- RDMA over Converged Ethernet (RoCE) to improve performance and CPU utilization

- Lossless Ethernet that offers advanced flow control, improved congestion handling, hashing enhancements and improved buffering

- the UEC is building a community of tech firms which aims to deliver Ethernet-based, open, interoperable, high performance, full-communications stack architecture to meet the growing network demands of AI and HPC at scale

But in environments where real-time data processing, high bandwidth and big data analytics are crucial — including HPC clusters, cloud computing and data centers — InfiniBand is the current leader of the pack.

## FAQ

What is InfiniBand?

InfiniBand is an open standard, high-speed, low-latency, scalable interconnect technology for use in high-performance computing (HPC) and data centers. It enhances and smooths communication by interconnecting servers, storage devices and embedded systems.

Why is InfiniBand different to other networking solutions?

While the rise of HPCs has seen rapid developments in CPU technology, InfiniBand’s HSI solution also addresses and improves the performance of the Peripheral Component Interface (PCI) for attaching hardware devices.

How does InfiniBand work?

NVIDIA’s systems are built around host channel adapters, switches, InfiniBand routers, cables and connectors. The Architecture Channel Adapter (CA) is divided into a Host Channel Adapter (HCA) and a Target Channel Adapter (TCA). InfiniBand switches are similar to other standard network switches, but perform better and cost less.

How are high speed data transfers maintained?

InfiniBand uses a two-layer architecture that separates the physical layer and data link layer from the network layer. This allows InfiniBand applications to exchange data across the network without putting pressure on the operating system, freeing the CPU for more important tasks.

What data transfer rates can InfiniBand support?

At its highest possible specs, InfiniBand can currently support data transfer rates of up to 400Gbit/s, which is significantly faster than traditional networking technologies.

How does InfiniBand latency compare to traditional Ethernet?

While Ethernet latencies range from around 20 to 80 microseconds, InfiniBand clocks in at 3 to 5 microseconds and significantly boosts the speed at which devices on the network can access data.

What tools are available to admins in InfiniBand?

InfiniBand includes a range of QoS features that allow admins to prioritize traffic, allocate bandwidth and manage network resources. Users can also create virtual lanes to isolate tasks and run multiple jobs on the network simultaneously.

How does InfiniBand’s RDMA technology improve data transfer?

InfiniBand’s RDMA technology enables direct data transfer between the memory of multiple computers without CPU involvement or using any intermediate software or hardware. This leaves the CPU free to work on more important tasks.

Why is direct data transfer without CPU involvement important?

This process eliminates the need for data to be copied, and offloads data transfer tasks to network hardware. In turn, this improves CPU utilization and reduces the load handled by individual processor cores.

In which fields is InfiniBand most used?

InfiniBand technology is commonly used in fields where large volumes of data need to be processed. This includes scientific research, financial modelling, meteorology and oil and gas exploration.

How does InfiniBand avoid data congestion?

If a network is approaching capacity, InfiniBand’s congestion management mechanism kicks in. It uses a credit system to indicate the amount of buffer space available for incoming data.

What does the future hold for InfiniBand?

This year NVIDIA announced the X800 series of networking switches, which claim to be the world’s first networking platforms capable of end-to-end 800Gb/s throughput. Future innovations are likely to include new interfaces and technology to smooth connectivity.

Is the game over for Ethernet?

Not at all. Future Ethernet advancements are set to include RDMA over Converged Ethernet (RoCE) to improve performance and CPU utilization, and Lossless Ethernet that offers advanced flow control, improved congestion handling, hashing enhancements and improved buffering.

## Explore Nebius AI

Get started​
Documentation​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

Nebius AI monthly digest, May 2024

In May, we published a guide on using DVC in Nebius, discussed Slurm vs K8s and fundamentals of LoRA, picked the best GPUs for CV, hosted a webinar on applying RAG — and welcomed our tech partner Weights & Biases with its Launch agent in Marketplace.

June 6, 2024
3 mins to read

### 

Introducing feature requests: share your ideas on advancing Nebius AI

There’s a new, convenient way to share ideas for advancing our AI-centric cloud, discuss them with us and the community, and get upvotes from others interested. Introducing the place for requesting Nebius AI features.

June 17, 2024
1 min to read

### 

Slurm vs Kubernetes: Which to choose for model training

Scaling your machine learning workloads will eventually require resource orchestration. This article compares the most popular options today — Slurm and Kubernetes, covering their design origins, ML adaptations and other factors to consider.

May 29, 2024
13 mins to read

Sign in to save this post
Sign In
