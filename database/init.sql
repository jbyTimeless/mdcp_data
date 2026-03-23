-- mdcp_data.data_project definition

CREATE TABLE `data_project` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '【物理主键】数据库自增ID，仅内部使用',
  `project_id` varchar(64) NOT NULL COMMENT '【业务主键】项目唯一ID（自定义规则：雪花ID/UUID/业务编码）',
  `project_name` varchar(32) NOT NULL COMMENT '项目名称（全局唯一）',
  `project_en_name` varchar(32) NOT NULL COMMENT '项目英文名称（英文开头，字母/数字/中划线/下划线）',
  `is_compliance_open` tinyint NOT NULL DEFAULT '0' COMMENT '是否开启合规：1-开启 0-关闭',
  `is_share_storage` tinyint NOT NULL DEFAULT '0' COMMENT '是否共享存储空间：1-开启 0-关闭',
  `storage_type` varchar(32) NOT NULL DEFAULT 'baidu_bos' COMMENT '存储类型',
  `storage_endpoint` varchar(128) NOT NULL COMMENT '存储端点',
  `bucket_name` varchar(64) NOT NULL COMMENT 'bucket名称',
  `storage_dir` varchar(256) NOT NULL COMMENT '存储目录',
  `write_ak` varchar(128) DEFAULT NULL COMMENT '写入账号AK',
  `write_sk` varchar(256) DEFAULT NULL COMMENT '写入账号SK',
  `read_ak` varchar(128) DEFAULT NULL COMMENT '读取账号AK',
  `read_sk` varchar(256) DEFAULT NULL COMMENT '读取账号SK',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_project_id` (`project_id`),
  UNIQUE KEY `uk_project_name` (`project_name`),
  UNIQUE KEY `uk_project_en_name` (`project_en_name`),
  KEY `idx_create_user` (`create_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据项目表（数据集顶层管理单元）';


-- mdcp_data.data_stat_config definition

CREATE TABLE `data_stat_config` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `stat_id` bigint NOT NULL COMMENT '统计配置业务关联ID',
  `parent_stat_id` bigint NOT NULL DEFAULT '0' COMMENT '父统计ID，顶层为0',
  `stat_name` varchar(64) NOT NULL COMMENT '统计分类名称',
  `level` tinyint NOT NULL COMMENT '层级：1-一级 2-二级 3-三级',
  `summary_type` varchar(32) NOT NULL DEFAULT 'SUM' COMMENT '汇总类型：SUM/COUNT等',
  `description` varchar(512) DEFAULT NULL COMMENT '备注描述',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_parent_stat_name` (`parent_stat_id`,`stat_name`),
  KEY `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据统计配置表（统计树管理）';


-- mdcp_data.data_subset definition

CREATE TABLE `data_subset` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `subset_id` bigint NOT NULL COMMENT '子集业务关联ID',
  `dataset_id` bigint NOT NULL COMMENT '所属数据集ID',
  `parent_subset_id` bigint NOT NULL DEFAULT '0' COMMENT '父子集ID，顶层子集为0',
  `subset_name` varchar(50) NOT NULL COMMENT '子集名称（数据集内唯一）',
  `subset_en_name` varchar(50) NOT NULL COMMENT '子集英文名称',
  `subset_path` varchar(256) NOT NULL COMMENT '子集存储路径',
  `level` tinyint NOT NULL COMMENT '层级（1-5，文档规定最深5层）',
  `description` varchar(512) DEFAULT NULL COMMENT '子集描述',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_dataset_subset_name` (`dataset_id`,`parent_subset_id`,`subset_name`),
  KEY `idx_dataset_id` (`dataset_id`),
  KEY `idx_parent_subset` (`parent_subset_id`),
  KEY `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据子集表（数据集物理树形分层）';


-- mdcp_data.dataset_info definition

CREATE TABLE `dataset_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `dataset_id` bigint NOT NULL COMMENT '数据集业务关联ID',
  `project_id` bigint NOT NULL COMMENT '所属项目ID',
  `dataset_name` varchar(64) NOT NULL COMMENT '数据集名称（项目内唯一）',
  `dataset_en_name` varchar(64) NOT NULL COMMENT '数据集英文名称',
  `dataset_path` varchar(256) NOT NULL COMMENT '数据集存储路径',
  `dataset_type` varchar(32) NOT NULL COMMENT '数据集类型（标注数据集/暂存数据集等）',
  `media_type` varchar(32) NOT NULL COMMENT '数据媒体形式（图片/点云/视频等）',
  `application_scenario` varchar(32) DEFAULT NULL COMMENT '应用场景（研发训练/仿真测试等）',
  `is_data_update_open` tinyint NOT NULL DEFAULT '0' COMMENT '是否开启数据更新：1-开启 0-关闭',
  `related_dataset_id` bigint DEFAULT NULL COMMENT '关联数据集ID',
  `stat_level1_id` bigint DEFAULT NULL COMMENT '关联统计树一级分类ID',
  `stat_level2_id` bigint DEFAULT NULL COMMENT '关联统计树二级分类ID',
  `stat_level3_id` bigint DEFAULT NULL COMMENT '关联统计树三级分类ID',
  `tags` varchar(256) DEFAULT NULL COMMENT '数据集标签，逗号分隔',
  `description` text COMMENT '数据集简介/概览描述',
  `schema_config` json DEFAULT NULL COMMENT '数据结构Schema配置（对应文档2.3.2.6.1）',
  `column_config` json DEFAULT NULL COMMENT '数据列配置（对应文档2.3.2.6.2）',
  `visual_config` json DEFAULT NULL COMMENT '可视化信息配置（对应文档2.3.2.7）',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_project_dataset_name` (`project_id`,`dataset_name`),
  UNIQUE KEY `uk_project_dataset_en_name` (`project_id`,`dataset_en_name`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_create_user` (`create_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集主表（数据集核心元数据表）';


-- mdcp_data.dataset_permission definition

CREATE TABLE `dataset_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `permission_id` bigint NOT NULL COMMENT '权限业务关联ID',
  `resource_type` varchar(32) NOT NULL COMMENT '资源类型：project-项目 dataset-数据集 subset-子集 view-视图',
  `resource_id` bigint NOT NULL COMMENT '资源ID（对应项目/数据集/子集/视图主键）',
  `user_id` bigint NOT NULL COMMENT '被授权用户ID',
  `permission_type` varchar(32) NOT NULL COMMENT '权限类型：view-查看 edit-编辑 manage-管理',
  `grant_user_id` bigint NOT NULL COMMENT '授权人用户ID',
  `grant_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1-生效 0-失效',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_resource_user` (`resource_type`,`resource_id`,`user_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_resource` (`resource_type`,`resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集权限表（细粒度权限控制）';


-- mdcp_data.dataset_view definition

CREATE TABLE `dataset_view` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `view_id` bigint NOT NULL COMMENT '视图业务关联ID',
  `dataset_id` bigint NOT NULL COMMENT '所属数据集ID',
  `view_name` varchar(64) NOT NULL COMMENT '视图名称（数据集内唯一）',
  `view_en_name` varchar(64) NOT NULL COMMENT '视图英文名称',
  `filter_condition` text COMMENT '视图筛选条件SQL/DSL',
  `description` varchar(512) DEFAULT NULL COMMENT '视图描述',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_dataset_view_name` (`dataset_id`,`view_name`),
  KEY `idx_dataset_id` (`dataset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集视图表（数据集逻辑筛选视图）';


-- mdcp_data.label_delivery_task definition

CREATE TABLE `label_delivery_task` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `task_id` bigint NOT NULL COMMENT '送标任务业务关联ID',
  `task_name` varchar(128) NOT NULL COMMENT '标注任务名称',
  `label_category` varchar(32) NOT NULL COMMENT '标注分类',
  `label_type_id` bigint NOT NULL COMMENT '标注类型ID',
  `related_channel_code` varchar(64) NOT NULL COMMENT '关联标注平台通道号',
  `source_dataset_id` bigint NOT NULL COMMENT '源数据集ID',
  `source_subset_id` bigint DEFAULT NULL COMMENT '源数据子集ID',
  `data_count` bigint DEFAULT '0' COMMENT '标注数据量',
  `delivery_dataset_id` bigint NOT NULL COMMENT '标注结果交付数据集ID',
  `remark` text COMMENT '备注信息',
  `task_status` varchar(32) NOT NULL DEFAULT 'pending' COMMENT '任务状态：pending-待处理 forwarding-待转发 labeling-标注中 finished-已标注 failed-失败',
  `label_platform_batch_no` varchar(64) DEFAULT NULL COMMENT '标注平台批次号',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  KEY `idx_label_type` (`label_type_id`),
  KEY `idx_source_dataset` (`source_dataset_id`),
  KEY `idx_task_status` (`task_status`),
  KEY `idx_batch_no` (`label_platform_batch_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据送标任务表';


-- mdcp_data.label_type definition

CREATE TABLE `label_type` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `type_id` bigint NOT NULL COMMENT '标注类型业务关联ID',
  `label_category` varchar(32) NOT NULL COMMENT '标注分类（2D/3D等）',
  `type_name` varchar(32) NOT NULL COMMENT '标注类型名称',
  `type_en_name` varchar(32) NOT NULL COMMENT '标注类型英文名称',
  `related_channel_code` varchar(64) NOT NULL COMMENT '关联标注平台通道号/项目号',
  `description` varchar(512) DEFAULT NULL COMMENT '描述',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1-启用 0-禁用',
  `create_user_id` bigint NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_type_name` (`type_name`),
  UNIQUE KEY `uk_channel_code` (`related_channel_code`),
  KEY `idx_label_category` (`label_category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='标注类型配置表';


-- mdcp_data.stat_dataset_relation definition

CREATE TABLE `stat_dataset_relation` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `relation_id` bigint NOT NULL COMMENT '关联业务关联ID',
  `stat_id` bigint NOT NULL COMMENT '三级统计分类ID',
  `project_id` bigint NOT NULL COMMENT '所属项目ID',
  `dataset_id` bigint NOT NULL COMMENT '数据集ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_stat_dataset` (`stat_id`,`dataset_id`),
  KEY `idx_stat_id` (`stat_id`),
  KEY `idx_dataset_id` (`dataset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='统计-数据集关联表';


-- mdcp_data.sys_role definition

CREATE TABLE `sys_role` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '【物理主键】数据库自增ID，仅内部使用',
  `role_id` bigint NOT NULL COMMENT '【业务主键】角色唯一ID（自定义雪花ID）',
  `role_name` varchar(32) NOT NULL COMMENT '角色名称',
  `role_code` varchar(32) NOT NULL COMMENT '角色编码',
  `role_desc` varchar(256) DEFAULT NULL COMMENT '角色职责描述',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1-启用 0-禁用',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_id` (`role_id`),
  UNIQUE KEY `uk_role_code` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统角色表';


-- mdcp_data.sys_user definition

CREATE TABLE `sys_user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '【物理主键】数据库自增ID，仅内部使用',
  `user_id` bigint NOT NULL COMMENT '【业务主键】用户唯一ID（自定义雪花ID）',
  `account` varchar(64) NOT NULL COMMENT '用户登录账号',
  `username` varchar(32) NOT NULL COMMENT '用户姓名',
  `access_key` varchar(128) NOT NULL COMMENT 'AK用户身份凭证',
  `secret_key` varchar(256) NOT NULL COMMENT 'SK密钥凭证',
  `role_code` varchar(32) NOT NULL COMMENT '角色编码',
  `email` varchar(64) DEFAULT NULL COMMENT '用户邮箱（审批/通知用）',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1-启用 0-禁用',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  UNIQUE KEY `uk_account` (`account`),
  UNIQUE KEY `uk_ak` (`access_key`),
  KEY `idx_role_code` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统用户表';


-- mdcp_data.view_subset_relation definition

CREATE TABLE `view_subset_relation` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `biz_id` varchar(64) NOT NULL COMMENT '业务唯一主键ID（全局唯一）',
  `relation_id` bigint NOT NULL COMMENT '关联业务关联ID',
  `view_id` bigint NOT NULL COMMENT '视图ID',
  `subset_id` bigint NOT NULL COMMENT '数据子集ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_biz_id` (`biz_id`),
  UNIQUE KEY `uk_view_subset` (`view_id`,`subset_id`),
  KEY `idx_view_id` (`view_id`),
  KEY `idx_subset_id` (`subset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='视图-子集关联表（多对多）';