from influxdb import InfluxDBClient
import time
import json
import os
import threading

INFLUX_HOST = "influxdb"
INFLUX_PORT = 8086
INFLUX_DB = "umidade"
BUFFER_FILE = "/app/buffer.jsonl"

lock = threading.Lock()
influx_online = False


def get_influx_client():
    global influx_online
    for attempt in range(10):
        try:
            client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
            client.ping()
            client.create_database(INFLUX_DB)
            client.switch_database(INFLUX_DB)
            influx_online = True
            print("Conectado ao InfluxDB")
            return client
        except Exception as e:
            influx_online = False
            print("Aguardando InfluxDB...", e)
            time.sleep(3)
    raise Exception("InfluxDB indisponível")


def save_to_buffer(dados):
    with lock:
        with open(BUFFER_FILE, "a") as f:
            f.write(json.dumps(dados) + "\n")


def replay_buffer(client):
    if not os.path.exists(BUFFER_FILE):
        return

    print("♻️ Reenviando buffer...")
    with lock:
        lines = open(BUFFER_FILE).readlines()
        open(BUFFER_FILE, "w").close()

    for line in lines:
        dados = json.loads(line)
        write_to_influx(client, dados, buffering=False)


def monitor_influx(client):
    global influx_online
    last_state = influx_online

    while True:
        try:
            client.ping()
            influx_online = True
        except:
            influx_online = False

        # Só quando voltar
        if not last_state and influx_online:
            replay_buffer(client)

        last_state = influx_online
        time.sleep(5)


def write_to_influx(client, dados, buffering=True):
    global influx_online

    json_body = [{
        "measurement": "umidade",
        "tags": {"device_id": dados["device_id"]},
        "fields": {
            "temperature": float(dados["temperature"]),
            "humidity": float(dados["humidity"])
        }
    }]

    try:
        client.write_points(json_body)
        influx_online = True
    except Exception as e:
        influx_online = False
        print("Influx indisponível, salvando no buffer...", e)
        if buffering:
            save_to_buffer(dados)


