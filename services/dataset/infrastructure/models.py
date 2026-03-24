from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text, JSON, text
from sqlalchemy.sql import func
from common.dependencies.database import Base

class SysUser(Base):
    __tablename__ = 'sys_user'
    __table_args__ = {'comment': '系统用户表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='【物理主键】数据库自增ID，仅内部使用')
    user_id = Column(String(64), nullable=False, unique=True, comment='【业务主键】用户唯一ID（自定义雪花ID）')
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
    create_user_id = Column(String(64), nullable=False, index=True, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')

class DatasetInfo(Base):
    __tablename__ = 'dataset_info'
    __table_args__ = {'comment': '数据集主表（数据集核心元数据表）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    dataset_id = Column(String(64), nullable=False, comment='数据集业务关联ID')
    project_id = Column(String(64), nullable=False, index=True, comment='所属项目ID')
    dataset_name = Column(String(64), nullable=False, comment='数据集名称（项目内唯一）')
    dataset_en_name = Column(String(64), nullable=False, comment='数据集英文名称')
    dataset_path = Column(String(256), nullable=False, comment='数据集存储路径')
    dataset_type = Column(String(32), nullable=False, comment='数据集类型（标注数据集/暂存数据集等）')
    media_type = Column(String(32), nullable=False, comment='数据媒体形式（图片/点云/视频等）')
    application_scenario = Column(String(32), nullable=True, comment='应用场景（研发训练/仿真测试等）')
    is_data_update_open = Column(Integer, nullable=False, server_default=text("0"), comment='是否开启数据更新：1-开启 0-关闭')
    related_dataset_id = Column(String(64), nullable=True, comment='关联数据集ID')
    stat_level1_id = Column(String(64), nullable=True, comment='关联统计树一级分类ID')
    stat_level2_id = Column(String(64), nullable=True, comment='关联统计树二级分类ID')
    stat_level3_id = Column(String(64), nullable=True, comment='关联统计树三级分类ID')
    tags = Column(String(256), nullable=True, comment='数据集标签，逗号分隔')
    description = Column(Text, nullable=True, comment='数据集简介/概览描述')
    schema_config = Column(JSON, nullable=True, comment='数据结构Schema配置')
    column_config = Column(JSON, nullable=True, comment='数据列配置')
    visual_config = Column(JSON, nullable=True, comment='可视化信息配置')
    create_user_id = Column(String(64), nullable=False, index=True, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')


class DataStatConfig(Base):
    __tablename__ = 'data_stat_config'
    __table_args__ = {'comment': '数据统计配置表（统计树管理）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    stat_id = Column(String(64), nullable=False, comment='统计配置业务关联ID')
    parent_stat_id = Column(String(64), nullable=False, server_default=text("0"), comment='父统计ID，顶层为0')
    stat_name = Column(String(64), nullable=False, comment='统计分类名称')
    level = Column(Integer, nullable=False, comment='层级：1-一级 2-二级 3-三级')
    summary_type = Column(String(32), nullable=False, server_default=text("'SUM'"), comment='汇总类型：SUM/COUNT等')
    description = Column(String(512), nullable=True, comment='备注描述')
    create_user_id = Column(String(64), nullable=False, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')


class StatDatasetRelation(Base):
    __tablename__ = 'stat_dataset_relation'
    __table_args__ = {'comment': '统计-数据集关联表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    relation_id = Column(String(64), nullable=False, comment='关联业务关联ID')
    stat_id = Column(String(64), nullable=False, index=True, comment='三级统计分类ID')
    project_id = Column(String(64), nullable=False, comment='所属项目ID')
    dataset_id = Column(String(64), nullable=False, index=True, comment='数据集ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')


class DatasetPermission(Base):
    __tablename__ = 'dataset_permission'
    __table_args__ = {'comment': '数据集权限表（细粒度权限控制）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    permission_id = Column(String(64), nullable=False, comment='权限业务关联ID')
    resource_type = Column(String(32), nullable=False, index=True, comment='资源类型：project-项目 dataset-数据集 subset-子集 view-视图')
    resource_id = Column(String(64), nullable=False, index=True, comment='资源ID')
    user_id = Column(String(64), nullable=False, index=True, comment='被授权用户ID')
    permission_type = Column(String(32), nullable=False, comment='权限类型：view-查看 edit-编辑 manage-管理')
    grant_user_id = Column(String(64), nullable=False, comment='授权人用户ID')
    grant_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='授权时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    status = Column(Integer, nullable=False, server_default=text("1"), comment='状态：1-生效 0-失效')


class DataSubset(Base):
    __tablename__ = 'data_subset'
    __table_args__ = {'comment': '数据子集表（数据集物理树形分层）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    subset_id = Column(String(64), nullable=False, comment='子集业务关联ID')
    dataset_id = Column(String(64), nullable=False, index=True, comment='所属数据集ID')
    parent_subset_id = Column(String(64), nullable=False, server_default=text("0"), comment='父子集ID，顶层子集为0')
    subset_name = Column(String(50), nullable=False, comment='子集名称（数据集内唯一）')
    subset_en_name = Column(String(50), nullable=False, comment='子集英文名称')
    subset_path = Column(String(256), nullable=False, comment='子集存储路径')
    level = Column(Integer, nullable=False, comment='层级（1-5，文档规定最深5层）')
    description = Column(String(512), nullable=True, comment='子集描述')
    create_user_id = Column(String(64), nullable=False, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')


class DatasetView(Base):
    __tablename__ = 'dataset_view'
    __table_args__ = {'comment': '数据集视图表（数据集逻辑筛选视图）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    view_id = Column(String(64), nullable=False, comment='视图业务关联ID')
    dataset_id = Column(String(64), nullable=False, index=True, comment='所属数据集ID')
    view_name = Column(String(64), nullable=False, comment='视图名称（数据集内唯一）')
    view_en_name = Column(String(64), nullable=False, comment='视图英文名称')
    filter_condition = Column(Text, nullable=True, comment='视图筛选条件SQL/DSL')
    description = Column(String(512), nullable=True, comment='视图描述')
    create_user_id = Column(String(64), nullable=False, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')
    is_deleted = Column(Integer, nullable=False, server_default=text("0"), comment='软删除：0-未删除 1-已删除')


class LabelType(Base):
    __tablename__ = 'label_type'
    __table_args__ = {'comment': '标注类型配置表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    type_id = Column(BigInteger, nullable=False, comment='标注类型业务关联ID')
    label_category = Column(String(32), nullable=False, index=True, comment='标注分类（2D/3D等）')
    type_name = Column(String(32), nullable=False, unique=True, comment='标注类型名称')
    type_en_name = Column(String(32), nullable=False, comment='标注类型英文名称')
    related_channel_code = Column(String(64), nullable=False, unique=True, comment='关联标注平台通道号/项目号')
    description = Column(String(512), nullable=True, comment='描述')
    status = Column(Integer, nullable=False, server_default=text("1"), comment='状态：1-启用 0-禁用')
    create_user_id = Column(String(64), nullable=False, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')


class LabelDeliveryTask(Base):
    __tablename__ = 'label_delivery_task'
    __table_args__ = {'comment': '数据送标任务表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    task_id = Column(String(64), nullable=False, comment='送标任务业务关联ID')
    task_name = Column(String(128), nullable=False, comment='标注任务名称')
    label_category = Column(String(32), nullable=False, comment='标注分类')
    label_type_id = Column(BigInteger, nullable=False, index=True, comment='标注类型ID')
    related_channel_code = Column(String(64), nullable=False, comment='关联标注平台通道号')
    source_dataset_id = Column(String(64), nullable=False, index=True, comment='源数据集ID')
    source_subset_id = Column(String(64), nullable=True, comment='源数据子集ID')
    data_count = Column(BigInteger, nullable=True, server_default=text("0"), comment='标注数据量')
    delivery_dataset_id = Column(String(64), nullable=False, comment='标注结果交付数据集ID')
    remark = Column(Text, nullable=True, comment='备注信息')
    task_status = Column(String(32), nullable=False, server_default=text("'pending'"), index=True, comment='任务状态：pending-待处理 forwarding-待转发 labeling-标注中 finished-已标注 failed-失败')
    label_platform_batch_no = Column(String(64), nullable=True, index=True, comment='标注平台批次号')
    create_user_id = Column(String(64), nullable=False, comment='创建人用户ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')


class ViewSubsetRelation(Base):
    __tablename__ = 'view_subset_relation'
    __table_args__ = {'comment': '视图-子集关联表（多对多）'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='物理主键ID')
    relation_id = Column(String(64), nullable=False, comment='关联业务关联ID')
    view_id = Column(String(64), nullable=False, index=True, comment='视图ID')
    subset_id = Column(String(64), nullable=False, index=True, comment='数据子集ID')
    create_time = Column(DateTime, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
