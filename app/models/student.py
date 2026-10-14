import uuid
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class Student(Base):
    __tablename__ = "students_table"

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

    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools_table.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="student") # type: ignore

    school: Mapped["School"] = relationship(back_populates="students") # type: ignore

    orders: Mapped[List["Order"]] = relationship(back_populates="student", cascade="all, delete-orphan") # type: ignore