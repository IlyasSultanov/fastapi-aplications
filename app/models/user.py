from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import BaseModel


class User(BaseModel):
    first_name: Mapped[str] = mapped_column(description="Write your first name")
    last_name: Mapped[str] = mapped_column(description="Write your last name")
    email: Mapped[str] = mapped_column(
        description="Write your email", unique=True, index=True
    )
    password: Mapped[str] = mapped_column(description="Write your password")
