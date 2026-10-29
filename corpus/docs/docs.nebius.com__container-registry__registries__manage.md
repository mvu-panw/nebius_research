# How to manage registries in Container Registry

Source: https://docs.nebius.com/container-registry/registries/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage registries in Container Registry

Registries in Container Registry store Docker images and make them available to your resources. This guide will help you create and delete registries in Container Registry.

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to create a registry

**CLI**

Run the following command:

```bash theme={null}
nebius registry create \
  --name <registry_name>
```

Though the `--name` parameter is not required, the registry name simplifies finding the registry in the list of registries in Container Registry.

In the output, the registry ID is in the `metadata.id` parameter and the registry fully qualified domain name (FQDN) is in the `status.registry_fqdn` parameter.

**Go SDK**

```go theme={null}
createService := sdk.Services().Registry().V1().Registry()
createOperation, err := createService.Create(
    ctx,
    &registry.CreateRegistryRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<registry_name>",
        },
        Spec: &registry.RegistrySpec{},
    },
)
if err != nil {
    return fmt.Errorf("create registry: %w", err)
}
createOperation, err = createOperation.Wait(ctx)
if err != nil {
    return fmt.Errorf("wait for registry creation: %w", err)
}
createdRegistry, err := createService.Get(
    ctx,
    &registry.GetRegistryRequest{Id: createOperation.ResourceID()},
)
if err != nil {
    return fmt.Errorf("get created registry: %w", err)
}
fmt.Println(createdRegistry)
```

Though `Metadata.Name` is not required, the registry name simplifies finding the registry in the list of registries in Container Registry.

The response returns the registry ID in `Metadata.Id` and the registry fully qualified domain name (FQDN) in `Status.RegistryFqdn`.

**Python SDK**

```python theme={null}
registry_service = RegistryServiceClient(sdk)
create_operation = await registry_service.create(
    CreateRegistryRequest(
        metadata=ResourceMetadata(name="<registry_name>"),
        spec=RegistrySpec(),
    ),
)
await create_operation.wait()
created_registry = await registry_service.get(
    GetRegistryRequest(id=create_operation.resource_id),
)
print(created_registry)
```

Though `metadata.name` is not required, the registry name simplifies finding the registry in the list of registries in Container Registry.

The response returns the registry ID in `metadata.id` and the registry fully qualified domain name (FQDN) in `status.registry_fqdn`.

**JavaScript SDK**

```ts theme={null}
const createService = new RegistryService(sdk);
const createOperation = await createService.create(
  CreateRegistryRequest.create({
    metadata: { name: "<registry_name>" },
    spec: {},
  }),
).result;
await createOperation.wait();
const createdRegistry = await createService.get(
  GetRegistryRequest.create({ id: createOperation.resourceId() }),
).result;
console.log(createdRegistry);
```

Though `metadata.name` is not required, the registry name simplifies finding the registry in the list of registries in Container Registry.

The response returns the registry ID in `metadata.id` and the registry fully qualified domain name (FQDN) in `status.registryFqdn`.

To access the created registry, use its URL:

```bash theme={null}
<registry_FQDN>/<registry_path>
```

The registry path is the registry ID without the `registry-` prefix. For example, the registry with the `registry-a00bcdefghe12xyz3f` ID in the `eu-north1` region has the `cr.eu-north1.nebius.cloud/a00bcdefghe12xyz3f` URL.

## How to delete a registry

To delete a registry:

1. Get the registry ID by listing the registries:

   **CLI**

   ```bash theme={null}
   nebius registry list
   ```

   The ID is returned in the `.metadata.id` parameter of the registry resource.

   **Go SDK**

   ```go theme={null}
   listService := sdk.Services().Registry().V1().Registry()
   registries, err := listService.List(
       ctx,
       &registry.ListRegistriesRequest{},
   )
   if err != nil {
       return fmt.Errorf("list registries: %w", err)
   }
   fmt.Println(registries)
   ```

   The response returns the ID of each registry in `Items[].Metadata.Id`.

   **Python SDK**

   ```python theme={null}
   registry_service = RegistryServiceClient(sdk)
   registries = await registry_service.list(ListRegistriesRequest())
   print(registries)
   ```

   The response returns the ID of each registry in `items[].metadata.id`.

   **JavaScript SDK**

   ```ts theme={null}
   const listService = new RegistryService(sdk);
   const registries = await listService.list(
     ListRegistriesRequest.create({}),
   ).result;
   console.log(registries);
   ```

   The response returns the ID of each registry in `items[].metadata.id`.

2. Delete the registry:

   **CLI**

   ```bash theme={null}
   nebius registry delete --id <registry_ID>
   ```

   In this command, set `--id` to the registry ID. If the registry contains images, the deletion fails. To delete the registry together with its images, add the `--force` parameter.

   **Go SDK**

   ```go theme={null}
   deleteService := sdk.Services().Registry().V1().Registry()
   deleteOperation, err := deleteService.Delete(
       ctx,
       &registry.DeleteRegistryRequest{Id: "<registry_ID>"},
   )
   if err != nil {
       return fmt.Errorf("delete registry: %w", err)
   }
   if _, err := deleteOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for registry deletion: %w", err)
   }
   ```

   In the code, set `Id` to the registry ID. If the registry contains images, the deletion fails. To delete the registry together with its images, add `Force: true` to `DeleteRegistryRequest`.

   **Python SDK**

   ```python theme={null}
   registry_service = RegistryServiceClient(sdk)
   delete_operation = await registry_service.delete(
       DeleteRegistryRequest(id="<registry_ID>"),
   )
   await delete_operation.wait()
   ```

   In the code, set `id` to the registry ID. If the registry contains images, the deletion fails. To delete the registry together with its images, add `force=True` to `DeleteRegistryRequest`.

   **JavaScript SDK**

   ```ts theme={null}
   const deleteService = new RegistryService(sdk);
   const deleteOperation = await deleteService.delete(
     DeleteRegistryRequest.create({ id: "<registry_ID>" }),
   ).result;
   await deleteOperation.wait();
   ```

   In the code, set `id` to the registry ID. If the registry contains images, the deletion fails. To delete the registry together with its images, add `force: true` to `DeleteRegistryRequest`.
