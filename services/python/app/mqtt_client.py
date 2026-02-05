import json
import paho.mqtt.client as mqtt
from influx_write import write_to_influx

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "umidade"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Conectado ao MQTT")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic)

    try:
        payload = json.loads(msg.payload.decode())
        print("Payload:", payload)

        if "temperature" not in payload or "humidity" not in payload:
            print("JSON inválido:", payload)
            return

        write_to_influx(payload)
        print("Dados gravados no InfluxDB")

    except Exception as e:
        print("Erro ao processar mensagem MQTT:", e)


def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

