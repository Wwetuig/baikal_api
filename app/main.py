from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from api.v1 import users, files
from schemas.schemas import UserOut, UserCreate
from core.security import verify_token, oauth2_scheme, verify_password, create_access_token
from db.CRUD import get_link, get_user_by_login, create_user
from db.database import get_db



# Создание FastAPI приложения
app = FastAPI()

#CORS Configuring
origins = [
    "http://localhost:3000",
    "127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(users.user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(files.files_router, prefix="/api/v1/files", tags=["Files"])


