from fastapi import APIRouter
from app.handlers.ping import router as ping_router
from app.handlers.tasks import router as task_router
from app.handlers.user import router as user_router
from app.handlers.auth import router as auth_router

router = APIRouter()

router.include_router(ping_router, prefix="/ping", tags=["ping"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
