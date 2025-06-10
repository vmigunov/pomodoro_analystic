from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.dependency import get_auth_service
from app.schema.user import UserCreateSchema, UserLoginSchema
from app.service.auth import AuthService
from app.exceptions import UserNotCorrectPasswordException, UserNotFoundException


router = APIRouter()


@router.post("/login", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/login/google")
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_google_redirect_url()
    return RedirectResponse(url=redirect_url)


@router.get("/auth/google", response_class=RedirectResponse)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    """Обработка callback от Google OAuth"""
    try:
        login_data = await auth_service.google_auth(code=code)
        return RedirectResponse(
            url=f"/?user_id={login_data.user_id}&token={login_data.access_token}"
        )
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Google authentication failed")


@router.get("/login/yandex")
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_yandex_redirect_url()
    return RedirectResponse(url=redirect_url)


@router.get("/auth/yandex", response_class=RedirectResponse)
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    try:
        login_data = await auth_service.yandex_auth(code=code)
        return RedirectResponse(
            url=f"/?user_id={login_data.user_id}&token={login_data.access_token}"
        )
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Google authentication failed")
