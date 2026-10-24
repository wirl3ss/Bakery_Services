import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence

from app.models.order import Order

# Get Order

async def get_all_orders(db: AsyncSession) -> Sequence[Order]:
    stmt = select(Order)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Order | None:
    return await db.get(Order, id)

async def get_by_student(db: AsyncSession, student_id: uuid.UUID) -> Sequence[Order]:
    stmt = select(Order).where(Order.student_id == student_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_product(db: AsyncSession, product_id: uuid.UUID) -> Sequence[Order]:
    stmt = select(Order).where(Order.product_id == product_id)
    result = await db.execute(stmt)
    return result.scalars().all()

