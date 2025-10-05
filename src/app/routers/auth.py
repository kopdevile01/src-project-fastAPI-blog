from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.auth import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, email=payload.email, password=payload.password)
    except ValueError:
        raise HTTPException(409, detail="User already exists")
    return user


@router.post("/login")
def login(payload: UserCreate, response: Response, db: Session = Depends(get_db)):
    token = authenticate_user(db, email=payload.email, password=payload.password)
    if not token:
        raise HTTPException(401, detail="Invalid credentials")

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # в проде → True (если https)
        max_age=60 * 60,
    )
    return {"access_token": token}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"ok": True}
