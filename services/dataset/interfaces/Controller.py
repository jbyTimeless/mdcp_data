from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from common.dependencies.database import get_db
from common.dependencies.minio_client import minio_client
from common.dependencies.es_client import es_client
from services.dataset.interfaces.DatasetController import router as dataset_router

router = APIRouter()
router.include_router(dataset_router)
@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    status = {"status": "ok", "db": "unknown", "minio": "unknown", "es": "unknown"}
    
    # Check DB
    try:
        await db.execute(text("SELECT 1"))
        status["db"] = "connected"
    except Exception as e:
        status["db"] = f"error: {str(e)}"
    
    # Check MinIO
    try:
        # Just calling list_buckets to verify connection
        minio_client.list_buckets()
        status["minio"] = "connected"
    except Exception as e:
        status["minio"] = f"error: {str(e)}"

    # Check ES
    try:
        await es_client.info()
        status["es"] = "connected"
    except Exception as e:
        status["es"] = f"error: {str(e)}"

    return status
@router.get("/hello")
def hello():
    return {"message": "Hello World"}