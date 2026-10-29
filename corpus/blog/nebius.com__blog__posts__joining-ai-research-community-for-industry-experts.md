# Joining AI research community: overview for industry experts

Source: https://nebius.com/blog/posts/joining-ai-research-community-for-industry-experts

Skip to main content

The global network of ML engineers is divided into two parts: industrial and academic. The flow of information, methods of interaction, and especially events follow unique unspoken rules in different parts. If you belong to the first world, then the second may seem distant and even irrelevant to you.

Indeed, it is possible to build AI products for end users without venturing into research territory. However, understanding the second world and at least occasionally participating in AI research conferences will boost your perspective, make you a more versatile specialist, and give you new ideas that can be directly applied in your work.

This article will help ML engineers from companies learn how the world of AI research is structured. We will cover all the main topics, including articles, conferences, datasets, and the transfer of scientific ideas into services.

For researchers in the field of computer science (which includes not only the AI domain, of course), the primary indicator of success is the publication of their work at one of the top international conferences. This represents the initial “checkpoint” in gaining recognition for their research. For example, key AI conferences traditionally include the International Conference on Machine Learning (ICML) and the Conference on Neural Information Processing Systems (NeurIPS, formerly known as NIPS). For the most interesting and relevant ones in 2024, see the list curated by ML experts at Nebius AI. There are also many conferences dedicated to specific areas within ML, such as computer vision, information retrieval, speech technology, machine translation, and others.

## The many pros of sharingThe many pros of sharing

Those outside the computer science field might believe that the most valuable ideas should be kept secret to capitalize on their uniqueness. However, the reality is quite the opposite. A scientist’s reputation is judged by the significance of their research and how frequently their papers are cited by others (the citation index). This is a crucial aspect of their career. Researchers advance in their professional hierarchy and earn respect in their community only if they consistently produce influential work that is published, widely recognized, and forms the foundation for the work of other scientists. One example of such a foundational, highly cited study is this paper on the EfficientNet family of models, presented at ICML 2019 (over 13,000 citations).

Many top studies, and possibly the majority, are the result of international collaborations between researchers from various universities and companies around the world. A significant and highly valued milestone in a researcher’s career is when they gain the experience to independently identify and evaluate ideas. However, even beyond this point, the invaluable assistance of colleagues remains essential. Scientists aid each other in refining ideas and co-author papers. The greater a researcher’s contribution to science, the easier it becomes for them to connect with like-minded peers.

Lastly, due to the vast density and accessibility of information today, different researchers often independently develop very similar (and indeed valuable) scientific ideas simultaneously. If you don’t publish your idea, it’s almost certain that someone else will. The “winner” in these cases is usually not the one who conceived the innovation slightly earlier, but rather the one who published it first. Or it could be the one who presented the idea in the most comprehensive, clear, and persuasive manner.

## Describing an achievement in text and codeDescribing an achievement in text and code

An academic article is constructed around the core idea proposed by the researcher, which represents their contribution to computer science. The article begins with a description of this idea, succinctly formulated in a few sentences. Following this is an introduction that outlines the range of problems addressed by the proposed innovation. The description and introduction are generally written in simple language, understandable to a broad audience. After the introduction, it’s necessary to formalize the presented problems in mathematical language and introduce precise definitions.

The researcher then must present a clear and comprehensive explanation of the essence of their innovation, highlighting how it differs from previous, similar methods. All theoretical expositions must be supported by references to existing proofs or independently verified by the author. This might involve certain assumptions, such as providing a proof for a scenario where there is an infinite amount of training data (clearly an unachievable situation) or where the data is completely independent. Nearing the end of the paper, the researcher discusses the experimental results they have achieved. Here’s a great example of a paper that follows this structure, presented at NeurIPS 2019 by the developers of PyTorch.

For an article to be favorably received by reviewers invited by conference organizers, it must possess one or more key attributes. The most critical factor increasing the likelihood of approval is the scientific novelty of the proposed idea.

Often, this novelty is measured against existing ideas, and it is the responsibility of the article’s author, not the reviewers, to make this assessment. Ideally, the author should thoroughly discuss existing methods in the article and, if feasible, demonstrate how they are special cases of the proposed method. By doing so, the scientist demonstrates that conventional approaches are not always sufficient, having expanded and proposed a more comprehensive, adaptable, and thus more effective theoretical framework. If the novelty is indisputable, reviewers tend to be less stringent in their assessment of other aspects, such as overlooking poor English.

To reinforce the novelty, it’s best to include comparisons with existing methods using one or several open datasets that are recognized in the academic community. Examples of such datasets include the ImageNet image repository and databases from institutions like the Modified National Institute of Standards and Technology (MNIST) and the Canadian Institute For Advanced Research (CIFAR). A complication arises because these “academic” datasets often differ structurally from real-world data encountered in the industry. As a result, the effectiveness of the proposed method can vary with different datasets. Researchers, especially those with ties to the industry, are mindful of this discrepancy and might include disclaimers indicating different outcomes on their proprietary data versus publicly available datasets.

Occasionally, a method is so specifically tailored to an open database that it underperforms with real-world data. A solution to this prevalent issue is the introduction of new, more representative datasets. However, this often involves private content that companies cannot legally disclose. In such cases, they may resort to data anonymization, removing identifiable details like faces and numbers in photographs. Furthermore, for a dataset to be widely accepted and become a benchmark in the scientific community, it requires more than just making it available; it necessitates a separate, well-cited publication detailing its merits and advantages.

When open datasets are absent in the research topic, reviewers are left to take the author’s results at face value. Theoretically, an author could exaggerate these results and remain undetected, but such practices are unlikely in the academic community, where the majority of scientists are genuinely committed to advancing science.

In several ML fields it’s also customary to attach code links (usually to GitHub) to papers. For instance, one of the 2022 OpenAI papers on language models using human feedback refers to a corresponding InstructGPT page on GitHub. The papers themselves usually contain little or no code, or just pseudocode. Here again, complications arise if the paper is written by a researcher from a company rather than a university, as corporate or startup code is by default protected by NDA. Researchers and their colleagues often have to put in significant effort to separate the code related to the described idea from internal and private repositories.

The likelihood of publication also depends on the relevance of the chosen subject. Relevance is largely dictated by products and services: if a corporation or startup is interested in developing a new service or improving an existing one based on the idea from the paper, it’s always a huge advantage.

As previously mentioned, papers in computer science are rarely written solo. However, typically one of the authors invests much more time and effort than the others, making their contribution to the scientific novelty the greatest. This individual is listed first among the authors, and in future citations of the paper, only their name might be mentioned (for example, “Smith et al, ” which translates from Latin as “Smith and others”). Nevertheless, the contributions of the other authors are also extremely valuable — otherwise, it would be impossible for them to be listed as authors.

## Peer reviewPeer review

Submissions for articles usually close several months prior to the conference. After an article is submitted, reviewers typically have 3–5 weeks to read, evaluate, and comment on it. This process follows either a single-blind system, where the authors do not see the reviewers’ names, or a double-blind system, where the reviewers also do not see the authors’ names. The latter is considered more impartial: various studies have demonstrated that an author’s reputation can influence a reviewer’s decision. For instance, they might assume that a scientist with numerous published articles is inherently deserving of a higher evaluation.

The famous arXiv

Even in a double-blind review, however, a reviewer can often guess the author if they are in the same field. Additionally, the article may already be published in the arXiv database — the largest repository of scientific papers — by the time it undergoes review. Conference organizers do not prohibit this, but they recommend using a different title and abstract for the arXiv publication. Nonetheless, if the article has been posted there, locating it is still relatively straightforward.

Evaluating an article always involves multiple reviewers. One of them is assigned the role of a meta-reviewer, whose job is to overview the verdicts of their colleagues and make the final decision. If there’s a divergence in the reviewers’ assessments, the meta-reviewer may also read the paper for a more comprehensive understanding.

Sometimes, after reviewing the ratings and comments, authors have the opportunity to engage in discussion with the reviewer; there’s even a chance to persuade them to change their decision (though this system is not in place at all conferences, and influencing the final verdict is even rarer). In these discussions, authors cannot refer to other scientific works, except for those already cited in their paper. The goal is simply to help the reviewer better understand the content of the article.

### Where to publishWhere to publish

Computer science articles are more commonly submitted to conferences than to scientific journals. The reason is that journal publications have more stringent requirements and the review process can take months or even years. Computer science is a rapidly evolving field, so authors are usually unwilling to wait that long for publication. However, a paper accepted at a conference can later be expanded (e.g., with more detailed results) and published in a journal where there are less strict limitations on length.

## What to expect when visitingWhat to expect when visiting

The format of the authors' presence for accepted papers at the conference is determined by the reviewers. If a paper is given the green light, authors are most often allotted a space for a poster presentation. A poster is a static slide summarizing the paper with illustrations. Parts of the conference hall are filled with long rows of poster stands. Authors spend a significant amount of time near their posters, interacting with scientists interested in their work.

Source: AGU

A slightly more prestigious form of participation is a quick presentation, or a “lightning talk.” If reviewers deem the paper worthy of a lightning talk, the author is given about three minutes to speak in front of a broad audience. On one hand, a lightning talk is a great opportunity to present the idea not only to those who showed interest in the poster but also to a wider audience. On the other hand, visitors who approach the poster are typically more prepared and deeply immersed in your specific topic than the average listener in the hall. Therefore, during a lightning talk, it’s crucial to efficiently introduce the audience to the subject matter.

Usually, at the end of their lightning talk, authors mention their poster number, enabling interested listeners to find it and gain a deeper understanding of the paper.

And finally, the most prestigious option is a combination of a poster and a full presentation of the idea, allowing for a more relaxed and detailed discussion.

Source: ICML

Participating in conferences as an author of an accepted paper leads to impressive results. For instance, in 2010, Yutaka Matsuo, a distinguished AI researcher from Japan, developed an algorithm capable of detecting early earthquake signs by monitoring Twitter mentions of tremors. He showcased this work at the annual WWW conference, significantly boosting his career. In 2019, he became the first AI specialist added to the board of the Japanese technology giant Softbank, reflecting the impact of his study and the attention it garnered from major IT corporations.

However, scientists, including paper authors, attend conferences not solely for self-promotion. Firstly, they naturally seek out posters related to their field for obvious reasons. Secondly, it’s important for them to expand their contact list with the aim of future collaborative academic work. This is not hunting — or at least, it’s just the very first stage of what is typically followed by a mutually beneficial exchange of ideas, findings, and joint work on one or several papers.

At the same time, productive networking at a top conference is challenging due to the total lack of free time. If a scientist still has energy left after a full day spent at lectures and discussions around posters, and has overcome jet lag, they might head to one of the numerous parties. These are often organized by corporations and, as a result, these gatherings sometimes have more of a hunting vibe. However, many attendees use these events not for job hunting but for networking. In the evening, with no lectures or posters, it’s easier to “catch” the specialist you’re interested in. As an example, OpenAI hosted a party during the days of NeurIPS 2022.

Source: Nemanja Rakicevic via Towards Data Science

## Getting it into users' handsGetting it into users' hands

Computer science (again, including AI/ML) is one of the few fields where the interests of corporations and startups are closely intertwined with the academic realm. At conferences like NeurIPS, ICML, and others, numerous industry professionals attend, not just those from universities. This is typical for computer science but quite the opposite for most other sciences.

Perhaps the most cited example of a scientific work whose ideas quickly found application in services is 'Attention Is All You Need' from 2017. This paper marked the beginning of the famous transformers, which underlie many modern AI products — we recently discussed this story in detail. The paper was presented at NIPS 2017, later renamed to NeurIPS.

On the other hand, not all ideas presented in papers are immediately applied to the creation or improvement of services. The cycle of transferring into production can vary and sometimes spans decades. For instance, convolutional neural networks, whose roots go all the way back to 1980, only gained real prevalence in the 2010s. Their use continues today: for example, Midjourney utilizes this type of network, among others. There might not be such long 'breaks' anymore: advancements in the ML field, as you know, were too long slowed down by a lack of computing power and data. The current pace of development seems unlikely to allow such a situation to recur, but it’s impossible to say for sure: for example, quantum computing has not yet reached the average consumer.

Even within a single company, a researcher may propose a scientifically groundbreaking idea to their service team colleagues and be denied implementation for various reasons. The famous Xerox PARC laboratory made numerous incredible discoveries in the 70s and 80s, but the parent company did not always use these innovations in products. As a result, for example, the windowed GUI, largely invented at PARC, was 'borrowed' and more rapidly integrated into operating systems by Apple and Microsoft. Returning to the topic of modern machine learning, one of the reasons why it’s challenging to implement ideas in services is the (already mentioned) discrepancy between 'academic' and actual real-world datasets. Additionally, bringing the idea to life could be delayed, require extensive resources, or improve only one metric at the expense of others.

The situation is mitigated by the fact that many developers and industrial ML engineers are also somewhat researchers. They attend conferences, speak the same language as academics, propose ideas, sometimes participate in creating papers (for example, in coding), or even author them themselves. If a developer is immersed in the academic process, keeps up with what’s happening in the research department — in short, if they demonstrate a reciprocal movement towards scientists, the cycle of transforming scientific ideas into new service capabilities is shortened.

## Get in touch if you need GPUs

Request access​
Contact us​

## Key services

Compute Cloud​
Managed Service for Kubernetes​
Object Storage​

Nebius team

## See also

### 

On Kubernetes significance for ML/AI engineers

K8s has become the tool of choice for machine learning teams large and small. What are its properties that have made it today’s industry standard?

November 14, 2023
7 mins to read

### 

H100 and other GPUs  — which are relevant for your ML workload?

Let’s break down the differences between NVIDIA’s top-tier GPUs and identify workloads where each GPU model performs at its best.

November 21, 2023
11 mins to read

Sign in to save this post
Sign In
