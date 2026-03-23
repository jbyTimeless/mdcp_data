from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from pydantic import BaseModel
from services.dataset.domain.entities.project import Project

class ProjectListItemDTO(BaseModel):
    id: int
    project_id: str
    project_name: str
    project_en_name: str
    my_permission: Optional[str] = None
    creator_name: str

class ProjectRepository(ABC):
    @abstractmethod
    async def create_project(self, req: 'ProjectCreateReq', current_user_id: int) -> 'ProjectInfoResp':
        pass
        
    @abstractmethod
    async def get_by_id(self, project_id: str) -> Optional[Project]:
        pass
        
    @abstractmethod
    async def save(self, project: Project) -> Project:
        pass
        
    @abstractmethod
    async def delete(self, project: Project) -> None:
        pass
        
    @abstractmethod
    async def check_name_conflicts(self, project_name: str, project_en_name: str) -> Optional[str]:
        """Return 'name' if project_name exists, 'en_name' if project_en_name exists, or None"""
        pass
        
    @abstractmethod
    async def is_project_empty(self, project_db_id: int) -> bool:
        """Check if project has no associated datasets"""
        pass
        
    @abstractmethod
    async def list_projects(self, user_id: int, page: int, size: int) -> Tuple[List[ProjectListItemDTO], int]:
        """Return a list of projects and total count"""
        pass
