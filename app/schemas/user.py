import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.user import Role

class UserCreate(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=20,
        description="Name of the user",
    )
    password: str = Field(
        min_length=1,
        max_length=255,
        description="User's password to acces the account",
    )
    email: str = Field(
        min_length=1,
        max_length=255,
        description="User's email",
    )

class UserUpdate(BaseModel):
    username: str | None = Field(
        min_length=1,
        max_length=20,
        description="New name of the user",
    )
    password: str | None = Field(
        min_length=1,
        max_length=255,
        description="User's new password",
    )
    email: str | None = Field(
        min_length=1,
        max_length=255,
        description="User's new email",
    )

class UserUpdateRole(BaseModel):
    role: Role = Field(
        description="New Role of the User",
    )

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str = Field(
        min_length=1,
        max_length=20,
        description="Name of the user",
    )
    email: str = Field(
        min_length=1,
        max_length=255,
        description="User's new email",
    )
    role: Role = Field(
        description="User's role and permissions",
    )
    created_at:datetime = Field(
        description="Timestamp of the creation of the user",
    )

    model_config = ConfigDict(from_attributes=True)