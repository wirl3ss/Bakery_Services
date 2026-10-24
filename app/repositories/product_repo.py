import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from collections.abc import Sequence

from app.core.exceptions import (
    ProductAlreadyExistsError,
    ProductNotFoundError,
    UnableToUpdateProductError,
    UnableToDeleteProductError,
)
from app.models.product import Product

# Get Product

async def get_all_products(db: AsyncSession) -> Sequence[Product]:
    stmt = select(Product)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Product | None:
    return await db.get(Product, id)

async def get_by_shop(db: AsyncSession, shop_id: uuid.UUID) -> Sequence[Product]:
    stmt = select(Product).where(Product.shop_id == shop_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_by_name(db: AsyncSession, name: str) -> Product | None:
    stmt = select(Product).where(Product.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Create Product

async def create_product(
    db: AsyncSession,
    product: Product,
) -> Product:
    product_exists = await get_by_name(db, product.name)
    if product_exists is not None:
        raise ProductAlreadyExistsError()

    db.add(product)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ProductAlreadyExistsError from exc

    await db.refresh(product)
    return product

# Update Product

async def update_product(
    db: AsyncSession,
    id: uuid.UUID,
    data: dict,
) -> Product:
    product = await get_by_id(db, id)
    if product is None:
        raise ProductNotFoundError()

    try:
        stmt = (
            update(Product)
            .where(Product.id == id)
            .values(**data)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(product)

    except Exception as exc:
        await db.rollback()
        raise UnableToUpdateProductError from exc

    return product

# Delete Product

async def delete_product(db: AsyncSession, id: uuid.UUID) -> None:
    product = await get_by_id(db, id)
    if product is None:
        raise ProductNotFoundError()

    try:
        await db.delete(product)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise UnableToDeleteProductError from exc