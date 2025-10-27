import os
import rasterio
import numpy as np

def fix_alpha_channel(input_path):
    """Явно задает прозрачность в альфа-канале для черных, темных и NoData областей"""
    with rasterio.open(input_path) as src:
        # Проверяем наличие альфа-канала
        if src.count != 4:
            print(f"Файл {input_path} не содержит альфа-канала (только {src.count} каналов)")
            return
            
        # Читаем все каналы
        data = src.read()
        meta = src.meta.copy()
        
        # Определяем области для прозрачности:
        # 1. Пиксели, где R=G=B=0 (черный цвет)
        # 2. Пиксели, где R,G,B < 10 (темные области)
        # 3. Пиксели, где альфа=0 (если уже есть прозрачность)
        # 4. NoData пиксели (если указаны)
        
        # Маска для черных пикселей (R=G=B=0)
        black_mask = (data[0] == 0) & (data[1] == 0) & (data[2] == 0)
        
        # Маска для темных пикселей (R,G,B < 10)
        dark_mask = (data[0] < 10) & (data[1] < 10) & (data[2] < 10)
        
        # Маска для существующей прозрачности (если альфа=0)
        existing_alpha_mask = (data[3] == 0)
        
        # Маска для NoData (если указано)
        if src.nodata is not None:
            nodata_mask = (data[0] == src.nodata) | (data[1] == src.nodata) | (data[2] == src.nodata)
        else:
            nodata_mask = np.zeros(src.shape, dtype=bool)
        
        # Объединяем все маски
        transparency_mask = black_mask | dark_mask | existing_alpha_mask | nodata_mask
        
        # Создаем новый альфа-канал
        new_alpha = np.where(transparency_mask, 0, 255).astype(np.uint8)
        
        # Обновляем данные
        data[3] = new_alpha
        
        # Сохраняем изменения
        with rasterio.open(input_path, 'w', **meta) as dst:
            dst.write(data)
            
        # Проверяем результат
        with rasterio.open(input_path) as check_src:
            alpha = check_src.read(4)
            transparent = np.sum(alpha == 0)
            opaque = np.sum(alpha == 255)
            print(f"Файл {input_path} обработан. Прозрачные: {transparent}, Непрозрачные: {opaque}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python addAlpha.py <input_file_path>")
        print("Дополнительные параметры можно изменить в коде (clip_percentiles)")
        sys.exit(1)
    
    try:
        input_file = str(sys.argv[1])
    except ValueError:
        print("Error: args must be string type")
        sys.exit(1)

fix_alpha_channel(input_file )