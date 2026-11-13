from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_db

# Database Dependencies
DbSession = Annotated[AsyncSession, Depends(get_db)]

# Authentication dependecies
