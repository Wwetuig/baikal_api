import os
import subprocess
import sys

def slice_file(input_file_path, output_dir):
    
    # Путь к gdal2tiles.py conda env
    gdal2tiles_path = r"/usr/bin/gdal2tiles.py"

    # Диапазон уровней масштабировани
    zoom_levels = "5-12"

# файл переведенный в 8битный формат 
    temp_vrt = "temp.vrt"



# Проверяем, что выходная папка существует, или создаём её
    os.makedirs(output_dir, exist_ok=True)


    filename = input_file_path.split('/')[-1]
    if filename.lower().endswith(".tif"):

            # Генерация папки для текущего файла
        tile_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
        os.makedirs(tile_output_dir, exist_ok=True)
            
        print(f"Processing file: {input_file_path}")

        try:
                # Команда 1: gdal_translate
            translate_command = [
                "gdal_translate",
                "-of", "VRT",
                "-ot", "Byte",
                "-scale",
                input_file_path,
                temp_vrt
            ]
            subprocess.run(translate_command, check=True)
            print("Step 1: gdal_translate completed.")

                # Команда 2: gdal2tiles.py
            tiles_command = [
                "python3", gdal2tiles_path,
                "-z", zoom_levels,
                "-w", "openlayers",
                temp_vrt,
                tile_output_dir
            ]
            subprocess.run(tiles_command, check=True)
            print("Step 2: gdal2tiles.py completed.")


        except subprocess.CalledProcessError as e:
            print(f"Error processing file {input_file_path}: {e}")

        finally:
            # Команда 3: Удаление временного файла temp.vrt
            if os.path.exists(temp_vrt):
                os.remove(temp_vrt)
                print("Step 3: temp.vrt deleted.")

        print(f"Finished processing: {filename}")







if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <input_file_path> <output_dir_path>")
        sys.exit(1)
    
    try:
        input_file = str(sys.argv[1])
        output_dir = str(sys.argv[2])
    except ValueError:
        print("Error: args must be string type")
        sys.exit(1)
    
    slice_file(input_file, output_dir)

    print("success")