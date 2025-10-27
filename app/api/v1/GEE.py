#Google Eath Engine

from fastapi import Query, HTTPException, APIRouter
from fastapi.responses import Response
from datetime import timedelta
import ee

from core.utils import parse_date_str

from core.security import oauth2_scheme
from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from db.CRUD import get_current_active_user_email

import httpx

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import aiosmtplib

GEERouter = APIRouter() # GEE endpoints


#mail service
#говнокод потому что надо показать заказчику отправку писем 
from aiosmtplib import send
SMTP_SERVER='mail.ict.nsc.ru'
SMTP_PORT=465
SMTP_USERNAME='baikal@ict.sbras.ru'
SMTP_PASSWORD='Thi5bohgahQu'
FROM_EMAIL='baikal@ict.sbras.ru'

async def send_email(to: str, message: str):
    try:
        
        await send(
            message,
            sender=FROM_EMAIL,
            recipients=[to],
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            use_tls=True,
        )
        return {"status": "success", "message": "Email sent successfully"}
        
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    

    'https://baikal.ict.nsc.ru/api/v1/users/verify_email?token=w'

async def send_verification_email(to: str, verification_token: str):
    VERIFICATION_URL = 'https://baikal.ict.nsc.ru/api/v1/users/verify_email'
    #verification_url = f"{VERIFICATION_URL}?token={verification_token}"
    verification_url = f"{VERIFICATION_URL}/{verification_token}"
    
    message = f"""
    <h2>Подтверждение Email</h2>
    <p>Пожалуйста, нажмите на ссылку ниже чтобы подтвердить ваш email адрес:</p>
    <a href="{verification_url}">Подтвердить Email</a>
    <p>Или скопируйте ссылку: {verification_url}</p>
    <p><em>Ссылка действительна 15 минут</em></p>
    """.encode('utf-8')
    
    try:
        await send(
            message,
            sender=FROM_EMAIL,
            recipients=[to],
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            use_tls=True
        )
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))


async def send_file_via_email(
    url: str,
    to_email: str,
    message: str
):
    # Получаем файл
    file_data = await download_file(url)
    
    # Создаем email сообщение
    email_message = MIMEMultipart()
    email_message["From"] = FROM_EMAIL
    email_message["To"] = to_email
    
    # Добавляем текстовую часть
    email_message.attach(MIMEText(message, "plain"))
    
    # Добавляем файл как вложение
    attachment = MIMEApplication(file_data["content"])
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=file_data["filename"]
    )
    email_message.attach(attachment)
    
    # Отправляем email
    try:
        await aiosmtplib.send(
            email_message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            use_tls=True
        )
        return {"status": "success", "message": f"Файл отправлен на {to_email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки email: {str(e)}")
    
async def download_file(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return {
                "content": response.content,
                "content_type": response.headers.get("content-type", "application/octet-stream"),
                "filename": url.split("/")[-1] or "downloaded_file"
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=404, detail=f"File not found: {e}")
        


#GEE endpoints
@GEERouter.get("/lst/period/")
def get_lst_by_period(
    token: str = Depends(oauth2_scheme),
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
        token: str = Depends(oauth2_scheme),
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
async def get_lst_geotiff_period(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
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
    email = ""
    try:
        email = await get_current_active_user_email(token, db)
    except Exception as e:
        return {"email error": str(e)}
    
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
        
        try:
            print(f"user email: {email}\nurl: {url}")
            #await send_email(email, f"Download GeoTIFF: {url}")
            msg = "Download GeoTIFF"
            await send_file_via_email(url, email, msg)
        except Exception as e:
            return {"cant send email": str(e)}
        
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
async def get_lst_geotiff_link(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
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
    
    email = ""
    try:
        email = await get_current_active_user_email(token, db)
    except Exception as e:
        return {"email error": str(e)}
    
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
        
        try:
            print(f"user email: {email}\nurl: {url}")
            #await send_email(email, f"Download GeoTIFF: {url}")
            msg = "Download GeoTIFF"
            await send_file_via_email(url, email, msg)
        except Exception as e:
            return {"cant send email": str(e)}

        return {
            "date": date.isoformat(),
            "region": polygon_coords,
            "download_url": url,
            "note": "Значения в GeoTIFF указаны в градусах Цельсия"
        }

    except Exception as e:
        return {"error": str(e)}











 


@GEERouter.get("/lst/geotiff/period/temp/")
async def get_lst_geotiff_period(
    db: AsyncSession = Depends(get_db),
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
            "download_url": url
        }

    except Exception as e:
        return {"error": str(e)}
    

@GEERouter.get("/lst/geotiff/temp/")
async def get_lst_geotiff_link(
    db: AsyncSession = Depends(get_db),
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
            "download_url": url
        }

    except Exception as e:
        return {"error": str(e)}