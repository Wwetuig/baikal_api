from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1 import users, files

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

@app.get("/")
async def read_root():
    return {"framework": "FastAPI",
            "message": "The API for BAIKAL Information System"
            }


