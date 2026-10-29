# Managing DNS zones

Source: https://docs.nebius.com/vpc/dns/manage-zones

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing DNS zones

Nebius AI Cloud creates a [system-managed DNS zone](https://docs.nebius.com/vpc/dns/overview.md#system-managed-and-custom-zones) for each virtual network automatically, but you can also create [custom DNS zones](https://docs.nebius.com/vpc/dns/overview.md#dns-zones) and manage them.

Custom zones are private. Names in them resolve only from workloads inside the network the zone is attached to.

> [!NOTE]
>
> System-managed zones, for example, `<network_ID>.compute.internal.`, are read-only and cannot be modified or deleted.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Creating DNS zones

**Web console**

> [!NOTE]
>
> If you want to set a name for the zone or configure the negative caching time-to-live (TTL), use a different interface. The web console doesn't support these settings.

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Click **Actions** → **Create DNS zone**.
3. In the window that opens, enter a fully qualified domain name (FQDN) that ends with a dot (`.`), for example, `my.example.`. Single-label names, such as `example.`, and reserved names, such as `console.nebius.`, aren't allowed. Learn more in [Zone domain name restrictions](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md#zone-domain-name-restrictions).
4. Select the network to attach the DNS zone to.
5. Click **Create DNS zone**.

You cannot change the domain name or attached network after creating the zone. To use another domain name or network, [delete the zone](#deleting-dns-zones) and create a new one.

**CLI**

Run the following command:

```bash theme={null}
nebius dns zone create \
  --domain-name <domain_name> \
  --parent-id <project_ID> \
  --name <name> \
  --labels <key>=<value>,<key2>=<value2> \
  --soa-spec-negative-ttl <negative_TTL> \
  --vpc-primary-network-id <network_ID>
```

In the command, specify the following parameters:

* `--domain-name`: Domain name for the zone. Use a fully qualified domain name (FQDN) that ends with a dot (`.`), for example, `my.example.`. You cannot change the domain name after the zone is created. Top-level domains such as `example.` and some names that are reserved for internal use, such as `console.nebius.`, aren't allowed. Learn more in [Zone domain name restrictions](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md#zone-domain-name-restrictions).
* `--parent-id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3).
* `--vpc-primary-network-id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#cli-2) of the network to attach the zone to. You cannot change the network after the zone is created.
* `--name` (optional): Name of the zone.
* `--labels` (optional): Labels in the `key=value` format.
* `--soa-spec-negative-ttl` (optional): How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.

The output looks like the following:

```yaml theme={null}
metadata:
  id: dnszone-e00**
  parent_id: project-e00**
  resource_version: "144465"
  created_at: "2026-06-30T12:50:55.335401Z"
  updated_at: "2026-06-30T12:50:55.335401Z"
spec:
  domain_name: my.example.
  vpc:
    primary_network_id: vpcnetwork-e00**
  soa_spec:
    negative_ttl: "300"
status:
  record_count: "2"
```

The returned resource shows the parameters you specified and the following:

* `resource_version` is the current version of the zone. If you later update or delete the zone, you can pass this value in `--resource-version` to make sure that the command applies only to this version of the zone.
* `status.record_count` shows how many [DNS records](https://docs.nebius.com/vpc/dns/manage-records.md) the zone currently contains. This value can already be greater than `0` after creation because the zone includes service-managed records that are automatically created.

**Terraform**

1. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_dns_v1_zone" "my_zone" {
     domain_name = "<domain_name>"
     parent_id   = "<project_ID>"

     vpc = {
       primary_network_id = "<network_ID>"
     }

     name = "<name>"

     labels = {
       <key> = "<value>"
     }

     soa_spec = {
       negative_ttl = <negative_TTL>
     }
   }
   ```

   In the configuration, specify the following parameters:

   * `domain_name`: Domain name for the zone. Use a fully qualified domain name (FQDN) that ends with a dot (`.`), for example, `my.example.`. You cannot change the domain name after the zone is created. Top-level domains such as `example.` and some names that are reserved for internal use, such as `console.nebius.`, aren't allowed. Learn more in [Zone domain name restrictions](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md#zone-domain-name-restrictions).
   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `vpc.primary_network_id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) of the network to attach the zone to. You cannot change the network after the zone is created.
   * `name` (optional): Name of the zone.
   * `labels` (optional): Labels in the `key = "value"` format.
   * `soa_spec.negative_ttl` (optional): How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.

   For all the parameters of the resource, see [nebius\_dns\_v1\_zone](https://docs.nebius.com/terraform-provider/reference/resources/dns_v1_zone.md) in the Terraform provider reference.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Run the following code:

```go theme={null}
zoneLabels := map[string]string{}
for _, label := range strings.Split("<key>=<value>,<key2>=<value2>", ",") {
    key, value, _ := strings.Cut(label, "=")
    zoneLabels[key] = value
}
dnsZoneService := sdk.Services().DNS().V1().
    Zone()
dnsZoneOperation, err := dnsZoneService.Create(
    ctx,
    &dns.CreateZoneRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<name>",
            ParentId: "<project_ID>",
            Labels: zoneLabels,
        },
        Spec: &dns.ZoneSpec{
            DomainName: "<domain_name>",
            Scope: &dns.ZoneSpec_Vpc{
                Vpc: &dns.VpcZoneScope{
                    PrimaryNetworkId: "<network_ID>",
                },
            },
            SoaSpec: &dns.SoaSpec{
                NegativeTtl: <negative_TTL>,
            },
        },
    },
)
if err != nil {
    return err
}
if _, err = dnsZoneOperation.Wait(ctx); err != nil {
    return err
}
fmt.Println(dnsZoneOperation)
```

In the code, set the following parameters:

* `Metadata.Name` (optional): Name of the zone.
* `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
* `Metadata.Labels` (optional): Labels. The code builds them from the comma-separated `key=value` pairs in `zoneLabels`.
* `Spec.DomainName`: Domain name for the zone. Use a fully qualified domain name (FQDN) that ends with a dot (`.`), for example, `my.example.`. You cannot change the domain name after the zone is created. Top-level domains such as `example.` and some names that are reserved for internal use, such as `console.nebius.`, aren't allowed. Learn more in [Zone domain name restrictions](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md#zone-domain-name-restrictions).
* `PrimaryNetworkId` under `Spec.Scope`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-2) of the network to attach the zone to. You cannot change the network after the zone is created — delete and recreate the zone instead.
* `Spec.SoaSpec.NegativeTtl` (optional): How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.

To get the zone ID, use `dnsZoneOperation.ResourceID()`.

**Python SDK**

Run the following code:

```python theme={null}
zone_labels = dict(
    label.split("=", 1)
    for label in "<key>=<value>,<key2>=<value2>".split(",")
)
dns_zone_service = ZoneServiceClient(sdk)
dns_zone_operation = await dns_zone_service.create(
    CreateZoneRequest(
        metadata=ResourceMetadata(
            name="<name>",
            parent_id="<project_ID>",
            labels=zone_labels,
        ),
        spec=ZoneSpec(
            domain_name="<domain_name>",
            vpc=VpcZoneScope(
                primary_network_id="<network_ID>",
            ),
            soa_spec=SoaSpec(
                negative_ttl=<negative_TTL>,
            ),
        ),
    ),
)
await dns_zone_operation.wait()
print(dns_zone_operation)
```

In the code, set the following parameters:

* `name` (optional): Name of the zone.
* `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
* `labels` (optional): Labels. The code builds them from the comma-separated `key=value` pairs in `zone_labels`.
* `domain_name`: Domain name for the zone. Use a fully qualified domain name (FQDN) that ends with a dot (`.`), for example, `my.example.`. You cannot change the domain name after the zone is created. Top-level domains such as `example.` and some names that are reserved for internal use, such as `console.nebius.`, aren't allowed. Learn more in [Zone domain name restrictions](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md#zone-domain-name-restrictions).
* `vpc.primary_network_id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-2) of the network to attach the zone to. You cannot change the network after the zone is created — delete and recreate the zone instead.
* `soa_spec.negative_ttl` (optional): How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.

To get the zone ID, use `dns_zone_operation.resource_id`.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const zoneLabels = Object.fromEntries(
  "<key>=<value>,<key2>=<value2>".split(",").map((label) => {
    const index = label.indexOf("=");
    return [label.slice(0, index), label.slice(index + 1)];
  }),
);
const dnsZoneService = new ZoneService(sdk);
const dnsZoneOperation = await dnsZoneService.create(
  CreateZoneRequest.create({
    metadata: {
      name: "<name>",
      parentId: "<project_ID>",
      labels: zoneLabels,
    },
    spec: {
      domainName: "<domain_name>",
      scope: {
        "$case": "vpc",
        "vpc": {
          primaryNetworkId: "<network_ID>",
        },
      },
      soaSpec: {
        negativeTtl: <negative_TTL>,
      },
    },
  }),
).result;
await dnsZoneOperation.wait();
console.log(dnsZoneOperation);
```

In the code, set the following parameters:

* `metadata.name` (optional): Name of the zone.
* `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
* `metadata.labels` (optional): Labels. The code builds them from the comma-separated `key=value` pairs in `zoneLabels`.
* `spec.domainName`: Domain name for the zone. Use a fully qualified domain name (FQDN) that ends with a dot (`.`), for example, `my.example.`. You cannot change the domain name after the zone is created. Top-level domains such as `example.` and some names that are reserved for internal use, such as `console.nebius.`, aren't allowed. Learn more in [Zone domain name restrictions](https://docs.nebius.com/vpc/dns/resources/quotas-limits.md#zone-domain-name-restrictions).
* `primaryNetworkId` under `spec.scope`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-2) of the network to attach the zone to. You cannot change the network after the zone is created — delete and recreate the zone instead.
* `spec.soaSpec.negativeTtl` (optional): How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.

To get the zone ID, use `dnsZoneOperation.resourceId()`.

## Updating DNS zones

> [!NOTE]
>
> You cannot update DNS zones in the web console. To update a custom DNS zone, use a different interface.

**CLI**

1. Get the ID of the zone that you want to update:

   ```bash theme={null}
   nebius dns zone list
   ```

   Find the zone that you want to update. The output contains the zone ID in the `.metadata.id` parameter.

2. Run the following command:

   ```bash theme={null}
   nebius dns zone update <DNS_zone_ID> \
     --name <name> \
     --soa-spec-negative-ttl <negative_TTL> \
     --resource-version <resource_version>

   # To replace all labels, add:
   # --labels <key>=<value>,<key2>=<value2>
   #
   # To add or remove specific labels, add:
   # --labels-add <key>=<value>
   # --labels-remove <label_key>
   ```

   Specify the zone ID you got in the previous step as `<DNS_zone_ID>`. In the command, you can specify the following parameters to update them:

   * `--name` (optional): Name of the zone.
   * `--labels` (optional): Replace all labels with the specified labels, in the `key=value` format.
   * `--labels-add` (optional): Add labels, in the `key=value` format, without replacing the existing labels.
   * `--labels-remove` (optional): Remove existing labels by key.
   * `--soa-spec-negative-ttl` (optional): How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.
   * `--resource-version` (optional): Current version of the zone. Use the `metadata.resource_version` value returned when you create the zone or when you get its ID and details if you want to update only the current version that you last checked. If the zone changed and has a different version, the command fails.

**Terraform**

1. In the configuration file, update the `nebius_dns_v1_zone` resource:

   ```hcl theme={null}
   resource "nebius_dns_v1_zone" "my_zone" {
     name = "<name>"

     labels = {
       <key> = "<value>"
     }

     soa_spec = {
       negative_ttl = <negative_TTL>
     }

     # ...
   }
   ```

   You can update the following parameters:

   * `name`: Name of the zone.
   * `labels`: Labels in the `key = "value"` format.
   * `soa_spec.negative_ttl`: How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.

   Terraform recreates a DNS zone if you change `domain_name` or `vpc.primary_network_id`. You cannot change them in an already existing DNS zone.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the zone that you want to update. List the zones in the project, with `ParentId` set to the project ID:

   ```go theme={null}
   dnsZonesService := sdk.Services().DNS().V1().
       Zone()
   dnsZonesResponse, err := dnsZonesService.List(
       ctx,
       &dns.ListZonesRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(dnsZonesResponse)
   ```

   Find the zone that you want to update in `Items`. The zone ID is in `Metadata.Id`.

2. Update the zone:

   ```go theme={null}
   updatedZoneService := sdk.Services().DNS().V1().
       Zone()
   updatedZone, err := updatedZoneService.Get(
       ctx,
       &dns.GetZoneRequest{
           Id: "<DNS_zone_ID>",
       },
   )
   if err != nil {
       return err
   }
   updatedZone.Metadata.Name = "<name>"
   updatedZone.Metadata.ResourceVersion = <resource_version>
   updatedZone.Spec.SoaSpec = &dns.SoaSpec{
       NegativeTtl: <negative_TTL>,
   }
   // Optionally replace, add, or remove labels:
   // updatedZone.Metadata.Labels = map[string]string{
   //     "environment": "stage", "team": "docs",
   // }
   // updatedZone.Metadata.Labels["owner"] = "platform"
   // delete(updatedZone.Metadata.Labels, "team")
   zoneUpdateOperation, err := updatedZoneService.Update(
       ctx,
       &dns.UpdateZoneRequest{
           Metadata: updatedZone.Metadata,
           Spec: updatedZone.Spec,
       },
   )
   if err != nil {
       return err
   }
   if _, err = zoneUpdateOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set `Id` to the zone ID you got in the previous step. The code gets the zone and updates the following parameters. Remove the lines for the parameters that you don't want to change:

   * `Metadata.Name`: Name of the zone.
   * `Metadata.ResourceVersion`: Version of the zone that you last checked. If the zone changed and has a different version, the update fails.
   * `Spec.SoaSpec.NegativeTtl`: How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.
   * `Metadata.Labels`: To replace, add or remove labels, uncomment the corresponding lines in the code.

**Python SDK**

1. Get the ID of the zone that you want to update. List the zones in the project, with `parent_id` set to the project ID:

   ```python theme={null}
   dns_zones_service = ZoneServiceClient(sdk)
   dns_zones_response = await dns_zones_service.list(
       ListZonesRequest(
           parent_id="<project_ID>",
       ),
   )
   print(dns_zones_response)
   ```

   Find the zone that you want to update in `items`. The zone ID is in `metadata.id`.

2. Update the zone:

   ```python theme={null}
   updated_zone_service = ZoneServiceClient(sdk)
   updated_zone = await updated_zone_service.get(
       GetZoneRequest(
           id="<DNS_zone_ID>",
       ),
   )
   updated_zone.metadata.name = "<name>"
   updated_zone.metadata.resource_version = <resource_version>
   updated_zone.spec.soa_spec = SoaSpec(
       negative_ttl=<negative_TTL>,
   )
   # Optionally replace, add, or remove labels:
   # updated_zone.metadata.labels = {
   #     "environment": "stage", "team": "docs",
   # }
   # updated_zone.metadata.labels["owner"] = "platform"
   # updated_zone.metadata.labels.pop("team", None)
   zone_update_operation = await updated_zone_service.update(
       UpdateZoneRequest(
           metadata=updated_zone.metadata,
           spec=updated_zone.spec,
       ),
   )
   await zone_update_operation.wait()
   ```

   Set `id` to the zone ID you got in the previous step. The code gets the zone and updates the following parameters. Remove the lines for the parameters that you don't want to change:

   * `metadata.name`: Name of the zone.
   * `metadata.resource_version`: Version of the zone that you last checked. If the zone changed and has a different version, the update fails.
   * `spec.soa_spec.negative_ttl`: How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.
   * `metadata.labels`: To replace, add or remove labels, uncomment the corresponding lines in the code.

**JavaScript SDK**

1. Get the ID of the zone that you want to update. List the zones in the project, with `parentId` set to the project ID:

   ```ts theme={null}
   const dnsZonesService = new ZoneService(sdk);
   const dnsZonesResponse = await dnsZonesService.list(
     ListZonesRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(dnsZonesResponse);
   ```

   Find the zone that you want to update in `items`. The zone ID is in `metadata.id`.

2. Update the zone:

   ```ts theme={null}
   const updatedZoneService = new ZoneService(sdk);
   const updatedZone = await updatedZoneService.get(
     GetZoneRequest.create({
       id: "<DNS_zone_ID>",
     }),
   ).result;
   updatedZone.metadata.name = "<name>";
   updatedZone.metadata.resourceVersion = <resource_version>;
   updatedZone.spec.soaSpec = {
     negativeTtl: <negative_TTL>,
   };
   // Optionally replace, add, or remove labels:
   // updatedZone.metadata.labels = {
   //   environment: "stage", team: "docs",
   // };
   // updatedZone.metadata.labels.owner = "platform";
   // delete updatedZone.metadata.labels.team;
   const zoneUpdateOperation = await updatedZoneService.update(
     UpdateZoneRequest.create({
       metadata: updatedZone.metadata,
       spec: updatedZone.spec,
     }),
   ).result;
   await zoneUpdateOperation.wait();
   ```

   Set `id` to the zone ID you got in the previous step. The code gets the zone and updates the following parameters. Remove the lines for the parameters that you don't want to change:

   * `metadata.name`: Name of the zone.
   * `metadata.resourceVersion`: Version of the zone that you last checked. If the zone changed and has a different version, the update fails.
   * `spec.soaSpec.negativeTtl`: How long DNS resolvers can cache a "record not found" response for this zone, in seconds. Values below `5` are ignored, and the service default of `900` is used instead.
   * `metadata.labels`: To replace, add or remove labels, uncomment the corresponding lines in the code.

## Deleting DNS zones

You cannot delete system-managed DNS zones. To delete a custom DNS zone, first [delete all records](https://docs.nebius.com/vpc/dns/manage-records.md#deleting-dns-records) except the default `NS @` and `SOA @` records.

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. On the **DNS** tab, find the zone and click  → **Delete**.
3. Confirm the deletion.

**CLI**

1. Get the ID of the zone that you want to delete:

   ```bash theme={null}
   nebius dns zone list
   ```

   Find the zone that you want to delete. The output contains the zone ID in the `.metadata.id` parameter.

2. Run the following command:

   ```bash theme={null}
   nebius dns zone delete \
     --id <DNS_zone_ID> \
     --resource-version <resource_version>
   ```

   In the command, specify the following parameters:

   * `--id`: ID of the DNS zone to delete, `<DNS_zone_ID>`.
   * `--resource-version` (optional): Current version of the zone. Use the `metadata.resource_version` value returned when you create the zone or when you get its ID and details if you want to delete only the current version that you last checked. If the zone changed and has a different version, the command fails. If you omit this parameter or set it to `0`, the command uses the current version of the zone.

**Terraform**

1. Remove the corresponding `nebius_dns_v1_zone` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the zone that you want to delete. List the zones in the project, with `ParentId` set to the project ID:

   ```go theme={null}
   dnsZonesService := sdk.Services().DNS().V1().
       Zone()
   dnsZonesResponse, err := dnsZonesService.List(
       ctx,
       &dns.ListZonesRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(dnsZonesResponse)
   ```

   Find the zone that you want to delete in `Items`. The zone ID is in `Metadata.Id`.

2. Delete the zone:

   ```go theme={null}
   deletedZoneService := sdk.Services().DNS().V1().
       Zone()
   deletedZoneOperation, err := deletedZoneService.Delete(
       ctx,
       &dns.DeleteZoneRequest{
           Id: "<DNS_zone_ID>",
           ResourceVersion: <resource_version>,
       },
   )
   if err != nil {
       return err
   }
   if _, err = deletedZoneOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   In the code, set the following parameters:

   * `Id`: ID of the DNS zone to delete.
   * `ResourceVersion` (optional): Version of the zone that you last checked, from its `Metadata.ResourceVersion`. If the zone changed and has a different version, the deletion fails. If you set it to `0`, the deletion uses the current version of the zone.

**Python SDK**

1. Get the ID of the zone that you want to delete. List the zones in the project, with `parent_id` set to the project ID:

   ```python theme={null}
   dns_zones_service = ZoneServiceClient(sdk)
   dns_zones_response = await dns_zones_service.list(
       ListZonesRequest(
           parent_id="<project_ID>",
       ),
   )
   print(dns_zones_response)
   ```

   Find the zone that you want to delete in `items`. The zone ID is in `metadata.id`.

2. Delete the zone:

   ```python theme={null}
   deleted_zone_service = ZoneServiceClient(sdk)
   deleted_zone_operation = await deleted_zone_service.delete(
       DeleteZoneRequest(
           id="<DNS_zone_ID>",
           resource_version=<resource_version>,
       ),
   )
   await deleted_zone_operation.wait()
   ```

   In the code, set the following parameters:

   * `id`: ID of the DNS zone to delete.
   * `resource_version` (optional): Version of the zone that you last checked, from its `metadata.resource_version`. If the zone changed and has a different version, the deletion fails. If you set it to `0`, the deletion uses the current version of the zone.

**JavaScript SDK**

1. Get the ID of the zone that you want to delete. List the zones in the project, with `parentId` set to the project ID:

   ```ts theme={null}
   const dnsZonesService = new ZoneService(sdk);
   const dnsZonesResponse = await dnsZonesService.list(
     ListZonesRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(dnsZonesResponse);
   ```

   Find the zone that you want to delete in `items`. The zone ID is in `metadata.id`.

2. Delete the zone:

   ```ts theme={null}
   const deletedZoneService = new ZoneService(sdk);
   const deletedZoneOperation = await deletedZoneService.delete(
     DeleteZoneRequest.create({
       id: "<DNS_zone_ID>",
       resourceVersion: <resource_version>,
     }),
   ).result;
   await deletedZoneOperation.wait();
   ```

   In the code, set the following parameters:

   * `id`: ID of the DNS zone to delete.
   * `resourceVersion` (optional): Version of the zone that you last checked, from its `metadata.resourceVersion`. If the zone changed and has a different version, the deletion fails. If you set it to `0`, the deletion uses the current version of the zone.
