import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.core.exceptions import (
    ShopAlreadyExistsError,
    ShopNotFoundError,
    UnableToDeleteShopError,
)
from app.models.shop import Shop

# Get Shop

async def get_all_shops(db: AsyncSession) -> Sequence[Shop]:
    stmt = select(Shop)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Shop | None:
    return await db.get(Shop, id)

async def get_by_user(db: AsyncSession, user_id: uuid.UUID) -> Shop | None:
    stmt = select(Shop).where(Shop.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Create Shop

async def create_shop(
    db: AsyncSession,
    shop: Shop,
) -> Shop:
    shop_exists = await get_by_user(db, shop.user_id)
    if shop_exists is not None:
        raise ShopAlreadyExistsError()

    db.add(shop)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ShopAlreadyExistsError from exc

    await db.refresh(shop)
    return shop

# Update Shop

# Delete Shop

async def delete_shop(
    db: AsyncSession,
    id: uuid.UUID,
) -> None:
    shop = await get_by_id(db, id)
    if shop is None:
        raise ShopNotFoundError()

    try:
        await db.delete(shop)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteShopError from exc