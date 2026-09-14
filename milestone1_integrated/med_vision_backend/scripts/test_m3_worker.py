import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uuid
from app.db.session import SessionLocal
from app.db.models import PredictionRecord, ProcessingStatus, User
from app.storage.client import storage_client
from app.worker.tasks import process_prediction_job

db = SessionLocal()
try:
    user = db.query(User).first()
    if not user:
        user = User(
            email="test_m3@example.com",
            hashed_password="dummy_password",
            full_name="M3 Tester",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    record_id = str(uuid.uuid4())
    s3_key = f"uploads/{record_id}.png"
    with open("test_data/sample_xray.png", "rb") as f:
        image_url = storage_client.upload_file(f, s3_key, "image/png")

    record = PredictionRecord(
        id=record_id,
        user_id=user.id,
        original_image_url=image_url,
        status=ProcessingStatus.pending,
    )
    db.add(record)
    db.commit()
    print(f"Created pending record {record_id}")

    print("Executing worker task...")
    process_prediction_job(record_id)

    db.refresh(record)
    print(f"Final status: {record.status}")
    print(f"Heatmap URL: {record.heatmap_image_url}")
    print(f"Prediction result stored: {bool(record.prediction_result)}")

    assert record.status == ProcessingStatus.completed
    assert record.heatmap_image_url is not None
    print("\nMilestone 3 Worker pipeline verified end-to-end!")

finally:
    db.close()
