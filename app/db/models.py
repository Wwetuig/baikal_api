from sqlalchemy.dialects.postgresql import DATERANGE
from sqlalchemy import LargeBinary

from sqlalchemy import Column, Integer, String, Float, Date, Boolean, func

from db.database import Base



# Определение модели таблицы
class First_sputnik_data(Base):
    __tablename__ = "first_sputnik_data"
    __table_args__ = {"schema": "knowledgebase"}

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
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    description = Column(String, index=True)
    measured_parameters_id = Column(Integer, index=True)
    measuring_devices_id = Column(Integer, index=True)
    month_id = Column(Integer, index=True)
    years_id = Column(Integer, index=True)
    file_number = Column(Integer, index=True)
    times_day_id = Column(Integer, index=True)
    data_type_id = Column(Integer, index=True)

class Third_sputnik_data(Base):
    __tablename__ = "third_sputnik_data"
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    description = Column(String, index=True)
    measured_parameters_id = Column(Integer, index=True)
    measuring_devices_id = Column(Integer, index=True)
    month_id = Column(Integer, index=True)
    file_number = Column(Integer, index=True)
    times_day_id = Column(Integer, index=True)
    data_type_id = Column(Integer, index=True)
    date_range = Column(DATERANGE, index=True)

class Measurement_data(Base): #ground_data
    __tablename__ = "measurement_data"
    __table_args__ = {"schema": "database"}

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(Date, index=True)
    note = Column(String, index=True)
    data_sources_id = Column(Integer, index=True)
    measured_parameters_id = Column(Integer, index=True)
    measuring_devices_id = Column(Integer, index=True)
    value = Column(Float, index=True)
    data_type_id = Column(Integer, index=True)
    speed = Column(Float, index=True)
    coordinates_id = Column(Integer, index=True)
    units_measurement_id = Column(Integer, index=True)

class Data_source(Base): #ground_data
    __tablename__ = "data_sources;"
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    name_organization = Column(String, index=True)
    url = Column(String, index=True)
    data_type_id = Column(Integer, index=True)

class Coordinates(Base): #ground_data
    __tablename__ = "coordinates"
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    coordinates = Column(String, index=True)
    description = Column(String, index=True)


class Units_measurement(Base): #ground_data
    __tablename__ = "units_measurement"
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    unit = Column(String, index=True)
    description_unit = Column(String, index=True)
    description = Column(String, index=True)

class Data_type(Base):
    __tablename__ = "data_type"
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    description = Column(String, index=True)

class Measuring_devices(Base):
    __tablename__ = "measuring_devices"
    __table_args__ = {"schema": "knowledgebase"}

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
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    name_indicator = Column(String, index=True)
    description = Column(String, index=True)
    units_measurement_id = Column(Integer, index=True)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, index=True)
    password = Column("pass", String, index=True)
    roles_id = Column(Integer, index=True)
    login = Column(String, index=True)
    mail = Column(String, index=True)
    date_created = Column(Date, default=func.current_date())
    locked = Column(Boolean, index=True)
    phone_number = Column(String, index=True)
    active = Column(Boolean, index=True)
    foto = Column(LargeBinary, index=True)

class External_services(Base):
    __tablename__ = "external_services"
    __table_args__ = {"schema": "knowledgebase"}

    id = Column(Integer, primary_key=True, index=True)
    name_service = Column(String, index=True)
    description = Column(String, index=True)
    url_reference = Column(String, index=True)



# Создание таблиц в базе данных (если они не существуют)
#Base.metadata.create_all(bind=engine)

