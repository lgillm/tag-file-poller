from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from model.tag_reading import TagReading as TagModel
from utils.performance import clock
from schema.tag_reading import TagReadingCreate


def fetch_tags(db: Session):
    return db.query(TagModel).all()


def fetch_one(db: Session):
    return db.query(TagModel).first()


def add_many(tags: list[TagReadingCreate], db: Session):
    models: list[TagModel] = [TagModel(**tag.model_dump()) for tag in tags]
    db.bulk_save_objects(models)
    db.commit()
    db.refresh(models[0])
    return models[0]


@clock(active=True)
def insert_tag_readings(readings: list[TagReadingCreate], session: Session):
    readings_data = [TagModel(**reading.model_dump()) for reading in readings]
    before_insert = len(session.new)
    session.bulk_save_objects(readings_data)
    session.commit()
    # for reading in readings_data:
    #     session.refresh(reading)
    return len(readings_data)


def add_readings_from_dicts(readings: list[dict], db: Session):
    models: list[TagModel] = [TagModel(**tag) for tag in readings]
    db.bulk_save_objects(models)
    db.commit()
    db.refresh(models[0])
    return models[0]


def insert_tag_reading(reading: TagReadingCreate, session: Session):
    tag_model = TagModel(**reading.model_dump())
    session.add(reading)
    session.commit()
    session.refresh(tag_model)
    return tag_model


