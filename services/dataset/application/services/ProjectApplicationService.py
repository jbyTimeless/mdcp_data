from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, in_
from fastapi import HTTPException, status
from typing import List
from services.dataset.infrastructure.models import SysUser
from services.dataset.domain.entities.project import Project, ProjectPermission
from services.dataset.domain.repositories.project_repository import ProjectRepository
from services.dataset.application.schemas.project import (
    ProjectListResp, ProjectUpdateReq, ProjectPermissionItem, 
    ProjectPermissionListResp, ProjectPermissionUpdateReq, ProjectInfoResp
)
from services.dataset.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl

class ProjectApplicationService:

    @staticmethod
    async def create_project(req: 'ProjectCreateReq', current_user_id: int, repo: ProjectRepository) -> 'ProjectInfoResp':
        conflict = await repo.check_name_conflicts(req.project_name, req.project_en_name)
        if conflict == "name":
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Project name already exists")
        if conflict == "en_name":
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Project English name already exists")
        
        return await repo.create_project(req, current_user_id)  








    @staticmethod
    async def list_projects(user_id: int, page: int, size: int, repo: ProjectRepository) -> ProjectListResp:
        items, total = await repo.list_projects(user_id, page, size)
        return ProjectListResp(total=total, items=items)

    @staticmethod
    async def update_project(project_id: str, req: ProjectUpdateReq, repo: ProjectRepository) -> ProjectInfoResp:
        project = await repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        # Update info and storage
        project.update_info(project_name=req.project_name)
        
        # We need to check if we can update storage
        is_empty = await repo.is_project_empty(project.id)
        try:
            project.update_storage(
                is_empty=is_empty,
                is_compliance_open=req.is_compliance_open,
                is_share_storage=req.is_share_storage,
                storage_type=req.storage_type,
                storage_endpoint=req.storage_endpoint,
                bucket_name=req.bucket_name,
                storage_dir=req.storage_dir,
                write_ak=req.write_ak,
                write_sk=req.write_sk,
                read_ak=req.read_ak,
                read_sk=req.read_sk
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            
        # Save changes
        saved_project = await repo.save(project)
        return ProjectInfoResp.model_validate(saved_project)

    @staticmethod
    async def delete_project(project_id: str, repo: ProjectRepository) -> None:
        project = await repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        try:
            await repo.delete(project)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def get_project_permissions(project_id: str, repo: ProjectRepository, db: AsyncSession) -> ProjectPermissionListResp:
        project = await repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        if not project.permissions:
            return ProjectPermissionListResp(items=[])
            
        # Fetch usernames
        user_ids = [p.user_id for p in project.permissions]
        stmt = select(SysUser.id, SysUser.username).where(SysUser.id.in_(user_ids))
        result = await db.execute(stmt)
        user_map = {row.id: row.username for row in result.all()}
        
        items = []
        for p in project.permissions:
            items.append(ProjectPermissionItem(
                user_id=p.user_id,
                username=user_map.get(p.user_id, "Unknown"),
                permission_type=p.permission_type
            ))
            
        return ProjectPermissionListResp(items=items)

    @staticmethod
    async def update_project_permissions(project_id: str, req: ProjectPermissionUpdateReq, grant_user_id: int, repo: ProjectRepository) -> None:
        project = await repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        new_permissions = [
            ProjectPermission(
                user_id=p.user_id,
                permission_type=p.permission_type,
                grant_user_id=grant_user_id
            ) for p in req.permissions
        ]
        
        project.update_permissions(new_permissions)
        await repo.save(project)
