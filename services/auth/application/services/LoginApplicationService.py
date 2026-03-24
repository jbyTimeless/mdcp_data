from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import settings
from services.auth.application.schemas.login import LoginRequest, LoginResponse, UserInfoDTO
from services.auth.domain.entities.user import User
from services.auth.domain.repositories.user_repository import IUserRepository
from services.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from services.auth.infrastructure.services.ldap_service import ldap_service
from common.utils.id_generator import generate_user_id, generate_access_key, generate_secret_key
from common.utils.jwt_util import jwt_util
from common.exceptions import BusinessException

class LoginApplicationService:
    """登录应用服务"""
    
    def __init__(self, db_session: AsyncSession):
        self.user_repository: IUserRepository = UserRepositoryImpl(db_session)
    
    async def login(self, request: LoginRequest) -> LoginResponse:
        """用户登录"""
        # 1. LDAP认证
        ldap_user = await ldap_service.authenticate(request.email, request.password)
        if not ldap_user:
            raise BusinessException(message="邮箱或密码错误", code=401)
        
        # 2. 查询用户是否存在
        user = await self.user_repository.get_by_email(request.email)
        
        if not user:
            # 3. 新用户，创建账号
            user = User(
                user_id=generate_user_id(),
                account=ldap_user['account'],
                username=ldap_user['username'],
                access_key=generate_access_key(),
                secret_key=generate_secret_key(),
                role_code="user",  # 默认普通用户角色
                email=ldap_user['email'],
                status=1
            )
            user = await self.user_repository.create(user)
        else:
            # 4. 已有用户，检查是否启用
            if not user.is_enabled():
                raise BusinessException(message="账号已被禁用", code=403)
            
            # 可选：每次登录重置凭证（根据需求决定是否开启）
            # user.reset_credentials(generate_access_key(), generate_secret_key())
            # user = await self.user_repository.update(user)
        
        # 5. 生成JWT令牌
        expires_delta = timedelta(hours=settings.jwt_expire_hours)
        access_token = jwt_util.generate_token(
            user_id=user.user_id,
            secret_key=user.secret_key,
            expires_delta=expires_delta
        )
        
        # 6. 令牌存入Redis
        await jwt_util.save_token_to_redis(
            user_id=user.user_id,
            token=access_token,
            expire=settings.jwt_expire_hours * 3600
        )
        
        # 7. 构造返回结果
        user_info = UserInfoDTO(
            user_id=user.user_id,
            account=user.account,
            username=user.username,
            email=user.email,
            role_code=user.role_code,
            access_key=user.access_key
        )
        
        return LoginResponse(
            access_token=access_token,
            expires_in=settings.jwt_expire_hours * 3600,
            user_info=user_info.model_dump()
        )