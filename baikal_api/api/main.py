from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine, get_db
from models import First_sputnik_data, Second_sputnik_data, Third_sputnik_data


# Создание таблиц в базе данных (если они не существуют)
Base.metadata.create_all(bind=engine)

# Создание FastAPI приложения
app = FastAPI()

#CORS Configuring
origins = [
    "http://localhost:3000",
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
async def find_the_link_to_a_specific_file(data_type_id: int,
                             measured_parameters_id: int,
                             measuring_devices_id: int,
                             years_id: int,
                             month_id: int,
                             day_id: int,
                             num: int,
                             db: Session = Depends(get_db)):
    try:
        for f in (First_sputnik_data, Second_sputnik_data, Third_sputnik_data):
            file = db.query(f).filter(
                f.measured_parameters_id == measured_parameters_id,
                f.data_type_id == data_type_id,
                f.measuring_devices_id == measuring_devices_id,
                f.years_id == years_id,
                f.month_id == month_id,
                f.day_id == day_id,
            ).first()

            if(file):
                break

        return {'link': file.link}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching file: {str(e)}")