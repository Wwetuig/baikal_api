from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from core.security import verify_password, create_access_token, create_refresh_token, create_new_tokens
from db.CRUD import get_user_by_login, create_user
from db.database import get_db
from schemas.users import UserOut, UserCreate, UserProfile

from core.security import oauth2_scheme

from core.security import verify_token

from db.CRUD import get_current_active_user, get_user_by_id

user_router = APIRouter()


@user_router.post('/register', response_model=UserOut)
async def register_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_login(user.login, db)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user(user, db)


# Авторизация пользователя. Эндпоинт для получения токена
@user_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await get_user_by_login(form_data.username, db)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерация access токена
    access_token = create_access_token(data={"sub": user.login, "type": "access"})

    # генерация refresh токена
    refresh_token = create_refresh_token(data={"sub": user.login})

    return {"token_type": "bearer", "access_token": access_token, "refresh_token": refresh_token}


# обновление токенов
@user_router.post('/refresh')
async def refresh_tokens(refresh_token: str):
    tokens = await create_new_tokens(refresh_token)
    return tokens


@user_router.get("/me", response_model=UserProfile)
async def protected_endpoint(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user, role = await get_current_active_user(token, db)
    roles = []
    roles.append(role)
    '''  
    roles.append(role)
    if user.roles_id == 1:
        roles.append("Авторизованный пользователь")
    elif user.roles_id == 2:
        roles.append("Авторизованный пользователь")
    elif user.roles_id == 3:
        roles.append("Администратор")
    else: raise HTTPException(status_code=400, detail="Role doesnt exist")
    '''
    profile = UserProfile(
        fio = user.fio,
        login=user.login,
        mail=user.mail,
        phone_number=user.phone_number,
        date_created=user.date_created,
        roles=roles,  # Используем название роли вместо roles_id
        locked=user.locked
    )
    return profile


# Эндпоинт для получения пользователя по ID
@user_router.get("/{user_id}", response_model=UserProfile)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получение информации о пользователе по ID
    """

    user = await get_user_by_id(user_id, db)  # Замените на вашу функцию

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )

    return user