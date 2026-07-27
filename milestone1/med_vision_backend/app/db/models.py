import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProcessingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    original_filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    file_size_bytes = Column(String, nullable=False) # or BigInteger, keeping string for simplicity if Alembic expects it
    
    r2_image_key = Column(String, nullable=False)   # S3 key/URL of uploaded image
    r2_log_key = Column(String, nullable=True)      # S3 key for audit log

    # Heatmap & results for ML worker
    heatmap_image_url = Column(String, nullable=True)      # filled in after processing completes
    prediction_result = Column(String, nullable=True)       # JSON string

    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)