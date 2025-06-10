import httpx
from fastapi import Depends, HTTPException, Request, Security, security
from sqlalchemy.orm import Session


from app.database.accessor import get_db_session
from app.repository import TaskCache, TaskRepository
from app.service.task import TaskService
from cache.accessor import get_redis_connection
from app.repository.user import UserRepository
from app.service.user import UserService
from app.service.auth import AuthService
from app.settings import Settings
from app.exceptions import TokenExpired, TokenNotCorrect
from client.google_client import GoogleClient


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


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
    return TaskService(task_repository=task_repository, task_cache=task_cache)


def get_user_repository(
    db_session: Session = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
    )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)

    except TokenNotCorrect as e:
        raise HTTPException(status_code=401, detail=e.detail)

    return user_id


def delete_task(self, task_id: int, user_id: int) -> None:
    task = self.task_repository.get_task_by_id(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    self.task_repository.delete_task(task_id=task_id, user_id=user_id)
