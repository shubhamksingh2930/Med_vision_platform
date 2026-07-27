# init_db.py
import asyncio
from app.core.database import engine, Base
# Import models so SQLAlchemy registers metadata
from app.models.medical_record import User, MedicalRecord

async def init_tables():
    async with engine.begin() as conn:
        print("Creating tables in PostgreSQL...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_tables())