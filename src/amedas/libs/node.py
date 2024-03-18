"""Access information about Raspberry Pi."""

from subprocess import PIPE, Popen
from datetime import datetime
from dataclasses import dataclass
import platform


@dataclass
class Node:
    """Get node information."""

    cpu: str = platform.machine()  #: CPU Type Name
    platformname: str = platform.platform()  #: Platform Information
    hostname: str = platform.node()  #: Hostname
    date_time: datetime = datetime.now()  #: Measured Date and Time
    soc_temperature: float = -273.15  #: SOC Temperature ['C]

    def __post_init__(self):
        self.date_time = datetime.now()

        command: list = ["cat", "/sys/class/thermal/thermal_zone0/temp"]
        with Popen(args=command, stdout=PIPE, text=True) as res:
            if not res.returncode:
                self.soc_temperature = float(res.communicate()[0]) / 1000.0


if __name__ == "__main__":
    print(__file__)
