# Beyond prompting: Fine-Tuning LLMs with Nebius AI Studio

Source: https://nebius.com/blog/posts/fine-tuning-llms-with-nebius-ai-studio

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

LLMs like DeepSeek-V3 and Qwen-2.5-72B are quite versatile but can sometimes struggle with domain-specific or highly structured tasks. That’s where fine-tuning comes in: you can adjust a general model to better handle specialized use cases.

In this blog post, we’ll demonstrate how to fine-tune an LLM using Nebius AI Studio with a function-calling task as our running example. The goal isn’t to achieve state-of-the-art results but to walk you through the steps and showcase why fine-tuning matters.

You’ll learn to launch your fine-tuning task with Nebius AI Studio from dataset preparation to final evaluation. By the end of this post, you will be ready to tailor an LLM to your needs and reap the benefits of customized performance for real-world applications.

For convenience, we’ve provided a Jupyter notebook that contains all the code and examples from this blog post.

Let’s start by importing the necessary packages.

import os
from dotenv import load_dotenv

from typing import Sequence
from openai import Client
from datasets import load_dataset, Dataset, concatenate_datasets
from tqdm import tqdm
import pandas as pd
import json
import time
import numpy as np
import requests

To run the code in this blog post using Nebius AI Studio, you will need to create and set up an API key. It is advisable that you store it as an environmental variable NEBIUS_API_KEY in the .env file.

You can load it by using the load_dotenv() function as demonstrated in the cell below. The cell also creates an OpenAI-like Client to work with AI Studio. Lastly, it defines the directory to store the dataset.

load_dotenv()

BASE_URL = "https://api.studio.nebius.ai"
CACHE_DIR = "cache"

client = Client(
 base_url=BASE_URL + "/v1",
 api_key=os.getenv("NEBIUS_API_KEY")
)

# Data preprocessingData preprocessing

We’ll fine-tune the LLM on the ToolACE dataset [1], a function-calling dataset, which contains 26.5K accurately verified function-calling dialogs. Each sample consists of a structured conversation in JSON format, including a user query, an assistant response, tool invocation details, and simulated API execution results.

To reduce fine-tuning costs, we will use a random subset of 10k instances for training and 1k for validation.

dataset = dataset['train'].train_test_split(train_size=11_000, shuffle=True, seed=42)['train']
dataset

>>> Dataset({
 features: ['system', 'conversations'],
 num_rows: 11000
})

Let’s examine a random instance from the dataset. We have a list of possible tools, a user’s query, and a desired answer.

dataset[42]

>>> {'system': 'You are an expert in composing functions. You are given a question and a set of possible functions. \nBased on the question, you will need to make one or more function/tool calls to achieve the purpose. \nIf none of the function can be used, point it out. If the given question lacks the parameters required by the function,\nalso point it out.\nThe current time is 2020-12-10 16:55:41.Here is a list of functions in JSON format that you can invoke:\n[{"name": "market/list-indices", "description": "Retrieve a list of available stock market indices from CNBC", "parameters": {"type": "dict", "properties": {"region": {"description": "Filter indices by region (e.g., US, Europe, Asia)", "type": "string"}, "exchange": {"description": "Filter indices by exchange (e.g., NYSE, NASDAQ, LSE)", "type": "string"}}, "required": ["region"]}, "required": null}, {"name": "Balance", "description": "Provides annual or quarterly balance sheet statements of a single stock company.", "parameters": {"type": "dict", "properties": {"symbol": {"description": "The stock symbol of the company", "type": "string"}, "period": {"description": "The period for which the balance sheet is required (annual or quarterly)", "type": "string"}}, "required": ["symbol", "period"]}, "required": null}, {"name": "Get Competitors", "description": "Retrieve a list of competitors for a given stock performance ID.", "parameters": {"type": "dict", "properties": {"performanceId": {"description": "The ID of the stock performance to retrieve competitors for.", "type": "string", "default": "0P0000OQN8"}}, "required": ["performanceId"]}, "required": null}, {"name": "Nonfarm Payrolls Not Adjusted API", "description": "Retrieves the monthly not seasonally adjusted nonfarm payrolls data from the United States Economic Indicators tool.", "parameters": {"type": "dict", "properties": {"year": {"description": "The year for which to retrieve the nonfarm payrolls data.", "type": "int"}, "month": {"description": "The month for which to retrieve the nonfarm payrolls data.", "type": "int"}}, "required": ["year", "month"]}, "required": null}, {"name": "Medium News API", "description": "Retrieve official news from Medium related to finance.", "parameters": {"type": "dict", "properties": {"category": {"description": "Filter news by category (e.g., stocks, bonds, etc.)", "type": "string"}, "string_range": {"description": "Specify the string range for which to retrieve news (e.g., last 24 hours, last week, etc.)", "type": "string"}}, "required": ["category"]}, "required": null}, {"name": "stock/get-detail", "description": "Retrieve detailed information about a specific stock, market, or index.", "parameters": {"type": "dict", "properties": {"PerformanceId": {"description": "The unique identifier of the stock, market, or index.", "type": "string", "default": "0P0000OQN8"}}, "required": ["PerformanceId"]}, "required": null}]. \nShould you decide to return the function call(s). \nPut it in the format of [func1(params_name=params_value, params_name2=params_value2...), func2(params)]\n\nNO other text MUST be included. \n',
 'conversations': [{'from': 'user',
 'value': 'Could you please provide the balance sheets for Apple for the last quarter, and also for Microsoft and Tesla for the annual period of last year?'},
 {'from': 'assistant',
 'value': '[Balance(symbol="AAPL", period="quarterly"), Balance(symbol="MSFT", period="annual"), Balance(symbol="TSLA", period="annual")]'}]}

The next step is to prepare our dataset for fine-tuning. First, we should split our dataset into training and validation parts.

dataset_split = dataset.train_test_split(test_size=1_000, seed=42, shuffle=True)

Then we need to format our subsets and store them into separate files.

Fine-tuning is particularly useful to avoid long and detailed prompts, reducing token consumption and accelerating model inference. However, providing general instructions is still highly recommended. This will mitigate the “gradient shock” when starting fine-tuning since the output will be somewhat “expected” by the model and will likely help to yield higher model quality. Hence, we will preserve the task description contained in the system prompts.

with open('fine_tuning_train.jsonl', 'w') as f:
 for inst in dataset_split['train']:
 dict_to_write = {
 "messages": [
 {
 "role": "system",
 "content": inst["system"],
 }
 ] + [
 {"role": x["from"], "content": x["value"]}
 for x in inst["conversations"]
 ]
 }
 json.dump(dict_to_write, f, ensure_ascii=False)
 f.write('\n')

with open('fine_tuning_validation.jsonl', 'w') as f:
 for inst in dataset_split['test']:
 dict_to_write = {
 "messages": [
 {
 "role": "system",
 "content": inst["system"],
 }
 ] + [
 {"role": x["from"], "content": x["value"]}
 for x in inst["conversations"]
 ]
 }
 json.dump(dict_to_write, f, ensure_ascii=False)
 f.write('\n')

After both files are created, upload them to the service.

fine_tuning_train_file = client.files.create(
 file=open("fine_tuning_train.jsonl", "rb"),
 purpose="fine-tune"
)
fine_tuning_train_file

>>> FileObject(id='file-6b971a65-a89b-4916-b144-6b3715a7919b', bytes=32200356, created_at=1741093528, filename='fine_tuning_train.jsonl', object='file', purpose='fine-tune', status=None, status_details=None)

# Fine-tuningFine-tuning

Heads up: Running this part will cost ~$9. You can minimize the amount by reducing the train dataset size to 1000, for example. You will still see the benefits of a fine-tuned model.

We are ready to launch the fine-tuning! We’ll use the 'Instruct' version of Llama-3.1-8B [2] because the task of function-calling is not that trivial and may require some “internal consideration” by the model, which the 'Instruct' version is slightly better at. Still, the question of whether to use the 'base' or 'instruct' models can often only be answered experimentally.

We’ll start by training LoRA adapters to reduce the model’s usage price. By slightly increasing the LoRA rank (lora_r parameter), we’ll reduce the quality gap between full fine-tuning and fine-tuning of LoRA adapters. We also increase the LoRA alpha value correspondingly to keep the ratio of lora_r to lora_alpha equal to 1, as suggested in the original LoRA paper [3].

Since our inputs and outputs are not that long, we can use the maximum available batch size (32). To reduce the costs, we’ll train our model for only 3 epochs.

fine_tuning_validation_file = client.files.create(
 file=open("fine_tuning_validation.jsonl", "rb"),
 purpose="fine-tune"
)

ft_job = client.fine_tuning.jobs.create(
 training_file=fine_tuning_train_file.id,
 validation_file=fine_tuning_validation_file.id,
 model="meta-llama/Llama-3.1-8B-Instruct",
 hyperparameters={
 "n_epochs": 3,
 "batch_size": 32,
 "lora": True,
 "lora_r": 16,
 "lora_alpha": 16,
 },
 seed=42
)
ft_job

>>> FineTuningJob(id='ftjob-a738c495caa04458943d816480a8d7b4', created_at=1741123457, error=None, fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(batch_size=32, learning_rate_multiplier=None, n_epochs=3, learning_rate=1e-05, warmup_ratio=0.0, weight_decay=0.0, lora=True, lora_r=16, lora_alpha=16, lora_dropout=0.0, packing=True, max_grad_norm=1.0), model='meta-llama/Llama-3.1-8B-Instruct', object='fine_tuning.job', organization_id='', result_files=[], seed=42, status='running', trained_tokens=0, training_file='file-dce61a3d-1cc7-45a4-9b5a-cc9ee506fd26', validation_file='file-6be93d68-817b-4948-a73d-9c4d36533e16', estimated_finish=None, integrations=[], method=None, suffix='')

This process may take some time. The loop below will update the state of the fine-tuning job every 15 seconds. The value succeeded will usher in its completion.

active_statuses = ["validating_files", "queued", "running"]
while ft_job.status in active_statuses:
 time.sleep(15)
 ft_job = client.fine_tuning.jobs.retrieve(ft_job.id)
 print("Current status:", ft_job.status)

>>> Current status: succeeded

ft_checkpoints = client.fine_tuning.jobs.checkpoints.list(ft_job.id).data
metrics = []
for epoch_data in ft_checkpoints:
 epoch_metrics = {}
 epoch_metrics["train_loss"] = epoch_data.metrics.train_loss
 epoch_metrics["valid_loss"] = epoch_data.metrics.valid_loss
 metrics.append(epoch_metrics)

df_metrics = pd.DataFrame(metrics)
df_metrics.style.background_gradient(cmap='Reds')

 | 
 | train_loss
 | valid_loss

 | 0
 | 0.340166\color{red}{0.340166}0.340166
 | 0.414448\color{purple}{0.414448}0.414448

 | 1
 | 0.354320\color{purple}{0.354320}0.354320
 | 0.399534\color{pink}{0.399534}0.399534

 | 2
 | 0.299520\color{black}{0.299520}0.299520
 | 0.395712\color{black}{0.395712}0.395712

We can see our loss on the validation set has been gradually decreasing, meaning that, most likely, we could train our adapters even further to improve quality. Let’s save the last trained checkpoint.

save_dir = "llama-3.1-8b-tool"
!mkdir $save_dir

n_selected_epoch = 2 # Counting from 0
best_checkpoint = ft_checkpoints[n_selected_epoch]

for model_file_id in best_checkpoint.result_files:
 # Get the name of the file
 file_name = client.files.retrieve(model_file_id).filename.split('/')[1]
 # Retrieve the contents of the file
 file_content = client.files.content(model_file_id)
 # Save the file
 file_content.write_to_file(os.path.join(save_dir, file_name))

# Deploy the modelDeploy the model

Nebius AI Studio provides an API to automatically deploy your LoRA adapters to the AI Studio inference platform, enabling seamless integration and use of your trained model for inference. Here is how to do this:

lora_creation_request = {
 "name": "tool-calling", # You can set whatever name you like
 "base_model": "meta-llama/Meta-Llama-3.1-8B-Instruct", # Base model. You can also use the `-fast` version, which is faster and slighly more expensive
 "source": f"{ft_job.id}:{best_checkpoint.id}",
 "description": "Llama-3.1-8B-Instuct model fine-tuned on the tool calling dataset."
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
response.text

>>> '{"name":"tool-calling","base_model":"meta-llama/Meta-Llama-3.1-8B-Instruct","file_id":"ftjob-a738c495caa04458943d816480a8d7b4:ftckpt_ba1680ef-f0e5-4721-b5ef-5a5a9ae630eb","description":"Llama-3.1-8B-Instuct model fine-tuned on the tool calling dataset.","status":"validating","created_at":1741172496,"validated_at":null,"running_from":null,"cancelled_at":null}'

It will take a few minutes for the model to launch. To see if it has been deployed, you can check the list of available models. Once the model is in this list, it is available for inference.

model_id = lora_creation_request["base_model"] + "-LoRA:" + lora_creation_request["name"]

while model_id not in {x.id for x in client.models.list()}:
 time.sleep(5)
print(f"Model {model_id} has been successfully deployed!")

>>> Model meta-llama/Meta-Llama-3.1-8B-Instruct-LoRA:tool-calling has been successfully deployed!

Alternatively, you can host the model locally via vllm’s OpenAI-compatible API and only change the client’s base URL. Here is an example code of how to host it with vllm (don’t forget to first install vllm with pip install vllm):

python3 -m vllm.entrypoints.openai.api_server --model $PATH_TO_BASE_MODEL --served-model-name llama-lora --trust-remote-code --disable-log-requests --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser llama3_json --gpu-memory-utilization 0.95 --max-num-seqs 128 --enable-lora --max-loras 1 --max-lora-rank 16 --lora-modules llama-3.1-8b-tool=llama-3.1-8b-tool --max-model-len 32768

Here, PATH_TO_BASE_MODEL is a path to Llama-3.1-8B-Instruct, saved via .save_pretrained(). If you’re running this code from the same machine where the model is hosted, you need to change the base_url attribute of your Client object to http://127.0.0.1:8000/v1. Otherwise, 127.0.0.1 needs to be changed to the VM’s IP address.

Let’s see how to use our model and test it on a complicated example. It’s preferable to stick with the same prompt template used during fine-tuning, as reproduced below.

SYSTEM_PROMPT_TEMPLATE = """
You are an expert in composing functions. \
You are given a question and a set of possible functions. \
Based on the question, you will need to make one or more function/tool calls to achieve the purpose. \
If none of the function can be used, point it out. \
If the given question lacks the parameters required by the function, also point it out. \
The current time is 2025-03-01 08:15:41. \
Here is a list of functions in JSON format that you can invoke:
{tools}

NO other text MUST be included.
""".strip()

Now let’s create a complicated example. The one below was generated with DeepSeek-R1.

tools = [
 {
 "name": "meme_factory.generate_meme",
 "description": "Creates a customized meme based on a template and text inputs.",
 "parameters": {
 "type": "dict",
 "properties": {
 "template_name": {
 "type": "string",
 "enum": [
 "Distracted Boyfriend",
 "Drake",
 "Two Buttons",
 "Change My Mind",
 "Expanding Brain"
 ],
 "description": "The base meme template to use."
 },
 "text_elements": {
 "type": "array",
 "description": "The text elements to overlay on the meme, in order of placement.",
 "items": {
 "type": "string"
 }
 },
 "style_options": {
 "type": "dict",
 "properties": {
 "font": {
 "type": "string",
 "enum": [
 "Impact",
 "Comic Sans",
 "Helvetica",
 "Arial Black"
 ],
 "description": "Font style for the meme text."
 },
 "color_scheme": {
 "type": "string",
 "enum": [
 "Classic",
 "Vaporwave",
 "Dark Mode",
 "Neon"
 ],
 "description": "Overall color theme of the meme."
 },
 "irony_level": {
 "type": "integer",
 "enum": [
 1,
 2,
 3,
 4,
 5
 ],
 "description": "How ironic/meta the meme should be (1=straightforward, 5=extremely meta)."
 }
 },
 "required": [
 "font"
 ]
 }
 } ,
 "required": [
 "template_name",
 "text_elements"
 ]
 }
 },
 {
 "name": "meme_factory.translate_to_memeglish",
 "description": "Converts regular text into internet meme language with popular references.",
 "parameters": {
 "type": "dict",
 "properties": {
 "input_text": {
 "type": "string",
 "description": "The original text to be converted."
 },
 "meme_dialect": {
 "type": "string",
 "enum": [
 "LOLcat",
 "Doge",
 "SpongeBob Mocking",
 "Modern TikTok",
 "Reddit"
 ],
 "description": "The specific meme language style to use."
 },
 "intensity": {
 "type": "integer",
 "enum": [
 1,
 2,
 3,
 4,
 5
 ],
 "description": "How intense the translation should be (1=mild, 5=incomprehensible to normies)."
 },
 "include_emojis": {
 "type": "boolean",
 "description": "Whether to include relevant emojis in the translation."
 }
 },
 "required": [
 "input_text",
 "meme_dialect"
 ]
 }
 },
 {
 "name": "meme_factory.schedule_post",
 "description": "Schedules a meme to be posted on selected social media platforms.",
 "parameters": {
 "type": "dict",
 "properties": {
 "content_id": {
 "type": "string",
 "description": "The ID of the previously generated meme or content."
 },
 "platforms": {
 "type": "array",
 "description": "List of social media platforms to post to.",
 "items": {
 "type": "string",
 "enum": [
 "Reddit",
 "Twitter",
 "Instagram",
 "TikTok",
 "Discord"
 ]
 }
 },
 "posting_time": {
 "type": "dict",
 "properties": {
 "time": {
 "type": "string",
 "description": "The time to post in 24-hour format (HH:MM)."
 },
 "timezone": {
 "type": "string",
 "enum": [
 "EST",
 "PST",
 "GMT",
 "UTC",
 "JST"
 ],
 "description": "The timezone for the posting time."
 },
 "day": {
 "type": "string",
 "enum": [
 "Today",
 "Tomorrow",
 "Next Monday",
 "Next Friday",
 "Next Meme Monday"
 ],
 "description": "The day to post."
 }
 },
 "required": [
 "time",
 "day"
 ]
 },
 "audience_targeting": {
 "type": "dict",
 "properties": {
 "age_group": {
 "type": "string",
 "enum": [
 "Gen Z",
 "Millennials",
 "Gen X",
 "Boomers",
 "All"
 ],
 "description": "Target age demographic."
 },
 "interests": {
 "type": "array",
 "description": "Specific interest categories to target.",
 "items": {
 "type": "string"
 }
 }
 }
 }
 },
 "required": [
 "content_id",
 "platforms",
 "posting_time"
 ]
 }
 }
]

user_query = """
Yo i need an expanding brain meme very funny with 4 levels showing how people chat: normal convo, reddit, TikTok, and Discord, \
and translate 'This meme perfectly encapsulates online communication evolution' to Doge-speak with max intensity and lots of emojis. \
All in one message, separate actions with two line breaks
""".strip()

Here’s how you run the model:

messages = [
 {'role': 'system', 'content': str(SYSTEM_PROMPT_TEMPLATE).format(tools=json.dumps(tools, indent=4))},
 {'role': 'user', 'content': user_query}
]

resp = client.chat.completions.create(
 model='meta-llama/Meta-Llama-3.1-8B-Instruct-LoRA:tool-calling',
 messages=messages,
 top_p=0.01,
 max_tokens=1024,
)
ft_model_generation = resp.choices[0].message.content

print(ft_model_generation)

>>> 
meme_factory.generate_meme(template_name="Expanding Brain", text_elements=["Normal conversation", "Reddit", "TikTok", "Discord"], style_options={"font": "Impact", "color_scheme": "Classic", "irony_level": 5})

meme_factory.translate_to_memeglish(input_text="This meme perfectly encapsulates online communication evolution", meme_dialect="Doge", intensity=5, include_emojis=True)

It did the job perfectly! It made two completely correct function calls, transformed the jargon “convo” to “conversation,” and separated the function calls with two line breaks as required.

Yet this is only one case. Let’s evaluate the quality of our fine-tuned model and ensure it improves over the original one. We can again do this conveniently using Nebius AI Studio.

# Evaluate the modelEvaluate the model

Heads up: Running this part will cost ~$0.1 if the model is deployed in AI Studio.

Let’s use the amazing Berkeley Function Calling Leaderboard (BFCL) dataset [4] to evaluate the tool-calling capabilities of our model and compare it with the original one.

To prepare the environment for evaluation, complete the instructions from the dataset repository guide.

Next, replace the value for OPENAI_API_KEY in the .env file with the Nebius API Key and add the following line:

OPENAI_BASE_URL=https://api.studio.nebius.ai/v1

If you launched the model locally, replace the value above with the corresponding url.

Finally, add your model name to the files ./gorilla/berkeley-function-call-leaderboard/bfcl/model_handler/handler_map.py and ./gorilla/berkeley-function-call-leaderboard/bfcl/eval_checker/model_metadata.py. For the first file, add add your model to api_inference_handler_map as follows:

api_inference_handler_map = {
<YOUR_MODEL_NAME>: OpenAIHandler,
...

For the ./gorilla/berkeley-function-call-leaderboard/bfcl/eval_checker/model_metadata.py, add your model to MODEL_METADATA_MAPPING as follows:

MODEL_METADATA_MAPPING = {
 <YOUR_MODEL_NAME>: [
 <YOUR_MODEL_NAME>,
 "",
 "",
 "",
 ],
...

Once you’re done with the preliminary steps above, launch the evaluation using the code below. An environment activation may differ for you depending on how you set up the environment. We will only evaluate our model on the AST-evaluation tasks to reduce costs.

If you host the model locally, you can most likely increase the number of parallel requests. We’ll use 2 to avoid encountering rate limit errors.

source .bfcl_venv/bin/activate
cd gorilla/berkeley-function-call-leaderboard/
export MODEL_ID=meta-llama/Meta-Llama-3.1-8B-Instruct-LoRA:tool-calling
export DATASETS=ast

bfcl generate \
--model $MODEL_ID \
--test-category $DATASETS \
--num-threads 2

bfcl evaluate \
--model $MODEL_ID \
--test-category $DATASETS

The output will look something like this:

Generating results for ['meta-llama/Meta-Llama-3.1-8B-Instruct-LoRA:tool-calling']
Running full test cases for categories: ['irrelevance', 'java', 'javascript', 'live_irrelevance', 'live_multiple', 'live_parallel', 'live_parallel_multiple', 'live_relevance', 'live_simple', 'multiple', 'parallel', 'parallel_multiple', 'simple'].
Generating results for meta-llama/Meta-Llama-3.1-8B-Instruct-LoRA:tool-calling: 100%|██████████| 3641/3641 [22:19<00:00, 2.72it/s] 
Number of models evaluated: 100%|██████████| 2/2 [00:01<00:00, 1.90it/s]
🦍 Model: meta-llama_Meta-Llama-3.1-8B-Instruct-LoRA:tool-calling
🔍 Running test: irrelevance
✅ Test completed: irrelevance. 🎯 Accuracy: 0.7166666666666667
🔍 Running test: java
✅ Test completed: java. 🎯 Accuracy: 0.65
🔍 Running test: javascript
✅ Test completed: javascript. 🎯 Accuracy: 0.86
🔍 Running test: live_irrelevance
✅ Test completed: live_irrelevance. 🎯 Accuracy: 0.37188208616780044
🔍 Running test: live_multiple
✅ Test completed: live_multiple. 🎯 Accuracy: 0.7369420702754036
🔍 Running test: live_parallel_multiple
✅ Test completed: live_parallel_multiple. 🎯 Accuracy: 0.625
🔍 Running test: live_parallel
✅ Test completed: live_parallel. 🎯 Accuracy: 0.8125
🔍 Running test: live_relevance
✅ Test completed: live_relevance. 🎯 Accuracy: 0.9444444444444444
🔍 Running test: live_simple
✅ Test completed: live_simple. 🎯 Accuracy: 0.7713178294573644
🔍 Running test: multiple
✅ Test completed: multiple. 🎯 Accuracy: 0.95
🔍 Running test: parallel_multiple
✅ Test completed: parallel_multiple. 🎯 Accuracy: 0.915
🔍 Running test: parallel
✅ Test completed: parallel. 🎯 Accuracy: 0.91
🔍 Running test: simple
✅ Test completed: simple. 🎯 Accuracy: 0.95
📈 Aggregating data to generate leaderboard score table...
🏁 Evaluation completed. See /home/aktsvigun/llama-tool-calling/gorilla/berkeley-function-call-leaderboard/score/data_overall.csv for overall evaluation results on BFCL V3.
See /home/aktsvigun/llama-tool-calling/gorilla/berkeley-function-call-leaderboard/score/data_live.csv, /home/aktsvigun/llama-tool-calling/gorilla/berkeley-function-call-leaderboard/score/data_non_live.csv and /home/aktsvigun/llama-tool-calling/gorilla/berkeley-function-call-leaderboard/score/data_multi_turn.csv for detailed evaluation results on each sub-section categories respectively.

The results are saved in ./gorilla/berkeley-function-call-leaderboard/score/data_non_live.csv and .../data_live.csv. Please note that your scores may not completely coincide with the ones listed in this blog post due to non-determinism in LLM kernels, but should be roughly the same.

Below you can check our fine-tuned model’s results versus the Llama-3.1-8B-Instruct reported scores on the leaderboard (ranked 70th as of Feb 2 2025):

 | Task
 | Fine-tuned model
 | Original model

 | Overall Non-Live AST
 | 0.899
 | 0.842

 | Non-Live Simple AST
 | 0.82
 | 0.728

 | Non-Live Multiple AST
 | 0.95
 | 0.935

 | Non-Live Parallel AST
 | 0.91
 | 0.87

 | Non-Live Parallel Multiple AST
 | 0.915
 | 0.835

 | 
 | 
 | 

 | Overall Live AST
 | 0.742
 | 0.713

 | Live Simple AST
 | 0.771
 | 0.74

 | Live Multiple AST
 | 0.737
 | 0.733

 | Live Parallel AST
 | 0.813
 | 0.563

 | Live Parallel Multiple AST
 | 0.625
 | 0.542

Overall value is the weighted average of the four embedded metrics. Bold formatting means higher scores within the task.

We can see our fine-tuned model outperformed the original across all related tasks. This underpins the necessity and benefits of fine-tuning. The evaluation results confirm that aligning an LLM to your specific needs can dramatically improve its quality on the target task.

# ConclusionConclusion

In this blog post, we demonstrated how fine-tuning unlocks a new level of model customization, improving performance on specialized tasks while trimming overall token usage due to shorter and potentially non-detailed prompts. Nebius AI Studio lets you streamline your entire workflows and adapt powerful models to your applications.

By simplifying every step of the process, AI Studio empowers you to quickly deploy tailored solutions that truly fit your real-world needs. We are looking forward to your first fine-tuning job!

### ReferencesReferences

- 

Weiwen Liu, Xu Huang, Xingshan Zeng, Xinlong Hao, Shuai Yu, Dexun Li, Shuai Wang, Weinan Gan, Zhengying Liu, Yuanqing Yu, Zezhong Wang, Yuxian Wang, Wu Ning, Yutai Hou, Bin Wang, Chuhan Wu, Xinzhi Wang, Yong Liu, Yasheng Wang, Duyu Tang, Dandan Tu, Lifeng Shang, Xin Jiang, Ruiming Tang, Defu Lian, Qun Liu, Enhong Chen. ToolACE: Winning the Points of LLM Function Calling. arXiv

- 

Touvron, Hugo, Lavril, Thibaut, Izacard, Gautier, Martinet, Xavier, Lachaux, Marie-Anne, Lacroix, Timothée, Rozière, Baptiste, Goyal, Naman, Hambro, Eric, Azhar, Faisal, others. The Llama 3 Herd of Models. arXiv

- 

Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang and Weizhu Chen. LoRA: Low-Rank Adaptation of Large Language Models. The Tenth International Conference on Learning Representations, ICLR 2022. arXiv

- 

Fanjia Yan, Huanzhi Mao, Charlie Cheng-Jie Ji and Tianjun Zhang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez. Berkeley Function Calling Leaderboard. Berkeley.edu

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius AI Cloud

Sign up​
Docs​

Akim Tsvigun
Senior ML Solutions Architect at Nebius

Contents

- Data preprocessing

- Fine-tuning

- Deploy the model

- Evaluate the model

- Conclusion

- References

## See also

### 

Make AI work for you: fine-tuning launches on Nebius AI Studio

Today marks a significant step forward for AI developers and businesses: fine-tuning is now available in Nebius AI Studio. This launch transforms how you can customize leading open-source models, making them work precisely for your specific needs.

March 5, 2025
2 mins to read

### 

Transforming ideas into images: Introducing text-to-image generation on Nebius AI Studio

From concept art to product visuals, text-to-image AI is revolutionizing creative workflows, reducing hours of design work to mere minutes. Today, we’re excited to launch Nebius AI Studio’s text-to-image service, delivering premium, production-ready image generation at a fraction of typical costs.

January 22, 2025
4 mins to read

### 

Nebius AI Studio expands with vision models, new language models, embeddings and LoRA

As the holiday season approaches and we all juggle year-end projects, we’re excited to bring you a gift of expanded capabilities on Nebius AI Studio. These updates — including advanced vision models, a broader range of language models, powerful embeddings and LoRA hosting — are designed to help you jumpstart the new year with stronger, more versatile AI tools.

December 17, 2024
2 mins to read

Sign in to save this post
Sign In
