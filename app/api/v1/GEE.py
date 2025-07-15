#Google Eath Engine

from fastapi import Query, HTTPException, APIRouter
from datetime import timedelta
import ee

from core.utils import parse_date_str


GEERouter = APIRouter() # GEE endpoints
@GEERouter.get("/lst/period/")
def get_lst_by_period(
    lat: float = Query(..., description="Широта точки"),
    lon: float = Query(..., description="Долгота точки"),
    start_param: str = Query(..., alias="start", description="Дата начала в формате ГГГГ-ММ-ДД или ГГГГ.ММ.ДД"),
    end_param: str = Query(..., alias="end", description="Дата конца в формате ГГГГ-ММ-ДД или ГГГГ.ММ.ДД")
):
    start = parse_date_str(start_param)
    end = parse_date_str(end_param)

    if start > end:
        raise HTTPException(status_code=400, detail="Дата начала не может быть позже даты конца")

    try:
        point = ee.Geometry.Point([lon, lat])
        start_date = start.isoformat()
        end_date = end.isoformat()

        dataset = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date, end_date) \
            .filterBounds(point) \
            .select("LST_Day_1km")

        image = dataset.mean()
        if image is None:
            return {"error": "Нет данных за указанный период и точку."}

        temp_dict = image.reduceRegion(
            reducer=ee.Reducer.first(),
            geometry=point,
            scale=1000,
            bestEffort=True
        ).getInfo()

        lst_raw = temp_dict.get("LST_Day_1km")
        if lst_raw is None:
            return {"error": "Нет данных по указанной точке и периоду."}

        lst_celsius = (lst_raw * 0.02) - 273.15
        return {
            "lat": lat,
            "lon": lon,
            "start_date": start_date,
            "end_date": end_date,
            "Mean LST (°C)": round(lst_celsius, 2)
        }

    except Exception as e:
        return {"error": str(e)}



@GEERouter.get("/lst/point/date/")
def get_lst_by_date(
        lat: float = Query(..., description="Широта точки"),
        lon: float = Query(..., description="Долгота точки"),
        date_param: str = Query(..., alias="date", description="Дата в формате ГГГГ-ММ-ДД или ГГГГ.ММ.ДД")
):
    dt = parse_date_str(date_param)
    try:
        point = ee.Geometry.Point([lon, lat])
        start_date = dt.isoformat()
        end_date = (dt + timedelta(days=1)).isoformat()

        dataset = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date, end_date) \
            .filterBounds(point) \
            .select("LST_Day_1km")

        image = dataset.first()
        if image is None:
            return {"error": "Нет данных за эту дату и точку."}

        temp_dict = image.reduceRegion(
            reducer=ee.Reducer.first(),
            geometry=point,
            scale=1000,
            bestEffort=True
        ).getInfo()

        lst_raw = temp_dict.get("LST_Day_1km")
        if lst_raw is None:
            return {"error": "Нет данных по указанной точке и дате."}

        lst_celsius = (lst_raw * 0.02) - 273.15
        return {
            "lat": lat,
            "lon": lon,
            "date": start_date,
            "LST (°C)": round(lst_celsius, 2)
        }

    except Exception as e:
        return {"error": str(e)}




@GEERouter.get("/lst/geotiff/period/")
def get_lst_geotiff_period(
    lat1: float = Query(..., description="Широта точки 1"),
    lon1: float = Query(..., description="Долгота точки 1"),
    lat2: float = Query(..., description="Широта точки 2"),
    lon2: float = Query(..., description="Долгота точки 2"),
    lat3: float = Query(..., description="Широта точки 3"),
    lon3: float = Query(..., description="Долгота точки 3"),
    lat4: float = Query(..., description="Широта точки 4"),
    lon4: float = Query(..., description="Долгота точки 4"),
    start_date: str = Query(..., description="Дата начала периода (ГГГГ-ММ-ДД)"),
    end_date: str = Query(..., description="Дата конца периода (ГГГГ-ММ-ДД)")
):
    try:
        start = parse_date_str(start_date)
        end = parse_date_str(end_date)

        if start > end:
            raise HTTPException(status_code=400, detail="Дата начала не может быть позже даты конца")

        polygon_coords = [
            [lon1, lat1],
            [lon2, lat2],
            [lon3, lat3],
            [lon4, lat4],
            [lon1, lat1]
        ]
        geometry = ee.Geometry.Polygon([polygon_coords])

        dataset = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start.isoformat(), end.isoformat()) \
            .filterBounds(geometry) \
            .select("LST_Day_1km")

        # Преобразование в градусы Цельсия
        image = dataset.mean() \
            .multiply(0.02) \
            .subtract(273.15) \
            .clip(geometry)

        url = image.getDownloadURL({
            'scale': 1000,
            'region': geometry.getInfo()['coordinates'],
            'format': 'GEO_TIFF'
        })

        return {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "region": polygon_coords,
            "download_url": url,
            "note": "Значения в GeoTIFF указаны в градусах Цельсия"
        }

    except Exception as e:
        return {"error": str(e)}



@GEERouter.get("/lst/geotiff/")
def get_lst_geotiff_link(
        lat1: float = Query(..., description="Широта точки 1"),
        lon1: float = Query(..., description="Долгота точки 1"),
        lat2: float = Query(..., description="Широта точки 2"),
        lon2: float = Query(..., description="Долгота точки 2"),
        lat3: float = Query(..., description="Широта точки 3"),
        lon3: float = Query(..., description="Долгота точки 3"),
        lat4: float = Query(..., description="Широта точки 4"),
        lon4: float = Query(..., description="Долгота точки 4"),
        date_param: str = Query(..., alias="date", description="Дата конца периода (ГГГГ-ММ-ДД)")
):
    try:
        date = parse_date_str(date_param)

        polygon_coords = [
            [lon1, lat1],
            [lon2, lat2],
            [lon3, lat3],
            [lon4, lat4],
            [lon1, lat1]
        ]
        geometry = ee.Geometry.Polygon([polygon_coords])

        dataset = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(date.isoformat(), (date + timedelta(days=1)).isoformat()) \
            .filterBounds(geometry) \
            .select("LST_Day_1km")

        image = dataset.mean() \
            .multiply(0.02) \
            .subtract(273.15) \
            .clip(geometry)

        url = image.getDownloadURL({
            'scale': 1000,
            'region': geometry.getInfo()['coordinates'],
            'format': 'GEO_TIFF'
        })

        return {
            "date": date.isoformat(),
            "region": polygon_coords,
            "download_url": url,
            "note": "Значения в GeoTIFF указаны в градусах Цельсия"
        }

    except Exception as e:
        return {"error": str(e)}
