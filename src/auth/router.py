from typing import Any
from fastapi import APIRouter, Depends, Form
from .schemas import Token, UserSchema
from .service import user_service
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

auth_router = APIRouter(prefix='/auth', tags=['JWT Auth'])


@auth_router.post('/login', response_model=Token)
async def login_for_access_token(
    username: str = Form(),
    password: str = Form()
) -> Any:
    token = await user_service.authenticate_user(username, password)
    return token


@auth_router.get('/users/me', response_model=UserSchema)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Any:
    user = await user_service.get_current_user(token)
    return user
