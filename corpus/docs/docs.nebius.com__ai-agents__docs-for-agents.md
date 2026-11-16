# Using docs with AI

Source: https://docs.nebius.com/ai-agents/docs-for-agents

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Using docs with AI

Nebius documentation includes AI-ready formats and integrations that help you work with AI agents and coding assistants.

## How to read pages in Markdown

Agents don't need to parse the HTML version of this documentation. To read any documentation page in Markdown:

* Append `.md` to the page URL. For example, [docs.nebius.com/serverless/overview.md](https://docs.nebius.com/serverless/overview.md).
* Use the page menu on any page to copy or view the page content in Markdown.
* In scripts, send an `Accept: text/markdown` header with a page URL without changing its path:

  ```bash theme={null}
  curl -H "Accept: text/markdown" https://docs.nebius.com/serverless/overview
  ```

## llms.txt and llms-full.txt

Give your AI agent or coding assistant context on Nebius AI Cloud and how it works with these files when it needs documentation context beyond a single page:

| Resource | Best for | Use it when you want to |
| - | - | - |
| [llms.txt](https://docs.nebius.com/llms.txt) | Introduction to Nebius AI Cloud and quick orientation | Get your agent started with the right Nebius product or AI Cloud service for your workload |
| [llms-full.txt](https://docs.nebius.com/llms-full.txt) | Broad documentation context | Answer questions that span multiple services, provide a larger documentation snapshot to an AI tool, or compare concepts across different parts of the platform |

## Docs MCP server

Nebius AI Cloud documentation hosts its own Model Context Protocol (MCP) server that lets your AI tool search and read the documentation. The server is available at `https://docs.nebius.com/mcp` and doesn't require authentication. This server differs from the [Nebius MCP server](https://docs.nebius.com/ai-agents/mcp-server.md), which looks up CLI help and runs CLI commands. To let your agent also manage your resources, [connect it to Nebius AI Cloud](https://docs.nebius.com/ai-agents/connect.md).

1. To add the docs MCP server to your AI tool:

   > [tab] Claude Code
   >
   > In your terminal, run:
   >
   > ```bash theme={null}
   > claude mcp add --transport http --scope user nebius-docs https://docs.nebius.com/mcp
   > ```

   > [tab] Codex
   >
   > In your terminal, run:
   >
   > ```bash theme={null}
   > codex mcp add nebius-docs --url https://docs.nebius.com/mcp
   > ```

   > [tab] Cursor
   >
   > Add the server to the `mcpServers` object in `~/.cursor/mcp.json`:
   >
   > ```json theme={null}
   > {
   >   "mcpServers": {
   >     "nebius-docs": {
   >       "url": "https://docs.nebius.com/mcp"
   >     }
   >   }
   > }
   > ```

   > [tab] VS Code
   >
   > In the Command Palette, run **MCP: Add Server**, select **HTTP**, and enter `https://docs.nebius.com/mcp`.

   > [tab] Claude
   >
   > 1. In Claude, go to **Settings** → **Connectors** and click **Add custom connector**.
   > 2. Enter `nebius-docs` as the name and `https://docs.nebius.com/mcp` as the URL, then click **Add**.
   > 3. In a chat, click **+** and turn on the `nebius-docs` connector.

   > [tab] Other agents
   >
   > In the agent's MCP settings, add a remote HTTP server with the `https://docs.nebius.com/mcp` URL.

2. To test the docs MCP server, start a new agent session and ask a question about Nebius AI Cloud:

   ```markdown wrap theme={null}
   Using the Nebius AI Cloud docs, how do I enable InfiniBand for VMs with GPUs?
   ```

> [!TIP]
>
> You can use the docs MCP tools as HTTP API endpoints directly via curl, for example, from a script. See [llms.txt](https://docs.nebius.com/llms.txt).
