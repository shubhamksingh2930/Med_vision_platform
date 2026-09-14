MedVision — Explainable Medical Imaging AI
Platform
An end-to-end clinical decision support platform for chest X-ray pathology classification and
interpretability. The system uses a fine-tuned DenseNet-121 model deployed via ONNX Runtime for
high-performance inference, generates visual explanations using Grad-CAM with PyTorch, and provides
an authenticated single-page clinical console built with React and Vite.
Architecture Overview
 Frontend: React (Vite), Axios, Server-Sent Events (SSE) EventSource.
 API Layer: FastAPI, OAuth2 with JWT authentication, Pydantic v2 schemas, SSE streaming.
 Worker &amp; Queue: Celery with Redis broker, solo pool orchestration.
 ML &amp; Explainability Pipeline:
 Inference: TorchXRayVision DenseNet-121 (densenet121-res224-all, 18 pathology classes)
wrapped into a traceable ExportableDenseNet module and executed via onnxruntime.
 Explainability: Secondary forward/backward pass on raw PyTorch layers using
pytorch_grad_cam to generate Grad-CAM heatmaps.
 Preprocessing: Strict [-1024, 1024] pixel normalization with TorchXRayVision center crop and
resize (224x224).
 Storage: S3-compatible object storage (MinIO) using Boto3 presigned URLs.
 Database: PostgreSQL with SQLAlchemy ORM and Alembic migrations.
Milestone 4: Frontend &amp; API Integration Breakdown
Milestone 4 bridged the gap between the asynchronous worker pipeline and clinical end-users by
constructing a full web interface and the necessary API endpoints:

1. Authentication-Aware Data Flow: Gated access requiring JWT tokens for prediction creation,
   event subscriptions, and history retrieval.
2. Real-Time Job Tracking via SSE: Real-time status dispatching (pending → processing → completed
   / failed) using Server-Sent Events (sse-starlette).
3. Dual-Image Clinical Viewer: Side-by-side display of the original chest radiograph and the
   generated Grad-CAM heatmap overlay.
4. Sorted Pathology Probabilities: Dynamic parsing and sigmoid probability computation across all
   18 clinical pathology classes.
5. Paginated Historical Feed: User-scoped historical log allowing clinicians to inspect and reload past
   predictions.

Complete Setup &amp; Execution Guide (PowerShell)

1. Branch Checkout &amp; API Scaffolding

# Checkout milestone-4 branch

git checkout -b milestone-4

# Create backend API directories and files

New-Item -ItemType Directory -Force -Path app/api
New-Item -ItemType File -Force -Path app/api/**init**.py, app/api/routes.py,
app/api/schemas.py, app/main.py 2. Frontend Scaffolding

# Initialize Vite React template

npm create vite@latest frontend -- --template react

# Move into directory, install core dependencies, and create component structure

Set-Location frontend
npm install
npm install axios
New-Item -ItemType Directory -Force -Path src/components
New-Item -ItemType File -Force -Path src/api.js, src/components/Auth.jsx,
src/components/UploadDashboard.jsx, src/components/Viewer.jsx,
src/components/PredictionHistory.jsx, src/App.jsx
Set-Location .. 3. Running All System Services
Run each command in a separate terminal:
Terminal 1: FastAPI Backend (med_vision_backend)
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
Terminal 2: Celery Worker (med_vision_backend)
.\venv\Scripts\Activate.ps1
celery -A app.worker.celery_app worker --loglevel=info --pool=threads --concurrency=3
Terminal 3: React Frontend (med_vision_backend/frontend)
Set-Location frontend
npm run dev
Problems Encountered &amp; Resolutions

1. Terminal Environment &amp; Shell Syntax

 Problem: Standard Linux/Bash scaffolding commands (mkdir -p, touch) failed on Windows
PowerShell.
 Resolution: Replaced them with PowerShell commandlets: New-Item -ItemType Directory -Force
and New-Item -ItemType File -Force. 2. Vite Scaffolding in Pre-Created Directory
 Problem: Running npm run dev threw ENOENT: no such file or directory, open
&#39;frontend/package.json&#39; because file creation occurred before Vite initialized the package root.
 Resolution: Scaffolded Vite directly into the directory using npm create vite@latest . -- --template
react, selected &#39;Ignore files and continue&#39;, and installed project dependencies cleanly via npm install
and npm install axios. 3. Default Vite Landing Page Overriding Console
 Problem: Navigating to http://localhost:5173 rendered the default Vite/React placeholder instead of
the login interface.
 Resolution: Cleared all boilerplate styling inside src/index.css and src/App.css, ensured src/App.jsx
cleanly imported the authentication and dashboard components, and cleared stale tokens from
localStorage. 4. Router Definition Crash on Backend Reload
 Problem: Uvicorn crashed with NameError: name &#39;router&#39; is not defined during code updates.
 Resolution: Restored the complete file structure in app/api/routes.py, ensuring APIRouter()
initialization, database models, Boto3 storage client, and task imports preceded route decorator
declarations. 5. SSE Authorization Header Limitations
 Problem: Native browser EventSource APIs cannot send custom headers (such as Authorization:
Bearer &lt;token&gt;), blocking authenticated live status tracking.
 Resolution: Updated prediction_events in app/api/routes.py to accept the JWT as a query
parameter (token: str = Query(...)), manually validating the payload and user_id subject claim inside
the route. 6. Negative Percentage Outputs in UI
 Problem: The UI rendered negative finding values (e.g., -18.8%, -92.5%).
 Resolution: The ONNX DenseNet-121 model outputs raw logit scores rather than normalized
probabilities. Implemented a sigmoid mathematical transformation in
frontend/src/components/Viewer.jsx: σ(x) = 1 / (1 + e^(-x)). This normalized all outputs into valid
probabilities [0, 1] before scaling by 100.

7. Broken Images via Direct MinIO Paths (403 Forbidden)
    Problem: &lt;img&gt; tags failed to render the original chest X-ray and Grad-CAM heatmap because the
   backend returned raw MinIO bucket URLs (http://127.0.0.1:9000/med-vision-bucket/...) that lacked
   public read access.
    Resolution: Updated get_prediction in app/api/routes.py to intercept the response and call
   storage_client.get_presigned_url(key) for both original_image_url_key and
   heatmap_image_url_key, yielding valid, time-limited presigned GET URLs for browser rendering.
