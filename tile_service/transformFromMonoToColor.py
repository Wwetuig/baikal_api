import os
import sys
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def create_red_to_cyan_colormap():
    """Создает пользовательскую цветовую карту от темно-красного через желтый к голубому"""
    colors = [
        (0.00, '#000000'),
        (0.03, '#070038'),  # Темно-синий (очень холодно)
        (0.05, '#0a0049'),
        (0.10, '#0f0047'),
        (0.15, '#140060'),
        (0.20, '#1a0080'),  # Синий
        (0.25, '#003399'),
        (0.30, '#0066cc'),
        (0.35, '#0099ff'),  # Голубой
        (0.40, '#00ccff'),
        (0.45, '#00ffff'),  # Циан (вода/умеренные значения)
        (0.50, '#33ff99'),  # Зеленый (нейтральная зона)
        (0.55, '#99ff33'),
        (0.60, '#ccff00'),  # Желто-зеленый
        (0.65, '#ffff00'),  # Ярко-желтый
        (0.70, '#ffcc00'),
        (0.75, '#ff9900'),  # Оранжевый (тепло)
        (0.80, '#ff6600'),
        (0.85, '#ff3300'),  # Красный
        (0.90, '#800000'),
        (0.95, '#6e0000'),
        (1.00, '#330000')   # Темно-красный (очень горячо)
    ]
    return LinearSegmentedColormap.from_list('red_cyan', colors)

def clip_outliers(data, mask, lower_percentile=2, upper_percentile=98):
    """
    Обрезает выбросы по указанным процентилям.
    Возвращает обрезанные данные и новые границы.
    """
    valid_data = data[~mask]
    
    if len(valid_data) > 0:
        lower_bound = np.percentile(valid_data, lower_percentile)
        upper_bound = np.percentile(valid_data, upper_percentile)
        clipped_data = np.clip(data, lower_bound, upper_bound)
        return clipped_data, lower_bound, upper_bound
    else:
        return data, np.nan, np.nan

def normalize_data(data, mask, min_val, max_val):
    """
    Нормализует данные в диапазон [0, 1] относительно min_val и max_val.
    Устанавливает 0 для маскированных значений.
    """
    # Нормализуем к [0, 1]
    norm_data = (data - min_val) / (max_val - min_val)
    norm_data = np.clip(norm_data, 0, 1)  # Гарантируем, что значения в [0, 1]
    
    # Устанавливаем 0 для маскированных значений
    norm_data[mask] = 0
    
    return norm_data

def convert_mono_to_color(input_path, output_dir, colormap='viridis', clip_percentiles=(1, 99)):
    """
    Конвертирует монохромный TIFF в цветной, применяя цветовую карту.
    Для каждого файла индивидуально растягивает цветовую карту от минимального до максимального значения.
    """
    # Открываем входной файл
    with rasterio.open(input_path) as src:
        # Читаем данные (предполагаем одноканальное изображение)
        data = src.read(1)
        meta = src.meta.copy()
        
        # Создаем маску для NoData значений
        if src.nodata is not None:
            mask = (data == src.nodata) | np.isnan(data)
        else:
            mask = (data == 0) | np.isnan(data)


        # 1. Обрезаем выбросы по процентам
        clipped_data, actual_min, actual_max = clip_outliers(data, mask, 
                                                           clip_percentiles[0], 
                                                           clip_percentiles[1])
        
        print(f"Для файла {os.path.basename(input_path)}:")
        print(f"Минимальное значение: {actual_min:.2f}")
        print(f"Максимальное значение: {actual_max:.2f}")
        print(f"Диапазон после обрезания {clip_percentiles[0]}%-{clip_percentiles[1]}%: min = {actual_min:.2f} - max = {actual_max:.2f}")


        #2.1 Находим центральный пик (пик с максимальным количеством пикселей)
        valid_data = data[~np.isnan(data)].compressed() if isinstance(data, np.ma.MaskedArray) else data[~np.isnan(data)]
        counts, bins, patches = plt.hist(valid_data, bins=100, color='red', alpha=0.7, edgecolor='black')
        main_peak_index = np.argmax(counts)
        main_peak_count = counts[main_peak_index]
        
        # Определяем порог как 10% от количества пикселей в пике
        threshold = 0.1 * main_peak_count
 	#2.1 Находим правую границку (колово пикселей равное 10% от максимума)
        found_temp_right = None
        for i in range(main_peak_index + 1, len(counts)):
            if counts[i] < threshold:
                found_temp_right = (bins[i] + bins[i+1]) / 2
                break
        
        if found_temp_right is not None:
            plt.axvline(found_temp_right, color='purple', linestyle='dashed', linewidth=1, 
                       label=f'Граница справа: {found_temp_right:.2f}°C (пикселей < {threshold})')
            right_ridge = round(found_temp_right, 2)
            print(f"right ridge = {right_ridge}")
        
        found_temp_left = None
        for i in range(main_peak_index - 1, -1, -1):
            if counts[i] < threshold:
                found_temp_left = (bins[i] + bins[i+1]) / 2
                break
        
        if found_temp_left is not None:
            plt.axvline(found_temp_left, color='orange', linestyle='dashed', linewidth=1, 
                        label=f'Граница слева: {found_temp_left:.2f}°C (пикселей < {threshold})')
            left_ridge = round(found_temp_left, 2)
            print(f"left_ridge = {left_ridge}")
            
        # 3. Нормализуем данные от минимального к максимальному значению в файле
        #norm_data = normalize_data(clipped_data, mask, actual_min, actual_max)
        norm_data = normalize_data(clipped_data, mask, left_ridge, right_ridge)
        
        # Применяем цветовую карту
        if isinstance(colormap, str):
            cmap = plt.get_cmap(colormap)
        else:
            cmap = colormap
            
        colored_data = (cmap(norm_data) * 255).astype(np.uint8)  # Конвертируем в 0-255
        
        # Устанавливаем полную прозрачность для NoData участков
        colored_data[mask, 3] = 0  # Альфа-канал = 0 для прозрачности
        
        # Транспонируем из (h, w, 4) в (4, h, w) для Rasterio
        colored_data = np.rollaxis(colored_data, 2, 0)
        
        # Обновляем метаданные для цветного файла
        meta.update({
            'count': 4,  # RGBA
            'dtype': 'uint8',
            'photometric': 'RGB',
            'nodata': 0  # Указываем, что прозрачность определяется альфа-каналом
        })

        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, filename)
        
        # Сохраняем результат
        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(colored_data)

# Создаем пользовательскую цветовую карту
custom_cmap = create_red_to_cyan_colormap()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <input_file_path> <output_dir_path>")
        print("Дополнительные параметры можно изменить в коде (clip_percentiles)")
        sys.exit(1)
    
    try:
        input_file = str(sys.argv[1])
        output_dir = str(sys.argv[2])
    except ValueError:
        print("Error: args must be string type")
        sys.exit(1)

    
    # Параметры обработки (можно изменить)
    CLIP_PERCENTILES = (1, 99)  # Обрезать 1% с каждого края
    
    # Используем нашу пользовательскую цветовую карту
    convert_mono_to_color(input_file, output_dir, 
                         colormap=custom_cmap,
                         clip_percentiles=CLIP_PERCENTILES)

    print("success")
