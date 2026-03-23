from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.dependencies.database import get_db
from sqlalchemy import select
from typing import List, Optional
from services.dataset.infrastructure.models import SysUser
from services.dataset.domain.entities.project import Project, ProjectPermission
from services.dataset.domain.repositories.project_repository import ProjectRepository
from services.dataset.application.schemas.project import (
    ProjectListResp, ProjectUpdateReq, ProjectPermissionItem, 
    ProjectPermissionListResp, ProjectPermissionUpdateReq, ProjectInfoResp, ProjectCreateReq,
    ProjectListReq
)
from services.dataset.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl

def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepositoryImpl:
    return ProjectRepositoryImpl(db)

class ProjectApplicationService:
    def __init__(self, repo: ProjectRepository = Depends(get_project_repo), db: AsyncSession = Depends(get_db)):
        self.repo = repo
        self.db = db

    async def create_project(self, req: ProjectCreateReq, current_user_id: int) -> ProjectInfoResp:
        conflict = await self.repo.check_name_conflicts(req.project_name, req.project_en_name)
        if conflict == "name":
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Project name already exists")
        if conflict == "en_name":
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Project English name already exists")
        
        saved_project = await self.repo.create_project(req, current_user_id)
        return ProjectInfoResp.model_validate(saved_project)

    async def list_projects(self, req: ProjectListReq, user_id: int) -> ProjectListResp:
        items, total = await self.repo.list_projects(
            user_id, 
            req.page, 
            req.size,
            project_name_like=req.project_name_like,
            creator_name_like=req.creator_name_like,
            create_time_start=req.create_time_start,
            create_time_end=req.create_time_end,
            update_time_start=req.update_time_start,
            update_time_end=req.update_time_end,
            order_by=req.order_by,
            order_direction=req.order_direction
        )
        return ProjectListResp(total=total, items=items)

    async def update_project(self, project_id: str, req: ProjectUpdateReq) -> ProjectInfoResp:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Partial update logic
        update_data = req.model_dump(exclude_unset=True)
        
        # Categorize updates
        base_keys = {"project_name", "is_compliance_open"}
        storage_keys = {
            "is_share_storage", "storage_type", "storage_endpoint", 
            "bucket_name", "storage_dir", "write_ak", "write_sk", "read_ak", "read_sk"
        }
        
        base_updates = {k: v for k, v in update_data.items() if k in base_keys}
        storage_updates = {k: v for k, v in update_data.items() if k in storage_keys}
        
        # Mandatory fields that shouldn't be set to None (DB nullable=False)
        mandatory_fields = {
            "project_name", "storage_type", "storage_endpoint", 
            "bucket_name", "storage_dir", "is_compliance_open", "is_share_storage"
        }
        
        if base_updates:
            # Filter out None values for mandatory fields
            base_updates = {k: v for k, v in base_updates.items() if v is not None or k not in mandatory_fields}
            
            new_name = base_updates.pop("project_name", project.project_name)
            project.update_info(project_name=new_name, **base_updates)
            
        if storage_updates:
            # Filter out None values for mandatory fields
            storage_updates = {k: v for k, v in storage_updates.items() if v is not None or k not in mandatory_fields}
            
            is_empty = await self.repo.is_project_empty(project.id)
            try:
                project.update_storage(is_empty=is_empty, **storage_updates)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
                
        saved_project = await self.repo.save(project)
        return ProjectInfoResp.model_validate(saved_project)

    async def delete_project(self, project_id: str) -> None:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        try:
            await self.repo.delete(project)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_project_permissions(self, project_id: str) -> ProjectPermissionListResp:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        if not project.permissions:
            return ProjectPermissionListResp(items=[])
            
        # Fetch usernames
        user_ids = [p.user_id for p in project.permissions]
        stmt = select(SysUser.id, SysUser.username).where(SysUser.id.in_(user_ids))
        result = await self.db.execute(stmt)
        user_map = {row.id: row.username for row in result.all()}
        
        items = []
        for p in project.permissions:
            items.append(ProjectPermissionItem(
                user_id=p.user_id,
                username=user_map.get(p.user_id, "Unknown"),
                permission_type=p.permission_type
            ))
            
        return ProjectPermissionListResp(items=items)

    async def update_project_permissions(self, project_id: str, req: ProjectPermissionUpdateReq, grant_user_id: int) -> None:
        project = await self.repo.get_by_id(project_id)
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
        await self.repo.save(project)
