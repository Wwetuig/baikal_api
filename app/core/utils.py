# маппинг словарей DI
# {parameter_from_the_frontend: real_name_in_the_database}
import os
from math import sqrt

import rasterio
import numpy as np
from rasterio.warp import transform as warp_transform
from rasterio.windows import Window

type_dict = {
    "Озеро Байкал": "Спутниковые данные",
    "Байкальская природная территория": "Спутниковые данные",
    "Наземные Данные": "Наземные данные",
}

devices_dict = {
    "VIIRS": "VIIRS",
    "LANDSAT": "Landsat-8",
    "MODIS Terra": "MODIS/Terra",
    "MODIS Aqua": "Aqua"
}

parameters_dict = {
    "Прозрачность": "Прозрачность",
    "LST": "Отдельные снимки температуры",
    "Хлорофилл": "Хлорофилл А"
}


# Зависимость для получения словарей
def get_mapping_dicts():
    return {
        "type_dict": type_dict,
        "devices_dict": devices_dict,
        "parameters_dict": parameters_dict
    }


def get_mapped_time_of_day_id():
    return {"Дневные": 1,
            "Ночные": 2,
            "Суточные": 3}


def find_directory(root_dir, target_dir):
    # Получаем список всех элементов в директории
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        # Проверяем, что это директория и имя совпадает
        if os.path.isdir(item_path) and item == target_dir:
            return item_path
    return None  # Если не найдено


import numpy as np
import rasterio
from rasterio.warp import transform as warp_transform
from math import sqrt


def get_temperature_list_with_coordinates(tiff_path: str, target_lon: float, target_lat: float):
    def extract_temperature_data(tiff_path, band_number=None):
        """
        Извлекает температурные данные из TIFF-файла.
        """
        with rasterio.open(tiff_path) as src:
            if band_number is None:
                band_number = detect_temperature_band(src)
                print(f"Используется канал {band_number} для температурных данных")

            band_data = src.read(band_number)
            height, width = band_data.shape
            result = {}

            for y in range(height):
                for x in range(width):
                    temp_value = band_data[y, x]
                    if not np.isnan(temp_value) and temp_value != src.nodata:
                        lon, lat = pixel_to_lonlat(x, y, src.transform, src.crs)
                        result[(lon, lat)] = float(temp_value)
            return result, band_number

    def pixel_to_lonlat(x, y, affine_transform, src_crs):
        """Преобразует координаты пикселя в долготу/широту"""
        easting, northing = affine_transform * (x, y)
        lon, lat = warp_transform(
            src_crs,
            'EPSG:4326',
            [easting],
            [northing]
        )
        return lon[0], lat[0]

    def detect_temperature_band(src):
        """Автоматически определяет наиболее вероятный канал с температурой."""
        candidates = []
        for i in range(1, src.count + 1):
            data = src.read(i)
            valid_data = data[data != src.nodata]

            if valid_data.size == 0:
                continue

            stats = {
                'band': i,
                'unique': len(np.unique(valid_data)),
                'range': (np.min(valid_data), np.max(valid_data)),
                'mean': np.mean(valid_data)
            }

            if stats['unique'] > 50 and 0 < stats['range'][1] <= 100:
                candidates.append(stats)

        if candidates:
            return sorted(candidates, key=lambda x: x['unique'], reverse=True)[0]['band']
        else:
            return 1

    temperature_data, used_band = extract_temperature_data(tiff_path)

    min_distance = float('inf')
    nearest_temp = None
    nearest_coords = None

    for (lon, lat), temp in temperature_data.items():
        distance = sqrt((lon - target_lon) ** 2 + (lat - target_lat) ** 2)

        if distance < min_distance:
            min_distance = distance
            nearest_temp = temp
            nearest_coords = (lon, lat)

    print(f"Минимальное расстояние = {min_distance} градусов")
    print(f"Ближайшие координаты = {nearest_coords}")

    # Возвращаем None если ближайшая точка дальше 0.1 градуса
    if min_distance > 0.1:
        print("Ближайшая точка находится слишком далеко (> 0.1 градуса)")
        return None

    return nearest_temp