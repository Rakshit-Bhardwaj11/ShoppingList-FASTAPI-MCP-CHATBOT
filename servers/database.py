import os 
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL","sqlite+aiosqlite:///./shopping_list.db")

async_engine=create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_size=20,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False)

Base=declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

#Request comes in
#        ↓
# get_db()
#        ↓
# create database session
#        ↓
# endpoint uses session
#        ↓
# request finishes
#        ↓
# close session