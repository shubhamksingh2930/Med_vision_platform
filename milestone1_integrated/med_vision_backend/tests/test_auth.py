import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "email": "dr.smith@hospital.com",
        "password": "SecurePassword123!",
        "full_name": "Dr. Alice Smith"
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "email": "duplicate@hospital.com",
        "password": "Password123!",
        "full_name": "Dr. Duplicate"
    }
    res1 = await client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert "Email already registered" in res2.json()["detail"]

@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient):
    # Register user
    reg_payload = {
        "email": "radiologist@clinic.com",
        "password": "ClinicPassword123!",
        "full_name": "Dr. Bob"
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    # Login
    login_data = {
        "username": "radiologist@clinic.com",
        "password": "ClinicPassword123!"
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    reg_payload = {
        "email": "nurse@clinic.com",
        "password": "CorrectPassword123!"
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    login_data = {
        "username": "nurse@clinic.com",
        "password": "WrongPassword!"
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_me_profile_success(client: AsyncClient):
    reg_payload = {
        "email": "profile@clinic.com",
        "password": "Password123!",
        "full_name": "Dr. Profile"
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    login_res = await client.post("/api/v1/auth/login", data={
        "username": "profile@clinic.com",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    user_data = me_res.json()
    assert user_data["email"] == "profile@clinic.com"

@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
