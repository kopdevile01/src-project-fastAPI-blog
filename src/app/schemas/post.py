from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int
    image_url: str | None = None


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None
    image_url: str | None = None


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    image_url: str | None
    category_id: int
    model_config = ConfigDict(from_attributes=True)
