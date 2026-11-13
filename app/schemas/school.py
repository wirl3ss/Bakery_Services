import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SchoolCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
        description="School's name",
    )
    address: str = Field(
        min_length=1,
        max_length=255,
        description="School's address",
    )

class SchoolUpdate(BaseModel):
    name: str | None = Field(
        min_length=1,
        max_length=255,
        description="School's new name",
    )
    address: str | None = Field(
        min_length=1,
        max_length=255,
        description="School's new address",
    )

class SchoolResponse(BaseModel):
    id: uuid.UUID
    name: str = Field(
        min_length=1,
        max_length=255,
        description="School's name",
    )
    address: str = Field(
        min_length=1,
        max_length=255,
        description="School's address",
    )
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)