# Scaling data collection for training software engineering agents

Source: https://nebius.com/blog/posts/scaling-data-collection-for-training-swe-agents

Skip to main content

In our recent research blog post, “Leveraging training and search for better software engineering agents,” we discussed our use of search-based methods to automatically tackle software engineering tasks. Our findings suggest that applying critic-guided search methods on top of a coding agent can be highly beneficial. This holds true both for agents based on frontier LLMs and those using less powerful open-weight models.

Our action generator model, trained on the data we’re sharing via Hugging Face, achieves a score of 19.2% on the subset of 50 random instances from the SWE-bench Verified benchmark, representing a 30% relative improvement over its parent model Qwen2.5-72B-Instruct, which scored 14.8%. Further augmenting the action generator with a guided search based on a critic model, also trained on this data, we achieve 40.6% on the full SWE-bench Verified benchmark, which is state-of-the-art among agents using solely open-weight models.

Figure 1. Fine-tuning on trajectory data improves upon Qwen-2.5-72B Instruct. Bar heights indicate mean resolved rate computed by averaging over 5 runs. Error bars represent one standard deviation of the mean.

# IntroductionIntroduction

### Lack of open data for training software engineering agentsLack of open data for training software engineering agents

Large language models for code are typically trained on datasets like Stack V2¹, which consist of raw repository files, or are fine-tuned on instruction datasets that pair function descriptions with their implementations. These datasets primarily focus on code generation and lack data where the model adjusts its actions in response to environment feedback, such as error logs or the output of executed commands. Additionally, models trained on isolated files or code snippets struggle to make sense of the broader context of multi-file projects, which is crucial for handling complex changes. As a result, existing datasets lack the comprehensive context needed to effectively train automated software engineering agents.

The need for data that captures the entire chain of reasoning — including an agent’s actions, the environment’s responses and the outcomes of verifying the solution to the originally stated problem — led us to develop an infrastructure capable of collecting such data at scale. While step-by-step reasoning datasets exist for domains like mathematics², there is a notable absence of similar data for code-related tasks. This gap in available data makes it difficult to train agents capable of effective problem-solving in software development. In theory, software engineering agents can be trained using reinforcement learning (RL) instead of supervised learning. In practice, however, starting with a well-initialized policy that can occasionally correct its mistakes yields better results. Therefore, regardless of the approach, high-quality datasets for supervised learning are essential. Building such datasets for software engineering poses unique challenges, such as setting up the environments needed for agents to take actions and conducting large-scale tests to verify their correctness. This is why we created a large dataset that can be used for supervised training of agent policy, as well as for training of auxiliary models such as critics.

### Issue solving: A crucial task for software engineering agentsIssue solving: A crucial task for software engineering agents

One important real-world scenario where agents can be beneficial is resolving issues (e.g., fixing bugs) within an existing codebase. Software engineering agents can already provide valuable support by automating aspects of debugging and feature enhancement.

Software engineering agents can be tasked with various challenges, including implementing specific methods or classes within an existing project, writing documentation or reviewing code. Among these, the task of solving issues stands out for several reasons:

- 

Issues submitted to task trackers are typically described in natural language and require analysis of the entire project’s code. This involves navigating a large repository, understanding how functions interact across files or pinpointing subtle errors in complex code.

- 

Having a pull request that resolves an issue implies that, in most cases, the information from the issue and the repository state is sufficient to address the problem.

- 

The tests included in the pull request might help distinguish between solutions that solve the problem and those that do not.

While not all issues meet these three conditions, they hold true in many cases. Issue solving and bug fixing are only part of a software engineer’s responsibilities. These responsibilities also include refactoring, implementing new large subsystems, performance optimization, and more. We chose to focus on issue solving for our initial research because there is an evaluation methodology for this type of task.

# Collection of an extended dataset of SWE-bench-like problem instancesCollection of an extended dataset of SWE-bench-like problem instances

Our methodology for collecting issues is based on the methodology used to build SWE-bench benchmark³. We aim to create a richer dataset, which we call SWE-bench Extra, that builds upon the approach of collecting issue–pull request pairs while increasing the amount of data available for training.

Figure 2. A total of 6,411 instances are obtained after filtering. Improving the recall of the Execution-based Validation will further increase the number of final instances.

### Collection of pull request and issue data from Python repositoriesCollection of pull request and issue data from Python repositories

To begin, we compile a list of GitHub repositories that meet specific criteria, such as having a permissive license and containing at least 85% Python code. We collect around 640,000 pull requests linked to issues from approximately 38,000 Python repositories using our data pipelines. To ensure decontamination, we exclude repositories already included in SWE-bench, as well as their forks.

To gather detailed activity data, we utilize GitHub Archive⁴, which captures public GitHub events such as commits, forks, issues and comments. GitHub Archive’s hourly archives provide us with a rich source of information for our analysis.

Our primary interest lies in GitHub issues and pull requests. Issues contain natural language descriptions of problems or requested features, often including code snippets or error stack traces that aid in reproducing the problem. Pull requests contain code changes and merge status information.

After collecting data from GitHub Archive, we link issues with the corresponding pull requests to identify which pull requests resolve which issues. We apply the following filtering criteria to ensure quality:

- The issue must be labeled as resolved

- The pull request must be merged into the main branch

- Pull requests that contain multiple linked issues are filtered out

- The issue description must be longer than 40 characters and primarily in English

- The pull request must include tests to verify the fix, with changes beyond just adding tests

- The changes must involve between 1 and 7 files, and the patch must not exceed 300 lines of code

For filtering, we use a pipeline consisting of a set of map-reduce operations. We rely on TractoAI as our main platform for data collection, preparation and storage. The platform’s scalable support for map-reduce operations allows us to rerun the preprocessing pipeline on the entire dataset whenever we make changes. By applying the filtering criteria, we obtain approximately 110,000 instances. We also clone the necessary repositories into our TractoAI storage for further processing.

Figure 3. Annual distribution of GitHub issues. The majority of issues are recent, with 81% created in the last five years.

### Execution-based validation of collected instancesExecution-based validation of collected instances

The goal of validation is to ensure that the correct environment could be set up and that the tests introduced in the pull request helped to indicate its resolution status. We enhance the SWE-bench scripts to automate dependency installation, eliminating the need for manual setup and efficiently scaling the process.

For each instance, we establish a default setup script that applies to all instances. First, we initialize a conda environment with Python 3.8. We choose Python 3.8 for all issues, as it is widely supported in projects updated over the last five years. Next, we install the most common packages, like gcc or pytest. The list of these tools was obtained by analyzing the logs from running the initial versions of the installation script. The absence of these packages is often the cause of errors when running project tests. We use the command pip install -e. to install the project along with the core dependencies specified in setup.py. Developers often distinguish between dependencies required to run the project code and those needed for development and testing. Therefore, we add a step to search for common files like requirements-dev.txt, requirements-test.txt, etc. and install the corresponding dependencies.

To validate the instance, the changes in the pull request’s code are divided into two patches: code_patch and test_patch. We apply test_patch and perform two test runs — one before and one after applying code_patch. Using the test run logs, we select the final instances where the pull request tests fail prior to applying code_patch but pass afterward. Additionally, these test logs must not contain any ImportError or AttributeError, ensuring that no non-existent methods are being tested.

After running our scripts, we obtain 6,411 instances that pass dependency installation and test execution without any errors. To further improve the process, one could develop an agent capable of automatically configuring environments based on the specific needs of each repository. This would offer a custom setup for each instance, helping collect more data.

While automating the installation of dependencies simplifies the process, it also presents challenges. We may miss repositories that don’t properly list dependencies, those using older Python versions or those relying on development versions of packages that are later removed. Additionally, we might overlook certain types of tasks, such as repositories containing both backend and frontend code that require testing methods different from pytest.

 | Data 　　　　　　　　　　　　　　 
 | Type
 | Mean
 | p75
 | Max

 | Issue text
 | Length (words)
 | 111.5
 | 146
 | 1,294

 | Code base
 | Files (Non-test)
 | 71.71
 | 72
 | 2,264

 | 
 | Lines (Non-test)
 | 15,163.38
 | 13,777
 | 1,039,288

 | Gold patch
 | Files edited
 | 2.6
 | 3
 | 7

 | 
 | Lines edited
 | 56
 | 76
 | 300

 | Tests
 | Fail to pass
 | 10.94
 | 5
 | 4,941

 | 
 | Total
 | 58.5
 | 49
 | 7,280

Average, 75th percentile, and maximum values characterising various attributes of the collected instances. Statistics are micro-averaged without grouping by repository.

Figure 4. Bug location in issue descriptions: 32.5% of issues include a detailed natural language description of bug localization, while 26.6% of descriptions lack any information about bug localization.

### Challenges in gathering issue dataChallenges in gathering issue data

Collecting data for training software engineering agents poses numerous challenges, including:

- 

Volume of data: GitHub contains a vast number of different projects. Our dataset of repositories consists of 678,313 repos. Manually collecting data from each repository takes too much time, so we need an automated pipeline for data collection.

- 

Parallel test execution: To validate each collected instance, we need to download it, set up the environment, and run tests multiple times. There are many tests, so it’s better to run them in parallel. A single machine won’t be enough; we need a distributed solution across multiple machines. This requires an infrastructure that can run these tasks on a cluster.

- 

Stable environments for testing: Each instance requires a unique set of dependencies and configurations, which must be accurately reproduced. We use containerization technologies to save consistent environments for each instance, ensuring reproducibility during data collection.

TractoAI is instrumental in addressing these challenges. As a serverless platform, TractoAI makes it easy to process large datasets at scale without having to think about the infrastructure deployment. It allows us to efficiently run distributed tasks, while also supporting containerization to ensure stable environments for testing with consistent dependency management and reproducibility.

# Collection of a dataset of agent trajectoriesCollection of a dataset of agent trajectories

### Agent trajectories on SWE-bench Extra instancesAgent trajectories on SWE-bench Extra instances

Once we create SWE-bench Extra, we move on to capture the trajectories of the agents that solve the collected instances (available on Hugging Face). We use SWE-Agent⁵ as the software engineering agent and a fine-tuned open-weight model as the action generator. The initial agent trajectories for training the action generator are generated using the dev split of SWE-bench and instruction tuned models.

The process of trajectory collection involves the following steps:

- 

Run the agent on selected instances: We run our agent models on a set of selected instances to generate trajectories. Each trajectory captures the agent’s sequence of actions and observations, including reading the issue, modifying code and validating the changes.

- 

Save and evaluate trajectories: We save each generated trajectory along with detailed logs of the agent’s actions. We then evaluate these trajectories, including the patches generated by the model, to identify successful paths and failures.

- 

Rejection fine-tuning step: We use the RFT approach⁶, keeping only those trajectories for training where the generated patch passes the tests. These trajectories are further analyzed for errors, such as incorrect edits or failed validation attempts. Based on these evaluations, we tune our refinement process, which we explain in more detail in the next section.

- 

Action generator evaluation: We evaluate the action generators to select the best one, which we will use in the next iteration of data collection.

We repeat this process several times, gradually expanding our dataset. We start with “lite” instances — simple tasks that require modifications to only a single file and no more than three small code changes. These lite instances help us collect initial data and test basic agent capabilities. Once we have enough data to train a reasonably capable agent generator, we expand to more complex tasks that involve modifications across multiple files and larger patches.

We use two datasets to evaluate the model’s performance:

- 

The “easy-lite 50” dataset, consisting of 50 instances randomly chosen from the set of tasks solvable by SWE-Agent paired with GPT-4o. We choose this subset because it is sensitive to minor model improvements, due to the simplicity of its instances. To solve them, the bug needs to be localized, and a small code change made in one or two specific places within a single file. Therefore, small but consistent improvements in any of the solution steps — bug localization or correct file editing — will improve the score on this dataset.

- 

An unbiased random subset of SWE-bench Verified containing 50 problems, that we call “verified-50”. We validated that for the SWE-agent with gpt-4o, our results on verified-50 match the results independently reported on the full SWE-bench Verified test set.

We use various open-weight models for data collection, with later iterations predominantly utilizing the Llama-3.1-70b and Qwen-2.5-72b models fine-tuned on the previous versions of the dataset. Inference is conducted with a temperature setting between 0.3 and 1.2, and any trajectory generating processes that fail due to infrastructure issues are retried to ensure a complete dataset.

After each iteration of trajectory collection, we update the dataset and conduct a series of experiments to determine the optimal setup for training models on the current dataset. We run the majority of experiments on different data mixtures using smaller models from the same family, such as LLama-3.1-8b and Qwen-2.5-7b, to enable fast iterations. This approach allows us to test and refine hypotheses more efficiently. Once we identify the most promising mixtures, we train larger models to validate these results. The best-performing models are then used for the next cycle of data collection.

 | 
 | 
 | Issue resolved
 | Issue not resolved

 | Trajectory
 | Average steps count
 | 31.3
 | 58.4

 | 
 | Average context length (Llama 3 tokenizer)
 | 8,352.4
 | 15,241

 | Final patch
 | Files edited
 | 1.33
 | 2.17

 | 
 | Lines edited
 | 20.7
 | 61

 | Exit status rate (grouped by target)
 | Submits
 | 94.6%
 | 57.6%

 | 
 | Exit context
 | 5.31%
 | 30.4%

 | 
 | Other
 | 0.37%
 | 12%

 | Correct steps
 | At least one correct file opened
 | 83%
 | 40%

 | Total
 | 
 | 13,389
 | 66,647

### Using the data to train an action generatorUsing the data to train an action generator

Let’s look at how we use the dataset of collected trajectories to fine-tune our action generator and explore some of the nuances involved. This process has its complexities, and understanding the pitfalls is helpful in building better action generators.

After running several iterations of data bootstrapping, we analyze the quality of action generator models trained on these data and observe that simply growing the dataset without filtering is not a good strategy. The reason for that is that occasionally, even good models can make mistakes and choose actions poorly. When such models are used for data collection, these mistakes accumulate in the training data. A model trained on such data will learn to copy these mistakes, but may also introduce new ones due to its own imperfections. Repeating this data collection and model retraining process over multiple iterations can lead to a model that makes an increasing number of errors. It is therefore important to learn not to repeat mistakes, while also learning how to respond appropriately when mistakes have been made. To address this, we experiment with filtering and retain only those trajectories that improve quality in experimental runs.

To ensure that our dataset for training the action generator contains only high-quality trajectories, we apply several filtering steps:

- 

Context length and loop prevention: We remove trajectories that exceed context length limits due to looping behavior, such as repeatedly attempting an unsuccessful action without resolving the issue.

- 

Syntax errors: Trajectories containing syntax errors or actions that lead to failed steps are filtered out.

- 

Directory errors: Instances where the agent misinterprets its position in the directory structure and attempts to edit or access incorrect files are excluded.

- 

Formatting errors: Actions written with incorrect formatting that cause parsing failures are removed from the dataset.

- 

Selecting efficient trajectories: For instances with multiple successful trajectories, we retain only the 30 shortest paths, eliminating redundant or unnecessary actions.

- 

Focus on successful outcomes: We keep trajectories that end with a successful “submit” step, ensuring that only those which solve the problem without failed steps are used for training.

After analyzing the trajectories, we also consider how to derive value from negative trajectories. We decide to keep a fraction of these negative trajectories, truncating them to the steps where the agent successfully identifies the correct files to edit or reproduces the bug described in the issue. To do this for each trajectory, we apply the following heuristic: we identify the latest action by the model that opens the required file to solve the task or successfully reproduces the issue, without any syntax or formatting errors before this step. Then the trajectory is truncated up to this step. The file needed to solve the issue is taken from the final patch, and the confirmation that the issue is reproduced is determined by the presence of phrases like “We successfully reproduced the issue” in the model’s message following the action. In our experiments with the LLama-3.1-70b model, this approach shows promising results.

The filtering and refinement process allowed us to distill a large set of initial data into a smaller, more effective training dataset. This refined dataset was instrumental in helping our models learn from both their successes and mistakes, resulting in more capable software engineering agents ready for real-world challenges.

The filtering and refinement process allowed us to distill a large set of initial data into a smaller, more effective training dataset. This refined dataset was instrumental in helping our models learn from both their successes and mistakes, resulting in more capable software engineering agents ready for real-world challenges.

Figure 5. Effect of filtering: Each step of filtering led to noticeable improvements, with the “add truncated” method achieving the highest resolution rate of 60%, compared to 48% for the baseline.

We are releasing 6,411 instances obtained after the final execution-based filtering stage, as well as 80,036 trajectories collected by various models.

Issue data instances contain the following fields:

 | Field name
 | Type
 | Description

 | instance_id
 | str
 | A formatted instance identifier, usually as repo_owner__repo_name-PR-number

 | patch
 | str
 | The gold patch, the patch generated by the PR (minus test-related code), that resolved the issue

 | repo
 | str
 | The repository owner/name identifier from GitHub

 | base_commit
 | str
 | The commit hash of the repository representing the HEAD of the repository before the solution PR is applied

 | hints_text
 | str
 | Comments made on the issue prior to the creation of the solution PR’s first commit creation date

 | created_at
 | str
 | The creation date of the pull request

 | test_patch
 | str
 | A test-file patch that was contributed by the solution PR

 | problem_statement
 | str
 | The issue title and body

 | version
 | str
 | Installation version to use for running evaluation

 | environment_setup_commit
 | str
 | commit hash to use for environment setup and installation

 | FAIL_TO_PASS
 | str
 | A json list of strings that represent the set of tests resolved by the PR and tied to the issue resolution

 | PASS_TO_PASS
 | str
 | A json list of strings that represent tests that should pass before and after the PR application

 | meta
 | str
 | A json dictionary indicating whether the instance is lite, along with a list of failed lite validators if it is not

 | license
 | str
 | The type of license of the repository.

An agent’s trajectory includes the following information:

 | Field name
 | Type
 | Description

 | instance_id
 | str
 | The identifier of the instance with the issue the agent tried to solve, consisting of the repository name and issue number

 | model_name
 | str
 | The name of the model used to generate the trajectory

 | target
 | bool
 | Whether the model solved the issue in this trajectory

 | trajectory
 | str
 | A json list with the logged trajectory consisting of a list of model reasoning and actions (under the role: ai) and observations from the environment (under the role: user). The first entry is the system prompt under the system role

 | exit_status
 | str
 | The status of the agent’s completion

 | generated
 | str
 | The final patch generated by the model while modifying the project files

 | eval_logs
 | str
 | The logs of test execution to verify the final patch

# Future steps and potential improvementsFuture steps and potential improvements

We believe that our experiments will serve as a good starting point for further work. We see several directions in which our experiments can be expanded:

- 

Broaden language support: Collect more SWE-Bench-like issues in languages other than Python. This would allow our agents to learn from a wider range of examples and improve their versatility in solving software engineering problems across different technologies.

- 

Expand PR scope: Expand beyond using only PRs that solve issues by including others as well, while rethinking the verification process to ensure relevance and quality.

- 

Develop adaptive agents for environment setup: Create an adaptive agent capable of configuring development environments. This would enable smoother automation of the setup process, making it easier for agents to address issues across different codebases and configurations.

- 

Automatic assessment of tests and issue descriptions: Learn to determine, based on the issue description, tests and code changes, whether it is possible to write a solution that passes tests based solely on the issue description, e.g. the description is not underspecified and tests are not overspecified.

# ConclusionConclusion

We built a dataset of 6,411 high-quality problem instances from an initial collection of 640,000 pull requests across 38,000 repositories, aimed at training software engineering agents for real-world coding challenges. We also generated and released 80,036 agent trajectories to aid in the development of intelligent software tools. This data can be used for training action generators and critic models, and for generating new trajectories.

In our experiments, we used smaller models to test different data mixtures and larger models to validate experiments and gather new data. This process resulted in significant improvements, yielding a reliable dataset and agents that demonstrated notable performance gains. These agents outperformed existing instruct models on key benchmarks, showcasing the effectiveness of our methods.

Looking ahead, we plan to expand language support, broaden pull request selection and improve environment adaptability. These advancements will help create even more capable software engineering agents, ultimately enhancing productivity and reducing the burden on human developers.

## ContributorsIbragim Badertdinov, Maria Trofimova, Yury Anapolskiy, Sergey Abramov, Karina Zainullina, Alexander Golubev, Sergey Polezhaev, Daria Litvintseva, Simon Karasik, Filipp Fisin, Sergey Skvortsov, Maxim Nekrashevich, Anton Shevtsov, Boris Yangel＊

IB, MT, YA and SA collected the dataset of extra instances and trajectories, KZ, AG, SP, IB and MT trained the action generator and critic models. DL, SK and SP built the inference and evaluation infrastructure. FF and SS improved training and inference performance, especially for long sequences. FF supported training infrastructure. MN, AS and BY contributed to model training and infrastructure. BY led the project.

＊Correspondence to byangel@nebius.com

## Citation information
Please cite as:

 | Badertdinov et al., "Scaling data collection for training software engineering agents", Nebius blog, 2024.

BibTeX citation:

 | @article{badertdinov2024scaling,
   title={Scaling data collection for training software engineering agents},
   author={Badertdinov, Ibragim and Trofimova, Maria and Anapolskiy, Yury and Abramov, Sergey and Zainullina, Karina and Golubev, Alexander and Polezhaev, Sergey and Litvintseva, Daria and Karasik, Simon and Fisin, Filipp and Skvortsov, Sergey and Nekrashevich, Maxim and Shevtsov, Anton and Yangel, Boris},
   year={2024},
   journal={Nebius blog},
   note={}
 }

## References

- Lozhkov, Anton, et al. (2024). "Starcoder 2 and the stack v2: The next generation." arXiv preprint arXiv:2402.19173 ↵ 

- Yue, Xiang, et al. (2023). "Mammoth: Building math generalist models through hybrid instruction tuning." arXiv preprint arXiv:2309.05653 ↵ 

- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" arXiv:2310.06770 ↵ 

- Grigorik, I. (2024). GH Archive [Software]. GitHub ↵ 

- Yang, John, et al. (2024). "Swe-agent: Agent-computer interfaces enable automated software engineering." arXiv preprint arXiv:2405.15793 ↵ 

- Yuan, Zheng, et al. (2023). "Scaling relationship on learning mathematical reasoning with large language models" arXiv preprint arXiv:2308.01825 ↵ 

## Explore Nebius

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

#### See the contributors

Contents

- 

Introduction

- Lack of open data for training software engineering agents

- Issue solving: A crucial task for software engineering agents

- 

Collection of an extended dataset of SWE-bench-like problem instances

- Collection of pull request and issue data from Python repositories

- Execution-based validation of collected instances

- Challenges in gathering issue data

- 

Collection of a dataset of agent trajectories

- Agent trajectories on SWE-bench Extra instances

- Using the data to train an action generator

- 

Future steps and potential improvements

- 

Conclusion

- 

Contributors

- 

Citation information

- 

References

## See also

### 

Leveraging training and search for better software engineering agents

In this blog post, we’ll share some of our recent findings on how search can enhance agentic systems for software engineering. Specifically, we’ll demonstrate how we’ve built an SWE-agent-based system that exclusively uses open-weight LLMs and achieves a 40.6% resolved rate on SWE-bench Verified.

November 15, 2024
10 mins to read

### 

How transformers, RNNs and SSMs are more alike than you think

By uncovering surprising links between seemingly unrelated LLM architectures, a way might be paved for effective idea exchange and boosting efficiency.

August 21, 2024
10 mins to read

### 

Mixtures of Experts and scaling laws

Mixture of Experts (MoE) has become popular as an efficiency-boosting architectural component for LLMs. In this blog, we’ll explore the steps researchers have taken on the road toward the perfect mixture of experts.

August 6, 2024
8 mins to read

Sign in to save this post
Sign In
