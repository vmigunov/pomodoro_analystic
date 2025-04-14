from fastapi import APIRouter
from app.handlers.ping import router as ping_router
from app.handlers.tasks import router as task_router

router = APIRouter()

router.include_router(ping_router, prefix="/ping", tags=["ping"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])
