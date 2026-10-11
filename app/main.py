from fastapi import FastAPI

from app.core.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}