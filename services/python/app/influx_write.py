from influxdb import InfluxDBClient
import time

INFLUX_HOST = "influxdb"
INFLUX_PORT = 8086
INFLUX_DB = "umidade"

client = InfluxDBClient(
    host=INFLUX_HOST,
    port=INFLUX_PORT
)

# Cria o banco se não existir
client.create_database(INFLUX_DB)
client.switch_database(INFLUX_DB)

def write_to_influx(dados):
    json_body = [
        {
            "measurement": "ambiente",
            "tags": {
                "device": dados["device_id"]
            },
            "time": int(time.time() * 1000),  # timestamp opcional
            "fields": {
                "temperature": float(dados["temperature"]),
                "humidity": float(dados["humidity"])
            }
        }
    ]

    client.write_points(json_body)

