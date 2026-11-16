# Nebius MCP server

Source: https://docs.nebius.com/ai-agents/mcp-server

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius MCP server

Use the Nebius Model Context Protocol (MCP) server to let a coding agent look up Nebius AI Cloud CLI help and run CLI commands with your CLI profile.

For the list of tools and the source code, see the [nebius/mcp-server](https://github.com/nebius/mcp-server) repository on GitHub:

The Nebius MCP server differs from the [docs MCP server](https://docs.nebius.com/ai-agents/docs-for-agents.md#docs-mcp-server), which only searches this documentation.

The Nebius MCP server is [in preview](https://docs.nebius.com/overview/services.md#service-and-application-stages).

## Prerequisites

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. [Install Python 3.13](https://www.python.org/downloads/) or later.
3. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

## How to install and update the Nebius MCP server

To install the server together with the CLI and agent skills, follow [How to connect your AI agent to Nebius AI Cloud](https://docs.nebius.com/ai-agents/connect.md).

To add the server to an agent manually, see [AGENT\_SETUP.md](https://github.com/nebius/mcp-server/blob/main/AGENT_SETUP.md) on GitHub.

The agent automatically updates the MCP server to the latest version each time the agent starts.

## Security recommendations

* Run the agent with a CLI profile that has only the roles your task needs. The agent acts with the [roles](https://docs.nebius.com/iam/authorization/roles.md) of the account in your CLI profile. [Set up a CLI profile for a service account](https://docs.nebius.com/cli/configure.md#how-to-set-up-the-cli-for-a-service-account) with limited roles and ask the agent to use this profile.
* Keep safe mode on. Safe mode is on unless you set the `SAFE_MODE` environment variable to `false` for the server.
* Check each command before you approve it. When the agent asks for permission to use the `nebius_cli_execute` tool, approve each command separately. The server blocks only some commands:

  * It always blocks the `nebius iam get-access-token` command and the `static-key` and `auth-public-key` commands.
  * In safe mode, it also blocks commands that contain `update`, `delete`, `purge`, or `deactivate`.
  * It runs all other commands, including commands that create, start, or stop resources and commands that read secrets.

The server checks only the commands that the agent runs through it. For commands that the agent runs in the terminal, see [Nebius AI Cloud agent skills](https://docs.nebius.com/ai-agents/skills.md#security-recommendations).

## How to report a problem

To report a problem with the server, [open an issue](https://github.com/nebius/mcp-server/issues/new) in the repository. If the server runs a command that it should block or exposes credentials, [report a vulnerability](https://github.com/nebius/mcp-server/security/advisories/new) instead of opening a public issue.
