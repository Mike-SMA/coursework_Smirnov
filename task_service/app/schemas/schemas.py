from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel
from app.models.models import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    deadline: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    deadline: Optional[date]
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
