from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreatorBase(BaseModel):
    name: str
    platform: str
    handle: str


class CreatorCreate(CreatorBase):
    pass


class Creator(CreatorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ClipBase(BaseModel):
    creator_id: int
    title: str
    platform: str
    url: str
    thumbnail_url: str
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    posted_at: datetime


class ClipCreate(ClipBase):
    pass


class Clip(ClipBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    viral_score: float
    created_at: datetime
