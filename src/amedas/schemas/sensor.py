"""Schema.

:class DataSet:
:class Sensor:
:class Amedas:
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class Sensor(BaseModel):
    name: str = Field(..., description="Sensor Name")
    i2c_address: int = Field(..., description="I2C Address")


class DataSet(BaseModel):
    name: str = Field(..., description="Type Name")
    date_time: datetime = Field(..., description="Measured Date-Time")
    data: float = Field(..., description="Measurement")


class Amedas(BaseModel):
    sensor: Sensor
    list_dataset: List[DataSet]
