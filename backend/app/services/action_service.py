from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import ActionItem
from app.schemas.actions import VerificationRequest


APPROVED = "approved"
REJECTED = "rejected"
PENDING = "pending"


def list_actions(db: Session, status: str | None = None, department: str | None = None, search: str | None = None):
    query = db.query(ActionItem)
    if status:
        query = query.filter(ActionItem.verification_status == status)
    if department:
        query = query.filter(ActionItem.department == department)
    if search:
        term = f"%{search}%"
        query = query.filter(ActionItem.action_summary.ilike(term) | ActionItem.source_text.ilike(term))
    return query.order_by(ActionItem.created_at.desc()).all()


def get_action(db: Session, action_id: int) -> ActionItem:
    action = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found.")
    return action


def verify_action(db: Session, action_id: int, payload: VerificationRequest):
    if payload.status not in {APPROVED, REJECTED, PENDING}:
        raise HTTPException(status_code=400, detail="Status must be approved, rejected, or pending.")

    action = get_action(db, action_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "status":
            continue
        setattr(action, field, value)
    action.verification_status = payload.status
    db.commit()
    db.refresh(action)
    return action

