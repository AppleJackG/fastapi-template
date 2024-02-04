from uuid import UUID
from .models import User
from sqlalchemy import select
from ..database import session_factory


class UserRepository:

    @staticmethod
    async def get_user_by_username(username: str) -> User | None:
        query = select(User).where(User.username==username)
        async with session_factory() as session:
            result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> User | None:
        query = select(User).where(User.user_id==user_id)
        async with session_factory() as session:
            result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user


user_repository = UserRepository()
