# EE250_Project: Remote Garden Monitor

GitHub Repo: https://github.com/TQW0909/EE250_Project.git

Our project utilizes the GrovePI sensors on a RaspberryPi to track the temperature, humidity, and light data regarding a garden, and is complemented by weather data (current weather condition and cloudiness percentage) fetched from the OpenWeather API. The data is communicated between the Raspberry Pi and our server hosted on Azure through encrypted MQTT.

The project provides a user interface accessible through a web browser to visualize all the collected data in real-time. In addition, we have also incorporated a controller feature to allow the user to water the garden with a click of a button on the web page.


## Team Members

- Tingqi (Ting) Wang (twang356@usc.edu)

- Jeremiah Lim (limjerem@usc.edu)

## Execution Instructions

List of external libraries:

- ssl
- threading
- flask
- requests
- json
- time
- paho-mqtt
- grovepi

### Server

Run on Azure

To run the server: `python3 server.py`

### Rpi

Run on Rpi

To run the Rpi code: `python3 rasberrypi.py`

### Client

On web browser visit `http://20.25.184.178:5555/`

Note: The ip address of another Azure server will be different (20.25.184.178 is IP of our Azure server) and the port the server is running on is determined in the `server.py` file.
