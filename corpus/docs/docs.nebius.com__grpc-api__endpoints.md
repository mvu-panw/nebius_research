# Nebius AI Cloud API endpoints

Source: https://docs.nebius.com/grpc-api/endpoints

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius AI Cloud API endpoints

Nebius AI Cloud gRPC services are available at endpoints in the following format:

```
<service_name>.api.nebius.cloud:443
```

The value of `<service_name>` corresponds to the `api_service_name` parameter that is defined in the respective `.proto` file.

> For example, requests to [TokenExchangeService](https://github.com/nebius/api/blob/main/nebius/iam/v1/token_exchange_service.proto) from the `iam` API package must be sent to `tokens.iam.api.nebius.cloud:443`.

For the complete list of services and their endpoints, see [Services and their endpoints](https://github.com/nebius/api/blob/main/endpoints.md) on GitHub.

## OperationService endpoint

[OperationService](https://github.com/nebius/api/blob/main/nebius/common/v1/operation_service.proto) from the `common` API package does not have its own endpoint. It represents an operation as a result of some action in any service. For example, creating a virtual machine or changing settings of a Managed Service for Kubernetes® cluster both return an operation.

Use the same endpoint for OperationService as the service that initiated the operation.

> For example, if you performed an operation on a disk by using [DiskService](https://github.com/nebius/api/blob/main/nebius/compute/v1/disk_service.proto) from the compute API package, use `compute.api.nebius.cloud:443` to check that the operation is successful.
