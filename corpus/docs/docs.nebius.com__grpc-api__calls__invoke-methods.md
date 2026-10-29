# How to invoke a Nebius AI Cloud API method by using gRPCurl

Source: https://docs.nebius.com/grpc-api/calls/invoke-methods

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to invoke a Nebius AI Cloud API method by using gRPCurl

To manually invoke or debug a Nebius AI Cloud gRPC API method, you can send an authenticated gRPC request with `grpcurl`:

1. Get an access token for authentication:

   ```bash theme={null}
   nebius iam get-access-token
   ```

2. In the [services and endpoints list](https://github.com/nebius/api/blob/main/endpoints.md), find a gRPC service that you want to send a request to, and determine its endpoint.

   For example, to get a list of virtual machines (VMs) in a project, use the following:

   * `compute.api.nebius.cloud:443` endpoint for the Compute service.
   * `nebius.compute.v1.InstanceService` gRPC service for VMs.

   For more information, see [How to define an endpoint](https://docs.nebius.com/grpc-api/endpoints/define.md).

3. To check what the request body should contain, open the `***_service.proto` file of the selected endpoint. You can open it from the same [services and endpoints list](https://github.com/nebius/api/blob/main/endpoints.md).

   For example, to get a list of VMs in a project, use the `ListInstancesRequest` message. It requires the `parent_id` parameter (the ID of your project).

4. Send the `grpcurl` request with the request body and authorization header.

   For example, to get a list of VMs, you can run the following `grpcurl` command:

   ```bash theme={null}
   grpcurl -rpc-header "Authorization: Bearer <access_token>" \
      -d '{
            "parent_id": "project-e***"
          }' \
      compute.api.nebius.cloud:443 \
      nebius.compute.v1.InstanceService/List
   ```
