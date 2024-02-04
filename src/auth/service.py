from uuid import UUID
from .repository import user_repository, UserRepository
from .models import User
from typing import NoReturn
from .utils import auth_utils
from .schemas import Token


class UserService:
    
    def __init__(self, user_repo: UserRepository) -> None:
        self.repo = user_repo

    async def authenticate_user(self, username: str, password: str) -> Token | NoReturn:
        user = await self.repo.get_user_by_username(username)
        if auth_utils.check_credentials(user, password):
            jwt_payload = {
                'sub': str(user.user_id),
                'username': user.username,
                'email': user.email
            }
            access_token = auth_utils.encode_token(jwt_payload)
            return Token(
                access_token=access_token,
                token_type='Bearer'
            )

    async def get_current_user(self, token: str) -> User:
        payload = auth_utils.decode_token(token)
        user_id: UUID | None = payload.get('sub')
        user = await self.repo.get_user_by_id(user_id)
        return user


user_service = UserService(user_repository)