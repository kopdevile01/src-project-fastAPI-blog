from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.auth import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login")
def login(payload: UserCreate, response: Response, db: Session = Depends(get_db)):
    token = authenticate_user(db, email=payload.email, password=payload.password)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    response.set_cookie(
        "access_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return {"access_token": token}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"ok": True}
