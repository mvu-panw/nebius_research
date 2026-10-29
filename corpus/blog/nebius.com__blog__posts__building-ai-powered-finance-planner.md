# Building an AI-powered finance planner with full-stack Next.js and Nebius AI Studio

Source: https://nebius.com/blog/posts/building-ai-powered-finance-planner

Skip to main content

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

Why build something like this? Imagine having a financial assistant available 24/7, ready to analyze your spending and provide personalized recommendations. After a significant purchase, this AI-powered app could suggest budgeting tips or saving strategies tailored to your transactional data. It could also assess your creditworthiness, offer insights into your expenses and uncover trends you might otherwise overlook. This is the transformative power of AI-driven financial tools.

# IntroductionIntroduction

This guide is curated to be a starting point for most folks. You can use it as a playground for experimentation, whether you’re familiar with Nebius AI Studio or entirely new to Generative AI. Feel free to modify the code, explore its structure, and make it your own.

The guide covers four primary steps:

- Setting up the dev environment

- Building the frontend

- Mocking bank APIs

- Integrating Nebius AI Studio

We’ll use mock financial data, including transaction and card data, throughout this project.

By the end of the guide, you’ll be able to:

- Create a full-stack Next.js application

- Integrate with Nebius AI Studio

- Use Zustand for state management

- Utilize Shadcn components to streamline frontend development

# Why use Nebius AI Studio?Why use Nebius AI Studio?

Studio provides an Inference Service (hosted machine learning model) designed to simplify complex tasks. You can access leading open-source models from Meta, Microsoft, DeepSeek and more. Nebius AI Studio’s intuitive and user-friendly interface ensures a smooth experience. The platform also features a simple playground where you can experiment with AI models without needing to open a code editor.

Cloud resource billing can be intimidating. What sets Nebius AI Studio apart from other hosting providers is its generous welcome credit of up to 1 million tokens*, enabling you to experiment freely.

Once you sign up, the interface will look like this:

# Project walkthroughProject walkthrough

In this project, you’ll view financial transactions related to bot income, expenses and subscriptions. The dashboard displays all transactional data, with options to add more features in the future.

The key highlight is the AI-powered knowledge base integrated into the app, allowing you to query the model with questions about your specific data.

Here’s a snapshot of a simple query:

# Building Money-GuardBuilding Money-Guard

Let’s name the financial planner application “Money-Guard” to give it a touch of personality.

Money-Guard is a sleek, full-stack Next.js app built in under two hours. It processes user data from bank transactions and, based on user queries, handles input through a React form event, returning responses powered by OpenAI.

### Step 0: Setting up a Next.js projectStep 0: Setting up a Next.js project

Install Node.js. Then, run the following commands in the terminal.

npx create-next-app@latest

Answer the prompts as follows:

Would you like to use TypeScript? Yes
Would you like to use ESLint? Yes
Would you like to use Tailwind CSS? Yes
Would you like your code inside a `src/` directory? No
Would you like to use App Router? (recommended) Yes
Would you like to use Turbopack for `next dev`? Yes
Would you like to customize the import alias (`@/*` by default)? Yes
What import alias would you like configured? @/*

I’m using npm for this project, but you can swap to any other package manager of your choice.

Navigate to the Money-Guard directory by running cd money-guard, start the project with npm run dev and open it in your code editor.

### Step 1: Celebrate!Step 1: Celebrate!

Just one step? Yes, only one. Your Next.js project with the App Router is up and running, and you didn’t even break a sweat.

Next, we’ll set up project dependencies and define the application structure. Here’s what the final application will look like:

### Step 2: Add componentsStep 2: Add components

Now, we’ll set up some simpler parts so we can focus on the more complex tasks later.

In this section, we’ll configure Shadcn components to reduce the need for writing CSS. Run the following command to set it up:

npx shadcn@latest init -d

Then we can go ahead and add the following components to our project:

npx shadcn@latest add alert button card chart input skeleton textarea

You will notice a newly generated folder called components.

Inside this folder, create the following files:

NavItem.tsx

This is what our NavItem will look like. At this stage, you can run npm install lucide-react if it’s not already installed.

import Link from "next/link";

type NavItemProps = {
　icon: LucideIcon;
　label: string;
　href: string;
};

export const NavItem: React.FC<NavItemProps> = ({
　icon: Icon,
　label,
　href,
}) => (
　<Link
　　href={href || "/"}
　　className="flex flex-col lg:flex-row items-center justify-center lg:justify-start lg:gap-9 p-2 w-full rounded hover:text-orange-400"
　>
　　<Icon size={24} className="transition-colors duration-300" />
　　<span className="text-xs mt-1 transition-colors duration-300">{label}</span>
　</Link>
);

MobileMenu.tsx

Since our UI will be fully responsive, this is the component for our mobile menu:

import { useState } from "react";
import { Menu } from "lucide-react";
import { Home, PieChart, CreditCard, List } from "lucide-react";
import { NavItem } from "./NavItem";
export const MobileMenuToggle = () => {
　const [isMenuOpen, setIsMenuOpen] = useState(false);

　return (
　　<>
　　　<div className="lg:hidden flex items-center justify-between p-4 bg-white">
　　　　<h2 className="text-xl font-bold">MoneyGuard</h2>
　　　　<button onClick={() => setIsMenuOpen(!isMenuOpen)}>
　　　　　<Menu size={24} />
　　　　</button>
　　　</div>
　　　{/* Mobile Bottom Nav */}
　　　<div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white z-20 flex justify-around items-center h-16">
　　　　<NavItem icon={Home} label="Home" href="/" />
　　　　<NavItem icon={PieChart} label="Invest" href="/" />
　　　　<NavItem icon={CreditCard} label="Cards" href="/" />
　　　　<NavItem icon={List} label="Trans." href="/" />
　　　</div>
　　</>
　);
};

Sidebar.tsx

Next, we’ll add our sidebar:

import Image from "next/image";
import { NavItem } from "./NavItem";

export const Sidebar = () => {
　return (
　　<div className="hidden lg:flex lg:flex-col lg:w-64 bg-white p-4">
　　　<div className="mb-8">
　　　　<Image
　　　　　height={100}
　　　　　width={100}
　　　　　src="https://i.pravatar.cc/150?img=64"
　　　　　alt="UsMober"
　　　　　priority={true}
　　　　　className="rounded-full mb-2 w-20 h-20"
　　　　/>
　　　　<p className="text-sm text-gray-950">Welcome back!</p>
　　　　<h3 className="text-lg font-semibold">Adam Jacobs</h3>
　　　</div>
　　　<nav className="flex-1 space-y-2">
　　　　<NavItem icon={Home} label="Dashboard" href="/" />
　　　　<NavItem icon={PieChart} label="Investments" href="/" />
　　　　<NavItem icon={CreditCard} label="My Cards" href="/" />
　　　　<NavItem icon={List} label="Transactions" href="/" />
　　　</nav>
　　</div>
　);
};

Layout.tsx

The layout provides room for a sidebar, allowing you to easily add more features across all pages in your app if needed.

import type { Metadata } from "next";

import "./globals.css";
import { MobileMenuToggle } from "@/components/MobileMenu";
import { Sidebar } from "@/components/SideBar";

export const metadata: Metadata = {
　title: "Create Next App",
　description: "Generated by create next app",
};

export default function RootLayout({
　children,
}: Readonly<{
　children: React.ReactNode;
}>) {
　return (
　　<html lang="en">
　　　<body>
　　　　<div className="flex flex-col h-screen bg-gray-100 text-black">
　　　　　{/* Top bar for mobile */}
　　　　　<MobileMenuToggle />

　　　　　<div className="flex flex-1 overflow-hidden">
　　　　　　<Sidebar />

　　　　　　{/* Main Content */}
　　　　　　<div className="flex-1 overflow-y-auto p-4 pb-20 lg:pb-4">
　　　　　　　{children}
　　　　　　</div>
　　　　　</div>
　　　　</div>
　　　</body>
　　</html>
　);
}

page.tsx

After editing the layout to match the code above, go to the page.tsx file, delete all the existing code, replace it with ’hello world’ at the center and run your app.

export default function Home() {
　return <div>Hello</div>;
}

Error! In next.config.mjs

Oops! Sorry about the ’Invalid source’ error. To fix this issue on your browser or terminal, we need to add image domains for the avatar image we used. Here’s the error we encountered on our end:

Go ahead and edit next.config.mjs file to have the domain for our image resource as below:

/** @type {import('next').NextConfig} */
const nextConfig = {
images: {
　　domains: ['i.pravatar.cc'],
　},
};

export default nextConfig;

### Step 3: Serverless API route and integrate Nebius AI StudioStep 3: Serverless API route and integrate Nebius AI Studio

#### Setup StudioSetup Studio

Now we’re getting to the interesting part. Create an account with Nebius AI Studio to retrieve your API key — this is the only thing we will need.

As shown in the image below, you can retrieve the key from the user menu in the top-right corner. Copy it and store it in a safe place.

#### Create env.local file at the root of our projectCreate env.local file at the root of our project

Once you have your API key, add the following environment variable name:

NEBIUS_API_KEY = your_api_key

Setup the server: Inside your app folder, create a directory called API, then another one named nebius inside it and finally, a route.ts file inside the nebius directory, as shown in the tree image below:

route.ts

This is where we’ll handle incoming HTTP requests and send responses to the frontend using NextRequest and NextResponse, which you can find here.

We are also going to use the official OpenAI Typescript library for chat completions. Install it with the command npm install openai.

For this demo, we’ll use the meta-llama/Meta-Llama-3.1-70B-Instruct model. Since this is the only model in use, there’s no need to manage multiple models in the code.

#### Initialize the OpenAI client in route.tsInitialize the OpenAI client in route.ts

Now that the server route is set up and OpenAI is installed, initialize the OpenAI client in this file. This is quite simple: you’ll need the base URL for the Nebius AI Studio API and the environment variable you’ve already set:

const client = new OpenAI({
　baseURL: "https://api.studio.nebius.ai/v1/",
　apiKey: process.env.NEBIUS_API_KEY,
});

Next, define some type interfaces and types for the structure of the data handled by the API. You can preview this data in the Nebius AI Studio console. Once you’ve previewed it, include these types in your code:

type MessageRole = "system" | "user" | "assistant" | "function";

interface BaseMessage {
　role: MessageRole;
　content: string;
}

interface FunctionMessage extends BaseMessage {
　role: "function";
　name: string;
}

type Message = BaseMessage | FunctionMessage;

Finally, create the POST function that will make the API call to Nebius AI Studio. Import the necessary modules using the quick fix option.

There are five steps to writing this function.

- Define an asynchronous function that takes a NextRequest as an argument and returns a NextResponse. These are imported from “next/server” and handle the HTTP POST request to Nebius AI Studio.

export async function POST(request: NextRequest){
//All the logic goes here
return NextResponse.json(
　// Return response here and status code
　　);
}

- Next, in your logic part, extract the JSON body from the request. This will provide the messages, max_tokens and temperature fields required in our integration.

const body: {
　messages: Message[];
　max_tokens?:number;
　temperature?:number;
} = await request.json();

- Message formatting (Optional): Format the message inputs to match the required request structure. This step includes adding a name field when applicable.

const formattedMessages = body.messages.map((msg) => {
　if (msg.role === "function") {
　　return {
　　　role: msg.role,
　　　content: msg.content,
　　　name: (msg as FunctionMessage).name,
　　};
　}
　return {
　　role: msg.role,
　　content: msg.content,
　};
});

- The elephant in the room (API call): Make the API call to Nebius AI Studio. Use the formatted messages, along with the max_tokens and temperature parameters, to generate the completion request.

const completion = await client.chat.completions.create({
model: "meta-llama/Meta-Llama-3.1-70B-Instruct",
messages: formattedMessages,
max_tokens: body.max_tokens || 500,
temperature: body.temperature || 0.7,
});

- Handle the response and errors in the section labeled “Response Handling,” and use the following code as the final version. Process the output to return meaningful data to the frontend.

export async function POST(request: NextRequest) {
　const body: {
　　messages: Message[];
　　max_tokens?: number;
　　temperature?: number;
　} = await request.json();

　console.log("Received request body:", JSON.stringify(body, null, 2));

　try {
　　const formattedMessages = body.messages.map((msg) => {
　　　if (msg.role === "function") {
　　　　// Cast to FunctionMessage and ensure name is included
　　　　return {
　　　　　role: msg.role,
　　　　　content: msg.content,
　　　　　name: (msg as FunctionMessage).name,
　　　　};
　　　}

　　　return {
　　　　role: msg.role,
　　　　content: msg.content,
　　　};
　　});
　　console.log(
　　　"Formatted messages:",
　　　JSON.stringify(formattedMessages, null, 2)
　　);

　　const completion = await client.chat.completions.create({
　　　model: "meta-llama/Meta-Llama-3.1-70B-Instruct",
　　　messages: formattedMessages, // Pass formatted messages
　　　max_tokens: body.max_tokens || 500, // Increased from 100 to 500
　　　temperature: body.temperature || 0.7,
　　});

　　console.log(
　　　"Nebius AI Studio response:",
　　　JSON.stringify(completion.choices[0].message, null, 2)
　　);

　　return NextResponse.json(completion.choices[0].message);
　} catch (error) {
　　console.error("Error:", error);
　　if (error instanceof Error) {
　　　return NextResponse.json({ error: error.message }, { status: 500 });
　　}
　　return NextResponse.json(
　　　{ error: "An unknown error occurred" },
　　　{ status: 500 }
　　);
　}
}

### Step 4: Setup State Management with ZustandStep 4: Setup State Management with Zustand

In this application, we’ll create smaller components for different features. This modular approach makes global state management ideal. Since Zustand is less complex compared to Redux or useContext, we’ll only need a single file for the state.

Let’s install the Zustand library:

# NPM
npm install zustand
# Or, use any package manager of your choice.

Next, let’s define the TypeScript types representing the structure of the financial data in our application. Inside the types directory, add a file for mock data. We are using mock data in this demo to avoid the added complexity and costs associated with integrating banking APIs.

This file includes the type interfaces for Transaction and Card, along with the data and three functions that:

- 

Retrieve all the mock transactions (which can be imported anywhere in our project).

- 

Retrieve all the card data.

- 

Filter and return all transactions that are subscriptions from our financial data.

types/mockData.ts

export interface Transaction {
　id: string;
　name: string;
　mode: string;
　date: string;
　amount: number;
　isSubscription: boolean;
　type: "income" | "expense";
}

export interface Card {
　id: string;
　number: string;
　name: string;
　expiryDate: string;
}

export const mockTransactions: Transaction[] = [
　{
　　id: "1",
　　name: "Salary",
　　mode: "Bank Transfer",
　　date: "01-09-2024",
　　amount: 350000,
　　isSubscription: false,
　　type: "income",
　},
　{
　　id: "2",
　　name: "Rent",
　　mode: "Bank Transfer",
　　date: "05-09-2024",
　　amount: -30000,
　　isSubscription: true,
　　type: "expense",
　},
　{
　　id: "3",
　　name: "Groceries",
　　mode: "Credit Card",
　　date: "10-09-2024",
　　amount: -5000,
　　isSubscription: false,
　　type: "expense",
　},
];

export const mockCards: Card[] = [
　{
　　id: "1",
　　number: "12XX XXXX XXXX XX66",
　　name: "Adam Jacobs",
　　expiryDate: "04/28",
　},
　{
　　id: "2",
　　number: "91XX XXXX XXXX XX46",
　　name: "Adam Jacobs",
　　expiryDate: "04/30",
　},
];

export function getTransactions(): Transaction[] {
　return mockTransactions;
}

export function getCards(): Card[] {
　return mockCards;
}

export function getSubscriptions(): Transaction[] {
　return mockTransactions.filter((transaction) => transaction.isSubscription);
}

types/financialTypes.ts

Now, create a directory named types in the root of our application and a file named financialTypes.ts.

This section contains the types for all the stateful logic in our application. Let’s break them down bit by bit:

- 

ButtonName type: Represents the different button options users can interact with.

- 

FinancialTotals: Holds computed totals like balance, income, and expense, calculated on the client side.

- 

FinancialState: Contains the initial state and functions for managing all app logic.

// types/financialTypes.ts

import { Card, Transaction } from "@/lib/mockData";

export type ButtonName = "subscriptions" | "bills" | "buyOrRent" | "userInput";

export interface FinancialTotals {
　balance: number;
　income: number;
　expense: number;
　savedPercentage: number;
　incomeChangePercentage: number;
　expenseChangePercentage: number;
}

export type ResponseData = {
　markdownText: string;
};

export interface FinancialState {
　loading: boolean;
　generating: boolean;
　activeButton: ButtonName | null;
　parsedResponse: ResponseData | null;
　displayText: string;
　textIndex: number;
　transactions: Transaction[];
　subscriptions: Transaction[];
　cards: Card[];
　setLoading: (loading: boolean) => void;
　setGenerating: (generating: boolean) => void;
　setActiveButton: (activeButton: ButtonName | null) => void;
　setParsedResponse: (parsedResponse: ResponseData | null) => void;
　setDisplayText: (displayText: string) => void;
　setTextIndex: (textIndex: number) => void;
　handleButtonClick: (buttonName: ButtonName, userInput?: string) => void;
　fetchTransactions: () => void;
　fetchSubscriptions: () => void;
　fetchCards: () => void;
　calculateTotals: () => void;
}

utils/financilUtils.ts

One more functionality is a utility that will have the static suggestions for our prompts as shown below:

import { ButtonName, ResponseData } from "@/types/financialTypes";

export const generatePrompt = (
　buttonName: ButtonName,
　userInput?: string
): string => {
　switch (buttonName) {
　　case "subscriptions":
　　　return "Generate a list of active subscriptions with their costs and a summary of total monthly cost based on the provided transaction data.";
　　case "bills":
　　　return "Generate a list of upcoming bills with their amounts and due dates, and a summary of total amount due based on the provided transaction data.";
　　case "buyOrRent":
　　　return "Provide an analysis on whether to buy or rent a home, considering the user’s current financial situation based on their transaction history.";
　　case "userInput":
　　　return userInput || "";
　　default:
　　　return "";
　}
};

export const parseResponse = (responseText: string): ResponseData => {
　console.log(responseText);
　return {
　　markdownText: responseText,
　};
};

store/financialApi.ts

This file is responsible for hitting the endpoint we created at api/nebius and it has been modified to include transaction, card and subscription data from our mock data. The responses are also sent in Markdown format.

import { Card, Transaction } from "@/lib/mockData";
import { ButtonName } from "@/types/financialTypes";
import { generatePrompt } from "@/utils/financialUtils";

export const fetchFinancialData = async (
　buttonName: ButtonName,
　userInput: string | undefined,
　transactions: Transaction[],
　subscriptions: Transaction[],
　cards: Card[]
) => {
　const prompt = generatePrompt(buttonName, userInput);

　const response = await fetch("/api/nebius", {
　　method: "POST",
　　headers: { "Content-Type": "application/json" },
　　body: JSON.stringify({
　　　messages: [
　　　　{
　　　　　role: "system",
　　　　　content:
　　　　　　"You are a financial assistant. Respond in markdown format and us dollars. Use the provided transaction data to inform your responses.",
　　　　},
　　　　{
　　　　　role: "user",
　　　　　content: `Here is the user’s transaction data:\n${JSON.stringify({
　　　　　　transactions,
　　　　　　subscriptions,
　　　　　　cards,
　　　　　})}\n\n${prompt}`,
　　　　},
　　　],
　　　max_tokens: 500,
　　　temperature: 0.7,
　　}),
　});

　if (!response.ok) {
　　throw new Error("API request failed");
　}

　return await response.json();
};

store/useFinancialStore.ts

This will be our central store. It’s essentially a hook that we can use anywhere in our application.

The hook contains loading and text generation states, as well as UI rendering states (buttons, responses and parsed text), computations for our financial data and data-fetching logic. All functions and variables are named descriptively, so you won’t have any trouble understanding them.

Since we are using TypeScript, all modular imports will be automatically recognized.

export const useFinancialStore = create<FinancialState & FinancialTotals>(
　(set, get) => ({
　　loading: false,
　　generating: false,
　　activeButton: null,
　　parsedResponse: null,
　　displayText: "",
　　textIndex: 0,
　　transactions: [],
　　subscriptions: [],
　　cards: [] as Card[],
　　balance: 0,
　　income: 0,
　　expense: 0,
　　savedPercentage: 0,
　　incomeChangePercentage: 0,
　　expenseChangePercentage: 0,
　　setLoading: (loading) => set({ loading }),
　　setGenerating: (generating) => set({ generating }),
　　setActiveButton: (activeButton) => set({ activeButton }),
　　setParsedResponse: (parsedResponse) => set({ parsedResponse }),
　　setDisplayText: (displayText) => set({ displayText }),
　　setTextIndex: (textIndex) => set({ textIndex }),
　　calculateTotals: () => {
　　　const transactions = get().transactions;
　　　const income = transactions
　　　　.filter((t) => t.type === "income")
　　　　.reduce((sum, t) => sum + t.amount, 0);
　　　const expense = Math.abs(
　　　　transactions
　　　　　.filter((t) => t.type === "expense")
　　　　　.reduce((sum, t) => sum + t.amount, 0)
　　　);
　　　const balance = income - expense;

　　　// These percentages should ideally be calculated by comparing with previous period data
　　　// For now, we’ll use mock values
　　　const savedPercentage = 5.6;
　　　const incomeChangePercentage = 3.8;
　　　const expenseChangePercentage = -1.8;

　　　set({
　　　　balance,
　　　　income,
　　　　expense,
　　　　savedPercentage,
　　　　incomeChangePercentage,
　　　　expenseChangePercentage,
　　　});
　　},
　　fetchTransactions: () => {
　　　const transactions = getTransactions();
　　　set({ transactions }, false);
　　　get().calculateTotals();
　　},
　　fetchSubscriptions: () => {
　　　const subscriptions = getSubscriptions();
　　　set({ subscriptions });
　　},
　　fetchCards: () => {
　　　const cards = getCards();
　　　set({ cards });
　　},
　　handleButtonClick: async (buttonName: ButtonName, userInput?: string) => {
　　　set({
　　　　loading: true,
　　　　activeButton: buttonName,
　　　　parsedResponse: null,
　　　　displayText: "",
　　　　textIndex: 0,
　　　　generating: false,
　　　});

　　　try {
　　　　const transactions = getTransactions();
　　　　const subscriptions = getSubscriptions();
　　　　const cards = getCards();
　　　　const data = await fetchFinancialData(
　　　　　buttonName,
　　　　　userInput,
　　　　　transactions,
　　　　　subscriptions,
　　　　　cards
　　　　);
　　　　const parsedResponse = parseResponse(data.content);
　　　　const displayText = parsedResponse.markdownText;

　　　　set({
　　　　　loading: false,
　　　　　generating: false,
　　　　　parsedResponse,
　　　　　displayText,
　　　　});
　　　} catch (error) {
　　　　console.error("Error:", error);
　　　　set({
　　　　　loading: false,
　　　　　generating: false,
　　　　　parsedResponse: {
　　　　　　markdownText: `An error occurred while fetching data. Please check the console for more details.`,
　　　　　},
　　　　　displayText:
　　　　　　"An error occurred while fetching data. Please check the console for more details.",
　　　　});
　　　}
　　},
　})
);

### Step 5: Complete our final features in the UIStep 5: Complete our final features in the UI

As shown in the image above, the features will include ActionButtons, FinancialSummary, MarkdownRenderer, PromptInput, QueryDisplay, RecentTransactions, TotalBalance and YourCards.

Let’s break down the features one by one:

- components/features/FinancialSummary.tsx. In this section, we’ll have the financial summary that displays the computed totals obtained from the store using the hooks that have already been provided.

"use client";
import { useFinancialStore } from "@/store/useNebius";
import React, { useEffect } from "react";

const FinancialSummary = () => {
　const {
　　balance,
　　income,
　　expense,
　　savedPercentage,
　　incomeChangePercentage,
　　expenseChangePercentage,
　　fetchTransactions,
　} = useFinancialStore();

　useEffect(() => {
　　fetchTransactions();
　}, [fetchTransactions]);

　return (
　　<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
　　　<div className="bg-white p-4 rounded shadow-md">
　　　　<h4 className="text-sm text-gray-950 mb-2">Total Balance</h4>
　　　　<p className="text-3xl font-bold">
　　　　　{balance.toLocaleString("en-US", {
　　　　　　style: "currency",
　　　　　　currency: "USD",
　　　　　})}
　　　　</p>
　　　　<p className="text-green-500">↑ {savedPercentage.toFixed(2)}% Saved</p>
　　　</div>
　　　<div className="bg-white p-4 shadow-md rounded">
　　　　<h4 className="text-sm text-gray-950 mb-2">Total Income</h4>
　　　　<p className="text-3xl font-bold">
　　　　　{income.toLocaleString("en-US", {
　　　　　　style: "currency",
　　　　　　currency: "USD",
　　　　　})}
　　　　</p>
　　　　<span className="text-green-950 text-sm">
　　　　　↑ {incomeChangePercentage.toFixed(2)}%
　　　　</span>
　　　</div>
　　　<div className="bg-white p-4 rounded shadow-md border">
　　　　<h4 className="text-sm text-gray-950 mb-2">Total Expense</h4>
　　　　<p className="text-3xl font-bold">
　　　　　{expense.toLocaleString("en-US", {
　　　　　　style: "currency",
　　　　　　currency: "USD",
　　　　　})}
　　　　</p>
　　　　<span className="text-red-950 text-sm">
　　　　　↓ {expenseChangePercentage.toFixed(2)}%
　　　　</span>
　　　</div>
　　</div>
　);
};

export default FinancialSummary;

- components/features/MakrdownRenderer.ts. Since we’ll receive all our responses in Markdown format, we need to format it beautifully. We will also need to install react-markdown (npm i react-markdown@8.0.6), as our prompts will be returned in Markdown format from the OpenAI models. These are the formatted styles for our response component:

import React from "react";
import ReactMarkdown from "react-markdown";

type MarkdownRendererProps = {
　content: string;
};

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
　content,
}) => {
　return (
　　<div className="prose prose-slate max-w-none">
　　 <ReactMarkdown
　　 components={{
　　 h1: ({ ...props }) => (
　　 <h1 className="text-2xl font-bold my-2" {...props} />
　　 ),
　　 h2: ({ ...props }) => (
　　 <h2 className="text-xl font-bold my-2" {...props} />
　　 ),
　　 h3: ({ ...props }) => (
　　 <h3 className="text-lg font-semibold my-2" {...props} />
　　 ),
　　 p: ({ ...props }) => <p className="my-2" {...props} />,
　　 ul: ({ ...props }) => (
　　 <ul className="list-disc pl-6 my-2" {...props} />
　　 ),
　　 ol: ({ ...props }) => (
　　 <ol className="list-decimal pl-6 my-2" {...props} />
　　 ),
　　 li: ({ ...props }) => <li className="my-1" {...props} />,
　　 table: ({ ...props }) => (
　　 <div className="overflow-x-auto my-4">
　　 <table
　　 className="min-w-full table-auto border-collapse border border-gray-300"
　　 {...props}
　　 />
　　 </div>
　　 ),
　　 thead: ({ ...props }) => <thead className="bg-gray-100" {...props} />,
　　 th: ({ ...props }) => (
　　 <th
　　 className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border border-gray-300"
　　 {...props}
　　 />
　　 ),
　　 td: ({ ...props }) => (
　　 <td
　　 className="px-6 py-4 whitespace-nowrap border border-gray-300"
　　 {...props}
　　 />
　　 ),
　　 tr: ({ ...props }) => <tr className="even:bg-gray-50" {...props} />,
　　 strong: ({ ...props }) => <strong className="font-bold" {...props} />,
　　 em: ({ ...props }) => <em className="italic" {...props} />,
　　 blockquote: ({ ...props }) => (
　　 <blockquote
　　 className="border-l-4 border-gray-200 pl-4 my-4 italic"
　　 {...props}
　　 />
　　 ),
　　 code: ({ ...props }) => (
　　 <code
　　 className="block bg-gray-100 p-4 rounded my-4 overflow-x-auto"
　　 {...props}
　　 />
　　 ),
　　 }}
　　 >
　　 {content}
　　 </ReactMarkdown>
　　</div>
　);
};

- components/features/PromptInput.tsx:

const MoneyGuardAssistant = () => {
　const [query, setQuery] = useState("What is my most expensive transaction?");
　const { handleButtonClick, loading } = useFinancialStore();

　const moneyguardPrompts = [
　　{ name: "subscriptions", prompt: "List my subscriptions" },
　　{ name: "bills", prompt: "More on my bills..." },
　　{ name: "buyOrRent", prompt: "Should I buy or rent?" },
　];

　const onSubmit = (e: FormEvent) => {
　　e.preventDefault();
　　if (query.trim()) {
　　　handleButtonClick("userInput", query);
　　}
　};

　return (
　　<div className="flex w-full mb-4 flex-col gap-2">
　　　<div className="bg-white border-gray-300 py-4 dark:border-orange-700 dark:bg-orange-900 rounded-md border">
　　　　<ul className="text-orange-500 dark:text-orange-200 text-sm">
　　　　　{moneyguardPrompts.map(({ name, prompt }, index) => (
　　　　　　<li
　　　　　　　key={index}
　　　　　　　className="cursor-pointer px-4 py-1 hover:bg-orange-100 dark:hover:bg-orange-800"
　　　　　　>
　　　　　　　<button
　　　　　　　　className="text-left w-full"
　　　　　　　　onClick={() => handleButtonClick(name as ButtonName)}
　　　　　　　>
　　　　　　　　{prompt}
　　　　　　　</button>
　　　　　　</li>
　　　　　))}
　　　　</ul>
　　　</div>
　　　<form onSubmit={onSubmit} className="relative w-full">
　　　　<label htmlFor="aiPrompt" className="sr-only">
　　　　　ai prompt
　　　　</label>
　　　　<svg
　　　　　xmlns="http://www.w3.org/2000/svg"
　　　　　viewBox="0 0 16 16"
　　　　　aria-hidden="true"
　　　　　className="absolute left-3 top-1/2 size-4 -translate-y-1/2 fill-orange-600 dark:fill-orange-400"
　　　　>
　　　　　<path
　　　　　　fillRule="evenodd"
　　　　　　d="M5 4a.75.75 0 0 1 .738.616l.252 1.388A1.25 1.25 0 0 0 6.996 7.01l1.388.252a.75.75 0 0 1 0 1.476l-1.388.252A1.25 1.25 0 0 0 5.99 9.996l-.252 1.388a.75.75 0 0 1-1.476 0L4.01 9.996A1.25 1.25 0 0 0 3.004 8.99l-1.388-.252a.75.75 0 0 1 0-1.476l1.388-.252A1.25 1.25 0 0 0 4.01 6.004l.252-1.388A.75.75 0 0 1 5 4ZM12 1a.75.75 0 0 1 .721.544l.195.682c.118.415.443.74.858.858l.682.195a.75.75 0 0 1 0 1.442l-.682.195a1.25 1.25 0 0 0-.858.858l-.195.682a.75.75 0 0 1-1.442 0l-.195-.682a1.25 1.25 0 0 0-.858-.858l-.682-.195a.75.75 0 0 1 0-1.442l.682-.195a1.25 1.25 0 0 0 .858-.858l.195-.682A.75.75 0 0 1 12 1ZM10 11a.75.75 0 0 1 .728.568.968.968 0 0 0 .704.704.75.75 0 0 1 0 1.456.968.968 0 0 0-.704.704.75.75 0 0 1-1.456 0 .968.968 0 0 0-.704-.704.75.75 0 0 1 0-1.456.968.968 0 0 0 .704-.704A.75.75 0 0 1 10 11Z"
　　　　　　clipRule="evenodd"
　　　　　/>
　　　　</svg>
　　　　<input
　　　　　id="aiPrompt"
　　　　　type="text"
　　　　　className="w-full border-outline bg-orange-50 border border-orange-300 rounded-md px-2 py-2 pl-10 pr-24 text-sm text-orange-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500 disabled:cursor-not-allowed disabled:opacity-75 dark:border-orange-700 dark:bg-orange-900/50 dark:text-orange-200 dark:focus-visible:outline-orange-400"
　　　　　value={query}
　　　　　onChange={(e) => setQuery(e.target.value)}
　　　　　name="prompt"
　　　　　placeholder="Ask AI ..."
　　　　　disabled={loading}
　　　　/>
　　　　<button
　　　　　type="submit"
　　　　　className="absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer bg-orange-500 hover:bg-orange-700 text-white font-bold rounded-md px-2 py-1 text-xs tracking-wide transition focus:outline-none focus:ring-2 focus:ring-orange-600 focus:ring-opacity-50 active:bg-orange-800"
　　　　　disabled={loading}
　　　　>
　　　　　{loading ? <Loader2Icon className="animate-spin" /> : "Generate"}
　　　　</button>
　　　</form>
　　</div>
　);
};

- features/QueryDisplay.tsx. We will now import our markdown renderer here. In this component, we will manage the loading state with a beautiful skeleton to indicate to the user that AI generation is in progress.

export const ResponseDisplay: React.FC = () => {
　const { loading, parsedResponse } = useFinancialStore();

　const getContent = () => {
　　if (!parsedResponse) return "";

　　try {
　　　const response = parsedResponse as MarkdownResponse;
　　　return response.markdownText || "";
　　} catch (error) {
　　　console.error("Error parsing response:", error);
　　　return "";
　　}
　};

　if (!loading && !parsedResponse) return null;

　return (
　　<Card className="w-full">
　　　<CardHeader>
　　　　<CardTitle>{loading ? "Loading..." : "Response"}</CardTitle>
　　　</CardHeader>
　　　<CardContent>
　　　　{loading ? (
　　　　　<div className="space-y-2">
　　　　　　<Skeleton className="h-4 w-full" />
　　　　　　<Skeleton className="h-4 w-full" />
　　　　　　<Skeleton className="h-4 w-3/4" />
　　　　　</div>
　　　　) : (
　　　　　<MarkdownRenderer content={getContent()} />
　　　　)}
　　　</CardContent>
　　</Card>
　);
};

- features/RecentTransactions. This component will contain all the financial transaction data. We have two functions that format the Amount to local currency and format the date to the normal time format.

export const RecentTransactions = () => {
　const { fetchTransactions, transactions } = useFinancialStore();

　useEffect(() => {
　　fetchTransactions();
　}, [fetchTransactions]);

　const formatAmount = (amount: number) => {
　　const absAmount = Math.abs(amount);
　　const formattedAmount = new Intl.NumberFormat("en-US", {
　　　style: "currency",
　　　currency: "USD",
　　　minimumFractionDigits: 0,
　　}).format(absAmount);
　　return amount < 0 ? `-formattedAmount‘:‘+{formattedAmount}` : `+formattedAmount‘:‘+{formattedAmount}`;
　};

　const formatDate = (dateString: string) => {
　　const date = new Date(dateString);
　　return date
　　　.toLocaleDateString("en-US", {
　　　　day: "2-digit",
　　　　month: "2-digit",
　　　　year: "numeric",
　　　})
　　　.replace(/\//g, "-");
　};

　return (
　　<div className="bg-white shadow-md p-4 w-full rounded">
　　　<h4 className="text-lg font-semibold mb-4">Recent Transactions</h4>
　　　<div className="overflow-x-auto">
　　　　<table className="w-full">
　　　　　<thead>
　　　　　　<tr className="text-gray-950 text-sm">
　　　　　　　<th className="text-left pb-2">Name</th>
　　　　　　　<th className="text-left pb-2">Mode</th>
　　　　　　　<th className="text-left pb-2">Date</th>
　　　　　　　<th className="text-right pb-2">Amount</th>
　　　　　　</tr>
　　　　　</thead>
　　　　　<tbody>
　　　　　　{transactions.map((transaction) => (
　　　　　　　<tr key={transaction.id}>
　　　　　　　　<td className="py-2">{transaction.name}</td>
　　　　　　　　<td>{transaction.mode}</td>
　　　　　　　　<td>{formatDate(transaction.date)}</td>
　　　　　　　　<td
　　　　　　　　　className={`text-right ${
　　　　　　　　　　transaction.amount < 0 ? "text-red-800" : "text-green-800"
　　　　　　　　　}`}
　　　　　　　　>
　　　　　　　　　{formatAmount(transaction.amount)}
　　　　　　　　</td>
　　　　　　　</tr>
　　　　　　))}
　　　　　</tbody>
　　　　</table>
　　　</div>
　　</div>
　);
};

- components/features/YourCards.tsx. This component fetches our cards data and displays them. We map through the data and extract the number, name and date to display them dynamically.

"use client";
import { useFinancialStore } from "@/store/useNebius";
import { useEffect } from "react";

export const YourCard = () => {
　const { cards, fetchCards } = useFinancialStore();

　useEffect(() => {
　　fetchCards();
　}, [fetchCards]);

　return (
　　<div className="bg-white shadow-md p-4 w-full rounded">
　　　<h4 className="text-lg font-semibold mb-4">Your Cards</h4>
　　　<div className="space-y-4">
　　　　{cards.map(({ number, name, expiryDate, id }) => (
　　　　　<div className="bg-gray-100 p-4 rounded" key={id}>
　　　　　　<p className="text-sm mb-1">{number}</p>
　　　　　　<p className="text-sm">{name}</p>
　　　　　　<p className="text-sm text-gray-950">{expiryDate}</p>
　　　　　</div>
　　　　))}
　　　</div>
　　</div>
　);
};

### Final Step: Update Features in page.tsx and test our applicationFinal Step: Update Features in page.tsx and test our application

Good news: in this step, we’re simply organizing all the components created earlier into the main page of the application.

Sidenote: We’ve already written the code for all these components, so you don’t need to stress about this part. We’re only importing all of the other written components, since logic was handled separately. This ensures we have simple and organized code.

Here’s page.tsx:

import React from "react";

import { RecentTransactions } from "@/components/features/RecentTransactions";
import { YourCard } from "@/components/features/YourCards";

import { ResponseDisplay } from "@/components/features/QueryDisplay";

import FinancialSummary from "@/components/features/FinancialSummary";
import MoneyGuardAssistant from "@/components/features/PromptInput";

const FinancialDashboard = async () => {
　return (
　　<>
　　　<div className="flex-1 overflow-y-auto p-4 pb-20 lg:pb-4">
　　　　<div className="bg-white p-4 rounded mb-4">
　　　　　<MoneyGuardAssistant />
　　　　　<ResponseDisplay />
　　　　</div>
　　　　<FinancialSummary />
　　　　<div className="flex flex-col lg:flex-row w-full justify-between gap-3">
　　　　　<RecentTransactions />
　　　　　<YourCard />
　　　　</div>
　　　</div>
　　</>
　);
};

export default FinancialDashboard;

Now, when you run the application, you’re supposed to see the final result, you can check the live project here.

### Closing thoughtsClosing thoughts

Building an AI-powered app on Nebius AI Studio is straightforward and doesn’t require specialized knowledge. The AI landscape offers tons of possibilities, making it easy for anyone to create applications reflecting their ideas. Get started with Nebius AI Studio today.

This article introduced the foundational elements of a full-featured financial application. If you wish to expand its functionality, consider:

- 

Filter and sort: Implement functionality to filter transactions by type (currently achievable through AI queries).

- 

Add or edit subscriptions: Enable users to add or modify their subscriptions manually.

- 

Integrate real banking APIs: Explore the integration of real banking APIs, as this demo project uses mock data.

Next.js has simplified the development process for frontend developers, highlighting the advantages of JavaScript in building and deploying applications.

## Explore Nebius Token Factory

Sign up​
Docs and support​

## Explore Nebius

Sign up​
Docs​

Nebius team

## See also

### 

How to choose between large and small AI models: A cost-benefit analysis

This blog post will guide you through the differences, use cases and cost-benefit analysis of different AI models, especially in the context of inference.

October 28, 2024
7 mins to read

### 

How to run Meta Llama 3.1 405B with Nebius AI Studio API

Discover how Nebius AI Studio enables you to integrate the famous Llama 3.1 405B large language model in your applications.

October 17, 2024
8 mins to read

### 

Leveraging training and search for better software engineering agents

In this blog post, we’ll share some of our recent findings on how search can enhance agentic systems for software engineering. Specifically, we’ll demonstrate how we’ve built an SWE-agent-based system that exclusively uses open-weight LLMs and achieves a 40.6% resolved rate on SWE-bench Verified.

November 15, 2024
10 mins to read

Sign in to save this post
Sign In
