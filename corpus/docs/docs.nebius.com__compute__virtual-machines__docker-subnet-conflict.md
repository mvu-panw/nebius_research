# Virtual machine is unreachable due to a Docker subnet conflict

Source: https://docs.nebius.com/compute/virtual-machines/docker-subnet-conflict

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Virtual machine is unreachable due to a Docker subnet conflict

Virtual machines (VMs) running Docker cannot reach remote private IPv4 addresses in the `172.17.0.0/16` CIDR block. If you assign an address from this range to a VM, other VMs that run Docker cannot reach this address. Since the default boot disk images come with Docker preinstalled, this affects most VMs in the [network](https://docs.nebius.com/vpc/overview.md#network).

This happens because Docker uses `172.17.0.0/16` for its default bridge network and adds a kernel route for that range on every host where it runs. When a VM running Docker sends traffic to an address in this range, the route directs the packets to the local Docker bridge instead of the network interface, so they never leave the VM or reach the network.

To resolve the conflict, do one of the following:

* [Assign the VM a subnet](https://docs.nebius.com/vpc/addressing/custom-private-addresses.md) outside `172.17.0.0/16`.
* Reconfigure the default Docker bridge to use a non-overlapping range. To do this, on every VM that runs Docker and needs to reach an address in `172.17.0.0/16`, add the following parameters to the [cloud-init configuration](https://docs.nebius.com/compute/virtual-machines/manage.md#optional-create-a-user-data-configuration):

  ```yaml theme={null}
  write_files:
    - path: /etc/docker/daemon.json
      content: |
        {
          "bip": "192.168.200.1/24"
        }
      owner: root:root
      permissions: '0644'

  runcmd:
    - systemctl restart docker
  ```

  The `bip` value sets the subnet of the default Docker bridge. Replace `192.168.200.1/24` with any range that does not overlap with the private IP addresses used in your network.

  For more information about configuring the default Docker bridge, see the [Docker bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/) documentation.

#### See also

* [Private and public IP addresses of Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/network.md)
* [Ranges of private IP addresses per region for a default private pool](https://docs.nebius.com/vpc/addressing/available-addresses.md)
