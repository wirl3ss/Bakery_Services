import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from collections.abc import Sequence
from sqlalchemy.exc import IntegrityError

from app.services.exceptions import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UnableToUpdateUserError,
    UnableToDeleteUserError,
    )
from app.models.user import User, Role

# Get User

async def get_all_users(db: AsyncSession) -> Sequence[User]:
    stmt = select(User)
    result = await db.execute(stmt)
    return  result.scalars().all()

async def get_by_id(db: AsyncSession, id:uuid.UUID) -> User | None:
    return await db.get(User, id)

async def get_by_role(db: AsyncSession, role: Role) -> Sequence[User]:
    stmt = select(User).where(User.role == role)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_username(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

# Create User

async def create_user(db: AsyncSession, user: User) -> User:
    if await get_by_username(db, user.username) is not None:
        raise UsernameAlreadyExistsError()

    if await get_by_email(db, user.email) is not None:
        raise EmailAlreadyExistsError()

    db.add(user)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise UserAlreadyExistsError from exc

    await db.refresh(user)
    return user

# Update User

async def update_user(
    db: AsyncSession,
    id: uuid.UUID,
    data: dict,
) -> User | None:
    user = await get_by_id(db, id)

    if user is None:
        raise UserNotFoundError()

    try:
        stmt = (
            update(User)
            .where(User.id == id)
            .values(**data)
        )

        await db.execute(stmt)
        await db.commit()
        await db.refresh(user)
    except IntegrityError as exc:
        await db.rollback()
        raise UnableToUpdateUserError() from exc

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateUserError() from exc

    return user

async def update_role(
        db: AsyncSession,
        id: uuid.UUID,
        role: Role,
) -> User | None:
    user = await get_by_id(db, id)

    if user is None:
        raise UserNotFoundError()

    try:
        stmt = (
            update(User)
            .where(User.id == id)
            .values(role=role)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(user)

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateUserError() from exc

    return user

async def delete_user(db: AsyncSession, id: uuid.UUID) -> None:
    user = await get_by_id(db, id)
    if user is None:
        raise UserNotFoundError()

    try:
        await db.delete(user)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteUserError() from exc