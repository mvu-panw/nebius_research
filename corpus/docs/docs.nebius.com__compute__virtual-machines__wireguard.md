# Creating a jump server with WireGuard installed on it

Source: https://docs.nebius.com/compute/virtual-machines/wireguard

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating a jump server with WireGuard installed on it

You can create a jump server to build a reliable tunnel between two zones:

* Secure zone that consists of virtual machine (VMs) created in Nebius AI Cloud
* Demilitarized zone (DMZ) that consists of machines outside Nebius AI Cloud

All connections from the DMZ to the secure zone go through the jump server. This solution provides several benefits:

* You can use one public IP address to access all VMs.
* You can keep the number of public addresses within a [quota](https://docs.nebius.com/compute/resources/quotas-limits.md#network).
* You can limit access to the secure zone and allow only authorized machines to connect to the secure zone.

To create a jump server, deploy a VM with [WireGuard](https://www.wireguard.com) installed and configure a VPN. The traffic between the zones is routed in an encrypted form via the jump server.

To create a VM with WireGuard deployed, Nebius AI Cloud offers a Terraform-based solution. You can apply manifests that contain configuration of a VM with a WireGuard image.

## Costs

The tutorial includes the following chargeable resources:

* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram)
* [Compute disks](https://docs.nebius.com/compute/resources/pricing.md#disks)

## Prerequisites

1. [Install Terraform](https://developer.hashicorp.com/terraform/install).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI. The Terraform-based solution uses the CLI to get credentials.

   For enhanced security, [use a service account](https://docs.nebius.com/cli/configure.md#how-to-set-up-the-cli-for-a-service-account) to configure the CLI. Make sure that this account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. Install `jq`:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. Clone the [nebius-solution-library](https://github.com/nebius/nebius-solution-library/tree/main) repository from where the WireGuard solution is going to be deployed:

   ```bash theme={null}
   git clone git@github.com:nebius/nebius-solution-library.git
   ```

5. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

## Steps

### Deploy infrastructure

1. In your terminal, go to the `wireguard` directory in the cloned repository:

   ```bash theme={null}
   cd nebius-solution-library/wireguard
   ```

2. In the `environment.sh` file in this directory, uncomment the following variables and specify values for them:

   * `NEBIUS_TENANT_ID`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md).
   * `NEBIUS_PROJECT_ID`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `NEBIUS_REGION`: The [region](https://docs.nebius.com/overview/regions.md) where your project is located. You can find the region in the web console, in the list of projects.

3. Run the script that creates an access token for Terraform, saves the token to environment variables and configures Terraform state to be saved in Object Storage:

   ```bash theme={null}
   source ./environment.sh
   ```

4. Initialize Terraform in the `wireguard` directory:

   ```bash theme={null}
   terraform init
   ```

5. In the `terraform.tfvars` file in this directory, uncomment the following variables and specify values for them:

   * `ssh_user_name`: The user required for an SSH connection to the VM, for example `user1`.

   * `ssh_public_key`: The public SSH key that you [created earlier](#prerequisites).

     Specify either the key body or the path to this key.

   * `public_ip_allocation_id`: An ID of an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) with a public IP address.

     The WireGuard UI will be available at this address. To preserve the address even in case of the VM deletion, create the allocation:

     ```bash theme={null}
     nebius vpc allocation create \
       --ipv4-public-subnet-id <subnet_ID> \
       --name wireguard_allocation \
       --parent-id <project_ID> \
       --format jsonpath='{.metadata.id}'
     ```

     The command returns the allocation ID. Specify it in the `public_ip_allocation_id` variable.

6. Preview the configuration that you are going to deploy:
   ```bash theme={null}
   terraform plan
   ```

7. Apply the changes:

   ```bash theme={null}
   terraform apply
   ```

   When the command is finished, it returns the VM public address:

   ```text theme={null}
   Outputs:

   wg_instance_pib = "<public_IP_address>"
   ```

   Copy the address: It is required to connect to the deployed VM.

### Access WireGuard

1. Connect to the VM:

   ```bash theme={null}
   ssh -i <path_to_private_key> <username>@<public_IP_address>
   ```

   The command contains:

   * Path to the private SSH key that you [created earlier](#prerequisites)
   * Username specified in the `terraform.tfvars` file
   * Public IP address of the deployed VM

2. Get the WireGuard UI password:

   ```bash theme={null}
   sudo cat /var/lib/wireguard-ui/initial_password
   ```

3. In the browser, open the WireGuard UI at `http://<public_IP_address>:5000`.

4. In the window that opens, sign in with the `admin` username and the password retrieved from the VM.

   The working space of the WireGuard UI opens.

### Configure WireGuard

Set up a VPN and grant access to the VMs in the secure zone. To do this, add the DMZ machines as WireGuard clients:

1. Click  **New client**.

2. In the window that opens, specify details of the machines that require access.

   In the **Allowed IPs** field, enter CIDRs of these machines.

3. Click **Submit**.

4. After the window is closed, click **Apply config**.

   Click this button every time after you create, change or delete WireGuard clients.

After that, the DMZ machines are able to connect to the VMs in the secure zone.

You do not need to configure the same access for the jump server because it is located in the same subnet as the VMs in the secure zone.

## How to delete the created resources

The created Compute virtual machine and its boot disk are chargeable. If you do not need them, delete these resources, so Nebius AI Cloud does not charge for it. Use the following command to delete all the created infrastructure at once:

```bash theme={null}
terraform destroy -target=nebius_compute_v1_instance.wireguard_instance
```
