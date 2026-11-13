import uuid
from datetime import date, datetime
from pydantic import Field, BaseModel, ConfigDict

class OrderCreate(BaseModel):
    student_id: uuid.UUID
    product_id: uuid.UUID
    amount: int = Field(
        gt=0
    )
    day: date

class OrderUpdate(BaseModel):
    product_id: uuid.UUID
    amount: int = Field(
        gt=0
    )

class OrderResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    product_id: uuid.UUID
    amount: int = Field(
        gt=0
    )
    day: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)