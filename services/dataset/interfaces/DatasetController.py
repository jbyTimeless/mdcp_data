from fastapi import APIRouter, Depends, HTTPException, Path
from common.dependencies.auth import get_current_user
from common.schemas.response import ResponseStructure, success, error
from services.dataset.infrastructure.models import SysUser
from services.dataset.application.schemas.dataset import (
    DatasetCreateReq, DatasetInfoResp,
    DatasetOverviewUpdateReq, DatasetSchemaUpdateReq,
    DatasetColumnUpdateReq, DatasetVisualUpdateReq
)
from services.dataset.application.services.DatasetApplicationService import DatasetApplicationService

router = APIRouter(prefix="/dataset", tags=["Dataset Management"])


@router.post("/create", response_model=ResponseStructure[DatasetInfoResp])
async def create_dataset(
    req: DatasetCreateReq,
    current_user: SysUser = Depends(get_current_user),
    service: DatasetApplicationService = Depends()
):
    """
    新建数据集接口
    - 校验用户对目标项目的 manage/edit 权限
    - 校验数据集名称在项目内唯一
    - 自动生成数据集存储路径
    - 支持关联统计树层级
    """
    try:
        dataset_info = await service.create_dataset(req=req, current_user_id=current_user.id)
        return success(data=dataset_info, msg="Dataset created successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to create dataset: {str(e)}")


@router.post("/{dataset_id}/overview", response_model=ResponseStructure[DatasetInfoResp])
async def update_dataset_overview(
    dataset_id: int = Path(..., description="数据集ID"),
    req: DatasetOverviewUpdateReq = ...,
    current_user: SysUser = Depends(get_current_user),
    service: DatasetApplicationService = Depends()
):
    """
    更新数据集概览描述
    - 包括数据来源、标注规则、使用方式等信息
    - 需用户有数据集编辑或管理权限
    """
    try:
        dataset_info = await service.update_dataset_overview(
            dataset_id=dataset_id,
            description=req.description,
            current_user_id=current_user.id
        )
        return success(data=dataset_info, msg="Dataset overview updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update dataset overview: {str(e)}")


@router.post("/{dataset_id}/schema", response_model=ResponseStructure[DatasetInfoResp])
async def update_dataset_schema(
    dataset_id: int = Path(..., description="数据集ID"),
    req: DatasetSchemaUpdateReq = ...,
    current_user: SysUser = Depends(get_current_user),
    service: DatasetApplicationService = Depends()
):
    """
    更新数据集数据结构配置
    - 采用JSON格式，符合Elasticsearch 7 mapping定义
    - 自动校验保留字段`_doc_type`和`datasetsRelatedFiles`不能被占用
    - 字段类型确定后不可变更，但可新增字段
    - 需用户有数据集编辑或管理权限
    """
    try:
        dataset_info = await service.update_dataset_schema(
            dataset_id=dataset_id,
            schema_config=req.schema_config,
            current_user_id=current_user.id
        )
        return success(data=dataset_info, msg="Dataset schema updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update dataset schema: {str(e)}")


@router.post("/{dataset_id}/column-config", response_model=ResponseStructure[DatasetInfoResp])
async def update_dataset_column_config(
    dataset_id: int = Path(..., description="数据集ID"),
    req: DatasetColumnUpdateReq = ...,
    current_user: SysUser = Depends(get_current_user),
    service: DatasetApplicationService = Depends()
):
    """
    更新数据集数据列配置
    - 配置数据集下数据列表展示的列信息
    - 当前只支持JSON数据一层属性，不支持嵌套属性
    - 需用户有数据集编辑或管理权限
    """
    try:
        dataset_info = await service.update_dataset_column_config(
            dataset_id=dataset_id,
            column_config=req.column_config,
            current_user_id=current_user.id
        )
        return success(data=dataset_info, msg="Dataset column config updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update dataset column config: {str(e)}")


@router.post("/{dataset_id}/visual-config", response_model=ResponseStructure[DatasetInfoResp])
async def update_dataset_visual_config(
    dataset_id: int = Path(..., description="数据集ID"),
    req: DatasetVisualUpdateReq = ...,
    current_user: SysUser = Depends(get_current_user),
    service: DatasetApplicationService = Depends()
):
    """
    更新数据集可视化信息配置
    - 支持图片点线框、点云框、视频可视化配置效果
    - 需用户有数据集编辑或管理权限
    """
    try:
        dataset_info = await service.update_dataset_visual_config(
            dataset_id=dataset_id,
            visual_config=req.visual_config,
            current_user_id=current_user.id
        )
        return success(data=dataset_info, msg="Dataset visual config updated successfully")
    except HTTPException as e:
        return error(msg=e.detail, code=e.status_code)
    except Exception as e:
        return error(msg=f"Failed to update dataset visual config: {str(e)}")
