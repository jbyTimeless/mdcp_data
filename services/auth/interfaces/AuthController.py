from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.dependencies.database import get_db
from common.schemas.response import success, error
from services.auth.application.schemas.login import LoginRequest, LoginResponse
from services.auth.application.services.LoginApplicationService import LoginApplicationService

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login", summary="用户登录")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    用户登录接口
    - 基于LDAP企业邮箱认证
    - 新用户自动创建账号
    - 登录成功返回JWT令牌
    """
    try:
        login_service = LoginApplicationService(db)
        result = await login_service.login(request)
        return success(data=result.model_dump())
    except Exception as e:
        return error(msg=str(e), code=getattr(e, 'code', 500))
