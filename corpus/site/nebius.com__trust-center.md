# Trust center

Source: https://nebius.com/trust-center

Skip to main content

## Security by design

We integrate security into the design and development of our systems from the outset, ensuring that security controls and safeguards are built-in, not bolted on.

## Security by default

We configure our systems to be secure by default, ensuring that the most secure settings and options are enabled automatically, without manual intervention or explicit configuration.

## Security compliance

We are committed to the highest standards of security, privacy and business continuity, implementing GDPR and CCPA-compliant policies and practices with full transparency.

## SOC 2 Type II

With HIPAA. Evaluates the design and operational effectiveness of the controls.

## SOC 3

SOC 3 is a summarized version of the SOC 2 Type II audit, designed for public consumption.

## ISO 22301

Demonstrates resilience against disruptions while maintaining critical service continuity.

## ISO 27001

Demonstrates that Nebius has implemented comprehensive measures to protect personal data.

## ISO 27018

Demonstrates that Nebius is committed to protecting personal data responsibly.

## ISO 27032

By aligning with this guidance, Nebius demonstrates a proactive approach to cybersecurity.

## ISO 27701

Extends ISO/IEC 27001 with privacy-specific requirements for managing PII.

## ISO 27799

By following this standard, Nebius strengthens its security controls for health-related data.

## ISO 42001

Confirms compliance with the international standard for Artificial Intelligence Management Systems.

## NIS 2

Nebius aligns its cybersecurity practices with European Union’s cybersecurity law.

## DORA

Nebius aligns with EU uniform ICT risk management requirements for the financial sector.

## CSA STAR Level 1

Listing in the CSA STAR Registry demonstrates transparency about cloud security controls.

## Key security features

## Data center security

Our infrastructure is hosted in data centers that meet high industry standards for physical and environmental security.

These facilities are equipped with multi-layered access controls, including biometric authentication, video surveillance and 24/7 on-site security personnel. Critical systems are protected by redundant power, cooling and fire suppression systems, to ensure high availability and resilience.

## Secure SDLC

Our software development process employs separate development, test and production environments, with strict segregation of responsibilities.

We implement comprehensive version control and maintain controls over source code libraries, to ensure we adhere to structured SDLC methodologies. Security is integrated into every development phase — we conduct thorough application security testing and utilize automated source-code analysis tools to detect potential security defects before deployment.

## Vulnerability management and penetration testing

We maintain a robust vulnerability management program that includes automated and manual scanning of systems and applications, regular security assessments and integration of threat intelligence to detect emerging risks.

Identified vulnerabilities are prioritized based on severity, exploitability and business impact. We apply patches promptly, implement compensating controls when needed and track remediation through to resolution.

## Monitoring and incident management

We continuously monitor our systems, networks and applications for signs of suspicious activity, performance anomalies and potential security threats. Our monitoring infrastructure integrates automated alerting, log analysis and threat detection to provide real-time visibility across our environment.

In the event of a security incident, we follow a structured incident response plan designed to contain, investigate and remediate the issue swiftly. Our incident management process includes clear escalation paths, cross-functional coordination, root cause analysis and post-incident reviews. We are committed to transparency and, when appropriate, provide timely notifications to affected stakeholders, in accordance with regulatory and contractual obligations.

## Third-party risk management

We carefully assess and manage the security and privacy risks associated with our third-party vendors and service providers. All third parties undergo a risk-based evaluation process that includes due diligence, contractual safeguards and security assessments that are aligned with industry standards.

We ensure that our vendors implement appropriate technical and organizational measures to protect data and maintain service integrity. Ongoing monitoring, regular reassessments and audit rights help us maintain visibility into the evolving risk landscape.

## Access management

We implement strict access management controls to ensure that only authorized users have access to our systems and sensitive data. Our access policies are based on the principle of least privilege, meaning users are granted the minimum necessary access to perform their job functions.

Access rights are regularly reviewed and updated based on role changes, project requirements and security policies. We employ multi-factor authentication (MFA) for an added layer of security and we enforce strong password policies. Additionally, access to critical systems is closely monitored and logged, to detect any unauthorized attempts or suspicious activities.

## At rest and in-transit encryption

Our storage is encrypted by default* using strong encryption standards to protect sensitive data from unauthorized access. This ensures that all sensitive information remains secure, even in the event of a storage media compromise. Data transmitted between systems or across networks is encrypted by using secure protocols, such as TLS, to protect it from interception or tampering during transmission.

- 
- 
- 
- 
- 
- 

## Customer workload isolation

We design our infrastructure to ensure strong isolation between customer environments, to prevent unauthorized access and data leakage across tenants.

## Network isolation

Customer environments are segmented using virtual private clouds (VPCs) which provide isolated software-defined networks for secure communication and access control.

## InfiniBand isolation

We enforce traffic segregation across the InfiniBand network layer, ensuring strict separation of data paths.

## Kubernetes isolation

In our Managed Services for Kubernetes® offering, each tenant’s cluster is isolated at the virtual machine level. This ensures that workloads run in dedicated environments, enhancing both security and performance.

## Shared responsibility matrix

Understanding who’s responsible for what is critical to maintaining a secure cloud environment. Our shared responsibility model clarifies security obligations between Nebius and our customers.

Applications

Orchestration

Compute. Networking. Storage

On Premise

Identity & access management

Customer data backups

Application security

OS security

Network security (overlay)

Monitoring and logging

Encryption at rest

Network security (underlay)

Hardware security

Data center security

 Nebius

 Customer

 Shared**

## Security services

Our platform includes built-in security services that help customers manage access and maintain visibility across their environments.

## Identity and access management

Fine-grained access controls allow customers to manage user roles and permissions according to the principle of least privilege. Identity and access management policies can be customized to enforce secure access to resources and support integration with external identity providers.

## Audit logs

Comprehensive audit logging captures security-relevant events, including authentication attempts, configuration changes and access to sensitive data. These logs are immutable, time-stamped and can be used for compliance, troubleshooting and incident response.

## SecretStash

SecretStash enables you to store sensitive data in an encrypted form. For example, you can save API keys, tokens or certificates. After that, you can reuse them in your scripts, configuration files or applications, and thus avoid hardcoding sensitive data.

## Key Management Service

Key Management Service enables you to issue and store cryptographic keys, so you can protect and secure your applications. By using KMS symmetric and asymmetric keys, you can encrypt and decrypt data, sign hashes or apply envelope encryption.

## Privacy and data protection

## GDPR and other applicable legislation

As an EU data processor, we operate under GDPR — the gold standard for data privacy worldwide. This regulatory framework ensures our customers receive comprehensive data protection that meets the highest global standards. By building privacy by design into our products, we provide the robust data protection that GDPR compliance guarantees, fostering customer trust while ensuring full regulatory compliance.

Our technical and organizational measures are designed to safeguard data and uphold data subject rights; and ensure transparency, security and accountability throughout our services.

## Data residency

We honor our customers’ data residency requirements by ensuring that customer data remains within the geographic region of their choice. Our infrastructure is designed to support regional data localization, allowing customers to select where their data is stored and processed.

This approach helps meet compliance obligations and organizational policies related to security and privacy.

## Privacy by default and design

We embed Privacy by Design and by Default principles through concrete actions: conducting privacy impact assessments for each and every initiative potentially affecting personal data, establishing clear boundaries for legitimate interest processing, and maintaining full transparency in our communications.

Our systems default to the most privacy-friendly settings, implement role-based access controls, and automatically anonymize data where feasible. We integrate privacy considerations into our architecture from the ground up, ensuring data protection is built into our systems rather than added as an afterthought.

## Contact us

If you have any questions or concerns related to security, or if you’ve noticed something suspicious, please email us.

For any privacy-related inquiries, please contact our privacy team.
Email Security teamEmail Privacy team

* Excluding Network SSD Non-replicated and Network SSD IO M3 disks.

** Logging, monitoring and encryption are shared responsibilities in Nebius, as customers must configure observability and choose between encrypted or faster unencrypted storage based on their needs.
