from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.mid import time_now


class BaseSchemas(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={"example": {"id": "550e8400-e29b-41d4-a716-446655440000"}},
    )


class Base(BaseSchemas):

    id: UUID = Field(...)
    created_at: datetime = Field(default_factory=time_now)
    updated_at: datetime = Field(default_factory=time_now)
    deleted_at: Optional[datetime] = Field(default=None)
