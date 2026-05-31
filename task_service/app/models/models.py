from typing import Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    deadline: Optional[date] = None
    user_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
