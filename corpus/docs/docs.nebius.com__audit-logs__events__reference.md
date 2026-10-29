# Structure and fields of events in Audit Logs

Source: https://docs.nebius.com/audit-logs/events/reference

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Structure and fields of events in Audit Logs

Each event in Audit Logs has a JSON representation that conforms to the [CloudEvents specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md).

## JSON structure

> [!WARNING]
>
> This JSON is provided for reference purposes and is not a valid example of an event JSON. It contains pairs of fields that cannot occur together in a single event JSON: either `.authentication.subject.tenant_user_id` or `.authentication.subject.service_account_id`, and either `.authentication.token_credential` or `.authentication.static_key`.

```json theme={null}
{
  "id": "ba989c6d-d6fb-***",
  "source": "nebius.registry.v1.RegistryService/Update",
  "specversion": "1.0",
  "type": "ai.nebius.registry.registry.update",
  "service": {
    "name": "REGISTRY"
  },
  "action": "UPDATE",
  "time": "2025-03-25T17:29:22.024775156Z",
  "event_version": "1.04",
  "authentication": {
    "authenticated": true,
    "subject": {
      "tenant_user_id": "tenantuseraccount-***",
      "service_account_id": "serviceaccount-***",
      "name": "Jane Doe"
    },
    "federation": {
      "id": "federation-***",
      "name": "Acme Inc."
    },
    "authentication_type": "ACCESS_TOKEN",
    "token_credential": {
      "masked_token": "ne1cV***"
    },
    "static_key": {
      "id": "NAKI3UCA***"
    }
  },
  "authorization": {
    "authorized": true
  },
  "resource": {
    "metadata": {
      "id": "registry-***",
      "name": "test-registry",
      "type": "registry"
    },
    "hierarchy": [
      {
        "id": "tenant-***",
        "name": "tenant-***",
        "type": "tenant"
      },
      {
        "id": "project-***",
        "name": "test-project",
        "type": "project"
      }
    ],
    "state": {
      "previous": {
        "metadata": { ... },
        "spec": { ... },
        "status": { ... }
      },
      "current": {
        "metadata": { ... },
        "spec": { ... },
        "status": { ... }
      }
    }
  },
  "request": {
    "request_id": "481f7089-f6b0-***",
    "parameters": { ... },
    "idempotency_id": "38bceb03-610a-***",
    "trace_id": "313d***"
  },
  "response": {
    "status_code": "RESOURCE_EXHAUSTED",
    "error_message": "",
    "payload": { ... }
  },
  "status": "ERROR"
}
```

## Fields

Fields marked with \* are [required context attributes](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md#required-attributes) from the CloudEvents specification.

* `.id`\*

  The event identifier.

* `.source`\*

  The name of the event source; that is, the [gRPC API](https://docs.nebius.com/grpc-api/index.md) method of Nebius AI Cloud that the subject used to perform the action, for example, `nebius.iam.v1.ServiceAccountService/List`.

* `.specversion`\*

  The version of the [CloudEvents specification](https://github.com/cloudevents/spec) that the event uses. For more details, see [specversion](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md#specversion) in the list of CloudEvents context attributes.

* `.type`\*

  The event type. All types contain the `ai.nebius` prefix and reference Nebius AI Cloud services, types of resources in them and actions performed on these resources. For example, `ai.nebius.iam.service_account.list`.

* `.service.name`

  The name of the service where the event occurred. For the list of services and their `.service.name` values, see [Nebius AI Cloud services supported by Audit Logs](https://docs.nebius.com/audit-logs/services.md).

* `.action`

  The action type: `CREATE`, `UPDATE`, `DELETE`, etc.

* `.time`

  The timestamp of the event in the [RFC 3339 format](https://datatracker.ietf.org/doc/html/rfc3339#section-5.8). For example, `2025-03-25T17:29:22.024775156Z`.

* `.event_version`

  The version of Audit Logs event specification that the event uses. Format: `<major>.<minor>`; for example, `1.04`. Specifications with the same major version and different minor versions are backwards-compatible, but specifications with different major versions are not.

* `.authentication`

  The details about the subject that performed the action and how Nebius AI Cloud authenticated it:

  * `.authentication.authenticated`

    A Boolean that shows whether the authentication was successful.

  * `.authentication.subject`

    The details about the subject (the user account or the service account):

    * `.authentication.subject.name`

      The name of a service account or the email of a user account. If the service account name is `Nebius`, the event was triggered by Nebius as part of maintenance or a support investigation.

    * `.authentication.subject.tenant_user_id`

      The user account ID, with the `tenantuseraccount-` prefix.

    * `.authentication.subject.service_account_id`

      The service account ID, with the `serviceaccount-` prefix. For the `Nebius` service account, only the name is shown.

    > [!NOTE]
    >
    > Only `.authentication.subject.tenant_user_id` or `.authentication.subject.service_account_id` is included, depending on the type of the subject account.

  * `.authentication.federation`

    The details about the Nebius AI Cloud federation that the subject user account authenticated with:

    * `.authentication.federation.id`

      The federation ID, with the `federation-` prefix.

    * `.authentication.federation.name`

      The federation name.

  * `.authentication.authentication_type`

    The type of the credentials that the subject authenticated with: `ACCESS_TOKEN` for [access tokens](https://docs.nebius.com/iam/authorization/access-tokens.md) or `STATIC_KEY` for AWS-compatible [access keys](https://docs.nebius.com/iam/service-accounts/access-keys.md).

  * `.authentication.token_credential.masked_token`

    The access token without the signature.

  * `.authentication.static_key.id`

    The access key ID.

  > [!NOTE]
  >
  > Only `.authentication.token_credential` or `.authentication.static_key` is included, depending on the type of the credentials.

* `.authorization.authorized`

  A Boolean that shows whether Nebius AI Cloud successfully authorized the subject to perform the action.

* `.resource`

  The details about the resource on which the action was performed:

  * `.resource.metadata`

    The resource metadata:

    * `.resource.metadata.id`

      The ID of the resource.

    * `.resource.metadata.name`

      The name of the resource.

    * `.resource.metadata.type`

      The resource type. For example, `vpcallocation`.

  * `.resource.hierarchy`

    The list of the resource's ancestors, from tenant to parent. For example, ancestors of a Managed Service for PostgreSQL® cluster are the tenant and a project in the tenant. Each element of the list has the same fields as `.resource.metadata`: `.id`, `.name` and `.type`.

  * `.resource.state.previous`

    The state of the resource before the `UPDATE` or `DELETE` action. The state may contain, for example, the resource's metadata (`.metadata`), specification (`.spec`) and status (`.status`).

  * `.resource.state.current`

    The state of the resource after the `CREATE` or `UPDATE` action. For more information about states, see the description of `.resource.state.previous`.

* `.request`

  The metadata of the request from the subject to Nebius AI Cloud:

  * `.request.request_id`

    The request UUID. Each request, including requests that retry the same action, has a unique ID.

  * `.request.parameters`

    Parameters provided in the API call that triggered the action.

  * `.request.idempotency_id`

    The idempotency UUID of the request. When two requests are retries of the same action, they have the same idempotency ID.

  * `.request.trace_id`

    The [trace-id](https://www.w3.org/TR/trace-context/#trace-id) of the request. It is used to identify the [distributed trace](https://www.w3.org/TR/trace-context/#dfn-distributed-traces) of the event: a set of calls that were made between Nebius AI Cloud systems and components when the subject requested to perform the action.

* `.response`

  The status of the response from Nebius AI Cloud to the subject:

  * `.response.status_code`

    The [gRPC status code](https://grpc.io/docs/guides/status-codes/) returned in the response.

  * `.response.error_message`

    The error message. If `.response.status_code` is `OK`, the message is empty.

  * `.response.payload`

    Data returned by the system in response to the API call.

* `.status`

  The status of the Nebius AI Cloud operation associated with the event: `STARTED`, `DONE` or `ERROR`.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
