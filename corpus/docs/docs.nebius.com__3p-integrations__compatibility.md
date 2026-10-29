# Software compatibility and supported runtimes in Nebius AI Cloud

Source: https://docs.nebius.com/3p-integrations/compatibility

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Software compatibility and supported runtimes in Nebius AI Cloud

Nebius AI Cloud supports a wide range of workloads and software stacks, making it easy to run your machine learning jobs, endpoints and applications by using familiar tools and frameworks.

## Runtimes

### Nebius AI Cloud runtimes

You can launch and manage your workloads on the following Nebius AI Cloud services:

* **Compute virtual machines (VMs)**

  Cloud-hosted VMs with NVIDIA® GPU support for ML/AI workloads.

  [Web console](https://console.nebius.com/compute) | [Documentation](https://docs.nebius.com/compute/index.md)

* **Serverless AI Devlabs**

  Interactive development environments for coding, prototyping and debugging in the browser.

  [Web console](https://console.nebius.com) | [Documentation](https://docs.nebius.com/serverless/devlabs/manage.md)

* **Managed Service for Kubernetes® clusters**

  Fully managed Kubernetes clusters for scalable, containerized workloads.

  [Web console](https://console.nebius.com/mk8s) | [Documentation](https://docs.nebius.com/kubernetes/index.md)

* **Managed Service for Soperator clusters**

  Slurm-based clusters for distributed ML/AI training, also available as an open-source Kubernetes operator.

  [Web console](https://console.nebius.com/slurm) | [Documentation](https://docs.nebius.com/slurm-soperator/index.md)

### Third-party orchestrators

Nebius AI Cloud integrates with leading open-source orchestrators that help you manage and automate workloads:

* **dstack**

  Flexible workload manager for ML and data science.

  [Tutorial](https://docs.nebius.com/3p-integrations/dstack.md)

* **Metaflow (Outerbounds)**

  Production-grade workflow management for ML pipelines.

  [Blog post](https://nebius.com/blog/posts/nebius-outerbounds-strategic-technology-partnership-integration)

* **SkyPilot**

  Unified framework for running AI workloads across clouds, including Nebius AI Cloud.

  [Tutorial](https://docs.nebius.com/3p-integrations/skypilot.md)

## What you can run in Nebius AI Cloud

If your software runs on Ubuntu 20 or higher and supports containers, VMs or Kubernetes clusters, you can use Nebius AI Cloud runtimes to run it. This includes, but is not limited to, the tools, libraries and platforms listed below.

> [!TIP]
>
> Use containerized deployment where possible for better portability, scalability and management.

### ML libraries and frameworks

* [Apache MXNet](https://mxnet.apache.org/)
* [AutoKeras](https://autokeras.com/)
* [auto-sklearn](https://automl.github.io/auto-sklearn)
* [Caffe](https://caffe.berkeleyvision.org/)
* [Chainer](https://chainer.org/)
* [Darknet](https://pjreddie.com/darknet/)
* [Eclipse Deeplearning4j](https://deeplearning4j.konduit.ai/)
* [JAX](https://docs.jax.dev/en/latest/)
* [Keras](https://keras.io/)
* [LiteRT](https://ai.google.dev/edge/litert) (TensorFlow Lite)
* [MegEngine](https://github.com/MegEngine/MegEngine)
* [Microsoft Cognitive Toolkit (CNTK)](https://learn.microsoft.com/en-us/cognitive-toolkit/)
* [MindSpore](https://www.mindspore.cn/en)
* [MLlib](https://spark.apache.org/mllib/)
* [ML.NET](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet)
* [NVIDIA cuBLAS](https://developer.nvidia.com/cublas)
* [NVIDIA CUDA Deep Neural Network (cuDNN)](https://developer.nvidia.com/cudnn)
* [OpenVINO](https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/overview.html)
* [Paxml](https://github.com/google/paxml/tree/main) (Pax), including as a [Rosetta distribution](https://github.com/NVIDIA/JAX-Toolbox/tree/main/rosetta/rosetta/projects/pax)
* [PlaidML](https://plaidml.github.io/plaidml/)
* [PyTensor](https://pytensor.readthedocs.io/en/latest/)
* [PyTorch](https://pytorch.org/)
* [TensorFlow](https://www.tensorflow.org/)
* [Theano](https://github.com/Theano/Theano)
* [Torch](http://torch.ch/)
* [TPOT](https://github.com/EpistasisLab/tpot) (Tree-based Pipeline Optimization Tool)
* [XGBoost](https://xgboost.readthedocs.io/en/stable/)

### Distributed training frameworks

* [BigDL-LLM](https://bigdl.readthedocs.io/en/latest/)
* [DeepSpeed](https://www.deepspeed.ai/)
* [Horovod](https://horovod.ai/)
* [IPEX-LLM](https://github.com/intel/ipex-llm)
* [PaddlePaddle](https://www.paddlepaddle.org.cn/en)
* [Ray](https://www.ray.io/)
* [TorchFT](https://docs.pytorch.org/torchft/)

### Inference runtimes

* [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt)
* [SGlang](https://docs.sglang.ai/)
* [vLLM](https://vllm.ai/)

### Ecosystem AI platforms

* [Baseten](https://www.baseten.co/)
* [dstack](https://dstack.ai/) — see [tutorial](https://docs.nebius.com/3p-integrations/dstack.md)
* [Lightning AI](https://lightning.ai/)
* [Mithril](https://mithril.ai/)
* [NVIDIA NIM microservices](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/)
* [NVIDIA DGX Cloud](https://www.nvidia.com/en-us/data-center/dgx-cloud/)
* [NVIDIA Run:ai](https://www.nvidia.com/en-us/software/run-ai/) — see [tutorial](https://docs.nebius.com/3p-integrations/run-ai.md)
* [Outerbounds](https://outerbounds.com/) ([Metaflow](https://metaflow.org/))
* [SkyPilot](https://docs.skypilot.co/en/latest/overview.html) — see [tutorial](https://docs.nebius.com/3p-integrations/skypilot.md)
