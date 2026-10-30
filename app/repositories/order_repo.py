import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.core.exceptions import (
    UnableToCreateOrderError,
    OrderNotFoundError,
    UnableToUpdateOrderError,
    UnableToDeleteOrderError,
)
from app.models.order import Order

# Get Order

async def get_all_orders(
    db: AsyncSession,
    student_id: uuid.UUID | None = None,
    product_id: uuid.UUID | None = None,
    day: int | None = None,
) -> Sequence[Order]:

    stmt = select(Order)

    if student_id is not None:
        stmt = stmt.where(Order.student_id == student_id)

    if product_id is not None:
        stmt = stmt.where(Order.product_id == product_id)

    if day is not None:
        stmt = stmt.where(Order.day == day)

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

async def get_by_day(db: AsyncSession, day: int) -> Sequence[Order]:
    stmt = select(Order).where(Order.day == day)
    result = await db.execute(stmt)
    return result.scalars().all()

# Create Order

async def create_order(
    db: AsyncSession,
    order: Order,
) -> Order:

    db.add(order)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise UnableToCreateOrderError from exc

    await db.refresh(order)
    return order

async def update_order(
        db: AsyncSession,
        id: uuid.UUID,
        data: dict,
) -> Order:
    order = await get_by_id(db, id)
    if order is None:
        raise OrderNotFoundError()

    try:
        stmt = (
            update(Order)
            .where(Order.id == id)
            .values(**data)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(order)

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateOrderError from exc

    return order

async def delete_order(db: AsyncSession, id: uuid.UUID) -> None:
    order = await get_by_id(db, id)
    if order is None:
        raise OrderNotFoundError()

    try:
        await db.delete(order)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteOrderError from exc

    