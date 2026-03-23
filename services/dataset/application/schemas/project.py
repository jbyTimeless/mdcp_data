from pydantic import BaseModel, Field
from typing import Optional, List

class ProjectCreateReq(BaseModel):
    project_name: str = Field(..., max_length=32, description="项目名称（全局唯一）")
    project_en_name: str = Field(..., max_length=32, description="项目英文名称（英文开头，字母/数字/中划线/下划线）")
    is_compliance_open: int = Field(0, description="是否开启合规：1-开启 0-关闭")
    is_share_storage: int = Field(0, description="是否共享存储空间：1-开启 0-关闭")
    
    # Storage Configurations
    storage_type: str = Field("baidu_bos", max_length=32, description="存储类型")
    storage_endpoint: str = Field(..., max_length=128, description="存储端点")
    bucket_name: str = Field(..., max_length=64, description="bucket名称")
    storage_dir: str = Field(..., max_length=256, description="存储目录")
    
    # Write AK/SK
    write_ak: Optional[str] = Field(None, max_length=128, description="写入账号AK")
    write_sk: Optional[str] = Field(None, max_length=256, description="写入账号SK")
    
    # Read AK/SK
    read_ak: Optional[str] = Field(None, max_length=128, description="读取账号AK")
    read_sk: Optional[str] = Field(None, max_length=256, description="读取账号SK")

class ProjectInfoResp(BaseModel):
    id: int
    project_id: str
    project_name: str
    project_en_name: str
    is_compliance_open: int
    is_share_storage: int
    storage_type: str
    storage_endpoint: str
    bucket_name: str
    storage_dir: str
    create_user_id: int
    
    class Config:
        from_attributes = True

class ProjectListItemDTO(BaseModel):
    id: int
    project_id: str
    project_name: str
    project_en_name: str
    my_permission: Optional[str] = None
    creator_name: str

class ProjectListResp(BaseModel):
    total: int
    items: List[ProjectListItemDTO]

class ProjectUpdateReq(BaseModel):
    project_name: str
    is_compliance_open: int = 0
    is_share_storage: int = 0
    storage_type: str
    storage_endpoint: str
    bucket_name: str
    storage_dir: str
    write_ak: Optional[str] = None
    write_sk: Optional[str] = None
    read_ak: Optional[str] = None
    read_sk: Optional[str] = None

class ProjectPermissionItem(BaseModel):
    user_id: int
    username: str
    permission_type: str

class ProjectPermissionListResp(BaseModel):
    items: List[ProjectPermissionItem]

class ProjectPermissionUpdateItem(BaseModel):
    user_id: int
    permission_type: str

class ProjectPermissionUpdateReq(BaseModel):
    permissions: List[ProjectPermissionUpdateItem]
