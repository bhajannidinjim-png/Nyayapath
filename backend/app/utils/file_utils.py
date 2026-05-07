from pathlib import Path
import re
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.config.settings import ALLOWED_EXTENSIONS, MAX_UPLOAD_BYTES, MAX_UPLOAD_MB, UPLOAD_DIR


CHUNK_SIZE = 1024 * 1024


def _safe_filename(filename: str) -> str:
    name = Path(filename or "judgment.pdf").name
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return name or "judgment.pdf"


def validate_pdf(file: UploadFile) -> None:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    if file.content_type and file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")


def save_upload(file: UploadFile) -> Path:
    validate_pdf(file)
    safe_name = _safe_filename(file.filename or "judgment.pdf")
    destination = UPLOAD_DIR / f"{uuid4().hex}_{safe_name}"
    total = 0
    with destination.open("wb") as buffer:
        while chunk := file.file.read(CHUNK_SIZE):
            total += len(chunk)
            if total > MAX_UPLOAD_BYTES:
                destination.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail=f"PDF is too large. Maximum allowed size is {MAX_UPLOAD_MB} MB.")
            buffer.write(chunk)
    return destination
