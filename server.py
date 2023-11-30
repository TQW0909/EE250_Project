import threading
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

import requests
import json
import time
import paho.mqtt.client as mqtt
import ssl

app = Flask('Garden Monitor Server')

OWM_API_KEY = '62d326640bcae67b9575cc115e7ec392' # OpenWeatherMap API Key
DEFAULT_ZIP = 90089

# MQTT setup
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 8883 # Encrypted Broker port
MQTT_TOPIC_SENSOR = "garden/sensorData"
MQTT_TOPIC_CONTROL = "garden/control"

app_data = {
    "temperature"   : "",
    "humidity"      : "",
    "light"         : "",
    "weather"       : "",
    "cloudiness"    : ""
}

# Fetches weather from weather API (Virtual sensor)
def get_weather(zip_code):

    # Getting the lat and lon vlaues from a zip code
    coordinate_params = {
        'appid': OWM_API_KEY,
        'zip': str(zip_code) + ",US"
    }

    coordinate_response = requests.get('http://api.openweathermap.org/geo/1.0/zip', coordinate_params)

    if coordinate_response.status_code == 200: # Status: OK
        coords = coordinate_response.json()
    else:
        print('error: got response code %d' % coordinate_response.status_code)
        print(coordinate_response.text)
        return -1

    # After obtaining the lat and lon, make call to API to get data
    params = {
        'appid': OWM_API_KEY,
        'lat': coords["lat"],
        'lon': coords["lon"], 
        'units': "imperial"
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()
        output = {
            'weather' : data["weather"][0]["main"],
            'cloudiness' : data["clouds"]["all"]
        }
        return output

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return -1

# Function to be run by the thread in the background to periodically obtain the weather data 
def update_weather():
    while True:
        data = get_weather(DEFAULT_ZIP)
        if data != -1:
            app_data['weather'] = data["weather"]
            app_data['cloudiness'] = data["cloudiness"]
        else:
            print ("error")
            return -1
        time.sleep(60)

# Creating a thread to run in the backgrount to provide constant update to weather data
thread = threading.Thread(target=update_weather)
thread = thread.start()

# Handling the sensor data sent from rpi to brocker
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(payload)
        app_data['temperature'] = payload["temperature"]
        app_data['light'] = payload["light_intensity"]
        app_data["humidity"] = payload["humidity"]
    except Exception as e:
        print("Error handling message:", e)

# Setting up encrypted MQTT
client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC_SENSOR)
client.loop_start()

# Landing/main page
@app.route('/')
def index():
    return render_template('index.html')

# Get all the data stored
@app.route('/get-data')
def get_data():
    print(app_data)
    return json.dumps(app_data)

# Sends a signal to broker then rpi to water the plants
@app.route('/water-garden', methods={'POST'})
def water_garden():
    command = {
        "led" : "on"
    }
    client.publish(MQTT_TOPIC_CONTROL, json.dumps(command))
    return json.dumps({"status" : "success"})

if __name__ == '__main__':

    app.run(debug=False, host= '0.0.0.0', port=5555)