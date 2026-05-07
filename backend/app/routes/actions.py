from fastapi import APIRouter

router = APIRouter(prefix="/actions", tags=["actions"])

@router.get("")
def read_actions(status: str | None = None):
    return [
        {
            "id": 1,
            "title": "Test Action",
            "status": status or "approved"
        }
    ]
