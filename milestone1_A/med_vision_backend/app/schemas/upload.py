import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.db.models import ProcessingStatus

class MedicalRecordOut(BaseModel):
    id: uuid.UUID
    original_filename: str
    mime_type: str
    file_size_bytes: int
    r2_image_key: str
    r2_log_key: str
    status: ProcessingStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MedicalRecordListOut(BaseModel):
    total: int
    items: list[MedicalRecordOut]