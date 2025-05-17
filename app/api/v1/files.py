import os

from typing import Dict

from fastapi import APIRouter, Depends, Query, HTTPException

from db.CRUD import get_link
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from db.database import get_db

from core.utils import get_mapping_dicts
from core.utils import find_directory

from db.CRUD import get_all_first_sputnik_data, get_all_second_sputnik_data, get_all_third_sputnik_data

from schemas.files import FirstSputnikDataResponse, SecondSputnikDataResponse, ThirdSputnikDataResponse
from starlette.responses import FileResponse


from db.CRUD import get_available_parameters_by_date, get_available_sources_by_date, get_points_with_metadata


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

        root_dir_aqua_monthly_avg_year_day = r"/u/product/temperatura/color_tiles/aqua/monthly_avg_year/day"
        root_dir_aqua_monthly_avg_year_night = r"/u/product/temperatura/color_tiles/aqua/monthly_avg_year/night"

        root_directory_landsat_8 = r"/u/product/temperatura/color_tiles/landsat/8"

        root_dir_terra_monthly_avg_year_average_daily = r"/u/product/temperatura/color_tiles/terra/monthly_avg_year/average_daily"
        root_dir_terra_monthly_avg_year_day = r"/u/product/temperatura/color_tiles/terra/monthly_avg_year/day"
        root_dir_terra_monthly_avg_year_night = r"/u/product/temperatura/color_tiles/terra/monthly_avg_year/night"


        root_dir_viirs_monthly_avg_year_day = r"/u/product/temperatura/color_tiles/viirs/monthly_avg_year/day"
        root_dir_viirs_monthly_avg_year_night = r"/u/product/temperatura/color_tiles/viirs/monthly_avg_year/night"

        root_dir_viirs_monthly_avg_many_years = r"/u/product/temperatura/color_tiles/viirs/montly_avg_many_year"
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


@files_router.get("")
async def download_satellite_data_file(full_path: str):


    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="wrong file path")

    # Get filename with extension
    filename = os.path.basename(full_path)
    print(filename)

    return FileResponse(
        full_path,
        media_type="image/tiff",
        filename=filename
    )


@files_router.get("/ground_data/get_available_parameters")
async def return_available_parameters_by_date(startDate: date, endDate: date = Query(None), db: AsyncSession = Depends(get_db)):
    '''возвращает список доступных параметров за определенную дату'''
    data = await get_available_parameters_by_date(startDate, endDate, db)
    return data


@files_router.get("/ground_data/get_available_sources")
async def return_available_source_by_date_and_parameter(parameter: str, startDate: date, endDate: date = Query(None), db: AsyncSession = Depends(get_db)):
    '''возвращает список доступных ресурсов за определенную дату и с определенным парамтером'''
    data = await get_available_sources_by_date(parameter, startDate, endDate, db)
    return data

@files_router.get("/ground_data/get_points")
async def return_points_with_metadata(parameter: str, source: str,  startDate: date, endDate: date = Query(None), db: AsyncSession = Depends(get_db)):
    '''возвращает список точек с метаданными по пределенным парамтерам'''
    data = await get_points_with_metadata(parameter, source, startDate, endDate, db)
    return data

