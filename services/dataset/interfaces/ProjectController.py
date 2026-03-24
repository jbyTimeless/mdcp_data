from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from common.dependencies.auth import get_current_user
from common.schemas.response import ResponseStructure, success, error
from services.dataset.infrastructure.models import SysUser
from services.dataset.application.schemas.project import (
    ProjectCreateReq, ProjectInfoResp, ProjectListResp, ProjectUpdateReq,
    ProjectPermissionListResp, ProjectPermissionUpdateReq, ProjectListReq
)
from services.dataset.application.services.ProjectApplicationService import ProjectApplicationService

router = APIRouter(prefix="/project", tags=["Data Project"])


@router.post("/create", response_model=ResponseStructure[ProjectInfoResp])
async def create_data_project(
    req: ProjectCreateReq,
    current_user: SysUser = Depends(get_current_user),
    service: ProjectApplicationService = Depends()
):
    """
    新建项目接口
    """
    try:
        project_info = await service.create_project(req=req, current_user_id=str(current_user.id))
        return success(data=project_info, msg="Project created successfully")
    except Exception as e:
        if hasattr(e, "status_code") and getattr(e, "status_code") < 500:
            return error(msg=str(getattr(e, "detail", str(e))), code=getattr(e, "status_code"))
        return error(msg=f"Failed to create project: {str(e)}")

@router.post("/list", response_model=ResponseStructure[ProjectListResp])
async def list_projects(
    req: ProjectListReq,
    current_user: SysUser = Depends(get_current_user),
    service: ProjectApplicationService = Depends()
):
    """获取项目列表（分页、过滤、排序 - 支持POST Body）"""
    try:
        resp_data = await service.list_projects(req, str(current_user.id))
        return success(data=resp_data, msg="Success")
    except Exception as e:
        return error(msg=f"Failed to list projects: {str(e)}")

@router.put("/{project_id}", response_model=ResponseStructure[ProjectInfoResp])
async def update_project(
    project_id: str,
    req: ProjectUpdateReq,
    current_user: SysUser = Depends(get_current_user),
    service: ProjectApplicationService = Depends()
):
    """更新项目信息与存储配置（存储配置仅在项目为空时可修改）"""
    try:
        resp_data = await service.update_project(project_id, req)
        return success(data=resp_data, msg="Project updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update project: {str(e)}")

@router.delete("/{project_id}", response_model=ResponseStructure)
async def delete_project(
    project_id: str,
    current_user: SysUser = Depends(get_current_user),
    service: ProjectApplicationService = Depends()
):
    """删除项目（仅当项目下无可用数据集时可删除）"""
    try:
        await service.delete_project(project_id)
        return success(msg="Project deleted successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to delete project: {str(e)}")

@router.get("/{project_id}/permissions", response_model=ResponseStructure[ProjectPermissionListResp])
async def get_project_permissions(
    project_id: str,
    current_user: SysUser = Depends(get_current_user),
    service: ProjectApplicationService = Depends()
):
    """获取项目权限列表"""
    try:
        resp_data = await service.get_project_permissions(project_id)
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
    service: ProjectApplicationService = Depends()
):
    """更新项目权限（全量替换）"""
    try:
        await service.update_project_permissions(project_id, req, current_user.user_id)
        return success(msg="Project permissions updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update project permissions: {str(e)}")
