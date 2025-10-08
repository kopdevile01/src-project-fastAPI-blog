from __future__ import annotations
from fastapi import HTTPException, Request, status


def require_auth(request: Request):
    if not getattr(request.state, "user_id", None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return request.state.user_id
