from fastapi import APIRouter, status

from app.database.database import get_db_session
from app.fixtures import tasks as fixture_tasks
from app.schema.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all", response_model=list[Task])
async def get_tasks():
    result: list[Task] = []
    cursor = get_db_connection().cursor()
    tasks = cursor.execute("SELECT * FROM Tasks").fetchall()
    for task in tasks:
        result.append(Task(
            id=task[0],
            name=task[1],
            pomodoro_count=task[2],
            category_id=task[3]
        ))
    return result


@router.post("/", response_model=Task)
async def create_task(task: Task):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tasks (name, pomodoro_count, category_id) VALUES (?,?,?)",
                   (task.name, task.pomodoro_count, task.category_id))
    connection.commit()
    connection.close()
    
    return task


@router.post("/task/{task_id}")
async def task_id(task_id: int):
    return task_id


@router.patch("/{task_id}")
async def patch_task(task_id: int, name: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Tasks SET name =? WHERE id =?", (name, task_id))
    connection.commit()
    task = cursor.execute("SELECT * FROM Tasks WHERE id =?", f"{task_id}").fetchall()[0]
    connection.close()

    return Task(
            id=task[0],
            name=task[1],
            pomodoro_count=task[2],
            category_id=task[3]
        )


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id =?", (task_id, ))
    connection.close()
    return {"message": "task deleted successfuly"}
