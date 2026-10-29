# Copying images to and from registries in Container Registry

Source: https://docs.nebius.com/container-registry/images/copy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Copying images to and from registries in Container Registry

You can copy Docker images to and from Container Registry:

1. [Set up authentication in Container Registry](https://docs.nebius.com/container-registry/authentication.md) on your machine.

2. Get the fully qualified domain names (FQDNs) and paths of your source and destination registries.

   In Nebius AI Cloud, a registry's FQDN is `cr.<region_ID>.nebius.cloud` where `<region_ID>` is the ID of a [Nebius AI Cloud region](https://docs.nebius.com/overview/regions.md); for example, `cr.eu-north1.nebius.cloud`. To get a registry's FQDN, run the Nebius AI Cloud CLI command `nebius registry list` or `nebius registry get <registry_ID>`; the output contains the FQDN in the `.status.registry_fqdn` parameter. The registry path is the registry ID from the `.metadata.id` parameter without the `registry-` prefix. For more details about the commands, see the references for [nebius registry list](https://docs.nebius.com/cli/reference/registry/list.md) and [nebius registry get](https://docs.nebius.com/cli/reference/registry/get.md).

3. Pull the image from the source registry:

   ```bash theme={null}
   docker pull <source_FQDN>/<source_registry_path>/<image>:<tag>
   ```

4. Add a destination registry tag to the image and push it to the registry:

   ```bash theme={null}
   docker tag \
     <source_FQDN>/<source_registry_path>/<image>:<tag> \
     <destination_FQDN>/<destination_registry_path>/<image>:<tag>
   docker push <destination_FQDN>/<destination_registry_path>/<image>:<tag>
   ```

> For example, to copy the `hello-world:hello` image from the registry with the `registry-a00bcdefghe12xyz3f` ID in Nebius AI Cloud's `eu-north1` region and transfer it to a [GitHub Packages container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) called `octocat`, run the following commands:
>
> ```bash theme={null}
> docker pull cr.eu-north1.nebius.cloud/a00bcdefghe12xyz3f/hello-world:hello
> docker tag \
>   cr.eu-north1.nebius.cloud/a00bcdefghe12xyz3f/hello-world:hello \
>   ghcr.io/octocat/hello-world:hello
> docker push ghcr.io/octocat/hello-world:hello
> ```
