from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, JSON
from motor.motor_asyncio import AsyncIOMotorClient
import os

PG_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://ims_user:ims_password@localhost:5432/ims_db")
engine = create_async_engine(PG_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class IncidentModel(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, index=True)
    component_id = Column(String, index=True)
    severity = Column(String)
    state = Column(String, default="OPEN")
    rca_data = Column(JSON, nullable=True)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:adminpassword@localhost:27017/")
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client.ims_lake
raw_signals_collection = mongo_db.raw_signals

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)