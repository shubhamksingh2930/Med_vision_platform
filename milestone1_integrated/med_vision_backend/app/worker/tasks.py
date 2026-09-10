from app.worker.celery_app import celery_app
from app.db.session import SessionLocal
from app.db.models import PredictionRecord, ProcessingStatus
from app.services.inference import inference_service
from app.services.persistence import persistence_service

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_prediction_job(self, record_id: str):
    """
    Orchestration only. Does not touch S3, ONNX, or GradCAM directly —
    delegates to inference_service and persistence_service.
    """
    db = SessionLocal()
    try:
        record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
        if not record:
            raise ValueError(f"No record found for id={record_id}")

        # pending -> processing
        record.status = ProcessingStatus.processing
        db.commit()

        # delegate to inference (stubbed until M3)
        result = inference_service.run(record.original_image_url)

        # delegate to persistence -> processing -> completed
        persistence_service.save_result(db, record_id, result)

    except Exception as exc:
        persistence_service.mark_failed(db, record_id, str(exc))
        raise self.retry(exc=exc)
    finally:
        db.close()