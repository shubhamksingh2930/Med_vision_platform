import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "username": "dr.smith",
        "password": "SecurePassword123!",
    }
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    payload = {
        "username": "duplicate",
        "password": "Password123!",
    }
    res1 = await client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/auth/register", json=payload)
    assert res2.status_code == 400
    assert "Username already registered" in res2.json()["detail"]

@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient):
    reg_payload = {
        "username": "radiologist",
        "password": "ClinicPassword123!",
    }
    await client.post("/api/auth/register", json=reg_payload)

    login_data = {
        "username": "radiologist",
        "password": "ClinicPassword123!"
    }
    response = await client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    reg_payload = {
        "username": "nurse",
        "password": "CorrectPassword123!"
    }
    await client.post("/api/auth/register", json=reg_payload)

    login_data = {
        "username": "nurse",
        "password": "WrongPassword!"
    }
    response = await client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_me_profile_success(client: AsyncClient):
    reg_payload = {
        "username": "profile",
        "password": "Password123!",
    }
    await client.post("/api/auth/register", json=reg_payload)

    login_res = await client.post("/api/auth/login", data={
        "username": "profile",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me_res = await client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    user_data = me_res.json()
    assert user_data["username"] == "profile"

@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401
