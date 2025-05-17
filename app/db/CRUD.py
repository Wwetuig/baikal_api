from fastapi import HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models import First_sputnik_data, Second_sputnik_data, Third_sputnik_data, Measurement_data,Data_source

from db.models import Data_type, Measuring_devices, Measured_parameters, User, Coordinates, Units_measurement

from schemas.users import UserCreate

from core.security import hash_password

from core.utils import get_mapping_dicts

from core.utils import get_mapped_time_of_day_id

from datetime import date

from sqlalchemy import func



async def get_link(data_type: str,
                   measured_parameter: str,
                   measuring_device: str,
                   years_id: int,
                   month_id: int,
                   day_id: int,
                   time_of_day: str,
                   lst_num: int,
                   db: AsyncSession = Depends(get_db),
                   mapping_dicts: dict = Depends(get_mapping_dicts)
                   ):
    # Доступ к словарям
    devices_dict = mapping_dicts["devices_dict"]
    parameters_dict = mapping_dicts["parameters_dict"]
    type_dict = mapping_dicts["type_dict"]

    # get data_type_id
    data_type_id = await get_data_type_id(db, data_type, type_dict)

    # Получаем device_id
    device_id = await get_device_id(db, measuring_device, devices_dict)

    # Получаем parameter_id
    parameter_id = await get_parameter_id(db, measured_parameter, parameters_dict)

    if time_of_day:
        try:
            times_of_day_dict = get_mapped_time_of_day_id()
            time_of_day_id = times_of_day_dict[time_of_day]
        except:
            raise HTTPException(status_code=404, detail=f"incorrect time of day input")

    try:

        if device_id == 12:  # LANDSAT
            # Создаем запрос с помощью select
            stmt = select(First_sputnik_data).where(
                First_sputnik_data.measured_parameters_id == parameter_id,
                First_sputnik_data.data_type_id == data_type_id,
                First_sputnik_data.measuring_devices_id == device_id,
                First_sputnik_data.years_id == years_id,
                First_sputnik_data.month_id == month_id,
                First_sputnik_data.day_id == day_id,
            )

        #костыль! measured_parameters_id присваивается значение а не берется из бд, т.к. в бд параметр "LST",
        #"среднемесячные данные" и "среднемесячные многолетние" находятся в одной таблице measured_parameters
        #все три запроса ниже находят файл с измеряемым параметром LST, но в Second_sputnik_data и Third_sputnik_data
        #измеряемый параметр указан среднемесячные и среднемесячные многолетние соответственно
        #указать "среднемесячыне" и "LST" одновременно (как и есть на самом деле) невозможно т.к. оба параметра находятся в одной таблице


        elif device_id == 10 and day_id == None and years_id == None:  # VIIRS, среднемесячные многолетние спутниковые данные
            stmt = select(Third_sputnik_data).where(
                Third_sputnik_data.measured_parameters_id == 14,
                Third_sputnik_data.data_type_id == data_type_id,
                Third_sputnik_data.measuring_devices_id == device_id,
                Third_sputnik_data.month_id == month_id,
            )

        elif device_id == 10 and day_id == None:  # VIIRS, среднемесячные спутниковые данные
            stmt = select(Second_sputnik_data).where(
                Second_sputnik_data.measured_parameters_id == 13,
                Second_sputnik_data.data_type_id == data_type_id,
                Second_sputnik_data.measuring_devices_id == device_id,
                Second_sputnik_data.years_id == years_id,
                Second_sputnik_data.month_id == month_id,
                Second_sputnik_data.times_day_id == time_of_day_id,
            )

        elif (device_id == 11) or (device_id == 14)  and day_id == None:  # MODIS/TERRA, среднемесячные спутниковые данные
            stmt = select(Second_sputnik_data).where(
                Second_sputnik_data.measured_parameters_id == 13,
                Second_sputnik_data.data_type_id == data_type_id,
                Second_sputnik_data.measuring_devices_id == device_id,
                Second_sputnik_data.years_id == years_id,
                Second_sputnik_data.month_id == month_id,
                Second_sputnik_data.times_day_id == time_of_day_id,
            )

    except:
        raise HTTPException(status_code=404, detail=f"File not found")

        # Выполняем запрос
    result = await db.execute(stmt)

    # Получаем первый результат
    file = result.scalars().first()

    if file:
        return file.link
    else:
        raise HTTPException(status_code=404, detail=f"File not found")


# Асинхронная функция для получения data_type_id
async def get_data_type_id(db: AsyncSession, data_type: str, type_dict: dict):
    try:

        # Создаем запрос с помощью select
        query = select(Data_type).where(
            Data_type.type == type_dict[data_type]
        )

        # Выполняем запрос
        result = await db.execute(query)

        # Получаем первый результат
        data_type_obj = result.scalars().first()

        if not data_type_obj:
            raise HTTPException(status_code=404, detail="Device not found")

        data_type_id = data_type_obj.id
        return data_type_id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cant find data type id: {str(e)}")


# Асинхронная функция для получения device_id


async def get_device_id(db: AsyncSession, measuring_device: str, devices_dict: dict):
    try:
        # Создаем запрос с помощью select
        query = select(Measuring_devices).where(
            Measuring_devices.name_source == devices_dict[measuring_device]
        )

        # Выполняем запрос
        result = await db.execute(query)

        # Получаем первый результат
        device_obj = result.scalars().first()

        if not device_obj:
            raise HTTPException(status_code=404, detail="Device not found")

        device_id = device_obj.id
        return device_id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cant find device id: {str(e)}")


# Асинхронная функция для получения parameter_id


async def get_parameter_id(db: AsyncSession, measured_parameter: str, parameters_dict: dict):
    try:
        # Создаем запрос с помощью select
        query = select(Measured_parameters).where(
            Measured_parameters.name_indicator == parameters_dict[measured_parameter]
        )

        # Выполняем запрос
        result = await db.execute(query)

        # Получаем первый результат
        parameter_obj = result.scalars().first()

        if not parameter_obj:
            raise HTTPException(status_code=404, detail="Parameter not found")

        parameter_id = parameter_obj.id
        return parameter_id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cant find parameter id: {str(e)}")


# Асинхронная функция для получения всех спктниковых данных
async def get_all_first_sputnik_data(db: AsyncSession = Depends(get_db)):
    result_first = await db.execute(select(First_sputnik_data))
    first_sputnik_data_list = result_first.scalars().all()

    return first_sputnik_data_list


async def get_all_second_sputnik_data(db: AsyncSession = Depends(get_db)):
    result_second = await db.execute(select(Second_sputnik_data))
    second_sputnik_data_list = result_second.scalars().all()

    return second_sputnik_data_list


async def get_all_third_sputnik_data(db: AsyncSession = Depends(get_db)):
    result_third = await db.execute(select(Third_sputnik_data))
    third_sputnik_data_list = result_third.scalars().all()

    return third_sputnik_data_list


async def get_user_by_login(login: str, db: AsyncSession = Depends(get_db)):
    # Создаем запрос с помощью select
    stmt = select(User).where(User.login == login)

    # Выполняем запрос
    result = await db.execute(stmt)

    # Получаем первый результат
    user = result.scalars().first()
    return user


async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким логином
    stmt = select(User).where(User.login == user.login)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    default_role_id = 1  # unauthorized user

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this login already exists")

    # Создаем нового пользователя
    db_user = User(
        login=user.login,
        password=hash_password(user.password),
        fio=user.fio,
        mail=user.mail,
        phone_number=user.phone_number,
        roles_id=default_role_id,
        locked=False,
        active=False
    )

    # Добавляем пользователя в базу данных
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user



async def return_available_parameters_list(params: list, db: AsyncSession = Depends(get_db)):
    result_lst = []

    for param in params:

        try:
            # создание запроса
            stmt = select(Measured_parameters.name_indicator).where(
                Measured_parameters.id == param
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

            # Выполняем запрос
        result = await db.execute(stmt)

        # Получаем первый результат
        data = result.scalars().first()

        result_lst.append(data)

    return result_lst

async def get_available_parameters_by_date(startDate: date, endDate: date, db: AsyncSession = Depends(get_db)):
    try:
        if endDate:
            # создание запроса
            stmt = select(Measurement_data.measured_parameters_id).where(
                func.date(Measurement_data.date_time).between(startDate, endDate)
            ).distinct()
        else:
            stmt = select(Measurement_data.measured_parameters_id).where(
                func.date(Measurement_data.date_time) == startDate
            ).distinct()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # Выполняем запрос
    result = await db.execute(stmt)

    # Получаем первый результат
    data = result.scalars().all()

    result_lst = await return_available_parameters_list(data, db)
    if result_lst:
        return result_lst
    else:
        return []

async def get_available_sources_by_date(parameter: str, startDate: date, endDate: date, db: AsyncSession = Depends(get_db)):
    try:
        if endDate:
            # создание запроса
            stmt = select(Measurement_data.data_sources_id).where(
                (func.date(Measurement_data.date_time).between(startDate, endDate)) &
                (Measured_parameters.name_indicator == parameter)
                # Предполагаем, что это имя столбца в таблице measured_parameters
            ).join(Measured_parameters, Measurement_data.measured_parameters_id == Measured_parameters.id).distinct()
        else:
            stmt = select(Measurement_data.data_sources_id).where(
                (func.date(Measurement_data.date_time) == startDate) &
                (Measured_parameters.name_indicator == parameter)
                # Предполагаем, что это имя столбца в таблице measured_parameters
            ).join(Measured_parameters, Measurement_data.measured_parameters_id == Measured_parameters.id).distinct()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # Выполняем запрос
    result = await db.execute(stmt)

    # Получаем первый результат
    data = result.scalars().all()

    result_lst = await return_available_sources_list(data, db)
    if result_lst:
        return result_lst
    else:
        return []


async def return_available_sources_list(params: list, db: AsyncSession = Depends(get_db)):
    result_lst = []

    for param in params:

        try:
            # создание запроса
            stmt = select(Data_source.name_organization).where(
                Data_source.id == param
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

            # Выполняем запрос
        result = await db.execute(stmt)

        # Получаем первый результат
        data = result.scalars().first()

        result_lst.append(data)

    return result_lst


async def get_points_with_metadata(parameter: str, source: str, startDate: date, endDate: date, db: AsyncSession = Depends(get_db)):
    try:
        # создание запроса
        if endDate:
            stmt = (
                select(
                    Coordinates.coordinates,
                    Measurement_data.value,
                    Units_measurement.unit,
                    Units_measurement.description_unit,
                    Measuring_devices.name_source.label("sensor")
                )
                .join(Coordinates, Measurement_data.coordinates_id == Coordinates.id)
                .join(Units_measurement, Measurement_data.units_measurement_id == Units_measurement.id)
                .join(Measuring_devices, Measurement_data.data_sources_id == Measuring_devices.id)
                .where(
                    (func.date(Measurement_data.date_time).between(startDate, endDate)) &
                    (Measured_parameters.name_indicator == parameter) &
                    (Data_source.name_organization == source)
                )
                .join(Measured_parameters, Measurement_data.measured_parameters_id == Measured_parameters.id)
                .join(Data_source, Measurement_data.data_sources_id == Data_source.id)
            )
        else:
            stmt = (
                select(
                    Coordinates.coordinates,
                    Measurement_data.value,
                    Units_measurement.unit,
                    Units_measurement.description_unit,
                    Measuring_devices.name_source.label("sensor")
                )
                .join(Coordinates, Measurement_data.coordinates_id == Coordinates.id)
                .join(Units_measurement, Measurement_data.units_measurement_id == Units_measurement.id)
                .join(Measuring_devices, Measurement_data.data_sources_id == Measuring_devices.id)
                .where(
                    (func.date(Measurement_data.date_time) == startDate) &
                    (Measured_parameters.name_indicator == parameter) &
                    (Data_source.name_organization == source)
                )
                .join(Measured_parameters, Measurement_data.measured_parameters_id == Measured_parameters.id)
                .join(Data_source, Measurement_data.data_sources_id == Data_source.id)
            )



    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

            # Выполняем запрос
    result = await db.execute(stmt)

        # Получаем первый результат
    data = result.mappings().all()

    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="data not found")
