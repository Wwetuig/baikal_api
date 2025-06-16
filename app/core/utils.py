# маппинг словарей DI
# {parameter_from_the_frontend: real_name_in_the_database}
import os

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

def get_temperature_list_with_coordinates(tiff_path: str):

    def extract_temperature_data(tiff_path, band_number=None):
        """
        Извлекает температурные данные из TIFF-файла.

        Args:
            tiff_path (str): Путь к TIFF-файлу
            band_number (int, optional): Номер канала с температурой. Если None, будет попытка автоматического определения.

        Returns:
            dict: Словарь {(долгота, широта): температура}
            int: Номер использованного канала
        """
        with rasterio.open(tiff_path) as src:
            # Определение канала с температурой
            if band_number is None:
                band_number = detect_temperature_band(src)
                print(f"Используется канал {band_number} для температурных данных")

            # Чтение данных
            band_data = src.read(band_number)

            # Получение координат
            height, width = band_data.shape
            result = {}

            for y in range(height):
                for x in range(width):
                    temp_value = band_data[y, x]
                    # Проверяем, что значение не является nodata и не nan
                    if not np.isnan(temp_value) and temp_value != src.nodata:
                        # Получаем координаты для текущего пикселя
                        lon, lat = pixel_to_lonlat(x, y, src.transform, src.crs)
                        # Используем кортеж в качестве ключа
                        result[(round(lon, 4), round(lat, 4))] = float(temp_value)

            return result, band_number


    def pixel_to_lonlat(x, y, affine_transform, src_crs):
        """Преобразует координаты пикселя в долготу/широту"""
        # Получаем координаты в исходной проекции
        easting, northing = affine_transform * (x, y)

        # Преобразуем в WGS84 (lon/lat)
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

            # Критерии для температурного канала
            if stats['unique'] > 50 and 0 < stats['range'][1] <= 100:
                candidates.append(stats)

        if candidates:
            return sorted(candidates, key=lambda x: x['unique'], reverse=True)[0]['band']
        else:
            return 1

    temperature_data, used_band = extract_temperature_data(tiff_path)

    return temperature_data
