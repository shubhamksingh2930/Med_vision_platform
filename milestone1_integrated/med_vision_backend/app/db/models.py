import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

    # Backward compatibility aliases
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    original_filename = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    original_image_url = Column(String, nullable=False)
    original_image_url_key = Column(String, nullable=True)
    heatmap_image_url = Column(String, nullable=True)
    prediction_result = Column(String, nullable=True)

    status = Column(
        Enum(
            ProcessingStatus,
            name="processingstatus",
            values_callable=lambda obj: [e.value for e in obj],
            native_enum=True,
            create_type=False,
        ),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)