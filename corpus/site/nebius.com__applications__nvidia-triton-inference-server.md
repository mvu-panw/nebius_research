# NVIDIA Triton Inference Server — Nebius applications

Source: https://nebius.com/applications/nvidia-triton-inference-server

Skip to main content

# NVIDIA Triton Inference Server
by NVIDIA
Serving

NVIDIA Triton Inference Server serves AI models from TensorRT, TensorFlow, PyTorch, ONNX, OpenVINO, RAPIDS FIL, and custom Python/C++ backends behind a single HTTP and gRPC inference API. It supports concurrent model execution, dynamic and sequence batching, ensemble pipelines with Business Logic Scripting, and runs on NVIDIA GPUs as well as x86/ARM CPUs. Models are loaded from an S3-compatible bucket so you can update model versions without redeploying the server.Deploy on Nebius
Free

Deployment methods1
Setup timefrom 15 minutesDeploy (opens in a new tab)
Sign-in required to deploy. Free to browse and read docs.

Vendor:NVIDIA

Additional links
- NVIDIA Triton website (opens in a new tab)
- Triton documentation (opens in a new tab)
- Triton on GitHub (opens in a new tab)

Licenses
- NVIDIA Triton Inference ServerBSD-3-Clause
- NVIDIA Triton container imageNVIDIA AI Enterprise EULA

## Key features

### Multi-framework model serving

TensorRT, TensorFlow, PyTorch, ONNX, OpenVINO, RAPIDS FIL, and custom Python/C++ backends behind one inference API.

### Dynamic and sequence batching

Combine inference requests in flight to maximize GPU throughput; per-model sequence batchers preserve order for stateful models.

### Concurrent model execution

Run multiple models (or multiple copies of the same model) on a single GPU; the scheduler arbitrates compute across requests.

### Ensemble pipelines

Chain models and pre/post-processing steps into a single request with ensembles and Business Logic Scripting.

### Object-storage-backed model repository

Load models from a Nebius Object Storage bucket; update model versions by uploading new files — no server redeploy required.

### Built-in Prometheus metrics

GPU utilization, server throughput, request latency, and queue depth metrics out of the box on port 8002.

## Pricing

Additional Nebius infrastructure costs may apply. Use the Nebius Pricing Page (opens in a new tab) to estimate your infrastructure costs.

Self-managed

### NVIDIA Triton Inference Server on Kubernetes

Deploy the NVIDIA Triton Inference Server in your Kubernetes cluster to serve models from TensorRT, TensorFlow, PyTorch, ONNX, OpenVINO, and other frameworks behind a unified HTTP/gRPC inference API.
Free
Charged for resources

Setup time15+ minutes
ScalingManual
MaintenanceSelf-managed (cluster)Deploy (opens in a new tab)
White-glove

### Deploy with a solutions architect
Some applications are easier with a hand on the wheel. Talk to an architect who has deployed this in production.
- Architecture review & sizing
- Hands-on deploy session
- 30 days of follow-up supportTalk to an expert 

## Security & compliance

### Run NVIDIA Triton Inference Server on infrastructure built for AI workloads
Reliable AI infrastructure backed by top-tier NVIDIA GPUs, purpose-built for demanding inference workloads. Multiple deployment methods — virtual machines for full hardware control, Kubernetes for scalable cluster deployments, and managed serverless applications for teams that want inference running without infrastructure overhead.Learn about Nebius AI Cloud 

### Security & compliance, out of the box
Nebius meets a broad set of security and compliance standards. Fine-grained IAM controls, audit logs, and encrypted storage are available out of the box — so teams can meet security requirements without additional tooling.Explore the Trust center 
SOC 2 Type II with HIPAASOC 3ISO/IEC 27001ISO/IEC 27799ISO 22301ISO/IEC 27701ISO/IEC 27018ISO/IEC 27032NIS 2DORACSA STAR Level 1

## Support

### Application support
Provided by NVIDIA. See the documentation and project links above.

### Infrastructure support
Provided by Nebius for the underlying cloud infrastructure.

## More applications from Serving

### Ollama
by Ollama
Serving

Run local-first LLM models and switch between them on demand without restarts.
Free

### SGLang
by SGLang Project
Serving

Start serving LLMs and VLMs in under 5 minutes with one-click deploy.
Free

### +2 more apps in Serving
Inference servers, gateways, and model endpoints.Browse all
