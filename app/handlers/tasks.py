from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.repository.cache_task import TaskCache
from app.schema.task import Task, TaskCreateSchema
from app.repository.task import TaskRepository
from app.service.task import TaskService
from app.dependency import (
    get_tasks_repository,
    get_request_user_id,
    get_tasks_service,
)
from app.exceptions import TaskNotFound


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all", response_model=list[Task])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_tasks_service)]):
    return task_service.get_tasks()


@router.post("/", response_model=Task)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = task_service.create_task(body, user_id)
    return task


@router.post("/task/{task_id}")
async def task_id(task_id: int):
    return task_id


@router.patch("/{task_id}", response_model=Task)
async def patch_task(
    task_id: int,
    name: str,
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return task_service.update_task_name(
            task_id=task_id, name=name, user_id=user_id
        )
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    task_service.delete_task(task_id=task_id, user_id=user_id)
