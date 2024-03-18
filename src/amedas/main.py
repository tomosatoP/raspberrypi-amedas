"""Entrypoint for AMEDAS.

Provide routing to *node* and *sensor*.
  *Node* accesses information on the Rasberry Pi.
  *Sensor* accesses the value of each sensor.
"""

from fastapi import FastAPI

from src.amedas.routers import node, sensor

app = FastAPI()

app.include_router(node.router)
app.include_router(sensor.router)
