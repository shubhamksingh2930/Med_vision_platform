# MedVision — Explainable Chest X-Ray Platform

Predicts 18 pathological findings per chest X-ray and shows a Grad-CAM heatmap of exactly where the model looked for each result.

> **🚧 Under active development** — core pipeline is live and working. V2 roadmap includes model registry, DICOM ingestion, and production hardening. Expect rough edges.

## Live Demo

- **URL:** https://medviss.in
- Register free — no clinical data required. Built for learning and portfolio demonstration, not clinical diagnosis.

## What it does

Upload a chest X-ray (PNG/JPEG) and the model scores 18 independent pathological findings simultaneously — Lung Opacity, Mass, Consolidation, Effusion, Pneumonia, and more. A Grad-CAM heatmap overlays the exact image region that drove each prediction, giving you a visual explanation alongside the numbers. Results are stored in your prediction history, scoped to your account.

## Tech Stack

| Layer | Stack |
|---|---|
| Frontend | React (Vite), Axios, Server-Sent Events |
| API | FastAPI, JWT auth, Pydantic v2, SSE streaming |
| Queue | Celery, Redis |
| ML Inference | ONNX Runtime, TorchXRayVision DenseNet-121 (18 classes) |
| Explainability | Grad-CAM (PyTorch, separate forward pass) |
| Storage | MinIO (S3-compatible), Boto3 |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Deployment | Docker Compose, Cloudflare Tunnel |

## Architecture decisions worth noting

- The Celery worker is a thin orchestrator only — it never touches S3, the database, or the model directly, delegating to isolated InferenceService, GradCAMService, and PersistenceService classes.
- ONNX Runtime handles classification (fast, CPU-deployable); raw PyTorch handles Grad-CAM separately because ONNX doesn't expose intermediate layer activations.
- GradCAM's shared mutable hook state caused cross-user result contamination under concurrent load — fixed with a threading.Lock scoped to only the CAM call, keeping ONNX inference fully concurrent.
- SSE token auth uses a query parameter (not Authorization header) because browser EventSource cannot send custom headers — a known, accepted trade-off documented here explicitly.

## Model

- TorchXRayVision DenseNet-121, weights: densenet121-res224-all
- Trained on pooled public datasets: NIH ChestX-ray14, CheXpert, MIMIC-CXR, PadChest
- 18 independent sigmoid outputs (multi-label, not softmax — multiple findings can fire simultaneously)
- Preprocessing: center crop + resize to 224x224, pixel normalization to [-1024, 1024]
- Research-licensed weights. Not clinically validated. Not for diagnostic use.

## Running locally

```bash
# 1. Start infrastructure
docker compose up -d

# 2. Run migrations
alembic upgrade head

# 3. Export ONNX model (first time only)
python scripts/export_onnx.py

# 4. Start API (terminal 1)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 5. Start worker (terminal 2)
celery -A app.worker.celery_app worker --loglevel=info --pool=threads --concurrency=3

# 6. Start frontend (terminal 3)
cd frontend && npm install && npm run dev
```

## Known limitations / honest gaps

- No job idempotency — a retried Celery task could double-process
- SSE polling uses a single DB session across an async sleep loop (stale read risk)
- Presigned image URLs expire after 1 hour
- No rate limiting on the worker queue (only on the upload endpoint)
- Runs on local infrastructure (laptop + Cloudflare Tunnel) for this validation phase
