from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.s3 import gen_image_key, upload_bytes

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(400, detail="Only images are allowed")

    data = await file.read()
    key = gen_image_key(file.filename)
    try:
        url = upload_bytes(key, data, content_type=file.content_type)
    except Exception as e:
        raise HTTPException(500, detail=f"Upload failed: {e}") from e

    return {"url": url, "key": key}
