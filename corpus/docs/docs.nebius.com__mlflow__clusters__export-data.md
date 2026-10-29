# How to export data from Managed Service for MLflow clusters

Source: https://docs.nebius.com/mlflow/clusters/export-data

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to export data from Managed Service for MLflow clusters

You can export models, experiments and training runs from your Managed MLflow cluster to a directory on your machine:

1. [Configure connection to your cluster](https://docs.nebius.com/mlflow/quickstart.md#configure-connection-to-mlflow-tracking) by setting the `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD` environment variables used by MLflow Tracking.

   > [!NOTE]
   >
   > Clusters with disabled public access do not have public tracking URIs. You can save the private tracking URI to `MLFLOW_TRACKING_URI` and use it to export data to a Compute virtual machine that belongs to the same [network](https://docs.nebius.com/vpc/overview.md#network) as the cluster.

2. Install the [MLflow Export Import](https://github.com/mlflow/mlflow-export-import) package:

   ```bash theme={null}
   pip install git+https://github.com/mlflow/mlflow-export-import/#egg=mlflow-export-import
   ```

3. Run `export-all` to export all data from the cluster:

   ```bash theme={null}
   export-all --output-dir </output/directory> --use-threads True
   ```

   You can also use other tools from the package to export single and multiple objects, or to move them between clusters. For details, see the [tools overview](https://github.com/mlflow/mlflow-export-import/blob/master/README.md#tools-overview) and the [guide to tools for copying](https://github.com/mlflow/mlflow-export-import/blob/master/README_copy.md) in the package documentation.
