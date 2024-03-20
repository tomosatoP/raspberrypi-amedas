# Monitor indoor environment like AMeDAS.

Indoor environmental monitoring using RPZ-IR-Sensor for Raspberry Pi 3 A+

Referenced Books: "動かして学ぶ！Python FastAPI 開発入門" ISBN978-4-7981-7771-7

## Hardware

* [Raspberry Pi 3A+](https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/)
* [RPZ-IR-Sensor](https://www.indoorcorgielec.com/products/rpz-ir-sensor/)
* uSD-CARD 16GByte

## Setup Raspberry Pi 3A+

[setup](RASPI3APLUS.md)

## Download & Install

~~~sh
git clone --depth 1 https://github.com/tomosatoP/raspberrypi-amedas.git

cd raspberrypi-amedas
mkdir .dockervenv

docker compose build --pull --no-cache
# create "poetry.lock"
docker compose run --entrypoint "poetry update --lock --only main" amedas
# install packages
docker compose run --entrypoint "poetry install --no-root --only main" amedas
~~~

## Run

~~~sh
cd raspberrypi-amedas
docker compose up -d
~~~

## Check
### node
~~~sh
curl -X GET http://localhost:8000/node
~~~
~~~json
{
    "cpu": "aarch64",
    "platformname": "Linux-6.6.20+rpt-rpi-2712-aarch64-with-glibc2.36",
    "hostname": "f9f29ef5bc4a",
    "soc_temperature": 49.6,
    "date_time": "2024-03-18T11:17:04.958436"
}
~~~

### sensors

~~~sh
curl -X GET http://localhost:8000/sensors
~~~
~~~json
[
    {
        "name": "MOUNTED TSL2572",
        "i2c_address": 57
    },
    {
        "name": "EXTERNAL BME280",
        "i2c_address": 118
    },
    {
        "name": "MOUNTED BME280",
        "i2c_address": 119
    }
]
~~~

### sensors/{i2c_address}

~~~sh
curl -X GET http://localhost:8000/sensors/118
~~~
~~~json
{
    "sensor": {
        "name": "EXTERNAL BME280",
        "i2c_address": 118
    },
    "list_dataset": [
        {
            "name": "TEMPERATURE",
            "date_time": "2024-03-18T11:23:08.952919",
            "data": 22.0
        },
        {
            "name": "HUMIDITY",
            "date_time": "2024-03-18T11:23:08.952938",
            "data": 33.7
        },
        {
            "name": "PRESSURE",
            "date_time": "2024-03-18T11:23:08.952940",
            "data": 1016.4
        }
    ]
}
~~~
---