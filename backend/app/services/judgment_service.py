from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.extraction.action_engine import generate_actions
from app.extraction.metadata_extractor import extract_metadata
from app.extraction.pdf_extractor import extract_pdf_pages
from app.models import ActionItem, Judgment
from app.utils.file_utils import save_upload


def process_upload(db: Session, file: UploadFile) -> Judgment:
    path = save_upload(file)
    try:
        extracted = extract_pdf_pages(path)
        metadata = extract_metadata(extracted["pages"])
        actions = generate_actions(extracted["pages"])

        judgment = Judgment(
            filename=file.filename or path.name,
            file_path=str(path),
            status="pending_verification",
            total_pages=extracted["total_pages"],
            scanned_pages=extracted["scanned_pages"],
            metadata_json=metadata,
            pages_json=extracted["pages"],
        )
        db.add(judgment)
        db.flush()

        for action in actions:
            db.add(ActionItem(judgment_id=judgment.id, **action))

        db.commit()
        db.refresh(judgment)
        return judgment
    except HTTPException:
        db.rollback()
        path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        db.rollback()
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Unable to process this PDF: {exc}") from exc


def get_judgments(db: Session):
    return db.query(Judgment).order_by(Judgment.created_at.desc()).all()


def get_judgment(db: Session, judgment_id: int):
    return db.query(Judgment).filter(Judgment.id == judgment_id).first()
