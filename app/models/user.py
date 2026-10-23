import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class Role(enum.Enum):
    STUDENT = "student"
    SHOP = "shop"
    ADMIN = "admin"
    NOT_SPECIFIED = "not_specified"

class User(Base):
    __tablename__ = "users_table"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    username: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role"),
        nullable=False,
        default=Role.NOT_SPECIFIED  
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    student: Mapped["Student"] = relationship(back_populates="user", cascade="all, delete-orphan") # type: ignore

    shop: Mapped["Shop"] = relationship(back_populates="user", cascade="all, delete-orphan") # type: ignore