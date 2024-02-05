from uuid import UUID
from .repository import user_repository, UserRepository
from .models import User
from typing import NoReturn
from .utils import auth_utils
from .schemas import Token, UserCreate
from .exceptions import UsernameIsTaken, EmailIsTaken


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

user_service = UserService(user_repository)