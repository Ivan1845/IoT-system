from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from file_datasource import FileDatasource
from schema.parking_schema import ParkingSchema
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, topic, datasource, delay):
    datasource.startReading()
    while True:
        time.sleep(delay)

        agg_data, parking_data = datasource.read()

        #Відправляємо дані про ями
        msg_agg = AggregatedDataSchema().dumps(agg_data)
        client.publish(topic, msg_agg)

        #Відправляємо дані про паркінг
        msg_parking = ParkingSchema().dumps(parking_data)
        client.publish("parking_data_topic", msg_parking)


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    # Infinity publish data
    publish(client, config.MQTT_TOPIC, datasource, config.DELAY)


if __name__ == "__main__":
    run()
