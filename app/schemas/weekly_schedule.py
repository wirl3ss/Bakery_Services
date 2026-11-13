import uuid
from pydantic import Field, BaseModel, ConfigDict

class WeeklyScheduleCreate(BaseModel):
    shop_id: uuid.UUID
    day_of_week: int = Field(
        ge=0,
        le=6,
    )
    is_open: bool

class WeeklyScheduleUpdate(BaseModel):
    is_open: bool

class WeeklyScheduleResponse(BaseModel):
    id: uuid.UUID
    shop_id: uuid.UUID
    day_of_week: int = Field(
        ge=0,
        le=6,
    )
    is_open: bool

    model_config = ConfigDict(from_attributes=True)