# Nebius AI Cloud agent skills

Source: https://docs.nebius.com/ai-agents/skills

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius AI Cloud agent skills

Use the agent skills to run and manage your AI workloads on Nebius AI Cloud from a coding agent, such as Claude Code, Codex, or Cursor. The agent picks the skill that fits your request and runs Nebius AI Cloud CLI commands for you.

For the list of skills and their rules, see the [nebius/skills](https://github.com/nebius/skills) repository on GitHub:

With the skills, you can ask the agent for help with the following tasks:

| Task | What you can ask the agent to do |
| - | - |
| Get GPUs | Check GPU capacity, quotas, and the resources you have, then create VMs, shared filesystems, and GPU clusters. |
| Develop, train, and serve models | Create Devlabs with GPUs for notebooks. Run your container as a Serverless AI job, including multi-GPU training and preemptible fine-tuning with checkpoints, or deploy vLLM or your own container as a Serverless AI endpoint. |
| Control costs | Estimate prices before you create resources, cap the price of preemptible VMs, jobs, and endpoints, and limit how long a job runs. The agent tells you when a job, endpoint, or Devlab is still running and how much it costs per hour. |
| Troubleshoot and get answers | Find out why a job or endpoint is stuck or failed, collect debug logs of failed CLI, Terraform, and SDK calls, and get answers about Nebius AI Cloud with links to the documentation. |

## Prerequisites

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. [Install Node.js 22.20](https://nodejs.org/en/download) or later to install and update the skills in Cursor and other agents.

## How to install and update skills

To install the skills together with the CLI and the Nebius MCP server, follow [How to connect your AI agent to Nebius AI Cloud](https://docs.nebius.com/ai-agents/connect.md).

If you installed the skills earlier, update them to the latest version:

> [tab] Claude Code
>
> In your terminal, run:
>
> ```bash theme={null}
> claude plugin update nebius-cloud@nebius
> ```
>
> To update the skills automatically, run `/plugin`, go to the **Marketplaces** tab, select the `nebius` marketplace, and select **Enable auto-update**. Auto-update is off by default for this marketplace. For details, see the [Claude Code documentation](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

> [tab] Codex
>
> Codex doesn't update the skills automatically. To update them, run:
>
> ```bash theme={null}
> codex plugin marketplace upgrade nebius
> ```

> [tab] Cursor
>
> Cursor doesn't update the skills automatically. To update them, run:
>
> ```bash theme={null}
> npx skills update -g
> ```

> [tab] Other agents
>
> In the project where you installed the skills, run:
>
> ```bash theme={null}
> npx skills update
> ```

## Security recommendations

* Run the agent with a CLI profile that has only the roles your task needs. The agent acts with the [roles](https://docs.nebius.com/iam/authorization/roles.md) of the account in your CLI profile. [Set up a CLI profile for a service account](https://docs.nebius.com/cli/configure.md#how-to-set-up-the-cli-for-a-service-account) with limited roles and ask the agent to use this profile. For example, with the `viewer` role, the agent only reads resources and you make all changes yourself.
* Review every command that the agent asks to run. The skills instruct the agent to ask for your confirmation before it creates, updates, starts, or stops resources. The agent gives you commands that delete resources or issue credentials to run yourself. These rules are only instructions, so the agent can still run any command that your CLI profile allows.

## How to report a problem

If a command from the agent contradicts this documentation or the output of `nebius <command> --help`, follow the documentation and the CLI help. [Open an issue](https://github.com/nebius/skills/issues/new) in the repository with the skill name, the command, the output of `nebius version`, and what happened. To report a skill that exposes credentials or runs destructive commands, [report a vulnerability](https://github.com/nebius/skills/security/advisories/new) instead.
