# How to connect your AI agent to Nebius AI Cloud

Source: https://docs.nebius.com/ai-agents/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to connect your AI agent to Nebius AI Cloud

You can work with Nebius AI Cloud by using a coding agent. Once you connect the agent, it can check your resources and create new ones with your confirmation. The steps on this page install three components that the agent uses:

* [Nebius AI Cloud CLI](https://docs.nebius.com/cli.md): Manages your resources with the configured CLI profile.
* [Nebius MCP server](https://docs.nebius.com/ai-agents/mcp-server.md): Gives the agent tools to find and run CLI commands.
* [Agent skills](https://docs.nebius.com/ai-agents/skills.md): Give the agent procedures for common tasks.

## Prerequisites

1. Use a coding agent that supports local MCP servers and the [Agent Skills](https://agentskills.io) standard.
2. [Sign up for Nebius AI Cloud](https://docs.nebius.com/signup-billing/sign-up.md).
3. [Set up billing](https://docs.nebius.com/signup-billing/sign-up.md#set-up-billing) to let the agent create resources.
4. [Install Python 3.13](https://www.python.org/downloads/) or later for the local MCP server to work.
5. [Install Node.js 22.20](https://nodejs.org/en/download) or later to install the skills in Cursor and other agents.

## Steps

1. In your coding agent, send the following setup prompt:

   ```markdown wrap theme={null}
   Read `https://github.com/nebius/mcp-server/blob/main/AGENT_SETUP.md` and follow all its steps to set up the Nebius AI Cloud CLI and the Nebius MCP server for this agent.
   ```

   The agent checks your environment, installs [uv](https://docs.astral.sh/uv/getting-started/installation/) and the Nebius AI Cloud CLI if they're missing, and adds the Nebius MCP server to its configuration. If you don't have a CLI profile yet, the agent asks you to create one with `nebius profile create`.

2. Install the [skills](https://docs.nebius.com/ai-agents/skills.md) and restart the agent:

   > [tab] Claude Code
   >
   > 1. Add the Nebius plugin marketplace:
   >
   >    ```bash theme={null}
   >    claude plugin marketplace add nebius/skills
   >    ```
   >
   > 2. Install the `nebius-cloud` plugin:
   >
   >    ```bash theme={null}
   >    claude plugin install nebius-cloud@nebius
   >    ```
   >
   > 3. Restart Claude Code, so that it loads the MCP server and the skills.

   > [tab] Codex
   >
   > 1. Add the Nebius plugin marketplace:
   >
   >    ```bash theme={null}
   >    codex plugin marketplace add nebius/skills
   >    ```
   >
   > 2. Restart Codex.
   >
   > 3. Run `/plugins`, then install and turn on the `nebius-cloud` plugin.
   >
   > 4. Restart Codex, so that it loads the MCP server and the skills.

   > [tab] Cursor
   >
   > 1. Install the skills:
   >
   >    ```bash theme={null}
   >    npx skills add nebius/skills -g -a cursor
   >    ```
   >
   > 2. Restart Cursor, so that it loads the MCP server and the skills.

   > [tab] Other agents
   >
   > 1. If your agent supports [Agent Skills](https://agentskills.io), run:
   >
   >    ```bash theme={null}
   >    npx skills add nebius/skills
   >    ```
   >
   > 2. Restart the agent, so that it loads the MCP server and the skills.

3. Check that the agent has loaded the MCP server and the skills:

   > [tab] Claude Code
   >
   > In your terminal:
   >
   > * Run `claude mcp list` and check that the list includes the `nebius` server.
   > * Run `claude plugin list` and check that `nebius-cloud@nebius` is enabled.

   > [tab] Codex
   >
   > * In your terminal, run `codex mcp list` and check that the list includes the `nebius` server.
   > * In Codex, run `/plugins` and check that the `nebius-cloud` plugin is installed and turned on.

   > [tab] Cursor
   >
   > In Cursor, open **Customize** in the sidebar:
   >
   > * Check that the `nebius` MCP server is listed and turned on.
   > * Go to **Skills** and check that the `nebius-*` skills are listed.

   > [tab] Other agents
   >
   > * In the agent's MCP settings, check that the `nebius` server is listed.
   > * In the agent's skills directory, check that the `nebius-*` skills are present.

4. Ask the agent to make a request to Nebius AI Cloud:

   ```markdown wrap theme={null}
   List my Nebius AI Cloud projects
   ```

   The agent replies with the projects in your tenant, with their names and IDs. The agent may ask for permission to run a `nebius` command. Check that the command only lists projects, then allow it.

## What's next

Ask the agent what you can build on Nebius AI Cloud, or give it a task. For example:

```markdown wrap theme={null}
Which GPU platforms can I use in my project's region?
```

```markdown wrap theme={null}
Estimate the monthly price of an H200 VM
```

To limit what the agent can do, see the security recommendations for the [agent skills](https://docs.nebius.com/ai-agents/skills.md#security-recommendations) and the [Nebius MCP server](https://docs.nebius.com/ai-agents/mcp-server.md#security-recommendations).

## Troubleshooting

> [accordion] The agent doesn't see the Nebius MCP server
>
> 1. Restart the agent. Agents load MCP servers when they start.
> 2. Check the configuration as described in step 3 of [Steps](#steps). If the `nebius` server isn't listed, send the setup prompt again.
> 3. If the server is listed but doesn't start, check that `uvx --version` and `python3 --version` work in your terminal and that Python is 3.13 or later. For other causes, see the MCP documentation of your agent, for example, [Claude Code](https://code.claude.com/docs/en/mcp), [Codex](https://learn.chatgpt.com/docs/extend/mcp), or [Cursor](https://cursor.com/docs/mcp).

> [accordion] The agent doesn't use the skills
>
> 1. Check that the skills are loaded as described in step 3 of [Steps](#steps). If they aren't, install them again.
> 2. Update the Nebius AI Cloud CLI to the latest version by running `nebius update`.
> 3. [Update the skills](https://docs.nebius.com/ai-agents/skills.md#how-to-install-and-update-skills) to the latest version.

> [accordion] The agent gets a permission error
>
> If a command fails with the `PERMISSION_DENIED` error, the account in your CLI profile doesn't have the IAM role that the action requires. Ask an administrator of your tenant to add your account to a group that has the role. For details, see [Roles](https://docs.nebius.com/iam/authorization/roles.md) and [Managing custom groups](https://docs.nebius.com/iam/authorization/groups/manage.md).
>
> If the agent uses a CLI profile with limited roles, run the command yourself or switch to a profile that has the role.

> [accordion] The agent gets a billing error when it creates resources
>
> To create resources, your account needs billing details. [Set up billing](https://docs.nebius.com/signup-billing/sign-up.md#set-up-billing) in the web console, then ask the agent to try again.

> [accordion] The agent reaches a quota limit
>
> If a command fails with the `RESOURCE_EXHAUSTED` error, a quota in your tenant is used up. Ask the agent which quota it reached, then delete the resources that you no longer need or [request a quota increase](https://docs.nebius.com/overview/quotas.md).

> [accordion] The agent proposes an expensive GPU platform
>
> For a first test, the agent may suggest a more powerful GPU platform than you need. Ask it to estimate the price before it creates anything, and to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md) or a cheaper GPU platform that is [available in the region of your project](https://docs.nebius.com/overview/regions.md#availability-of-platforms-per-region).

> [accordion] The Nebius AI Cloud CLI is missing or uses the wrong profile
>
> * If the agent can't find the CLI, [install it](https://docs.nebius.com/cli/install.md) or send the setup prompt again.
> * If the agent works with the wrong tenant or project, ask it to run `nebius profile current`. The CLI uses the active profile, unless the `--profile` parameter or the `NEBIUS_PROFILE` environment variable sets another one. Check that neither is set in the agent's environment or in its MCP server configuration, or switch the active profile with `nebius profile activate <profile_name>`. For details, see [How to configure the CLI](https://docs.nebius.com/cli/configure.md).

## How to disconnect your agent

1. Remove the MCP server and the skills from the agent:

   > [tab] Claude Code
   >
   > ```bash theme={null}
   > claude mcp remove nebius --scope user
   > claude plugin uninstall nebius-cloud@nebius
   > ```

   > [tab] Codex
   >
   > 1. Remove the `nebius` server from `~/.codex/config.toml`.
   > 2. Run `/plugins` and uninstall the `nebius-cloud` plugin.

   > [tab] Cursor
   >
   > 1. Remove the `nebius` server from `~/.cursor/mcp.json`.
   > 2. Remove the `nebius-*` skills from `~/.agents/skills/`.

   > [tab] Other agents
   >
   > 1. Remove the `nebius` server from the agent's MCP configuration.
   > 2. Remove the `nebius-*` skills from the agent's skills directory.

2. If you created credentials only for the agent, such as a CLI profile or a [service account](https://docs.nebius.com/iam/service-accounts/manage.md#deleting-a-service-account), delete them. Keep the CLI profiles that you use with other tools.
