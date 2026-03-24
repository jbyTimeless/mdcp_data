import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from config.settings import settings
from common.dependencies.redis_client import redis_client

class JWTUtil:
    """JWT工具类"""
    
    @staticmethod
    def generate_token(user_id: str, secret_key: str, expires_delta: Optional[timedelta] = None) -> str:
        """生成JWT令牌"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.jwt_expire_hours)
        
        to_encode = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, secret_key: str) -> Optional[Dict]:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.PyJWTError:
            return None
    
    @staticmethod
    async def save_token_to_redis(user_id: str, token: str, expire: int = settings.jwt_expire_hours * 3600):
        """将令牌存入Redis"""
        key = f"{settings.jwt_redis_prefix}:{user_id}"
        await redis_client.set(key, token, expire)
    
    @staticmethod
    async def get_token_from_redis(user_id: str) -> Optional[str]:
        """从Redis获取令牌"""
        key = f"{settings.jwt_redis_prefix}:{user_id}"
        return await redis_client.get(key)
    
    @staticmethod
    async def delete_token_from_redis(user_id: str):
        """从Redis删除令牌"""
        key = f"{settings.jwt_redis_prefix}:{user_id}"
        await redis_client.delete(key)

# 全局JWT工具实例
jwt_util = JWTUtil()