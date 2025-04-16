from fastapi import Depends


from app.database.database import get_db_session
from app.repository import TaskCache, TaskRepository
from app.service.task import TaskService
from cache.accessor import get_redis_connection


def get_tasks_repository():
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_tasks_cahce_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_tasks_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache: TaskCache = Depends(get_tasks_cahce_repository),
) -> TaskService:
    return TaskService(
        task_repository=get_tasks_repository(), task_cache=get_tasks_cahce_repository()
    )
