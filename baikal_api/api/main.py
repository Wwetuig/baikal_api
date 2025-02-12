from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import First_sputnik_data, Second_sputnik_data, Third_sputnik_data

# Создание таблиц в базе данных (если они не существуют)
Base.metadata.create_all(bind=engine)

# Создание FastAPI приложения
app = FastAPI()

# Роут для проверки подключения к базе данных
@app.get("/check_db")
async def check_db(db: Session = Depends(get_db)):
    try:
        # Простой запрос для проверки подключения
        result = db.execute(text("SELECT 1")).fetchall()
        if result:
            return {"status": "success", "message": "Database connection is successful"}
        else:
            raise HTTPException(status_code=500, detail="Failed to verify database connection")
    except Exception as e:
        # Логируем подробную информацию об ошибке
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {str(e)}")

#роут для получения конкретного объекта из бд по параметрам
@app.get('/file')
async def read_concrete_file(data_type_id: int,
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