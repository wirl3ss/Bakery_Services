from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.exception_handlers import register_exceptions_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

register_exceptions_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}