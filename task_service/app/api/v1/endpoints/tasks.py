from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.dependencies import get_current_user_id
from app.db.database import get_session
from app.models.models import TaskStatus, TaskPriority
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    data: TaskCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TaskService(session)
    return service.create_task(data, user_id)


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TaskService(session)
    return service.get_all_tasks(user_id, status, priority)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TaskService(session)
    return service.get_task(task_id, user_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TaskService(session)
    return service.update_task(task_id, user_id, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    service = TaskService(session)
    service.delete_task(task_id, user_id)
