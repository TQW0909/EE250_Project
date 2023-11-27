import time
import grovepi
import paho.mqtt.client as mqtt
import json
import ssl

# sensor setup
# Connect Temp & Hum Sensor to D4
temp_humidity_sensor = 4  
sensor_type = 0  # if didnt work change to 0 
# Connect Light Sensor to A0
light_sensor = 0

# Connect the LED to D2
led = 2
grovepi.pinMode(led, "OUTPUT")
grovepi.digitalWrite(led, 0)  # LED on

# MQTT settings
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 8883
MQTT_TOPIC_SENSOR = "garden/sensorData"
MQTT_TOPIC_CONTROL = "garden/control"

# Setup MQTT client
client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt", tls_version=ssl.PROTOCOL_TLSv1_2)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_CONTROL)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(payload)
        if msg.topic == MQTT_TOPIC_CONTROL:
            # Check the control message 
            led_status = payload.get("led")
            if led_status == "on":
                grovepi.digitalWrite(led, 1)  # LED on
                time.sleep(5)
                grovepi.digitalWrite(led, 0)  # LED off
    except Exception as e:
        print("Error handling message:", e)

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

while True:
    try:
        # Read data
        [temp, humidity] = grovepi.dht(temp_humidity_sensor, sensor_type)
        light_intensity = grovepi.analogRead(light_sensor)

        message = json.dumps({
            "temperature": temp,
            "humidity": humidity,
            "light_intensity": light_intensity,
        })

        print(message)

        client.publish(MQTT_TOPIC_SENSOR, message)

    except IOError as e:
        print("Error reading sensors:", e)

    time.sleep(60)


client.loop_stop()
