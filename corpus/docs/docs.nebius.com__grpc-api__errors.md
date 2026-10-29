# Errors in the gRPC API

Source: https://docs.nebius.com/grpc-api/errors

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Errors in the gRPC API

When a request fails, the Nebius AI Cloud API returns a status code and an error message. For example:

```bash theme={null}
grpcurl -rpc-header "Authorization: Bearer <access_token>" \
   compute.api.nebius.cloud:443 \
   nebius.compute.v1.InstanceService/Create

ERROR:
  Code: InvalidArgument
  Message: invalid resource size type: <nil>
```

The response includes the following:

* `Code`: Canonical gRPC status code.
* `Message`: Description of the error.

The Nebius AI Cloud API only uses canonical codes in the [full list of gRPC status codes](https://grpc.io/docs/guides/status-codes/#the-full-list-of-status-codes). The following table describes the possible status codes:

| gRPC status code | Description |
| - | - |
| `0 OK` | The request completed successfully. |
| `1 CANCELLED` | You canceled the request. |
| `2 UNKNOWN` | An unexpected exception or an error in parsing a gRPC status occurred (for example, the status code is outside the 0–16 range). |
| `3 INVALID_ARGUMENT` | The request is invalid or is out of the service constraints. Make sure that you specified the method, headers and request body correctly. |
| `4 DEADLINE_EXCEEDED` | The request timed out. For requests that change the state of the system, this error may occur even if the request completed successfully but the response was delayed. |
| `5 NOT_FOUND` | The requested resource doesn't exist. For example, it may have been deleted. Make sure that you address an existing resource — check its ID or name in the request. |
| `6 ALREADY_EXISTS` | The resource with the specified parameters already exists. For example, you try to create a virtual machine with the same name as an existing virtual machine. To fix the error, use a different name. |
| `7 PERMISSION_DENIED` | You don't have permission to perform the request. Check that you have the required IAM role. This error is different from `16 UNAUTHENTICATED` because `7 PERMISSION_DENIED` indicates a missing role, while `16 UNAUTHENTICATED` points to incorrect credentials. |
| `8 RESOURCE_EXHAUSTED` | The [quotas](https://docs.nebius.com/overview/quotas.md) of the requested resources are exhausted. Clean up the resources or increase the quotas. If the request tries to exceed the service constraints, another error `3 INVALID_ARGUMENT` occurs. |
| `9 FAILED_PRECONDITION` | The request can't be performed because of the current state of resources. For example, the service only allows deleting empty directories, but you attempt to delete a non-empty one. In that case, first delete resources within the directory and then delete the directory itself. |
| `10 ABORTED` | The request is aborted, usually due to a concurrency issue such as a resource version mismatch. |
| `11 OUT_OF_RANGE` | The request attempts to use a value outside the valid parameter range. Change the value so it's within the range. |
| `12 UNIMPLEMENTED` | The requested method hasn't been implemented yet. |
| `13 INTERNAL` | An important system condition isn't met. |
| `14 UNAVAILABLE` | The service is unavailable. Try again later. |
| `16 UNAUTHENTICATED` | The request is sent with invalid authentication credentials. Check your credentials. This error is different from `7 PERMISSION_DENIED` because `16 UNAUTHENTICATED` only checks the credentials, not roles. |

The list doesn't include the `15 DATA_LOSS` error because the gRPC API by Nebius AI Cloud never returns it.
