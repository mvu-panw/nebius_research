# Managing projects in Nebius AI Cloud

Source: https://docs.nebius.com/iam/manage-projects

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing projects in Nebius AI Cloud

Resources in Nebius AI Cloud are organized and managed within projects. When a tenant is created, a project per [region](https://docs.nebius.com/overview/regions.md) is created by default. You can additionally [create](#how-to-create-a-project) projects and [edit](#how-to-edit-a-project) existing ones.

## Prerequisites

The prerequisites for this guide depend on the interface that you use.

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

> [!WARNING]
>
> **Use one profile per project**
>
> Create a separate Nebius AI Cloud CLI profile for each project to ensure correct [region](https://docs.nebius.com/overview/regions.md)-specific configuration.

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

[Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create a project

**Web console**

1. In the [web console](https://console.nebius.com), expand the list of projects.

2. Click  **Create project**.

3. In the project creation form, specify the project settings:

   * Select the tenant and region. You cannot change them later.
   * Enter the name of the new project. The name should be unique in the tenant. You can [edit](#how-to-edit-a-project) it later.

4. Click **Create project**.

**CLI**

Create a project:

```bash theme={null}
nebius iam v2 project create \
  --parent-id <tenant_ID> \
  --name <project_name> \
  --region <region_name>
```

The command contains the following parameters:

* `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
* `--name`: Name of the project.
* `--region`: Name of the [region](https://docs.nebius.com/overview/regions.md) where the project is created.

  > [!WARNING]
  >
  > You can only create a project via the Nebius AI Cloud CLI in [public regions](https://docs.nebius.com/overview/regions.md#public-regions). If you try to create a project in a private region, you receive an error.

**Terraform**

1. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_iam_v2_project" "<project_name>" {
     name      = "<project_name>"
     parent_id = "<tenant_ID>"
     region    = "<region_name>"
   }
   ```

   The resource contains the following parameters:

   * `parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md).
   * `name`: Name of the project.
   * `region`: Name of the [region](https://docs.nebius.com/overview/regions.md) where the project is created.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

```go theme={null}
createProjectService := sdk.Services().IAM().V2().
    Project()
projectCreateOperation, err := createProjectService.Create(
    ctx,
    &iamv2.CreateProjectRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<tenant_ID>",
            Name:     "<project_name>",
        },
        Spec: &iamv2.ProjectSpec{
            Region: "<region_name>",
        },
    },
)
if err != nil {
    return err
}
if _, err = projectCreateOperation.Wait(ctx); err != nil {
    return err
}
```

In the code, set the following parameters:

* `Metadata.ParentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).
* `Metadata.Name`: Name of the project.
* `Spec.Region`: Name of the [region](https://docs.nebius.com/overview/regions.md) where the project is created.

  > [!WARNING]
  >
  > You can only create a project via the Nebius AI Cloud SDK in [public regions](https://docs.nebius.com/overview/regions.md#public-regions). If you try to create a project in a private region, you receive an error.

**Python SDK**

```python theme={null}
create_project_service = ProjectServiceClient(sdk)
project_create_operation = await create_project_service.create(
    CreateProjectRequest(
        metadata=ResourceMetadata(
            parent_id="<tenant_ID>",
            name="<project_name>",
        ),
        spec=ProjectSpec(region="<region_name>"),
    ),
)
await project_create_operation.wait()
```

In the code, set the following parameters:

* `metadata.parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).
* `metadata.name`: Name of the project.
* `spec.region`: Name of the [region](https://docs.nebius.com/overview/regions.md) where the project is created.

  > [!WARNING]
  >
  > You can only create a project via the Nebius AI Cloud SDK in [public regions](https://docs.nebius.com/overview/regions.md#public-regions). If you try to create a project in a private region, you receive an error.

**JavaScript SDK**

```ts theme={null}
const createProjectService = new ProjectService(sdk);
const projectCreateOperation =
  await createProjectService.create(
    CreateProjectRequest.create({
      metadata: ResourceMetadata.create({
        parentId: "<tenant_ID>",
        name: "<project_name>",
      }),
      spec: ProjectSpec.create({
        region: "<region_name>",
      }),
    }),
  ).result;
await projectCreateOperation.wait();
```

In the code, set the following parameters:

* `metadata.parentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).
* `metadata.name`: Name of the project.
* `spec.region`: Name of the [region](https://docs.nebius.com/overview/regions.md) where the project is created.

  > [!WARNING]
  >
  > You can only create a project via the Nebius AI Cloud SDK in [public regions](https://docs.nebius.com/overview/regions.md#public-regions). If you try to create a project in a private region, you receive an error.

## How to get a project ID

**Web console**

1. In the [web console](https://console.nebius.com), expand the list of projects.
2. Next to the project name, click  →  **Copy project ID**.

**CLI**

Run the following command:

```bash theme={null}
nebius iam v2 project get-by-name --parent-id <tenant_ID> --name <project_name>
```

In this command, specify the parameters:

* `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2) where the project is created.
* `--name`: Name of the project.
  If you do not know the exact name of the project, use the `list` command to view the list of all projects of your tenant:

  ```bash theme={null}
  nebius iam v2 project list --parent-id <tenant_ID>
  ```

**Terraform**

In your Terraform working directory, get the attributes of your project using its name:

```bash theme={null}
terraform state show nebius_iam_v2_project.<project_name>
```

The `id` attribute in the output contains the project ID.

If you do not know the exact name of the project, list all the resources from your Terraform state file (`.tfstate`) to find the project name:

```bash theme={null}
terraform state list
```

**Go SDK**

```go theme={null}
getProjectService := sdk.Services().IAM().V2().
    Project()
project, err := getProjectService.GetByName(
    ctx,
    &iamv2.GetProjectByNameRequest{
        ParentId: "<tenant_ID>",
        Name:     "<project_name>",
    },
)
if err != nil {
    return err
}
projectID := project.GetMetadata().GetId()
if projectID == "" {
    return errors.New("project ID is missing")
}
fmt.Println(projectID)
```

In the code, set the following parameters:

* `ParentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2) where the project is created.
* `Name`: Name of the project.

  If you don't know the exact name of the project, list all projects of your tenant by using `sdk.Services().IAM().V2().Project().List()`.

The response returns the project ID in `Metadata.Id`.

**Python SDK**

```python theme={null}
get_project_service = ProjectServiceClient(sdk)
project = await get_project_service.get_by_name(
    GetProjectByNameRequest(
        parent_id="<tenant_ID>",
        name="<project_name>",
    ),
)
project_id = project.metadata.id
print(project_id)
```

In the code, set the following parameters:

* `parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2) where the project is created.
* `name`: Name of the project.

  If you don't know the exact name of the project, list all projects of your tenant by using `ProjectServiceClient(sdk).list()`.

The response returns the project ID in `metadata.id`.

**JavaScript SDK**

```ts theme={null}
const getProjectService = new ProjectService(sdk);
const project = await getProjectService.getByName(
  GetProjectByNameRequest.create({
    parentId: "<tenant_ID>",
    name: "<project_name>",
  }),
);
const projectId = project.metadata?.id;
if (!projectId) {
  throw new Error("project ID is missing");
}
console.log(projectId);
```

In the code, set the following parameters:

* `parentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2) where the project is created.
* `name`: Name of the project.

  If you don't know the exact name of the project, list all projects of your tenant by using `new ProjectService(sdk).list()`.

The response returns the project ID in `metadata.id`.

## How to edit a project

For an existing project, you can only edit the name. You cannot move a project to another region or tenant.

To edit the project name:

**Web console**

1. In the [web console](https://console.nebius.com), expand the list of projects.
2. In the line of the required project, click  → **Configure**.
3. Enter a new value in the **Name** field.
4. Click **Save**.

**CLI**

Run the following command:

```bash theme={null}
nebius iam v2 project edit \
  --id <project_ID>
  [--editor '<editor_terminal_name> --wait'] \
  [--format <json|yaml>]
```

In this command, specify the parameters:

* `--id`: ID of the project.

* `--editor` (optional): Editor name. It can be any editor installed on your machine, such as `nano` or `emacs`. To check which of the popular editors are installed, run the following command:

  ```bash theme={null}
  which code emacs gedit micro nano subl vi vim
  ```

  For an editor that opens in a separate window, add the `--wait` parameter to its name to ensure that the command waits until you close the editor.

* `--format` (optional): Data format. Only `json` and `yaml` values are accepted. By default, YAML format is used.

The editor you choose opens and shows the current configuration of the project. Change the project name and save the configuration. When you exit the editor, the Nebius AI Cloud CLI checks if the data is valid and updates the resource.

**Terraform**

1. In the configuration file, edit the `name` argument of the corresponding `nebius_iam_v2_project` resource.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

The SDK has no partial update call, so to change the project name, get the project, modify `Metadata.Name`, then send the updated metadata and spec back:

```go theme={null}
projectService := sdk.Services().IAM().V2().
    Project()
projectForUpdate, err := projectService.Get(
    ctx,
    &iamv2.GetProjectRequest{Id: "<project_ID>"},
)
if err != nil {
    return err
}
projectForUpdate.GetMetadata().Name = "<new_project_name>"
updateProjectOperation, err := projectService.
    Update(
        ctx,
        &iamv2.UpdateProjectRequest{
            Metadata: projectForUpdate.GetMetadata(),
            Spec:     projectForUpdate.GetSpec(),
        },
    )
if err != nil {
    return err
}
if _, err = updateProjectOperation.Wait(ctx); err != nil {
    return err
}
```

In the code, set the following parameters:

* `Id` in `GetProjectRequest`: ID of the project.
* `Metadata.Name`: New name of the project.

**Python SDK**

The SDK has no partial update call, so to change the project name, get the project, modify `metadata.name`, then send the updated metadata and spec back:

```python theme={null}
project_service = ProjectServiceClient(sdk)
project_for_update = await project_service.get(
    GetProjectRequest(id="<project_ID>"),
)
project_for_update.metadata.name = "<new_project_name>"
update_project_operation = (
    await project_service.update(
        UpdateProjectRequest(
            metadata=project_for_update.metadata,
            spec=project_for_update.spec,
        ),
    )
)
await update_project_operation.wait()
```

In the code, set the following parameters:

* `id` in `GetProjectRequest`: ID of the project.
* `metadata.name`: New name of the project.

**JavaScript SDK**

The SDK has no partial update call, so to change the project name, get the project, modify `metadata.name`, then send the updated metadata and spec back:

```ts theme={null}
const projectService = new ProjectService(sdk);
const projectForUpdate = await projectService.get(
  GetProjectRequest.create({id: "<project_ID>"}),
);
projectForUpdate.metadata.name = "<new_project_name>";
const updateProjectOperation =
  await projectService.update(
    UpdateProjectRequest.create({
      metadata: projectForUpdate.metadata,
      spec: projectForUpdate.spec,
    }),
  ).result;
await updateProjectOperation.wait();
```

In the code, set the following parameters:

* `id` in `GetProjectRequest`: ID of the project.
* `metadata.name`: New name of the project.

## How to delete a project

Before you delete a project, make sure to remove all resources from it. You can only delete an empty project.

**Web console**

1. In the [web console](https://console.nebius.com), expand the list of projects.
2. In the line of the required project, click  → **Delete project**.

**CLI**

Delete the project:

```bash theme={null}
nebius iam v2 project delete --id <project_ID>
```

**Terraform**

1. Remove the corresponding `nebius_iam_v2_project` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Delete the project:

```go theme={null}
deleteProjectService := sdk.Services().IAM().V2().
    Project()
deleteProjectOperation, err := deleteProjectService.Delete(
    ctx,
    &iamv2.DeleteProjectRequest{Id: "<project_ID>"},
)
if err != nil {
    return err
}
if _, err = deleteProjectOperation.Wait(ctx); err != nil {
    return err
}
```

In the code, set `Id` to the ID of the project.

**Python SDK**

Delete the project:

```python theme={null}
delete_project_service = ProjectServiceClient(sdk)
delete_project_operation = await delete_project_service.delete(
    DeleteProjectRequest(id="<project_ID>"),
)
await delete_project_operation.wait()
```

In the code, set `id` to the ID of the project.

**JavaScript SDK**

Delete the project:

```ts theme={null}
const deleteProjectService = new ProjectService(sdk);
const deleteProjectOperation =
  await deleteProjectService.delete(
    DeleteProjectRequest.create({id: "<project_ID>"}),
  ).result;
await deleteProjectOperation.wait();
```

In the code, set `id` to the ID of the project.
