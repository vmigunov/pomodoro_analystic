from typing import Annotated

from fastapi import APIRouter, status, Depends

from app.schema.task import Task
from app.repository.task import TaskRepository
from app.handlers.dependecy import get_tasks_repository


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all", response_model=list[Task])
async def get_tasks(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    tasks = task_repository.get_tasks()
    return tasks


@router.post("/", response_model=Task)
async def create_task(
    task: Task,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task


@router.post("/task/{task_id}")
async def task_id(task_id: int):
    return task_id


@router.patch("/{task_id}", response_model=Task)
async def patch_task(
    task_id: int,
    name: str,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    return task_repository.update_task_name(task_id, name)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    task_repository.delete_task(task_id)
    return {"message": "task deleted seccuessfully"}
