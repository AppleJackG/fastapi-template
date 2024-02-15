from httpx import AsyncClient


async def test_user_signup(ac: AsyncClient):
    new_user = {
        "username": "test_user",
        "password": "qwerty",
        "email": "user@example.com"
    }
    response = await ac.post('/users/signup', json=new_user)
    assert response.status_code == 201
    assert response.json()['username'] == 'test_user'
    assert response.json()['email'] == 'user@example.com'
    assert 'user_id' in response.json()
    assert not ('password' in response.json())