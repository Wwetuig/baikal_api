from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Настройки подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Инициализация SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()