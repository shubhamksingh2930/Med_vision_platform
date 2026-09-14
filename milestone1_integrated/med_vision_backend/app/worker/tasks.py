import io
import json
import logging
import os
import tempfile
from urllib.parse import urlparse
from app.worker.celery_app import celery_app
from app.db.session import SessionLocal
from app.db.models import PredictionRecord, ProcessingStatus
from app.services.inference import inference_service
from app.services.gradcam import gradcam_service
from app.services.persistence import persistence_service
from app.storage.client import storage_client

logger = logging.getLogger(__name__)

def _extract_s3_key(url_or_key: str) -> str:
    if url_or_key.startswith("http://") or url_or_key.startswith("https://"):
        parsed = urlparse(url_or_key)
        parts = parsed.path.lstrip("/").split("/", 1)
        return parts[1] if len(parts) > 1 else parts[0]
    return url_or_key

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_prediction_job(self, record_id: str):
    db = SessionLocal()
    local_path = None
    try:
        record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
        if not record:
            raise ValueError(f"No record found for id={record_id}")

        if record.status == ProcessingStatus.completed:
            logger.info(f"Prediction {record_id} already completed, skipping reprocessing")
            return

        # pending -> processing
        record.status = ProcessingStatus.processing
        db.commit()

        # download original image to temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            local_path = tmp.name

        s3_key = _extract_s3_key(record.original_image_url)
        storage_client.download_file(s3_key, local_path)

        # classification via ONNX
        probabilities = inference_service.run(local_path)
        top_pathology = max(probabilities, key=probabilities.get)
        top_index = list(probabilities.keys()).index(top_pathology)

        # heatmap via GradCAM
        heatmap_bytes = gradcam_service.generate_heatmap(local_path, top_index)

        # upload heatmap to S3 / MinIO
        heatmap_key = f"heatmaps/{record_id}.png"
        heatmap_url = storage_client.upload_file(io.BytesIO(heatmap_bytes), heatmap_key, "image/png")

        # persist results -> completed
        result = {
            "prediction_result": json.dumps(probabilities),
            "heatmap_image_url": heatmap_url,
        }
        persistence_service.save_result(db, record_id, result)

    except Exception as exc:
        persistence_service.mark_failed(db, record_id, str(exc))
        raise self.retry(exc=exc)
    finally:
        if local_path and os.path.exists(local_path):
            os.remove(local_path)
        db.close()