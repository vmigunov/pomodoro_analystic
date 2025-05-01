from fastapi import Depends
from sqlalchemy.orm import Session


from app.database.accessor import get_db_session
from app.repository import TaskCache, TaskRepository
from app.service.task import TaskService
from cache.accessor import get_redis_connection
from app.repository.user import UserRepository
from app.service.user import UserService


def get_tasks_repository(
    db_session: Session = Depends(get_db_session),
) -> TaskRepository:
    return TaskRepository(db_session=db_session)


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


def get_user_repository(
    db_session: Session = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repository)
