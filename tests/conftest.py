from src.database import Base, engine
from src.config import settings
import pytest_asyncio
from httpx import AsyncClient
from src.main import app
from typing import AsyncGenerator
from fastapi.testclient import TestClient

    
@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    assert settings.MODE1 == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


client = TestClient(app)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac