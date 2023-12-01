# EE250_Project: Remote Garden Monitor

GitHub Repo: https://github.com/TQW0909/EE250_Project.git

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
