from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


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


class DatasetInfoResp(BaseModel):
    id: int
    biz_id: str
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
    create_user_id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
