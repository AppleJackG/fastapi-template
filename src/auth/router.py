from typing import Annotated, Any
from uuid import UUID
from fastapi import APIRouter, Depends, Form, Header, Response
from fastapi.responses import JSONResponse

from .models import User
from .schemas import Token, UserPatch, UserSchema, UserCreate, UserUpdate
from .service import user_service, auth_service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

auth_router = APIRouter(prefix='/auth', tags=['JWT Auth'])
user_router = APIRouter(prefix='/users', tags=['Users'])
superuser_router = APIRouter(prefix='/superuser', tags=['Super user actions'])


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


@auth_router.post('/logout')
async def logout(user: UserSchema = Depends(user_service.get_current_user)) -> JSONResponse:
    await auth_service.logout(user)
    return {
        'message': 'successful logout'
    }


@user_router.post('/signup', response_model=UserSchema, status_code=201)
async def signup(user_data: UserCreate) -> Any:
    user = await user_service.register_new_user(user_data)
    return user


@user_router.get('/me', response_model=UserSchema)
async def get_current_user(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    return user


@user_router.post('/me/change_password', response_model=UserSchema)
async def change_password(
    user: User = Depends(user_service.get_current_user),
    old_password: str = Form(),
    new_password: str = Form()
) -> Any:
    user = await user_service.change_password(user, old_password, new_password)
    return user


@user_router.patch('/me', response_model=UserSchema)
async def update_user(
    new_data: UserUpdate,
    user: UserSchema = Depends(user_service.get_current_user)
) -> Any:
    user = await user_service.patch_user(user.user_id, new_data)
    return user


@user_router.delete('/me', response_model=UserSchema)
async def delete_myself(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    await user_service.delete_user(user.user_id)
    return user


@superuser_router.get('/get_users_list', response_model=list[UserSchema])
async def get_users_list(offset: int = 0, limit: int = 100) -> Any:
    users = await user_service.get_users_list(offset, limit)
    return users


@superuser_router.get('/user/{user_id}', response_model=UserSchema)
async def get_user_by_id(user_id: UUID) -> Any:
    user = await user_service.get_user_by_id(user_id)
    return user


@superuser_router.patch(
    '/update_user', 
    response_model=UserSchema,
    dependencies=[Depends(user_service.get_current_superuser)]
)
async def patch_user(user_id: UUID, new_values: UserPatch) -> Any:
    user = await user_service.patch_user(user_id, new_values)
    return user


@superuser_router.delete(
    '/delete_user', 
    dependencies=[Depends(user_service.get_current_superuser)]
)
async def delete_user(user_id: UUID) -> JSONResponse:
    await user_service.delete_user(user_id)
    return {
        'message': f'user {user_id} deleted'
    }