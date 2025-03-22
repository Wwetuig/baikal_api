from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from core import config

# Настройки подключения к базе данных
DATABASE_URL = config.DATABASE_URL

# Инициализация SQLAlchemy
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Получение асинхронной сессии базы данных
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db