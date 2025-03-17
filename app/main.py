from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from db.CRUD import get_link
from db.database import Base, engine, get_db



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
