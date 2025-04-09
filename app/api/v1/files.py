import os
from typing import Dict

from fastapi import APIRouter, Depends, Query, HTTPException

from db.CRUD import get_link
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from db.database import get_db

from core.utils import get_mapping_dicts

from db.CRUD import get_all_first_sputnik_data, get_all_second_sputnik_data, get_all_third_sputnik_data

from schemas.files import FirstSputnikDataResponse, SecondSputnikDataResponse, ThirdSputnikDataResponse

from core.utils import find_directory

files_router = APIRouter()

#роут для получения ссылки конкретного объекта из бд по параметрам
@files_router.get('/get_link', response_model=Dict[str, str])

async def find_the_link_to_a_specific_file(data_type: str,
                             measured_parameter: str,
                             measuring_device: str,
                             month_id: int,
                             years_id: int = Query(None),
                             day_id: int = Query(None),
                             lst_num: int = Query(None),
                             db: AsyncSession = Depends(get_db),
                             mapping_dicts: dict = Depends(get_mapping_dicts)):
    """Возвращает ссылку на файл .tif по определенным параметрам """
    response = await get_link(data_type,
             measured_parameter,
             measuring_device,
             years_id,
             month_id,
             day_id,
             lst_num,
             db,
             mapping_dicts)

    return response


@files_router.get('/get_tiles')
async def get_tiles(data_type: str,
                    measured_parameter: str,
                    measuring_device: str,
                    month_id: int,
                    years_id: int = Query(None),
                    day_id: int = Query(None),
                    lst_num: int = Query(None),
                    db: AsyncSession = Depends(get_db),
                    mapping_dicts: dict = Depends(get_mapping_dicts)):
    """Возвращает ссылку на директорию с нарезанными тайлами. """

    full_path = await get_link(data_type,
                               measured_parameter,
                               measuring_device,
                               years_id,
                               month_id,
                               day_id,
                               lst_num,
                               db,
                               mapping_dicts)


    try:
        # Извлечение имени файла без расширения
        filename = full_path.split('/')[-1].split('.')[0]

        root_directory = r"/u/product/temperatura/landsat/june/2024"
        target_directory = filename

        found_path = find_directory(root_directory, target_directory)

    except:
        raise HTTPException(status_code=404, detail="the directory with tiles does not exist")

    result = found_path + "/{z}/{x}/{-y}.png"

    return result


'''
@files_router.get('/first_sputnik_data', response_model=list[FirstSputnikDataResponse])
async def get_first_sputnik_data(db: AsyncSession = Depends(get_db)):
    response = await get_all_first_sputnik_data(db)
    return response

@files_router.get('/second_sputnik_data', response_model=list[SecondSputnikDataResponse])
async def get_second_sputnik_data(db: AsyncSession = Depends(get_db)):
    response = await get_all_second_sputnik_data(db)
    return response

@files_router.get('/third_sputnik_data', response_model=list[ThirdSputnikDataResponse])
async def get_third_sputnik_data(db: AsyncSession = Depends(get_db)):
    response = await get_all_third_sputnik_data(db)
    return response
'''