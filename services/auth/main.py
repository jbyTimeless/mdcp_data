from fastapi import FastAPI
from services.auth.interfaces.AuthController import router as auth_router
from common.dependencies.database import engine, Base
from common.dependencies.redis_client import redis_client
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # 连接Redis
    await redis_client.connect()
    yield
    # 断开Redis连接
    await redis_client.disconnect()

app = FastAPI(title="Auth Service", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Auth Service"}