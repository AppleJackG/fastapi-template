from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

session_factory = async_sessionmaker(autoflush=False, autocommit=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
