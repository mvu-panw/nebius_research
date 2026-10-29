# Ranges of private IP addresses per region for a default private pool

Source: https://docs.nebius.com/vpc/addressing/available-addresses

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Ranges of private IP addresses per region for a default private pool

Every project has a [default pool](https://docs.nebius.com/vpc/overview.md#default-virtual-networks-resources) of private IPv4 addresses, called `default-network-pool`. Its CIDR block depends on the [region](https://docs.nebius.com/overview/regions.md) of the project (private regions are marked with <sup>\*</sup>):

<table>
  <thead>
    <tr>
      <th>Region</th>
      <th>CIDR block</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>`eu-north1` (Finland)</td>
      <td>10.0.0.0/13</td>
    </tr>

    <tr>
      <td>`eu-west1` (France)</td>
      <td>10.48.0.0/13</td>
    </tr>

    <tr>
      <td>`me-west1` (Israel)</td>
      <td>10.144.0.0/13</td>
    </tr>

    <tr>
      <td>`us-central1` (Kansas City, Missouri, US)</td>
      <td>10.96.0.0/13</td>
    </tr>

    <tr>
      <td>`uk-south1` (United Kingdom)</td>
      <td>10.64.0.0/13</td>
    </tr>

    <tr>
      <td>`uk-south2` (United Kingdom)</td>
      <td>10.80.0.0/13</td>
    </tr>

    <tr>
      <td>`eu-north2`*\** (Iceland)</td>
      <td>10.24.0.0/13</td>
    </tr>

    <tr>
      <td>`eu-south1` (Madrid, Spain)</td>
      <td>10.88.0.0/13</td>
    </tr>

    <tr>
      <td>`eu-west2` (France)</td>
      <td>10.72.0.0/13</td>
    </tr>

    <tr>
      <td>`us-north1` (Woodbury, Minnesota, US)</td>
      <td>10.104.0.0/13</td>
    </tr>
  </tbody>
</table>

These CIDR blocks are allocated for the default network, and the default subnet reuses them.

If you need other CIDR blocks, you can either edit the CIDR block of the default private pool or create new pools with the required CIDR blocks.

> [!NOTE]
>
> When you choose a custom CIDR block, avoid `172.17.0.0/16`. It conflicts with the Docker default bridge network and can make virtual machines unreachable. For more information, see [Virtual machine is unreachable due to a Docker subnet conflict](https://docs.nebius.com/compute/virtual-machines/docker-subnet-conflict.md).
