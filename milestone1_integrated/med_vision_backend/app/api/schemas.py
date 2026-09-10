from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class PredictionCreateResponse(BaseModel):
    id: uuid.UUID
    status: str

class PredictionDetail(BaseModel):
    id: uuid.UUID
    status: str
    original_image_url: str
    heatmap_image_url: Optional[str] = None
    prediction_result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PredictionListItem(BaseModel):
    id: uuid.UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class PredictionListResponse(BaseModel):
    items: List[PredictionListItem]
    total: int
    page: int
    page_size: int