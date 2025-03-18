from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from core.security import verify_password, create_access_token
from db.CRUD import get_user_by_login, create_user
from db.database import get_db
from schemas.schemas import UserOut, UserCreate

user_router = APIRouter()
@user_router.post('/register', response_model=UserOut)
async def register_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_login(user.login, db)
    print('login: '+ user.login)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(user, db)

# Авторизация пользователя. Эндпоинт для получения токена
@user_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = get_user_by_login(form_data.username, db)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерация токена
    access_token = create_access_token(data={"sub": {'id': user.id, 'login': user.login}})
    return {"token_type": "bearer", "access_token": access_token}

