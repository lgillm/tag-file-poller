from pydantic import BaseModel
from datetime import datetime
from typing import Union

class TagReadingBase(BaseModel):
    location: str
    devicename: str
    t_stamp: datetime
    quality: int
    date_value: datetime
    float_value: Union[float, int, None, str]
    string_value: Union[float, int, None, str]


class TagReadingCreate(TagReadingBase):
    pass


class TagReading(TagReadingBase):
    class Config:
        from_attribute = True

