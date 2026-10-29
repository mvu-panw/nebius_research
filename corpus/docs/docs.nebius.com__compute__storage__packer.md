# Creating boot disk images with Packer

Source: https://docs.nebius.com/compute/storage/packer

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating boot disk images with Packer

You can create custom boot disk images based on existing images by using [Packer](https://developer.hashicorp.com/packer) and the [Nebius Packer plug-in](https://github.com/nebius/packer-plugin-nebius/blob/main/README.md).

The Nebius Packer plug-in creates a temporary virtual machine (VM) from a base image, connects to it over SSH, runs provisioners and then creates a new boot disk image.

Use this workflow to:

* Pre-install packages and system dependencies
* Prepare versioned images for repeated VM creation
* Standardize environments across teams or workloads

## Before you start

1. Install [Packer](https://developer.hashicorp.com/packer/downloads).

2. Make sure your project has sufficient [quotas](https://docs.nebius.com/overview/quotas.md) for image creation:

   * Number of images
   * Total storage capacity of all images

3. Set up authentication by using one of the following methods.

   * **Service account**

     1. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md) and [generate a key pair](https://docs.nebius.com/iam/service-accounts/authorized-keys.md#create-a-key-pair).
        The key pair is saved to a JSON file, for example, `~/.nebius/<service_account_ID>_credentials.json`.
     2. Open the file and copy the value of the `private_key` field.
     3. Save the key to the `private.pem` file.
     4. Use the values from the JSON file in your Packer configuration.

   * **Access token**

     Generate an access token:

     ```bash theme={null}
     nebius iam get-access-token
     ```

     An access token is valid for 12 hours. After it expires, create a new one.

## Steps

### Install the Nebius Packer plug-in

1. Create the `config.pkr.hcl` file and add the Nebius plug-in configuration:

   ```hcl theme={null}
   packer {
     required_plugins {
       nebius = {
         source  = "github.com/nebius/nebius"
         version = ">= 0.0.4"
       }
     }
   }
   ```

2. Initialize the plug-in in the directory that contains your Packer configuration files:

   ```bash theme={null}
   packer init .
   ```

### Build the disk image

The Nebius image builder creates a VM from a base image, provisions it over SSH and publishes a new image.

1. Create the `build.pkr.hcl` file and add the `nebius-image` source to it:

   ```hcl theme={null}
   source "nebius-image" "ubuntu2404" {
     communicator = "ssh"
     ssh_username = "ubuntu"

     # Service account credentials used for image creation
     service_account {
       private_key_file = "./private.pem"
       public_key_id    = "<public_key_ID>"
       account_id       = "<service_account_ID>"
     }
     # Alternatively, use an access token
     # token        = <token>
    
     # Boot disk configuration for the temporary VM
     disk {
       size_gibibytes = 60
     }

     # Source image used to create the temporary VM
     base_image {
       family = "ubuntu24.04-driverless"
     }

    # Network configuration for the temporary VM
     network {
       subnet_id = "<subnet_ID>"
       associate_public_ip_address = true
     }

     # Compute resources for the temporary VM
     instance {
       platform = "cpu-d3"
       preset   = "16vcpu-64gb"
     }

     # Parameters of the resulting image
     image {
       name                        = "ubuntu24.04-131-0.0.1"
       version                     = "0.0.1"
       image_family                = "ubuntu24.04-131"
       cpu_architecture            = "amd64"
       image_family_human_readable = "Ubuntu 24.04 CUDA 13.1 Hackathon"
     }
     # Project where the image will be created
     parent_id = "<project_ID>"
   }
   ```

   The `nebius-image` source has the following parameters:

   **General parameters**

   * `communicator` (optional): Specifies how Packer connects to the VM. Supported value: `ssh` (default).
   * `parent_id`: ID of the project where the resulting image will be created.
   * `ssh_username`: Username used to connect to the VM.

   **Authentication**

   * `service_account.private_key_file`: Path to the private key file.
   * `service_account.public_key_id`: ID of the public key.
   * `service_account.account_id`: Service account ID.
   * `token`: Access token used for authentication. Use this as an alternative to `service_account`.

   **Disk configuration**

   * `disk.size_gibibytes`: Size of the disk in GiB.

   **Base image**

   * `base_image.family`: Image family name.
   * `base_image.id`: Specific image ID.

   **Network**

   * `network.subnet_id` (optional): ID of an existing subnet that will be used to create a VM. If not provided, the plug-in attempts to find the project's default network.
   * `network.associate_public_ip_address` (optional): Assigns a public IP address. Use a public IP if your build environment connects directly via SSH.

   **VM configuration**

   * `instance.platform`: VM [platform](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `instance.preset`: VM platform preset (number of GPUs and vCPUs, RAM size).

   **Output image configuration**

   * `image.name`: Image name.
   * `image.version` (optional): Image version.
   * `image.image_family` (optional): Image family identifier.
   * `image.image_family_human_readable` (optional): Display name for the image family.
   * `image.cpu_architecture` (optional): CPU architecture.

2. Add the build block to the `build.pkr.hcl` file:

   ```hcl theme={null}
   build {
     sources = ["source.nebius-image.ubuntu2404"]

     provisioner "file" {
       # Path to a local script in your project
       source      = "some-local-file.txt"
       destination = "/tmp/helloworld.txt"
     }

     provisioner "shell" {
       inline = [
       "cd /tmp",
       "echo Installing hello world text",
       "sudo mv /tmp/helloworld.txt /root",
       "echo Resetting cloud-init and caches",
       "sudo apt clean",
       "sudo uv cache clean",
       "sudo cloud-init clean --logs",
       "sudo sync",
       ]
     }
   }
   ```

3. From the directory with the configuration files, run:

   ```bash theme={null}
   packer init .
   packer build build.pkr.hcl
   ```

### Check the image

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Disks**.
2. Go to the **Images** tab and locate your image.
