from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple
from pydantic import BaseModel
from services.dataset.domain.entities.project import Project

class ProjectListItemDTO(BaseModel):
    id: int
    project_id: str
    project_name: str
    project_en_name: str
    create_user_id: int
    creator_name: str
    create_time: datetime
    update_time: datetime
    my_permission: Optional[str] = None

class ProjectRepository(ABC):
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
    async def list_projects(
        self, 
        user_id: int, 
        page: int, 
        size: int,
        project_name_like: Optional[str] = None,
        creator_name_like: Optional[str] = None,
        create_time_start: Optional[datetime] = None,
        create_time_end: Optional[datetime] = None,
        update_time_start: Optional[datetime] = None,
        update_time_end: Optional[datetime] = None,
        order_by: str = "id",
        order_direction: str = "asc"
    ) -> Tuple[List[ProjectListItemDTO], int]:
        """Return a list of projects and total count with filtering and sorting"""
        pass
