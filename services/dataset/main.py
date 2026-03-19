from fastapi import FastAPI
from services.dataset.interfaces.router import router
from common.dependencies.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup for simplicity in this demo
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Dataset Service", version="1.0.0", lifespan=lifespan)

app.include_router(router, prefix="/api/v1/datasets", tags=["datasets"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Dataset Service"}
