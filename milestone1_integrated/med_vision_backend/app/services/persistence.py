from sqlalchemy.orm import Session
from app.db.models import PredictionRecord, ProcessingStatus

class PersistenceService:
    def save_result(self, db: Session, record_id: str, result: dict):
        record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
        if not record:
            raise ValueError(f"No prediction record found for id={record_id}")

        record.prediction_result = result["prediction_result"]
        record.heatmap_image_url = result["heatmap_image_url"]
        record.status = ProcessingStatus.COMPLETED
        db.commit()

    def mark_failed(self, db: Session, record_id: str, error: str):
        record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
        if record:
            record.status = ProcessingStatus.FAILED
            record.error_message = error
            db.commit()

persistence_service = PersistenceService()