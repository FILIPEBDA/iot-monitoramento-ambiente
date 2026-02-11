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
            ok = write_to_influx(client_influx, payload)

            if ok:
                print("Dados gravados no InfluxDB")
            else:
                print("Salvo no buffer")

        except Exception as e:
            print("Erro ao processar mensagem:", e)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("Conectando ao broker MQTT...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Mantém o processo vivo
    client.loop_forever()

