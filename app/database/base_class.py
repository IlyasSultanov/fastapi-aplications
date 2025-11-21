from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped


from . import Base


class BaseModel(Base):

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True)

    # Timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Soft delete support
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r})"