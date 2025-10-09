from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_jwt
from app.tasks.email import send_registration_email
from app.repositories import users as users_repo


def register_user(db: Session, *, email: str, password: str):
    if users_repo.get_by_email(db, email):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")

    user = users_repo.create(db, email=email, hashed_password=hash_password(password))

    send_registration_email.delay(to_email=email, username=email.split("@")[0])
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> str | None:
    user = users_repo.get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return create_jwt(str(user.id))
