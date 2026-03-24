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

    # LDAP
    ldap_url: str = "ldap://10.234.46.20:389"
    ldap_base: str = "OU=Magna Group,DC=magna,DC=global"
    ldap_user_prefix: str = "magna\\"
    ldap_password: str = ""

    # Redis
    redis_host: str = "10.234.46.73"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # JWT
    jwt_expire_hours: int = 24
    jwt_redis_prefix: str = "mdcp:user:login"

    # Snowflake ID
    snowflake_worker_id: int = 1
    snowflake_datacenter_id: int = 1

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
