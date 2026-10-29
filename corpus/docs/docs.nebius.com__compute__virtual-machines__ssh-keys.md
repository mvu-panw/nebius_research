# How to generate SSH keys

Source: https://docs.nebius.com/compute/virtual-machines/ssh-keys

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to generate SSH keys

An *SSH key pair* is used to authenticate with a remote resource over SSH. It consists of:

* A *public key* that you add to the resource or share with an administrator.
* A *private key* that you keep on your local machine and use when connecting.

You need an SSH key pair to:

* Configure SSH access when [creating a virtual machine (VM)](https://docs.nebius.com/compute/virtual-machines/manage.md) and to [connect to your Compute VM](https://docs.nebius.com/compute/virtual-machines/connect.md) over SSH.
* [Create a job](https://docs.nebius.com/serverless/jobs/manage.md#how-to-create-a-job) or [endpoint](https://docs.nebius.com/serverless/endpoints/manage.md#how-to-create-an-endpoint) with SSH access.
* [Give another user access to a VM](https://docs.nebius.com/compute/virtual-machines/connect.md#shared-access-to-the-vm).
* [Connect to login and worker nodes in a Soperator cluster](https://docs.nebius.com/slurm-soperator/clusters/connect.md).
* [Access a VM through a jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) when the VM does not have a public IP address.

## Generating a key pair

1. In the terminal, create the `.ssh` directory if it does not exist:

   ```bash theme={null}
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ```

2. Go to the `~/.ssh` directory:

   ```bash theme={null}
   cd ~/.ssh
   ```

3. Generate an SSH key pair:

   ```bash theme={null}
   ssh-keygen -t ed25519
   ```

   * To add a comment that identifies the key, add the optional `-C` parameter:

     ```bash theme={null}
     ssh-keygen -t ed25519 -C "<key_comment>"
     ```

4. When prompted, enter the file path where you want to save the key pair.

   * To save the key pair to the default location, press `Enter`.
   * If you already have a key in the default location, specify a custom file name, for example:

     ```bash theme={null}
     /home/<username>/.ssh/nebius_ed25519
     ```

5. (Optional) When prompted, enter a passphrase for the private key.

   Press `Enter` to generate a key without a passphrase. However, using a passphrase protects the private key if someone gets access to your local machine.

6. Repeat the passphrase when prompted.

The command creates two files:

* The private key, for example `~/.ssh/id_ed25519`.
* The public key, for example `~/.ssh/id_ed25519.pub`.

## Getting the public key

You need the contents of the public key when a resource or configuration asks for an SSH public key. For example, you can add it to a VM to configure SSH access or send it to an administrator who manages access to the resource.

To get the contents of the public key, run:

```bash theme={null}
cat ~/.ssh/id_ed25519.pub
```

If you saved the public key to a custom file when you generated the key, specify the name with the `.pub` extension:

```bash theme={null}
cat ~/.ssh/<key_file_name>.pub
```

The output contains the contents of the public key, for example:

```text theme={null}
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI*** user@example.com
```

## Protecting the private key

Follow these recommendations when using SSH keys:

* Keep the private key only on your local machine and don't share it with others.
* Share only the public key, which is stored in the file with the `.pub` extension.
* Use a passphrase for the private key.
* Use a separate key pair for each user.
* Remove public keys that are no longer used from the resource.
