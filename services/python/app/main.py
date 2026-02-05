from influx_write import get_influx_client
from mqtt_client import start_mqtt

def main():
    print("Serviço Python IoT iniciado")
    client_influx = get_influx_client()
    start_mqtt()

if __name__ == "__main__":
    main()

