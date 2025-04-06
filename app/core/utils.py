# маппинг словарей DI
# {parameter_from_the_frontend: real_name_in_the_database}
import os

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


def find_directory(root_dir, target_dir):
    # Получаем список всех элементов в директории
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        # Проверяем, что это директория и имя совпадает
        if os.path.isdir(item_path) and item == target_dir:
            return item_path
    return None  # Если не найдено
