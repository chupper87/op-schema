from ..core.base import Base
from datetime import datetime, timezone, timedelta
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, String, Text, Boolean, func, ForeignKey


class Token(Base):
    __tablename__ = "tokens"

    # Token information
    token: Mapped[str] = mapped_column(String, unique=True, index=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    expire_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=24),
    )
    # Relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="tokens")


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=False
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="user",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    tokens: Mapped[List["Token"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )

    @property
    def full_name(self) -> str:
        return f"{self.employee.first_name} {self.employee.last_name}"

    @property
    def role(self) -> str:
        return self.employee.role

    @property
    def schedules(self):
        """Returns all schedules for the user via employee"""
        return [se.schedule for se in self.employee.schedules]

    def __repr__(self) -> str:
        return f"<User {self.username}>"
