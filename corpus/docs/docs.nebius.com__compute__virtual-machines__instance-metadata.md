# How to access VM metadata

Source: https://docs.nebius.com/compute/virtual-machines/instance-metadata

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to access VM metadata

The *instance metadata service* (IMDS) provides information about a running virtual machine (VM), including metadata, labels, resources, user and network data.

## How to access IMDS

IMDS is available only from within a VM itself.

Once you connect to a VM, use the following base URL to request metadata:

```
http://metadata.nebius.internal
```

All IMDS requests must use the `GET` method and include the `Metadata: true` header. Requests without this header return `400 Bad Request`. Requests that use any method other than `GET` return `405 Method Not Allowed`.

IMDS blocks requests containing any of the following forwarding headers and returns `403 Forbidden`:

* `X-Forwarded-For`
* `X-Forwarded-Host`
* `X-Real-IP`
* `Forwarded`

### Metadata updates

IMDS provides metadata captured at VM start time. The following endpoints are not refreshed in real time:

* `instance-data`
* `parent-data`
* `network-data`
* `user-data`

To get updated values from these endpoints after a change, stop and restart the VM.

> [!NOTE]
>
> Unlike the other endpoints, `instance-events` provides live updates and does not require a VM restart. A maintenance event may take up to five minutes to appear in the response.

## Example requests

The following examples show how to retrieve different types of metadata from IMDS.

### Getting all VM metadata

To get all available VM metadata in JSON format, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-data \
  -H "Metadata: true"
```

Example output:

```json theme={null}
{
  "id": "computeinstance-***",
  "parent_id": "project-***",
  "name": "example-vm",
  "hostname": "example-hostname",
  "platform": "gpu-h200-sxm",
  "preset": "1gpu-16vcpu-200gb",
  "labels": {
    "env": "example-env",
    "runners_count": "24"
  },
  "resource_version": 1,
  "created_at": "2025-11-11T08:03:31.754114Z",
  "service_account_id": "serviceaccount-***",
  "gpu_cluster_id": "computegpucluster-***",
  "infiniband_fabric": "fabric-5",
  "infiniband_topology_path": ["hash-1", "hash-2", "hash-3"],
  "region": "eu-west1"
}
```

`labels` is always returned as a JSON object. If no labels were set, IMDS returns an empty object.

The following fields are optional and are returned only when available for the VM:

* `hostname`
* `service_account_id`
* `gpu_cluster_id`
* `infiniband_fabric`
* `infiniband_topology_path`

### Getting a specific metadata field

To get a specific metadata field as plain text, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-data/<field> \
  -H "Metadata: true"
```

Example:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-data/id \
  -H "Metadata: true"
```

Example output:

```
computeinstance-***
```

### Getting VM labels

To get all labels for the VM, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-data/labels \
  -H "Metadata: true"
```

Example output:

```json theme={null}
{
  "env": "example-env",
  "runners_count": "24"
}
```

To get a specific label, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-data/labels/<label_name> \
  -H "Metadata: true"
```

Example:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-data/labels/env \
  -H "Metadata: true"
```

Example output:

```
example-env
```

### Getting parent resource metadata

To get parent resource metadata in JSON format, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/parent-data \
  -H "Metadata: true"
```

Example output:

```json theme={null}
{
  "id": "project-***",
  "parent_id": "tenant-***",
  "name": "example-project",
  "created_at": "2025-11-11T08:03:30.754114Z",
  "labels": {
    "teamcity_build_id": "13672974"
  }
}
```

> [!NOTE]
>
> To access `parent-data`, the VM must have an attached service account with permissions to read the parent resource metadata. Otherwise, the request returns `403 Forbidden`.

### Getting user data

To get the user data that was provided when the VM was created, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/user-data \
  -H "Metadata: true"
```

Example output:

```yaml theme={null}
#cloud-config
package_update: true
packages:
  - nginx
runcmd:
  - systemctl enable --now nginx
```

### Getting network data

To get the VM network data, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/network-data \
  -H "Metadata: true"
```

This request returns the network data that cloud-init used to initialize the VM during its first boot.

Example output:

```yaml theme={null}
version: 2
ethernets:
  interface0:
    match:
      macaddress: "XX:XX:XX:XX:XX:XX"
    set-name: "eth0"
    dhcp4: true
    mtu: 1450
```

### Getting service account information

To get information about the service account attached to the VM and its IAM token, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/iam/sa \
  -H "Metadata: true"
```

Example output:

```json theme={null}
{
  "service_account_id": "serviceaccount-***",
  "token": {
    "access_token": "<access_token>",
    "expires_at": "2027-01-01T00:00:00Z"
  }
}
```

To get only the IAM token object (the access token and its expiration time), run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/iam/sa/token \
  -H "Metadata: true"
```

Example output:

```json theme={null}
{
  "access_token": "<access_token>",
  "expires_at": "2027-01-01T00:00:00Z"
}
```

To get only the raw access token string, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/iam/sa/token/access_token \
  -H "Metadata: true"
```

Example output:

```
<access_token>
```

### Getting maintenance events

To check if a maintenance event is scheduled for the VM, run:

```bash theme={null}
curl http://metadata.nebius.internal/v1/instance-events \
  -H "Metadata: true"
```

Example output:

```json theme={null}
{
  "data": [
    {
      "id": "computemaintenance-***",
      "type": "maintenance",
      "status": "scheduled",
      "created_at": "2026-02-28T15:10:00Z",
      "not_before": "2026-03-01T10:00:00Z",
      "extra": {
        "support_center_ticket_id": "123456",
        "is_planned": "false"
      }
    }
  ]
}
```

If there are no active maintenance events, IMDS returns an empty array:

```json theme={null}
{
  "data": []
}
```

## Request throttling

Nebius AI Cloud applies throttling to IMDS requests on a per-VM basis to reduce accidental overload and abuse:

* 10 requests per second for regular requests
* 20 requests per second for burst requests

If you exceed the limit, IMDS returns `429 Too Many Requests`.

## Status codes

| HTTP status code | Description |
| - | - |
| `200 OK` | The request succeeded. |
| `400 Bad Request` | The `Metadata: true` header is missing or invalid. |
| `403 Forbidden` | The VM does not have permission to access the requested resource. |
| `404 Not Found` | The requested resource or field does not exist. |
| `405 Method Not Allowed` | The request used a method other than `GET`. |
| `429 Too Many Requests` | The request rate limit was exceeded. Retry the request. |
| `500 Internal Server Error` | The server encountered an error. Retry the request. |
| `501 Not Implemented` | The requested feature is not implemented. |
| `503 Service Unavailable` | The service is temporarily unavailable, or the request could not be attributed to this VM. Retry the request. |
