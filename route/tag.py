
from fastapi import Depends, APIRouter, HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from db.db import get_db

from schema.tag_reading import TagReadingBase, TagReadingCreate
from service import tag_service
from utils.utils import load_config

router = APIRouter(
    prefix="/tag/readings",
    tags=['Poll Tag data']
)


@router.get('/single')
def fetch_reading(db: Session = Depends(get_db)):
    return tag_service.fetch_one(db)


@router.get('/all', response_model=list[TagReadingBase])
def fetch_readings(db: Session = Depends(get_db)):
    return tag_service.fetch_tags(db)


@router.put('/add/many', response_model=list[TagReadingBase])
def add_readings(tag_readings: list[TagReadingCreate], db: Session = Depends(get_db)):
    return tag_service.insert_tag_readings(tag_readings, db)


@router.put('/add/one')
def add_reading(tag_reading: TagReadingCreate, db: Session = Depends(get_db)):
    return tag_service.insert_tag_reading(tag_reading, db)