from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class Dataset(BaseModel):
    """
    Dataset Aggregate Root
    """
    id: Optional[int] = None
    biz_id: str
    dataset_id: int
    project_id: int  # FK to data_project.id
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
    is_deleted: int = 0

    def update_info(self, **kwargs):
        """Update basic dataset info (name, type, tags, description, etc.)"""
        for k, v in kwargs.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

    def update_data_update_setting(self, is_open: int):
        """Toggle data update permission"""
        self.is_data_update_open = is_open

    def update_stat_association(
        self,
        stat_level1_id: Optional[int] = None,
        stat_level2_id: Optional[int] = None,
        stat_level3_id: Optional[int] = None,
    ):
        """Update statistics tree association"""
        self.stat_level1_id = stat_level1_id
        self.stat_level2_id = stat_level2_id
        self.stat_level3_id = stat_level3_id

    def delete(self):
        """Soft delete dataset"""
        self.is_deleted = 1
