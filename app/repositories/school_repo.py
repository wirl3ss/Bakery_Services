import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence

from app.services.exceptions import (
    SchoolNameAlreadyExistsError,
    SchoolAddressAlreadyExistsError,
    SchoolNotFoundError,
    UnableToDeleteSchoolError,
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
    return result.scalars().first()

async def get_by_address(db: AsyncSession, address: str) -> School | None:
    stmt = select(School).where(School.address == address)
    result = await db.execute(stmt)
    return result.scalars().first()

# Create School

async def create_school(db: AsyncSession, school: School) -> School:
    if await get_by_name(db, school.name) is not None:
        raise SchoolNameAlreadyExistsError()

    if await get_by_address(db, school.address) is not None:
        raise SchoolAddressAlreadyExistsError()

    db.add(school)

    try:
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise SchoolAddressAlreadyExistsError from exc

    await db.refresh(school)
    return school

# Delete School

async def delete_school(db: AsyncSession, id: uuid.UUID) -> None:
    school = get_by_id(db, id)
    if await school is None:
        raise SchoolNotFoundError()

    try:
        await db.delete(school)
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteSchoolError from exc