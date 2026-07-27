import pytest
from httpx import AsyncClient

async def get_auth_headers(client: AsyncClient, email: str = "testuser@hospital.com") -> dict:
    await client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Test User"
    })
    login_res = await client.post("/api/v1/auth/login", data={
        "username": email,
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_upload_png_image_success(client: AsyncClient, sample_png_bytes: bytes):
    headers = await get_auth_headers(client, "png@hospital.com")
    files = {"file": ("chest_xray.png", sample_png_bytes, "image/png")}

    response = await client.post("/api/v1/upload/", headers=headers, files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "chest_xray.png"
    assert data["mime_type"] == "image/png"
    assert data["status"] == "PENDING"
    assert "raw_images/" in data["r2_image_key"]
    assert "logs/" in data["r2_log_key"]

@pytest.mark.asyncio
async def test_upload_dicom_file_success(client: AsyncClient, sample_dicom_bytes: bytes):
    headers = await get_auth_headers(client, "dicom@hospital.com")
    files = {"file": ("scan.dcm", sample_dicom_bytes, "application/dicom")}

    response = await client.post("/api/v1/upload/", headers=headers, files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "scan.dcm"
    assert data["status"] == "PENDING"

@pytest.mark.asyncio
async def test_upload_pdf_report_success(client: AsyncClient, sample_pdf_bytes: bytes):
    headers = await get_auth_headers(client, "pdf@hospital.com")
    files = {"file": ("lab_report.pdf", sample_pdf_bytes, "application/pdf")}

    response = await client.post("/api/v1/upload/", headers=headers, files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "lab_report.pdf"
    assert data["mime_type"] == "application/pdf"

@pytest.mark.asyncio
async def test_upload_unsupported_format(client: AsyncClient):
    headers = await get_auth_headers(client, "invalid@hospital.com")
    files = {"file": ("notes.txt", b"plain text content", "text/plain")}

    response = await client.post("/api/v1/upload/", headers=headers, files=files)
    assert response.status_code == 400
    assert "Unsupported media type" in response.json()["detail"]

@pytest.mark.asyncio
async def test_upload_empty_file(client: AsyncClient):
    headers = await get_auth_headers(client, "empty@hospital.com")
    files = {"file": ("empty.png", b"", "image/png")}

    response = await client.post("/api/v1/upload/", headers=headers, files=files)
    assert response.status_code == 400
    assert "File is empty" in response.json()["detail"]

@pytest.mark.asyncio
async def test_upload_unauthenticated(client: AsyncClient, sample_png_bytes: bytes):
    files = {"file": ("chest_xray.png", sample_png_bytes, "image/png")}
    response = await client.post("/api/v1/upload/", files=files)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_and_get_user_uploads(client: AsyncClient, sample_png_bytes: bytes, sample_pdf_bytes: bytes):
    headers = await get_auth_headers(client, "multi@hospital.com")

    # Upload 2 files
    res1 = await client.post("/api/v1/upload/", headers=headers, files={"file": ("img.png", sample_png_bytes, "image/png")})
    res2 = await client.post("/api/v1/upload/", headers=headers, files={"file": ("report.pdf", sample_pdf_bytes, "application/pdf")})
    
    record1_id = res1.json()["id"]

    # List uploads
    list_res = await client.get("/api/v1/upload/", headers=headers)
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] == 2
    assert len(list_data["items"]) == 2

    # Get single upload record
    get_res = await client.get(f"/api/v1/upload/{record1_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == record1_id
