# Exporting data from the Qdrant application

Source: https://docs.nebius.com/applications/qdrant/export-data

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Exporting data from the Qdrant application

You can export your [collections](https://qdrant.tech/documentation/concepts/collections/) from the Qdrant application by creating and downloading [snapshots](https://qdrant.tech/documentation/concepts/snapshots/):

**Web interface**

1. [Connect to the application](https://docs.nebius.com/applications/qdrant/connect.md).
2. In the sidebar, click  **Collections**.
3. Open the collection and then go to the **Snapshots** tab.
4. Click **Take snapshot**.
5. In the row of the created snapshot, click  → **Download**.
6. Save the file.

**API**

1. [Get the application's public endpoint](https://docs.nebius.com/applications/qdrant/connect.md).

2. Create the collection's snapshot:

   ```bash theme={null}
   curl -X POST \
     'https://<public_URL>/collections/<collection_name>/snapshots' \
     --header 'api-key: <API_key>'
   ```

   The output contains the snapshot's name:

   ```json theme={null}
   {
     "time": 0.002,
     "status": "ok",
     "result": {
       "name": "<snapshot_name>",
       ...
     }
   }
   ```

3. Get the snapshot:

   ```bash theme={null}
   curl -X GET \
     'https://<public_URL>/collections/<collection_name>/snapshots/<snapshot_name>' \
     --header 'api-key: <API_key>'
   ```

   For more details, see [Qdrant API reference](https://api.qdrant.tech/).
