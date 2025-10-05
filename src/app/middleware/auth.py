from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.security import decode_jwt


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        request.state.user_id = None
        if token:
            try:
                payload = decode_jwt(token)
                request.state.user_id = payload.get("sub")
            except Exception:
                pass
        return await call_next(request)
