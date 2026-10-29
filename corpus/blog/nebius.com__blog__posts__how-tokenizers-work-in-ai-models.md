# How tokenizers work in AI models: A beginner-friendly guide

Source: https://nebius.com/blog/posts/how-tokenizers-work-in-ai-models

Skip to main content

Before AI can generate text, answer questions or summarize information, it first needs to read and understand human language. That’s where tokenization comes in.

A tokenizer takes raw text and breaks it into smaller pieces or tokens. These tokens may represent whole words, parts of words or even individual characters and each is mapped to a unique numerical ID that models can process mathematically.

In this article we’ll explore how tokenizers work, examine common approaches and walk through the basics of building one yourself.

# What is a tokenizer in AIWhat is a tokenizer in AI

To help you understand tokenizers, we’ll start with the most commonly asked questions:

- 

What is a tokenizer? — A tokenizer is the first step in allowing a machine to read and understand human language.

- 

How does a tokenizer work? — At its simplest, a tokenizer is a tool that takes raw text and breaks it into smaller, manageable pieces called tokens. Depending on the design, tokens might be words, subwords, characters or even punctuation marks. By dividing text into smaller units, the tokenizer provides a structured representation that a language model can work with.

- 

What is a tokenizer in LLM? — In LLMs such as GPT, tokenization does more than just splitting text. Each token is mapped to a unique numerical ID, creating a sequence of numbers that the model can process mathematically. This is critical because neural networks cannot directly ‘read’ letters or words — they only operate on numbers.

Without tokenization, the connection between our human-readable sentences and the model’s numerical computations would be impossible.

Think of tokenization as turning language into Lego blocks. Each block (token) represents a small, well-defined piece of the whole. By snapping these blocks together in different ways, the model can build meaning, generate new sentences or understand context. Just as Lego blocks allow many different creations from a finite set of pieces, tokens give AI the flexibility to interpret and generate a vast range of human language.

You can read more about tokens and how AI processes language in our blog.

# How does a tokenizer workHow does a tokenizer work

At a high level, a tokenizer transforms raw text into something a model can understand. It does this by following a predictable workflow:

- Take the input

- Break it into smaller pieces

- Map those pieces to numerical IDs

Let’s examine the process step-by-step:

### Take input stringTake input string

The process starts with a plain text input, such as a sentence or prompt. For example:

Nebius is the best

### Split into meaningful units (words, subwords or characters)Split into meaningful units (words, subwords or characters)

The tokenizer divides the string into smaller chunks. Depending on the tokenizer, these may be entire words, smaller subwords or single characters. For example:

[“Nebius”, “is”, “the”, “best”]

### Map each unit to a token ID using a vocabularyMap each unit to a token ID using a vocabulary

Next, each unit is converted into a numerical ID, based on a predefined vocabulary. These IDs act as the model’s “language”, allowing it to work with numbers instead of text. For example:

[5001, 40, 78, 312]

### ExamplesExamples

Here’s a simple view of the pipeline:

Text → Tokens → IDs
"Nebius is the best"
→ ["Nebius”, " is", " the", " best"]
→ [5001, 40, 78, 312]

Think of it like a translation process: natural language goes in, machine-readable numbers come out.

Here’s how it looks with the Hugging Face transformers library, which you can run directly in Python. This version uses GPT-2’s tokenizer.

from transformers import GPT2Tokenizer

# Load pretrained GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Step 1: Take input string
text = "Nebius is the best"

# Step 2 and 3: Encode text into token IDs
token_ids = tokenizer.encode(text)

# Optional: decode back into tokens for clarity
tokens = [tokenizer.decode([tid]) for tid in token_ids]

print("Text:", text)
print("Tokens:", tokens)
print("Token IDs:", token_ids)

This is what happens:

- 

The tokenizer is loaded from the pretrained GPT-2 model.

- 

The text is automatically split into subwords and mapped to IDs.

- 

In this example we’ve also decoded each ID back into its sub-token, so you can see both forms.

- 

All the IDs we’ve used in this example are illustrative, not real GPT or BERT IDs — if you run this code yourself, you will get different IDs.

# Types of tokenization methodsTypes of tokenization methods

To grasp how to train a tokenizer, you first need to understand that not all tokenizers break text in the same way. Different strategies exist, each with its own strengths and weaknesses. The method you choose can have a direct impact on vocabulary size, efficiency and the model’s ability to handle unusual words.

### Word tokenizationWord tokenization

This is the most straightforward method, where each word in a sentence becomes a token. For example, “AI is powerful” would become ["AI", "is", "powerful"].

But while this is simple to understand, word tokenization has limitations. Languages have vast vocabularies and many variations — such as plurals or misspellings — that can create entirely new tokens. This leads to large vocabularies and poor handling of unusual words, which is why modern LLMs rarely rely on word-level tokenization.

### Character tokenizationCharacter tokenization

Here, each character, including spaces and punctuation, is treated as a token. For example, “AI” would tokenize into [“A”, “I”].

Character tokenization avoids the problem of out-of-vocabulary words, as every possible string can be expressed as a sequence of characters. However, this method produces much longer token sequences, which can increase processing times and make it harder for models to capture meaning across larger contexts.

### Subword tokenizationSubword tokenization

This is the most widely used approach, where subword tokenization strikes a balance between words and characters.

Algorithms such as Byte-Pair encoding (BPE), WordPiece and the Unigram language model split text into chunks that are often whole words, but can also be meaningful fragments (for example, “un” and “able”).

This allows models to efficiently represent common words while handling unusual terms by breaking them into smaller parts. Subword methods are at the core of tokenizers used in models such as GPT, BERT and many others.

This table summarises the advantages, limitations and typical use cases of each approach.

 | Method
 | Advantages
 | Limitations
 | Typical use cases

 | Word tokenization
 | Simple and intuitive; preserves whole word meaning
 | Large vocabulary; fails with unusual words; less effective for complex languages
 | Early Natural Language Processing (NLP) systems, basic search and text classification

 | Character tokenization
 | Small sets of characters; works for any language or script
 | Very long sequences; loses meaning of words
 | Processing languages without clear word boundaries (for example, Chinese and Japanese)

 | Subword tokenization
 | Balances vocabulary size and flexibility; handles rare and compound words
 | Slightly more complex; rules vary across methods (for example, BPE, WordPiece and SentencePiece)
 | Modern LLMs like BERT, GPT and multilingual models

See Nebius AI Cloud docs to find a variety of articles and tutorials to help you make the best of your AI projects.

# What is a tokenizer in LLMs like GPT or BERTWhat is a tokenizer in LLMs like GPT or BERT

Tokenizers in LLMs such as GPT or BERT are highly optimized systems designed for both efficiency and consistency.

For example, GPT-4 uses a Byte-Pair Encoding (BPE) tokenizer, which can handle any text by representing it as subword units at the byte level. This allows the model to seamlessly process words from different languages, emojis, code snippets and even unusual spellings without breaking down.

These tokenizers also introduce special tokens to mark important positions in text. For instance, a beginning-of-sequence (BOS) token signals the start of input, while an end-of-sequence (EOS) token marks where it finishes.

In dialogue systems such as ChatGPT, other special tokens may be used to separate user instructions, model responses or system messages. These formatting tokens act as guideposts, ensuring the model knows how to interpret and generate structured text.

One of the most critical aspects is consistency: the tokenizer used during pretraining must also be applied during inference. For example if, during model training, the model learned to associate a certain token ID with the fragment “un”, then breaking “unhappy” in a different way at inference would confuse the model and degrade performance.

In practice, this means the tokenizer is not an optional accessory — instead, it’s an inseparable part of the model’s architecture. Understanding how it works helps explain why LLMs can generalize so well across vast volumes of human words.

You can read more about AI training and inference in the machine learning lifecycle in our blog.

# How to make a tokenizer from scratchHow to make a tokenizer from scratch

Sometimes an off-the-shelf tokenizer isn’t enough. If you’re working with large custom datasets, fine-tuning for a niche application or building models for low-resource languages, creating your own tokenizer ensures that the model learns from tokens tailored to your domain and vocabulary.

### Step 1: Collect text corpusStep 1: Collect text corpus

Start by gathering a large, representative dataset of the text you want your model to understand. For example, medical journals for a healthcare model or legal documents for a law-focused LLM.

You can read more about methods for maximizing efficiency in preparation for training large models.

### Step 2: Choose a method (for example, BPE)Step 2: Choose a method (for example, BPE)

Decide on the tokenization strategy. Subword methods like Byte-Pair Encoding (BPE) are most common, but alternatives such as WordPiece or Unigram Language Model may suit your needs better.

### Step 3: Train a tokenizer model using tools, such as those in the Hugging Face tokenizers libraryStep 3: Train a tokenizer model using tools, such as those in the Hugging Face tokenizers library

Feed your corpus into a tokenizer training framework. Libraries such as Hugging Face’s tokenizers make this process efficient, automatically splitting text and building vocabularies.

### Step 4: Save vocabulary and use during training and inferenceStep 4: Save vocabulary and use during training and inference

Once trained, export the tokenizer’s vocabulary and merge rules. These files must be used consistently during both model training and inference to ensure reliable results.

### Tools required: Hugging Face tokenizers, SentencePiece, spaCyTools required: Hugging Face tokenizers, SentencePiece, spaCy

Popular libraries such as Hugging Face, spaCy and SentencePiece — which is used by Google and others — provide ready-to-use implementations. They simplify everything from training to deployment, allowing you to focus on fine-tuning your model rather than reinventing the wheel.

As pre-training LLMs requires a stable environment to deliver results on schedule and budget, find out how Nebius builds reliable clusters for distributed AI workloads.

# Why tokenization matters in AIWhy tokenization matters in AI

Tokenization isn’t just a preprocessing step — it’s foundational to how language models function. The way text is split into tokens directly affects how efficiently a model learns, how much computation it requires and even how fairly it represents different kinds of language.

### Affects model efficiency and accuracyAffects model efficiency and accuracy

A well-designed tokenizer reduces redundancy and captures meaning with fewer tokens. This allows the model to focus on learning meaningful patterns, improving both training efficiency and accuracy. On the other hand, poor tokenization can waste capacity on unhelpful splits.

### Controls sequence length (cost impact)Controls sequence length (cost impact)

Since model inputs are limited by a maximum number of tokens, tokenization affects how much text fits into a prompt. More tokens mean higher computational costs and slower responses. Compact tokenization helps reduce expense while maximizing the information carried per token.

### Influences generalization and robustnessInfluences generalization and robustness

Subword-based tokenization lets models handle unusual words or variations by breaking them into smaller, familiar pieces. This flexibility improves robustness, allowing the model to generalize beyond its training data.

### Can introduce biases depending on training corpusCan introduce biases depending on training corpus

If the training corpus over-represents certain spellings, dialects or languages, the tokenizer’s vocabulary may reflect those biases. As a result, the model could underperform on underrepresented groups or styles of writing. Choosing diverse, balanced text sources helps to mitigate this issue.

If you’re interested in diving deeper into machine learning experiments and finding out more, you can read what it takes to build a reasoning model.

# ConclusionConclusion

Tokenizers are the bridge between human language and machine intelligence. By breaking text into tokens and mapping them to numerical IDs, they allow LLMs such as GPT and BERT to process, understand and generate language.

Far from being a background detail, the tokenizer’s design directly affects efficiency, accuracy and cost. A poorly chosen tokenization method can inflate sequence lengths, miss subtle meanings or reinforce biases hidden in the training data. Well-designed tokenization, by contrast, makes models more robust, adaptable and scalable.

For anyone learning about LLMs, understanding tokenization is an essential step. The good news is that libraries such as Hugging Face or SentencePiece make it easy to experiment. By training a simple tokenizer on a custom dataset, you can see how different choices — word level, character level or subword — impact performance.

If you want to grasp how AI models ‘think’, start with tokenization. It’s the invisible layer that transforms messy human language into machine-readable building blocks. By exploring and experimenting, you’ll gain deeper insight into how today’s most powerful AI systems are built and how you can shape them for your own projects. Chat with us today to find the right solution for your business.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- 

What is a tokenizer in AI

- 

How does a tokenizer work

- Take input string

- Split into meaningful units (words, subwords or characters)

- Map each unit to a token ID using a vocabulary

- 

Types of tokenization methods

- Word tokenization

- Character tokenization

- Subword tokenization

- 

What is a tokenizer in LLMs like GPT or BERT

- 

How to make a tokenizer from scratch

- Step 1: Collect text corpus

- Step 2: Choose a method (for example, BPE)

- Step 3: Train a tokenizer model using tools, such as those in the Hugging Face tokenizers library

- Step 4: Save vocabulary and use during training and inference

- Tools required: Hugging Face tokenizers, SentencePiece, spaCy

- 

Why tokenization matters in AI

- Affects model efficiency and accuracy

- Controls sequence length (cost impact)

- Influences generalization and robustness

- Can introduce biases depending on training corpus

- 

Conclusion

## See also

### 

What is Jupyter Notebook in the context of AI

Jupyter Notebook is a browser-based tool for interactive coding, data exploration and documentation. It lets you run code step by step while combining results, visualizations and explanations in one place. Widely used in machine learning, it speeds up experimentation, ensures reproducibility and makes collaboration easier. This article looks at how Jupyter supports ML workflows, its key features and the tasks it handles best.

September 15, 2025
9 mins to read

### 

Epochs in day-to-day machine learning processes

This guide explains what an epoch means in day-to-day ML pipelines and workflows, how to recognize when you’ve trained enough, and which factors determine a sensible stopping point.

August 19, 2025
8 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
