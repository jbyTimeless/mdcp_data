import uuid
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from services.dataset.domain.entities.project import Project, ProjectPermission
from services.dataset.domain.repositories.project_repository import ProjectRepository, ProjectListItemDTO
from services.dataset.infrastructure.models import DataProject, DatasetPermission, DatasetInfo, SysUser
from services.dataset.application.schemas.project import ProjectInfoResp

class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_project(self, req: 'ProjectCreateReq', current_user_id: int) -> 'ProjectInfoResp':
        project = Project(
            project_id=uuid.uuid4().hex,
            project_name=req.project_name,
            project_en_name=req.project_en_name,
            is_compliance_open=req.is_compliance_open,
            is_share_storage=req.is_share_storage,
            storage_type=req.storage_type,
            storage_endpoint=req.storage_endpoint,
            bucket_name=req.bucket_name,
            storage_dir=req.storage_dir,
            write_ak=req.write_ak,
            write_sk=req.write_sk,
            read_ak=req.read_ak,
            read_sk=req.read_sk,
            create_user_id=current_user_id
        )
        
        saved_project = await self.save(project)
        return ProjectInfoResp.model_validate(saved_project)

    async def get_by_id(self, project_id: str) -> Optional[Project]:
        stmt = select(DataProject).where(DataProject.project_id == project_id, DataProject.is_deleted == 0)
        result = await self.session.execute(stmt)
        data_project = result.scalars().first()
        if not data_project:
            return None
            
        # Get permissions
        perm_stmt = select(DatasetPermission).where(
            DatasetPermission.resource_type == 'project',
            DatasetPermission.resource_id == data_project.id,
            DatasetPermission.status == 1
        )
        perm_result = await self.session.execute(perm_stmt)
        permissions_db = perm_result.scalars().all()
        
        permissions = [
            ProjectPermission(
                user_id=p.user_id,
                permission_type=p.permission_type,
                grant_user_id=p.grant_user_id
            ) for p in permissions_db
        ]

        return Project(
            id=data_project.id,
            project_id=data_project.project_id,
            project_name=data_project.project_name,
            project_en_name=data_project.project_en_name,
            is_compliance_open=data_project.is_compliance_open,
            is_share_storage=data_project.is_share_storage,
            storage_type=data_project.storage_type,
            storage_endpoint=data_project.storage_endpoint,
            bucket_name=data_project.bucket_name,
            storage_dir=data_project.storage_dir,
            write_ak=data_project.write_ak,
            write_sk=data_project.write_sk,
            read_ak=data_project.read_ak,
            read_sk=data_project.read_sk,
            create_user_id=data_project.create_user_id,
            is_deleted=data_project.is_deleted,
            permissions=permissions
        )

    async def save(self, project: Project) -> Project:
        if project.id is None:
            # Create
            new_project = DataProject(
                project_id=project.project_id,
                project_name=project.project_name,
                project_en_name=project.project_en_name,
                is_compliance_open=project.is_compliance_open,
                is_share_storage=project.is_share_storage,
                storage_type=project.storage_type,
                storage_endpoint=project.storage_endpoint,
                bucket_name=project.bucket_name,
                storage_dir=project.storage_dir,
                write_ak=project.write_ak,
                write_sk=project.write_sk,
                read_ak=project.read_ak,
                read_sk=project.read_sk,
                create_user_id=project.create_user_id
            )
            self.session.add(new_project)
            await self.session.flush()
            project.id = new_project.id
        else:
            # Update base info
            stmt = select(DataProject).where(DataProject.id == project.id)
            result = await self.session.execute(stmt)
            data_project = result.scalars().first()
            if data_project:
                data_project.project_name = project.project_name
                data_project.is_compliance_open = project.is_compliance_open
                data_project.is_share_storage = project.is_share_storage
                data_project.storage_type = project.storage_type
                data_project.storage_endpoint = project.storage_endpoint
                data_project.bucket_name = project.bucket_name
                data_project.storage_dir = project.storage_dir
                data_project.write_ak = project.write_ak
                data_project.write_sk = project.write_sk
                data_project.read_ak = project.read_ak
                data_project.read_sk = project.read_sk
                data_project.is_deleted = project.is_deleted

        # Handle permissions (Delete all and re-insert for simplicity)
        if project.id:
            del_stmt = delete(DatasetPermission).where(
                DatasetPermission.resource_type == 'project',
                DatasetPermission.resource_id == project.id
            )
            await self.session.execute(del_stmt)
            
            for p in project.permissions:
                new_perm = DatasetPermission(
                    biz_id=uuid.uuid4().hex,
                    permission_id=0, # or some snowflake ID logic
                    resource_type='project',
                    resource_id=project.id,
                    user_id=p.user_id,
                    permission_type=p.permission_type,
                    grant_user_id=p.grant_user_id,
                    status=1
                )
                self.session.add(new_perm)

        await self.session.commit()
        return project

    async def delete(self, project: Project) -> None:
        project.delete(await self.is_project_empty(project.id))
        await self.save(project)

    async def check_name_conflicts(self, project_name: str, project_en_name: str) -> Optional[str]:
        stmt = select(DataProject).where(
            (DataProject.project_name == project_name) | 
            (DataProject.project_en_name == project_en_name),
            DataProject.is_deleted == 0
        )
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            if existing.project_name == project_name:
                return "name"
            if existing.project_en_name == project_en_name:
                return "en_name"
        return None

    async def is_project_empty(self, project_db_id: int) -> bool:
        stmt = select(func.count(DatasetInfo.id)).where(
            DatasetInfo.project_id == project_db_id,
            DatasetInfo.is_deleted == 0
        )
        result = await self.session.execute(stmt)
        return result.scalar() == 0

    async def list_projects(self, user_id: int, page: int, size: int) -> Tuple[List[ProjectListItemDTO], int]:
        # Count query
        count_stmt = select(func.count(DataProject.id)).where(DataProject.is_deleted == 0)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar()

        # Join SysUser for creator_name (Outer join just in case creator is missing in dummy DB)
        # Outer join DatasetPermission for user's permission
        stmt = select(
            DataProject,
            SysUser.username.label("creator_name"),
            DatasetPermission.permission_type.label("my_permission")
        ).outerjoin(
            SysUser, DataProject.create_user_id == SysUser.id
        ).outerjoin(
            DatasetPermission,
            (DatasetPermission.resource_type == 'project') &
            (DatasetPermission.resource_id == DataProject.id) &
            (DatasetPermission.user_id == user_id) &
            (DatasetPermission.status == 1)
        ).where(DataProject.is_deleted == 0) \
         .order_by(DataProject.create_time.desc()) \
         .offset((page - 1) * size) \
         .limit(size)
         
        result = await self.session.execute(stmt)
        rows = result.all()
        
        items = []
        for dp, creator_name, my_perm in rows:
            # Fallback for creator name if not in DB
            eff_creator_name = creator_name if creator_name else f"User {dp.create_user_id}"
            eff_perm = 'manage' if dp.create_user_id == user_id else my_perm
            
            items.append(ProjectListItemDTO(
                id=dp.id,
                project_id=dp.project_id,
                project_name=dp.project_name,
                project_en_name=dp.project_en_name,
                creator_name=eff_creator_name,
                my_permission=eff_perm
            ))
            
        return items, total
