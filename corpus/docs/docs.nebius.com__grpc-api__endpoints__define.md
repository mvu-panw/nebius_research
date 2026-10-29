# How to define an endpoint

Source: https://docs.nebius.com/grpc-api/endpoints/define

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to define an endpoint

To call a Nebius AI Cloud gRPC service, construct its endpoint from the service name defined in the API proto files.

1. In the [Nebius AI Cloud API repository](https://github.com/nebius/api/tree/main/nebius), find and open the `.proto` file of the required service.

2. Find the value of the `api_service_name` option.

   The `.proto` file of [OperationService](https://docs.nebius.com/grpc-api/endpoints/index.md#operationservice-endpoint) does not contain the `api_service_name` option because the service does not have its own endpoint. Use the endpoint of the service that initiated the operation.

3. Paste the value into the endpoint format: `<service_name>.api.nebius.cloud:443`.

4. Send a gRPC request to the resulting endpoint.

## Example

To define the endpoint for `TokenExchangeService`:

1. Open the service [.proto file](https://github.com/nebius/api/blob/main/nebius/iam/v1/token_exchange_service.proto).
2. Copy the value of the `api_service_name` option. In this example, it is `tokens.iam`.
3. Paste the value into the endpoint format: `tokens.iam.api.nebius.cloud:443`.
