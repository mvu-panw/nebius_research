# Managing DNS records

Source: https://docs.nebius.com/vpc/dns/manage-records

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing DNS records

In a custom [DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md), you can create DNS records that resolve from inside the [network](https://docs.nebius.com/vpc/overview.md#network) attached to the zone. This page shows how to create, update and delete DNS records.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. [Create a custom DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md) to which to add records.

**CLI**

1. [Install and configure the Nebius AI Cloud CLI](https://docs.nebius.com/cli/quickstart.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create a custom DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md) to which to add records.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create a custom DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md) to which to add records.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create a custom DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md) to which to add records.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create a custom DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md) to which to add records.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create a custom DNS zone](https://docs.nebius.com/vpc/dns/manage-zones.md) to which to add records.

## Record types

A record stores its data in the **Data** parameter as the RDATA part of the record in the [presentation (zonefile) format](https://datatracker.ietf.org/doc/html/rfc9499#name-resource-records). For example, for a `www 600 IN A 192.0.2.10` resource record in a zonefile, the record data is `192.0.2.10`.

You can create the following record types in a custom DNS zone:

| Type | Example data value | Format |
| - | - | - |
| `a` | `192.0.2.10` | IPv4 address |
| `mx` | `10 mail.my.example.` | Priority and mail server domain name |
| `txt` | `"v=spf1 -all"` | One or more quoted text strings |
| `srv` | `10 5 5060 sip.my.example.` | Priority, weight, port and target domain name |
| `caa` | `0 issue "letsencrypt.org"` | Flags, tag and quoted value |
| `svcb` | `1 backend.my.example. port=8080` | Priority, target domain name and service parameters |
| `https` | `1 backend.my.example. alpn=h2` | Priority, target domain name and service parameters |

The following record types are restricted:

* `ns`: Custom DNS zones do not support delegation. Nebius AI Cloud creates an NS record at the zone apex together with the zone. You cannot create, update or delete NS records.
* `soa`: Each zone contains exactly one SOA record that Nebius AI Cloud creates together with the zone. You cannot create additional SOA records or delete the existing one. To control how long resolvers cache a "record not found" response, [set the zone's negative caching time-to-live (TTL)](https://docs.nebius.com/vpc/dns/manage-zones.md#creating-dns-zones). This value appears in the last field of the SOA record data.
* `cname`: CNAME records are not supported. Instead of an alias, create a record of the required type directly at that name, for example, an `a` record with the target's IP address.
* `aaaa`: AAAA records are not supported in custom DNS zones.

> [!NOTE]
>
> In Terraform, write the record type in uppercase, for example, `A` or `TXT`. The provider rejects the lowercase values that the CLI uses.

## Creating DNS records

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.

2. On the **DNS** tab, select the zone to which you want to add records.

3. Click **Create record**.

4. In **Relative domain name**, enter the zone-relative name of the record, for example, `www` for `www.<zone_domain_name>`. Use `@` to create the record at the zone apex. Use `*` as the leftmost label to create a wildcard record that answers queries for names that do not otherwise exist in the zone.

5. In **Record type**, select the [record type](#record-types) and fill the fields that appear:

   > **A**
   >
   > * **IPv4 address**: IPv4 address to which the name resolves.

   > **MX**
   >
   > * **Hostname**: Hostname of the mail server.
   > * **Priority**: Priority of the mail server.

   > **TXT**
   >
   > * **Value**: Text to store in the record.
   >
   > For email records such as DMARC and SPF, split text longer than 255 characters into multiple quoted blocks of 1–255 characters each.

   > **SRV**
   >
   > * **Target**: Hostname of the target server.
   > * **Priority**: Priority of the target host.
   > * **Weight**: Relative weight of the target host among records with the same priority.
   > * **Port**: Port on which the service is available.
   > * **Protocol** (optional): Protocol used by the service, for example, `_tcp` or `_udp`.
   > * **Service** (optional): Name of the service.

   > **CAA**
   >
   > * **Value**: Value associated with the selected tag.
   > * **Flag**: CAA record flag.
   > * **Tag**: Tag type. Select `issue`, `issuewild` or `iodef`.

   > **SVCB**
   >
   > * **Target**: Hostname of the service endpoint.
   > * **Priority**: Priority of the service endpoint.
   > * **Parameters** (optional): Service parameters.

   > **HTTPS**
   >
   > * **Target**: Hostname of the HTTPS service endpoint.
   > * **Priority**: Priority of the HTTPS service endpoint.
   > * **Parameters** (optional): Service parameters.

6. (Optional) In **TTL**, enter how long DNS resolvers can cache the record, in seconds.

7. (Optional) Enable **Delete protection** to protect the record from accidental deletion.

8. Click **Create record**.

**CLI**

To create a DNS record, run the following command:

```bash theme={null}
nebius dns record create \
  --parent-id <DNS_zone_ID> \
  --name <name> \
  --relative-name <relative_name> \
  --type <record_type> \
  --data <record_data> \
  --ttl <TTL>
```

In the command, specify the following parameters:

* `--parent-id`: ID of the DNS zone to create the record in. To get zone IDs, run `nebius dns zone list`.

* `--name` (optional): Name of the record resource. This is not the domain name of the record. The resource name identifies the record in Nebius AI Cloud and lets you look the record up by name. The name must be unique within the zone. Records that Nebius AI Cloud creates automatically have no resource name.

* `--relative-name`: Zone-relative name of the record, for example, `www` for `www.<zone_domain_name>`. Use `@` to create the record at the zone apex. Use `*` as the leftmost label to create a wildcard record that answers queries for names that do not otherwise exist in the zone. You cannot change the relative name after the record is created.

* `--type`: [Record type](#record-types). You cannot change the type after the record is created.

* `--data`: Record data in the format that corresponds to the [record type](#record-types). Each record holds one value. To serve several values for the same name, for example, several IP addresses in a round robin, create several records with the same relative name and type. Their data must differ; creating a record that repeats the relative name, type and data of an existing record fails with an `AlreadyExists` error.

  Write domain names in `--data` in fully qualified form with a trailing dot, for example, `service.my.example.`. For TXT records, enclose the values in double quotes. For SVCB and HTTPS records, specify the target as a domain name. The `.` shorthand for the record's own name is not supported.

* `--ttl` (optional): Time-to-live in seconds. How long resolvers cache the record before querying again. Default: `600`. Give records that share a relative name and type the same TTL, because resolvers handle a set with mixed TTLs inconsistently.

* `--labels` (optional): Labels in the `key=value` format.

The output looks like the following:

```yaml theme={null}
metadata:
  id: dnsrecord-e00**
  parent_id: dnszone-e00**
  name: www-a-record
  resource_version: "126446"
  created_at: "2026-07-08T14:15:01.805225Z"
  updated_at: "2026-07-08T14:15:01.805225Z"
spec:
  relative_name: www
  type: A
  ttl: "600"
  data: 192.0.2.10
status:
  zone_domain_name: my.example.
  effective_fqdn: www.my.example.
```

The returned resource shows the parameters you specified and the following:

* `status.effective_fqdn` is the absolute domain name that the record resolves at: the relative name joined with the zone domain name. You need this value to [verify the DNS record](#verifying-dns-records).
* `metadata.resource_version` is the current version of the record. If you later update or delete the record, you can pass this value in `--resource-version` to make sure that the command applies only to this version of the record.

To protect a record from accidental deletion, add the `--deletion-protection` parameter:

```bash theme={null}
nebius dns record create \
  --parent-id <DNS_zone_ID> \
  --name spf-record \
  --relative-name "@" \
  --type txt \
  --data '"v=spf1 -all"' \
  --ttl 3600 \
  --deletion-protection
```

With `--deletion-protection` enabled, you can [delete](#deleting-dns-records) a protected record only by using the `--force` parameter.

**Terraform**

1. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_dns_v1_record" "my_record" {
     parent_id     = "<DNS_zone_ID>"
     name          = "<name>"
     relative_name = "<relative_name>"
     type          = "<record_type>"
     data          = "<record_data>"
     ttl           = <TTL>

     labels = {
       <key> = "<value>"
     }
   }
   ```

   In the configuration, specify the following parameters:

   * `parent_id`: ID of the DNS zone to create the record in. If you create a record in the same configuration file where the DNS zone configuration is located, refer to this zone as `nebius_dns_v1_zone.my_zone.id`.

   * `name` (optional): Name of the record resource. This is not the domain name of the record. The resource name identifies the record in Nebius AI Cloud and lets you look the record up by name. The name must be unique within the zone. Records that Nebius AI Cloud creates automatically have no resource name.

   * `relative_name`: Zone-relative name of the record, for example, `www` for `www.<zone_domain_name>`. Use `@` to create the record at the zone apex. Use `*` as the leftmost label to create a wildcard record that answers queries for names that do not otherwise exist in the zone. You cannot change the relative name after the record is created.

   * `type`: [Record type](#record-types) in uppercase, for example, `A`. You cannot change the type after the record is created.

   * `data`: Record data in the format that corresponds to the [record type](#record-types). Each record holds one value. To serve several values for the same name, for example, several IP addresses in a round robin, create several records with the same relative name and type. Their data must differ; creating a record that repeats the relative name, type and data of an existing record fails with an `AlreadyExists` error.

     Write domain names in `data` in fully qualified form with a trailing dot, for example, `service.my.example.`. For TXT records, enclose the values in double quotes and escape them, for example, `data = "\"v=spf1 -all\""`. For SVCB and HTTPS records, specify the target as a domain name. The `.` shorthand for the record's own name is not supported.

   * `ttl` (optional): Time-to-live in seconds, as a number without quotes. How long resolvers cache the record before querying again. Default: `600`. Give records that share a relative name and type the same TTL, because resolvers handle a set with mixed TTLs inconsistently.

   * `labels` (optional): Labels in the `key = "value"` format.

   For all the parameters of the resource, see [nebius\_dns\_v1\_record](https://docs.nebius.com/terraform-provider/reference/resources/dns_v1_record.md) in the Terraform provider reference.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

To protect a record from accidental deletion, add the `deletion_protection` attribute:

```hcl theme={null}
resource "nebius_dns_v1_record" "my_protected_record" {
  parent_id     = "<DNS_zone_ID>"
  name          = "spf-record"
  relative_name = "@"
  type          = "TXT"
  data          = "\"v=spf1 -all\""
  ttl           = 3600

  deletion_protection = true
}
```

If you want to delete this record later, set `deletion_protection` to `false`, apply the changes and then [delete the record](#deleting-dns-records).

**Go SDK**

Run the following code:

```go theme={null}
dnsRecordService := sdk.Services().DNS().V1().
    Record()
dnsRecordOperation, err := dnsRecordService.Create(
    ctx,
    &dns.CreateRecordRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<DNS_zone_ID>",
            Name: "<name>",
        },
        Spec: &dns.RecordSpec{
            RelativeName: "<relative_name>",
            Type: dns.RecordSpec_A,
            Data: "<record_data>",
            Ttl: <TTL>,
        },
    },
)
if err != nil {
    return err
}
if _, err = dnsRecordOperation.Wait(ctx); err != nil {
    return err
}
dnsRecordID := dnsRecordOperation.ResourceID()
fmt.Println(dnsRecordOperation)
```

In the code, set the following parameters:

* `Metadata.ParentId`: ID of the DNS zone to create the record in.

* `Metadata.Name` *(optional)*: Name of the record resource. This is not the domain name of the record. The resource name identifies the record in Nebius AI Cloud and lets you look the record up by name. The name must be unique within the zone. Records that Nebius AI Cloud creates automatically have no resource name.

* `Spec.RelativeName`: Zone-relative name of the record, for example, `www` for `www.<zone_domain_name>`. Use `@` to create the record at the zone apex. Use `*` as the leftmost label to create a wildcard record that answers queries for names that do not otherwise exist in the zone. You cannot change the relative name after the record is created.

* `Spec.Type`: [Record type](#record-types). The example uses `dns.RecordSpec_A`. You cannot change the type after the record is created.

* `Spec.Data`: Record data in the format that corresponds to the [record type](#record-types). Each record holds one value. To serve several values for the same name, for example, several IP addresses in a round robin, create several records with the same relative name and type. Their data must differ; creating a record that repeats the relative name, type and data of an existing record fails with an `AlreadyExists` error.

  Write domain names in `Spec.Data` in fully qualified form with a trailing dot, for example, `service.my.example.`. For TXT records, enclose the values in double quotes. For SVCB and HTTPS records, specify the target as a domain name. The `.` shorthand for the record's own name is not supported.

* `Spec.Ttl` *(optional)*: Time-to-live in seconds. How long resolvers cache the record before querying again. Default: `600`. Give records that share a relative name and type the same TTL, because resolvers handle a set with mixed TTLs inconsistently.

The code saves the record ID to `dnsRecordID`. The record's `Status.EffectiveFqdn` is the absolute domain name that the record resolves at: the relative name joined with the zone domain name. You need this value to [verify the DNS record](#verifying-dns-records).

To protect a record from accidental deletion, set `Spec.DeletionProtection` to `true`:

```go theme={null}
protectedRecordService := sdk.Services().DNS().V1().
    Record()
protectedRecordOperation, err := protectedRecordService.Create(
    ctx,
    &dns.CreateRecordRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<DNS_zone_ID>",
            Name: "spf-record",
        },
        Spec: &dns.RecordSpec{
            RelativeName: "@",
            Type: dns.RecordSpec_TXT,
            Data: "\"v=spf1 -all\"",
            Ttl: 3600,
            DeletionProtection: true,
        },
    },
)
if err != nil {
    return err
}
if _, err = protectedRecordOperation.Wait(ctx); err != nil {
    return err
}
protectedRecordID := protectedRecordOperation.ResourceID()
fmt.Println(protectedRecordOperation)
```

With `Spec.DeletionProtection` enabled, you can [delete](#deleting-dns-records) a protected record only by setting `Force` to `true`.

**Python SDK**

Run the following code:

```python theme={null}
dns_record_service = RecordServiceClient(sdk)
dns_record_operation = await dns_record_service.create(
    CreateRecordRequest(
        metadata=ResourceMetadata(
            parent_id="<DNS_zone_ID>",
            name="<name>",
        ),
        spec=RecordSpec(
            relative_name="<relative_name>",
            type=RecordSpec.RecordType.A,
            data="<record_data>",
            ttl=<TTL>,
        ),
    ),
)
await dns_record_operation.wait()
dns_record_id = dns_record_operation.resource_id
print(dns_record_operation)
```

In the code, set the following parameters:

* `parent_id`: ID of the DNS zone to create the record in.

* `name` *(optional)*: Name of the record resource. This is not the domain name of the record. The resource name identifies the record in Nebius AI Cloud and lets you look the record up by name. The name must be unique within the zone. Records that Nebius AI Cloud creates automatically have no resource name.

* `relative_name`: Zone-relative name of the record, for example, `www` for `www.<zone_domain_name>`. Use `@` to create the record at the zone apex. Use `*` as the leftmost label to create a wildcard record that answers queries for names that do not otherwise exist in the zone. You cannot change the relative name after the record is created.

* `type`: [Record type](#record-types). The example uses `RecordSpec.RecordType.A`. You cannot change the type after the record is created.

* `data`: Record data in the format that corresponds to the [record type](#record-types). Each record holds one value. To serve several values for the same name, for example, several IP addresses in a round robin, create several records with the same relative name and type. Their data must differ; creating a record that repeats the relative name, type and data of an existing record fails with an `AlreadyExists` error.

  Write domain names in `data` in fully qualified form with a trailing dot, for example, `service.my.example.`. For TXT records, enclose the values in double quotes. For SVCB and HTTPS records, specify the target as a domain name. The `.` shorthand for the record's own name is not supported.

* `ttl` *(optional)*: Time-to-live in seconds. How long resolvers cache the record before querying again. Default: `600`. Give records that share a relative name and type the same TTL, because resolvers handle a set with mixed TTLs inconsistently.

The code saves the record ID to `dns_record_id`. The record's `status.effective_fqdn` is the absolute domain name that the record resolves at: the relative name joined with the zone domain name. You need this value to [verify the DNS record](#verifying-dns-records).

To protect a record from accidental deletion, set `deletion_protection` to `True`:

```python theme={null}
protected_record_service = RecordServiceClient(sdk)
protected_record_operation = await protected_record_service.create(
    CreateRecordRequest(
        metadata=ResourceMetadata(
            parent_id="<DNS_zone_ID>",
            name="spf-record",
        ),
        spec=RecordSpec(
            relative_name="@",
            type=RecordSpec.RecordType.TXT,
            data="\"v=spf1 -all\"",
            ttl=3600,
            deletion_protection=True,
        ),
    ),
)
await protected_record_operation.wait()
protected_record_id = protected_record_operation.resource_id
print(protected_record_operation)
```

With `deletion_protection` enabled, you can [delete](#deleting-dns-records) a protected record only by setting `force` to `True`.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const dnsRecordService = new RecordService(sdk);
const dnsRecordOperation = await dnsRecordService.create(
  CreateRecordRequest.create({
    metadata: {
      parentId: "<DNS_zone_ID>",
      name: "<name>",
    },
    spec: {
      relativeName: "<relative_name>",
      type: RecordSpec_RecordType.A,
      data: "<record_data>",
      ttl: <TTL>,
    },
  }),
).result;
await dnsRecordOperation.wait();
const dnsRecordId = dnsRecordOperation.resourceId();
console.log(dnsRecordOperation);
```

In the code, set the following parameters:

* `parentId`: ID of the DNS zone to create the record in.

* `name` *(optional)*: Name of the record resource. This is not the domain name of the record. The resource name identifies the record in Nebius AI Cloud and lets you look the record up by name. The name must be unique within the zone. Records that Nebius AI Cloud creates automatically have no resource name.

* `relativeName`: Zone-relative name of the record, for example, `www` for `www.<zone_domain_name>`. Use `@` to create the record at the zone apex. Use `*` as the leftmost label to create a wildcard record that answers queries for names that do not otherwise exist in the zone. You cannot change the relative name after the record is created.

* `type`: [Record type](#record-types). The example uses `RecordSpec_RecordType.A`. You cannot change the type after the record is created.

* `data`: Record data in the format that corresponds to the [record type](#record-types). Each record holds one value. To serve several values for the same name, for example, several IP addresses in a round robin, create several records with the same relative name and type. Their data must differ; creating a record that repeats the relative name, type and data of an existing record fails with an `AlreadyExists` error.

  Write domain names in `data` in fully qualified form with a trailing dot, for example, `service.my.example.`. For TXT records, enclose the values in double quotes. For SVCB and HTTPS records, specify the target as a domain name. The `.` shorthand for the record's own name is not supported.

* `ttl` *(optional)*: Time-to-live in seconds. How long resolvers cache the record before querying again. Default: `600`. Give records that share a relative name and type the same TTL, because resolvers handle a set with mixed TTLs inconsistently.

The code saves the record ID to `dnsRecordId`. The record's `status.effectiveFqdn` is the absolute domain name that the record resolves at: the relative name joined with the zone domain name. You need this value to [verify the DNS record](#verifying-dns-records).

To protect a record from accidental deletion, set `deletionProtection` to `true`:

```ts theme={null}
const protectedRecordService = new RecordService(sdk);
const protectedRecordOperation = await protectedRecordService.create(
  CreateRecordRequest.create({
    metadata: {
      parentId: "<DNS_zone_ID>",
      name: "spf-record",
    },
    spec: {
      relativeName: "@",
      type: RecordSpec_RecordType.TXT,
      data: "\"v=spf1 -all\"",
      ttl: 3600,
      deletionProtection: true,
    },
  }),
).result;
await protectedRecordOperation.wait();
const protectedRecordId = protectedRecordOperation.resourceId();
console.log(protectedRecordOperation);
```

With `deletionProtection` enabled, you can [delete](#deleting-dns-records) a protected record only by setting `force` to `true`.

## Verifying DNS records

DNS records resolve only from the [DNS zone's network](https://docs.nebius.com/vpc/dns/overview.md#dns-zones). To verify a record, query its fully qualified domain name (FQDN) from a virtual machine (VM) attached to one of the network's subnets.

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. On the **DNS** tab, find the zone that contains the record you want to verify. The **Network** column shows the zone's network.
3. Click the network name to view its subnets.
4. Return to the **DNS** tab and select the DNS zone.
5. Find the record and click  next to its FQDN.
6. [Connect to a VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) attached to one of the network's subnets.
7. Query the copied FQDN from the VM, for example:

   ```bash theme={null}
   dig www.my.example.
   ```

**CLI**

To verify a record in a custom DNS zone, [connect to a VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) attached to a subnet of the zone's network and query the FQDN from the record's `status.effective_fqdn`:

```bash theme={null}
dig www.my.example.
```

The VM resolves the name through the network resolver at `169.254.169.2` without additional configuration. The output contains the record data in the answer section:

```bash theme={null}
;; ANSWER SECTION:
www.my.example.    600    IN    A    192.0.2.10
```

A newly created record becomes visible within a minute. If you queried the name before creating the record, the resolver keeps returning the cached "record not found" response until the zone's [negative caching TTL](https://docs.nebius.com/vpc/dns/manage-zones.md#creating-dns-zones) expires, which takes 15 minutes by default.

## Updating DNS records

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. On the **DNS** tab, select the zone that contains the record you want to update.
3. Find the record and click .
4. Change the record data, **TTL** or **Delete protection**.
5. Click **Save changes**.

**CLI**

1. Get the ID of the record that you want to update. List the records in the zone:

   ```bash theme={null}
   nebius dns record list \
     --parent-id <DNS_zone_ID>
   ```

   Find the record you want to update and take its ID from the `.metadata.id` parameter. To list every record in one response instead of the first 100, add the `--all` parameter.

   If you set a resource name for the record when you created it, you can look it up by that name instead:

   ```bash theme={null}
   nebius dns record get-by-name \
     --parent-id <DNS_zone_ID> \
     --name <record_name>
   ```

   Here `--name` is the record's resource name from `metadata.name`, not its domain name.

2. Update the record:

   ```bash theme={null}
   nebius dns record update <record_ID> \
     --data <record_data> \
     --ttl <TTL>
   ```

   Specify the record ID you got in the previous step as `<record_ID>`. In the command, you can specify the following parameters to update them:

   * `--data` (optional): Record data in the format that corresponds to the [record type](#record-types).

   * `--ttl` (optional): Record TTL in seconds.

   * `--name` (optional): Name of the record resource.

   * `--deletion-protection` (optional): Protection from the record deletion. When enabled, you can delete a protected record only by using the `--force` parameter.

     Set to `false` to remove the protection.

   * `--labels` (optional): Replace all labels with the specified labels, in the `key=value` format.

   * `--labels-add` (optional): Add labels, in the `key=value` format, without replacing the existing labels.

   * `--labels-remove` (optional): Remove existing labels by key.

   * `--resource-version` (optional): Current version of the record from `metadata.resource_version`. If the record changed and has a different version, the command fails.

**Terraform**

1. In the configuration file, update the `nebius_dns_v1_record` resource:

   ```hcl theme={null}
   resource "nebius_dns_v1_record" "my_record" {
     name = "<name>"
     data = "<record_data>"
     ttl  = <TTL>

     labels = {
       <key> = "<value>"
     }

     deletion_protection = <true|false>

     # ...
   }
   ```

   You can update the following parameters:

   * `name`: Name of the record resource.
   * `data`: Record data in the format that corresponds to the [record type](#record-types).
   * `ttl`: Record TTL in seconds.
   * `labels`: Labels in the `key = "value"` format.
   * `deletion_protection`: Protection from the record deletion. When enabled, you cannot delete the record.

     Set to `false` to remove the protection.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the record that you want to update. List the records in the zone with `ParentId` set to the zone ID:

   ```go theme={null}
   dnsRecordsService := sdk.Services().DNS().V1().
       Record()
   dnsRecordsResponse, err := dnsRecordsService.List(
       ctx,
       &dns.ListRecordsRequest{
           ParentId: "<DNS_zone_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(dnsRecordsResponse)
   ```

   Find the record you want to update in `Items` and take its ID from `Metadata.Id`.

   If you set a resource name for the record when you created it, you can look it up by that name instead:

   ```go theme={null}
   namedRecordService := sdk.Services().DNS().V1().
       Record()
   namedRecord, err := namedRecordService.GetByName(
       ctx,
       &common.GetByNameRequest{
           ParentId: "<DNS_zone_ID>",
           Name: "<record_name>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(namedRecord)
   ```

   Here `Name` is the record's resource name from `Metadata.Name`, not its domain name.

2. Update the record:

   ```go theme={null}
   updatedRecordService := sdk.Services().DNS().V1().
       Record()
   updatedRecord, err := updatedRecordService.Get(
       ctx,
       &dns.GetRecordRequest{
           Id: "<record_ID>",
       },
   )
   if err != nil {
       return err
   }
   updatedRecord.Spec.Data = "<record_data>"
   updatedRecord.Spec.Ttl = <TTL>
   recordUpdateOperation, err := updatedRecordService.Update(
       ctx,
       &dns.UpdateRecordRequest{
           Metadata: updatedRecord.Metadata,
           Spec: updatedRecord.Spec,
       },
   )
   if err != nil {
       return err
   }
   if _, err = recordUpdateOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set `Id` to the record ID you got in the previous step. The code gets the record and updates the following parameters:

   * `Spec.Data`: Record data in the format that corresponds to the [record type](#record-types).
   * `Spec.Ttl`: Record TTL in seconds.

   To change other settings, such as `Metadata.Name`, `Metadata.Labels` or `Spec.DeletionProtection`, set them on `updatedRecord` before the update in the same way. Set `Spec.DeletionProtection` to `false` to remove the protection.

**Python SDK**

1. Get the ID of the record that you want to update. List the records in the zone with `parent_id` set to the zone ID:

   ```python theme={null}
   dns_records_service = RecordServiceClient(sdk)
   dns_records_response = await dns_records_service.list(
       ListRecordsRequest(
           parent_id="<DNS_zone_ID>",
       ),
   )
   print(dns_records_response)
   ```

   Find the record you want to update in `items` and take its ID from `metadata.id`.

   If you set a resource name for the record when you created it, you can look it up by that name instead:

   ```python theme={null}
   named_record_service = RecordServiceClient(sdk)
   named_record = await named_record_service.get_by_name(
       GetByNameRequest(
           parent_id="<DNS_zone_ID>",
           name="<record_name>",
       ),
   )
   print(named_record)
   ```

   Here `name` is the record's resource name from `metadata.name`, not its domain name.

2. Update the record:

   ```python theme={null}
   updated_record_service = RecordServiceClient(sdk)
   updated_record = await updated_record_service.get(
       GetRecordRequest(
           id="<record_ID>",
       ),
   )
   updated_record.spec.data = "<record_data>"
   updated_record.spec.ttl = <TTL>
   record_update_operation = await updated_record_service.update(
       UpdateRecordRequest(
           metadata=updated_record.metadata,
           spec=updated_record.spec,
       ),
   )
   await record_update_operation.wait()
   ```

   Set `id` to the record ID you got in the previous step. The code gets the record and updates the following parameters:

   * `spec.data`: Record data in the format that corresponds to the [record type](#record-types).
   * `spec.ttl`: Record TTL in seconds.

   To change other settings, such as `metadata.name`, `metadata.labels` or `spec.deletion_protection`, set them on `updated_record` before the update in the same way. Set `spec.deletion_protection` to `False` to remove the protection.

**JavaScript SDK**

1. Get the ID of the record that you want to update. List the records in the zone with `parentId` set to the zone ID:

   ```ts theme={null}
   const dnsRecordsService = new RecordService(sdk);
   const dnsRecordsResponse = await dnsRecordsService.list(
     ListRecordsRequest.create({
       parentId: "<DNS_zone_ID>",
     }),
   ).result;
   console.log(dnsRecordsResponse);
   ```

   Find the record you want to update in `items` and take its ID from `metadata.id`.

   If you set a resource name for the record when you created it, you can look it up by that name instead:

   ```ts theme={null}
   const namedRecordService = new RecordService(sdk);
   const namedRecord = await namedRecordService.getByName(
     GetByNameRequest.create({
       parentId: "<DNS_zone_ID>",
       name: "<record_name>",
     }),
   ).result;
   console.log(namedRecord);
   ```

   Here `name` is the record's resource name from `metadata.name`, not its domain name.

2. Update the record:

   ```ts theme={null}
   const updatedRecordService = new RecordService(sdk);
   const updatedRecord = await updatedRecordService.get(
     GetRecordRequest.create({
       id: "<record_ID>",
     }),
   ).result;
   updatedRecord.spec.data = "<record_data>";
   updatedRecord.spec.ttl = <TTL>;
   const recordUpdateOperation = await updatedRecordService.update(
     UpdateRecordRequest.create({
       metadata: updatedRecord.metadata,
       spec: updatedRecord.spec,
     }),
   ).result;
   await recordUpdateOperation.wait();
   ```

   Set `id` to the record ID you got in the previous step. The code gets the record and updates the following parameters:

   * `spec.data`: Record data in the format that corresponds to the [record type](#record-types).
   * `spec.ttl`: Record TTL in seconds.

   To change other settings, such as `metadata.name`, `metadata.labels` or `spec.deletionProtection`, set them on `updatedRecord` before the update in the same way. Set `spec.deletionProtection` to `false` to remove the protection.

The relative name and type of a record cannot be updated. To move a record to a different name or change its type, delete the record and create a new one.

An updated record becomes visible within a minute, and resolvers can serve the previous value until the record's TTL expires.

## Deleting DNS records

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.

2. On the **DNS** tab, select the zone that contains the record you want to delete.

3. If the record has deletion protection:

   1. Next to the record, click .
   2. Disable **Delete protection** and click **Save changes**.

4. Find the record and click  → **Delete**.

5. Confirm the deletion.

**CLI**

1. Get the ID of the record that you want to delete. List the records in the zone:

   ```bash theme={null}
   nebius dns record list \
     --parent-id <DNS_zone_ID>
   ```

   Find the record you want to delete and take its ID from the `.metadata.id` parameter. To list every record in one response instead of the first 100, add the `--all` parameter.

2. Delete the record:

   ```bash theme={null}
   nebius dns record delete <record_ID>
   ```

3. If the record is protected from deletion, the command fails with a `FailedPrecondition` error. To delete a protected record, add the `--force` parameter:

   ```bash theme={null}
   nebius dns record delete <record_ID> \
     --force
   ```

**Terraform**

1. If the record is protected from deletion, set `deletion_protection` to `false` in the `nebius_dns_v1_record` resource. Then, apply the changes. Otherwise, `terraform apply` fails with the `FailedPrecondition` error.
2. Remove the corresponding `nebius_dns_v1_record` resource from the configuration file.
3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the record that you want to delete. List the records in the zone with `ParentId` set to the zone ID:

   ```go theme={null}
   dnsRecordsService := sdk.Services().DNS().V1().
       Record()
   dnsRecordsResponse, err := dnsRecordsService.List(
       ctx,
       &dns.ListRecordsRequest{
           ParentId: "<DNS_zone_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(dnsRecordsResponse)
   ```

   Find the record you want to delete in `Items` and take its ID from `Metadata.Id`.

2. Delete the record. Set `Id` to the record ID:

   ```go theme={null}
   deletedRecordService := sdk.Services().DNS().V1().
       Record()
   deletedRecordOperation, err := deletedRecordService.Delete(
       ctx,
       &dns.DeleteRecordRequest{
           Id: "<record_ID>",
       },
   )
   if err != nil {
       return err
   }
   if _, err = deletedRecordOperation.Wait(ctx); err != nil {
       return err
   }
   ```

3. If the record is protected from deletion, the request fails with a `FailedPrecondition` error. To delete a protected record, set `Force` to `true`:

   ```go theme={null}
   forcedRecordService := sdk.Services().DNS().V1().
       Record()
   forcedRecordOperation, err := forcedRecordService.Delete(
       ctx,
       &dns.DeleteRecordRequest{
           Id: "<record_ID>",
           Force: true,
       },
   )
   if err != nil {
       return err
   }
   if _, err = forcedRecordOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the ID of the record that you want to delete. List the records in the zone with `parent_id` set to the zone ID:

   ```python theme={null}
   dns_records_service = RecordServiceClient(sdk)
   dns_records_response = await dns_records_service.list(
       ListRecordsRequest(
           parent_id="<DNS_zone_ID>",
       ),
   )
   print(dns_records_response)
   ```

   Find the record you want to delete in `items` and take its ID from `metadata.id`.

2. Delete the record. Set `id` to the record ID:

   ```python theme={null}
   deleted_record_service = RecordServiceClient(sdk)
   deleted_record_operation = await deleted_record_service.delete(
       DeleteRecordRequest(
           id="<record_ID>",
       ),
   )
   await deleted_record_operation.wait()
   ```

3. If the record is protected from deletion, the request fails with a `FailedPrecondition` error. To delete a protected record, set `force` to `True`:

   ```python theme={null}
   forced_record_service = RecordServiceClient(sdk)
   forced_record_operation = await forced_record_service.delete(
       DeleteRecordRequest(
           id="<record_ID>",
           force=True,
       ),
   )
   await forced_record_operation.wait()
   ```

**JavaScript SDK**

1. Get the ID of the record that you want to delete. List the records in the zone with `parentId` set to the zone ID:

   ```ts theme={null}
   const dnsRecordsService = new RecordService(sdk);
   const dnsRecordsResponse = await dnsRecordsService.list(
     ListRecordsRequest.create({
       parentId: "<DNS_zone_ID>",
     }),
   ).result;
   console.log(dnsRecordsResponse);
   ```

   Find the record you want to delete in `items` and take its ID from `metadata.id`.

2. Delete the record. Set `id` to the record ID:

   ```ts theme={null}
   const deletedRecordService = new RecordService(sdk);
   const deletedRecordOperation = await deletedRecordService.delete(
     DeleteRecordRequest.create({
       id: "<record_ID>",
     }),
   ).result;
   await deletedRecordOperation.wait();
   ```

3. If the record is protected from deletion, the request fails with a `FailedPrecondition` error. To delete a protected record, set `force` to `true`:

   ```ts theme={null}
   const forcedRecordService = new RecordService(sdk);
   const forcedRecordOperation = await forcedRecordService.delete(
     DeleteRecordRequest.create({
       id: "<record_ID>",
       force: true,
     }),
   ).result;
   await forcedRecordOperation.wait();
   ```

> [!NOTE]
>
> You cannot delete the zone's SOA record or the NS record at the zone apex. These records are deleted when you [delete the zone](https://docs.nebius.com/vpc/dns/manage-zones.md#deleting-dns-zones).
