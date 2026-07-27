import io
import uuid
import json
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.models import MedicalRecord, User, ProcessingStatus
from app.schemas.upload import MedicalRecordOut, MedicalRecordListOut
from app.storage.client import storage_client

router = APIRouter()

ALLOWED_MIME_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "application/pdf": ".pdf",
    "application/dicom": ".dcm",
    "image/dicom": ".dcm",
    "application/x-dicom": ".dcm",
    "application/octet-stream": ".dcm"
}

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".dcm"}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB Limit

def get_file_extension(filename: str | None, mime_type: str) -> str | None:
    if filename:
        lower_name = filename.lower()
        for ext in ALLOWED_EXTENSIONS:
            if lower_name.endswith(ext):
                return ".jpg" if ext in (".jpg", ".jpeg") else ext
    return ALLOWED_MIME_TYPES.get(mime_type)

@router.post("/", response_model=MedicalRecordOut, status_code=status.HTTP_201_CREATED)
def upload_medical_record(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    extension = get_file_extension(file.filename, file.content_type)
    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported media type '{file.content_type}'. Allowed formats: PNG, JPEG, PDF, DICOM (.dcm)."
        )

    file_bytes = file.file.read()
    file_size = len(file_bytes)

    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum allowed limit of 100MB."
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty."
        )

    record_id = uuid.uuid4()
    r2_image_key = f"raw_images/{current_user.id}/{record_id}{extension}"
    r2_log_key = f"logs/{current_user.id}/{record_id}_audit.json"

    storage_client.upload_file(io.BytesIO(file_bytes), r2_image_key, content_type=file.content_type or "application/octet-stream")

    audit_log = {
        "record_id": str(record_id),
        "user_id": str(current_user.id),
        "original_filename": file.filename or "unknown",
        "mime_type": file.content_type,
        "file_size_bytes": file_size,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "VALIDATED_AND_STORED"
    }
    storage_client.upload_file(io.BytesIO(json.dumps(audit_log).encode("utf-8")), r2_log_key, content_type="application/json")

    db_record = MedicalRecord(
        id=record_id,
        user_id=current_user.id,
        original_filename=file.filename or "unknown",
        mime_type=file.content_type or "application/octet-stream",
        file_size_bytes=str(file_size),
        r2_image_key=r2_image_key,
        r2_log_key=r2_log_key,
        status=ProcessingStatus.PENDING
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record

@router.get("/", response_model=MedicalRecordListOut)
def list_medical_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(MedicalRecord).filter(MedicalRecord.user_id == current_user.id).order_by(MedicalRecord.created_at.desc()).all()
    return {"total": len(records), "items": records}

@router.get("/{record_id}", response_model=MedicalRecordOut)
def get_medical_record(
    record_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record or record.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found.")
    return record