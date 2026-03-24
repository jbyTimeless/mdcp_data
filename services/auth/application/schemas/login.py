from pydantic import BaseModel, EmailStr
from datetime import datetime

class LoginRequest(BaseModel):
    """登录请求DTO"""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """登录响应DTO"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user_info: dict

class UserInfoDTO(BaseModel):
    """用户信息DTO"""
    user_id: str
    account: str
    username: str
    email: str
    role_code: str
    access_key: str