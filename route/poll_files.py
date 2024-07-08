import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import Depends, APIRouter, HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session
from time import perf_counter

from db.db import get_db, get_engine
from schema.tag_reading import TagReadingCreate
from service.tag_service import insert_tag_readings
from utils.utils import load_config

router = APIRouter(
    prefix="/collect/files",
    tags=['Poll Tag data']
)




# @router.get('/poll')
# def poll_files(db: Session = Depends(get_db)):
#     total_records = 0
#     logger.info(f'Searching for files')
#     poll_directories: list[str] = load_config().get("poll_locations")
#     for directory in poll_directories:
#         files = os.listdir(directory)
#         logger.info(f'Found {len(files)} files')
#         for file in files:
#             df: pd.DataFrame = pd.read_csv(os.path.join(directory, file))
#             logger.info(f'Found {len(df)} records in {file}')
#             models = [TagReadingCreate(**row.to_dict()) for i, row in df.iterrows()]
#             total_records += insert_tag_readings(models, db)
#             logger.info(f'Inserted {len(df)} records in {file}')
#     return total_records

def process_file(directory, file):
    logger.info(f'Processing {file}')
    df: pd.DataFrame = pd.read_csv(os.path.join(directory, file))
    logger.info(f'Found {len(df)} records in {file}')
    models = [TagReadingCreate(**row.to_dict()) for i, row in df.iterrows()]

    # Create a new database session for this thread
    with Session(get_engine()) as db:
        record_count = insert_tag_readings(models, db)

    logger.info(f'Inserted {record_count} records in {file}')
    return record_count


@router.get('/poll')
def poll_files(db: Session = Depends(get_db)):
    total_records = 0
    start = perf_counter()
    logger.info(f'Searching for files')
    poll_directories: list[str] = load_config().get("poll_locations")

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Iterate over each directory and file in each directory
        tasks = [executor.submit(process_file, directory, file)
                 for directory in poll_directories
                 for file in os.listdir(directory)]

        # Wait for all threads to finish and get results
        for task in as_completed(tasks):
            total_records += task.result()

    logger.info(f'Inserted total {total_records} records completed in {perf_counter() - start}')
    return total_records



