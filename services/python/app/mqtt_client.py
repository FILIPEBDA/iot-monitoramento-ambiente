import json
import time
import paho.mqtt.client as mqtt
from influx_write import write_to_influx

def start_mqtt(client_influx):
    MQTT_BROKER = "mosquitto"
    MQTT_PORT = 1883
    MQTT_TOPIC = "umidade"

    def on_connect(client, userdata, flags, reason_code, properties=None):
        print("Conectado ao MQTT")
        client.subscribe(MQTT_TOPIC)

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            write_to_influx(client_influx, payload)
            print("Dados gravados no InfluxDB")
        except Exception as e:
            print("Erro ao gravar:", e)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("Conectando ao broker MQTT...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # BLOQUEIA O PROCESSO (mantém vivo)
    client.loop_forever()

