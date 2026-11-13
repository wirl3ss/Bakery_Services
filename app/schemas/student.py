import uuid
from pydantic import BaseModel, ConfigDict, Field

class StudentCreate(BaseModel):
    user_id: uuid.UUID
    school_id: uuid.UUID

class StudentUpdate(BaseModel):
    school_id: uuid.UUID

class StudentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    school_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)