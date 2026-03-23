from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple
from pydantic import BaseModel
from services.dataset.domain.entities.dataset import Dataset


class DatasetListItemDTO(BaseModel):
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
    tags: Optional[str] = None
    description: Optional[str] = None
    create_user_id: int
    creator_name: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None


class DatasetRepository(ABC):

    @abstractmethod
    async def save(self, dataset: Dataset) -> Dataset:
        pass

    @abstractmethod
    async def get_by_id(self, dataset_db_id: int) -> Optional[Dataset]:
        pass


    @abstractmethod
    async def check_name_conflicts(self, project_db_id: int, dataset_name: str, dataset_en_name: str) -> Optional[str]:
        pass

    @abstractmethod
    async def check_user_project_permission(self, project_db_id: int, user_id: int, required_perms: List[str]) -> bool:
        pass

    @abstractmethod
    async def check_user_dataset_permission(self, dataset_db_id: int, user_id: int, required_perms: List[str]) -> bool:
        pass

    @abstractmethod
    async def get_project_by_business_id(self, project_id: str):
        """Get project ORM object by business project_id string"""
        pass

    @abstractmethod
    async def list_datasets(
        self,
        project_db_id: int,
        user_id: int,
        page: int,
        size: int,
        dataset_name_like: Optional[str] = None,
        dataset_type: Optional[str] = None,
        media_type: Optional[str] = None,
        order_by: str = "id",
        order_direction: str = "asc"
    ) -> Tuple[List[DatasetListItemDTO], int]:
        pass
