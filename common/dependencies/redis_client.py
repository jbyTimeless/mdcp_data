import redis.asyncio as redis
from config.settings import settings
from typing import Optional

class RedisClient:
    """Redis客户端"""
    
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        """连接Redis"""
        self.redis = await redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password if settings.redis_password else None,
            decode_responses=True
        )
    
    async def disconnect(self):
        """断开连接"""
        if self.redis:
            await self.redis.close()
    
    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """设置缓存"""
        if expire:
            await self.redis.setex(key, expire, value)
        else:
            await self.redis.set(key, value)
    
    async def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        return await self.redis.get(key)
    
    async def delete(self, key: str):
        """删除缓存"""
        await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """检查key是否存在"""
        return await self.redis.exists(key) > 0

# 全局Redis客户端实例
redis_client = RedisClient()