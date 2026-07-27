import pytest
import pytest_asyncio
import io
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock, patch

from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.models import Base
from app.db.session import get_db
from app.storage.client import storage_client

# In-memory SQLite DB for ultra-fast, isolated testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest_asyncio.fixture(scope="function")
async def client(db_session: Session) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Mock Person B's MinIO storage service calls
    with patch.object(storage_client, "upload_file", new=MagicMock(return_value="mock_key")):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c

    app.dependency_overrides.clear()

@pytest.fixture
def sample_png_bytes() -> bytes:
    # 1x1 pixel PNG
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00"
        b"\x02\x00\x01H\xafA\x0c\x00\x00\x00\x00IEND\xaeB`\x82"
    )

@pytest.fixture
def sample_dicom_bytes() -> bytes:
    # 128-byte preamble + "DICM" magic header + dummy tag
    preamble = b"\x00" * 128
    magic = b"DICM"
    data = b"\x08\x00\x16\x00\x04\x00\x00\x001.2.3"
    return preamble + magic + data

@pytest.fixture
def sample_pdf_bytes() -> bytes:
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
