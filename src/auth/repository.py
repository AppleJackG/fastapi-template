from uuid import UUID
from .models import User
from sqlalchemy import select, insert
from ..database import session_factory
from pydantic import EmailStr


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
    
    @staticmethod
    async def get_user_by_email(email: EmailStr) -> User | None:
        query = select(User).where(User.email==email)
        async with session_factory() as session:
            result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    @staticmethod
    async def create_new_user(new_user_data: dict[str, str]) -> User:
        stmt = insert(User).values(**new_user_data).returning(User)
        async with session_factory() as session:
            result = await session.execute(stmt)
            await session.commit()
        created_user = result.scalar_one()
        return created_user


user_repository = UserRepository()
