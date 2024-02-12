from typing import Any
from fastapi import APIRouter, Depends, Form, Header, Response
from fastapi.responses import JSONResponse

from .models import User
from .schemas import Token, UserSchema, UserCreate
from .service import user_service, auth_service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

auth_router = APIRouter(prefix='/auth', tags=['JWT Auth'])
user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/signup', response_model=UserSchema)
async def signup(user_data: UserCreate) -> Any:
    user = await user_service.register_new_user(user_data)
    return user


@auth_router.post('/login', response_model=Token)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends()
) -> Any:
    token = await auth_service.login(credentials.username, credentials.password)
    return token


@auth_router.post('/refresh', response_model=Token)
async def refresh_token(refresh_token: str = Header()):
    token = await auth_service.refresh_token(refresh_token)
    return token


@user_router.get('/me', response_model=UserSchema)
async def get_current_user(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    return user


@user_router.post('/change_password', response_model=UserSchema)
async def change_password(
    user: User = Depends(user_service.get_current_user),
    old_password: str = Form(),
    new_password: str = Form()
) -> Any:
    user = await user_service.change_password(user, old_password, new_password)
    return user


@auth_router.post('/logout')
async def logout(user: UserSchema = Depends(user_service.get_current_user)) -> JSONResponse:
    await auth_service.logout(user)
    return {
        'message': 'successful logout'
    }