from typing import Any
from fastapi import APIRouter, Depends, Form, Header, Response
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


@user_router.get('/users/me', response_model=UserSchema)
async def get_current_user(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    return user
