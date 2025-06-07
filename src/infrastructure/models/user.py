import datetime

from sqlalchemy import ARRAY, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    permissions: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])
    created_at: Mapped[datetime.date] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.date | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, is_admin={self.is_admin})>"
