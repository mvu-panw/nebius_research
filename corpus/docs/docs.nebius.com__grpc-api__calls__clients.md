# Generating clients for the Nebius AI Cloud API from the proto files

Source: https://docs.nebius.com/grpc-api/calls/clients

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Generating clients for the Nebius AI Cloud API from the proto files

To make gRPC API calls to Nebius AI Cloud services in your code, you can generate API clients from the Protocol Buffer specifications hosted on [GitHub](https://github.com/nebius/api/).

The proto files come with a configuration file for [Buf](https://buf.build/docs/). To generate an API client by using the Buf CLI:

1. [Install the Buf CLI](https://buf.build/docs/installation/) for macOS or Linux, for example, by using Homebrew:

   ```bash theme={null}
   brew install bufbuild/buf/buf
   ```

2. Clone the [Nebius AI Cloud API repository](https://github.com/nebius/api/) and view the [Nebius AI Cloud Buf configuration](https://github.com/nebius/api/blob/main/buf.gen.yaml):

   ```bash theme={null}
   git clone https://github.com/nebius/api.git
   cd api
   cat buf.gen.yaml
   ```

3. Edit the configuration to keep only the programming languages you support. For example, for Java only:

   ```yaml theme={null}
   version: v2
   plugins:
     - remote: buf.build/protocolbuffers/java
       out: gen/java
     - remote: buf.build/grpc/java
       out: gen/java
   ```

4. To generate the client code, run the following command:

   ```bash theme={null}
   buf generate
   ```

5. To get the generated client code, go to the `gen/<language>` directory. For example, if you generated a Java client, go to `gen/java`.
