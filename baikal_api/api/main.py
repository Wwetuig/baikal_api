from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from database import Base, engine, get_db
from models import First_sputnik_data, Second_sputnik_data, Third_sputnik_data, Measuring_devices, Measured_parameters, \
    Data_type

# Создание таблиц в базе данных (если они не существуют)
Base.metadata.create_all(bind=engine)

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

#dictionaries  {parameter_from_the_frontend: real_name_in_the_database}
    type_dict = {
        "Озеро Байкал": "Спутниковые данные",
        "Байкальская природная территория": "Спутниковые данные",
        "Наземные Данные": "Наземные данные",
    }

    devices_dict = {
        "VIIRS": "VIIRS",
        "LANDSAT": "Landsat-8",
        "MODIS Terra": "MODIS/Terra",
        "MODIS Aqua": "Aqua"
    }

    parameters_dict = {
        "Прозрачность": "Прозрачность",
        "LST": "Отдельные снимки температуры",
        "Хлорофилл": "Хлорофилл А"
    }

    # get data_type_id
    try:
        data_type_obj = (db.query(Data_type).filter(
            Data_type.type == type_dict[data_type],
        ).first())

        data_type_id = data_type_obj.id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cant find type id: {str(e)}")

    # get device_id
    try:
        device_obj = db.query(Measuring_devices).filter(
            Measuring_devices.name_source == devices_dict[measuring_device],
        ).first()

        device_id = device_obj.id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cant find device id: {str(e)}")

    #get parameter_id
    try:
        parameter_obj = db.query(Measured_parameters).filter(
            Measured_parameters.name_indicator == parameters_dict[measured_parameter],
        ).first()

        parameter_id = parameter_obj.id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cant find parameter id: {str(e)}")

    #main query: get link of specific file
    try:
        for f in (First_sputnik_data, Second_sputnik_data, Third_sputnik_data):
            file = db.query(f).filter(
                f.measured_parameters_id == parameter_id,
                f.data_type_id == data_type_id,
                f.measuring_devices_id == device_id,
                f.years_id == years_id,
                f.month_id == month_id,
                f.day_id == day_id,
            ).first()

            if(file):
                break

        return {'link': file.link}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching file: {str(e)}")



