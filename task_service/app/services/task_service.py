from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.models import Task, TaskStatus, TaskPriority
from app.schemas.schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, data: TaskCreate, user_id: int) -> Task:
        task = Task(**data.model_dump(), user_id=user_id)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task(self, task_id: int, user_id: int) -> Task:
        task = self.session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Доступ запрещён")
        return task

    def get_all_tasks(
        self,
        user_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        query = select(Task).where(Task.user_id == user_id)
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        return list(self.session.exec(query).all())

    def update_task(self, task_id: int, user_id: int, data: TaskUpdate) -> Task:
        task = self.get_task(task_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.get_task(task_id, user_id)
        self.session.delete(task)
        self.session.commit()
