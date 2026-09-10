📌 Overview
Milestone 3 successfully integrates the core machine learning components into our FastAPI/Celery backend. The objective was to deploy a medical imaging model (torchxrayvision DenseNet121) to classify 18 thoracic pathologies from chest X-rays, provide spatial explainability using GradCAM, and orchestrate the entire flow asynchronously using Celery, PostgreSQL, and MinIO (S3).

To optimize inference speed and decouple our production environment from heavy PyTorch training dependencies, the classification backbone was exported to ONNX, executed via onnxruntime, while PyTorch was retained exclusively for the gradient-based GradCAM generation.

🏗️ Architecture & Components Created
preprocessing.py: Handles X-ray specific normalization (8-bit to [-1024, 1024] range), center cropping, and reshaping to 224x224.

inference.py: Loads the ONNX model and executes forward passes via CPUExecutionProvider.

gradcam.py: Uses pytorch_grad_cam to hook into the final convolutional layer of the DenseNet backbone, generating a localized heatmap overlaid on the original image.

app/worker/tasks.py: The Celery orchestrator. It manages the full lifecycle: DB state updates -> MinIO download -> ONNX Inference -> PyTorch GradCAM -> MinIO heatmap upload -> DB result persistence.

🛑 Challenges Faced & Technical Solutions
During the implementation and ONNX export process, we encountered several edge-cases related to tracing PyTorch models into static computation graphs. Here is a detailed breakdown of the problems and how they were resolved.

1. get_model API Incompatibility
   Problem: Attempting to load the model via xrv.models.get_model("densenet121-res224-all", from_hf_hub=True) resulted in a TypeError: DenseNet.**init**() got an unexpected keyword argument 'from_hf_hub'.

Solution: Bypassed the wrapper function and instantiated the class directly using the exact weights keyword: xrv.models.DenseNet(weights="densenet121-res224-all").

2. ONNX Exporter Dependency Missing
   Problem: ModuleNotFoundError: No module named 'onnxscript'. PyTorch's newer Dynamo-based exporter requires this module for ONNX translation.

Solution: Added onnxscript to the requirements.txt environment.

3. Data-Dependent Tracing Errors (GuardOnDataDependentSymNode)
   Problem: During torch.onnx.export, the Dynamo tracer crashed with Could not guard on data-dependent expression Eq(u0, 1).

Cause: The torchxrayvision library includes a warn_normalization(x) function in its forward pass. This function dynamically evaluates x.min() and x.max() at runtime to warn users if the image isn't normalized properly. Symbolic graph tracing cannot compile dynamic if statements based on tensor data values.

Solution:

Temporarily monkey-patched the library function during export: xrv.utils.warn_normalization = lambda x: None.

Switched from the experimental Dynamo exporter (dynamo=True) to the legacy TorchScript tracing engine (dynamo=False) targeting Opset 18.

4. ONNX Runtime Shape Inference Failure
   Problem: At inference time, onnxruntime crashed with: Non-zero status code returned while running Reshape node... input_shape_size == requested_shape_size was false.

Cause: The default DenseNet module in torchxrayvision executes custom features2() pooling and dynamic resolution fixing (fix_resolution). When exported to ONNX with dynamic_axes, these internal reshapes compiled into static sizes that broke when evaluating variable batch sizes.

Solution: Created a custom wrapper class, ExportableDenseNet(nn.Module). We extracted the raw base_model.features and base_model.classifier, completely bypassing the custom library functions. We manually bridged them using static, ONNX-friendly operations: torch.nn.functional.adaptive_avg_pool2d and torch.flatten.

5. API Namespace Errors (adaptive_avg_pool2d)
   Problem: AttributeError: module 'torch' has no attribute 'adaptive_avg_pool2d'.

Solution: Corrected the namespace call. The function lives in the functional API, requiring import torch.nn.functional as F and calling F.adaptive_avg_pool2d.

6. Broken Upstream Test Data (HTTP 404)
   Problem: The official torchxrayvision sample image URL was returning a 404 Not Found error, blocking pipeline verification.

Solution: Used numpy and PIL to generate a synthetic grayscale test image directly in memory, ensuring our ML pipeline tests are fully decoupled from external network resources.

7. Path Resolution in Standalone Scripts
   Problem: Running scripts/test_m3_worker.py threw ModuleNotFoundError: No module named 'app'.

Solution: Injected the project root into sys.path dynamically at the top of the test scripts using sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(**file**), ".."))).

🚀 Verification
The pipeline is fully verified end-to-end. Running python scripts/test_m3_worker.py successfully:

Creates a synthetic user and database record.

Uploads a sample image to MinIO.

Triggers the Celery task which orchestrates ONNX classification and PyTorch GradCAM.

Uploads the resulting heatmap to MinIO and updates the PostgreSQL record to ProcessingStatus.COMPLETED.
