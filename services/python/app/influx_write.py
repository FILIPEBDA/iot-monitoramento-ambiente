from influxdb import InfluxDBClient
import time

INFLUX_HOST = "influxdb"
INFLUX_PORT = 8086
INFLUX_DB = "umidade"

def get_influx_client():
    for attempt in range(10):
        try:
            client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
            client.create_database(INFLUX_DB)
            client.switch_database(INFLUX_DB)
            print("Conectado ao InfluxDB")
            return client
        except Exception as e:
            print("Aguardando InfluxDB...", e)
            time.sleep(3)
    raise Exception("InfluxDB indisponível")

def write_to_influx(client, dados):
    json_body = [{
        "measurement": "umidade",
        "tags": {"device_id": dados["device_id"]},
        "fields": {
            "temperature": float(dados["temperature"]),
            "humidity": float(dados["humidity"])
        }
    }]
    client.write_points(json_body)

