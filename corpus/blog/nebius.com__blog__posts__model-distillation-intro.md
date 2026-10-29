# Introduction to model distillation: Efficient knowledge transfer for AI applications

Source: https://nebius.com/blog/posts/model-distillation-intro

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

# IntroductionIntroduction

Model distillation is a powerful technique in machine learning where a compact “student” model learns to replicate the behavior of a larger, more complex “teacher” model within the given task. By transferring knowledge from the teacher to the student, distillation enables lightweight models to achieve comparable performance within the task, while being dramatically faster and cheaper to deploy (and, consequently, cheaper to run inference with).

The benefits are compelling:

- 

Latency improvement: Smaller models perform much faster, which makes them ideal for real-time applications like agentic scenarios or other tasks where an immediate response is required.

- 

Cost reduction: Smaller models require less compute for inference, and hence are available at cheaper rates. Furthermore, the fine-tuned model removes the need in long, detailed prompts to ensure a specific format of the output data, which also reduces the price due to the lower consumption of tokens.

In this tutorial, we demonstrate how to perform distillation by using Nebius AI Studio, to create a grammar-correcting model. We will:

- 

Generate high-quality training data via batched LLM generation, by using the recently released Qwen3-235B-A22B.

- 

Fine-tune a Qwen3-4B non-reasoning student model by using LoRA adapters.

- 

Deploy, evaluate and compare the distilled model with a 3.5x larger model of this family, Qwen3-14B, by using the most powerful open-source LLM to date, DeepSeek-R1, as evaluator.

By leveraging Nebius AI Studio’s batched generation, fine-tuning API, optimized inference and zero-click model deployment, we streamline the entire workflow — proving that large capabilities can indeed come in small packages. Let’s dive in!

Before we start, please note three things:

First, the procedure we employ differs from traditional distillation where the student model is trained on the teacher’s internal representations — instead, we will simply train the student model on the completions of the teacher model.

Second, the goal of this blog post is not to maximize the quality of the model on the given task, but rather exhibit how to perform distillation correctly and why it matters. Hence, we will not focus on task-specific quality-optimization tricks or play around with the data. However, we will include all the best practices for distillation so that your distilled model goes beyond your expectations!

Finally, due to non-deterministic parameters recommended by Qwen3 authors to run Qwen3, your results may differ slightly from the ones you see here if you relaunch the code. But don’t worry — we made sure the quality of the fine-tuned model is guaranteed to stay within the confidence interval of the baseline model!

For convenience, we’ve provided a Jupyter notebook that contains all the code and examples from this blog post.

Let’s start with importing the necessary packages.

import os
from dotenv import load_dotenv

from typing import Sequence
from openai import Client
from datasets import load_dataset, Dataset, concatenate_datasets
from tqdm import tqdm
import pandas as pd
import json
import numpy as np
import time
import requests
import re

You can conveniently store your Nebius API key in the .env file.

The cell below loads the key, creates the OpenAI-like Client to work with Nebius AI Studio and defines necessary variables.

load_dotenv()

DATASETS_CACHE_DIR = 'cache'
BASE_URL = "https://api.studio.nebius.ai"

client = Client(
 base_url=f'{BASE_URL}/v1',
 api_key=os.getenv('NEBIUS_API_KEY')
)

In this tutorial, we want to demonstrate how to train a small model — given only a dataset of input texts — by leveraging the most powerful LLMs to generate the desired outputs.

We will take a C4-200M dataset [1] for these purposes, which is intended for GEC models pre-training. Its outputs are otherwise unsuitable for the direct fine-tuning of a GEC model because it contains many errors, for example:

- 

Input: review narrow river as if air surf …

- 

Output: air washer review boneco w200 air washer winix air washer review.

We will use its inputs and generate correct outputs by using a state-of-the-art LLM — the recently released Qwen3-235B-A22B [2]. With proper prompt tuning, we can urge the model output the data in an easy-to-reuse format so that we can create the dataset to fine-tune our target small model — Qwen3-4B [2].

Tens of thousands observations are generally enough to improve the quality of the model. Let’s take a subset of 25k observations, process it by removing too short and too long sentences (this will leave us at 22k) and split it into train and validation subsets for fine-tuning (21k and 1k).

input_dataset = load_dataset('Aktsvigun/c4_200m_25k', split='train', cache_dir=DATASETS_CACHE_DIR)
input_dataset
>>> Dataset({
 features: ['input'],
 num_rows: 25000
})

Let’s examine a random instance from the dataset.

input_dataset[2025]
>>> {'input': 'Are you dissapointed on DNF or upsng race ettiraces?'}

The C4-200M dataset is intended to contain sentences. Sentences below 3 or above 40 words are outliers, and they most likely contain some garbage inputs. Let’s filter out such input texts.

input_dataset = input_dataset.filter(lambda x: 40 > len(x['input'].split()) > 3)
input_dataset
>>> Dataset({
 features: ['input'],
 num_rows: 22114
})

# Batch inferenceBatch inference

Heads up: Running this part will cost ~USD 4.90

You can use normal synchronous generations with Qwen3-235B-A22B to generate outputs for the dataset. However, if you are not in a last-minute rush, using batch inference is recommended. The cost can be as much as 2x cheaper, and is guaranteed to finish within 24 hours. In most cases, it takes a few hours or even minutes; again, it depends on the size of the dataset.

Let’s see how to use the batched generation to annotate our input dataset.

First, we need a carefully designed prompt so that the data is generated in the desired format. The desired format here is the untouched input sentence if it is already grammatically correct; or its corrected version, if it is not.

To urge the model to follow the desired format for generation (without adding an introduction like “Here is the corrected text” or further explanations), we will leverage few-shot learning examples. We provide two example input texts in our prompt: one grammatically correct and one grammatically incorrect.

system_prompt_distillation = """
Act as an experienced English proofreader. Please check the grammar of the user's text. If the text contains errors or misprints, print the corrected text. Otherwise, print the text as it is, otherwise. Check only the grammar of the text. Don't print anything else.

Examples for few-shot learning:
Example 1 (the text contains errors):
User: In fact who let me know abut this program was him.
Assistant: In fact, he was the one who let me know about this program.

Example 2 (the text does not contain errors):
User: On the other hand, it's very efficient computationally as it only requires one forward pass through the model per example.
Assistant: On the other hand, it's very efficient computationally as it only requires one forward pass through the model per example.
""".strip()

Let’s format the dataset and save it as a .jsonl file.

!mkdir data

max_tokens = 4096

with open('data/batch_input.jsonl', 'w') as f:
 for i, inst in enumerate(input_dataset, 1):
 dict_to_write = {
 "custom_id": f"request-{i}",
 "method": "POST",
 "url": "/v1/chat/completions",
 "body": {
 "model": "Qwen/Qwen3-235B-A22B",
 "messages": [
 {"role": "system", "content": system_prompt_distillation},
 {"role": "user", "content": inst["input"]}
 ],
 "max_tokens": max_tokens
 }
 }
 json.dump(dict_to_write, f, ensure_ascii=False)
 f.write('\\n')

Next, let’s upload our input dataset to Nebius AI Studio.

batch_input_file = client.files.create(
 file=open("data/batch_input.jsonl", "rb"),
 purpose="batch"
)
batch_input_file
>>> FileObject(id='file-93628738-bba0-44cf-845b-93b68fdf5783', bytes=24630543, created_at=1746778371, filename='batch_input.jsonl', object='file', purpose='batch', status=None, expires_at=None, status_details=None)

Now that all the preliminary steps are done, use the uploaded dataset to create the batched generation job. The code below launches the batched generation.

batch_input_file_id = batch_input_file.id
batch = client.batches.create(
 input_file_id=batch_input_file_id,
 endpoint="/v1/chat/completions",
 completion_window="24h",
 metadata={
 "description": "Distillation of Qwen/Qwen3-235B-A22B for GEC"
 }
)
batch
>>> Batch(id='batch_ce821447-46a8-4a9a-ad1c-980ab0e7e7de', completion_window='24h', created_at=1746778399, endpoint='/v1/chat/completions', input_file_id='file-93628738-bba0-44cf-845b-93b68fdf5783', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=None, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'Distillation of Qwen/Qwen3-235B-A22B for GEC'}, output_file_id=None, request_counts=BatchRequestCounts(completed=None, failed=None, total=None))

It will now take some time to complete your job, and it will depend on the workload of the model. In our case, it finished within one hour.

You can periodically monitor the status of your job. When the job is completed, the status will be equal to 'done'. The cell below will update its status every minute and stop running once the job is finished.

update_num_seconds = 60
active_statuses = ["validating", "validated", "running"]
while batch.status in active_statuses:
 time.sleep(update_num_seconds)
 # Retrieve the batch state
 batch = client.batches.retrieve(batch.id)
 print("Current status:", batch.status) 
>>> Current status: running
Current status: running
...
Current status: done

Our batch has been successfully processed. Let’s save the generations to a file and examine the format in which it comes.

file_response = client.files.content(batch.output_file_id)
file_response.write_to_file('data/batch_output.jsonl')

# Display the first line from the output file

with open('data/batch_output.jsonl') as f:
 for line in f.readlines():
 output = json.loads(line)
 break
print(json.dumps(output, indent=4))
>>> {
 "id": "batch_req_557c8556-bb2a-4d3c-ab5b-e524de4276bb",
 "custom_id": "request-10521",
 "response": {
 "id": "chatcmpl-d127ae78af5f4108bd15adc21fb4dbfb",
 "choices": [
 {
 "finish_reason": "stop",
 "index": 0,
 "logprobs": null,
 "message": {
 "content": "<think>\\nOkay, let's take a look at this user's query. The user provided a sentence that needs grammar checking. The example given has some errors, so I need to carefully check each part.\\n\\nFirst, the original text is: \\"6 p.m.: of Scheduled readings of: Amanda Ricachica, Scuri Annah, Scuri Lexi, Griffin Birdsong, Emi Bergquist, Dig Reeder, Reeder Stan, Reuben J. Appelman and Winn Christian now.\\"\\n\\nStarting with \\"6 p.m.: of Scheduled readings of:...\\" The colon after 6 p.m. is correct, but \\"of Scheduled\\" seems off. It should probably be \\"Scheduled readings: Amanda...\\" without the \\"of\\" after the colon. Also, \\"of:\\" at the end of \\"readings of:\\" is incorrect. There's a colon after \\"readings,\\" so maybe the structure is \\"Scheduled readings: [list] now.\\" But \\"now\\" at the end feels out of place. Maybe \\"now\\" is part of the event name or a typo. Alternatively, the sentence might be trying to say that readings are scheduled at 6 p.m., so the structure could be adjusted for clarity.\\n\\nLooking at the names: \\"Scuri Annah, Scuri Lexi.\\" Typically, in a list, if \\"Scuri\\" is a last name, it should be \\"Annah Scuri\\" and \\"Lexi Scuri.\\" But maybe in this context, they are using the format of Title or something else. However, the original example might have intended the names as written. So unless there's a clear error, like a missing space or punctuation, I should leave the names as they are. \\n\\n\\"Dig Reeder, Reeder Stan\\" \\u2013 \\"Dig\\" could be a nickname or abbreviation. Not sure if that's correct, but unless it's a typo, it should stay. \\"Reeder Stan\\" might be \\"Stan Reeder\\" reversed, but again, without knowing the context, it's safer to assume it's intentional unless there's a grammatical error.\\n\\n\\"Reuben J. Appelman\\" \\u2013 the period after the initial \\"J\\" is correct. \\"Winn Christian now.\\" \\"Now\\" at the end seems odd. Maybe it's a typo or misplaced. The sentence ends with \\"now,\\" which doesn't fit grammatically. Perhaps it should be \\"Scheduled readings now: [list]\\" but the timing is at 6 p.m., so \\"now\\" might be redundant or misplaced.\\n\\nPutting it all together, the corrected version would adjust the structure after 6 p.m., remove the unnecessary \\"of,\\" fix the colon placement, and remove \\"now\\" at the end. So the corrected text would be: \\"6 p.m.: Scheduled readings: Amanda Ricachica, Scuri Annah, Scuri Lexi, Griffin Birdsong, Emi Bergquist, Dig Reeder, Reeder Stan, Reuben J. Appelman and Winn Christian.\\"\\n\\nWait, the original had \\"and Winn Christian now.\\" The \\"now\\" is likely a mistake. The corrected version should remove \\"now\\" unless it's part of a name, which it doesn't seem to be. Also, adding a comma before \\"and\\" in the list for proper Oxford comma usage, which is optional but often preferred in such contexts. The user's example 1 had \\"he was the one who let me know about this program,\\" so the assistant corrected the structure and removed the misplaced word. Similarly, here, removing \\"of\\" and \\"now\\" would fix the grammar issues.\\n</think>\\n\\n6 p.m.: Scheduled readings: Amanda Ricachica, Scuri Annah, Scuri Lexi, Griffin Birdsong, Emi Bergquist, Dig Reeder, Reeder Stan, Reuben J. Appelman and Winn Christian.",
 "refusal": null,
 "role": "assistant",
 "audio": null,
 "function_call": null,
 "tool_calls": [],
 "reasoning_content": null
 },
 "stop_reason": null
 }
 ],
 "created": 1746781419,
 "model": "Qwen/Qwen3-235B-A22B",
 "object": "chat.completion",
 "service_tier": null,
 "system_fingerprint": null,
 "usage": {
 "completion_tokens": 796,
 "prompt_tokens": 234,
 "total_tokens": 1030,
 "completion_tokens_details": null,
 "prompt_tokens_details": null
 },
 "prompt_logprobs": null
 },
 "error": null
}

To get a model suitable for online application, let’s query only the generations without the thinking part. Next, create a dataset that we’ll afterwards merge with the input dataset.

Even though our dataset isn’t that large, let’s create the Dataset object from the file so that at no point do we store the whole dataset in RAM — this will be a helpful example of how to deal with large datasets.

Since we want to exhibit a distillation for real-world use cases, we will only train the model on completions and discard the thinking part. This ensures the responses are generated immediately, which is generally crucial for production applications. Hence, we extract the content after the </think> tag to save only the final, corrected version.

There may be cases where the model thought for so long that it didn’t reach the final output. We will filter these cases by removing observations where the number of completion tokens coincides with the maximum tokens we used for generation (4096).

output_save_path = 'data/batch_output_processed.jsonl'
prompt_tokens = 0
completion_tokens = 0
ids_to_filter = set()

with open(output_save_path, 'w') as f_out:
 with open('data/batch_output.jsonl') as f_in:
 for line in f_in.readlines():
 output = json.loads(line)
 output_text = output['response']['choices'][0]['message']['content']
 output_without_thinking = output_text.split('</think>')[-1].strip()
 output_id = int(output['custom_id'].split('-')[1])
 # Check the generation was finished. We won't remove these instances at the moment:
 # we will remove them once we concatenate the outputs with the input dataset
 if output['response']['usage']['completion_tokens'] == max_tokens:
 ids_to_filter.add(output_id)

 json.dump({'output': output_without_thinking, 'id': output_id}, f_out, ensure_ascii=False)
 f_out.write('\\n')
 # Calculate token statistics
 prompt_tokens += output['response']['usage']['prompt_tokens']
 completion_tokens += output['response']['usage']['completion_tokens']

Let’s also calculate the price of the batched generation. We can take the price for input/output tokens of a model from the Nebius AI Studio home page. For Qwen/Qwen3-235B-A22B, it is USD 0.20 and USD 0.60 for 1M input/output tokens. However, thanks to using batched generation, it costs half the price, at USD 0.10 and USD 0.30 for 1M input/output tokens.

price = (prompt_tokens * 0.1 + completion_tokens * 0.3) / 1_000_000
print(f'Batched generation price: ${price:.1f}')
>>> Batched generation price: $4.9

output_dataset = Dataset.from_json(output_save_path, split="train")
output_dataset = output_dataset.sort('id')
output_dataset
>>> Dataset({
 features: ['output', 'id'],
 num_rows: 22114
})

Now, let’s merge our dataset containing outputs with the dataset containing inputs, remove the instance for which the generation has not been finished and check that the merge didn’t break anything.

assert len(input_dataset) == len(output_dataset)
ft_dataset = concatenate_datasets([input_dataset, output_dataset], axis=1)
# Filter out unfinished generations
ft_dataset = ft_dataset.filter(lambda x: x['id'] not in ids_to_filter)
# Remove the `id` column, which is not useful anymore
ft_dataset = ft_dataset.remove_columns('id')
ft_dataset
>>> Dataset({
 features: ['input', 'output'],
 num_rows: 22097
})

ft_dataset[42]
>>> {'input': 'I think we need both 48bit & softprin in Libdrm.',
'output': 'I think we need both 48-bit and softprin in Libdrm.'}

Our dataset for fine-tuning is created! We can now proceed to fine-tuning — which is the most exciting part for most AI developers.

# Fine-tuningFine-tuning

Heads up: Running this part will cost ~USD 7.10

First, let’s split our dataset into training and validation parts. As mentioned above, we’ll leave 21k observations for training, allocating ~5% of observations to validate the model performance.

validation_size = 1097
seed = 42

ft_dataset_split = ft_dataset.train_test_split(test_size=validation_size, seed=seed, shuffle=True)
ft_dataset_split
>>> DatasetDict({
 train: Dataset({
 features: ['input', 'output'],
 num_rows: 21000
 })
 test: Dataset({
 features: ['input', 'output'],
 num_rows: 1097
 })
})

We now need to format our subsets and store them in separate files.

While fine-tuning allows avoiding the use of a long, detailed prompt, it in turn also reduces the token consumption and accelerates the model inference; so, providing general instructions is still highly recommended. This will prevent large gradient updates in the first steps of the fine-tuning because the output will be somewhat “expected” by the model. Large gradient updates generally lead model weights away from local minima and result in a lower quality model after fine-tuning.

Furthermore, after pre-training, Qwen3 models underwent a large-scale four-phase training, and each of the phases ensured the assistant’s message starts with the thinking part (for non-thinking generations, this thinking part is empty). Consequently, similar to the system prompt, let’s include the empty thinking part into the assistant’s messages to avoid large gradients.

system_prompt_fine_tuning = "Please correct the grammar in the user's text if necessary."
empty_reasoning_prefix = """
<think>

</think>

""".lstrip()

ft_train_save_path = 'data/fine_tuning_train.jsonl'
ft_validation_save_path = 'data/fine_tuning_validation.jsonl'

with open(ft_train_save_path, 'w') as f:
 for inst in ft_dataset_split['train']:
 dict_to_write = {
 "messages": [
 {
 "role": "system",
 "content": system_prompt_fine_tuning,
 },
 {
 "role": "user",
 "content": inst["input"],
 },
 {
 "role": "assistant",
 "content": empty_reasoning_prefix + inst["output"],
 }
 ]
 }
 json.dump(dict_to_write, f, ensure_ascii=False)
 f.write('\\n')

with open(ft_validation_save_path, 'w') as f:
 for inst in ft_dataset_split['test']:
 dict_to_write = {
 "messages": [
 {
 "role": "system",
 "content": system_prompt_fine_tuning,
 },
 {
 "role": "user",
 "content": inst["input"],
 },
 {
 "role": "assistant",
 "content": empty_reasoning_prefix + inst["output"],
 }
 ]
 }
 json.dump(dict_to_write, f, ensure_ascii=False)
 f.write('\\n')

After both files are created, upload them to the service.

fine_tuning_train_file = client.files.create(
 file=open(ft_train_save_path, "rb"),
 purpose="fine-tune"
)
fine_tuning_train_file
>>> FileObject(id='file-b0b9ffde-9bb4-4985-8cb4-94a357246d53', bytes=8793623, created_at=1746788217, filename='fine_tuning_train.jsonl', object='file', purpose='fine-tune', status=None, expires_at=None, status_details=None)

fine_tuning_validation_file = client.files.create(
 file=open(ft_validation_save_path, "rb"),
 purpose="fine-tune"
)
fine_tuning_validation_file
>>> FileObject(id='file-2d9b5ccb-1166-4357-be9c-e9cd0d20a0f6', bytes=458259, created_at=1746788217, filename='fine_tuning_validation.jsonl', object='file', purpose='fine-tune', status=None, expires_at=None, status_details=None)

We are ready to launch the fine-tuning. We’ll train LoRA adapters to reduce the usage price of the model. We slightly increase the rank of the LoRA (lora_r parameter) to reduce the quality gap between the full fine-tuning and fine-tuning of LoRA adapters. We also increase the LoRA alpha value correspondingly, to keep the ratio of lora_r to lora_alpha equal to 1, as suggested in the original LoRA paper [3].

Since our inputs and outputs are pretty short, we can use the maximum available batch size (32). We will train the model for 10 epochs.

ft_job = client.fine_tuning.jobs.create(
 training_file=fine_tuning_train_file.id,
 validation_file=fine_tuning_validation_file.id,
 model="Qwen/Qwen3-4B",
 hyperparameters={
 "n_epochs": 10,
 "batch_size": 32,
 "lora": True,
 "lora_r": 16,
 "lora_alpha": 16,
 "packing": True
 },
 seed=42
)
ft_job
>>> FineTuningJob(id='ftjob-3eafe4486d0448d9b8f203342de0e79c', created_at=1746788223, error=None, fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(batch_size=32, learning_rate_multiplier=None, n_epochs=10, learning_rate=1e-05, warmup_ratio=0.0, weight_decay=0.0, lora=True, lora_r=16, lora_alpha=16, lora_dropout=0.0, packing=True, max_grad_norm=1.0), model='Qwen/Qwen3-4B', object='fine_tuning.job', organization_id='', result_files=[], seed=42, status='running', trained_tokens=0, training_file='file-b0b9ffde-9bb4-4985-8cb4-94a357246d53', validation_file='file-2d9b5ccb-1166-4357-be9c-e9cd0d20a0f6', estimated_finish=None, integrations=[], metadata=None, method=None, suffix='')

As with batched generation, this process may take some time. The loop below will update the state of the fine-tuning job every minute and stop once it is finished.

active_statuses = ["validating_files", "queued", "running"]
while ft_job.status in active_statuses:
 time.sleep(update_num_seconds)
 ft_job = client.fine_tuning.jobs.retrieve(ft_job.id)
 print("Current status:", ft_job.status)
>>> Current status: running
Current status: running
...
Current status: succeeded

Let’s examine the loss on the validation set on each epoch, so we can download the checkpoint yielding the highest quality.

ft_checkpoints = client.fine_tuning.jobs.checkpoints.list(ft_job.id).data
metrics = []
for epoch_data in ft_checkpoints:
 epoch_metrics = {}
 epoch_metrics["train_loss"] = epoch_data.metrics.train_loss
 epoch_metrics["valid_loss"] = epoch_data.metrics.valid_loss
 metrics.append(epoch_metrics)

df_metrics = pd.DataFrame(metrics)
df_metrics.style.background_gradient(cmap='Reds')
>>> 

We can see our loss on the validation set has been gradually decreasing — meaning that, most likely, we could train our adapters even further to squeeze out the best quality. Therefore, let’s save the last trained checkpoint.

save_dir = "qwen3-4b-grammar-checker"
!mkdir $save_dir

n_selected_epoch = -1
best_checkpoint = ft_checkpoints[n_selected_epoch]

for model_file_id in best_checkpoint.result_files:
 # Get the name of the file
 file_name = client.files.retrieve(model_file_id).filename.split('/')[1]
 # Retrieve the contents of the file
 file_content = client.files.content(model_file_id)
 # Save the file
 file_content.write_to_file(os.path.join(save_dir, file_name))

The price for fine-tuning a model under 20B parameters is \$0.40/1M tokens (see pricing). Let’s calculate the total fine-tuning price.

price = ft_job.trained_tokens * 0.4 / 1_000_000
print(f'Fine-tuning price: ${price:.1f}')
>>> Fine-tuning price: $7.1

# Deploy the model in Nebius AI StudioDeploy the model in Nebius AI Studio

Nebius AI Studio provides a zero-click deployment feature, which enables automatic deployment of trained LoRA adapters to the Nebius AI Studio inference platform, thus empowering seamless use of your trained model for inference *. Here’s how to do this:

*: The list of models supported for integration of fine-tuning and inference is provided at Base LoRA adapter models available for deployment.

lora_creation_request = {
 "name": "grammar-checker", # You can set whatever name you like
 "base_model": "Qwen/Qwen3-4B-fast", # Base model. Qwen3-4B is only available with the `fast` mode
 "source": f"{ft_job.id}:{best_checkpoint.id}",
 "description": "Qwen-3-4B model fine-tuned on the grammatic error correction task."
}
url = f"{BASE_URL}/v0/models"

response = requests.post(
 url,
 json=lora_creation_request,
 headers={
 "Content-Type": "application/json",
 "Authorization": f"Bearer {os.getenv('NEBIUS_API_KEY')}"
 }
)
response_json = response.json()
model_name = response_json["name"]
response_json
>>> {'name': 'Qwen/Qwen3-4B-fast-LoRa:grammar-checker-RGXZ',
'base_model': 'Qwen/Qwen3-4B-fast',
'source': 'ftjob-3eafe4486d0448d9b8f203342de0e79c:ftckpt_91e64c71-6e05-4d77-bf8d-a24f51ca7983',
'description': 'Qwen-3-4B model fine-tuned on the grammatic error correction task.',
'created_at': 1746804992,
'status': 'validating'}

We need to wait a few seconds for it to deploy.

url = f"{BASE_URL}/v0/models/{model_name}"
active_statuses = ["validating"]
update_num_seconds = 15

while response_json['status'] in active_statuses:
 time.sleep(update_num_seconds)
 response = requests.get(
 url,
 headers={
 "Content-Type": "application/json",
 "Authorization": f"Bearer {os.getenv('NEBIUS_API_KEY')}"
 }
 )
 response_json = response.json()
 print("Current status:", response_json['status'])
>>> Current status: active

Let’s test our model on an example.

Original sentence: “Nebius AI Studio is a comprehensive platform designed to simplify the integration of AI capabilities into applications.”

Modified sentence: “Nebius AI Studio is a comprehensive platform designed too simplify the integration of AI capabiltes into applcations.”

The errors introduced are highlighted in bold.

First, generate the corrected version by using our trained model, then compare it with the original sentence.

sample_text = "Nebius AI Studio is a comprehensive platform designed to simplify the integration of AI capabilities into applications."
text_with_errors = "Nebius AI Studio is comprehensive platform designed too simplify integration of AI capabiltes into applcations."
resp = client.chat.completions.create(
 model=model_name,
 messages=[
 {'role': 'system', 'content': system_prompt_fine_tuning},
 {'role': 'user', 'content': text_with_errors}
 ],
 temperature=0.7,
 top_p=0.8,
 max_tokens=40
)
model_generation = resp.choices[0].message.content.split('</think>')[-1].strip()

if sample_text == model_generation:
 print('Model generation coincides with the original text!')
else:
 print('Model generation differs from the original text:', model_generation)
>>> Model generation coincides with the original text!

We can see that the generation coincides with the original text, which means our model did its job! Let’s now evaluate the quality of our fine-tuned model and ensure it provides superior quality compared to a baseline model — Qwen3-14B — a larger model from the same family. Again, we can do this conveniently by using Nebius AI Studio.

# Evaluate the modelEvaluate the model

Heads up: Running this part will cost ~USD 3.40 (generations with the models cost ~USD 0.02). Changing the evaluation model to its non-reasoning version DeepSeek-V3 will reduce the cost of running the model to ~USD 0.50, but this can slightly decrease the reliability of the evaluation

The evaluation procedure in text generation tasks is not as straightforward as in classification tasks. This is because the task can have multiple correct outputs for the given input. For example, in our task, in the input text “The team leader which I spoke to yesterday, …”, the word “which” can be corrected to “who” or “whom, ” and both options are correct.

Therefore, the procedure of evaluation highly depends on the nature of the task. In some cases, for example, story generation, one would have to ask an LLM to verify every generated story against the input data. For other tasks, such as sentence paraphrasing, some generated paraphrases may coincide with the reference ones, removing the need to run the LLM on these coinciding cases. Still, for almost any text-generation task, some cases need to be evaluated either with a human’s or an LLM’s help. We can again leverage Nebius AI Studio to run the evaluator LLM.

We will take the test set of the JFLEG dataset [4], used for evaluation of grammatical error correction systems. Each instance is a sentence that contains four corrections from four language experts. Some corrections may coincide with the original sentence if the sentence is grammatically correct. The dataset contains spaces before the punctuation marks — we’ll remove them to have the data in a human-like format.

For our task, grammatic error correction, we can also leverage its peculiarities to simplify the evaluation and reduce the number of cases where the results depend on another LLM’s verdict.

We will use the following pipeline. After we generate corrections with the fine-tuned and baseline models, we will compare these corrections with the reference corrections. If a model generation coincides with at least one expert correction, we will consider it valid. If it doesn’t, and the model generation introduces no edits to the original text, this means an error since all the experts suggested corrections. Finally, if none of the conditions above are met, we will ask a powerful LLM to assess whether the correction suggested by the model is correct or not.

Because the baseline model is not that large (14B parameters) and it was not trained to generate data in the desired format, it can sometimes fail to follow the output format strictly. For this reason, we’ll use extended instructions with few-shot learning examples to guide it to output the results in the desired format — the system prompt we used to distill Qwen/Qwen3-235B-A22B.

As already discussed, we will use both models in non-reasoning mode to simulate their real-world application, where the result should be generated on the fly.

Let’s load the dataset.

eval_dataset = load_dataset('jhu-clsp/jfleg', cache_dir=DATASETS_CACHE_DIR)['test']
# Remove bad instances where no corrections are suggested or the sentence is empty
eval_dataset = eval_dataset.filter(lambda x: x['sentence'] != '' and not all(y == '' for y in x['corrections']))
print(eval_dataset[0])
eval_dataset
>>> {'sentence': 'New and new technology has been introduced to the society .', 'corrections': ['New technology has been introduced to society .', 'New technology has been introduced into the society .', 'Newer and newer technology has been introduced into society .', 'Newer and newer technology has been introduced to the society .']}
>>> Dataset({
 features: ['sentence', 'corrections'],
 num_rows: 747
})

Preprocess it by removing spaces before punctuation marks.

def fix_spacing(text):
 return re.sub(r'\\s+([.,:;?!])', r'\\1', text).strip()

eval_dataset = eval_dataset.map(lambda x: {"sentence": fix_spacing(x["sentence"])}, remove_columns="sentence")
eval_dataset = eval_dataset.map(lambda x: {"corrections": list(map(fix_spacing, x["corrections"]))}, remove_columns="corrections")
eval_dataset
>>> Dataset({
 features: ['sentence', 'corrections'],
 num_rows: 747
})

Now that we have the data, let’s generate results with both models. To diversify our tutorial, let’s use normal synchronous generation here. We can parallelize it to accelerate the process.

We have two choices to enable non-reasoning mode:

- 

Force the models to start generation with the empty reasoning pattern — this is what the authors of Qwen3 suggest doing.

- 

Add the “/no_think” token to the user’s message.

Since the “/no_think” token will urge the model to start the generation with the empty reasoning pattern, let’s use the first option. We’ll need to adopt two additional arguments for the completion endpoint of Nebius AI Studio: continue_final_message and add_generation_prompt. The first argument formats the chat so that the final message in the chat is open-ended, without any EOS tokens. This enables the model to continue the final message rather than starting a new one. When it is set to True, the second argument must be set to False.

from concurrent.futures import ThreadPoolExecutor, as_completed

def _call_llm(input_text: str, system_prompt: str, **call_kwargs):
 return client.chat.completions.create(
 messages=[
 {'role': 'system', 'content': system_prompt},
 {'role': 'user', 'content': input_text},
 {'role': 'assistant', 'content': empty_reasoning_prefix}
 ],
 extra_body={"continue_final_message": True, "add_generation_prompt": False},
 **call_kwargs
 ).choices[0].message.content

def generate(
 input_text: str,
 model: str = model_name,
 system_prompt: str = system_prompt_fine_tuning,
 max_tokens: int = 128, # setting to 128 as default to make sure our generation won't terminate on long sentences
 top_p: float = 0.8, # as suggested by Qwen3 authors
 temperature: float = 0.7, # as suggested by Qwen3 authors
) -> str:
 # Use try-except construction in case we encounter an error
 output = None
 while output is None:
 try:
 return _call_llm(
 input_text=input_text,
 system_prompt=system_prompt,
 model=model,
 max_tokens=max_tokens,
 top_p=top_p
 )
 except Exception as e:
 print(f'Error for input text {input_text}:\\n{e}\\nSleeping for 3 seconds and trying again...')
 time.sleep(3)
 continue

ft_model_generations = [None] * len(eval_dataset)
# Be careful with quota limits - you may need to reduce it
max_workers = 12
with ThreadPoolExecutor(max_workers=max_workers) as executor:
 futures = {executor.submit(generate, inst['sentence'], model_name, system_prompt_fine_tuning): idx for idx, inst in enumerate(eval_dataset)}
 for future in tqdm(as_completed(futures), total=len(eval_dataset)):
 idx = futures[future]
 ft_model_generations[idx] = future.result()
ft_model_generations[:2]
>>> 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 747/747 [00:38<00:00, 18.41it/s]
>>> ['New and new technology has been introduced to society.',
'One possible outcome is that an environmentally-induced reduction in motorization levels in the richer countries will outweigh any rise in motorization levels in the poorer countries.']

Let’s repeat the procedure for the baseline model. We need to change the prompt to a more detailed one and reduce the number of parallelization workers in order not to exceed the quota.

bs_model_generations = [None] * len(eval_dataset)
# Reduce the parallelization to prevent rate limit errors
max_workers = 16
with ThreadPoolExecutor(max_workers=max_workers) as executor:
 futures = {
 executor.submit(
 generate,
 inst['sentence'],
 'Qwen/Qwen3-14B',
 system_prompt_distillation,
 ): idx
 for idx, inst in enumerate(eval_dataset)
 }
 for future in tqdm(as_completed(futures), total=len(eval_dataset)):
 idx = futures[future]
 bs_model_generations[idx] = future.result()
bs_model_generations[:2]
>>> 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 747/747 [01:41<00:00, 7.23it/s]
>>> ['New and new technology has been introduced to society.',
'One possible outcome is that an environmentally-induced reduction in motorization levels in the richer countries will outweigh any rise in motorization levels in the poorer countries.']

Now, let’s determine the cases where an LLM is required to evaluate the generation of the model. As discussed, this means cases where the model generation differs from all corrections and the original sentence. If both models generated the same result in some cases, we can optimize the usage of the evaluation LLM by calling it only once, and use this result for the second model.

ft_results = {}
bs_results = {}
ft_ids_require_verification = []
bs_ids_require_verification = []
coinciding_ids = set()

for i in range(len(eval_dataset)):
 row = eval_dataset[i]
 sentence = row['sentence']
 corrections = row['corrections']
 # If generation is in corrections, it is considered valid
 if ft_model_generations[i] in corrections:
 ft_results[i] = 1
 # Else, if generation coincides with the original sentence, it is considered
 # invalid because the original sentence is not among the corrections
 # (otherwise it would meet the previous condition)
 elif ft_model_generations[i] == sentence:
 ft_results[i] = 0
 # Otherwise need to call an LLM for verification
 else:
 ft_ids_require_verification.append(i)

 # Same for the baseline model
 if bs_model_generations[i] in corrections:
 bs_results[i] = 1
 elif bs_model_generations[i] == sentence:
 bs_results[i] = 0
 # If the generation doesn't fall under the two conditions and coincides with the fine-tuned model generation,
 # we don't need to duplicate verification for the baseline model
 elif bs_model_generations[i] == ft_model_generations[i]:
 coinciding_ids.add(i)
 else:
 bs_ids_require_verification.append(i)
len(ft_ids_require_verification), len(bs_ids_require_verification)
>>> (486, 356)

Verification of generations is not a trivial task and requires some reasoning from the model. Furthermore, to avoid correlation of scores with the generations *, let’s use another powerful reasoning LLM here — DeepSeek-R1. We will use its ‘fast’ checkpoint to speed up the process.

*: Our fine-tuned model was trained on data produced by Qwen/Qwen3-235B-A22B, while the baseline model also comes from the Qwen3 family. Using Qwen/Qwen3-235B-A22B for evaluation in this scenario may lead to overrated scores since this model’s generations correlate with generations of the two models we are evaluating.

evaluation_model = 'deepseek-ai/DeepSeek-R1-fast'

system_prompt_evaluate = """
Act as an experienced grammar checker.

You will be provided with:
1. A sentece that may contain errors
2. Its 4 corrections suggested by 4 language experts (corrections may coincide with the sentence if the expert believes the sentence is grammatically correct)
3. Its correction suggested by the proofreader

Please evaluate whether the correction written by a proofreader is valid (1) or not (0). \\
The correction is considered invalid if it omits editing any of the errors or rectifies indeed gramatically correct pieces of text. \\
Otherwise, it is considered valid.

Again, please output:
- "1", if the editing suggested by the proofreader is correct
- "0", if the editing suggested by the proofreader is incorrect

Only output the number ("0" / "1") and nothing else.
""".strip()

user_prompt_evaluate_template = """
Sentence:
{sentence}

Corrections:
{corrections}

Proofreader's correction:
{generation}
""".strip()

def evaluate_text(
 row: dict[str, str | list[str]], generation: str, system_prompt: str = system_prompt_evaluate
) -> str:
 formatted_corrections = '\\n'.join(f"{i}. {correction}" for i, correction in enumerate(row['corrections']))
 user_prompt = str(user_prompt_evaluate_template).format(
 sentence=row['sentence'],
 corrections=formatted_corrections,
 generation=generation
 )
 answer_with_reasoning = client.chat.completions.create(
 model=evaluation_model,
 messages=[
 {'role': 'system', 'content': system_prompt_evaluate},
 {'role': 'user', 'content': user_prompt},
 ],
 max_tokens=4096, # to make sure the model finishes the reasoning and outputs an answer
 top_p=0.01, # to make the results as deterministic as possible
 ).choices[0].message.content
 answer = answer_with_reasoning.split('</think>')[-1].strip()
 return convert_verdict_to_number(answer)

def convert_verdict_to_number(verdict: str) -> int:
 if verdict.isdigit():
 return int(verdict)
 # To make sure we don't overrate the performance of the model, if DeepSeek-R1 outputs smth else
 # than a number, consider the editing of the model invalid
 print(f"Cannot parse the answer {verdict}. Replacing with 0.")
 return 0

def evaluate(ids_require_verification: Sequence[int], model_generations: list[str]) -> str:
 data_require_verification = eval_dataset.select(ids_require_verification)
 model_labels = [None] * len(ids_require_verification)
 max_workers = 16
 with ThreadPoolExecutor(max_workers=max_workers) as executor: # Reduce the parallelization by 8 times
 futures = {
 executor.submit(
 evaluate_text,
 data_require_verification[idx],
 generation
 ): idx
 for idx, generation in enumerate(
 [model_generations[x] for x in ids_require_verification]
 )
 }
 for future in tqdm(as_completed(futures), total=len(ids_require_verification)):
 idx = futures[future]
 model_labels[idx] = future.result()
 return np.array(model_labels)

ft_verif_labels = evaluate(ft_ids_require_verification, ft_model_generations)
ft_verif_labels[:5]
>>> 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 486/486 [24:58<00:00, 3.08s/it]
>>> array([0, 1, 0, 1, 1])

Let’s apply the same procedure to the generations of the baseline model.

bs_verif_labels = evaluate(bs_ids_require_verification, bs_model_generations)
bs_verif_labels[:5]
>>> 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 356/356 [08:33<00:00, 1.44s/it]
>>> array([0, 0, 0, 1, 0])

Let’s print the accuracy, build 95% confidence intervals and see how our fine-tuned model performs against the baseline. Since the number of observations is quite large (747) and ppp (observed accuracy) is not close to 0 or 1, we can use the normal approximation for a binomial proportion.

def print_confidence_interval(p, num_obs):
 # Critical value for 95% CI
 z = 1.96
 deviation = z * ((p * (1 - p) / num_obs) ** .5)
 left_boundary = p - deviation
 right_boundary = p + deviation
 print(f'95% confidence interval: {p:.3f} ± {deviation:.3f}\\tLeft boundary: {left_boundary:.3f}\\tRight boundary: {right_boundary:.3f}')

# Fine-tuned model
ft_verif_dict = {idx: label for idx, label in zip(ft_ids_require_verification, ft_verif_labels)}
ft_results.update(ft_verif_dict)
ft_accuracy = np.mean(list(ft_results.values()))
print('Fine-tuned model:')
print_confidence_interval(ft_accuracy, len(ft_results))

# Baseline model
bs_verif_dict = {idx: label for idx, label in zip(bs_ids_require_verification, bs_verif_labels)}
bs_results.update(bs_verif_dict)
# Coinciding ids
for idx in coinciding_ids:
 bs_results[idx] = ft_verif_dict[idx]
bs_accuracy = np.mean(list(bs_results.values()))
print('Baseline model:')
print_confidence_interval(bs_accuracy, len(bs_results))

assert len(ft_results) == len(bs_results) == len(eval_dataset)
>>> Fine-tuned model:
95% confidence interval: 0.721 ± 0.032 Left boundary: 0.689 Right boundary: 0.753
Baseline model:
95% confidence interval: 0.697 ± 0.033 Left boundary: 0.665 Right boundary: 0.730

We can see the fine-tuned model slightly outperforms the baseline model on average, with the scores staying within each other’s confidence interval. On the other side, the fine-tuned model works 2.5x times faster and reduces the token consumption due to the possibility of using shorter prompts, making the model both more efficient and effective.

# ConclusionConclusion

In this tutorial, we’ve demonstrated the power of model distillation. By leveraging Qwen3-235B-A22B as our teacher model and fine-tuning Qwen3-4B as a student, we’ve created a grammar correction model that performs on par with a larger baseline Qwen3-14B model, while being 3.5x times smaller and requiring less computational resources at inference time.

AI Studio streamlines the entire distillation workflow — from generating high-quality training data with powerful teacher models, to fine-tuning efficient student models and seamlessly deploying them for inference. The end-to-end platform makes advanced AI techniques accessible even without extensive infrastructure or expertise.

## References

- Stahlberg, F., & Kumar, S. (2021). Synthetic data generation for grammatical error correction with tagged corruption models. In Proceedings of the 16th Workshop on Innovative Use of NLP for Building Educational Applications (pp. 37–47) . Association for Computational Linguistics. https://www.aclweb.org/anthology/2021.bea-1.4 ↵ 

- Qwen Team. (2025, April 29). Qwen3: Think deeper, act faster. Qwen Blog. https://qwenlm.github.io/blog/qwen3/ ↵ 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang and Weizhu Chen. LoRA: Low-Rank Adaptation of Large Language Models.. The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022, 2022: https://openreview.net/forum?id=nZeVKeeFYf9. ↵ 

- Napoles, C., Sakaguchi, K., & Tetreault, J. (2017). JFLEG: A fluency corpus and benchmark for grammatical error correction. In Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers (pp. 229–234).Association for Computational Linguistics. arXiv:2501.12948 ↵

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Akim Tsvigun
Senior ML Solutions Architect at Nebius

Contents

- Introduction

- Batch inference

- Fine-tuning

- Deploy the model in Nebius AI Studio

- Evaluate the model

- Conclusion

## See also

### 

Beyond prompting: Fine-tuning LLMs with Nebius AI Studio

In this blog post, we’ll demonstrate how to fine-tune an LLM using Nebius AI Studio with a function-calling task as our running example. The goal isn’t to achieve state-of-the-art results but to walk you through the steps and showcase why fine-tuning matters.

March 26, 2025
13 mins to read

### 

Make AI work for you: fine-tuning launches on Nebius AI Studio

Today marks a significant step forward for AI developers and businesses: fine-tuning is now available in Nebius AI Studio. This launch transforms how you can customize leading open-source models, making them work precisely for your specific needs.

March 5, 2025
2 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
