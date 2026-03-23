from typing import List, Optional
from pydantic import BaseModel

class ProjectPermission(BaseModel):
    user_id: int
    permission_type: str  # 'view', 'edit', 'manage'
    grant_user_id: int

class Project(BaseModel):
    """
    Project Aggregate Root
    """
    id: Optional[int] = None
    project_id: str
    project_name: str
    project_en_name: str
    is_compliance_open: int
    is_share_storage: int
    storage_type: str
    storage_endpoint: str
    bucket_name: str
    storage_dir: str
    write_ak: Optional[str] = None
    write_sk: Optional[str] = None
    read_ak: Optional[str] = None
    read_sk: Optional[str] = None
    create_user_id: int
    is_deleted: int = 0
    permissions: List[ProjectPermission] = []
    
    def update_info(self, project_name: str, **kwargs):
        """Update basic project info"""
        self.project_name = project_name
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
                
    def update_storage(self, is_empty: bool, **storage_configs):
        """Update storage configuration, only allowed if project is empty"""
        if not is_empty:
            raise ValueError("Storage configuration can only be modified when the project is empty (no datasets associated).")
        for k, v in storage_configs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def delete(self, is_empty: bool):
        """Delete project, only allowed if empty"""
        if not is_empty:
            raise ValueError("Project can only be deleted when it has no datasets.")
        self.is_deleted = 1
        
    def update_permissions(self, new_permissions: List[ProjectPermission]):
        """Replace current permissions with new ones"""
        self.permissions = new_permissions
