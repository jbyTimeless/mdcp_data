import uuid
import random
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc
from services.dataset.domain.entities.dataset import Dataset
from services.dataset.domain.repositories.dataset_repository import DatasetRepository, DatasetListItemDTO
from services.dataset.infrastructure.models import (
    DatasetInfo, DataProject, DatasetPermission, SysUser, StatDatasetRelation
)


class DatasetRepositoryImpl(DatasetRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project_by_business_id(self, project_id: str):
        """Get project ORM object by business project_id string"""
        stmt = select(DataProject).where(
            DataProject.project_id == project_id,
            DataProject.is_deleted == 0
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def check_user_project_permission(
        self, project_db_id: int, user_id: int, required_perms: List[str]
    ) -> bool:
        """Check if user has required permission on a project (or is the creator)"""
        # Check if user is the project creator (always has manage permission)
        proj_stmt = select(DataProject.create_user_id).where(DataProject.id == project_db_id)
        proj_result = await self.session.execute(proj_stmt)
        creator_id = proj_result.scalar()
        if creator_id == user_id:
            return True

        # Check dataset_permission table
        perm_stmt = select(DatasetPermission.permission_type).where(
            DatasetPermission.resource_type == 'project',
            DatasetPermission.resource_id == project_db_id,
            DatasetPermission.user_id == user_id,
            DatasetPermission.status == 1
        )
        perm_result = await self.session.execute(perm_stmt)
        user_perm = perm_result.scalar()
        return user_perm in required_perms

    async def check_name_conflicts(
        self, project_db_id: int, dataset_name: str, dataset_en_name: str
    ) -> Optional[str]:
        """Check if dataset name or en_name already exists within the project"""
        stmt = select(DatasetInfo).where(
            DatasetInfo.project_id == project_db_id,
            DatasetInfo.is_deleted == 0,
            or_(
                DatasetInfo.dataset_name == dataset_name,
                DatasetInfo.dataset_en_name == dataset_en_name
            )
        )
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            if existing.dataset_name == dataset_name:
                return "name"
            if existing.dataset_en_name == dataset_en_name:
                return "en_name"
        return None

    async def save(self, dataset: Dataset) -> Dataset:
        if dataset.id is None:
            # Create new
            new_ds = DatasetInfo(
                biz_id=dataset.biz_id,
                dataset_id=dataset.dataset_id,
                project_id=dataset.project_id,
                dataset_name=dataset.dataset_name,
                dataset_en_name=dataset.dataset_en_name,
                dataset_path=dataset.dataset_path,
                dataset_type=dataset.dataset_type,
                media_type=dataset.media_type,
                application_scenario=dataset.application_scenario,
                is_data_update_open=dataset.is_data_update_open,
                related_dataset_id=dataset.related_dataset_id,
                stat_level1_id=dataset.stat_level1_id,
                stat_level2_id=dataset.stat_level2_id,
                stat_level3_id=dataset.stat_level3_id,
                tags=dataset.tags,
                description=dataset.description,
                schema_config=dataset.schema_config,
                column_config=dataset.column_config,
                visual_config=dataset.visual_config,
                create_user_id=dataset.create_user_id,
            )
            self.session.add(new_ds)
            await self.session.flush()
            dataset.id = new_ds.id

            # Handle stat_dataset_relation if stat_level3_id is provided
            if dataset.stat_level3_id:
                relation = StatDatasetRelation(
                    biz_id=uuid.uuid4().hex,
                    relation_id=random.randint(100000, 999999),
                    stat_id=dataset.stat_level3_id,
                    project_id=dataset.project_id,
                    dataset_id=new_ds.id,
                )
                self.session.add(relation)
        else:
            # Update existing
            stmt = select(DatasetInfo).where(DatasetInfo.id == dataset.id)
            result = await self.session.execute(stmt)
            ds = result.scalars().first()
            if ds:
                ds.dataset_name = dataset.dataset_name
                ds.dataset_en_name = dataset.dataset_en_name
                ds.dataset_type = dataset.dataset_type
                ds.media_type = dataset.media_type
                ds.application_scenario = dataset.application_scenario
                ds.is_data_update_open = dataset.is_data_update_open
                ds.related_dataset_id = dataset.related_dataset_id
                ds.stat_level1_id = dataset.stat_level1_id
                ds.stat_level2_id = dataset.stat_level2_id
                ds.stat_level3_id = dataset.stat_level3_id
                ds.tags = dataset.tags
                ds.description = dataset.description
                ds.schema_config = dataset.schema_config
                ds.column_config = dataset.column_config
                ds.visual_config = dataset.visual_config
                ds.is_deleted = dataset.is_deleted

        await self.session.commit()
        return dataset

    async def get_by_id(self, dataset_db_id: int) -> Optional[Dataset]:
        stmt = select(DatasetInfo).where(
            DatasetInfo.id == dataset_db_id,
            DatasetInfo.is_deleted == 0
        )
        result = await self.session.execute(stmt)
        ds = result.scalars().first()
        if not ds:
            return None
        return self._to_domain(ds)

    async def get_by_biz_id(self, biz_id: str) -> Optional[Dataset]:
        stmt = select(DatasetInfo).where(
            DatasetInfo.biz_id == biz_id,
            DatasetInfo.is_deleted == 0
        )
        result = await self.session.execute(stmt)
        ds = result.scalars().first()
        if not ds:
            return None
        return self._to_domain(ds)

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

        def apply_filters(query):
            query = query.where(
                DatasetInfo.project_id == project_db_id,
                DatasetInfo.is_deleted == 0
            )
            if dataset_name_like:
                query = query.where(
                    or_(
                        DatasetInfo.dataset_name.like(f"%{dataset_name_like}%"),
                        DatasetInfo.dataset_en_name.like(f"%{dataset_name_like}%")
                    )
                )
            if dataset_type:
                query = query.where(DatasetInfo.dataset_type == dataset_type)
            if media_type:
                query = query.where(DatasetInfo.media_type == media_type)
            return query

        # Count
        count_stmt = select(func.count(DatasetInfo.id))
        count_stmt = apply_filters(count_stmt)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar()

        # Data
        stmt = select(
            DatasetInfo,
            SysUser.username.label("creator_name")
        ).outerjoin(
            SysUser, DatasetInfo.create_user_id == SysUser.id
        )
        stmt = apply_filters(stmt)

        sort_col = getattr(DatasetInfo, order_by, DatasetInfo.id)
        if order_direction.lower() == "desc":
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))

        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        rows = result.all()

        items = []
        for ds, creator_name in rows:
            items.append(DatasetListItemDTO(
                id=ds.id,
                biz_id=ds.biz_id,
                dataset_id=ds.dataset_id,
                project_id=ds.project_id,
                dataset_name=ds.dataset_name,
                dataset_en_name=ds.dataset_en_name,
                dataset_path=ds.dataset_path,
                dataset_type=ds.dataset_type,
                media_type=ds.media_type,
                application_scenario=ds.application_scenario,
                is_data_update_open=ds.is_data_update_open,
                tags=ds.tags,
                description=ds.description,
                create_user_id=ds.create_user_id,
                creator_name=creator_name or f"User {ds.create_user_id}",
                create_time=ds.create_time,
                update_time=ds.update_time,
            ))
        return items, total

    def _to_domain(self, ds: DatasetInfo) -> Dataset:
        return Dataset(
            id=ds.id,
            biz_id=ds.biz_id,
            dataset_id=ds.dataset_id,
            project_id=ds.project_id,
            dataset_name=ds.dataset_name,
            dataset_en_name=ds.dataset_en_name,
            dataset_path=ds.dataset_path,
            dataset_type=ds.dataset_type,
            media_type=ds.media_type,
            application_scenario=ds.application_scenario,
            is_data_update_open=ds.is_data_update_open,
            related_dataset_id=ds.related_dataset_id,
            stat_level1_id=ds.stat_level1_id,
            stat_level2_id=ds.stat_level2_id,
            stat_level3_id=ds.stat_level3_id,
            tags=ds.tags,
            description=ds.description,
            schema_config=ds.schema_config,
            column_config=ds.column_config,
            visual_config=ds.visual_config,
            create_user_id=ds.create_user_id,
            is_deleted=ds.is_deleted,
        )
