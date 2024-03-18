"""Schema.

:class Node:
"""

from datetime import datetime
from pydantic import BaseModel, Field


class Node(BaseModel):
    cpu: str = Field(..., description="CPU")
    platformname: str = Field(..., description="Platform")
    hostname: str = Field(..., description="Hostname")
    soc_temperature: float = Field(..., description="SOC Temperature['C]")
    date_time: datetime = Field(..., description="Measured Date-Time")
