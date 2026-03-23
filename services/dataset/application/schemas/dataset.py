from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, validator


class DatasetCreateReq(BaseModel):
    project_id: str = Field(..., description="项目业务ID（project_id字符串）")
    dataset_name: str = Field(..., max_length=64, description="数据集名称（项目内唯一）")
    dataset_en_name: str = Field(..., max_length=64, description="数据集英文名称")
    dataset_type: str = Field(..., max_length=32, description="数据集类型（标注数据集/暂存数据集等）")
    media_type: str = Field(..., max_length=32, description="数据媒体形式（图片/点云/视频等）")
    application_scenario: Optional[str] = Field(None, max_length=32, description="应用场景（研发训练/仿真测试等）")
    is_data_update_open: int = Field(0, description="是否开启数据更新：1-开启 0-关闭")
    related_dataset_id: Optional[int] = Field(None, description="关联数据集ID")
    stat_level1_id: Optional[int] = Field(None, description="关联统计树一级分类ID")
    stat_level2_id: Optional[int] = Field(None, description="关联统计树二级分类ID")
    stat_level3_id: Optional[int] = Field(None, description="关联统计树三级分类ID")
    tags: Optional[str] = Field(None, max_length=256, description="数据集标签，逗号分隔")
    description: Optional[str] = Field(None, description="数据集简介/概览描述")


class DatasetOverviewUpdateReq(BaseModel):
    description: str = Field(..., description="数据集概览描述，包括数据来源、标注规则、使用方式等")


class DatasetSchemaUpdateReq(BaseModel):
    schema_config: Dict[str, Any] = Field(..., description="数据结构Schema配置，符合Elasticsearch 7 mapping格式")

    @validator('schema_config')
    def check_reserved_fields(cls, v):
        reserved_fields = ['_doc_type', 'datasetsRelatedFiles']
        for field in reserved_fields:
            if field in v:
                raise ValueError(f"Field '{field}' is a reserved field and cannot be used")
        return v


class DatasetColumnUpdateReq(BaseModel):
    column_config: Dict[str, Any] = Field(..., description="数据列配置，定义数据列表展示的列信息")


class DatasetVisualUpdateReq(BaseModel):
    visual_config: Dict[str, Any] = Field(..., description="可视化信息配置，支持图片点线框、点云框、视频可视化等")


class DatasetInfoResp(BaseModel):
    id: int
    dataset_id: int
    project_id: int
    dataset_name: str
    dataset_en_name: str
    dataset_path: str
    dataset_type: str
    media_type: str
    application_scenario: Optional[str] = None
    is_data_update_open: int = 0
    related_dataset_id: Optional[int] = None
    stat_level1_id: Optional[int] = None
    stat_level2_id: Optional[int] = None
    stat_level3_id: Optional[int] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    schema_config: Optional[Dict[str, Any]] = None
    column_config: Optional[Dict[str, Any]] = None
    visual_config: Optional[Dict[str, Any]] = None
    create_user_id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
