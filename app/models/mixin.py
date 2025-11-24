from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .user import User


class UserRelationMixin:
    _user_id_nullable: bool = False
    _user_id_unique: bool = False
    _user: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[str]:
        return mapped_column(
            ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=cls._user,
        )
