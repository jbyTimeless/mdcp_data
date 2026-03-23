from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.dependencies.database import get_db
from common.dependencies.auth import get_current_user
from common.schemas.response import ResponseStructure, success, error
from services.dataset.infrastructure.models import SysUser
from services.dataset.application.schemas.project import (
    ProjectCreateReq, ProjectInfoResp, ProjectListResp, ProjectUpdateReq,
    ProjectPermissionListResp, ProjectPermissionUpdateReq
)
from services.dataset.application.services.ProjectApplicationService import ProjectApplicationService
from services.dataset.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from fastapi import Query

def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepositoryImpl:
    return ProjectRepositoryImpl(db)

router = APIRouter(prefix="/project", tags=["Data Project"])


@router.post("/create", response_model=ResponseStructure[ProjectInfoResp])
async def create_data_project(
    req: ProjectCreateReq,
    current_user: SysUser = Depends(get_current_user),
    repo: ProjectRepositoryImpl = Depends(get_project_repo)
):
    """
    新建项目接口
    """
    try:
        project_info = await ProjectApplicationService.create_project(req=req, current_user_id=current_user.id, repo=repo)
        return success(data=project_info, msg="Project created successfully")
    except Exception as e:
        # In a real app we might handle specific HTTPExceptions thrown by the service
        # to return standard ErrorResponses with different codes.
        if hasattr(e, "status_code") and getattr(e, "status_code") < 500:
            return error(msg=str(getattr(e, "detail", str(e))), code=getattr(e, "status_code"))
        return error(msg=f"Failed to create project: {str(e)}")

@router.get("/list", response_model=ResponseStructure[ProjectListResp])
async def list_projects(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: SysUser = Depends(get_current_user),
    repo: ProjectRepositoryImpl = Depends(get_project_repo)
):
    """获取项目列表（分页）"""
    try:
        resp_data = await ProjectApplicationService.list_projects(
            user_id=current_user.id, page=page, size=size, repo=repo
        )
        return success(data=resp_data, msg="Success")
    except Exception as e:
        return error(msg=f"Failed to list projects: {str(e)}")

@router.put("/{project_id}", response_model=ResponseStructure[ProjectInfoResp])
async def update_project(
    project_id: str,
    req: ProjectUpdateReq,
    current_user: SysUser = Depends(get_current_user),
    repo: ProjectRepositoryImpl = Depends(get_project_repo)
):
    """更新项目信息与存储配置（存储配置仅在项目为空时可修改）"""
    try:
        resp_data = await ProjectApplicationService.update_project(project_id, req, repo)
        return success(data=resp_data, msg="Project updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update project: {str(e)}")

@router.delete("/{project_id}", response_model=ResponseStructure)
async def delete_project(
    project_id: str,
    current_user: SysUser = Depends(get_current_user),
    repo: ProjectRepositoryImpl = Depends(get_project_repo)
):
    """删除项目（仅当项目下无可用数据集时可删除）"""
    try:
        await ProjectApplicationService.delete_project(project_id, repo)
        return success(msg="Project deleted successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to delete project: {str(e)}")

@router.get("/{project_id}/permissions", response_model=ResponseStructure[ProjectPermissionListResp])
async def get_project_permissions(
    project_id: str,
    current_user: SysUser = Depends(get_current_user),
    repo: ProjectRepositoryImpl = Depends(get_project_repo),
    db: AsyncSession = Depends(get_db)
):
    """获取项目权限列表"""
    try:
        resp_data = await ProjectApplicationService.get_project_permissions(project_id, repo, db)
        return success(data=resp_data, msg="Success")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to get project permissions: {str(e)}")

@router.post("/{project_id}/permissions", response_model=ResponseStructure)
async def update_project_permissions(
    project_id: str,
    req: ProjectPermissionUpdateReq,
    current_user: SysUser = Depends(get_current_user),
    repo: ProjectRepositoryImpl = Depends(get_project_repo)
):
    """更新项目权限（全量替换）"""
    try:
        await ProjectApplicationService.update_project_permissions(project_id, req, current_user.id, repo)
        return success(msg="Project permissions updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update project permissions: {str(e)}")
