# Storing personal data on Nebius AI Cloud: Security, GDPR and AI readiness

Source: https://nebius.com/blog/posts/storing-personal-data-on-nebius-ai-cloud

Skip to main content

If you work with personal data and need to store it in the cloud, you have to choose a cloud provider that offers appropriate storage. If you’re wondering whether our cloud can store and process personal user data, the answer is yes. Our platform ensures the secure storage of personal data, in full compliance with applicable regulations. But what does that mean in practice? Let’s break it down.

# What qualifies as personal data?What qualifies as personal data?

First, let’s define what falls under the term of personal data. Under General Data Protection Regulation (GDPR), personal data is defined in Article 4(1) as:

“Any information relating to an identified or identifiable natural person (‘data subject’); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person.”

In simple terms, personal data is any information that can be used to identify someone, either on its own or when combined with other data. This includes obvious identifiers like names and ID numbers, but also less direct ones like IP addresses or location data.

### Special categories of personal data and sensitive personal dataSpecial categories of personal data and sensitive personal data

Within personal data, there are specific categories that constitute a subset deemed as sensitive personal data. These categories require additional security measures from data processors — as described by different frameworks. GDPR, HIPAA and PCI DSS are the most significant in this domain.

- 

Under GDPR, special categories of personal data include information about a person’s racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership, genetic data, biometric data (for identification), health data, and data concerning sex life or sexual orientation (Article 9). These require extra protection and can only be processed under specific legal bases.

In addition to the GDPR definition, you are probably familiar with frameworks such as HIPAA and PCI DSS, which are focused on specific types of sensitive data.

- 

HIPAA (Health Insurance Portability and Accountability Act) is a US law that covers protected health information (PHI), focusing on data handled by healthcare providers, plans and clearinghouses — this has overlap with GDPR guidelines for health data, but is narrower in scope.

- 

PCI DSS (Payment Card Industry Data Security Standard) is the industry standard for securing payment card data — such as credit card numbers and security codes. While GDPR doesn’t classify financial data as “special,” it still requires extra protection.

Currently, Nebius AI Cloud does not support special categories or sensitive personal data processing. For example, PHI and payment card data cannot be stored or processed in our cloud. However, we’re actively working toward HIPAA compliance, and we plan to undergo a third-party HIPAA audit later this year.

# AI and personal dataAI and personal data

Most AI models are trained on non-personal data. Machine learning engineers typically work with large datasets for pre-training and fine-tuning foundational models, and such datasets often exclude personal data. However, there are exceptions.

Some ML-driven applications require datasets containing personal data. Take demand forecasting, for example — retailers may use geolocation databases with real addresses to predict purchasing patterns. Meanwhile, RAG-based AI systems (retrieval-augmented generation), like customer support chatbots, rely on retrieving personal details to generate accurate, personalized responses.

For businesses operating in regulated industries, the ability to securely store personal data is essential. GDPR mandates that cloud service providers (CSPs) like Nebius act as compliant data processors, to ensure rigorous security measures are in place.

# How Nebius protects your dataHow Nebius protects your data

At Nebius, data security is our top priority — whether it’s personal data or non-personal datasets for AI training. We follow a security-by-design approach, meaning security regulations are embedded into the development of our infrastructure and applications from day one.

Our key security measures include:

- 

Encryption for data both in transit and at rest aligned the industry’s best practice.

- 

Data retention and deletion policies that comply with GDPR requirements

- 

Continuous internal monitoring to prevent data breaches

- 

Regular security testing and vulnerability assessments

- 

Incident response and breach notification procedures

- 

Secure data backup procedures

These security measures apply across computation and data storage services within the Nebius AI Cloud platform, including:

- 

Network disks

- 

Shared filesystem

- 

Object Storage

- 

Managed Service for PostgreSQL

When you become a Nebius customer, you sign our Data Processing Agreement (DPA), which outlines Nebius’ role as a data processor and its legal obligations.

By choosing Nebius, you ensure that your personal data is securely stored and meets the highest standards of data protection and compliance.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- What qualifies as personal data?

- Special categories of personal data and sensitive personal data

- AI and personal data

- How Nebius protects your data

## See also

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

Nebius and Outerbounds form strategic technology partnership through integration

We are excited to unveil our latest collaboration: Nebius AI Cloud, the ultimate cloud for AI innovators, and Outerbounds, an AI/ML platform powered by the popular open-source framework Metaflow, are now integrated as part of a broader technology partnership.

March 11, 2025
5 mins to read

### 

Nebius monthly digest: March 2025 and NVIDIA GTC

NVIDIA GTC was the highlight of last month for us. Our extensive participation included being a platinum sponsor, a strong presence with the booth, two tech talks, interviews with our leaders, partners and customers, and much more.

April 7, 2025
4 mins to read

Sign in to save this post
Sign In
