# Managing users in a Soperator cluster

Source: https://docs.nebius.com/slurm-soperator/users/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing users in a Soperator cluster

Create users in a Soperator cluster so they can [connect to the cluster nodes](https://docs.nebius.com/slurm-soperator/clusters/connect.md).

A Soperator cluster uses the [Ubuntu user management tools](https://documentation.ubuntu.com/server/how-to/security/user-management/index.html), so user administration on Soperator is similar to user administration on Ubuntu. The general difference is that you [create users](#how-to-create-a-user) with the `soperator-createuser` command, Soperator's wrapper over Ubuntu's [adduser](https://manpages.ubuntu.com/manpages/jammy/en/man8/adduser.8.html) command.

Every Soperator cluster has a default administrator called `root`. To manage users, connect to cluster nodes as `root`.

> [!WARNING]
>
> Only users with administrator privileges can create and delete other users. If you are not the `root` user, run the creation and deletion commands with `sudo`.

## How to create a user

1. Ask a user to [generate an SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md) and provide you with their SSH public key. They will use this key for connections.

2. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes).

3. Run the user creation command and specify a new username:

   ```bash theme={null}
   soperator-createuser <username> [--with-password] [--without-sudo] [--without-docker]
   ```

   You can add optional parameters. The `soperator-createuser` command supports the [same parameters](https://manpages.ubuntu.com/manpages/jammy/en/man8/adduser.8.html) as `adduser` and has several parameters of its own:

   * `--with-password`: Requires a password for the new user, in addition to their SSH key.
   * `--without-sudo`: Disables the default option to run commands with `sudo` for the user.
   * `--without-docker`: Disables the default option to run `docker` commands without `sudo` for the user.

     By default, `soperator-createuser` adds the user to the Unix `docker` group, which allows running `docker` commands without `sudo`. You can disable this by using the `--without-docker` parameter. For more information about the group, see the [Docker documentation](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

4. At the prompt that appears, enter the following information:

   * Password of the user, if you specified the `--with-password` parameter.
   * Optional full name of the user. We recommend specifying it, especially if the username does not match the full name. This helps you recognize the user.
   * Additional optional information, such as their room number or work phone.
   * SSH public key of the user.

## How to get a list of users

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes).
2. Run the user list command:

   ```bash theme={null}
   getent passwd
   ```

   Output example:

   ```text theme={null}
   root:x:0:0:root:/root:/bin/bash
   daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
   bin:x:2:2:bin:/bin:/usr/sbin/nologin
   sys:x:3:3:sys:/dev:/usr/sbin/nologin
   ...
   test-user-1:x:1004:1004:Test User Name,,,:/home/test-user-1:/bin/bash
   ```

   System users have IDs that are less than `1000`. Regular users have IDs that are larger than or equal to `1000`. In the example above, the system `bin` user has the ID `2` and the regular `test-user-1` user has the ID `1004`.

## How to delete a user

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes).
2. To copy the username, [get the list of users](#how-to-get-a-list-of-users).
3. Run the user deletion command:

   ```bash theme={null}
   deluser <username> --remove-home
   ```

   The command deletes the user and its home directory.

   Output example:

   ```text theme={null}
   Looking for files to backup/remove ...
   Removing files ...
   Removing user `test-user-1' ...
   Warning: group `test-user-1' has no more members.
   Done.
   ```

For more information about deleting users by using `deluser`, see the [Ubuntu documentation](https://documentation.ubuntu.com/server/how-to/security/user-management/index.html#delete-a-user).
