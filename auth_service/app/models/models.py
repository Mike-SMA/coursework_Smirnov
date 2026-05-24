from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str

    login_history: List["LoginHistory"] = Relationship(back_populates="user")


class LoginHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user_agent: str
    login_datetime: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="login_history")
