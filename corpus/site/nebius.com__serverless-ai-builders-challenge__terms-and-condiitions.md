# Terms and Conditions of the Nebius Serverless AI Builders Challenge (v1.0)

Source: https://nebius.com/serverless-ai-builders-challenge/terms-and-condiitions

Skip to main content

# Terms and Conditions of the Nebius Serverless AI Builders Challenge (v1.0)

The Nebius Serverless AI Builders Challenge (the “Challenge”) is organised by Nebius B.V. (“Nebius”) to recognise and reward the ML and AI practitioner community for building, documenting, and publishing reproducible examples using Nebius Serverless Jobs and Serverless Endpoints. The Challenge aims to grow awareness of Nebius Serverless products, produce high-quality practitioner-made content, and support the broader ML and AI community with reusable, open-source examples.

In these Terms and Conditions, the following definitions apply:

“Challenge Period” means the period commencing on the date these Terms and Conditions are published and ending on July 15, 2026, at 23:59 UTC.

“Judge Panel” has the meaning given in Section 7.

“Participant” or “Participants” means any individual or team admitted by Nebius for participation in the Challenge in accordance with Section 1.

“Submission” means a valid entry to the Challenge comprising all required components as set out in Section 3.

“Tenant ID” means the unique identifier associated with a Participant’s Nebius account.

## 1. Eligibility1. Eligibility

To participate in the Challenge, individuals or teams must meet the following requirements:

a) Be an individual developer, researcher, data scientist, or startup team of up to three (3) members. Both new and existing Nebius customers are eligible, including those already using Nebius Serverless Jobs or Serverless Endpoints.

b) Be 18 years or older.

c) Have access to a Nebius account (free tier is available for new registrations subject to the terms and conditions at Nebius website) and submit at least one Serverless Job or Serverless Endpoint run during the Challenge Period window. Existing Nebius accounts and prior Serverless usage are fully eligible.

d) Not be an employee, contractor, or agent of Nebius B.V. or any of its affiliates, subsidiaries, or partner organizations directly involved in organizing or judging the Challenge.

Nebius reserves the right, at its sole discretion, to refuse or reject any participation in the Challenge for any reason, including but not limited to failure to meet the eligibility criteria, incomplete or inaccurate submission, or any other reason that Nebius deems appropriate. Nebius’s decision in this regard shall be final and binding.

## 2. Compliance with Sanctions2. Compliance with Sanctions

By participating in the Challenge, Participants warrant that they, their team members, officers, and agents are not subject to any sanctions, embargoes, or other restrictive measures imposed by the United Nations, the European Union, the United States of America, or any other applicable government or regulatory authority.

Nebius reserves the right to verify compliance with these warranties and to refuse or disqualify any Participant if it has reason to believe that the Participant is not in compliance.

## 3. Submission Requirements3. Submission Requirements

A valid submission must include all of the following components:

a) Code repository — A public GitHub or GitLab repository containing:

• Code that uses or integrates with Nebius Serverless Jobs or Serverless Endpoints.

• A Dockerfile or reference to public Docker images for reproducibility.

• A README file with setup instructions, hardware configuration, expected outputs, and approximate runtime or cost information.

• An open-source license.

• No committed secrets, credentials, private keys, passwords, API tokens, access tokens, production datasets, confidential information, or unnecessary personal data.

b) Technical blog post — A post of at least 600 words, published on Medium, Dev community, a personal blog, Hashnode, or an equivalent public platform, that:

• Links to the code repository.

• Carries the required tag: #NebiusServerlessChallenge.

• Explains the problem, approach, Nebius architecture, implementation, and results.

• Evidenced that the submission runs on Nebius, in the form of screenshots, logs, or benchmark results.

Submissions must be entered via the official competition form on AI Academy before July 15, 2026, at 23:59 UTC. A submission is only valid if all two components are present, publicly accessible, and linked in the submission form.

Each Nebius Tenant ID may submit only one (1) entry to the Challenge. Where multiple submissions are received from the same Tenant ID, only the first valid submission will be considered; subsequent submissions from the same Tenant ID will be rejected

## 4. Originality and Content Requirements4. Originality and Content Requirements

By participating in the Challenge, Participants warrant that:

a) Their submission is original work, created solely for the purposes of the Challenge (or substantially extended for the Challenge), and has not been previously published in its current form.

b) The blog post contains original narrative content — including problem framing, results, architecture rationale, and lessons learned — and is not a copy or paraphrase of the code repository README.

c) Their submission does not infringe any third-party intellectual property rights, including copyright, trademark, patent, or trade secret rights.

d) Their submission does not contain harmful, offensive, defamatory, or otherwise inappropriate content.

Nebius reserves the right to disqualify any submission that violates these requirements.

## 5. Evaluation Criteria5. Evaluation Criteria

Each eligible submission will be scored by a domain-specific judge panel, using the following criteria:

Technical Implementation. Code runs end-to-end with no issues. Architecture is well-designed and appropriate for the use case. Nebius Serverless integration is correct, and effective. Code quality is high (readable, documented, no obvious bugs or anti-patterns).

Reproducibility. README is complete: architecture explanation, step-by-step setup, hardware/config specified, expected outputs shown, approximate runtime/cost noted. No committed secrets. Dependencies fully specified (pinned requirements.txt, pyproject.toml, environment.yml, or Dockerfile). Data is publicly available with download instructions, or synthetic data is included. Runs without modification.

Educational Content Quality. Post is well-structured and reads like a practitioner tutorial. Covers problem, approach, Nebius architecture, implementation walkthrough, results, and lessons learned. Technical depth is appropriate — assumes ML background, explains Serverless-specific choices. Writing is clear and concise.

Product Usage Depth. Serverless Jobs or Endpoints are central to the solution. The post explicitly explains why Serverless is a good fit for this use case (vs. alternatives). Non-trivial usage: handles orchestration, checkpoints, retry logic, async patterns, or similar real operational concerns.

Usefulness / Real-World Impact. Solves a clearly articulated real-world problem. The solution is immediately reusable or adaptable by others in the same domain. Has obvious practical value beyond the competition.

Originality / Creativity. Novel approach, domain-specific insight, or creative application of Serverless that hasn’t been done before (or is a meaningful improvement on prior art). Clearly goes beyond following a tutorial.

Individual scores assigned by judges will not be published or disclosed to Participants. Only the final award outcomes — winners, Special Award recipients, Community Choice, and Awesome Serverless Award recipients — will be announced publicly.

## 6. Automated Eligibility Check6. Automated Eligibility Check

Automated eligibility checks will run on a rolling basis during the submission period. All submissions will be assessed for structural completeness, content safety, topic relevance, and Serverless AI product signal. Submissions that do not pass this check will be notified of the main reason for the outcome, where reasonably possible, and may correct and resubmit their submission before the deadline. Each Participant is permitted a maximum of one (1) resubmission. Nebius may withhold detailed detection logic or security information where disclosure could compromise the integrity, security, or anti-abuse controls of the Challenge.

Automated tools may be used to support eligibility checks, content safety review, topic relevance assessment, Serverless product signal detection, and preliminary scoring. These tools are used to assist the Challenge administration and judging process. Final award decisions are subject to human review and confirmation by Nebius and/or the Judge Panel.

If a submission is rejected or not advanced as a result of an automated eligibility check, the Participant may request human review of the outcome by contacting Nebius at serverlesschallenge@nebius.com.

## 7. Judge Panel7. Judge Panel

The Challenge will be judged by domain-specific panels (each a “Judge Panel”), consisting of:

a) Recognised external experts in the relevant domain (which may include, without limitation; AI & ML, Healthcare & Life Science, or Robotics, or other fields as appropriate to the Submissions received), invited by Nebius.

b) Representatives from Nebius, providing expertise on Nebius Serverless products and engineering standards.

The Judge Panel is responsible for evaluating submissions and nominating winners in accordance with the published rubric and process. Judge Panel decisions are final subject to confirmation by Nebius.

## 8. Prizes8. Prizes

Nebius will award prizes to Participants whose Submissions are selected by the Judge Panel. Prizes comprise Nebius promotional credits, and non-monetary recognition, including certificates, listings and features on Nebius channels.

The following prize categories are available:

• Top 3 Overall — First, second, and third place awards, each receiving Nebius promotional credits.

• Special Awards — Best submission in the relevant domain, each receiving Nebius promotion; credits.

• Community Choice — The eligible Submission receiving the most community votes, as, determined by public voting after eligibility screening, receiving Nebius promotional credits.

• Awesome Serverless Awards — Up to twenty (20) outstanding Submissions nominated by the Judge Panel, each receiving Nebius promotional credits.

• Participation Reward — All valid eligible Submissions receive a Nebius promotional credit.

Nebius promotional credits are issued as promotional codes and are subject to the Nebius platform terms of use as available at Nebius website. Promotional credits are valid until 31 December 2026, after which any unused credits will lapse. Prizes are non-transferable and may not be exchanged for cash or any other form of payment.

Full details of prize values are published on the Challenge website. Nebius reserves the right to modify, substitute, or withdraw any prize at any time prior to the announcement of winners. It is the responsibility of Participants to review the Challenge website for the most current prize information.

## 9. Participation Terms9. Participation Terms

By participating in the Challenge, Participants agree to:

a) Provide accurate and complete information in their Submission and in the submission form.

b) Grant Nebius the right to use their Submission, including repository, blog post, and associated materials, for promoting the Challenge and Nebius Serverless AI products, as described in Section 11.

c) Participate in the evaluation process and provide any additional information reasonably requested by the Judge Panel.

d) Attend winner announcement events or online sessions where reasonably possible, and that advance notice has been given.

e) Ensure that any personal data included in their submission materials is included lawfully and in accordance with applicable data protection laws, and that they have obtained all rights and permissions, required to submit, publish, and make such materials available as part of the Challenge.

f) Comply with all applicable laws and regulations in connection with their participation.

## 10. Disqualification10. Disqualification

Participants may be disqualified, at Nebius’s sole discretion, for any of the following reasons:

a) Failure to meet eligibility requirements.

b) Submitting work that is not original, is plagiarised, or infringes third-party rights.

c) Providing false or misleading information in the submission form.

d) Violations of the content requirements set out in Section 4.

e) Any conduct that Nebius determines to be harmful to the integrity of the Challenge or to other Participants.

Nebius’s decision on disqualification is final and binding.

## 11. Publication and Marketing11. Publication and Marketing

By participating in the Challenge, Participants acknowledge that Nebius may publish and otherwise use the information and materials described in this Section 11 for the purposes of administering, announcing, and promoting the Challenge and showcasing examples built on Nebius Serverless products.

Nebius may publish and use the following information and materials:

a) Participants’ names, team names, public professional profiles or handles provided in the submission form, country or region where relevant to the Challenge announcement, and company, organization, or affiliation where provided by the Participant;

b) submission title, summary, category, award category, ranking or other award outcome, repository links, blog post links, screenshots, excerpts, outputs, and other submitted materials;

c) information about winners, Special Award recipients, Community Choice recipients, Awesome Serverless Award recipients, shortlisted submissions, highly ranked submissions, and other selected eligible submissions.

Nebius may use the information and materials listed above in Challenge-related communications and materials, including the Nebius website, the Challenge website, Nebius social media channels, blog posts, newsletters, press releases, webinars, conference presentations, product documentation, case studies, and other Nebius marketing or promotional materials.

Nebius will not use a Participant’s image, voice, interview, quote, testimonial, or similar endorsement in marketing materials unless the Participant has separately agreed to such use, except where the Participant has already made the relevant material publicly available as part of the submission.

## 12. Publication of Results12. Publication of Results

The results of the Challenge will be published on or before August 7, 2026, on the Nebius website and official Nebius social media channels. The publication will include the names of the winners, their team names (if applicable), and links to their submissions. Winners will be notified individually via email before the public announcement.

## 13. Intellectual Property13. Intellectual Property

a) Participants retain all intellectual property rights to their submitted code, blog posts, and associated materials.

b) By participating in the Challenge, each Participant grants Nebius a non-exclusive, fully paid-up, royalty-free, worldwide, and perpetual license to use, reproduce, distribute, and make publicly available their submission materials — including code repository content, blog posts, screenshots, and outputs — solely for the purposes of (i) evaluating the submission, and (ii) promoting the Challenge and Nebius Serverless products.

c) This license does not transfer ownership of the Participant’s intellectual property and does not restrict the Participant from using, licensing, or commercialising their own work independently.

## 14. Limitation of Liability14. Limitation of Liability

a) To the maximum extent permitted by applicable law, Nebius, its officers, directors, employees, agents, and representatives shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising out of or related to the Challenge, including but not limited to:

• Any errors, omissions, or inaccuracies in the evaluation process;

• Any delays, cancellations, or modifications to the Challenge schedule or prizes;

• Any technical malfunctions, failures, or interruptions;

• Any loss of business opportunities, revenue, profits, or goodwill claimed to result from participation or non-selection.

b) Nebius makes no warranties or representations regarding the Challenge, the evaluation process, or any prizes, and expressly disclaims all warranties, whether express or implied.

c) Participants acknowledge that participation in the Challenge does not guarantee any business relationship, partnership, investment, or commercial engagement with Nebius.

d) Nothing in these Terms and Conditions shall exclude or limit Nebius’s liability for death or personal injury caused by negligence, fraud or fraudulent misrepresentation, or any other liability that cannot be excluded or limited under applicable law.

## 15. Force Majeure15. Force Majeure

a) Nebius shall not be liable for any failure or delay in performing its obligations under these Terms and Conditions if such failure or delay is due to circumstances beyond its reasonable control, including but not limited to acts of God, natural disasters, pandemics, war, terrorism, government actions, strikes, or failure of telecommunications or internet services.

b) In the event of a force majeure occurrence, Nebius may suspend, modify, or cancel the Challenge as necessary. Nebius will make reasonable efforts to notify Participants through the Challenge website or direct communication.

c) Participants shall have no claim against Nebius for any damages or compensation arising from any force majeure event.

## 16. Governing Law16. Governing Law

These Terms and Conditions shall be governed by and construed in accordance with the laws of the Netherlands. Any disputes arising out of or related to the Challenge shall be resolved by the District Court of Amsterdam (Rechtbank Amsterdam).

## 17. Amendments17. Amendments

Nebius reserves the right to amend these Terms and Conditions at any time without notice. Participants are responsible for checking the latest version of the Terms and Conditions on the Challenge website.

## 18. Privacy Notice18. Privacy Notice

18.1. Controller

Nebius B.V., a company incorporated in the Netherlands, is the controller of personal data processed in connection with the Challenge.

Controller contact details:

Nebius B.V.

Schiphol Boulevard 165, 1118 BG Schiphol, the Netherlands

privacy@nebius.com

18.2 Personal Data We Process

Nebius may process the following categories of personal data in connection with the Challenge:

a) identification and contact details, such as name, email address, country or region, team name, company, organization or affiliation, and public profile or social media handles where provided;

b) Nebius account and platform usage information relevant to the Challenge, such as confirmation that a Participant has a Nebius account, Serverless Jobs or Serverless Endpoints usage signals, run metadata, timestamps, product usage indicators, and technical logs required to verify eligibility and execution;

c) submission information, such as repository links, blog post links, submission title, category, description, screenshots, logs, endpoint URLs, notebook outputs, benchmark results, README content, and other materials submitted by the Participant;

d) judging and administration information, such as eligibility status, rubric scores, judge comments, ranking, award category, communications with Nebius, and records of disqualification or resubmission;

e) prize fulfilment information, such as gift card delivery details, where required for prize administration;

f) marketing and publicity information, such as names, team names, submission links, award information, excerpts, screenshots, outputs, and other submitted materials used in accordance with Section 11.

Nebius asks Participants not to include unnecessary personal data in submissions, repositories, screenshots, logs, notebooks, endpoint outputs, benchmark materials, or other submission materials.

18.3 Purposes and Legal Bases

Nebius processes personal data for the following purposes and legal bases:

a) Registration, administration, communications with Participants, eligibility checks, and operation of the Challenge. This processing is necessary for the performance of these Terms and Conditions or to take steps at the Participant’s request before entering into them.

b) Verification of submissions, judging, scoring, selection of winners, prevention of fraud, abuse, plagiarism, security incidents, and protection of the integrity of the Challenge. This processing is necessary for Nebius’s legitimate interests in operating a fair, secure, and credible Challenge.

c) Compliance with sanctions, and other legal obligations. This processing is necessary for compliance with legal obligations to which Nebius is subject.

e) Publication of results and Challenge-related publicity as described in Sections 11 and 12. This processing is necessary for the performance of these Terms and Conditions and for Nebius’s legitimate interests in announcing results, recognizing Participants, and promoting the Challenge and Nebius Serverless products.

f) Optional marketing uses, such as use of interviews, testimonials, photographs, video recordings, quotes, or endorsements not already made public by the Participant as part of the submission. This processing will be based on the Participant’s separate consent, where required by applicable law.

18.4 Recipients

Nebius may share personal data with the following categories of recipients where necessary for the purposes described in this Section 18:

a) Nebius affiliates and group companies involved in administering, supporting, promoting, or operating the Challenge;

b) members of the Judge Panel, including external judges, solely for the purposes of evaluating submissions and selecting winners;

c) service providers acting on Nebius’s behalf, such as hosting providers, cloud services, form and submission platforms, email and communication tools, analytics tools, prize fulfilment providers, payment processors, tax and accounting providers, and security providers;

e) public audiences, where information is published in accordance with Sections 11 and 12;

f) professional advisers, auditors, insurers, banks, payment providers, and competent authorities where required for legal, accounting, compliance, dispute resolution, or enforcement purposes.

18.5 International Transfers

Some recipients of personal data may be located outside the European Economic Area.

Where Nebius transfers personal data outside the European Economic Area, Nebius will do so in accordance with applicable data protection law, including by relying on an adequacy decision, the European Commission’s Standard Contractual Clauses, or another lawful transfer mechanism where required.

18.6 Retention

Nebius will retain personal data only for as long as reasonably necessary for the purposes described in this Section 18.

Unless a longer retention period is required by law or necessary for legal claims, tax, accounting, audit, security, or compliance purposes.

18.7 For any matters relating to the processing of personal data that are not specifically addressed in these Terms and Conditions, Nebius will process personal data in accordance with the Nebius Privacy Notice available at: Nebius website.

By participating in the Nebius Serverless AI Builders Challenge, Participants acknowledge that they have read, understood, and agreed to these Terms and Conditions.
