from httpx import AsyncClient
from src.config import settings


async def test_refresh_token(ac: AsyncClient, refresh_token):
    response = await ac.post('/auth/refresh', headers={'refresh-token': refresh_token})
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None
    assert response.json()['expires_in'] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert response.json()['token_type'] == 'Bearer'