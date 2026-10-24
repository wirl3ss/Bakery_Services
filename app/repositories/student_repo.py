import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.core.exceptions import (
    StudentAlreadyExistsError,
    StudentNotFoundError,
    UnableToDeleteStudentError,
    UnableToUpdateStudentError,
)
from app.models.student import Student

# Get Student

async def get_all_students(db: AsyncSession) -> Sequence[Student]:
    stmt = select(Student)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Student | None:
    return await db.get(Student, id)

async def get_by_user(db: AsyncSession, user_id: uuid.UUID) -> Student | None:
    stmt = select(Student).where(Student.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_by_school(db: AsyncSession, school_id: uuid.UUID) -> Sequence[Student]:
    stmt = select(Student).where(Student.school_id == school_id)
    result = await db.execute(stmt)
    return result.scalars().all()

# Create User

async def create_student(db: AsyncSession, student: Student) -> Student:
    student_exists = await get_by_user(db, student.user_id)
    if student_exists is not None:
        raise StudentAlreadyExistsError()

    db.add(student)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise StudentAlreadyExistsError from exc

    await db.refresh(student)
    return student

# Update Student

async def update_school_id(
    db: AsyncSession,
    id: uuid.UUID,
    school_id: uuid.UUID,
) -> Student:
    student = await get_by_id(db, id)
    if student is None:
        raise StudentNotFoundError()

    try:
        stmt = (
            update(Student)
            .where(Student.id == id)
            .values(school_id=school_id)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(student)

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateStudentError from exc

    return student

# Delete Student

async def delete_student(db: AsyncSession, id: uuid.UUID) -> None:
    student = await get_by_id(db, id)
    if student is None:
        raise StudentNotFoundError()

    try:
        await db.delete(student)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteStudentError() from exc