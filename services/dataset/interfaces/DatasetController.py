from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.dependencies.database import get_db
from common.dependencies.auth import get_current_user
from common.schemas.response import ResponseStructure, success, error
from services.dataset.infrastructure.models import SysUser
from services.dataset.application.schemas.project import ProjectCreateReq, ProjectInfoResp
from services.dataset.application.services.DatasetService import DatasetService

router = APIRouter(prefix="/project", tags=["Data Project"])

@router.post("/create", response_model=ResponseStructure[ProjectInfoResp])
async def create_data_project(
    req: ProjectCreateReq,
    current_user: SysUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    新建项目接口
    """
    try:
        project_info = await DatasetService.create_project(req=req, current_user=current_user, db=db)
        return success(data=project_info, msg="Project created successfully")
    except Exception as e:
        # In a real app we might handle specific HTTPExceptions thrown by the service
        # to return standard ErrorResponses with different codes.
        if hasattr(e, "status_code") and getattr(e, "status_code") < 500:
            return error(msg=str(getattr(e, "detail", str(e))), code=getattr(e, "status_code"))
        return error(msg=f"Failed to create project: {str(e)}")
