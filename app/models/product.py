import uuid
from typing import List
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Numeric, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class Product(Base):
    __tablename__ = "products_table"

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

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    shop: Mapped["Shop"] = relationship(back_populates="products") # type: ignore

    orders: Mapped[List["Order"]] = relationship(back_populates="product", cascade="all, delete-orphan") # type: ignore

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_prices")
    )