from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_jwt
from app.models.user import User
from app.tasks.email import send_registration_email


def register_user(db: Session, *, email: str, password: str) -> User:
    exists = db.scalar(select(User).where(User.email == email))
    if exists:
        raise ValueError("User already exists")

    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    send_registration_email.delay(to_email=email, username=email.split("@")[0])
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> str | None:
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return create_jwt(str(user.id))
