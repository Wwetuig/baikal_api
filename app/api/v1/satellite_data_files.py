import os

from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db

from core.utils import get_mapping_dicts
from core.utils import find_directory

from starlette.responses import FileResponse

from db.CRUD import get_landsat_link, get_monthly_avg_file_link, get_monthly_avg_many_years_file_link

from db.CRUD import get_available_dates_for_firstSD, get_available_dates_for_secondSD, get_available_dates_for_thirdSD



satellite_data_router = APIRouter() # common endpoints
satellite_data_firstSD_router = APIRouter() #landsat
satellite_data_secondSD_router = APIRouter() #monthly avg
satellite_data_thirdSD_router = APIRouter() #monthly_avg many years


# роут для получения ссылки конкретного объекта из бд по параметрам
@satellite_data_firstSD_router.get('/get_landsat_link', response_model=str)
async def find_the_link_to_landsat_file(data_type: str,
                                           parameter: str,
                                           device: str,
                                           month_id: int,
                                           years_id: int,
                                           day_id: int,
                                           lst_num: int = Query(None),
                                           db: AsyncSession = Depends(get_db),
                                           mapping_dicts: dict = Depends(get_mapping_dicts)):
    '''возвращает ссылку на файл TIFF по данным для спутника Landsat'''
    response = await get_landsat_link(data_type,
                              parameter,
                              device,
                              years_id,
                              month_id,
                              day_id,
                              lst_num,
                              db,
                              mapping_dicts)

    return response

@satellite_data_secondSD_router.get('/get_monthly_avg_file_link', response_model=str)
async def find_the_link_to_monthly_avg_file(data_type: str,
                                           parameter: str,
                                           device: str,
                                           month_id: int,
                                           years_id: int,
                                           time_of_day: str,
                                           db: AsyncSession = Depends(get_db),
                                           mapping_dicts: dict = Depends(get_mapping_dicts)):
    '''возвращает ссылку на файл TIFF по по данным среднемесячным'''

    response = await get_monthly_avg_file_link(data_type,
                              parameter,
                              device,
                              years_id,
                              month_id,
                              time_of_day,
                              db,
                              mapping_dicts)

    return response


@satellite_data_thirdSD_router.get('/get_monthly_avg_many_years_file_link', response_model=str)
async def find_the_link_to_monthly_avg_many_years_file(data_type: str,
                                           parameter: str,
                                           device: str,
                                           month_id: int,
                                           db: AsyncSession = Depends(get_db),
                                           mapping_dicts: dict = Depends(get_mapping_dicts)):
    '''возвращает ссылку на файл TIFF по данным многолетним среднемесячным'''


    response = await get_monthly_avg_many_years_file_link(data_type,
                              parameter,
                              device,
                              month_id,
                              db,
                              mapping_dicts)

    return response
@satellite_data_firstSD_router.get('/get_landsat_tiles')
async def get_landsat_tiles(data_type: str,
                    parameter: str,
                    device: str,
                    month_id: int,
                    years_id: int,
                    day_id: int,
                    lst_num: int = Query(None),
                    db: AsyncSession = Depends(get_db),
                    mapping_dicts: dict = Depends(get_mapping_dicts)):
    """Возвращает ссылку на директорию с нарезанными цветными тайлами для спутника Landsat"""
    full_path = await get_landsat_link(data_type,
                              parameter,
                              device,
                              years_id,
                              month_id,
                              day_id,
                              lst_num,
                              db,
                              mapping_dicts)


    try:
        # Извлечение имени файла без расширения
        filename = full_path.split('/')[-1].split('.')[0]

        root_directory_landsat_8 = r"/u/product/temperatura/color_tiles/landsat/8"

         #target dir with tiles
        target_directory = filename

        found_path = find_directory(root_directory_landsat_8, target_directory)

    except:
        raise HTTPException(status_code=404, detail="the directory with tiles does not exist")

    result = found_path + "/{z}/{x}/{-y}.png"

    return result

@satellite_data_secondSD_router.get('/get_monthly_avg_tiles')
async def get_monthly_avg_tiles(data_type: str,
                    parameter: str,
                    device: str,
                    month_id: int,
                    years_id: int,
                    time_of_day: str,
                    db: AsyncSession = Depends(get_db),
                    mapping_dicts: dict = Depends(get_mapping_dicts)):
    """Возвращает ссылку на директорию с нарезанными цветными тайлами для среднемесячных данных"""
    full_path = await get_monthly_avg_file_link(data_type,
                               parameter,
                               device,
                               years_id,
                               month_id,
                               time_of_day,
                               db,
                               mapping_dicts)

    try:
        # Извлечение имени файла без расширения
        filename = full_path.split('/')[-1].split('.')[0]

        root_dir_aqua_monthly_avg_year_day = r"/u/product/temperatura/color_tiles/aqua/monthly_avg_year/day"
        root_dir_aqua_monthly_avg_year_night = r"/u/product/temperatura/color_tiles/aqua/monthly_avg_year/night"

        root_dir_terra_monthly_avg_year_average_daily = r"/u/product/temperatura/color_tiles/terra/monthly_avg_year/average_daily"
        root_dir_terra_monthly_avg_year_day = r"/u/product/temperatura/color_tiles/terra/monthly_avg_year/day"
        root_dir_terra_monthly_avg_year_night = r"/u/product/temperatura/color_tiles/terra/monthly_avg_year/night"


        root_dir_viirs_monthly_avg_year_day = r"/u/product/temperatura/color_tiles/viirs/monthly_avg_year/day"
        root_dir_viirs_monthly_avg_year_night = r"/u/product/temperatura/color_tiles/viirs/monthly_avg_year/night"

        #target dir with tiles
        target_directory = filename

        for dir in (root_dir_viirs_monthly_avg_year_day, root_dir_viirs_monthly_avg_year_night,
                    root_dir_terra_monthly_avg_year_average_daily,
                    root_dir_terra_monthly_avg_year_day, root_dir_terra_monthly_avg_year_night,
                    root_dir_aqua_monthly_avg_year_day, root_dir_aqua_monthly_avg_year_night):
            found_path = find_directory(dir, target_directory)

            if found_path:
                break

    except:
        raise HTTPException(status_code=404, detail="the directory with tiles does not exist")

    result = found_path + "/{z}/{x}/{-y}.png"

    return result


@satellite_data_thirdSD_router.get('/get_monthly_avg_many_years_tiles')
async def get_monthly_avg_many_years_tiles(data_type: str,
                    parameter: str,
                    device: str,
                    month_id: int,
                    time_of_day: str,
                    db: AsyncSession = Depends(get_db),
                    mapping_dicts: dict = Depends(get_mapping_dicts)):
    """Возвращает ссылку на директорию с нарезанными цветными тайлами для многолетних среднемесячных данных"""
    full_path = await get_monthly_avg_many_years_file_link(data_type,
                               parameter,
                               device,
                               month_id,
                               time_of_day,
                               db,
                               mapping_dicts)

    try:
        # Извлечение имени файла без расширения
        filename = full_path.split('/')[-1].split('.')[0]

        root_dir_viirs_monthly_avg_many_years = r"/u/product/temperatura/color_tiles/viirs/montly_avg_many_year"
        #target dir with tiles
        target_directory = filename

        found_path = find_directory(root_dir_viirs_monthly_avg_many_years, target_directory)

    except:
        raise HTTPException(status_code=404, detail="the directory with tiles does not exist")

    result = found_path + "/{z}/{x}/{-y}.png"

    return result

@satellite_data_router.get("/download")
async def download_satellite_data(full_path: str):
    """скачивание TIFF файла или отдельных тайлов .png"""

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



@satellite_data_firstSD_router.get('/get_available_dates_landsat')
async def get_available_dates_landsat(data_type: str,
                         device: str,
                         parameter:str,
                         lst_num: int = Query(None),
                         db: AsyncSession = Depends(get_db),
                         mapping_dicts: dict = Depends(get_mapping_dicts)):
    data = await get_available_dates_for_firstSD(data_type, device, parameter,lst_num, db, mapping_dicts)
    return data

@satellite_data_secondSD_router.get('/get_available_dates_monthly_avg')
async def get_available_dates_monthly_avg(data_type: str,
                         device: str,
                         parameter:str,
                         time_of_day: str,
                         db: AsyncSession = Depends(get_db),
                         mapping_dicts: dict = Depends(get_mapping_dicts)):
    data = await get_available_dates_for_secondSD(data_type, device, parameter, time_of_day, db, mapping_dicts)
    return data

@satellite_data_thirdSD_router.get('/get_available_dates_monthly_avg_many_years')
async def get_available_dates_monthly_avg_many_years(data_type: str,
                         device: str,
                         parameter:str,
                         time_of_day: str,
                         db: AsyncSession = Depends(get_db),
                         mapping_dicts: dict = Depends(get_mapping_dicts)):
    data = await get_available_dates_for_thirdSD(data_type, device, parameter, time_of_day, db, mapping_dicts)
    return data



