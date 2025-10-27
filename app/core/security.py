from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from typing import Optional

from jose import jwt

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, REFRESH_TOKEN_EXPIRE_DAYS

from starlette import status

# Инициализация контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#объект oauth2_scheme для реализации механизма аутентификации с использованием OAuth 2.0
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


#хеширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#---JWT

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#создание рефреш токена
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})  # Добавляем тип токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для проверки токена
def verify_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Проверяем тип токена
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Expected {token_type} token"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def create_new_tokens(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Проверяем, что это refresh токен
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        #create new tokens
        new_access_token = create_access_token(data={"sub": username, "type": "access"})
        new_refresh_token = create_refresh_token(data={"sub": username})

        return {
            "token_type": "bearer",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def create_verification_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "verification"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

