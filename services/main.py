import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from common.dependencies.database import engine, Base
from common.dependencies.redis_client import redis_client
from common.exceptions import BusinessException
from common.schemas.response import error
from services.auth.interfaces.AuthController import router as auth_router
from services.dataset.interfaces.Controller import router as dataset_router
from services.dataset.interfaces.ProjectController import router as project_router
from services.dataset.interfaces.DatasetController import router as dataset_detail_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化所有数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # 连接Redis
    await redis_client.connect()
    yield
    # 断开Redis连接
    await redis_client.disconnect()

app = FastAPI(
    title="MDCP Data Platform", 
    version="1.0.0", 
    lifespan=lifespan,
    # 配置国内swagger资源CDN，解决加载超时问题
    swagger_js_url="https://cdn.staticfile.org/swagger-ui/5.11.0/swagger-ui-bundle.js",
    swagger_css_url="https://cdn.staticfile.org/swagger-ui/5.11.0/swagger-ui.css",
    swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
)

# 注册路由
app.include_router(auth_router, prefix="/api/v1", tags=["认证"])
app.include_router(dataset_router, prefix="/api/v1/datasets", tags=["数据集"])
app.include_router(project_router, prefix="/api/v1/projects", tags=["项目"])
app.include_router(dataset_detail_router, prefix="/api/v1/dataset", tags=["数据集详情"])

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """全局业务异常处理器"""
    return JSONResponse(
        status_code=200,
        content=error(msg=exc.message, code=exc.code).model_dump()
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to MDCP Data Platform"}
