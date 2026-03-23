import uuid
import random
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.dependencies.database import get_db
from services.dataset.domain.entities.dataset import Dataset
from services.dataset.domain.repositories.dataset_repository import DatasetRepository
from services.dataset.application.schemas.dataset import DatasetCreateReq, DatasetInfoResp
from services.dataset.infrastructure.repositories.dataset_repository_impl import DatasetRepositoryImpl


class DatasetApplicationService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo: DatasetRepository = DatasetRepositoryImpl(db)
        self.db = db

    async def create_dataset(self, req: DatasetCreateReq, current_user_id: int) -> DatasetInfoResp:
        # 1. Resolve project by business ID
        project = await self.repo.get_project_by_business_id(req.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # 2. Permission check: user must have 'manage' or 'edit' on the project
        has_perm = await self.repo.check_user_project_permission(
            project.id, current_user_id, ['manage', 'edit']
        )
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to create datasets in this project"
            )

        # 3. Check name conflicts within the project
        conflict = await self.repo.check_name_conflicts(
            project.id, req.dataset_name, req.dataset_en_name
        )
        if conflict == "name":
            raise HTTPException(status_code=400, detail="Dataset name already exists in this project")
        if conflict == "en_name":
            raise HTTPException(status_code=400, detail="Dataset English name already exists in this project")

        # 4. Build dataset path from project storage config
        dataset_path = f"{project.storage_dir}/{req.dataset_en_name}"

        # 5. Create Dataset aggregate root
        dataset = Dataset(
            biz_id=uuid.uuid4().hex,
            dataset_id=random.randint(100000, 999999),
            project_id=project.id,
            dataset_name=req.dataset_name,
            dataset_en_name=req.dataset_en_name,
            dataset_path=dataset_path,
            dataset_type=req.dataset_type,
            media_type=req.media_type,
            application_scenario=req.application_scenario,
            is_data_update_open=req.is_data_update_open,
            related_dataset_id=req.related_dataset_id,
            stat_level1_id=req.stat_level1_id,
            stat_level2_id=req.stat_level2_id,
            stat_level3_id=req.stat_level3_id,
            tags=req.tags,
            description=req.description,
            create_user_id=current_user_id,
        )

        # 6. Save
        saved = await self.repo.save(dataset)
        return DatasetInfoResp(
            id=saved.id,
            biz_id=saved.biz_id,
            dataset_id=saved.dataset_id,
            project_id=saved.project_id,
            dataset_name=saved.dataset_name,
            dataset_en_name=saved.dataset_en_name,
            dataset_path=saved.dataset_path,
            dataset_type=saved.dataset_type,
            media_type=saved.media_type,
            application_scenario=saved.application_scenario,
            is_data_update_open=saved.is_data_update_open,
            related_dataset_id=saved.related_dataset_id,
            stat_level1_id=saved.stat_level1_id,
            stat_level2_id=saved.stat_level2_id,
            stat_level3_id=saved.stat_level3_id,
            tags=saved.tags,
            description=saved.description,
            create_user_id=saved.create_user_id,
        )
