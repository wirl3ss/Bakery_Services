import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.core.exceptions import (
    SchoolNameAlreadyExistsError,
    SchoolAddressAlreadyExistsError,
    SchoolNotFoundError,
    UnableToDeleteSchoolError,
    UnableToUpdateSchoolError,
)
from app.models.school import School

# Get School

async def get_all_schools(db: AsyncSession) -> Sequence[School]:
    stmt = select(School)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> School | None:
    return await db.get(School, id)

async def get_by_name(db: AsyncSession, name: str) -> School | None:
    stmt = select(School).where(School.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_by_address(db: AsyncSession, address: str) -> School | None:
    stmt = select(School).where(School.address == address)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Create School

async def create_school(db: AsyncSession, school: School) -> School:
    if await get_by_name(db, school.name) is not None:
        raise SchoolNameAlreadyExistsError()

    if await get_by_address(db, school.address) is not None:
        raise SchoolAddressAlreadyExistsError()

    db.add(school)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise SchoolAddressAlreadyExistsError from exc

    await db.refresh(school)
    return school

# Update School

async def update_school(
    db: AsyncSession,
    id: uuid.UUID,
    data: dict,
) -> School:
    school = await get_by_id(db, id)
    if school is None:
        raise SchoolNotFoundError()

    try:
        stmt = (
            update(School)
            .where(School.id == id)
            .values(**data)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(school)

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateSchoolError from exc

    return school

# Delete School

async def delete_school(db: AsyncSession, id: uuid.UUID) -> None:
    school = await get_by_id(db, id)
    if school is None:
        raise SchoolNotFoundError()

    try:
        await db.delete(school)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteSchoolError from exc