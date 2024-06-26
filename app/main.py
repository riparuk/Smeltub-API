from fastapi import FastAPI
from .routers import gas
from app.db import models
from app.db.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(gas.router)

@app.get("/")
async def root():
    return {"message": "Welcome Smeltub API"}
