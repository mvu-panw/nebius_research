# Monitoring agent on Compute virtual machines

Source: https://docs.nebius.com/observability/agents/monitoring-agent

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring agent on Compute virtual machines

With each Compute virtual machine or resource that a VM hosts, such as Managed Service for Kubernetes® nodes, Nebius AI Cloud provides the monitoring agent. It collects usage data for VM's system resources (GPU, vCPU, RAM) and sends it to Observability Metrics for display on dashboards in the web console. The agent can also [collect journald logs from systemd services](https://docs.nebius.com/observability/logs/journald.md) when enabled.

## How the agent works

Compute installs two components for monitoring on all new virtual machines:

* `nebius-observability-agent` collects resource's metrics. For Compute virtual machines, these metrics include GPU, InfiniBand™, operating system and other metrics.
* `nebius-observability-agent-updater` updates the agent and delivers new features.

The components are installed automatically on Nebius AI Cloud resources. When the resource is created, the agent works as follows:

1. Collects resource's metrics.
2. Stores the metrics in a safe storage in case the metrics collection endpoint becomes unavailable.
3. Adds labels that identify the resource and the project to the metrics.
4. Sends enriched metrics to Observability Metrics for display on web console dashboards.

## How to manage the agent

To manage the monitoring agent (for example, disable its updates or roll back to an older version), [connect to the VM over SSH](https://docs.nebius.com/compute/virtual-machines/connect.md) and follow instructions in the next sections.

> **Stop automatic agent updates**
>
> You can keep a particular version of the agent. The agent will still collect the metrics, but will stop updating and will not collect metrics for future features. To stop the agent from auto-updating, uninstall the agent updater:
>
> ```bash theme={null}
> sudo dpkg -r nebius-observability-agent-updater
> ```

> **Rollback to a previous agent revision**
>
> Nebius team observes the agent state and updates it in case of failures. However, if you find that the current version of the agent is not working as intended, you may prefer to work with a previous agent revision. To update the agent to a previous version:
>
> 1. [Connect to the VM over SSH](https://docs.nebius.com/compute/virtual-machines/connect.md).
>
> 2. On the VM, run:
>
>    ```bash theme={null}
>    apt-cache madison nebius-observability-agent
>    ```
>
>    This command lists every version of the `nebius-observability-agent` package available from your configured [APT sources](https://wiki.debian.org/SourcesList).
>
>    Example output:
>
>    ```text theme={null}
>    nebius-observability-agent |    0.1.140 | https://dr.nebius.cloud stable/main amd64 Packages
>    nebius-observability-agent |    0.1.139 | https://dr.nebius.cloud stable/main amd64 Packages
>    ...
>    nebius-observability-agent |     0.1.40 | https://dr.nebius.cloud stable/main amd64 Packages
>    ```
>
> 3. Select a version from the second column (for example, `0.1.139`).
>
> 4. Run the following commands, replacing `<agent_version>` with that version:
>
>    ```bash theme={null}
>    sudo apt update -o Dir::Etc::sourcelist="sources.list.d/agent.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"
>    echo -e "Package: nebius-observability-agent\nPin: version <agent_version>\nPin-Priority: 1001" > /etc/apt/preferences.d/agent.conf
>    sudo apt install -y nebius-observability-agent
>    ```
>
> 5. Check that the installed package version matches the one you selected:
>
>    ```bash theme={null}
>    dpkg-query -W -f='${Version}\n' nebius-observability-agent
>    ```
>
>    The output version should match `<agent_version>` (for example, `0.1.139`). If it doesn't, check `/etc/apt/preferences.d/agent.conf` and run the commands from the previous step again.

> **Uninstall the agent**
>
> If you no longer need the metrics to monitor and troubleshoot your resources, connect to each resource and delete the agent:
>
> ```bash theme={null}
> sudo dpkg -r nebius-observability-agent nebius-observability-agent-updater
> ```
>
> Keep in mind that after you uninstall the agent, Nebius support team will have no future data to investigate problems with your Nebius AI Cloud resources. Instead of uninstalling the agent, consider stopping its automatic updates.

> **Reinstall the agent**
>
> If you accidentally uninstall the agent, you can always reinstall it on the resource:
>
> 1. Install the agent:
>
>    ```bash theme={null}
>    sudo apt update && sudo apt install -y nebius-observability-agent
>    ```
>
> 2. (Optional) Enable automatic agent updates:
>
>    ```bash theme={null}
>    sudo apt update && sudo apt install -y nebius-observability-agent-updater
>    ```

## Data retention and deletion

Collected metrics are stored with full resolution (one datapoint every 15 seconds for most metrics) for 1 month and later with reduced resolution (one datapoint every 5 minutes) for 1 year.

If you want to delete all your metrics, [contact support](https://console.nebius.com/support/create-ticket). Keep in mind that after deleting your metrics, Nebius support team will have no data to investigate problems with your Nebius AI Cloud resources.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
