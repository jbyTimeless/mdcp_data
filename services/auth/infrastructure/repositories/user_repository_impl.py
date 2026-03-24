from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.auth.domain.entities.user import User
from services.auth.domain.repositories.user_repository import IUserRepository
from services.auth.infrastructure.models import SysUserModel

class UserRepositoryImpl(IUserRepository):
    """用户仓储实现类"""
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    def _to_entity(self, model: SysUserModel) -> User:
        """ORM模型转领域实体"""
        return User(
            id=model.id,
            user_id=model.user_id,
            account=model.account,
            username=model.username,
            access_key=model.access_key,
            secret_key=model.secret_key,
            role_code=model.role_code,
            email=model.email,
            status=model.status,
            create_time=model.create_time,
            update_time=model.update_time,
            is_deleted=model.is_deleted
        )
    
    def _to_model(self, entity: User) -> SysUserModel:
        """领域实体转ORM模型"""
        return SysUserModel(
            id=entity.id,
            user_id=entity.user_id,
            account=entity.account,
            username=entity.username,
            access_key=entity.access_key,
            secret_key=entity.secret_key,
            role_code=entity.role_code,
            email=entity.email,
            status=entity.status,
            create_time=entity.create_time,
            update_time=entity.update_time,
            is_deleted=entity.is_deleted
        )
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db_session.execute(
            select(SysUserModel).where(
                SysUserModel.email == email,
                SysUserModel.is_deleted == 0
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_account(self, account: str) -> Optional[User]:
        result = await self.db_session.execute(
            select(SysUserModel).where(
                SysUserModel.account == account,
                SysUserModel.is_deleted == 0
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self.db_session.add(model)
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return self._to_entity(model)
    
    async def update(self, user: User) -> User:
        result = await self.db_session.execute(
            select(SysUserModel).where(SysUserModel.id == user.id)
        )
        model = result.scalar_one()
        
        model.user_id = user.user_id
        model.account = user.account
        model.username = user.username
        model.access_key = user.access_key
        model.secret_key = user.secret_key
        model.role_code = user.role_code
        model.email = user.email
        model.status = user.status
        model.is_deleted = user.is_deleted
        
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return self._to_entity(model)