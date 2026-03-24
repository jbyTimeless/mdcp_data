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
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `project_quota` bigint NOT NULL DEFAULT '0' COMMENT '项目总存储配额，单位MB，0为不限制',
  `quota_used` bigint NOT NULL DEFAULT '0' COMMENT '项目已使用存储量，单位MB',
  `admin_user_id` varchar(64) NOT NULL COMMENT '项目管理员用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_project_id` (`project_id`),
  UNIQUE KEY `uk_project_name` (`project_name`),
  UNIQUE KEY `uk_project_en_name` (`project_en_name`),
  KEY `idx_create_user` (`create_user_id`),
  KEY `idx_project_id_covering` (`project_id`,`project_name`,`project_en_name`,`is_compliance_open`,`is_share_storage`,`create_user_id`,`create_time`,`is_deleted`),
  KEY `idx_admin_user` (`admin_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据项目表（数据集顶层管理单元）';



-- mdcp_data.data_stat_config definition
CREATE TABLE `data_stat_config` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `stat_id` varchar(64) NOT NULL COMMENT '统计配置业务关联ID',
  `parent_stat_id` varchar(64) NOT NULL DEFAULT '0' COMMENT '父统计ID，顶层为0',
  `stat_name` varchar(64) NOT NULL COMMENT '统计分类名称',
  `level` tinyint NOT NULL COMMENT '层级：1-一级 2-二级 3-三级',
  `summary_type` varchar(32) NOT NULL DEFAULT 'SUM' COMMENT '汇总类型：SUM/COUNT等',
  `description` varchar(512) DEFAULT NULL COMMENT '备注描述',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_parent_stat_name` (`parent_stat_id`,`stat_name`),
  KEY `idx_level` (`level`),
  KEY `idx_stat_id_covering` (`stat_id`,`parent_stat_id`,`stat_name`,`level`,`summary_type`,`create_user_id`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据统计配置表（统计树管理）';

-- mdcp_data.data_subset definition
CREATE TABLE `data_subset` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `subset_id` varchar(64) NOT NULL COMMENT '子集业务关联ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `parent_subset_id` varchar(64) NOT NULL DEFAULT '0' COMMENT '父子集ID，顶层子集为0',
  `subset_name` varchar(50) NOT NULL COMMENT '子集名称（数据集内唯一）',
  `subset_en_name` varchar(50) NOT NULL COMMENT '子集英文名称',
  `subset_path` varchar(256) NOT NULL COMMENT '子集存储路径',
  `level` tinyint NOT NULL COMMENT '层级（1-5，文档规定最深5层）',
  `description` varchar(512) DEFAULT NULL COMMENT '子集描述',
  `storage_used` bigint NOT NULL DEFAULT '0' COMMENT '子集已使用存储量，单位MB',
  `data_count` bigint NOT NULL DEFAULT '0' COMMENT '子集数据记录数',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dataset_subset_name` (`dataset_id`,`parent_subset_id`,`subset_name`),
  KEY `idx_dataset_id` (`dataset_id`),
  KEY `idx_parent_subset` (`parent_subset_id`),
  KEY `idx_level` (`level`),
  KEY `idx_subset_id_covering` (`subset_id`,`dataset_id`,`parent_subset_id`,`subset_name`,`subset_en_name`,`level`,`create_user_id`,`create_time`,`is_deleted`),
  KEY `idx_dataset_level` (`dataset_id`,`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据子集表（数据集物理树形分层）';

-- mdcp_data.dataset_info definition
CREATE TABLE `dataset_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '数据集业务关联ID',
  `project_id` varchar(64) NOT NULL COMMENT '所属项目ID',
  `dataset_name` varchar(64) NOT NULL COMMENT '数据集名称（项目内唯一）',
  `dataset_en_name` varchar(64) NOT NULL COMMENT '数据集英文名称',
  `dataset_path` varchar(256) NOT NULL COMMENT '数据集存储路径',
  `dataset_type` varchar(32) NOT NULL COMMENT '数据集类型（标注数据集/暂存数据集等）',
  `media_type` varchar(32) NOT NULL COMMENT '数据媒体形式（图片/点云/视频等）',
  `application_scenario` varchar(32) DEFAULT NULL COMMENT '应用场景（研发训练/仿真测试等）',
  `is_data_update_open` tinyint NOT NULL DEFAULT '0' COMMENT '是否开启数据更新：1-开启 0-关闭',
  `related_dataset_id` varchar(64) DEFAULT NULL COMMENT '关联数据集ID',
  `stat_level1_id` varchar(64) DEFAULT NULL COMMENT '关联统计树一级分类ID',
  `stat_level2_id` varchar(64) DEFAULT NULL COMMENT '关联统计树二级分类ID',
  `stat_level3_id` varchar(64) DEFAULT NULL COMMENT '关联统计树三级分类ID',
  `tags` varchar(256) DEFAULT NULL COMMENT '数据集标签，逗号分隔',
  `description` text COMMENT '数据集简介/概览描述',
  `schema_config` json DEFAULT NULL COMMENT '数据结构Schema配置（对应文档2.3.2.6.1）',
  `column_config` json DEFAULT NULL COMMENT '数据列配置（对应文档2.3.2.6.2）',
  `visual_config` json DEFAULT NULL COMMENT '可视化信息配置（对应文档2.3.2.7）',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `es_index_name` varchar(128) DEFAULT NULL COMMENT '关联ES索引名称（标签存储用）',
  `es_index_alias` varchar(128) DEFAULT NULL COMMENT 'ES索引别名，用于版本切换',
  `storage_quota` bigint NOT NULL DEFAULT '0' COMMENT '数据集存储配额，单位MB，0为不限制',
  `storage_used` bigint NOT NULL DEFAULT '0' COMMENT '已使用存储量，单位MB',
  `data_count` bigint NOT NULL DEFAULT '0' COMMENT '数据集总数据记录数',
  `config_version` int NOT NULL DEFAULT '1' COMMENT '配置版本号（schema/列/可视化配置）',
  `is_encrypted` tinyint NOT NULL DEFAULT '0' COMMENT '是否加密存储：1-是 0-否',
  `compliance_rule_id` varchar(64) DEFAULT NULL COMMENT '关联合规规则ID',
  `latest_snapshot_id` varchar(64) DEFAULT NULL COMMENT '最新快照ID',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_project_dataset_name` (`project_id`,`dataset_name`),
  UNIQUE KEY `uk_project_dataset_en_name` (`project_id`,`dataset_en_name`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_create_user` (`create_user_id`),
  KEY `idx_dataset_id_covering` (`dataset_id`,`project_id`,`dataset_name`,`dataset_en_name`,`dataset_type`,`media_type`,`create_user_id`,`create_time`,`is_deleted`),
  KEY `idx_es_index` (`es_index_name`),
  KEY `idx_project_quota` (`project_id`,`storage_quota`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集主表（数据集核心元数据表）';

-- mdcp_data.dataset_permission definition
CREATE TABLE `dataset_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `permission_id` varchar(64) NOT NULL COMMENT '权限业务关联ID',
  `resource_type` varchar(32) NOT NULL COMMENT '资源类型：project-项目 dataset-数据集 subset-子集 view-视图',
  `resource_id` varchar(64) NOT NULL COMMENT '资源ID（对应项目/数据集/子集/视图主键）',
  `user_id` varchar(64) NOT NULL COMMENT '被授权用户ID',
  `permission_type` varchar(32) NOT NULL COMMENT '权限类型：view-查看 edit-编辑 manage-管理',
  `grant_user_id` varchar(64) NOT NULL COMMENT '授权人用户ID',
  `grant_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权时间',
  `valid_start_time` datetime DEFAULT NULL COMMENT '权限生效时间',
  `valid_end_time` datetime DEFAULT NULL COMMENT '权限失效时间',
  `apply_id` varchar(64) DEFAULT NULL COMMENT '关联权限申请单ID',
  `permission_desc` varchar(512) DEFAULT NULL COMMENT '权限授权说明',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1-生效 0-失效',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_resource_user` (`resource_type`,`resource_id`,`user_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_resource` (`resource_type`,`resource_id`),
  KEY `idx_permission_id_covering` (`permission_id`,`resource_type`,`resource_id`,`user_id`,`permission_type`,`status`),
  KEY `idx_valid_time` (`valid_start_time`,`valid_end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集权限表（细粒度权限控制）';

-- mdcp_data.dataset_view definition
CREATE TABLE `dataset_view` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `view_id` varchar(64) NOT NULL COMMENT '视图业务关联ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `view_name` varchar(64) NOT NULL COMMENT '视图名称（数据集内唯一）',
  `view_en_name` varchar(64) NOT NULL COMMENT '视图英文名称',
  `filter_condition` text COMMENT '视图筛选条件SQL/DSL',
  `description` varchar(512) DEFAULT NULL COMMENT '视图描述',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dataset_view_name` (`dataset_id`,`view_name`),
  KEY `idx_dataset_id` (`dataset_id`),
  KEY `idx_view_id_covering` (`view_id`,`dataset_id`,`view_name`,`view_en_name`,`create_user_id`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集视图表（数据集逻辑筛选视图）';

-- mdcp_data.label_delivery_task definition
CREATE TABLE `label_delivery_task` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `task_id` varchar(64) NOT NULL COMMENT '送标任务业务关联ID',
  `task_name` varchar(128) NOT NULL COMMENT '标注任务名称',
  `label_category` varchar(32) NOT NULL COMMENT '标注分类',
  `label_type_id` bigint NOT NULL COMMENT '标注类型ID',
  `related_channel_code` varchar(64) NOT NULL COMMENT '关联标注平台通道号',
  `source_dataset_id` varchar(64) NOT NULL COMMENT '源数据集ID',
  `source_subset_id` varchar(64) DEFAULT NULL COMMENT '源数据子集ID',
  `data_count` bigint DEFAULT '0' COMMENT '标注数据量',
  `delivery_dataset_id` varchar(64) NOT NULL COMMENT '标注结果交付数据集ID',
  `remark` text COMMENT '备注信息',
  `task_status` varchar(32) NOT NULL DEFAULT 'pending' COMMENT '任务状态：pending-待处理 forwarding-待转发 labeling-标注中 finished-已标注 failed-失败',
  `label_platform_batch_no` varchar(64) DEFAULT NULL COMMENT '标注平台批次号',
  `finish_time` datetime DEFAULT NULL COMMENT '任务完成时间',
  `label_progress` int NOT NULL DEFAULT '0' COMMENT '标注进度百分比0-100',
  `send_back_reason` text COMMENT '标注驳回原因',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_label_type` (`label_type_id`),
  KEY `idx_source_dataset` (`source_dataset_id`),
  KEY `idx_task_status` (`task_status`),
  KEY `idx_batch_no` (`label_platform_batch_no`),
  KEY `idx_task_id_covering` (`task_id`,`task_name`,`label_category`,`source_dataset_id`,`delivery_dataset_id`,`task_status`,`create_user_id`,`create_time`),
  KEY `idx_create_time_status` (`create_time`,`task_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据送标任务表';

-- mdcp_data.label_type definition
CREATE TABLE `label_type` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `type_id` bigint NOT NULL COMMENT '标注类型业务关联ID',
  `label_category` varchar(32) NOT NULL COMMENT '标注分类（2D/3D等）',
  `type_name` varchar(32) NOT NULL COMMENT '标注类型名称',
  `type_en_name` varchar(32) NOT NULL COMMENT '标注类型英文名称',
  `related_channel_code` varchar(64) NOT NULL COMMENT '关联标注平台通道号/项目号',
  `description` varchar(512) DEFAULT NULL COMMENT '描述',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1-启用 0-禁用',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_type_name` (`type_name`),
  UNIQUE KEY `uk_channel_code` (`related_channel_code`),
  KEY `idx_label_category` (`label_category`),
  KEY `idx_type_id_covering` (`type_id`,`label_category`,`type_name`,`type_en_name`,`status`,`create_user_id`,`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='标注类型配置表';

-- mdcp_data.stat_dataset_relation definition
CREATE TABLE `stat_dataset_relation` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `relation_id` varchar(64) NOT NULL COMMENT '关联业务关联ID',
  `stat_id` varchar(64) NOT NULL COMMENT '三级统计分类ID',
  `project_id` varchar(64) NOT NULL COMMENT '所属项目ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '数据集ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_stat_dataset` (`stat_id`,`dataset_id`),
  KEY `idx_stat_id` (`stat_id`),
  KEY `idx_dataset_id` (`dataset_id`),
  KEY `idx_relation_id_covering` (`relation_id`,`stat_id`,`project_id`,`dataset_id`,`create_time`)
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
  UNIQUE KEY `uk_role_code` (`role_code`),
  KEY `idx_role_id_covering` (`role_id`,`role_name`,`role_code`,`status`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统角色表';

-- mdcp_data.sys_user definition
CREATE TABLE `sys_user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '【物理主键】数据库自增ID，仅内部使用',
  `user_id` varchar(64) NOT NULL COMMENT '【业务主键】用户唯一ID（自定义雪花ID）',
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
  KEY `idx_role_code` (`role_code`),
  KEY `idx_user_id_covering` (`user_id`,`account`,`username`,`role_code`,`email`,`status`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统用户表';

-- mdcp_data.view_subset_relation definition
CREATE TABLE `view_subset_relation` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `relation_id` varchar(64) NOT NULL COMMENT '关联业务关联ID',
  `view_id` varchar(64) NOT NULL COMMENT '视图ID',
  `subset_id` varchar(64) NOT NULL COMMENT '数据子集ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_view_subset` (`view_id`,`subset_id`),
  KEY `idx_view_id` (`view_id`),
  KEY `idx_subset_id` (`subset_id`),
  KEY `idx_relation_id_covering` (`relation_id`,`view_id`,`subset_id`,`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='视图-子集关联表（多对多）';



-- 1. dataset_es_index_mapping 数据集 - ES 索引映射表
CREATE TABLE `dataset_es_index_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `mapping_id` varchar(64) NOT NULL COMMENT '映射关系业务ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `es_index_name` varchar(128) NOT NULL COMMENT 'ES索引名称',
  `es_index_alias` varchar(128) DEFAULT NULL COMMENT 'ES索引别名',
  `index_shards` int NOT NULL DEFAULT '3' COMMENT '索引分片数',
  `index_replicas` int NOT NULL DEFAULT '1' COMMENT '索引副本数',
  `index_status` varchar(32) NOT NULL DEFAULT 'active' COMMENT '索引状态：active-正常 read_only-只读 deleted-已删除',
  `sync_strategy` varchar(32) NOT NULL DEFAULT 'real_time' COMMENT '同步策略：real_time-实时 near_real_time-近实时 scheduled-定时',
  `last_sync_time` datetime DEFAULT NULL COMMENT '最后一次同步时间',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dataset_id` (`dataset_id`),
  UNIQUE KEY `uk_es_index_name` (`es_index_name`),
  KEY `idx_index_status` (`index_status`),
  KEY `idx_mapping_id_covering` (`mapping_id`,`dataset_id`,`es_index_name`,`index_status`,`sync_strategy`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集-ES索引映射表（标签存储核心关联）';



-- 2. dataset_es_sync_task 数据同步任务表
CREATE TABLE `dataset_es_sync_task` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `task_id` varchar(64) NOT NULL COMMENT '同步任务业务ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `sync_type` varchar(32) NOT NULL COMMENT '同步类型：full-全量增量-增量',
  `sync_scope` varchar(32) NOT NULL DEFAULT 'all' COMMENT '同步范围：all-全量 subset-指定子集',
  `related_subset_ids` text COMMENT '关联子集ID列表，逗号分隔',
  `task_status` varchar(32) NOT NULL DEFAULT 'pending' COMMENT '任务状态：pending-待执行 running-执行中 success-成功 failed-失败',
  `schedule_cron` varchar(64) DEFAULT NULL COMMENT '定时任务cron表达式，定时同步用',
  `data_count_total` bigint DEFAULT '0' COMMENT '待同步总数据量',
  `data_count_success` bigint DEFAULT '0' COMMENT '同步成功数据量',
  `data_count_failed` bigint DEFAULT '0' COMMENT '同步失败数据量',
  `error_msg` text COMMENT '失败错误信息',
  `start_time` datetime DEFAULT NULL COMMENT '执行开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '执行结束时间',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_task_id` (`task_id`),
  KEY `idx_dataset_id` (`dataset_id`),
  KEY `idx_task_status` (`task_status`),
  KEY `idx_task_id_covering` (`task_id`,`dataset_id`,`sync_type`,`task_status`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ES数据同步任务表';

-- 3. dataset_es_sync_record 同步执行记录表
CREATE TABLE `dataset_es_sync_record` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `record_id` varchar(64) NOT NULL COMMENT '同步记录业务ID',
  `task_id` varchar(64) NOT NULL COMMENT '关联同步任务ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `data_unique_id` varchar(128) NOT NULL COMMENT '数据唯一溯源ID',
  `sync_type` varchar(32) NOT NULL COMMENT '操作类型：insert-新增 update-更新 delete-删除',
  `sync_status` varchar(32) NOT NULL COMMENT '同步状态：success-成功 failed-失败',
  `error_msg` text COMMENT '失败原因',
  `sync_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '同步时间',
  `create_user_id` varchar(64) NOT NULL COMMENT '操作人用户ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_record_id` (`record_id`),
  KEY `idx_task_id` (`task_id`),
  KEY `idx_dataset_data_id` (`dataset_id`,`data_unique_id`),
  KEY `idx_sync_time` (`sync_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ES同步执行明细记录表（单条数据粒度）';


-- 4. dataset_file_metadata 数据集文件元数据表
CREATE TABLE `dataset_file_metadata` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `file_id` varchar(64) NOT NULL COMMENT '文件唯一业务ID',
  `project_id` varchar(64) NOT NULL COMMENT '所属项目ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `subset_id` varchar(64) DEFAULT NULL COMMENT '所属子集ID',
  `data_unique_id` varchar(128) DEFAULT NULL COMMENT '关联数据记录唯一溯源ID',
  `file_name` varchar(256) NOT NULL COMMENT '文件名称',
  `file_suffix` varchar(32) DEFAULT NULL COMMENT '文件后缀',
  `file_type` varchar(32) NOT NULL COMMENT '文件类型：image-图片 point_cloud-点云 video-视频 record-录包 other-其他',
  `file_size` bigint NOT NULL COMMENT '文件大小，单位Byte',
  `file_md5` varchar(64) NOT NULL COMMENT '文件MD5值，用于完整性校验',
  `minio_bucket` varchar(128) NOT NULL COMMENT 'MinIO Bucket名称',
  `minio_object_path` varchar(512) NOT NULL COMMENT 'MinIO对象完整路径',
  `is_public` tinyint NOT NULL DEFAULT '0' COMMENT '是否公开访问：1-是 0-否',
  `access_count` bigint NOT NULL DEFAULT '0' COMMENT '访问次数',
  `last_access_time` datetime DEFAULT NULL COMMENT '最后访问时间',
  `file_status` varchar(32) NOT NULL DEFAULT 'normal' COMMENT '文件状态：normal-正常 archived-归档 deleted-已删除',
  `create_user_id` varchar(64) NOT NULL COMMENT '上传人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_file_id` (`file_id`),
  UNIQUE KEY `uk_minio_path` (`minio_bucket`,`minio_object_path`),
  KEY `idx_dataset_subset` (`dataset_id`,`subset_id`),
  KEY `idx_data_unique_id` (`data_unique_id`),
  KEY `idx_file_status` (`file_status`),
  KEY `idx_file_id_covering` (`file_id`,`dataset_id`,`file_type`,`file_size`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集文件元数据表（MinIO对象核心管理）';

-- 5. dataset_storage_lifecycle 存储生命周期规则表
CREATE TABLE `dataset_storage_lifecycle` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `rule_id` varchar(64) NOT NULL COMMENT '规则业务ID',
  `rule_name` varchar(64) NOT NULL COMMENT '规则名称',
  `resource_type` varchar(32) NOT NULL COMMENT '资源类型：project-项目 dataset-数据集',
  `resource_id` varchar(64) NOT NULL COMMENT '资源ID',
  `file_type` varchar(32) DEFAULT NULL COMMENT '适用文件类型，为空则全部适用',
  `auto_archive_days` int DEFAULT NULL COMMENT '自动归档天数，为空不归档',
  `auto_delete_days` int DEFAULT NULL COMMENT '自动删除天数，为空不删除',
  `rule_status` tinyint NOT NULL DEFAULT '1' COMMENT '规则状态：1-启用 0-禁用',
  `last_execute_time` datetime DEFAULT NULL COMMENT '最后执行时间',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_rule_id` (`rule_id`),
  KEY `idx_resource` (`resource_type`,`resource_id`),
  KEY `idx_rule_status` (`rule_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存储生命周期规则表（MinIO冷热数据/归档管理）';

-- 6. dataset_permission_apply 权限申请单表
CREATE TABLE `dataset_permission_apply` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `apply_id` varchar(64) NOT NULL COMMENT '申请单业务ID',
  `apply_user_id` varchar(64) NOT NULL COMMENT '申请人用户ID',
  `resource_type` varchar(32) NOT NULL COMMENT '资源类型：project-项目 dataset-数据集 subset-子集 view-视图',
  `resource_id` varchar(64) NOT NULL COMMENT '申请资源ID',
  `resource_name` varchar(128) NOT NULL COMMENT '资源名称，冗余字段便于展示',
  `apply_permission_type` varchar(32) NOT NULL COMMENT '申请权限类型：view-查看 edit-编辑 manage-管理',
  `valid_start_time` datetime NOT NULL COMMENT '权限生效时间',
  `valid_end_time` datetime DEFAULT NULL COMMENT '权限失效时间，为空则永久',
  `apply_reason` text NOT NULL COMMENT '申请理由',
  `approver_user_id` varchar(64) NOT NULL COMMENT '审批人用户ID（项目管理员）',
  `apply_status` varchar(32) NOT NULL DEFAULT 'pending' COMMENT '申请状态：pending-待审批 approved-已通过 rejected-已驳回 canceled-已撤销',
  `approval_opinion` text COMMENT '审批意见',
  `approval_time` datetime DEFAULT NULL COMMENT '审批时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_apply_id` (`apply_id`),
  KEY `idx_apply_user` (`apply_user_id`),
  KEY `idx_approver_user` (`approver_user_id`),
  KEY `idx_apply_status` (`apply_status`),
  KEY `idx_resource` (`resource_type`,`resource_id`),
  KEY `idx_apply_id_covering` (`apply_id`,`apply_user_id`,`resource_type`,`resource_id`,`apply_status`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集权限申请单表';


-- 7. dataset_permission_approval_record 审批记录表
CREATE TABLE `dataset_permission_approval_record` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `record_id` varchar(64) NOT NULL COMMENT '审批记录业务ID',
  `apply_id` varchar(64) NOT NULL COMMENT '关联申请单ID',
  `operate_user_id` varchar(64) NOT NULL COMMENT '操作人用户ID',
  `operate_type` varchar(32) NOT NULL COMMENT '操作类型：submit-提交 approve-通过 reject-驳回 cancel-撤销',
  `operate_opinion` text COMMENT '操作意见',
  `operate_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_record_id` (`record_id`),
  KEY `idx_apply_id` (`apply_id`),
  KEY `idx_operate_time` (`operate_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='权限审批流程记录表（全流程留痕）';

-- 8. label_delivery_data_detail 送标数据明细表
CREATE TABLE `label_delivery_data_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `detail_id` varchar(64) NOT NULL COMMENT '明细业务ID',
  `task_id` varchar(64) NOT NULL COMMENT '关联送标任务ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '源数据集ID',
  `subset_id` varchar(64) NOT NULL COMMENT '源数据子集ID',
  `data_unique_id` varchar(128) NOT NULL COMMENT '数据唯一溯源ID',
  `file_id_list` text COMMENT '关联文件ID列表，逗号分隔',
  `delivery_status` varchar(32) NOT NULL DEFAULT 'pending' COMMENT '送标状态：pending-待送标 delivered-已送标 labeling-标注中 finished-已完成 failed-失败',
  `label_platform_data_id` varchar(128) DEFAULT NULL COMMENT '标注平台数据ID',
  `label_result_backfilled` tinyint NOT NULL DEFAULT '0' COMMENT '是否已回灌：1-是 0-否',
  `backfill_time` datetime DEFAULT NULL COMMENT '回灌时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_detail_id` (`detail_id`),
  UNIQUE KEY `uk_task_data_id` (`task_id`,`data_unique_id`),
  KEY `idx_task_id` (`task_id`),
  KEY `idx_data_unique_id` (`data_unique_id`),
  KEY `idx_delivery_status` (`delivery_status`),
  KEY `idx_detail_id_covering` (`detail_id`,`task_id`,`data_unique_id`,`delivery_status`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='送标数据明细表（单条数据粒度）';



-- 9. label_result_backfill_detail 标注结果回灌明细表
CREATE TABLE `label_result_backfill_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `backfill_id` varchar(64) NOT NULL COMMENT '回灌明细业务ID',
  `task_id` varchar(64) NOT NULL COMMENT '关联送标任务ID',
  `data_unique_id` varchar(128) NOT NULL COMMENT '源数据唯一溯源ID',
  `label_platform_batch_no` varchar(64) NOT NULL COMMENT '标注平台批次号',
  `label_result_json` json NOT NULL COMMENT '标注结果JSON',
  `label_file_id_list` text COMMENT '标注结果文件ID列表，逗号分隔',
  `labeler` varchar(64) DEFAULT NULL COMMENT '标注人',
  `checker` varchar(64) DEFAULT NULL COMMENT '质检人',
  `label_finish_time` datetime DEFAULT NULL COMMENT '标注完成时间',
  `backfill_status` varchar(32) NOT NULL DEFAULT 'success' COMMENT '回灌状态：success-成功 failed-失败',
  `error_msg` text COMMENT '回灌失败原因',
  `backfill_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '回灌时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_backfill_id` (`backfill_id`),
  KEY `idx_task_id` (`task_id`),
  KEY `idx_data_unique_id` (`data_unique_id`),
  KEY `idx_batch_no` (`label_platform_batch_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='标注结果回灌明细表';



-- 10. label_data_quality_check 标注数据质检表
CREATE TABLE `label_data_quality_check` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `check_id` varchar(64) NOT NULL COMMENT '质检业务ID',
  `task_id` varchar(64) NOT NULL COMMENT '关联送标任务ID',
  `data_unique_id` varchar(128) NOT NULL COMMENT '数据唯一溯源ID',
  `check_type` varchar(32) NOT NULL COMMENT '质检类型：auto-自动质检 manual-人工质检',
  `check_result` varchar(32) NOT NULL COMMENT '质检结果：pass-合格 reject-驳回',
  `check_item` text COMMENT '质检项明细',
  `reject_reason` text COMMENT '驳回原因',
  `check_user_id` varchar(64) DEFAULT NULL COMMENT '质检人用户ID',
  `check_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '质检时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_check_id` (`check_id`),
  KEY `idx_task_id` (`task_id`),
  KEY `idx_data_unique_id` (`data_unique_id`),
  KEY `idx_check_result` (`check_result`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='标注数据质检表';


-- 11. dataset_operation_audit_log 数据集操作审计日志表
CREATE TABLE `dataset_operation_audit_log` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `log_id` varchar(64) NOT NULL COMMENT '日志唯一ID',
  `user_id` varchar(64) NOT NULL COMMENT '操作人用户ID',
  `user_account` varchar(64) NOT NULL COMMENT '操作人账号',
  `resource_type` varchar(32) NOT NULL COMMENT '资源类型：project-项目 dataset-数据集 subset-子集 view-视图 file-文件 data-数据记录',
  `resource_id` varchar(64) NOT NULL COMMENT '操作资源ID',
  `resource_name` varchar(128) DEFAULT NULL COMMENT '资源名称，冗余字段',
  `operation_type` varchar(32) NOT NULL COMMENT '操作类型：create-新增 query-查询 update-修改 delete-删除 download-下载 upload-上传 permission-权限配置',
  `operation_detail` text COMMENT '操作详情JSON',
  `client_ip` varchar(64) DEFAULT NULL COMMENT '客户端IP',
  `user_agent` varchar(512) DEFAULT NULL COMMENT '客户端UA',
  `operation_result` varchar(32) NOT NULL COMMENT '操作结果：success-成功 failed-失败',
  `error_msg` text COMMENT '失败原因',
  `operation_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_log_id` (`log_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_resource` (`resource_type`,`resource_id`),
  KEY `idx_operation_time` (`operation_time`),
  KEY `idx_operation_type` (`operation_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集操作审计日志表（全操作留痕，合规必备）';

-- 12. dataset_compliance_rule 合规规则配置表
CREATE TABLE `dataset_compliance_rule` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `rule_id` varchar(64) NOT NULL COMMENT '合规规则业务ID',
  `rule_name` varchar(64) NOT NULL COMMENT '规则名称',
  `rule_type` varchar(32) NOT NULL COMMENT '规则类型：data_mask-数据脱敏 access_control-访问控制 data_retention-数据留存 export_control-导出管控',
  `rule_content` text NOT NULL COMMENT '规则内容JSON',
  `rule_level` varchar(32) NOT NULL DEFAULT 'warn' COMMENT '规则级别：forbid-强制阻断 warn-告警提示',
  `rule_status` tinyint NOT NULL DEFAULT '1' COMMENT '规则状态：1-启用 0-禁用',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_rule_id` (`rule_id`),
  KEY `idx_rule_type` (`rule_type`),
  KEY `idx_rule_status` (`rule_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集合规规则配置表';

-- 13. dataset_quality_rule 数据质量规则配置表
CREATE TABLE `dataset_quality_rule` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `rule_id` varchar(64) NOT NULL COMMENT '质量规则业务ID',
  `rule_name` varchar(64) NOT NULL COMMENT '规则名称',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `rule_type` varchar(32) NOT NULL COMMENT '规则类型：non_null-非空 uniqueness-唯一性 range-数值范围 format-格式正则 custom-自定义',
  `rule_content` text NOT NULL COMMENT '规则配置JSON',
  `error_level` varchar(32) NOT NULL DEFAULT 'warn' COMMENT '错误级别：error-错误 warn-告警',
  `rule_status` tinyint NOT NULL DEFAULT '1' COMMENT '规则状态：1-启用 0-禁用',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_rule_id` (`rule_id`),
  KEY `idx_dataset_id` (`dataset_id`),
  KEY `idx_rule_type` (`rule_type`),
  KEY `idx_rule_status` (`rule_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据质量规则配置表';

-- 14. dataset_config_snapshot 数据集配置快照表
CREATE TABLE `dataset_config_snapshot` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `snapshot_id` varchar(64) NOT NULL COMMENT '快照业务ID',
  `dataset_id` varchar(64) NOT NULL COMMENT '所属数据集ID',
  `config_version` int NOT NULL COMMENT '配置版本号',
  `schema_config` json NOT NULL COMMENT '快照时的数据结构配置',
  `column_config` json NOT NULL COMMENT '快照时的数据列配置',
  `visual_config` json NOT NULL COMMENT '快照时的可视化配置',
  `dataset_base_info` json NOT NULL COMMENT '快照时的数据集基础信息',
  `snapshot_desc` varchar(512) DEFAULT NULL COMMENT '快照备注',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '快照创建时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_snapshot_id` (`snapshot_id`),
  UNIQUE KEY `uk_dataset_version` (`dataset_id`,`config_version`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集配置快照表（支持配置回滚）';


-- 15. dataset_data_operation_task 数据操作任务表
CREATE TABLE `dataset_data_operation_task` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键ID',
  `task_id` varchar(64) NOT NULL COMMENT '任务业务ID',
  `task_name` varchar(128) NOT NULL COMMENT '任务名称',
  `operation_type` varchar(32) NOT NULL COMMENT '操作类型：upload-上传 download-下载 migrate-迁移 copy-复制 delete-删除',
  `source_dataset_id` varchar(64) NOT NULL COMMENT '源数据集ID',
  `source_subset_id` varchar(64) DEFAULT NULL COMMENT '源子集ID',
  `filter_condition` text COMMENT '数据筛选条件',
  `target_dataset_id` varchar(64) DEFAULT NULL COMMENT '目标数据集ID（迁移/复制用）',
  `target_subset_id` varchar(64) DEFAULT NULL COMMENT '目标子集ID（迁移/复制用）',
  `task_status` varchar(32) NOT NULL DEFAULT 'pending' COMMENT '任务状态：pending-待执行 running-执行中 success-成功 failed-失败 canceled-已取消',
  `data_count_total` bigint DEFAULT '0' COMMENT '总数据量',
  `data_count_processed` bigint DEFAULT '0' COMMENT '已处理数据量',
  `file_size_total` bigint DEFAULT '0' COMMENT '总文件大小，单位Byte',
  `file_size_processed` bigint DEFAULT '0' COMMENT '已处理文件大小，单位Byte',
  `error_msg` text COMMENT '失败错误信息',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `create_user_id` varchar(64) NOT NULL COMMENT '创建人用户ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '软删除：0-未删除 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_task_id` (`task_id`),
  KEY `idx_operation_type` (`operation_type`),
  KEY `idx_task_status` (`task_status`),
  KEY `idx_source_dataset` (`source_dataset_id`),
  KEY `idx_create_user` (`create_user_id`),
  KEY `idx_task_id_covering` (`task_id`,`operation_type`,`task_status`,`source_dataset_id`,`create_time`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据集数据操作任务表（Client端批量操作管理）';