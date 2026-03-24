from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """用户领域实体"""
    id: Optional[int] = None
    user_id: Optional[str] = None
    account: Optional[str] = None
    username: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    role_code: Optional[str] = None
    email: Optional[str] = None
    status: int = 1
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    is_deleted: int = 0

    def is_enabled(self) -> bool:
        """检查用户是否启用"""
        return self.status == 1 and self.is_deleted == 0
    
    def reset_credentials(self, access_key: str, secret_key: str):
        """重置用户凭证"""
        self.access_key = access_key
        self.secret_key = secret_key