from app.db.session import SessionLocal
from app.db.models import User
from app.storage.client import storage_client
from sqlalchemy import text
import io

db = SessionLocal()
print("DB connected:", db.execute(text("SELECT 1")).scalar() == 1)
db.close()

try:
    storage_client.client.create_bucket(Bucket=storage_client.bucket)
except Exception:
    pass

fake_file = io.BytesIO(b"test content")
url = storage_client.upload_file(fake_file, "test/hello.txt", "text/plain")
print("Uploaded to:", url)