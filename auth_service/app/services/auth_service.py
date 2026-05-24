from typing import List
from datetime import datetime
from sqlmodel import Session, select
from app.models.models import User, LoginHistory
from app.schemas.auth import RegisterRequest, LoginRequest, UpdateUserRequest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from fastapi import HTTPException


class AuthService:
    def __init__(self, session: Session, redis=None):
        self.session = session
        self.redis = redis

    def register(self, data: RegisterRequest) -> User:
        existing = self.session.exec(select(User).where(User.email == data.email)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        user = User(email=data.email, hashed_password=hash_password(data.password))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def login(self, data: LoginRequest, user_agent: str) -> dict:
        user = self.session.exec(select(User).where(User.email == data.email)).first()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный email или пароль")
        history = LoginHistory(user_id=user.id, user_agent=user_agent, login_datetime=datetime.utcnow())
        self.session.add(history)
        self.session.commit()
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Невалидный refresh токен")
        access_token = create_access_token({"sub": payload.get("sub")})
        new_refresh = create_refresh_token({"sub": payload.get("sub")})
        return {"access_token": access_token, "refresh_token": new_refresh}

    def update_user(self, user: User, data: UpdateUserRequest) -> User:
        if data.email:
            user.email = data.email
        if data.password:
            user.hashed_password = hash_password(data.password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_login_history(self, user: User) -> List[LoginHistory]:
        return list(self.session.exec(select(LoginHistory).where(LoginHistory.user_id == user.id)).all())

    def logout(self, token: str) -> None:
        if self.redis:
            payload = decode_token(token)
            if payload and "exp" in payload:
                import time
                ttl = int(payload["exp"] - time.time())
                if ttl > 0:
                    self.redis.setex(f"blacklist:{token}", ttl, "1")
