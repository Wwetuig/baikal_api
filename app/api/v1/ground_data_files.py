from fastapi import APIRouter, Depends, Query

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db


from db.CRUD import get_available_parameters_by_date, get_available_sources_by_date, get_points_with_metadata

from db.CRUD import get_available_dates_for_ground_data

ground_data_router = APIRouter()



@ground_data_router.get("/get_available_parameters")
async def return_available_parameters_by_date(startDate: date, endDate: date = Query(None), db: AsyncSession = Depends(get_db)):
    '''возвращает список доступных параметров за определенную дату'''
    data = await get_available_parameters_by_date(startDate, endDate, db)
    return data


@ground_data_router.get("/get_available_sources")
async def return_available_source_by_date_and_parameter(parameter: str, startDate: date, endDate: date = Query(None), db: AsyncSession = Depends(get_db)):
    '''возвращает список доступных ресурсов за определенную дату и с определенным парамтером'''
    data = await get_available_sources_by_date(parameter, startDate, endDate, db)
    return data

@ground_data_router.get("/get_available_dates")
async def return_available_dates(db: AsyncSession = Depends(get_db)):
    '''возвращает список доступных ресурсов за определенную дату и с определенным парамтером'''
    data = await get_available_dates_for_ground_data(db)
    return data

@ground_data_router.get("/get_points")
async def return_points_with_metadata(parameter: str, source: str,  startDate: date, endDate: date = Query(None), db: AsyncSession = Depends(get_db)):
    '''возвращает список точек с метаданными по пределенным парамтерам'''
    data = await get_points_with_metadata(parameter, source, startDate, endDate, db)
    return data

