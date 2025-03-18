from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

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

#роут для получения ссылки конкретного объекта из бд по параметрам
@app.get('/file', tags=['File'])
async def find_the_link_to_a_specific_file(data_type: str,
                             measured_parameter: str,
                             measuring_device: str,
                             years_id: int,
                             month_id: int,
                             day_id: int,
                             lst_num: int,
                             db: Session = Depends(get_db)):
    response = get_link(data_type,
             measured_parameter,
             measuring_device,
             years_id,
             month_id,
             day_id,
             lst_num,
             db)

    return response

@app.post('/register', response_model=UserOut)
async def register_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_login(user.login, db)
    print('login: '+ user.login)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(user, db)

# Авторизация пользователя. Эндпоинт для получения токена
@app.post("/token")
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

