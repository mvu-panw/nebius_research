# Reasoning critics enable better parallel search for software engineering agents

Source: https://nebius.com/blog/posts/reasoning-critics-parallel-search-for-agents

Skip to main content

# IntroIntro

In our previous blogpost, we demonstrated how simple critic models that regress Q-values can be used to improve software engineering agents. These critics can be leveraged in various forms of guided search, such as parallel or lookahead search, to dramatically enhance agent performance and reliability, turning even a mid-quality policy into a reasonably capable one.

However, regression-based critic models have important limitations. First, they operate in a single forward pass, meaning they must evaluate a full trajectory in one go. This is analogous to someone glancing at a trajectory and making a snap judgment — there’s no capacity for deep, conditional reasoning or adaptive scrutiny based on complexity.

Second, as with all regression models, they are vulnerable to adversarial examples. And when you apply search with such critics, the problem gets worse — by systematically exploring the solution space, search algorithms are far more likely to discover and prioritize these adversarial cases. This manifests in two pathologies: limited parallel search scaling (where more sampling degrades quality) and value hacking in lookahead search (where predicted q-values grow without meaningful improvements in actual outcomes).

Figure 1. An example from [1]: increasing the number of trajectories to select from can lead to quality degradation. A similar effect has been noted in [3].

Figure 2. When lookahead search is applied to an agent, the average Q-value of unsuccessful trajectories grows as solution process progresses.

One remedy is to bootstrap the critic: run search using the current critic, gather new trajectories, retrain the model on the augmented dataset, and repeat. But this loop is expensive — both computationally and in terms of iteration time.

# Reasoning criticsReasoning critics

Recent progress in applying online reinforcement learning to language models has opened up new possibilities. In particular, models trained to reason before producing an answer have been shown [5] to be more robust on out-of-distribution inputs. The reasoning step adds a structural prior: the model must justify its decision, which helps filter out nonsense.

This suggests a straightforward idea: instead of training a regression model, why not train a reasoning critic? That is, a language model trained to distinguish good trajectories from bad using chain-of-thought reasoning. It is not immediately obvious how to train such a critic to evaluate intermediate steps, but at the very least, we can teach it to score whole trajectories. Since we know the ground truth outcome of each trajectory from evaluating it, we can automatically verify an answer provided by such a critic and, therefore, can train it using reinforcement learning.

In the subsequent sections, we share our preliminary results on building reasoning trajectory critics using prompting and reinforcement learning and compare them to the regression-based approach we used in [1].

Figure 3. Classification performance comparison of different agent trajectory critics on the same set of agent runs. To plot PR curves for CoT critics, we count how many CoTs out of 10 give the correct answer and compare this number to varying thresholds. For regression critic, we simply threshold the predicted Q-value for the terminating action.

### PromptingPrompting

We started by prompting a reasoning model, deepseek-ai/DeepSeek-R1-Distill-Qwen-32B [4], with the prompt below and running it against a dataset of trajectories produced by an agent.
Prompt for CoT critics

SETTING: You are an expert in evaluating the performance of a computer agent designed to function as an autonomous programmer.
The agent operates directly in a special environment where it has access to linux terminal and some special tools.

For example, the environment provides a file editor that allows the agent to view 100 lines of a file at a time or edit specific chunks of the files.
Agent also has access to commands that make it easy to navigate the file or search for specific code.

You will be given:
- A description of the task the agent is trying to complete
- A sequence of the agent's interactions with the environment that produces a patch in the working copy that should resolve the task.

Your job is to evaluate the whole trajectory and the resulting patch and determine whether this patch is:
- GOOD: the patch resolves the issue described in the task
- BAD: the resulting patch does not resolve the issue

*IMPORTANT*: your main goal is to evaluate the choices made by the agent, do not try to solve the task yourself or fix the solution.

RESPONSE FORMAT:
Explain your reasoning and thought process inside <think> </think> tags.
After your thinking, state your final decision that should have your verdict wrapped into \boxed{}, e.g. \boxed{GOOD} or \boxed{BAD}.

*IMPORTANT*:
- Please follow the format strictly.
- Don't overestimate the agent's ability to solve the task, be critical and objective, don't always trust the agent's claims, don't be too lenient.
- Be VERY strict with your decision. Never guess, if you have a reason for doubt, your answer should be \boxed{BAD}.
It is better to be strict and be wrong than lenient and be wrong. Your predictions will be used
to pick one correct trajectory out of many generated by the agent, so precision is much more important than recall.

Here is the agent's trajectory:

{% for turn in turns %}
{% if turn["role"] == "env" %}
ENVIRONMENT>> {{ turn["text"] }}
{% elif turn["role"] == "agent" %}
AGENT>> {{ turn["text"] }}
{% endif %}
{% endfor %}

Now please evaluate given trajectory and provide your verdict.

The prompted model grasped the task and produced meaningful chains of thought. However, as can be seen in Figure 3, it turned out to be overly optimistic, yielding high recall at the expense of poor precision, which is not great for a setting where critic predictions would be used to select one correct trajectory out of many, and a single false positive is enough to ruin the performance. The critic also mostly fell within the precision-recall Pareto frontier of the regression critic.

The prompted critic’s optimism is understandable: agent’s trajectories generally look plausible, and the prompt did not convey the exhaustive set of reasons why they might nevertheless fail during evaluation. Optimism could possibly have been reduced through more extensive prompting; however, we instead decided to explore whether simply tuning this model further with reinforcement learning could help the critic better learn the nuances of what makes trajectories successful, as well as shift the prediction balance more towards precision.

### Balanced CoT critic trainingBalanced CoT critic training

We next collected a dataset of agent trajectories on problem instances from SWE-Bench extra [2] to train the CoT critic. These problem instances are different from those used in evaluation, which, as in [1], we conducted on verified-50, a random subset of 50 instances from SWE-Bench Verified. We then did RL fine-tuning starting from DeepSeek-R1-Distill-Qwen-32B with a reward of 1 if the model correctly classifies the trajectory as correct or incorrect and 0 otherwise.

Our initial attempt at RL fine-tuning failed as the model quickly converged to always predicting “BAD” regardless of its own reasoning. We discovered that the root cause was the imbalance of positive and negative trajectories in the training data (there were significantly more negatives), which led the model to quickly learn a moderately successful strategy of always predicting “BAD” and then failing to escape this local optimum.

We alleviated this issue by balancing the dataset to have an equal proportion of correct and incorrect trajectories. As illustrated in Figure 3, this attempt at RL training (CoT, balanced) resulted in a critic with a similar precision-recall profile compared to the prompted version.

### Precision-prioritizing trainingPrecision-prioritizing training

We then decided to explicitly prioritize precision over recall by introducing a reward that penalizes false positives more than false negatives. We’ve trained 2 precision-prioritizing critic models with the following reward schemes for different prediction outcomes:

 | CoT critic 　　　　　　　　　　　　　 
 | TP reward
 | TN reward
 | FP reward
 | FN reward

 | Balanced
 | 1
 | 1
 | 0
 | 0

 | Precision
 | 0.8
 | 1
 | -0.5
 | 0

 | More precision
 | 0.5
 | 1
 | -1
 | 0

As shown in Figure 3, these reward structures indeed induce a different balance between precision and recall of the resulting classifier, potentially leading to better ranking performance. One of the precision-prioritizing critics managed to achieve a better precision-recall tradeoff than the regression critic.

### Using CoT critics for rankingUsing CoT critics for ranking

We then evaluated different critics on the downstream task of selecting the correct trajectory out of many agent trajectories for the same problem. To produce the trajectories for ranking, we ran the agent 10 times on the verified-50 dataset mentioned above.

CoT critics return a binary label, so their outputs aren’t directly suitable for trajectory selection. So, to compute selection scores for CoT critics, we ran them 10 times on each trajectory and averaged the predicted scores, thus marginalizing out reasoning chains and estimating the probability of the final answer.

Figure 4: Comparison of trajectory ranking performance of different critics. Scores for CoT critics are computed by averaging predictions over 10 runs.

Figure 4 compares the performance of CoT and regression-based critics. One interesting observation is that the prompted CoT critic that has high recall and low precision has a very similar performance profile to that of the critic having high precision and low recall. This emphasizes the point that classification performance alone isn’t indicative of top-1 selection performance. A high-recall critic may yield good performance by being able to recognize positive trajectories where other critics cannot, while a high-precision critic better avoids false positives.

This is further illustrated in Figure 5, where we show score profiles that allow one critic to win over the other.

Figure 5: Score profiles of different critics. X axis corresponds to different agent trajectories for the same problem, Y axis shows the score assigned by the critic computed by averaging over 10 CoTs. Green color indicates that the corresponding trajectory was successful. In groups of 2 bars left bar represents the score given by high-precision critic, while the right bar shows the score given by high-recall critic. Top row: high-precision critic gives zero scores to every trajectory, while high-recall critic successfully identifies the correct one. Bottom row: high precision critic correctly identifies the correct trajectory, while high recall critic gives high scores to a lot of false positives.

While the performance of both critics is similar in this particular scenario, one should prefer precision-prioritizing critics in cases where mistakenly accepting an incorrect trajectory has a high cost, or when a decision can be made to allocate additional compute to re-runthe agent in cases where there is no clear winner.

Below we also demonstrate chains of thought for trajectory #9 of sphinx-doc__sphinx-8595, which formally resolved the issue and received a relatively high score from the high-recall critic, but a zero score from the high-precision critic. It can be seen that the high-recall critic tends to trust the agent, while the high-precision critic is much more cautious about the generality of the proposed solution:
Agent’s patch

diff --git a/sphinx/ext/autodoc/__init__.py b/sphinx/ext/autodoc/__init__.py
index d85d79617..955f300bf 100644
--- a/sphinx/ext/autodoc/__init__.py
+++ b/sphinx/ext/autodoc/__init__.py
@@ -700,6 +700,9 @@ class Documenter:
 attr_docs = {}

 # process members and determine which to skip
+ if self.object and hasattr(self.object, '__all__') and not self.object.__all__:
+ return []
+
 for obj in members:
 membername, member = obj
 # if isattr is True, the member is documented as an attribute

Golden patch

diff --git a/sphinx/ext/autodoc/__init__.py b/sphinx/ext/autodoc/__init__.py
--- a/sphinx/ext/autodoc/__init__.py
+++ b/sphinx/ext/autodoc/__init__.py
@@ -1074,7 +1074,7 @@ def get_module_members(self) -> Dict[str, ObjectMember]:
 def get_object_members(self, want_all: bool) -> Tuple[bool, ObjectMembers]:
 members = self.get_module_members()
 if want_all:
- if not self.__all__:
+ if self.__all__ is None:
 # for implicit module members, check __module__ to avoid
 # documenting imported objects
 return True, list(members.values())

High-precision critic chain of thought

<think>
Okay, so I need to evaluate whether the patch the agent created is good or bad for resolving the issue where an empty __all__ attribute is being ignored by autodoc. The problem is that when __all__ is empty, sphinx is still showing all the members, but it should show none.

Looking at the agent's steps, they first tried to reproduce the issue by creating a reproduce.py file with an empty __all__ and some functions. They then tried to run sphinx.ext.autodoc directly but got an error because it can't be run as a script. So they switched to using sphinx-apidoc, which is the correct tool for generating API documentation.

They created a directory, moved the file, and ran sphinx-apidoc, which generated the reproduce.rst file. The issue was that all functions were showing up despite __all__ being empty. 

Next, they looked into the sphinx code, specifically the filter_members method in the Documenter class. They proposed adding a check at the beginning of this method: if the object has an __all__ attribute and it's empty, return an empty list, which would prevent any members from being documented.

Hmm, let me think about this. The __all__ attribute is a module-level attribute that tells autodoc which members to document. If __all__ is empty, autodoc should not document any members.

The agent's approach is to modify the filter_members method to check if self.object (which is the module being documented) has __all__ and if it's empty. If so, return an empty list, thus filtering out all members.

But wait, is self.object always the module? Because Documenter is a base class, and there are ModuleDocumenter, ClassDocumenter, etc. So in the case of ModuleDocumenter, self.object would be the module. But in other documenters, like for classes, self.object might be a class, which might not have an __all__ attribute. 

So adding this check in the base Documenter's filter_members might have unintended consequences. For example, if a class (accidentally) has an __all__ attribute, even though it's not standard practice, this code would incorrectly filter its members. But classes typically don't have __all__, so maybe that's not a big issue.

Another consideration: Does this check account for the fact that __all__ could be non-empty? For example, if __all__ is ["foo"], then only foo should be included. The current code only checks for an empty __all__, but that's correct because the issue is when __all__ is empty.

But wait, the PR is about the case where __all__ is empty, so the fix should handle that. So perhaps this approach is correct.

Another thing: The code is placed right before the loop over members. If the condition is met, it returns an empty list, which would mean no members are included. But let me check the return type of filter_members. It returns a list of tuples (name, member, isattr). So returning an empty list would correctly result in no members being documented.

But I should think about how the rest of the code handles this. For example, if __all__ is present and empty, but the user has specified members in the directive, like :members: foo. Should those be included or not?

In the current PR, the problem is that when __all__ is empty, autodoc shows all members. The expected behavior is that when __all__ is empty, no members are shown. So the agent's fix seems to target that correctly.

But what about cases where __all__ is not set? Because, by default, if __all__ is not set, autodoc includes all public members. The fix shouldn't affect that case because the condition is only triggered when __all__ exists and is empty.

So, I think the logic is sound. But let me think about possible edge cases.

Edge case 1: __all__ is None instead of an empty list. But the condition is checking if it's empty, so it would only trigger if it's an empty list or perhaps another empty iterable. Wait, in the code, self.object.__all__ is checked with "not self.object.__all__". So if __all__ is None, 'not None' is False, so the condition isn't met. So that's correct because None isn't an empty list.

Edge case 2: A module without __all__ defined. The condition doesn't trigger, so autodoc proceeds as usual, including public members.

Edge case 3: A module where __all__ is set to an empty list, but the user also specifies :members: explicitly. In that case, should autodoc still include the specified members? According to the PR description, the expected behavior is that no entries are shown when __all__ is empty, regardless of the members option. Or does :members: override __all__? I'm not sure about the intended behavior in that case.

Looking at the autodoc documentation, the :members: option includes all members if no list is given. However, if __all__ is set, it should respect that. So the fix as implemented would prevent any members from being shown even if :members: is used, which may or may not be desirable.

But according to the problem description, the user expects that with __all__ empty, no members are shown, regardless of the presence of :members:. So the fix is correct in that scenario.

Another thing: the code is in the filter_members method, which is in the Documenter class. This method is called for all types of documenters. But perhaps this check should only be applied when the documenter is a ModuleDocumenter, because __all__ is a module-level attribute.

Because in the current code, the condition would trigger for any object that has an empty __all__, which might not be intended. For example, if a class somehow has an __all__ attribute, the documenter would skip all its members, which is incorrect.

So, the fix as implemented may have a bug because it's checking for self.object.__all__ without considering whether self.object is a module.

Looking back at the code, self.object is set during import_object and other methods. So for ModuleDocumenter, self.object is the module. For ClassDocumenter, it's the class. So the current code would affect any documenter that has an object with an empty __all__. That's a problem because it's not specific to modules.

To fix that, the check should be done only for modules. So perhaps the condition should be something like:

if isinstance(self, ModuleDocumenter) and hasattr(self.object, '__all__') and not self.object.__all__:
 return []

Alternatively, check if the documenter is a ModuleDocumenter.

In the current implementation, the agent didn't do that, which could cause unexpected behavior for non-module documenters.

Therefore, the patch may be incorrect because it's too broad.

Another point: The change is in the filter_members method. But perhaps the correct place to apply this is earlier in the process, such as when collecting the members, rather than in filter_members. Alternatively, maybe the condition should be applied in the ModuleDocumenter's get_object_members method.

Looking at the ModuleDocumenter, it has its own get_object_members which is called when want_all is True or based on the options. Maybe that's a better place to enforce the empty __all__ check.

If the condition is placed in the ModuleDocumenter's get_object_members, it would be more specific and avoid affecting other documenters. So the current approach is incorrect because it's in the base Documenter class.

Thus, the agent's solution may be introducing a bug by checking __all__ in all documenters, not just modules.

Another consideration: The filter_members method's responsibility is to filter members based on visibility and options. Adding a condition based on __all__ here might not be the correct approach, as __all__ is a module-level concept.

So perhaps the correct place to handle this is in the ModuleDocumenter's get_object_members method. There, when want_all is False (i.e., when __all__ is not empty but the user hasn't specified :members:), it should respect the __all__.

Wait, perhaps the problem is that autodoc doesn't respect __all__ correctly when __all__ is empty. So the change should ensure that when a module has __all__ = [], the get_object_members returns an empty list.

Looking at the code in ModuleDocumenter's get_object_members:

def get_object_members(self, want_all: bool) -> ObjectMembers:
 if want_all:
 return self.get_all_members()
 else:
 return self.get_module_members()

get_module_members() collects the members based on __all__. So perhaps the issue is that get_module_members is not correctly handling the case where __all__ is empty.

Looking at get_module_members, in sphinx/ext/autodoc/__init__.py lines 1046-1072.

def get_module_members(self) -> ObjectMembers:
 module = self.object
 members = self.get_module_all() # type: ignore # E.g., sphinx.add_argument doesn't return anything
 if members is None: # could not read __all__ automatically
 all_members = pn.get_members(module, self.exclude_members)
 # add all public members
 for name, attr in all_members:
 if (self.can_document_member(attr, name, False, module) and
 (self.options.private_members or not name.startswith('_')) and
 (self.options.special_members or not (name.startswith('__') and name.endswith('__'))) and
 not name.startswith(('_ kodoc_', '_sphix_'))):
 self._add_member(name, attr, addsynopsis=False)
 else:
 for name in members:
 if name == '__all__':
 continue
 if name in pn.get_forward_imported_members(module):
 continue
 if name in self.exclude Members:
 continue
 try:
 attr = getattr(module, name)
 except AttributeError:
 logger.warning(__('could not get attribute %s from module %s') %
 (name, module.__name__), type='autodoc')
 continue
 if not self.can_document_member(attr, name, False, module):
 continue
 self._add_member(name, attr, addsynopsis=False)
 return self.object_members

Wait, but this is getting complicated. The real issue is that when __all__ is empty, autodoc still lists all members.

So the change should be made in get_module_members, to check if __all__ is empty and then return an empty list.

Looking at get_module_members, it seems that the __all__ is read via get_module_all(), which is from the import_analyzer.

If get_module_all() returns an empty list, perhaps that causes the else clause to run, but with members = [], leading to no members being added.

But if that's already the case, why is the issue happening? Maybe the problem is that the 'want_all' parameter is set to True when __all__ is empty, causing it to fall into the 'want_all' path, which returns all members.

Alternatively, perhaps the get_module_all() function isn't properly returning an empty list when __all__ is empty.

But in the code, want_all is determined in the parent method.

Looking back, in the Documenter's get_object_members:

def get_object_members(self, want_all: bool) -> ObjectMembers:
 if want_all:
 return self.get_all_members()
 else:
 return self.get_module_members()

So, if want_all is True, it calls get_all_members(), which includes all members regardless of __all__. The want_all parameter is determined based on the presence of an :all: option, or if __all__ is present.

Wait, the want_all is determined in the Documenter as follows:

Looking at the code, want_all is passed to get_object_members. It's set when self.options.members is None and self.options.show_inheritance is not set, or based on some other condition.

But perhaps in the case where __all__ is empty, the code isn't properly handling it and falls back to want_all=True, thus including all members.

So maybe the correct fix is to ensure that in get_object_members, when want_all is False, and __all__ is empty, it returns an empty list.

Alternatively, in the ModuleDocumenter's get_object_members, we can add a condition:

if not want_all and self.get_module_all() is not None and len(self.get_module_all()) == 0:
 return ObjectMembers()

But wait, self.get_module_all() can be None if it couldn't read __all__. So perhaps the condition should be:

members = self.get_module_all()
if members is not None and len(members) == 0:
 return ObjectMembers()

But I'm not sure.

Alternatively, perhaps the problem is that the code in get_module_members doesn't correctly handle the case where __all__ is empty, thus leading to members being all public ones.

In that case, adding a check in get_module_members would be more appropriate.

Given all that, the agent's approach of adding the condition in the base Documenter's filter_members method is flawed because it's not specific to modules, and the correct place to handle __all__ is within the ModuleDocumenter's logic.

Therefore, the patch is incorrect because it makes the assumption that any object with an empty __all__ should have its members filtered out, which isn't the case for non-module objects. Also, the fix doesn't address the root cause correctly, which is in how __all__ is handled during member collection in the ModuleDocumenter.

Thus, the patch may introduce unintended side effects and doesn't properly solve the issue in the correct place.
</think>

\boxed{BAD}

High-recall critic chain of thought

<think>
Okay, I need to evaluate the agent's solution to the problem where an empty `__all__` attribute is not being ignored by autodoc, causing all members to be documented. The goal is to determine if the patch the agent created is GOOD or BAD.

First, I'll look at the task description again. The user provided a scenario where a module has an empty `__all__` list, but all functions are still being documented. The expected behavior is that no members should be shown when `__all__` is empty.

The agent's approach was to modify the `filter_members` method in `sphinx/ext/autodoc/__init__.py`. The change they made checks if the object has an `__all__` attribute and if it's empty, returning an empty list immediately, which should prevent any members from being included.

I need to assess whether this change actually addresses the problem.

Looking at the code, the agent added a condition early in the `filter_members` method. If the object has `__all__` and it's empty, the method returns an empty list. That should stop any members from being processed further, which aligns with the desired behavior.

But wait, how does this affect other cases where `__all__` is not empty? If `__all__` has elements, the original logic should proceed as usual, including only those members. That seems correct.

I should also consider edge cases. What if `__all__` is not present? The condition `hasattr(self.object, '__all__')` ensures that only modules with `__all__` are checked. So modules without `__all__` are unaffected, which is correct.

Another consideration: the `filter_members` method is part of the Documenter class, which is used for both modules and classes. The change should be applied in a way that doesn't affect classes, which don't typically use `__all__` in the same way. But the check is on `self.object`, which for a module would be the module itself. For classes, `__all__` isn't standard, but the check is still safe because `hasattr` would return False for classes without `__all__`.

I should also think about how autodoc handles other cases, like when `__all__` is `None` or contains non-strings. But the agent's patch only handles the case when `__all__` is an empty list, which is the specific issue reported.

When the agent ran their tests, they observed that after the change, the `reproduce.rst` file showed no members, confirming the fix. However, in the environment logs, the `reproduce.rst` still had the automodule directive, but whether it shows members depends on the generated output, which the agent said was fixed.

Wait, in the environment log after running `cat reproduce.rst`, the output remained the same as before. That's confusing. Did the change actually take effect? Maybe the test wasn't thorough enough. It's possible that the change in `filter_members` didn't fully propagate through, or perhaps the documentation generation still includes members for other reasons.

Alternatively, maybe the agent's test didn't correctly reflect the change because the autodoc configuration or caching was causing the issue. It's also possible that the patch didn't cover all necessary paths where `__all__` is checked.

Another angle: the Documenter's `filter_members` is called during the member collection process. If `__all__` is empty, members should be filtered out before being added to the documentation. So in the test script, after the change, the generated `reproduce.rst` should have no .. autofunction directives for foo, bar, and baz.

But in the logs, after rerunning, the output still showed the module and the automodule directive, but it's unclear if the members were actually listed. The agent claims the fix worked, but without seeing the exact output, it's hard to be certain.

Also, the agent was supposed to clean up by removing `output.rst` but encountered an error, possibly because it didn't exist. That might be a minor issue but shows they followed through on their steps.

Overall, the change the agent made seems logically correct. By adding a check in `filter_members` for an empty `__all__`, they prevent any members from being included. The approach targets the correct part of the code and the logic seems sound.

But since the environment logs don't explicitly show that the members were excluded, I'm left with some doubt. However, trusting the agent's test result where they observed the fix, I think the patch is GOOD.
</think>

The agent addressed the issue by modifying the `filter_members` method to check for an empty `__all__` attribute, correctly preventing members from being documented. The approach is logical and should resolve the problem as described. 

\boxed{GOOD}

It is also worth noting that both the high-recall and high-precision critics perform notably better than the regression-based critic when ranking a large number of runs, despite being within the precision-recall Pareto frontier of the latter.

Finally, the CoT critic RL fine-tuned with the right balance of precision and recall outperforms the rest. The critic trained without prioritizing precision over recall (balanced) performs the worst, suffering from too many false positives, while not having high enough recall to compensate.

### CoT critic prediction quality scalingCoT critic prediction quality scaling

Since we compute scores by sampling CoT critic reasoning multiple times, we have also studied how the trajectory selection performance scales as the number of samples grows. Increasing the number of samples seems to improve selection quality monotonically, saturating at around 20 samples, thus providing yet another axis for scaling test-time computation.

Figure 6. Precision-prioritizing critic performance when increasing the number of CoT samples. Different lines are plotted by sampling a single random subset of the corresponding size from all CoTs available for each problem.

### Confident mistake analysisConfident mistake analysis

We have also manually analyzed cases where a precision-prioritizing critic gives a high-confidence correctness score to a trajectory that turns out to be incorrect. In all analyzed cases, we found the critic’s mistake to be somewhat justifiable.

For example, in one case where the agent was tasked with changing the signature of a certain function (django__django-1510), the agent changed the signature and successfully tested the changes using its own test script, but failed to notice that this function had a wrapper in a different file whose signature should have also been changed. And this wrapper function was actually called in tests used to verify the correctness of the fix. The trajectory itself had no information about the second function because the agent had never searched for it, leaving the critic no information to work with. The only way for the critic to handle this case correctly would have been to be extra cautious and to consider the trajectory incorrect simply because the agent didn’t perform a repository-wide search for other places that potentially needed a signature change.

However, for the version of agent we did the experiment on, such a strategy would have likely resulted in very low recall, making it suboptimal for RL to pick it up.
An example CoT for django__django-1510 with reasoning leading to an incorrect conclusion

<think>
Okay, I need to evaluate whether the patch the agent created is good or bad for making the element_id argument in json_script optional. Let me go through the process step by step.

First, I'll look at the original function. The json_script function takes two parameters: value and element_id. The goal is to make element_id optional, so the user can call it without providing an element_id, which is useful when they don't need an id, like inside a template.

The agent's approach was to modify the function signature by adding a default value of None to element_id. Then, they added a conditional check: if element_id exists (i.e., is not None), it includes the id attribute in the script tag; otherwise, it omits the id attribute.

Looking at the code, the function now looks like this:

def json_script(value, element_id=None):
 # ... some code ...
 if element_id:
 return format_html(... with id ...)
 else:
 return format_html(... without id ...)

This seems correct because when element_id is None, the else clause is triggered, and the script tag doesn't have the id attribute.

But wait, I should think about potential issues. One thing is how the function handles the element_id being an empty string. If someone passes an empty string, the condition (if element_id) would evaluate to False, which would exclude the id attribute. But that's probably not intended because an empty string is a valid value for an id attribute (though not common). So if element_id is an empty string, it would be treated as None, which might not be desired. However, in the context of the HTML spec, an empty id is allowed but generally not useful. So maybe this isn't a big issue.

Another consideration is backward compatibility. Before, element_id was a required argument. Now, it's optional. So existing code that was passing element_id as None would have caused an error before, but after this change, it would omit the id attribute, which is better. Users who were passing None would now have it work as expected.

Looking at how the function is used, the return value is a script tag. Without the id, it's just <script type="application/json">...</script>. That seems fine because the use case mentioned was embedding inside a template where the id isn't needed.

I should also check the format_html function. The format_html function is used with placeholders, and when element_id is None, it's handled by not including the id in the tag. The variables passed are element_id and mark_safe(json_str), which should handle any escaping needed.

Testing the scenario: if we call json_script(value) without providing element_id, it should return the script without the id. That's exactly what the code does.

Another edge case: what if element_id is an empty string? As discussed, it would be treated as False, so the id would be omitted. But this might be an oversight. If a user intentionally passes an empty string, they might expect the script tag to have id="", but that's probably not a common use case. The PR description didn't mention handling such cases, so perhaps it's acceptable.

Overall, the change seems to handle the case where element_id is None correctly by omitting the id attribute. It makes the argument optional as required. However, considering that the original function didn't have a default, adding one and handling it appropriately is the correct approach.

Wait, I should think about other possibilities. For example, someone might pass element_id as an empty string, but the current code treats it as if it's None. However, the user's PR only asked for making the argument optional, not handling all possible edge cases for the id value. Since the test cases were already updated, and the original function didn't have any constraints on the id being non-empty beyond its presence, the change should meet the requirements.

So, the code modification appears to correctly make element_id optional and omits the id attribute when it's None or not provided. It seems to handle the main use case without introducing obvious issues. Thus, the patch is good.
</think>

\boxed{GOOD}

The rest of the cases we analyzed followed a similar structure: the agent made a fix and successfully tested it, but either the change was a little bit too specific or the agent didn’t discover some important context.

### OOD robustnessOOD robustness

To assess whether chain-of-thought critics are more robust to OOD data, we compared them with the regression critic on two other sets of runs, which were produced with an agent scaffolding significantly different from the one all critics have been trained on, both in terms of available tools and the format of environment responses. These runs were also made using policies different from the one used to produce training data for critics. To our surprise, in both cases, the regression critic still demonstrated non-trivial selection performance. However, precision-prioritizing critics achieved better performance compared to both the trained regression critic and the prompted reasoning model.

Figure 7. Critic performance on an OOD scaffolding against a less capable OOD policy. RL fine-tuned precision-prioritizing critics outperform the rest.

Figure 8. Critic performance on an OOD scaffolding against a more capable OOD policy. RL fine-tuned precision-prioritizing critics slightly outperform the rest. Prompted critic does not outperform random baseline.

### Training detailsTraining details

We ran RL fine-tuning starting from DeepSeek-R1-Distill-Qwen-32B. We used GRPO-like fully on-policy training with a batch size of 256, 32 groups, and 8 completions per group. We computed advantage by subtracting the mean reward within each group. However, instead of applying advantage normalization within each group as is done in GRPO, we applied normalization over the whole batch after subtracting the mean. This strategy does not seem to cause performance degradation compared to GRPO, while being more general as it avoids amplifying noise when reward differences within a group are small. We trained models for 300 steps with 32 warm-up steps followed by a constant learning rate of 1e-6. We also added KL regularization to the initial model with a weight of 1e-3 to the loss, as some of our initial runs encountered instabilities without it.

# Conclusion and future workConclusion and future work

In this blogpost we’ve demonstrated how chain-of-thought agent critics can be a viable alternative to models that directly regress the prediction in a single forward pass. Such critics bring the benefits of providing more interpretable decisions (at least to the extent of chain-of-thought faithfulness [8]) and seem to generalize better to OOD models and scaffoldings, allowing for less frequent retraining in practical scenarios. In terms of computational requirements, chain-of-thought critics are comparable to regression-based models, as the majority of compute is spent on encoding the trajectory, with average chain-of-thought length in our experiments being around 600 tokens.

We’ve also demonstrated that when such critics are used to select one correct trajectory out of many, prompting alone might not be enough, and precision-prioritizing training might be necessary to teach the critic to avoid false positives that can easily ruin the selection process. Such training can be easily achieved using RL fine-tuning if a dataset of trajectories is available.

Interestingly, even chain-of-thought critics aren’t able to fully close the gap between critic and oracle performance. Our manual analysis has shown that remaining cases cannot be easily fixed as the trajectories simply lack the information necessary for the critic to make the right decision. Methods that perform execution-based validation of the proposed patches [7] or encouraging the agent itself to perform such validation might be necessary to make any further progress.

One other interesting question is whether RL-tuned models can also be a viable alternative for process supervision. Training a critic for such a task is not straightforward because, unlike in outcome supervision, the ground truth of what constitutes a good action isn’t readily available. However, one might try to estimate action advantages using Monte Carlo estimation (as proposed, for instance, in [6]), and then teach the critic to pick actions with the highest advantage.

Overall, we see RL-trained CoT critics as a fruitful direction for further scaling test-time computation productively.

## ContributorsBoris Yangel＊, Sergey Polezhaev

BY designed and implemented the RL training infrastructure and conducted the experiments described in the post, SP performed some of the evaluations.

＊Correspondence to byangel@nebius.com

## Citation information
Please cite as:

 | Yangel and Polezhaev, "Reasoning critics enable better parallel search for software engineering agents", Nebius blog, 2025.

BibTeX citation:

 | @article{yangel2025reasoningcritics,
   title={Reasoning critics enable better parallel search for software engineering agents},
   author={Yangel, Boris and Polezhaev, Sergey},
   year={2025},
   journal={Nebius blog},
   note={}
 }

## References

- Golubev, A., Polezhaev, S., Zainullina, K., Trofimova, M., Badertdinov, I., Anapolskiy, Y., Litvintseva, D., Karasik, S., Fisin, F., Skvortsov, S., Nekrashevich, M., Shevtsov, A., Abramov, S., & Yangel, B. (2024). Leveraging training and search for better software engineering agents. Nebius blog. nebius.com/blog/posts/training-and-search-for-software-engineering-agents ↵ 

- Badertdinov, I., Trofimova, M., Anapolskiy, Y., Abramov, S., Zainullina, K., Golubev, A., Polezhaev, S., Litvintseva, D., Karasik, S., Fisin, F., Skvortsov, S., Nekrashevich, M., Shevtsov, A., & Yangel, B. (2024). Scaling Data Collection for Training Software Engineering Agents. Nebius blog. nebius.com/blog/posts/scaling-data-collection-for-training-swe-agents ↵ 

- Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., & Schulman, J. (2021). Training Verifiers to Solve Math Word Problems. arXiv preprint: arXiv:2110.14168. ↵ 

- DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948 ↵ 

- Wang, H., Qin, Z., Shen, L., Wang, X., Cheng, M., & Tao, D. (2025). Leveraging Reasoning with Guidelines to Elicit and Utilize Knowledge for Enhancing Safety Alignment. arXiv:2502.04040 ↵ 

- Guan, X., Zhang, L. L., Liu, Y., Shang, N., Sun, Y., Zhu, Y., Yang, F., & Yang, M. (2025). rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking. arXiv preprint: arXiv:2501.04519 ↵ 

- Jain, N., Singh, J., Shetty, M., Zheng, L., Sen, K., & Stoica, I. (2024). R2E-Gym: Procedural Environment Generation and Hybrid Verifiers for Scaling Open-Weights SWE Agents. R2E-Gym Project. r2e-gym.github.io ↵

- Chen, Y., Benton, J., Radhakrishnan, A., Uesato, J., Denison, C., Schulman, J., Somani, A., Hase, P., Wagner, M., Roger, F., Mikulik, V., Bowman, S., Leike, J., Kaplan, J., & Perez, E. (2025). Reasoning Models Don’t Always Say What They Think. Anthropic. assets.anthropic.com/m/71876fabef0f0ed4 ↵ 

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

#### See the contributors

Contents

- 

Intro

- 

Reasoning critics

- Prompting

- Balanced CoT critic training

- Precision-prioritizing training

- Using CoT critics for ranking

- CoT critic prediction quality scaling

- Confident mistake analysis

- OOD robustness

- Training details

- 

Conclusion and future work

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

Scaling data collection for training software engineering agents

In this follow-up to our previous research blog post, we focus on the data collection process used to train our action generator and critic models. We’re also releasing two datasets on Hugging Face: nebius/SWE-bench-extra, containing 6,411 Issue/Pull-Request pairs, and nebius/SWE-agent-trajectories, featuring 80,036 software engineering agent trajectories, where an agent attempts to solve these issues.

December 20, 2024
9 mins to read

### 

Kvax: Fast and easy-to-use FlashAttention implementation for JAX

Today, we’re open-sourcing Kvax, our FlashAttention implementation based on JAX. Designed for efficient training with long sequences, Kvax supports context parallelism and optimized computation of document masks. It outperforms many other FlashAttention implementations in long-context training with dense packing, achieving state-of-the-art performance.

February 27, 2025
13 mins to read

Sign in to save this post
Sign In
