"""Routing.

:GET /node:
"""

from fastapi import APIRouter
from dataclasses import asdict

from src.amedas.schemas.node import Node as node_schema
from src.amedas.libs.node import Node as node_lib

router = APIRouter()


@router.get("/node", response_model=node_schema)
async def node_status():
    return node_schema.model_validate(asdict(node_lib()))
