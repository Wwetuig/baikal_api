import os
import subprocess
import time

LANDSAT_8_WATCH_DIR = "/u/product/temperatura/landsat/8"
LANDSAT_8_OUTPUT_DIR = "/u/product/temperatura/landsat/june/2024"

VIIRS_MONTHLY_AVG_MANY_YEARS_WATCH_DIR = "/u/product/temperatura/viirs/montly_avg_many_year"
VIIRS_MONTHLY_AVG_MANY_YEARS_OUTPUT_DIR = "/u/product/temperatura/tiles/viirs/montly_avg_many_year"

VIIRS_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR = "/u/product/temperatura/viirs/monthly_avg_year/night"
VIIRS_MONTHLY_AVG_YEAR_NIGHT_OUTPUT_DIR = "/u/product/temperatura/viirs/tiles/monthly_avg_year/night"

VIIRS_MONTHLY_AVG_YEAR_DAY_WATCH_DIR = "/u/product/temperatura/viirs/monthly_avg_year/day"
VIIRS_MONTHLY_AVG_YEAR_DAY_OUTPUT_DIR = "/u/product/temperatura/tiles/viirs/monthly_avg_year/day"

VIIRS_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR = "/u/product/temperatura/viirs/monthly_avg_year/average_daily"
VIIRS_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_OUTPUT_DIR = "/u/product/temperatura/tiles/viirs/monthly_avg_year/average_daily"

TERRA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR = "/u/product/temperatura/terra/monthly_avg_year/night"
TERRA_MONTHLY_AVG_YEAR_NIGHT_OUTPUT_DIR = "/u/product/temperatura/tiles/terra/monthly_avg_year/night"

TERRA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR = "/u/product/temperatura/terra/monthly_avg_year/day"
TERRA_MONTHLY_AVG_YEAR_DAY_OUTPUT_DIR = "/u/product/temperatura/tiles/terra/monthly_avg_year/day"

TERRA_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR = "/u/product/temperatura/terra/monthly_avg_year/average_daily"
TERRA_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_OUTPUT_DIR = "/u/product/temperatura/tiles/terra/monthly_avg_year/average_daily"

AQUA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR = "/u/product/temperatura/aqua/monthly_avg_year/night"
AQUA_MONTHLY_AVG_YEAR_NIGHT_OUTPUT_DIR = "/u/product/temperatura/tiles/aqua/monthly_avg_year/night"

AQUA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR = "/u/product/temperatura/aqua/monthly_avg_year/day"
AQUA_MONTHLY_AVG_YEAR_DAY_OUTPUT_DIR = "/u/product/temperatura/tiles/aqua/monthly_avg_year/day"

#previous files in dir
landsat_8_previous_files = set(os.listdir(LANDSAT_8_WATCH_DIR))
viirs_many_years_previous_files = set(os.listdir(VIIRS_MONTHLY_AVG_MANY_YEARS_WATCH_DIR))
viirs_year_night_previous_files = set(os.listdir(VIIRS_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR))
viirs_year_day_previous_files = set(os.listdir(VIIRS_MONTHLY_AVG_YEAR_DAY_WATCH_DIR))
viirs_year_avg_daily_previous_files = set(os.listdir(VIIRS_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR))
terra_year_night_previous_files = set(os.listdir(TERRA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR))
terra_year_day_previous_files = set(os.listdir(TERRA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR))
terra_year_avg_daily_previous_files = set(os.listdir(TERRA_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR))
aqua_year_night_previous_files = set(os.listdir(AQUA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR))
aqua_year_day_previous_files = set(os.listdir(AQUA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR))


def process_new_files(new_files, watch_dir, output_dir, product_type):
    if new_files:
        print(f"Новые файлы {product_type}: {new_files}")
        for file in new_files:
            translate_command = [
                "python3",
                "slicingScript.py",
                os.path.join(watch_dir, file),
                output_dir,
            ]
            try:
                subprocess.run(translate_command, check=True)
                print(f"Файл {file} успешно обработан")
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при обработке файла {file}: {e}")


while True:
    # Проверяем новые файлы для каждого продукта
    landsat_8_current_files = set(os.listdir(LANDSAT_8_WATCH_DIR))
    landsat_8_new_files = landsat_8_current_files - landsat_8_previous_files

    viirs_many_years_current_files = set(os.listdir(VIIRS_MONTHLY_AVG_MANY_YEARS_WATCH_DIR))
    viirs_many_years_new_files = viirs_many_years_current_files - viirs_many_years_previous_files

    viirs_year_night_current_files = set(os.listdir(VIIRS_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR))
    viirs_year_night_new_files = viirs_year_night_current_files - viirs_year_night_previous_files

    viirs_year_day_current_files = set(os.listdir(VIIRS_MONTHLY_AVG_YEAR_DAY_WATCH_DIR))
    viirs_year_day_new_files = viirs_year_day_current_files - viirs_year_day_previous_files

    viirs_year_avg_daily_current_files = set(os.listdir(VIIRS_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR))
    viirs_year_avg_daily_new_files = viirs_year_avg_daily_current_files - viirs_year_avg_daily_previous_files

    terra_year_night_current_files = set(os.listdir(TERRA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR))
    terra_year_night_new_files = terra_year_night_current_files - terra_year_night_previous_files

    terra_year_day_current_files = set(os.listdir(TERRA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR))
    terra_year_day_new_files = terra_year_day_current_files - terra_year_day_previous_files

    terra_year_avg_daily_current_files = set(os.listdir(TERRA_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR))
    terra_year_avg_daily_new_files = terra_year_avg_daily_current_files - terra_year_avg_daily_previous_files

    aqua_year_night_current_files = set(os.listdir(AQUA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR))
    aqua_year_night_new_files = aqua_year_night_current_files - aqua_year_night_previous_files

    aqua_year_day_current_files = set(os.listdir(AQUA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR))
    aqua_year_day_new_files = aqua_year_day_current_files - aqua_year_day_previous_files

    # Обрабатываем новые файлы для каждого продукта

    if landsat_8_new_files:
        process_new_files(landsat_8_new_files, LANDSAT_8_WATCH_DIR, LANDSAT_8_OUTPUT_DIR, "Landsat 8")
        landsat_8_previous_files = landsat_8_current_files

    if viirs_many_years_new_files:
        process_new_files(viirs_many_years_new_files, VIIRS_MONTHLY_AVG_MANY_YEARS_WATCH_DIR,
                          VIIRS_MONTHLY_AVG_MANY_YEARS_OUTPUT_DIR, "VIIRS Many Years")
        viirs_many_years_previous_files = viirs_many_years_current_files

    if viirs_year_night_new_files:
        process_new_files(viirs_year_night_new_files, VIIRS_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR,
                          VIIRS_MONTHLY_AVG_YEAR_NIGHT_OUTPUT_DIR, "VIIRS Year Night")
        viirs_year_night_previous_files = viirs_year_night_current_files

    if viirs_year_day_new_files:
        process_new_files(viirs_year_day_new_files, VIIRS_MONTHLY_AVG_YEAR_DAY_WATCH_DIR,
                          VIIRS_MONTHLY_AVG_YEAR_DAY_OUTPUT_DIR, "VIIRS Year Day")
        viirs_year_day_previous_files = viirs_year_day_current_files

    if viirs_year_avg_daily_new_files:
        process_new_files(viirs_year_avg_daily_new_files, VIIRS_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR,
                          VIIRS_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_OUTPUT_DIR, "VIIRS Year Average Daily")
        viirs_year_avg_daily_previous_files = viirs_year_avg_daily_current_files

    if terra_year_night_new_files:
        process_new_files(terra_year_night_new_files, TERRA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR,
                          TERRA_MONTHLY_AVG_YEAR_NIGHT_OUTPUT_DIR, "Terra Year Night")
        terra_year_night_previous_files = terra_year_night_current_files

    if terra_year_day_new_files:
        process_new_files(terra_year_day_new_files, TERRA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR,
                          TERRA_MONTHLY_AVG_YEAR_DAY_OUTPUT_DIR, "Terra Year Day")
        terra_year_day_previous_files = terra_year_day_current_files

    if terra_year_avg_daily_new_files:
        process_new_files(terra_year_avg_daily_new_files, TERRA_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_WATCH_DIR,
                          TERRA_MONTHLY_AVG_YEAR_AVERAGE_DAYLY_OUTPUT_DIR, "Terra Year Average Daily")
        terra_year_avg_daily_previous_files = terra_year_avg_daily_current_files

    if aqua_year_night_new_files:
        process_new_files(aqua_year_night_new_files, AQUA_MONTHLY_AVG_YEAR_NIGHT_WATCH_DIR,
                          AQUA_MONTHLY_AVG_YEAR_NIGHT_OUTPUT_DIR, "Aqua Year Night")
        aqua_year_night_previous_files = aqua_year_night_current_files

    if aqua_year_day_new_files:
        process_new_files(aqua_year_day_new_files, AQUA_MONTHLY_AVG_YEAR_DAY_WATCH_DIR,
                          AQUA_MONTHLY_AVG_YEAR_DAY_OUTPUT_DIR, "Aqua Year Day")
        aqua_year_day_previous_files = aqua_year_day_current_files

    time.sleep(5)  # Проверка каждые 5 секунд