import uuid, enum
from datetime import datetime, timezone, date
from sqlalchemy import String, ForeignKey, Integer, DateTime, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class Order(Base):
    __tablename__ = "orders_table"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students_table.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products_table.id", ondelete="CASCADE"),
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    day: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=lambda: date.today()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    student: Mapped["Student"] = relationship(back_populates="orders") # type: ignore

    product: Mapped["Product"] = relationship(back_populates="orders") # type: ignore

    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_amount"),
    )