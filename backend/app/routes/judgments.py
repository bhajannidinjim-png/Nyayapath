from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.judgments import JudgmentOut, UploadResponse
from app.services.judgment_service import get_judgment, get_judgments, process_upload

router = APIRouter(prefix="/judgments", tags=["judgments"])


@router.post("/upload", response_model=UploadResponse)
def upload_judgment(file: UploadFile = File(...), db: Session = Depends(get_db)):
    judgment = process_upload(db, file)
    return {"judgment": judgment, "message": "Judgment extracted. Human verification is required before dashboard publication."}


@router.get("", response_model=list[JudgmentOut])
def list_judgments(db: Session = Depends(get_db)):
    return get_judgments(db)


@router.get("/{judgment_id}", response_model=JudgmentOut)
def read_judgment(judgment_id: int, db: Session = Depends(get_db)):
    judgment = get_judgment(db, judgment_id)
    if not judgment:
        raise HTTPException(status_code=404, detail="Judgment not found.")
    return judgment

