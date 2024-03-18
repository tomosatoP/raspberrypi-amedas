"""Routing.

:GET /sensors:
:GET /sensors/{i2c_address}:
"""

from fastapi import APIRouter
from typing import List
from dataclasses import asdict

import src.amedas.schemas.sensor as sensor_schema
import src.amedas.libs.sensor as sensor_lib

router = APIRouter()


@router.get("/sensors", response_model=list[sensor_schema.Sensor])
async def list_sensor():
    result: List[sensor_schema.Sensor] = []

    for address in sensor_lib.Sensor.list_i2c_address():
        result.append(
            sensor_schema.Sensor.model_validate(
                asdict(sensor_lib.Sensor(i2c_address=address))
            )
        )
    return result


@router.get("/sensors/{i2c_address}", response_model=sensor_schema.Amedas)
async def list_sensor_data(i2c_address: int):
    return sensor_schema.Amedas.model_validate(
        asdict(sensor_lib.Amedas(sensor=sensor_lib.Sensor(i2c_address=i2c_address)))
    )
