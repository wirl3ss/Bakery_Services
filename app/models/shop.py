import uuid
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class Shop(Base):
    __tablename__ = "shops_table"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users_table.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="shop") # type: ignore

    products: Mapped[List["Product"]] = relationship(back_populates="shop", cascade="all, delete-orphan") # type: ignore

    weekly_schedules: Mapped[List["WeeklySchedule"]] = relationship(     # type: ignore
        back_populates="shop",
        cascade="all, delete-orphan"
    )

    calendar_exceptions: Mapped[List["CalendarException"]] = relationship( # type: ignore
        back_populates="shop",
        cascade="all, delete-orphan"
    )