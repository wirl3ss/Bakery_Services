import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    shop_id: uuid.UUID
    name: str = Field(
        min_length=1,
        max_length=255,
    )
    price: float = Field(
        gt=0,
    )

class ProductUpdate(BaseModel):
    name: str | None = Field(
        min_length=1,
        max_length=255,
    )
    price: float | None = Field(
        gt=0,
    )

class ProductResponse(BaseModel):
    id: uuid.UUID
    shop_id: uuid.UUID
    name: str = Field(
        min_length=1,
        max_length=255,
    )
    price: float = Field(
        gt=0,
    )
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)