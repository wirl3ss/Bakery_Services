import uuid
from datetime import date
from sqlalchemy import ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class CalendarException(Base):
    __tablename__ = "calendar_exceptions_table"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    shop_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shops_table.id", ondelete="CASCADE"),
        nullable=False,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    shop: Mapped["Shop"] = relationship(back_populates="calendar_exceptions") # type: ignore

    __table_args__ = (
        UniqueConstraint(
            "shop_id",
            "date",
            name="uq_calendar_exception_shop_date",
        ),
    )