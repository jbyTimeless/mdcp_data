from sqlalchemy import Column, Integer, String, BigInteger, DateTime, text
from sqlalchemy.sql import func
from common.dependencies.database import Base

class SysUser(Base):
    __tablename__ = 'sys_user'
    __table_args__ = {'comment': '系统用户表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='【物理主键】数据库自增ID，仅内部使用')
    user_id = Column(BigInteger, nullable=False, unique=True, comment='【业务主键】用户唯一ID（自定义雪花ID）')
    account = Column(String(64), nullable=False, unique=True, comment='用户登录账号')
    username = Column(String(32), nullable=False, comment='用户姓名')
    access_key = Column(String(128), nullable=False, unique=True, comment='AK用户身份凭证')
    secret_key = Column(String(256), nullable=False, comment='SK密钥凭证')
    role_code = Column(String(32), nullable=False, index=True, comment='角色编码')
    email = Column(String(64), nullable=True, comment='用户邮箱（审批/通知用）')
    status = Column(Integer, nullable=False, server_default=text("1"), comment='状态：1-启用 0-禁用')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')


class SysRole(Base):
    __tablename__ = 'sys_role'
    __table_args__ = {'comment': '系统角色表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='【物理主键】数据库自增ID，仅内部使用')
    role_id = Column(BigInteger, nullable=False, unique=True, comment='【业务主键】角色唯一ID（自定义雪花ID）')
    role_name = Column(String(32), nullable=False, comment='角色名称')
    role_code = Column(String(32), nullable=False, unique=True, comment='角色编码')
    role_desc = Column(String(256), nullable=True, comment='角色职责描述')
    status = Column(Integer, nullable=False, server_default=text("1"), comment='状态：1-启用 0-禁用')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')


class DataProject(Base):
    __tablename__ = 'data_project'
    __table_args__ = {'comment': '数据项目表（数据集顶层管理单元）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='【物理主键】数据库自增ID，仅内部使用')
    project_id = Column(String(64), nullable=False, unique=True, comment='【业务主键】项目唯一ID（自定义规则：雪花ID/UUID/业务编码）')
    project_name = Column(String(32), nullable=False, unique=True, comment='项目名称（全局唯一）')
    project_en_name = Column(String(32), nullable=False, unique=True, comment='项目英文名称（英文开头，字母/数字/中划线/下划线）')
    is_compliance_open = Column(Integer, nullable=False, server_default=text("0"), comment='是否开启合规：1-开启 0-关闭')
    is_share_storage = Column(Integer, nullable=False, server_default=text("0"), comment='是否共享存储空间：1-开启 0-关闭')
    storage_type = Column(String(32), nullable=False, server_default=text("'baidu_bos'"), comment='存储类型')
    storage_endpoint = Column(String(128), nullable=False, comment='存储端点')
    bucket_name = Column(String(64), nullable=False, comment='bucket名称')
    storage_dir = Column(String(256), nullable=False, comment='存储目录')
    write_ak = Column(String(128), nullable=True, comment='写入账号AK')
    write_sk = Column(String(256), nullable=True, comment='写入账号SK')
    read_ak = Column(String(128), nullable=True, comment='读取账号AK')
    read_sk = Column(String(256), nullable=True, comment='读取账号SK')
    create_user_id = Column(BigInteger, nullable=False, index=True, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')
