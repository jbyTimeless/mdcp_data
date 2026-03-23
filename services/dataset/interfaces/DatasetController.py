from fastapi import APIRouter, Depends, HTTPException
from common.dependencies.auth import get_current_user
from common.schemas.response import ResponseStructure, success, error
from services.dataset.infrastructure.models import SysUser
from services.dataset.application.schemas.dataset import DatasetCreateReq, DatasetInfoResp
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
