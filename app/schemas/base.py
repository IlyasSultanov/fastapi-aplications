from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Base(BaseModel):
    id: UUID = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    deleted_at: datetime = Field(...)