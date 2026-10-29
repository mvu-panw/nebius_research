# API and developer tools in Nebius AI Cloud

Source: https://docs.nebius.com/developer-tools

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# API and developer tools in Nebius AI Cloud

Nebius AI Cloud provides a series of developer tools and interfaces for resource management. The developer tools are practical when you create and manage a large number of resources. In contrast, the [web console](https://console.nebius.com) is more useful when you manage a few resources or when you need a web interface. In addition, the developer tools are more convenient in comparison with sending API requests directly.

## Developer tools

> **[CLI](https://docs.nebius.com/cli/index.md)**
>
> Manage resources in the terminal.

> **[Terraform provider](https://docs.nebius.com/terraform-provider/index.md)**
>
> Prepare and apply resource configuration by using a declarative approach.

> **[SDKs](https://docs.nebius.com/sdk/index.md)**
>
> Use off-the-shelf libraries for Go, Python and JavaScript, and manage resources with code.

> **[Pulumi](https://docs.nebius.com/terraform-provider/pulumi.md)**
>
> Based on the Terraform provider, generate a local Pulumi SDK and manage resources via it.

> **[MCP server (beta version)](https://github.com/nebius/mcp-server/)**
>
> Manage resources in your chats with AI agents by using the Model Context Protocol (MCP) server.

## Types of the API

> **[gRPC API](https://docs.nebius.com/grpc-api/index.md)**
>
> For high-performance systems and high loads.

> **[REST API](https://docs.nebius.com/rest-api/index.md)**
>
> For simple data communication and web-based applications.

## Common features of the developer tools

### Generating tools from a single API

The developer tools are automatically generated from the single Nebius AI Cloud API, which provides every tool with the same set of services, methods and parameters.

For example, the CLI command `nebius compute instance create` contains the `--gpu-cluster-id` parameter, and the equivalent Terraform resource `nebius_compute_v1_instance` contains the same `gpu_cluster.id` parameter.

Any changes that appear in the API are also reflected in the tools.

### Versioning

The API supports two types of versioning:

* *Alpha versions* are designed as `v1alpha1`, `v2alpha1` or similar. Considered unstable and can change.
* *Stable versions* are designed as `v1`, `v2` or similar.

If a stable version is supported, use it instead of an alpha version. In this case, the alpha version is to be deprecated.

The developer tools reflect the version as well as the API endpoints. You can see the version in CLI commands and Terraform manifests. For example, the `nebius iam v2 access-key` commands include the stable `v2` version.
