from fastapi import APIRouter
from app.settings import settings


router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/db")
async def ping_db():
    return {"message": "Database is working", "db_url": settings.db_url}


@router.get("/app")
async def ping_app():
    return {"text": "app is working"}
