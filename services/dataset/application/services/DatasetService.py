import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from services.dataset.infrastructure.models import DataProject, SysUser
from services.dataset.application.schemas.project import ProjectCreateReq, ProjectInfoResp

class DatasetService:
    @staticmethod
    async def create_project(req: ProjectCreateReq, current_user: SysUser, db: AsyncSession) -> ProjectInfoResp:
        # Check if project name exists
        stmt = select(DataProject).where(
            (DataProject.project_name == req.project_name) | 
            (DataProject.project_en_name == req.project_en_name)
        )
        result = await db.execute(stmt)
        existing_project = result.scalars().first()
        if existing_project:
            if existing_project.project_name == req.project_name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name already exists")
            if existing_project.project_en_name == req.project_en_name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project English name already exists")

        # Generate a new project ID (UUID without dashes, or snowflake depending on system logic)
        new_project_id = uuid.uuid4().hex
        
        # Create new project DO
        new_project = DataProject(
            project_id=new_project_id,
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
            create_user_id=current_user.id
        )
        
        db.add(new_project)
        try:
            await db.commit()
            await db.refresh(new_project)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
            
        return ProjectInfoResp.model_validate(new_project)
