# Exporting workflows and images from the ComfyUI application

Source: https://docs.nebius.com/applications/comfyui/export-data

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Exporting workflows and images from the ComfyUI application

You can export workflows that you create in the ComfyUI application and download images that these workflows generate.

Before you begin, [connect to the application](https://docs.nebius.com/applications/comfyui/connect.md).

## Exporting workflows

1. Select the workflow tab.

2. In the **Workflow** menu, select an option, depending on how you want to use the exported file:

   * **Export** creates a JSON file that you can import back into the web interface (**Workflow** → **Open**).
   * **Export (API)** creates a JSON file that you can use as a payload for `POST /prompt` API requests to ComfyUI. For more details, see [ComfyUI documentation](https://docs.comfy.org/development/comfyui-server/comms_routes) and an [example](https://github.com/comfyanonymous/ComfyUI/blob/master/script_examples/basic_api_example.py) in ComfyUI's GitHub repository. The file is also compatible with the web interface.

3. Enter the filename and then save the file.

## Downloading images

1. In the menu bar, click **Show Image Feed**.
2. In the image feed, click the image.
3. Save the image that opens.
