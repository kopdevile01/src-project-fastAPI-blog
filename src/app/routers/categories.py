from __future__ import annotations
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps.auth import require_auth
from app.schemas.category import CategoryCreate, CategoryOut
from app.services import categories as svc

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
):
    return svc.list_categories(
        db,
        page_number=page_number,
        page_size=page_size,
        search=search,
    )


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_auth)],
)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return svc.create_category(db, payload)
