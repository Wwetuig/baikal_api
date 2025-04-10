import os

from typing import Dict

from fastapi import APIRouter, Depends, Query, HTTPException

from db.CRUD import get_link
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from db.database import get_db

from core.utils import get_mapping_dicts
from core.utils import find_directory

from db.CRUD import get_all_first_sputnik_data, get_all_second_sputnik_data, get_all_third_sputnik_data

from schemas.files import FirstSputnikDataResponse, SecondSputnikDataResponse, ThirdSputnikDataResponse

files_router = APIRouter()


# роут для получения ссылки конкретного объекта из бд по параметрам
@files_router.get('/get_link', response_model=str)
async def find_the_link_to_a_specific_file(data_type: str,
                                           measured_parameter: str,
                                           measuring_device: str,
                                           month_id: int,
                                           years_id: int = Query(None),
                                           day_id: int = Query(None),
                                           time_of_day: str = Query(None),
                                           lst_num: int = Query(None),
                                           db: AsyncSession = Depends(get_db),
                                           mapping_dicts: dict = Depends(get_mapping_dicts)):
    response = await get_link(data_type,
                              measured_parameter,
                              measuring_device,
                              years_id,
                              month_id,
                              day_id,
                              time_of_day,
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
                    time_of_day: str = Query(None),
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
                               time_of_day,
                               lst_num,
                               db,
                               mapping_dicts)

    try:
        # Извлечение имени файла без расширения
        filename = full_path.split('/')[-1].split('.')[0]

        root_directory_landsat_8 = r"/u/product/temperatura/landsat/june/2024"

        root_dir_viirs_monthly_avg_year_day = "/u/product/temperatura/tiles/viirs/monthly_avg_year/day"
        root_dir_viirs_monthly_avg_year_night = "/u/product/temperatura/tiles/viirs/monthly_avg_year/night"
        root_dir_viirs_monthly_avg_many_years = "/u/product/temperatura/tiles/viirs/montly_avg_many_year"

        root_dir_terra_monthly_avg_year_average_daily = "/u/product/temperatura/tiles/terra/monthly_avg_year/average_daily"
        root_dir_terra_monthly_avg_year_day = "/u/product/temperatura/tiles/terra/monthly_avg_year/day"
        root_dir_terra_monthly_avg_year_night = "/u/product/temperatura/tiles/terra/monthly_avg_year/night"

        root_dir_aqua_monthly_avg_year_day = "/u/product/temperatura/tiles/aqua/monthly_avg_year/day"
        root_dir_aqua_monthly_avg_year_night = "/u/product/temperatura/tiles/aqua/monthly_avg_year/night"

        #target dir with tiles
        target_directory = filename

        for dir in (root_directory_landsat_8, root_dir_viirs_monthly_avg_year_day, root_dir_viirs_monthly_avg_year_night,
                    root_dir_viirs_monthly_avg_many_years, root_dir_terra_monthly_avg_year_average_daily,
                    root_dir_terra_monthly_avg_year_day, root_dir_terra_monthly_avg_year_night,
                    root_dir_aqua_monthly_avg_year_day, root_dir_aqua_monthly_avg_year_night):
            found_path = find_directory(dir, target_directory)

            if found_path:
                break

    except:
        raise HTTPException(status_code=404, detail="the directory with tiles does not exist")

    result = found_path + "/{z}/{x}/{-y}.png"

    return result
