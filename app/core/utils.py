#маппинг словарей DI
#{parameter_from_the_frontend: real_name_in_the_database}

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