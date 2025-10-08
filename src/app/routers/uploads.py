from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from app.core.s3 import gen_image_key, upload_bytes

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Only images are allowed")

    data = await file.read()
    key = gen_image_key(file.filename)
    try:
        url = upload_bytes(key, data, content_type=file.content_type)
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload failed")

    return {"url": url, "key": key}
