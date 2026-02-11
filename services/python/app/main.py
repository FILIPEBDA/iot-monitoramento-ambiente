from influx_write import get_influx_client, monitor_influx
from mqtt_client import start_mqtt
import threading

def main():
    client_influx = get_influx_client()

    t = threading.Thread(
        target=monitor_influx,
        args=(client_influx,),
        daemon=True
    )
    t.start()

    start_mqtt(client_influx)

if __name__ == "__main__":
    main()

