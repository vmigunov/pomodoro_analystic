from fastapi import APIRouter, status
from fixtures import tasks as fixture_tasks
from schema.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all", response_model=list[Task])
async def get_tasks():
    return fixture_tasks


@router.get("/tasks")
async def get_tasks():
    return []


@router.post("/", response_model=Task)
async def create_task(task: Task):
    fixture_tasks.append(task)
    return task


@router.post("/task/{task_id}")
async def task_id(task_id: int):
    return task_id


@router.patch("/{task_id}")
async def patch_task(task_id: int, name: str):
    for task in fixture_tasks:
        if task["id"] == task_id:
            task["name"] = name
            return task


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(fixture_tasks):
        if task["id"] == task_id:
            del fixture_tasks[index]
            return {"message": f"Task, id:{task_id} deleted"}
    return {"message": "task not found"}
