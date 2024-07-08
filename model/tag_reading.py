from sqlalchemy import Column, String, DateTime, Numeric, Boolean, Integer
from sqlalchemy.sql import func
from db.base import Base

class TagReading(Base):
    __tablename__ = 'tag_readings'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    location = Column(String(255))
    devicename = Column(String(255))
    t_stamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    quality = Column(Integer)
    date_value = Column(DateTime(timezone=True))
    float_value = Column(Numeric(precision=37, scale=10))
    string_value = Column(String(255))
