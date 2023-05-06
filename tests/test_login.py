import httpx
import pytest

from fastapi import status


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser1@gmail.com",
        "password": "testuser12345",
    }
    headers = {
        "accept": "application/json", 
        "Content-Type": "application/json"
    }
    test_response = {
        "message": "User successfully registered!"
    }

    response = await default_client.post("/user/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient):
    payload = {
        "username": "testuser1@gmail.com",
        "password": "testuser12345"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = await default_client.post("/user/signin", data=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["token_type"] == "Bearer"