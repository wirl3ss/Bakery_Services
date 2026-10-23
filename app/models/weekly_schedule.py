import uuid
from sqlalchemy import ForeignKey, Integer, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class WeeklySchedule(Base):
    __tablename__ = "weekly_scheduels_table"

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

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_open: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    shop: Mapped["Shop"] = relationship(back_populates="weekly_schedules") # type: ignore

    __table_args__ = (
        CheckConstraint("day_of_week >= 0 AND day_of_week <= 6"),
    )