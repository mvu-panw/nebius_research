# Using docs with AI

Source: https://docs.nebius.com/docs-ai

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Using docs with AI

Nebius documentation includes AI-ready formats and integrations that help you work with AI agents and coding assistants.

## Markdown pages

Agents don't need to parse the HTML version of this documentation. All documentation pages are available as Markdown:

* Append `.md` to the page URL. For example, [https://docs.nebius.com/serverless/overview.md](https://docs.nebius.com/serverless/overview.md).
* Use the menu in the top-right corner of any page to copy or view the page content in Markdown.
* Send an `Accept: text/markdown` header.
  This is useful when a tool or script already requests the HTML page URL, but you want the response as Markdown without changing the path.
  ```bash theme={null}
  curl -H "Accept: text/markdown" https://docs.nebius.com/serverless/overview
  ```

## Use llms.txt and llms-full.txt

Give your AI agent or coding assistant context on Nebius AI Cloud and how it works with these files when it needs documentation context beyond a single page:

| Resource | Best for | Use it when you want to |
| - | - | - |
| [llms.txt](https://docs.nebius.com/llms.txt) | A lightweight documentation index | Discover relevant pages, route an agent to specific documents or avoid loading more context than necessary |
| [llms-full.txt](https://docs.nebius.com/llms-full.txt) | Broad documentation context | Answer questions that span multiple services, provide a larger documentation snapshot to an AI tool or compare concepts across different parts of the platform |

## Docs Model Context Protocol server

The Nebius docs Model Context Protocol (MCP) server gives any [MCP](https://modelcontextprotocol.io/)-compatible AI tool a direct connection to the Nebius documentation. This is useful when you want your AI tool to search the current documentation and retrieve relevant pages while you work.

> [!TIP]
>
> The Nebius docs MCP server provides documentation search only. It doesn't execute Nebius CLI commands or act on your resources. To work with the Nebius CLI from an AI agent, see [nebius/mcp-server](https://github.com/nebius/mcp-server).

### URL-based connection

If your client supports remote MCP servers, paste the server URL into its connector settings.

```text theme={null}
https://docs.nebius.com/mcp
```

### Direct connectors

Our documentation pages include direct connectors in the `Copy page` menu in the top-right corner. You can use the menu to configure the MCP directly in VS Code or Claude.

### File-based configuration

If your client uses an `mcp.json` or equivalent configuration file, update it to connect to the hosted Nebius docs MCP server in one of the following ways:

**VS Code**

```json theme={null}
{
  "servers": {
    "nebius-docs": {
      "url": "https://docs.nebius.com/mcp"
    }
  }
}
```

**Cursor and other clients**

```json theme={null}
{
  "mcpServers": {
    "nebius-docs": {
      "url": "https://docs.nebius.com/mcp"
    }
  }
}
```

Most clients support an entry like the example above. If yours doesn't, check the client's documentation for the exact configuration wrapper.
