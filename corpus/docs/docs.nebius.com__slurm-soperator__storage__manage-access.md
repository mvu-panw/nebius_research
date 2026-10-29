# Managing file access in a Soperator cluster

Source: https://docs.nebius.com/slurm-soperator/storage/manage-access

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing file access in a Soperator cluster

As you run machine learning workloads on the Managed Service for Soperator cluster, you need to manage access to the training data and the results of training. You can create multiple groups and users to give people with separate roles different levels of access to your data.

## How to create user groups

You can [create users](https://docs.nebius.com/slurm-soperator/users/manage.md#how-to-create-a-user) for everyone who works with your cluster and add multiple groups that give their members different access permissions. Each user may be a member of several groups.

> [!NOTE]
>
> You need administrator privileges to create users and groups.

### Add a group

```bash theme={null}
sudo addgroup <group_name>
```

### Add a user to a group

```bash theme={null}
sudo adduser <username> <group_name>
```

For the group membership to take effect, after you add a user to a new group, ask them to log out and [reconnect](https://docs.nebius.com/slurm-soperator/clusters/connect.md) to your cluster.

## How to manage default permissions for created files

When you create a new file or directory, its permissions are determined by the [`umask` value](#umask) and the [default group settings](#default-groups) on the directory where the file is created.

### umask

The `umask` specifies which bits are removed from the full permissions (`666` for files and `777` for directories). All possible permissions are listed in full in the [Ubuntu documentation](https://help.ubuntu.com/community/FilePermissions).

Check your `umask` value:

```bash theme={null}
umask
```

The usual default value is `0002`, which means that the permissions are the following:

* For new files: `0666-0002 → 0664` — everyone can read, the owner and file group members can write.
* For new directories `0777-0002 → 0775` — everyone can read and execute, the owner and file group members can write.

To create new files and directories with more restrictive permissions, set a different `umask`, for example:

```bash theme={null}
umask 0022
```

This setting removes the write permissions from anyone but the file owner. New files are created with `644` permission, and new directories with `775`.

To make the `umask` setting permanent for the current user, add it to the shell configuration:

```bash theme={null}
echo 'umask 0022' >> ~/.bashrc
```

### Default groups

By default, a new file belongs to the primary group of the user who created it. For a shared directory owned by a group, you may want all new files created in the directory to inherit the same group. To do that, set the `setgid` bit in its permissions: `2` instead of `0` in the high-order octal digit of the group permissions.

To set the group ownership and inherit file permissions, run the following commands:

```bash theme={null}
sudo chown :<group_name> <directory_name>
sudo chmod 2755
```

## How to set granular permissions with ACLs

Access Control Lists (ACLs) let you override the default permissions and explicitly specify which users or groups have different levels of access to specific files or directories.

Use the `setfacl` command to set the ACL for a file or directory. For example, to give a user read and write permissions to a file, run the following command:

```bash theme={null}
setfacl -m u:<username>:rw- <file_name>
```

To give all group members read-only access to a file, run the following command:

```bash theme={null}
setfacl -m g:<group_name>:r-- <file_name>
```

### Set default access to a directory

To set default permissions, add the `-d` parameter to the `setfacl` command. This modifies the default ACL, and all new files created in this directory inherit these permissions.

For example, to give all group members read, write and execute permissions to a directory and all new files created in it, run the following command:

```bash theme={null}
setfacl -d -m g:<group_name>:rwx /<directory_name>
```

To give a specific user read and execute permissions to a directory and all new files created in it, run the following command:

```bash theme={null}
setfacl -d -m u:<username>:r-x /<directory_name>
```

### View current ACLs

To check the current ACLs for a file or directory, run the following command:

```bash theme={null}
getfacl <file_or_directory_name>
```

Example output for a file:

```bash theme={null}
# file: file.txt
# owner: alice
# group: developers
user::rw-
user:test_user:r--
group::rw-
group:testers:r--
other::r--
```

Example output for a directory:

```bash theme={null}
# file: mnt/data
# owner: alice
# group: developers
user::rwx
user:test_user:r--
group::rwx
group:testers:r--
other::r--
```

## Main scenarios

Depending on your workflow, you can create read-only datasets or read-write working directories and configure access for individual groups or all users.

### Read-only dataset shared with all users

Create a shared dataset that contains source data for training or evaluation. Make it read-only to prevent accidental changes or data corruption and ensure consistency across all training runs.

1. Create a directory in a shared filesystem, for example:

   ```bash theme={null}
   sudo mkdir /mnt/data/datasets/imagenet
   ```

2. Set permissions so that all users can read files, but only administrators can modify them:

   ```bash theme={null}
   sudo chown root:root /mnt/data/datasets/imagenet
   sudo chmod 755 /mnt/data/datasets/imagenet
   ```

3. Make sure your users can access it:

   * Single jobs can access the shared filesystem and the directory in it.
   * If needed, the users can mount the shared directory as a volume to their jobs or containers, in read-only mode.

If at some point the users need to write to this directory, they have to use `sudo`.

### Read-write directory for training results

Use a separate directory to save checkpoints, model outputs and logs. Make it writable by the job owners or a specific team.

1. Create a directory for results:

   ```
   sudo mkdir /mnt/data/results
   ```

2. [Create user groups](#add-a-group) (for example, `mlteam`) and [add users to them](#add-a-user-to-a-group). For the group membership to take effect, ask the users to log out and reconnect to your cluster.

3. Grant write permissions to the required group, for example:

   ```bash theme={null}
   sudo chown :mlteam /mnt/data/results
   sudo chmod 2775 /mnt/data/results
   ```

   The `2` in `2775` sets the `setgid` bit to ensure that all new files in the directory inherit the group.

Encourage users to organize their work into subdirectories by project or date to avoid file conflicts when writing to the directory.

### Collaboration between two groups

When two groups work on related tasks, configure three shared directories: private to group A, private to group B and accessible to everyone.

1. [Create user groups](#add-a-group). For example, `groupA` and `groupB` for each of the teams, and `users` for everyone.

2. [Add users](#add-a-user-to-a-group) to the groups. For the group membership to take effect, ask the users to log out and reconnect to your cluster.

3. Create the directories:

   ```bash theme={null}
   sudo mkdir -p /mnt/data/collab/groupA /mnt/data/collab/groupB /mnt/data/collab/common
   ```

4. Set the `groupA` and `groupB` directory permissions to full access for the corresponding group and no access for anyone else:

   ```bash theme={null}
   sudo chown :groupA /mnt/data/collab/groupA
   sudo chmod 2770 /mnt/data/collab/groupA

   sudo chown :groupB /mnt/data/collab/groupB
   sudo chmod 2770 /mnt/data/collab/groupB
   ```

   The `2` in `2770` sets the `setgid` bit to ensure that all new files in the directory inherit the group.

5. Set the `common` directory permissions to let everyone in the `users` group have full access:

   ```bash theme={null}
   sudo chown :users /mnt/data/collab/common
   sudo chmod 2775 /mnt/data/collab/common
   ```

This structure allows each group to store private data while sharing common outputs or logs with all users.
