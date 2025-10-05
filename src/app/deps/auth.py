from __future__ import annotations
from fastapi import HTTPException, Request


def require_auth(request: Request):
    if not getattr(request.state, "user_id", None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request.state.user_id
