# Create your own AI-powered code generator and reviewer: building an intelligent code companion

Source: https://nebius.com/blog/posts/building-ai-powered-code-generator

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

TL;DR: In this hands-on tutorial, you’ll build a full-stack AI code assistant using Next.js and Nebius AI Studio.

You’ll learn how to:

- 

Create a code generation system that works across multiple programming languages.

- 

Implement an intelligent code review feature with automated feedback.

- 

Set up and integrate AI models for code analysis.

- 

Build a professional-grade code editor interface.

Tech stack: Next.js, Monaco Editor, Nebius AI Studio

Time to complete: ~45 minutes

Difficulty level: Intermediate

Artificial intelligence is reshaping how we build modern applications. An increasing number of software products are adopting AI to create a more personalized experience for their users — even code editors and IDEs (Integrated Development Environments) are not left out.

Code editors like Visual Studio Code and IDEs such as PyCharm have integrated AI assistants to improve developer productivity. Highly intelligent code editors and assistants, such as Cursor and Tabnine, are being developed to help developers work more efficiently, debug code easily and ultimately reduce development time.

In this hands-on tutorial, you’ll learn how to create a powerful code generation and review application that you can customize to your exact needs.

We’ll build a full-stack application that can:

- 

Generate optimized code snippets in any programming language.

- 

Provide intelligent code reviews with actionable feedback.

- 

Explain complex code patterns in plain English.

- 

Help debug issues and suggest improvements.

Best of all? You’ll build this using open-source models and modern web technologies, making it both cost-effective and extensible.

Technical stack overview

We’ll use Next.js for the frontend and Nebius AI Studio for the AI capabilities. To fully understand this tutorial, a basic knowledge of React/Next.js is required.

## A note about Nebius AI StudioA note about Nebius AI Studio

Before we dive into the code, let’s briefly explore the AI platform we’ll be using. Nebius AI Studio is our recently launched inference platform designed specifically for developers building AI-powered applications. While you could use various platforms for this tutorial, we’ll demonstrate with AI Studio for a few practical reasons:

### What you’ll be able to use:What you’ll be able to use:

- 

Interactive playground: Test and refine your prompts before implementing them in code.

- 

Multiple model options: Access to DeepSeek Coder, Llama, Mixtral, Qwen, Nemotron and other leading open-source models.

- 

OpenAI-compatible API: If you’ve worked with OpenAI before, you’ll find the integration familiar.

- 

Cost efficiency: Competitive and transparent inference pricing, making it efficient for code generation scenarios where context can be large.

For this tutorial, we’ll be using the DeepSeek Coder model, which offers an excellent balance of performance and cost for code-related tasks. Now, let’s get started building our application!

## Building the application frontend with Next.jsBuilding the application frontend with Next.js

In this section, you’ll learn how to build the various UI components within the application. The application is divided into three components:

- 

The GenerateCode component accepts the user’s prompt and generates the code snippet that solves the problem.

- 

The ReviewCode component accepts a code snippet and an optional context, reviews the code to resolve any syntax errors and provides an adequate explanation.

- 

The Result component displays the responses from the code reviews and code snippet generation.

Create a new Typescript Next.js project by running the code snippet below:

npx create-next-app code-reviewer-app

Install the Monaco React Editor package, React Markdown and its dependencies.

npm install @monaco-editor/react react-markdown rehype-highlight remark-gfm

Before we proceed, create a types.d.ts file at the root of the Next.js project and copy the code snippet below into the file:

type ResultType = {
 code: string;
 explanation: string;
 language: string;
};

type CodeProps = {
 setToggleView: Dispatch<SetStateAction<"generate" | "review" | "result">>;
 setResultContent: Dispatch<
 SetStateAction<{ code: string; explanation: string; language: string }>
 >;
};

The code snippet above defines the structure of the variables used within the application.

Create a components folder within the Next.js app folder and add the GenerateCode.tsx, Result.tsx and ReviewCode.tsx files into the folder.

cd app
mkdir components && cd components
touch GenerateCode.tsx Result.tsx ReviewCode.tsx

Update the app/page.tsx file to render the home page of the application:

"use client";
import Link from "next/link";
import { useState } from "react";

type ViewType = "generate" | "review" | "result";

export default function Home() {
 const [toggleView, setToggleView] = useState<ViewType>("generate");

 return (
 <main className='w-full min-h-screen'>
 <nav className='w-full h-[10vh] flex items-center justify-between bg-blue-100 px-4 sticky top-0 z-10'>
 <Link href='/' className='text-xl font-bold'>
 CodePilot
 </Link>

 {toggleView === "generate" && (
 <button
 className='bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-700 cursor-pointer'
 onClick={() => setToggleView("review")}
 >
 Review Code
 </button>
 )}

 {toggleView === "review" && (
 <button
 className='bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-700 cursor-pointer'
 onClick={() => setToggleView("generate")}
 >
 Generate Code
 </button>
 )}

 {toggleView === "result" && (
 <button
 className='bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-700 cursor-pointer'
 onClick={() => setToggleView("generate")}
 >
 Generate Code
 </button>
 )}
 </nav>

 {/**--- The UI components placeholder*/}
 </main>
 );
}

The code snippet above renders a navigation element that allows users to toggle between different views, enabling them to either generate a new code snippet or review an existing one.

Next, render the UI components based on changes in the toggleView state value:

"use client";
import GenerateCode from "@/app/components/GenerateCode";
import ReviewCode from "@/app/components/ReviewCode";
import Result from "@/app/components/Result";
import Link from "next/link";
import { useState } from "react";

type ViewType = "generate" | "review" | "result";

export default function Home() {
 const [toggleView, setToggleView] = useState<ViewType>("generate");
 const [resultContent, setResultContent] = useState({
 code: "",
 explanation: "",
 language: "",
 } as ResultType);

 return (
 <main className='w-full min-h-screen'>
 <nav className='w-full h-[10vh] flex items-center justify-between bg-blue-100 px-4 sticky top-0 z-10'>
 {/** -- navigation bar and buttons -- */}
 </nav>

 {toggleView === "generate" && (
 <GenerateCode
 setToggleView={setToggleView}
 setResultContent={setResultContent}
 />
 )}
 {toggleView === "review" && (
 <ReviewCode
 setToggleView={setToggleView}
 setResultContent={setResultContent}
 />
 )}
 {toggleView === "result" && <Result resultContent={resultContent} />}
 </main>
 );
}

The code snippet above checks the current value of the toggleView state and renders the corresponding UI component. If the user chooses to generate or review a code snippet, the <GenerateCode /> or <ReviewCode /> component is rendered, respectively. When a result is available, the <Result /> component is displayed.

Now, let’s create the application UI components.

### The Generate Code componentThe Generate Code component

Copy the code snippet below into the GenerateCode.tsx file:

"use client";
import { useEffect, useState } from "react";
import { useMonaco } from "@monaco-editor/react";

export default function GenerateCode({
 setToggleView,
 setResultContent,
}: CodeProps) {
 const [languages, setLanguages] = useState<string[]>([]);
 const [selectedLanguage, setSelectedLanguage] = useState<string>("");
 const [context, setContext] = useState<string>("");
 const [disableBtn, setDisableBtn] = useState<boolean>(false);

 const monaco = useMonaco();

 //👇🏻 fetch the list of programming languages
 useEffect(() => {
 if (monaco) {
 const availableLanguages = monaco.languages
 .getLanguages()
 .map((lang) => lang.id);
 setLanguages(availableLanguages);
 }
 }, [monaco, selectedLanguage]);

 const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
 e.preventDefault();
 if (!selectedLanguage || !context.trim()) return;
 // 👉🏻 send data to the backend
 };

 return <main> {/** -- UI elements -- */}</main>;
}

From the code snippet above, the useEffect function returns a large array of programming languages supported by the React Monaco Editor and updates the setLanguages state with its result.

Return the following UI elements from the GenerateCode component:

return (
 <main className='w-full min-h-[90vh] p-4 flex flex-col items-center justify-center'>
 <h2 className='text-2xl font-bold mb-3'>Generate Code Snippets</h2>
 <form className='w-[90%] mx-auto' onSubmit={handleSubmit}>
 <textarea
 rows={6}
 required
 value={context}
 onChange={(e) => setContext(e.target.value)}
 placeholder='Provide a context for the code you need to generate'
 className='w-full border-[1px] border-gray-400 rounded px-4 py-2 mb-2'
 />
 <label
 htmlFor='language'
 className='block text-sm font-semibold text-gray-600 mb-2'
 >
 Select a programming language
 </label>
 <select
 className='w-full border-[1px] border-gray-400 rounded px-4 py-3 mb-5'
 value={selectedLanguage}
 onChange={(e) => setSelectedLanguage(e.target.value)}
 required
 >
 <option value=''>Select a language</option>
 {languages.map((lang) => (
 <option key={lang} value={lang}>
 {lang}
 </option>
 ))}
 </select>

 <button
 className='w-full bg-blue-500 text-white p-4 rounded-md hover:bg-blue-700 cursor-pointer'
 type='submit'
 disabled={disableBtn}
 >
 {disableBtn ? "Generating code..." : "Generate Code"}
 </button>
 </form>
 </main>
);

The code snippet above renders a form that allows users to enter a query for the code they want to generate and select their preferred programming language.

### The Review Code componentThe Review Code component

Copy the code snippet below into the ReviewCode.tsx file:

"use client";
import { useEffect, useState } from "react";
import Editor, { useMonaco } from "@monaco-editor/react";

export default function ReviewCode({
 setToggleView,
 setResultContent,
}: CodeProps) {
 //👇🏻 necessary React states
 const [languages, setLanguages] = useState<string[]>([]);
 const [selectedLanguage, setSelectedLanguage] =
 useState<string>("typescript");
 const [codeSnippet, setCodeSnippet] = useState<string>("");
 const [context, setContext] = useState<string>("");
 const [disableBtn, setDisableBtn] = useState<boolean>(false);
 const monaco = useMonaco();

 //👇🏻 fetch the list of languages
 useEffect(() => {
 if (monaco) {
 const availableLanguages = monaco.languages
 .getLanguages()
 .map((lang) => lang.id);
 setLanguages(availableLanguages);
 }
 }, [monaco, selectedLanguage]);

 const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
 e.preventDefault();
 if (!selectedLanguage || !context.trim() || !codeSnippet.trim()) {
 alert("Please provide a context and code snippet to review");
 return;
 }
 // 👉🏻 send data to the backend
 };

 return {
 /** -- UI elements -- */
 };
}

Return the following UI elements from the ReviewCode component. It renders a form that accepts the code snippet, its context and programming language.

return (
 <main className='w-full min-h-[90vh] p-4 flex flex-col items-center justify-center'>
 <h2 className='text-2xl font-bold mb-3'>Review Code Snippet</h2>
 <form className='w-[90%] mx-auto' onSubmit={handleSubmit}>
 <textarea
 rows={4}
 required
 value={context}
 onChange={(e) => setContext(e.target.value)}
 placeholder='Provide a context for the code you need to review'
 className='w-full border-[1px] border-gray-400 rounded px-4 py-2 mb-2'
 />
 <label
 htmlFor='language'
 className='block text-sm font-semibold text-gray-600 mb-2'
 >
 Select a programming language
 </label>
 <select
 className='w-full border-[1px] border-gray-400 rounded px-4 py-2 mb-5'
 value={selectedLanguage}
 onChange={(e) => setSelectedLanguage(e.target.value)}
 required
 >
 <option value=''>Select a language</option>
 {languages.map((lang) => (
 <option key={lang} value={lang}>
 {lang}
 </option>
 ))}
 </select>

 <div className=' w-full mx-auto border-[1px] border-blue-400 mb-5'>
 <Editor
 height='60vh'
 key={selectedLanguage}
 defaultLanguage={selectedLanguage}
 theme='vs-dark'
 defaultValue='// some comment'
 onChange={(value) => setCodeSnippet(value!)}
 />
 </div>

 <button
 className='w-full bg-blue-500 text-white p-4 rounded-md hover:bg-blue-700 cursor-pointer'
 disabled={disableBtn}
 >
 {disableBtn ? "Reviewing code..." : "Review Code"}
 </button>
 </form>
 </main>
);

### The Result componentThe Result component

The Result component displays the output returned from the ReviewCode and GenerateCode components, which includes a code snippet along with an explanation.

For instance, when a user generates code, the result will contain the AI-generated code and a description of its functionality. Similarly, when a user reviews a code snippet, the result will include a corrected (bug-free) version of the code along with an explanation.

Copy the code snippet below into the Result.tsx file:

import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css";
import Editor from "@monaco-editor/react";

export default function Result({
 resultContent,
}: {
 resultContent: { code: string; explanation: string; language: string };
}) {
 return (
 <main className='w-full min-h-screen p-4'>
 <div className=' w-full mx-auto border-[1px] border-blue-400 mb-2'>
 <Editor
 height='60vh'
 defaultLanguage={resultContent.language}
 theme='vs-dark'
 defaultValue={resultContent.code}
 />
 </div>

 <div className='min-h-[90vh] p-4 markdown-plain'>
 <Markdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
 {resultContent.explanation}
 </Markdown>
 </div>
 </main>
 );
}

The Editor component displays the code snippet, and the Markdown component renders the explanation from its Markdown format to a text format.

## How to set up Nebius AI in your software applicationsHow to set up Nebius AI in your software applications

Here, you’ll learn how to integrate Nebius AI into a Next.js application.

Before we proceed, you need to create an account using your Google or GitHub account.

Click on your profile icon to create an API Key.

Store the API key in .env.local file within your Next.js project.

NEBIUS_API_KEY=<your_Nebius_API_key>

Select Playground from the top bar menu to access the playground, where you can test and fine-tune your prompts using various AI models to ensure precise responses.

Nebius AI offers multiple models for both text and code generation. For this tutorial, we’ll use the DeepSeek-Coder-V2-Lite-Instruct model.

After multiple tests, I’ve created a prompt that generates consistent answers. Create a util folder, add a prompts.ts file and copy the following code snippet into the file:

const JsonResult = {
 code: "Code goes here",
 explanation: "# Explanation goes here",
};

export const generateCodePrompt = (
 userPrompt: string,
 language: string
): string => {
 const aiPrompt = `You are an AI code generator for an application that accepts user's request and generate the code that solves the user's problem in multiple programming languages. However, the user will provide his/her selected programming language and the problem to be solved. You are required to generate the code that solves the user's problem in the selected programming language. The user will provide the following information:
 - Programming language
 - Problem to be solved
 - Input data (if any)
 - Expected output (if any)
 - Constraints (if any)

 Now, your goal is to accept the user's request, generate the code that solves the user's problem in the selected programming and return a JSON object containing the code and the code explanation. The JSON object should be in the following format:
 ${JSON.stringify(JsonResult)}

 The user's request is:
 userPromptusing{userPrompt} usinguserPromptusing{language} programming language. Please use the format as stated above to generate the code and explanation that solves the user's problem in the selected programming language.
 Please ensure your result is a JSON object containing the code and explanation as object keys in the format stated above. `;

 return aiPrompt;
};

The generateCodePrompt function returns a string that represents the prompt, enabling users to generate code snippets in their preferred programming language and also return the correct result that can be used within the application.

Add the code snippet below to the prompts.ts file:

export const reviewCodePrompt = (
 userPrompt: string,
 code: string,
 language: string
): string => {
 const aiPrompt = `You are an AI code reviewer for an application that accepts user's code and review the code to ensure it meets the user's requirements. The user will provide the following information:
 
 - Programming language
 - The Code snippet to be reviewed
 - Context of the code
 - Expected output (if any)
 - Constraints (if any)

 Now, your goal is to accept the user's code snippet, review the code to ensure it meets the user's requirements and return a JSON object containing the review result. The JSON object should be in the following format:
 ${JSON.stringify(JsonResult)}

 The user's request is:
 Using following code snippet: \n codein{code} incodein{language} programming language. The context of the code is ${userPrompt}. Please use the format as stated above to review the code and return the result. Ensure your result is a JSON object containing the code and explanation as object keys in the format stated above.
 `;

 return aiPrompt;
};

The reviewCodePrompt function accepts the user’s prompt or context, the code snippet to be reviewed and its programming language. It returns a prompt that allows the user to review the code and obtain the desired result.

### Generating and reviewing code with Nebius AI StudioGenerating and reviewing code with Nebius AI Studio

After fine-tuning the prompts in Nebius AI Studio, you need to communicate with Nebius AI within the Next.js application.

Nebius AI allows you to use the OpenAI JavaScript SDK to communicate with the AI model within your application. Install the following package:

npm install openai

Create an API folder that will contain API endpoints for generating code snippets (/api/generate) and reviewing code snippets (/api/review) as shown below:

api
├── generate
│ └── index.ts
└── review
 └── index.ts

Copy the code snippet below into the generate/route.ts file:

import { generateCodePrompt } from "@/app/util/prompts";
import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

//👇🏻 OpenAI client for Nebius AI
const client = new OpenAI({
 baseURL: "https://api.studio.nebius.ai/v1/",
 apiKey: process.env.NEBIUS_API_KEY,
});

export async function POST(req: NextRequest) {
 const { context, language } = await req.json();
 //👇🏻 pass arguments into the AI prompt function
 const content = generateCodePrompt(context, language);

 //👉🏻 generate code and return result
}

The code snippet above creates an API endpoint that accepts the user’s query and the selected language, then performs a POST request to generate the code snippet.

Update the POST function to generate the code snippet using the selected model and specified prompt, then return the result to the frontend.

export async function POST(req: NextRequest) {
 const { context, language } = await req.json();

 const content = generateCodePrompt(context, language);

 //👇🏻 generate code using the prompt
 const response = await client.chat.completions.create({
 temperature: 0.3,
 max_tokens: 512,
 top_p: 0.95,
 model: "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
 messages: [
 {
 role: "user",
 content: content,
 },
 ],
 });

 const completion = response.choices[0];
 if (completion.message.content) {
 //👇🏻 gets the response
 const response = completion.message.content;
 //👇🏻 returns the JSON object
 const jsonMatch = response.match(/\{(.|\n)*\}/);
 const jsonObject = jsonMatch ? JSON.parse(jsonMatch[0]) : null;
 return NextResponse.json(
 { message: "Code generated successfully", data: jsonObject },
 { status: 200 }
 );
 } else {
 return NextResponse.json(
 { message: "No response", data: null },
 { status: 500 }
 );
 }
}

The POST function generates the code snippet using the Deepseek AI model and returns the result if successful; otherwise, it returns an error.

The review/route.ts file is similar to the generate/route.ts file, with the primary difference being the AI prompt and the parameters it receives. In addition to the user’s query and preferred language, the code review API endpoint also accepts the code snippet to be reviewed.

Copy the following code snippet into the review/route.ts file:

import { NextRequest, NextResponse } from "next/server";
import { reviewCodePrompt } from "@/app/util/prompts";
import OpenAI from "openai";

//👇🏻 OpenAI client for Nebius AI
const client = new OpenAI({
 baseURL: "https://api.studio.nebius.ai/v1/",
 apiKey: process.env.NEBIUS_API_KEY,
});

export async function POST(req: NextRequest) {
 const { context, selectedLanguage, codeSnippet } = await req.json();

 //👇🏻 pass arguments into the AI prompt function
 const content = reviewCodePrompt(context, codeSnippet, selectedLanguage);

 //👉🏻 generate code and return result
}

Finally, update the POST function to return the result after reviewing the code snippet:

export async function POST(req: NextRequest) {
 const { context, selectedLanguage, codeSnippet } = await req.json();

 const content = reviewCodePrompt(context, codeSnippet, selectedLanguage);

 const response = await client.chat.completions.create({
 temperature: 0.3,
 max_tokens: 512,
 top_p: 0.95,
 model: "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
 messages: [
 {
 role: "user",
 content: content,
 },
 ],
 });

 const completion = response.choices[0];
 if (completion.message.content) {
 const response = completion.message.content;
 const jsonMatch = response.match(/\{(.|\n)*\}/);
 const jsonObject = jsonMatch ? JSON.parse(jsonMatch[0]) : null;
 return NextResponse.json(
 { message: "Code generated successfully", data: jsonObject },
 { status: 200 }
 );
 } else {
 return NextResponse.json(
 { message: "No response", data: null },
 { status: 500 }
 );
 }
}

You can now make a request to each API endpoint to generate and review code snippets from both the GenerateCode and ReviewCode components, respectively.

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
 e.preventDefault();
 if (!selectedLanguage || !context.trim()) return;
 postRequest();
};

const postRequest = async () => {
 //👇🏻 disables button after a single click
 setDisableBtn(true);
 //👇🏻 sends a request
 const response = await fetch("/api/generate", {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({ context, language: selectedLanguage }),
 });

 //👇🏻 returns a response
 const data = await response.json();

 //👇🏻 displays the response
 if (data.data) {
 setResultContent({
 code: data.data.code,
 explanation: data.data.explanation,
 language: selectedLanguage,
 });
 setToggleView("result");
 } else {
 alert("An error occurred. Please try again");
 }
 setDisableBtn(false);
 setContext("");
 setSelectedLanguage("");
};

The code snippet above sends a request to the /api/generate endpoint, retrieves the result and displays it to the user. You can also create a similar function within the <Review/> component to pass in the necessary parameters and make a request to the /api/review endpoint.

Congratulations! You’ve completed the project for this tutorial.

## Next stepsNext steps

You’ve successfully built a powerful AI code assistant that you can customize and extend further. Try the live demo to see the application in action. Here are some ways to build upon this foundation:

### Enhance the applicationEnhance the application

- 

Add support for more complex code analysis scenarios.

- 

Implement user authentication to save favorite prompts and code snippets.

- 

Create shareable links for code reviews.

- 

Add support for team collaboration features.

### Optimize the AI integrationOptimize the AI integration

- 

Experiment with different models to find the best balance of speed and accuracy.

- 

Fine-tune prompts for specific use cases (e.g., specific frameworks or coding styles).

- 

Implement caching for commonly requested code patterns.

- 

Add streaming responses for faster feedback.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius

Sign up​
Docs​

Nebius team

## See also

### 

Building an AI-powered finance planner with full-stack Next.js and Nebius AI Studio

In this guide, we’ll build an AI-powered financial planner using the Meta Llama 3.1 70B model via Nebius AI Studio and a full-stack Next.js app. This solution works seamlessly whether you’re using the Pages Router or the App Router, as much of the customization relies on setting up a custom Next.js server.

November 27, 2024
9 mins to read

### 

How to run Meta Llama 3.1 405B with Nebius AI Studio API

Discover how Nebius AI Studio enables you to integrate the famous Llama 3.1 405B large language model in your applications.

October 17, 2024
8 mins to read

### 

How to choose between large and small AI models: A cost-benefit analysis

This blog post will guide you through the differences, use cases and cost-benefit analysis of different AI models, especially in the context of inference.

October 28, 2024
7 mins to read

Sign in to save this post
Sign In
