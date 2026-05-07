from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.actions import ActionOut, VerificationRequest
from app.services.action_service import get_action, list_actions, verify_action

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("/test")
def test_actions():
    return {"actions": "working"}


@router.get("", response_model=list[ActionOut])
def read_actions(
    status: str | None = None,
    department: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    return list_actions(
        db,
        status=status,
        department=department,
        search=search
    )


@router.get("/{action_id}", response_model=ActionOut)
def read_action(
    action_id: int,
    db: Session = Depends(get_db)
):
    return get_action(db, action_id)


@router.patch("/{action_id}/verify", response_model=ActionOut)
def verify(
    action_id: int,
    payload: VerificationRequest,
    db: Session = Depends(get_db)
):
    return verify_action(db, action_id, payload)
