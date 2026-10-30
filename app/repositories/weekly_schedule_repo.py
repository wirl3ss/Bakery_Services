import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from collections.abc import Sequence

from app.models.weekly_schedule import WeeklySchedule
from app.core.exceptions import (
    WeeklyScheduleAlreadyExistsError,
    UnableToCreateWeeklyScheduleError,
    WeeklyScheduleNotFoundError,
    UnableToUpdateWeeklyScheduleError,
)

# Get WeeklySchedule

async def get_all_weekly_schedules(
    db: AsyncSession,
    shop_id: uuid.UUID | None = None,
    day: int | None = None,
) -> Sequence[WeeklySchedule]:

    stmt = select(WeeklySchedule)

    if shop_id is not None:
        stmt = stmt.where(WeeklySchedule.shop_id == shop_id)

    if day is not None:
        stmt = stmt.where(WeeklySchedule.day_of_week == day)

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> WeeklySchedule | None:
    return await db.get(WeeklySchedule, id)

async def get_by_shop(db: AsyncSession, shop_id: uuid.UUID) -> Sequence[WeeklySchedule]:
    stmt = select(WeeklySchedule).where(WeeklySchedule.shop_id == shop_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_day(db: AsyncSession, day: int) -> Sequence[WeeklySchedule]:
    stmt = select(WeeklySchedule).where(WeeklySchedule.day_of_week == day)
    result = await db.execute(stmt)
    return result.scalars().all()

# create WeeklySchedule

async def create_weekly_schedule(
    db: AsyncSession,
    weekly_schedule: WeeklySchedule,
) -> WeeklySchedule:

    schedules = await get_all_weekly_schedules(
        db,
        weekly_schedule.shop_id,
        weekly_schedule.day_of_week,
    )

    if schedules:
        raise WeeklyScheduleAlreadyExistsError()

    db.add(weekly_schedule)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise UnableToCreateWeeklyScheduleError from exc

    await db.refresh(weekly_schedule)
    return weekly_schedule

# Update WeeklySchedule

async def update_weekly_schedule(
    db: AsyncSession,
    id: uuid.UUID,
    data: dict,
) -> WeeklySchedule:

    weekly_schedule = await get_by_id(db, id)
    if weekly_schedule is None:
        raise WeeklyScheduleNotFoundError()

    try:
        stmt = (
            update(WeeklySchedule)
            .where(WeeklySchedule.id == id)
            .values(**data)
        )

        await db.execute(stmt)
        await db.commit()
        await db.refresh(weekly_schedule)
    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateWeeklyScheduleError from exc

    return weekly_schedule

# Delete WeeklySchedule

async def delete_weekly_schedule(db: AsyncSession, id: uuid.UUID) -> None:
    weekly_schedule = await get_by_id(db, id)
    if weekly_schedule is None:
        raise WeeklyScheduleNotFoundError()

    try:
        await db.delete(weekly_schedule)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateWeeklyScheduleError from exc