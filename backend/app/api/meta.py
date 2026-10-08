from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.employee import Employee

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    """Returns service status and current employee count."""
    employee_count = db.query(Employee).count()
    return {"status": "ok", "employee_count": employee_count}
