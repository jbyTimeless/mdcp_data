from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime, func
from common.dependencies.database import Base

class SysUserModel(Base):
    """系统用户表ORM模型"""
    __tablename__ = "sys_user"
    __table_args__ = {'extend_existing': True, 'comment': '系统用户表'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="物理主键")
    user_id = Column(String(64), nullable=False, unique=True, comment="用户全局唯一ID")
    account = Column(String(64), nullable=False, unique=True, comment="用户登录账号")
    username = Column(String(32), nullable=False, comment="用户姓名")
    access_key = Column(String(128), nullable=False, unique=True, comment="API/JWT身份标识")
    secret_key = Column(String(256), nullable=False, comment="JWT签名密钥")
    role_code = Column(String(32), nullable=False, comment="角色编码")
    email = Column(String(64), nullable=True, comment="用户邮箱")
    status = Column(SmallInteger, nullable=False, default=1, comment="状态：1-启用 0-禁用")
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="软删除：0-未删除 1-已删除")
