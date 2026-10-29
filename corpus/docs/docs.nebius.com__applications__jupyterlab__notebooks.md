# Working with notebooks in the JupyterLab® application in Nebius AI Cloud

Source: https://docs.nebius.com/applications/jupyterlab/notebooks

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Working with notebooks in the JupyterLab® application in Nebius AI Cloud

After [deploying the JupyterLab application](https://docs.nebius.com/applications/jupyterlab/deploy.md) on a Managed Service for Kubernetes® cluster and [connecting to it](https://docs.nebius.com/applications/jupyterlab/connect.md), you can work with JupyterLab notebooks. For more details, see the [JupyterLab documentation](https://jupyterlab.readthedocs.io/en/latest/).

## Dependencies

Notebooks in the JupyterLab application include [PyTorch](https://pytorch.org/docs/stable/index.html) by default.

To install more Python dependencies in a notebook, run `!pip install <package_name> ...` in a notebook cell:

```text theme={null}
!pip install pandas numpy
```

To install non-Python dependencies, [upload their binaries](#working-with-files) to JupyterLab. The application does not support package manager commands such as `apt install` because they require `sudo`, and the application does not provide a password.

## Working with files

You can upload files to your JupyterLab notebooks and download files and notebooks themselves. The recommended method of uploading files depends on the file size.

### Uploading smaller files in the file browser

If your files are smaller than 3 GiB, you can upload them directly in the JupyterLab file browser.

To open the file browser in your notebook, click  in the sidebar. To upload files, drag and drop them onto the file browser, or click  **Upload**.

For more details, see the [JupyterLab documentation](https://jupyterlab.readthedocs.io/en/latest/user/files.html).

### Uploading larger files (3 GiB+)

Due to JupyterLab's limitations, when you use the file browser to upload files larger than 3 GiB (datasets, checkpoints, etc.), you may encounter network errors. As a workaround, you can upload them through an S3-compatible object storage, for example, the [Object Storage service](https://docs.nebius.com/object-storage/index.md) in Nebius AI Cloud:

1. If you do not have an Object Storage bucket yet, [create one](https://docs.nebius.com/object-storage/buckets/manage.md).

2. [Upload your object](https://docs.nebius.com/object-storage/objects/upload-download.md) to the bucket.

3. Get the object's URL:

   **Web console**

   1. In the sidebar, go to  **Storage** → **Object Storage**.
   2. Select the bucket in which you uploaded the object.
   3. In the object's line, click  → **Get link**. The pre-signed URL that includes credentials is copied to the clipboard. It is valid for one hour.

4. In your JupyterLab notebook, use built-in tools like `wget` or `curl` to download the file. For example:

   ```bash theme={null}
   wget https://storage.eu-north1.nebius.cloud/my-bucket/test-object?X-Amz-Algorithm=...
   ```

### Downloading files and notebooks

To download a file or a notebook to your machine:

1. In the sidebar, click  to open the file browser.
2. In the file browser, right-click the file or notebook and click  **Download**.

***

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
