# Serving LLMs with vLLM: A practical inference guide

Source: https://nebius.com/blog/posts/serving-llms-with-vllm-practical-guide

Skip to main content

# Neural network and transformer foundationsNeural network and transformer foundations

Before getting into details, you can revisit the main concepts we’re going to talk about:
Click to expand

### What is a neural network?What is a neural network?

A neural network is a computer program made of layers of simple units called neurons. Each layer processes information, building up understanding step by step. Early layers find simple features, like word patterns, while deeper layers combine these to understand more abstract ideas, like the meaning of a sentence.

All neurons and their weights are stored as arrays of numbers in RAM or GPU memory. When you load a neural network onto a GPU, you are copying all these weights and layers’ code onto the GPU so it can do the calculations quickly.

Larger models may not fit on a single GPU. In that case, the model is split across multiple GPUs or even multiple nodes. The system divides the layers or parts of them between devices. Neurons on different GPUs communicate by sending their outputs (arrays of numbers) over high-speed connections. This is managed by deep learning frameworks like PyTorch, which handle all the details.

When you use a neural network for inference (i.e. getting answers from a trained model), the data flows through the layers in one direction — this is called a “forward pass”. During training, the network learns by comparing its output to the correct answer and adjusting its internal settings using a “backward pass”. Inference only needs the forward pass, which is much faster and uses less memory than training.

### Embeddings, weights, and quantizationEmbeddings, weights, and quantization

Embeddings

- 

When text is tokenized, each token is mapped to a numeric vector called an embedding.

- 

Embedding values are typically small real numbers, often between -1 and 1, initialized and learned during training.

- 

Only the embedding weights (the embedding matrix) are saved in the model. Prompt-specific embeddings are computed fresh for each request.

Weights

- 

Weights are the learned parameters of the neural network, stored as arrays of numbers — usually float32 or float16 by default.

- 

Only the weights are saved after training. No prompt-specific tokens or embeddings are stored.

Quantization

- 

Quantization reduces the precision of weights (e.g., from FP32 or FP16 to INT8, INT4 or FP8), saving memory and speeding up inference.

- 

This allows larger models to fit on limited hardware but may slightly reduce output quality. vLLM supports quantized weights (INT8, INT4, FP8, GPTQ, AWQ, etc.).

- 

Quantization is a trade-off: Lower precision means more efficiency, but potentially less accuracy.

- 

Typical workflows can run offline or on-load. In the offline method, convert the model once to a quantized file, keep that artifact, then point vLLM at the quantized checkpoint when you start the server. While on-load quantization is possible, it increases startup time and CPU/GPU usage.

- 

Use GPU for conversion, but pre-quantized checkpoints are preferred from model vendors when possible.

### TransformersTransformers

What is a transformer?

A transformer is a type of neural network designed to understand and generate sequences of text, like sentences or conversations. It is especially good at handling context, meaning it can “pay attention” to all the words in your prompt, not just the most recent ones.

Why is it powerful?

- 

Transformers generate coherent, context-aware responses because they can relate every word in the prompt to all other words, no matter how far apart they are.

- 

This capability allows it to answer questions, continue stories or hold conversations in a way that feels natural.

# LLM inference workflowLLM inference workflow

### Step-by-step workflowStep-by-step workflow

Model and weights loading: Before inference begins, the model architecture and its learned weights are loaded from disk or remote storage into CPU/GPU memory. This step happens once, before any prompts are processed. Basically, the model should be loaded with all layers’ states ready to receive the input tokens (embeddings).

Input preparation: You provide a prompt, such as text or chat history, to the model.

Tokenization: The model uses its tokenizer to split your text into tokens (words, sub-words or special symbols) and maps each token to a unique token ID (an integer) using the tokenizer and vocab files from the model artifacts.

Embedding lookup: Each token ID is used to look up a learned embedding vector from the model’s embedding matrix that is saved among the model artifacts as well. These vectors represent tokens in a way the neural network can process.

Prefill phase: The prefill phase occurs when the model processes the input tokens once, using the loaded weights, to set up its internal state for generation. If the inference engine uses a KV cache, the prefill pass stores key and value tensors for all input tokens, so subsequent decoding steps reuse them to avoid re-computing attention over the prompt.

Decoding phase: The model generates output tokens one by one. For each step, it uses the current context to predict the next token. The current context is saved in a KV cache. In the decoding phase, the model uses cached keys and values to efficiently generate each new output token, avoiding re-computation of the entire prompt.

Sampling parameters: At each decoding step, the model assigns probability scores to possible next tokens. It uses sampling parameters (like temperature, top_k, top_p) to select one token from the most likely candidates. This controls how creative or focused the output is.

Detokenization: The output token IDs are converted back into readable text using the tokenizer’s vocabulary.

Output: The final text (completion or chat reply) is returned to you.

The workflow repeats decoding steps until the desired number of tokens is generated or a stop condition is met.

### Key benchmarking metrics for LLM inferenceKey benchmarking metrics for LLM inference

- 

Latency: How quickly the model responds — time to first output token, time to full response.

- 

Throughput: How much work the system can handle — requests per second, tokens per second.

- 

Concurrency: Number of requests or users served at the same time.

- 

Memory usage: Amount of GPU/CPU memory consumed during inference.

# Additional concepts in model inferencingAdditional concepts in model inferencing
Click to expand

### Context windowContext window

The context window is the span of tokens the model can consider at once. It includes your prompt, system instructions, chat history and any assistant output fed back for continuity. If total tokens exceed the model’s maximum context length, the earliest tokens must be truncated or summarized. Larger context supports richer tasks (RAG, long chats) but consumes more memory and increases prefill latency.

### Vocabulary (Vocab)Vocabulary (Vocab)

“Vocab” is the set of tokens the tokenizer can emit. Larger vocabularies (e.g., ~150k in Qwen) can encode some languages or scripts more efficiently, potentially reducing token counts for the same text. Different tokenizers (BPE, SentencePiece, tiktokenderived) segment text differently — this affects token counts, latency and cost. Always use the tokenizer intended for the model and be cautious when switching variants.

### Positional encodingPositional encoding

Since neural networks don’t naturally understand the sequence order of a sentence, positional encoding adds extra information, so the model knows which token comes first, second, third and so on. Positional encoding is a mathematical technique used inside the model to give each token information about its position in the sequence.

Different models use different methods for positional encoding, such as ALiBi (used by BLOOM) or RoPE (used by Qwen and LLaMA). The positional encoding method is chosen during model training and is part of the model’s architecture. However, the attention backend is chosen at inference time and must be compatible with the model’s positional encoding. For example, some backends (like FlashAttention) only work with certain positional encodings (such as RoPE), while Torch SDPA and others are more flexible.

Both input and output tokens receive positional information. The model computes positional info for every token index at runtime.

### CUDA graphsCUDA graphs

CUDA graphs are a performance optimization feature. They allow you to record a sequence of GPU operations, such as neural network computations and replay them efficiently, reducing the overhead of launching individual operations. This is especially useful for deep learning inference, where the same computation graph is executed repeatedly for different inputs.

By capturing the computation as a CUDA graph, you can speed up model inference and improve throughput. CUDA graphs do not change the model’s logic or attention mechanism — they simply make the execution faster and more efficient on supported hardware

### WarmupWarmup

The first few requests may be slower due to model loading, memory allocation or kernel compilation. Warmup ensures that subsequent measurements reflect steady-state, realistic performance, not one-time initialization overhead.

# Example: Step-by-step workflow from prompt to answerExample: Step-by-step workflow from prompt to answer

Let’s walk through how a neural network predicts an answer, using the prompt “how are you?” and the expected answer “I am fine”. We’ll first explain the layers in a simple NN, then show a concrete example.

### Neural network layers (simple example)Neural network layers (simple example)

A basic neural network has:

- 

Input layer: Receives the input data (e.g., token-ids for each word).

- 

Hidden layer (or layers): Transforms the input using learned weights and activation functions. May consist of one or more layers.

- 

Output layer: Produces the final prediction (e.g., the next token or word).

Suppose we have:

- 

4 input neurons (for 4 input tokens).

- 

4 hidden neurons.

- 

1 output neuron (for simplicity).

Click to expand

### Step-by-step workflowStep-by-step workflow

Tokenization

- 

The prompt “how are you?” is split into tokens: [“how”, “are”, “you”, “?”]

- 

Each token is mapped to a token ID (an integer) in this phase.

Input layer

- 

In the input layer (embedding layer), each token ID is used to look up its embedding vector (e.g., [0.1, 0.2, 0.3, 0.4]) from the embedding matrix.

- 

The output of the input layer is the embedding vectors for each token — these are the numeric representations intended for deeper layers. Activations are produced by hidden layers after further processing.

Hidden layer (or layers)

- 

Each hidden neuron computes a weighted sum of all input neurons, adds a bias and applies an activation function, like ReLU or tanh.

- 

For example, Hidden Neuron 1: h1 = activation(w1_1*0.1 + w1_2*0.2 + w1_3*0.3 + w1_4*0.4 + b1)

- 

This is done for all 4 hidden neurons, each with its own set of weights and bias.

Output layer

- 

The output neuron takes the outputs from all hidden neurons, computes a weighted sum, adds a bias and applies an activation function.

- 

For example: output = activation(v1*h1 + v2*h2 + v3*h3 + v4*h4 + b_out)

- 

The output is a score for the next token (e.g., the probability of “I”).

Prediction

- The model selects the token with the highest score as the next word (e.g., “I”).

Repeat for next token

- 

The new input is now [“how”, “are”, “you”, “?”, “I”]. The process repeats: the model encodes the new sequence, passes it through the network and predicts the next token (e.g., “am”).

- 

This continues until the model outputs “fine” and then a stop token.

Summary table

 | Step
 | Input Tokens
 | Input Embedding
 | Output Tokens

 | 1
 | how, are, you, ?
 | […], […], […], […]
 | I

 | 2
 | how, are, you, ? , I
 | …
 | am

 | 3
 | how, are, you, ? , I, am
 | …
 | fine

 | 4
 | how, are, you, ? , I, am, fine
 | …
 | <eos>

Note: In real LLMs, the network is much deeper and more complex, and the input values are high-dimensional embeddings, not just single numbers. But the principle is the same: each layer transforms the input, and the output layer predicts the next token based on all previous tokens.

# Attention definedAttention defined

Imagine reading a book and trying to answer a question about the story. Your brain doesn’t just focus on the last sentence, you recall relevant details from earlier pages, weighing which memories matter most for your answer. In AI, attention is the mechanism that lets a model do something similar. For each new word, it looks back at all previous ones for context, deciding which parts are most important for the next step.

Attention at a glance

- 

For each token, the model decides how much to “pay attention” to all other tokens. This helps it understand the meaning of the whole sentence, not just each word in isolation.

- 

Attention lets the model dynamically focus on relevant parts of the context window (prompt, history, instructions) for each output token. It does not store or recall information like human memory, but it can “integrate” previous context by weighting and combining it at each step. The KV cache is a technical optimization that lets the model reuse these computed weights efficiently, so it can generate long outputs without reprocessing the entire prompt every time.

- 

The KV cache is primarily an inference-time optimization. During inference, the KV cache stores key and value tensors for previously processed tokens, so the model can generate new tokens efficiently without recomputing attention for the whole sequence.

- 

Attention backend is the software implementation (kernel) used to compute the attention mechanism efficiently on your hardware during inference — such as Torch SDPA, FlashAttention, Triton.

- 

You cannot change a model’s attention mechanism at serve time. You only choose the implementation kernel (attention backend) compatible with it.

### Attention backends: how to chooseAttention backends: how to choose

Select an implementation kernel compatible with the model’s attention and your hardware:

- 

Torch SDPA (baseline): Robust and widely compatible with ALiBi and RoPE positional encodings. Use it when unsure or if other kernels are unstable.

- 

FlashAttention v2/v3: A fast option, great fit for RoPE models like Qwen. Requires compatible head dimensions and positional encodings (not ALiBi).

- 

Triton attention: Good alternative for ALiBi models when you want more speed than SDPA.

- 

FlashInfer and other backends: Specialized high-performance options depending on the build. Verify the support matrix for your device.

### Transformers with attention and KV cacheTransformers with attention and KV cache

Modern LLMs use the transformer architecture, which relies on self-attention and the KV cache for efficient, context-aware generation. The process is visualized in the diagram below:

Click to expand

#### How it worksHow it works

- KV cache calculation (prefill phase)

- 

When you send a prompt (e.g., “how are you”), the model processes all input tokens in parallel.

- 

For each token, it computes Key and Value vectors and stores them in the KV cache. This cache holds the context for the entire prompt and is ready before any output tokens are generated.

- Token generation (decoding phase)

- 

For each new output token, the following steps happen on the fly:

- 

Query: The model computes a query vector for the current position.

- 

Dot product (attention score): The query is compared (dot product) with all stored keys in the KV cache, producing attention scores.

- 

Softmax: The scores are normalized into attention weights (probabilities).

- 

Weighted sum: The model computes a weighted sum of all value vectors using these weights, blending information from the prompt and previous outputs.

- 

Project to logits: The result is projected onto the vocabulary space via a linear layer, producing a logit (score) for every possible output token.

- 

Argmax or sampling: The model selects the next token by either picking the highest logit (argmax) or sampling from the probability distribution for more creative outputs.

- 

Detokenization: The selected token ID is converted back to text.

- 

The new token’s key and value are added to the KV cache, and the process repeats for the next output token.

#### Key pointsKey points

- 

The KV cache is calculated once for the prompt and reused for all output tokens, making generation efficient.

- 

Query, attention scores, softmax and weighted sum are computed dynamically for each output token.

- 

Projecting to logits and selecting the next token (argmax or sampling) are the final steps before detokenization.

### Example: Prompting with “how are you?” (with KV cache in action)Example: Prompting with “how are you?” (with KV cache in action)

Suppose you prompt the model with “how are you?” and it will reply “I am fine”. Here’s what the transformer does when KV cache is used:

- 

Tokenization: The prompt is split into tokens — “how”, “are”, “you”, “?”.

- 

Embedding: Each token is mapped to a numeric vector (embedding). The tokenizer converts each token to a token ID (an integer). The embedding layer uses this token ID as an index to look up a row in the embedding matrix (a table of learned vectors). The result is the embedding vector for that token.

- 

Layer processing: The embedding vectors are then passed into the next layer (or layers) of the neural network, such as self-attention or a hidden layer. In these layers, the embedding vectors are multiplied by weights and combined with biases and activation functions to produce new representations.

- 

Self-attention and KV cache (prefill phase)

- 

The transformer looks at all tokens in the prompt at once. For each token, it decides how much to “pay attention” to every other token.

- 

As it processes the prompt [“how”, “are”, “you”, “?”], the model computes key and value tensors for each token in the attention layers and stores them in the KV cache. This cache now holds the context for the entire prompt.

- 

In a transformer, each attention layer is a neural network layer that contains parameters (weights) and performs the self-attention operation. It is made up of multiple heads, each with its own set of weights and processes the input embeddings using matrix multiplications and softmax.

Attention scores, softmax and the KV cache

- 

For each token, the model computes an “attention score” for all other tokens by taking the dot product of their query and key vectors.

- 

The softmax function turns these raw scores into normalized weights (probabilities that sum to 1), letting the model blend information from all tokens in a learnable way.

- 

During inference, the KV cache stores the key and value vectors for previous tokens. This allows the model to quickly compute new attention scores and softmax weights for each new token, without recalculating everything for the whole sequence.

- 

Layer processing: The model passes these representations through many layers, each refining its understanding of the prompt and building up context.

- 

Decoding and KV cache (autoregressive decoding)

- 

The model predicts the next token (“I”) by considering the entire prompt. It uses the KV cache to efficiently access the context [“how”, “are”, “you”, “?”].

- 

The new token (“I”) is appended to the sequence, and its key and value tensors are added to the KV cache.

- 

This process repeats at each step, as the model uses the cached context from previous tokens to predict the next one. After the new token is generated, its key and value are added to the KV cache for the next iteration.

- 

The token-by-token generation loop using the KV cache is called the autoregressive decoding.

- 

Common autoregressive examples include GPT, LLaMA, Qwen, BLOOM and Falcon models. In contrast, non-autoregressive models like BERT and diffusion models predict multiple tokens simultaneously. BERT and other bidirectional masked models do not use a KV cache for decoding. Inspect architectures, is_decoder, is_encoder_decoder and use_cache in the model configuration to confirm autoregressive or non-autoregressive behavior — as we’ll explain in the next section.

# Model architecture and artifactsModel architecture and artifacts

When you download a model (e.g., from Hugging Face), you get more than weights:

- 

Weights: The model parameters, learned during training.

- 

Configuration (config.json): Architecture hyperparameters and positional strategy.

- 

Tokenizer assets: Including tokenizer.json, tokenizer_config.json, vocab/merges, specials.

- 

Generation defaults (optional): generation_config.json. When you load a model with transformers, these defaults are automatically applied unless you override them in your code. This helps ensure consistent, reproducible generation behavior across different environments and makes it easier to use the model as intended by its authors.

- 

Adapters (optional): Small sets of extra weights (such as LoRA or PEFT) that let you fine-tune a large model for a specific task without retraining all its parameters. LoRA (Low-Rank Adaptation) and PEFT (Parameter-Efficient Fine-Tuning) are popular techniques that add or modify a few layers or parameters, making it much cheaper and faster to adapt a model. Community adapters are pre-made fine-tuning weights shared by others for tasks like sentiment analysis, chat or code generation. You can load these adapters on top of a base model to quickly switch its behavior for different use cases. In simple terms: Adapters are extra weights you can load into your model to change or specialize its behavior for new tasks, without retraining the whole model. For example, you can add an adapter to make a general language model better at answering medical questions or writing poetry.

- 

Custom code (rare): trust_remote_code. You should only enable trust_remote_code for models from sources you trust, as this code runs with full permissions and could be unsafe.

# How model artifacts get loaded into the CPU/GPU memoryHow model artifacts get loaded into the CPU/GPU memory

When you load a model for inference, the Python framework (like Hugging Face Transformers) performs these steps:

- 

Load model config (architecture and hyperparameters) into CPU/system memory.

- 

Load tokenizer assets (tokenizer and vocab files) into CPU/system memory.

- 

Load model parameters (weights and embedding matrix) into GPU memory.

This process ensures that the model structure, vocabulary and embeddings are all consistent with how the model was trained, so inference works as expected.

You can run the following code to inspect a model’s configuration, including its layers and hidden size. This process does not require a GPU or perform any neural network computation. It only loads configuration data and the tokenizer into CPU memory, which the CPU then uses to generate token IDs for the input text.

Inspect a model’s configuration:

#!/usr/bin/env bash
set -euo pipefail

# change this if you prefer another path
BASE_DIR="$HOME/vens"
VENV_DIR="$BASE_DIR/hf"

# ensure parent folder exists, idempotent
mkdir -p "$BASE_DIR"

# create venv if missing
if [ ! -d "$VENV_DIR" ]; then
python3 -m venv "$VENV_DIR"
fi

# activate and install required packages
# this activation only affects this script's shell
. "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip transformers sentencepiece

# run the inspection script
python - <<'PY'
from transformers import AutoTokenizer, AutoConfig
model_id = "bigscience/bloom"
config = AutoConfig.from_pretrained(model_id)
print("Model config:", config)
print("Number of layers:", getattr(config, "num_hidden_layers", "N/A"))
print("Hidden size (neurons per layer):", getattr(config, "hidden_size", "N/A"))
tokenizer = AutoTokenizer.from_pretrained(model_id)
text = "Write a short poem about the moon."
token_ids = tokenizer.encode(text, add_special_tokens=True)
print("Token IDs:", token_ids)
print("Decoded text:", tokenizer.decode(token_ids))
PY

# optional, deactivate the venv
deactivate || true

Notes

- 

The script is idempotent and it reuses an existing venv.

- 

It requires Python 3.8 or newer and internet access to download the tokenizer/config.

- 

Caches go to ~/.cache/huggingface on your device.

- 

Paste the script into print-config.sh, make it executable, then run it:

vi print-config.sh
chmod +x print-config.sh
./print-config.sh

Operational implications

- 

Token counts drive latency and cost.

- 

Tokenizers differ across models.

- 

Ensure tokenizer and weights are from the same model repo/revision.

# Model licensesModel licenses

What to check

- 

License type: Fully open source, researchonly or restricted/commercial. Examples include BLOOM RAIL (open with use constraints) and the Tongyi Qianwen license (commercial use allowed under specific terms).

- 

Commercial use: Verify if it’s permitted and under what conditions. Some licenses require registration or approval for commercial deployments.

- 

Redistribution and derivatives: Check whether you are allowed to redistribute weights, finetuned variants or quantized artifacts.

- 

Attribution and restrictions: Some licenses include RAILstyle acceptableuse clauses or attribution requirements.

- 

Practical guidance: Read the model’s license, follow all required registration or attribution steps, add a LICENSE file linking to the original license, record model details in a NOTICE file and consult legal advice if any terms are unclear.

# Model profilesModel profiles

### A comparison between BLOOM-176B vs Qwen-72B modelsA comparison between BLOOM-176B vs Qwen-72B models

Use official model cards for authoritative specs. Below are practitioner notes:

BLOOM-176B (bigscience/bloom)

- 

Size and memory: 176B parameters; BF16/FP16 weights alone are ~352 GB. Expect multi-node tensor parallelism or quantization for serving.

- 

Context and positions: The model was trained with ~2k context and ALiBi positional bias. ALiBi impacts attention backend choice, so FA3 is not recommended. Torch SDPA or Triton are better options — Torch SDPA has been tested and it worked.

- 

Tokenizer and prompts: HF fast tokenizer. The model has no built-in chat template — you will need to add one for chat-style prompts.

- 

License: BigScience BLOOM RAIL 1.0.

- 

Read the Model Card here.

Qwen-72B (Qwen/Qwen-72B)

- 

Size and memory: 72B parameters. Authors note that BF16/FP16 requires ~144 GB of total GPU memory, while INT4 variants can fit ≈48 GB GPU memory. Consider this when planning the number of GPUs for deployment.

- 

Context and positions: The model supports 32k context via extended RoPE. Backend kernels like FlashAttention v2 are supported. SDPA is a safe fallback for the backend.

- 

Tokenizer and prompts: tiktoken-derived large vocab (>150k). Some transformer flows require trust_remote_code, so make sure your runtime supports the model transformer version. Chat variants may provide templates. A chat template is not needed for this variant.

- 

License: Tongyi Qianwen license.

- 

Read the Model Card here.

# vLLM core concepts and featuresvLLM core concepts and features

vLLM is a fast, open-source library for serving and running LLMs with high efficiency and throughput. It is designed to make LLM inference easy, scalable and cost-effective for both research and production. vLLM achieves state-of-the-art performance by using advanced memory management (PagedAttention), continuous batching and optimized GPU kernels. It supports seamless integration with Hugging Face models, streaming outputs and an OpenAI-compatible API server. vLLM runs on a wide range of hardware and supports distributed inference with tensor, pipeline, data and expert parallelism.

Key features

- 

PagedAttention for efficient KV cache management

- 

Continuous batching of incoming requests

- 

Optimized attention backends, like FlashAttention, FlashInfer, SDPA and Triton

- 

Fast model execution with CUDA/HIP graphs

- 

Quantization support (GPTQ, AWQ, INT4, INT8, FP8)

- 

Speculative decoding and chunked/disaggregated prefill

- 

Prefix caching for repeated prompts

- 

Multi-LoRA and multimodal model support

- 

Streaming outputs

- 

OpenAI-compatible API server

- 

Metrics and logging for production

### Parallelism in vLLMParallelism in vLLM

vLLM supports several types of parallelism to scale LLM inference across multiple GPUs and nodes:

- 

Tensor Parallelism (TP): Splits the model’s tensor computations, such as matrix multiplications in each layer, across multiple GPUs. Each GPU handles a slice of the computation for every layer. TP is not strictly one-to-one with GPUs, but for most users and typical LLM deployments, matching TP size to GPU count is the standard and recommended approach. Advanced setups may use more flexible mappings. TP is the most common way to scale very large models that cannot fit on a single GPU. --tensor-parallel-size (set to number of GPUs per node, e.g. --tensor-parallel-size=4).

- 

Model parallelism: Splits different layers or blocks of the model across GPUs or nodes. Each device holds a part of the model and passes activations between devices. This is useful for extremely large models. vLLM does not natively support pipeline or model parallelism (splitting layers across GPUs/nodes) in the same way as Megatron-LM or DeepSpeed. Most vLLM deployments use tensor parallelism for scaling. The --pipeline-parallel-size <int> enables pipeline parallelism, but it’s not widely used.

- 

Data parallelism: Each GPU runs a full copy of the model and processes different batches of input data. Gradients or outputs are synchronized as needed. While this approach is more common during training, vLLM is focused on inference. Although data parallelism (multiple copies of the model processing different batches) is not a primary feature, you can run multiple vLLM servers for scaling inferencing throughput.

- 

Expert parallelism: Used for Mixture-of-Experts (MoE) models, where different “experts” (sub-neural-networks) are distributed across devices. Each expert processes only the relevant part of the input and vLLM coordinates routing and aggregation. vLLM supports Mixture-of-Experts (MoE) models, where expert parallelism is used. This is a more advanced and model-specific setup. A Mixture-of-Experts (MoE) model contains multiple expert sub-models (networks), each specialized for certain types of input or tasks. The model dynamically routes tokens to the most relevant expert (s) for efficient and specialized processing.

How vLLM works — high-level flow
Click to expand

- 

Load tokenizer assets and weights and initialize tensor-parallel ranks (TP): The model and tokenizer are loaded into memory and tensor parallelism is set up across available GPUs.

- 

Start OpenAI-compatible server on the configured host/port: vLLM launches its API server, ready to accept requests.

- 

Workflow for each request: tokenize → schedule/batch → prefill/decode → detokenize. Incoming requests are tokenized, batched/scheduled for efficient GPU usage, processed through prefill and decode phases, and detokenized to produce output text.

- 

Stream or return final text and update the KV cache for subsequent tokens: Results are streamed or returned, and the KV cache is updated for efficient generation of further tokens.

Internally, vLLM manages the parallelism strategies listed above using efficient scheduling, memory management and communication primitives for GPU-to-GPU transfers. You can configure tensor parallel size and other options to match your hardware and workload. For most LLMs, tensor parallelism is set to the number of GPUs per node, but advanced deployments may combine multiple strategies for optimal scaling. Make sure to choose builds and images compatible with your accelerator.

For a detailed, step by step guide on deploying vLLM in Nebius AI Cloud, refer to our GitHub repo.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Reza Bahmanzadeh
AI Engineer at Nebius

Contents

- 

Neural network and transformer foundations

- 

LLM inference workflow

- Step-by-step workflow

- Key benchmarking metrics for LLM inference

- 

Additional concepts in model inferencing

- 

Example: Step-by-step workflow from prompt to answer

- Neural network layers (simple example)

- Step-by-step workflow

- 

Attention defined

- 

Attention backends: how to choose

- 

Transformers with attention and KV cache

- How it works

- Key points

- 

Example: Prompting with “how are you?” (with KV cache in action)

- 

Model architecture and artifacts

- 

How model artifacts get loaded into the CPU/GPU memory

- 

Model licenses

- 

Model profiles

- A comparison between BLOOM-176B vs Qwen-72B models

- 

vLLM core concepts and features

- Parallelism in vLLM

- How vLLM works

## See also

### 

Nebius delivers Europe’s first live NVIDIA GB300 NVL72 deployment

Europe’s first operational NVIDIA GB300 NVL72 systems are now live in Nebius AI Cloud. The Blackwell Ultra-based platform is fully deployed in our Finland data center, delivering supercomputer-class performance for large-scale training and high-throughput inference. This rollout expands the compute foundation available to teams building next-generation models across Europe.

December 17, 2025
2 mins to read

### 

Leveraging high-speed, rack-scale GPU interconnect with NVIDIA GB200 NVL72

Let’s explore one of the key features that makes the new NVIDIA GB200 NVL72 stand out: the fifth generation NVIDIA NVLink™ scale-up fabric. We’ll discuss how it redefines infrastructure by moving beyond the traditional 8-GPU NVLink. You’ll see a practical example of how to take advantage of this capability. Finally, we’ll examine a real-world use case: pre-training the Nemotron-4 340B LLM.

October 23, 2025
10 mins to read

### 

Fault-tolerant training: How we build reliable clusters for distributed AI workloads

When starting a job, you expect it to run without interruptions. This expectation holds true across many domains, but it resonates especially deeply with machine learning engineers who launch large-scale pre-training jobs. Maintaining a stable training environment is crucial for delivering AI results on schedule and within budget constraints.

August 28, 2025
9 mins to read

Sign in to save this post
Sign In
