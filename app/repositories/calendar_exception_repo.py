import uuid
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.models.calendar_exception import CalendarException
from app.core.exceptions import (
    CalendarExceptionAlreadyExistsError,
    UnableToCreateCalendarExceptionError,
    CalendarExceptionNotFoundError,
    UnableToUpdateCalendarExceptionError,
    UnableToDeleteCalendarExceptionError,
)

async def get_all(db: AsyncSession) -> Sequence[CalendarException]:
    stmt = select(CalendarException)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> CalendarException | None:
    return await db.get(CalendarException, id)

async def get_by_shop(db: AsyncSession, shop_id: uuid.UUID) -> Sequence[CalendarException]:
    stmt = select(CalendarException).where(CalendarException.shop_id == shop_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_date(db: AsyncSession, date: date) -> Sequence[CalendarException]:
    stmt = select(CalendarException).where(CalendarException.date == date)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_shop_date(
    db: AsyncSession,
    shop_id: uuid.UUID,
    date: date,
) -> CalendarException | None:
    stmt = (
        select(CalendarException)
        .where(CalendarException.shop_id == shop_id)
        .where(CalendarException.date == date)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Create CalendarException

async def create_calendar_exception(
    db: AsyncSession,
    calendar_exception: CalendarException,
) -> CalendarException:

    if await get_by_shop_date(
        db,
        calendar_exception.shop_id,
        calendar_exception.date,
    ) is not None:
        raise CalendarExceptionAlreadyExistsError()

    db.add(calendar_exception)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise UnableToCreateCalendarExceptionError from exc

    await db.refresh(calendar_exception)
    return calendar_exception

# Update CalendarException

async def update_calendar_exception(
    db: AsyncSession,
    id: uuid.UUID,
    data: dict,
) -> CalendarException:

    calendar_exception = await get_by_id(db, id)
    if calendar_exception is None:
        raise CalendarExceptionNotFoundError()

    try:
        stmt = (
            update(CalendarException)
            .where(CalendarException.id == id)
            .values(**data)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(calendar_exception)

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateCalendarExceptionError from exc

    return calendar_exception

# Delete CalendarException

async def delete_calendar_exception(db: AsyncSession, id: uuid.UUID) -> None:
    calendar_exception = await get_by_id(db, id)
    if calendar_exception is None:
        raise CalendarExceptionNotFoundError()

    try:
        await db.delete(calendar_exception)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteCalendarExceptionError from exc