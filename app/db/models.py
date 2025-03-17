from sqlalchemy import Column, Integer, String, Float

from db.database import Base


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

class Data_type(Base):
    __tablename__ = "data_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    description = Column(String, index=True)

class Measuring_devices(Base):
    __tablename__ = "measuring_devices"

    id = Column(Integer, primary_key=True, index=True)
    name_source = Column(String, index=True)
    description = Column(String, index=True)
    error_rate = Column(Float, index=True)
    name_eng = Column(String, index=True)
    range = Column(String, index=True)
    country = Column(String, index=True)
    name_station = Column(String, index=True)
    url = Column(String, index=True)

class Measured_parameters(Base):
    __tablename__ = "measured_parameters"

    id = Column(Integer, primary_key=True, index=True)
    name_indicator = Column(String, index=True)
    description = Column(String, index=True)
    units_measurement_id = Column(Integer, index=True)