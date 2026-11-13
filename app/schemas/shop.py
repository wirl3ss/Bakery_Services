import uuid
from pydantic import BaseModel, ConfigDict, Field

class ShopCreate(BaseModel):
    user_id: uuid.UUID

class ShopResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)