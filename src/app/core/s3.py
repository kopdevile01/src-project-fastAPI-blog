from __future__ import annotations

import logging
import uuid
from pathlib import Path

import boto3
from botocore.config import Config as BotoConfig
from app.core.settings import settings

_cfg = BotoConfig(
    s3={"addressing_style": "path"},
    retries={"max_attempts": 3, "mode": "standard"},
)

_s3 = boto3.client(
    "s3",
    endpoint_url=settings.s3_endpoint,
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name="us-east-1",
    config=_cfg,
)

log = logging.getLogger(__name__)


def upload_bytes(key: str, data: bytes, *, content_type: str | None) -> str:
    extra = {}
    if content_type:
        extra["ContentType"] = content_type

    try:
        _s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=data, **extra)
    except Exception:  # noqa: BLE001 - логируем стек и пробрасываем дальше
        log.exception("S3 upload failed")
        raise

    return f"{settings.s3_public_url}/{settings.s3_bucket}/{key}"


def gen_image_key(filename: str | None) -> str:
    ext = Path(filename or "").suffix.lower() or ".bin"
    return f"images/{uuid.uuid4().hex}{ext}"
