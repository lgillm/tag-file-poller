from fastapi import Depends, APIRouter, HTTPException, status
from loguru import logger

from service.seed_data import create_files

router = APIRouter(
    prefix="/seed/test",
    tags=['Seed Data']
)


@router.put('/create/{num_files}/{tags_per_file}')
def seed_files(num_files: int, tags_per_file: int):
    logger.info(f'Creating files: {num_files} with {tags_per_file} tags for file')
    return create_files(num_files, tags_per_file)
