from uuid import UUID, uuid4

from fastapi import Depends
from loguru import logger
from .repository import AuthRepository, user_repository, UserRepository, auth_repository
from .models import User
from typing import NoReturn
from .utils import auth_utils
from .schemas import Token, UserCreate, RefreshTokenPayload
from .exceptions import InvalidToken, UsernameIsTaken, EmailIsTaken

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


class AuthService:

    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository) -> None:
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def login(self, username: str, password: str) -> Token | NoReturn:
        user = await self.user_repo.get_user_by_username(username)
        if auth_utils.check_credentials(user, password):
            access_key = uuid4()
            access_token = auth_utils.create_access_token(user, access_key)
            refresh_token = auth_utils.create_refresh_token(user, access_key)
            await self.auth_repo.add_refresh_token(refresh_token)
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type='Bearer'
            )
        
    async def refresh_token(self, refresh_token: str) -> Token:
        payload = auth_utils.decode_token(refresh_token)
        if not (token_in_db := await self.auth_repo.find_refresh_token(payload)):
            raise InvalidToken
        new_access_key = uuid4()
        new_access_token = auth_utils.create_access_token(token_in_db.user, new_access_key)
        new_refresh_token = auth_utils.create_refresh_token(token_in_db.user, new_access_key)
        await self.auth_repo.add_refresh_token(new_refresh_token)
        return Token(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type='Bearer'
            )
    

class UserService:
    
    def __init__(self, user_repo: UserRepository) -> None:
        self.repo = user_repo

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        payload = auth_utils.decode_token(token)
        user_id: UUID | None = payload.get('sub')
        user = await self.repo.get_user_by_id(user_id)
        return user
    
    async def register_new_user(self, user_data: UserCreate) -> User | NoReturn:
        user_dict = user_data.model_dump(exclude_unset=True)
        user_dict.update(
            {'password': auth_utils.hash_password(user_data.password)}
        )
        user_exists = await self.repo.get_user_by_username(user_dict.get('username'))
        if user_exists:
            raise UsernameIsTaken
        if email := user_dict.get('email'):
            user_exists = await self.repo.get_user_by_email(email)
            if user_exists:
                raise EmailIsTaken
        new_user = await self.repo.create_new_user(user_dict)
        return new_user


auth_service = AuthService(auth_repository, user_repository)
user_service = UserService(user_repository)