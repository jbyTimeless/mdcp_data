import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    project_name: str = "FastAPI Backend"
    
    # MySQL
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int
    mysql_db: str

    # MinIO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool

    # Elasticsearch
    es_host: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
