from datetime import datetime
from loguru import logger
from schema.tag_reading import TagReadingBase
import pandas as pd
import random


from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from datetime import datetime

def get_random_number():
    return random.randint(0, 5)


def type_map(index, value):
    if index % 5:
        return str(value) + index
    if index % 3:
        return int(value)
    if index % 2:
        return float(value)

def create_file(i: int, number_records_per_file: int) -> None:
    readings: List[Dict[str, Any]] = []
    for j in range(number_records_per_file):
        readings.append(
            TagReadingBase(
                devicename=f'device{j}',
                location='SEA10',
                t_stamp=datetime.now(),
                quality=get_random_number(),
                float_value=float((get_random_number() + 1) * i),
                string_value=str(i * j),
                date_value=datetime.now()
            ).model_dump()
        )
    pd.DataFrame(readings).to_csv(f'test/device_file_{i}.csv', index=False)
    logger.info(f'File #{i} completed')


def create_files(number_of_files: int, number_records_per_file: int) -> None:

    with ThreadPoolExecutor() as executor:
        executor.map(create_file, range(number_of_files), [number_records_per_file] * number_of_files)