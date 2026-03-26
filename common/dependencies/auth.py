from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from common.dependencies.database import get_db
from common.utils.jwt_util import jwt_util
from common.dependencies.redis_client import redis_client
from services.dataset.infrastructure.models import SysUser
from common.exceptions import BusinessException

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> SysUser:
    """
    验证JWT令牌并获取当前用户
    1. 从请求头提取Bearer令牌
    2. 解析令牌获取用户ID
    3. 查询用户信息获取专属密钥
    4. 使用用户专属密钥验证令牌签名
    5. 检查令牌是否存在于Redis（未被注销）
    6. 返回用户对象
    """
    # 从请求头提取令牌
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise BusinessException(message="未提供认证令牌", code=401)
    
    token = authorization[7:]  # 去掉"Bearer "前缀
    
    try:
        # 第一步：无验证解析令牌获取用户ID
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id: str = payload.get("sub")
        if user_id is None:
            raise BusinessException(message="令牌无效", code=401)
    except jwt.PyJWTError:
        raise BusinessException(message="令牌解析失败", code=401)
    
    # 第二步：查询用户信息
    stmt = select(SysUser).where(SysUser.user_id == user_id, SysUser.is_deleted == 0)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise BusinessException(message="用户不存在", code=401)
    
    # 第三步：使用用户专属密钥验证令牌签名
    try:
        payload = jwt_util.verify_token(token, user.secret_key)
        if payload is None:
            raise BusinessException(message="令牌签名验证失败", code=401)
        # 验证令牌中的用户ID与查询到的用户一致
        if payload.get("sub") != user_id:
            raise BusinessException(message="令牌归属错误", code=401)
    except jwt.PyJWTError:
        raise BusinessException(message="令牌验证失败", code=401)
    
    # 第四步：检查令牌是否存在于Redis（未被注销）
    redis_token = await redis_client.get(f"mdcp:user:login:{user_id}")
    if redis_token is None or redis_token != token:
        raise BusinessException(message="令牌已失效或已注销", code=401)
    
    # 第五步：检查用户状态
    if user.status != 1:
        raise BusinessException(message="用户已被禁用", code=403)
    
    # 第六步：刷新令牌有效期（续期30分钟）
    await redis_client.expire(f"mdcp:user:login:{user_id}", 1800)
    
    return user
