import uuid
import json
import asyncio
import redis
from fastapi import APIRouter, Request, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
from jose import jwt, JWTError

from app.core.config import settings
from app.core.limiter import limiter
from app.db.session import get_db
from app.db.models import PredictionRecord, User
from app.api.deps import get_current_user
from app.storage.client import storage_client
from app.worker.tasks import process_prediction_job
from app.api.schemas import (
    PredictionCreateResponse,
    PredictionDetail,
    PredictionListResponse,
    PredictionListItem,
)

router = APIRouter()

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    checks = {}

    try:
        db.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as exc:
        checks["postgres"] = f"error: {exc}"

    try:
        redis_client = redis.from_url(settings.redis_url, socket_connect_timeout=2)
        redis_client.ping()
        checks["redis"] = "ok"
    except Exception as exc:
        checks["redis"] = f"error: {exc}"

    try:
        storage_client.client.head_bucket(Bucket=storage_client.bucket)
        checks["storage"] = "ok"
    except Exception as exc:
        checks["storage"] = f"error: {exc}"

    failed = [name for name, result in checks.items() if result != "ok"]
    if failed:
        return JSONResponse(status_code=503, content={"status": "not ready", "checks": checks, "failed": failed})
    return {"status": "ready", "checks": checks}


@router.post("/predictions", response_model=PredictionCreateResponse, status_code=202)
@limiter.limit("5/hour")
def create_prediction(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, "Only PNG/JPEG supported in v1")

    contents = file.file.read()
    if len(contents) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(413, "File exceeds maximum allowed size of 10MB")
    file.file.seek(0)

    record = PredictionRecord(
        user_id=current_user.id,
        original_filename=file.filename,
        mime_type=file.content_type,
        original_image_url="",
        original_image_url_key="",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    key = f"uploads/{record.id}.png"
    url = storage_client.upload_file(file.file, key, file.content_type)
    record.original_image_url = url
    record.original_image_url_key = key
    db.commit()

    process_prediction_job.delay(str(record.id))
    return PredictionCreateResponse(id=record.id, status=record.status.value)


@router.get("/predictions", response_model=PredictionListResponse)
def list_predictions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        db.query(PredictionRecord)
        .filter(PredictionRecord.user_id == current_user.id)
        .order_by(PredictionRecord.created_at.desc())
    )
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PredictionListResponse(
        items=[PredictionListItem.model_validate(r) for r in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/predictions/{prediction_id}", response_model=PredictionDetail)
def get_prediction(
    prediction_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(PredictionRecord)
        .filter(
            PredictionRecord.id == prediction_id,
            PredictionRecord.user_id == current_user.id,
        )
        .first()
    )
    if not record:
        raise HTTPException(404, "Not found")

    detail = PredictionDetail.model_validate(record)

    if record.original_image_url_key:
        try:
            detail.original_image_url = storage_client.get_presigned_url(record.original_image_url_key)
        except Exception:
            pass

    if getattr(record, "heatmap_image_url_key", None):
        try:
            detail.heatmap_image_url = storage_client.get_presigned_url(record.heatmap_image_url_key)
        except Exception:
            pass
    elif record.heatmap_image_url and "heatmaps/" in record.heatmap_image_url:
        key = "heatmaps/" + record.heatmap_image_url.split("heatmaps/")[-1]
        try:
            detail.heatmap_image_url = storage_client.get_presigned_url(key)
        except Exception:
            pass

    return detail


@router.get("/predictions/{prediction_id}/events")
async def prediction_events(
    prediction_id: uuid.UUID,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    async def event_generator():
        last_status = None
        while True:
            db.expire_all()
            record = (
                db.query(PredictionRecord)
                .filter(
                    PredictionRecord.id == prediction_id,
                    PredictionRecord.user_id == uuid.UUID(user_id),
                )
                .first()
            )
            if not record:
                yield {"event": "error", "data": "not_found"}
                break
            if record.status.value != last_status:
                last_status = record.status.value
                yield {"event": "status", "data": json.dumps({"status": last_status})}
            if record.status.value in ("completed", "failed"):
                break
            await asyncio.sleep(2)

    return EventSourceResponse(event_generator())