from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone

from app.models.users import PyObjectId


class NoteModel(BaseModel):

    id: PyObjectId = Field(
        default=None,
        alias="_id",
        serialization_alias="id",
    )
    title: str = Field(max_length=256)
    body: str = Field(max_length=65536)
    user_id: PyObjectId = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    deleted: bool = False


class NoteCreate(BaseModel):
    title: str = Field(..., max_length=256)
    body: str = Field(..., max_length=65536)


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    body: str
    created_at: datetime
    updated_at: datetime | None = None
