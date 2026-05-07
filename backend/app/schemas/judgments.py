from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.actions import ActionOut


class MetadataField(BaseModel):
    value: str
    confidence: float
    source_text: str
    extraction_reason: str
    page_reference: int | None = None


class JudgmentOut(BaseModel):
    id: int
    filename: str
    status: str
    total_pages: int
    scanned_pages: list[int]
    metadata_json: dict[str, Any]
    pages_json: list[dict[str, Any]]
    created_at: datetime
    actions: list[ActionOut] = []

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    judgment: JudgmentOut
    message: str

