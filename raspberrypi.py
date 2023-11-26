import paho.mqtt.client as mqtt
import time
import json
import Adafruit_DHT

# need to define the sensor and pin
sensor = Adafruit_DHT.DHT22
pin = 'GPIO_PIN_NUMBER'

# MQTT settings
MQTT_BROKER = "MQTT_BROKER_ADDRESS"
MQTT_PORT = 1883
MQTT_TOPIC = "garden/sensorData"

# Setup MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    # Read  data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    light_intensity = read_light_sensor()  # Define this function based light sensor

    message = json.dumps({
        "temperature": temperature,
        "humidity": humidity,
        "light_intensity": light_intensity
    })

    client.publish(MQTT_TOPIC, message)

    time.sleep(60)
