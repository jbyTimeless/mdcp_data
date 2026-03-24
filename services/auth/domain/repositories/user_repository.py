from abc import ABC, abstractmethod
from typing import Optional
from services.auth.domain.entities.user import User

class IUserRepository(ABC):
    """用户仓储接口"""
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查询用户"""
        pass
    
    @abstractmethod
    async def get_by_account(self, account: str) -> Optional[User]:
        """根据账号查询用户"""
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """创建用户"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """更新用户信息"""
        pass