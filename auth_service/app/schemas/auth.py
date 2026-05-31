from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class LoginHistoryResponse(BaseModel):
    user_agent: str
    login_datetime: datetime

    class Config:
        from_attributes = True
