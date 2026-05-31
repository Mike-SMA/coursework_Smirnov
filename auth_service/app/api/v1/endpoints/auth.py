from typing import List
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from app.core.dependencies import get_current_user
from app.db.database import get_session
from app.db.redis_client import get_redis
from app.models.models import User
from app.schemas.auth import (
    RegisterRequest, LoginRequest, RefreshRequest,
    UpdateUserRequest, TokenResponse, UserResponse, LoginHistoryResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])
bearer = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    service = AuthService(session)
    return service.register(data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, session: Session = Depends(get_session), redis=Depends(get_redis)):
    service = AuthService(session, redis)
    user_agent = request.headers.get("user-agent", "unknown")
    tokens = service.login(data, user_agent)
    return TokenResponse(**tokens)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, session: Session = Depends(get_session)):
    service = AuthService(session)
    tokens = service.refresh(data.refresh_token)
    return TokenResponse(**tokens)


@router.put("/user/update", response_model=UserResponse)
def update_user(
    data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    service = AuthService(session)
    return service.update_user(current_user, data)


@router.get("/user/history", response_model=List[LoginHistoryResponse])
def get_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    service = AuthService(session)
    history = service.get_login_history(current_user)
    return [{"user_agent": h.user_agent, "login_datetime": h.login_datetime} for h in history]


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    redis=Depends(get_redis),
):
    service = AuthService(session, redis)
    service.logout(credentials.credentials)
    return {"detail": "Выход выполнен"}
