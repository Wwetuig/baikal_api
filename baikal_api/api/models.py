from sqlalchemy import Column, Integer, String
from database import Base

# Определение модели таблицы
class First_sputnik_data(Base):
    __tablename__ = "first_sputnik_data"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    description = Column(String, index=True)
    measured_parameters_id = Column(Integer, index=True)
    measuring_devices_id = Column(Integer, index=True)
    month_id = Column(Integer, index=True)
    years_id = Column(Integer, index=True)
    day_id = Column(Integer, index=True)
    file_number = Column(Integer, index=True)
    times_day_id = Column(Integer, index=True)
    data_type_id = Column(Integer, index=True)

class Second_sputnik_data(Base):
    __tablename__ = "second_sputnik_data"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    description = Column(String, index=True)
    measured_parameters_id = Column(Integer, index=True)
    measuring_devices_id = Column(Integer, index=True)
    month_id = Column(Integer, index=True)
    years_id = Column(Integer, index=True)
    day_id = Column(Integer, index=True)
    file_number = Column(Integer, index=True)
    times_day_id = Column(Integer, index=True)
    data_type_id = Column(Integer, index=True)

class Third_sputnik_data(Base):
    __tablename__ = "third_sputnik_data"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    description = Column(String, index=True)
    measured_parameters_id = Column(Integer, index=True)
    measuring_devices_id = Column(Integer, index=True)
    month_id = Column(Integer, index=True)
    years_id = Column(Integer, index=True)
    day_id = Column(Integer, index=True)
    file_number = Column(Integer, index=True)
    times_day_id = Column(Integer, index=True)
    data_type_id = Column(Integer, index=True)

