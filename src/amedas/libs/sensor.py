"""Access the values of each sensor.

+-----------------+-----------+-------------------------------------+
|sensor name      |i2c_address| dataset name                        |
+=================+===========+=====================================+
|"MOUNTED TSL2572"|0x39       |"ILLUMINANCE"                        |
+-----------------+-----------+-------------------------------------+
|"EXTERNAL BME280"|0x76       |"TEMPERATURE", "HUMIDITY", "PRESSURE"|
+-----------------+-----------+-------------------------------------+
|"MOUNTED BMD280" |0x77       |"TEMPERATURE", "HUMIDITY", "PRESSURE"|
+-----------------+-----------+-------------------------------------+
"""

from typing import List
from dataclasses import dataclass, field
from cgsensor import BME280, TSL2572
from datetime import datetime

_SENSOR = {0x39: "MOUNTED TSL2572", 0x76: "EXTERNAL BME280", 0x77: "MOUNTED BME280"}


@dataclass
class DataSet:
    """Observations and their information."""

    name: str = ""  #: name
    date_time: datetime = datetime.now()  #: datetime when the value was obtained
    data: float = 0.0  #: observed value


@dataclass
class Sensor:
    """Sensor name and i2c address."""

    name: str = ""  #: sensor name
    i2c_address: int = 0x00  #: i2c address of sensor

    def __post_init__(self):
        self.name = _SENSOR[self.i2c_address]

    @classmethod
    def list_i2c_address(cls) -> List[int]:
        """List of valid sensors for the node.

        :returns: List of valid sensor i2c addresses
        """
        result: List[int] = []

        for i2c_address in _SENSOR.keys():
            match i2c_address:
                case 0x39:
                    if TSL2572().check_id():
                        result.append(i2c_address)
                case 0x76 | 0x77:
                    if BME280(i2c_address).check_id():
                        result.append(i2c_address)

        return result


@dataclass
class Amedas:
    """Get the measurement results of the indoor environment."""

    sensor: Sensor  #: sensor
    list_dataset: List[DataSet] = field(default_factory=list)  #: List of dataset

    def __post_init__(self):
        match self.sensor.i2c_address:
            case 0x39:
                device = TSL2572()
                if device.single_auto_measure():
                    self.list_dataset.append(
                        DataSet(
                            name="ILLUMINANCE",
                            date_time=datetime.now(),
                            data=device.illuminance,
                        )
                    )
            case 0x76 | 0x77:
                device = BME280(self.sensor.i2c_address)
                if device.forced():
                    self.list_dataset.append(
                        DataSet(
                            name="TEMPERATURE",
                            date_time=datetime.now(),
                            data=device.temperature,
                        )
                    )
                    self.list_dataset.append(
                        DataSet(
                            name="HUMIDITY",
                            date_time=datetime.now(),
                            data=device.humidity,
                        )
                    )
                    self.list_dataset.append(
                        DataSet(
                            name="PRESSURE",
                            date_time=datetime.now(),
                            data=device.pressure,
                        )
                    )


if __name__ == "__main__":
    print(__file__)
