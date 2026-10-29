# Transforming ideas into images: Introducing text-to-image generation on Nebius AI Studio

Source: https://nebius.com/blog/posts/introducing-text-to-image-ai-studio

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

# What this means for youWhat this means for you

Generate stunning visuals at scale without breaking the bank. Our text-to-image service unlocks powerful new possibilities across industries: marketing teams can generate and test ad variations in minutes, game studios are able to rapidly prototype concept art, and design agencies gain the ability to accelerate their ideation process. For e-commerce brands, producing product lifestyle imagery at scale becomes seamless, while app developers can streamline UI/UX workflows with real-time visual generation.

With consistent style control and flexible pricing, you can experiment freely and scale confidently — whether you’re crafting custom social media content or generating assets for your next big launch. The service offers:

- 

High-resolution output up to 2000×2000: No more scrimping on quality.

- 

Speed at 1.8 seconds per image: Perfect for real-time feedback loops.

- 

Simple, predictable costs from 0.0013 USD per image: No hidden fees.

- 

Enterprise-grade reliability: Built to scale with your projects.

- 

Unlimited rate limits on request: Start with default caps and scale to virtually infinite throughput.

This combination sets a new standard for professional image generation, empowering you to create without limits.

# Meet the modelsMeet the models

Choose the perfect model for your specific needs:

### Flux SchnellFlux Schnell

- 

Ultra-fast generation in 1.8 seconds

- 

Perfect for rapid prototyping and real-time applications

- 

0.0013 USD per image (1.30 USD per 1K images)

- 

Ideal for: UI/UX workflows, live previews, rapid iterations

Figure 1. Example prompt: Nature documentary capture with focal length 180, close-up: [Gracious tiger crawls through the grass detecting his pray], [individual fur hairs slightly more under the breeze]. Focus stacking enabled, natural colors.

### Flux DevFlux Dev

- 

Production-quality output

- 

Advanced parameter control

- 

0.007 USD per image (7.00 USD per 1K images)

- 

Ideal for: marketing materials, e-commerce, professional content

Figure 2. Example prompt: Hyperrealistic brick-built llama, standing proud with visible studs, warm earth tones, studio lighting, clean background, photorealistic rendering, matte plastic texture.

### Stable Diffusion XLStable Diffusion XL

- 

Premium artistic quality

- 

Enhanced creative control

- 

0.003 USD per image (3.00 USD per 1K images)

- 

Ideal for: high-end visuals, detailed artwork, professional creative work

Figure 3. Example prompt: A sleek aluminum can with an iridescent teal-to-rose gradient on a rustic wooden table in a sunlit living room. Delicate condensation droplets catch the light. Minimal geometric patterns, photorealistic rendering, soft bokeh, natural lighting.

# Why Nebius AI Studio stands outWhy Nebius AI Studio stands out

We’ve built our service to scale with your imagination, with no resolution caps or strict quotas.

🔍 Superior Resolution & Quality

- 

Generate images up to 2000×2000 pixels (4 megapixels) — that’s up to 4 times larger than most alternatives

- 

Adjust your results with advanced parameter controls

- 

Achieve consistent results with seed management and negative prompts

💰 Industry-leading pricing

- 

No hidden fees or size-based pricing variations

- 

Simple, predictable costs for easier budgeting

🚀 Built for production

- 

OpenAI-compatible API for seamless integration

- 

Flexible rate limits that grow with your needs

- 

Enterprise-grade infrastructure for reliable scaling

# Short, hands-on examplesShort, hands-on examples

Implementing our text-to-image service is straightforward. Here’s a quick example using cURL:

curl -X 'POST' \
 'https://api.studio.nebius.ai/v1/images/generations' \
 -H 'accept: application/json' \
 -H "Authorization: Bearer $NEBIUS_API_KEY" \
 -H 'Content-Type: application/json' \
 -d '{
 "model": "black-forest-labs/flux-schnell",
 "prompt": "A serene landscape at sunset, with rolling hills and a lone tree silhouette",
 "response_format": "url"
 }'

And here’s the one for Python:

from openai import OpenAI

client = OpenAI(
 base_url="https://api.studio.nebius.ai/v1/",
 api_key="your_api_key"
)

response = client.images.generate(
 model="stability-ai/sdxl",
 prompt="A serene mountain landscape at sunrise, with mist in the valley",
 size="1024x1024",
 response_format="b64_json",
 extra_body={
 "response_extension": "webp", # Optimize for web delivery
 "num_inference_steps": 40, # Higher quality output
 "seed": 123456, # Reproducible results
 "negative_prompt": "dark, cloudy, storm, hazy"
 }
)

Key parameters to customize your generations include:

- 

size: Support for resolutions up to 2048×2048 pixels

- 

num_inference_steps: Adjust the generation quality

- 

seed: Enable consistent, reproducible results

- 

negative_prompt: Refine outputs by specifying what to exclude

- 

response_format: Get results as URLs or base64-encoded images

All models available in Studio support these parameters, allowing you to optimize for your specific needs — whether it’s ultra-fast generation with Flux Schnell or premium quality with SDXL.

Want to experiment without coding? Try our interactive Playground to test different models and prompts instantly.

### Three ways to master prompt craftingThree ways to master prompt crafting

The key to exceptional AI-generated images is in how you describe them. Here are three proven techniques to improve your results:

- 

Be specific with composition. Instead of “A cat,” try “A Persian cat sitting in a sunlit window, soft morning light, professional photography.”

- 

Use negative prompts to refine results:

{
"prompt": "Professional headshot of a business person",
"negative_prompt": "blurry, distorted features, unrealistic lighting"
}

- Save seeds for consistency. Keep your seed value when you find the perfect style and use it across multiple generations for consistent results. This approach is perfect for creating sets of related images.

# ConclusionConclusion

### What’s nextWhat’s next

We’re actively developing image-to-image transformations, advanced editing capabilities, model fine-tuning options, enhanced control features and an ability of running LoRA models. Plus, we’re continuously optimizing the models for even better quality and performance.

### How to get started in minutesHow to get started in minutes

- 

Experiment with our Playground for instant results.

- 

Get your API key to integrate text-to-image into your workflows.

- 

Explore our documentation for deeper insights.

We can’t wait to see what you create.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius

Sign up​
Docs​

Nebius team

## See also

### 

How to run Meta Llama 3.1 405B with Nebius AI Studio API

Discover how Nebius AI Studio enables you to integrate the famous Llama 3.1 405B large language model in your applications.

October 17, 2024
8 mins to read

### 

Building an AI-powered finance planner with full-stack Next.js and Nebius AI Studio

In this guide, we’ll build an AI-powered financial planner using the Meta Llama 3.1 70B model via Nebius AI Studio and a full-stack Next.js app. This solution works seamlessly whether you’re using the Pages Router or the App Router, as much of the customization relies on setting up a custom Next.js server.

November 27, 2024
9 mins to read

### 

Creating your own AI-powered code generator and reviewer

In this hands-on tutorial, you’ll learn how to create a powerful code generation and review application that you can customize to your exact needs. We’ll use Nebius AI Studio and open-source models, making it both cost-effective and extensible.

December 3, 2024
20 mins to read

Sign in to save this post
Sign In
