"""This sript is the main program for Oxygène HVAC"""

import sys
import time
import json
import logging
import os
import requests # pylint: disable=import-error
from signalrcore.hub_connection_builder import HubConnectionBuilder # pylint: disable=import-error
# import mysql.connector as mysql


class Main:
    """Main Class"""
    def __init__(self):
        self._hub_connection = None
        self.host = os.environ["HVAC_HOST"]
        self.token = os.environ["HVAC_TOKEN"]

    def __del__(self):
        if self._hub_connection is not None :
            self._hub_connection.stop()

    def setup(self):
        """Setup function"""
        self.set_sensor_hub()

    def start(self):
        """Start function"""
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

        self._hub_connection.stop()
        sys.exit(0)

    def set_sensor_hub(self):
        """Function to connect to the server."""
        self._hub_connection = HubConnectionBuilder()\
        .with_url(f"{self.host}/SensorHub?token={self.token}")\
        .configure_logging(logging.INFO)\
        .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 999
        }).build()

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(
            f"||| An exception was thrown closed: {data.error}"))

    def on_sensor_data_received(self, data):
        """Function to extract the date and the temperature when we reveive data"""
        try:
            print(data[0]["date"]  + " --> " + data[0]["data"])
            temperature = float(data[0]["data"])

            self.analyze_datapoint(temperature)
        # pylint: disable=broad-except
        except Exception as err:
            print(err)

    def analyze_datapoint(self, data):
        """Function to activate the AC or heater if the temperature is too high or too low"""
        if data >= 80.0 :
            self.send_action_to_hvac("TurnOnAc", 6)
        elif data <= 20.0 :
            self.send_action_to_hvac("TurnOnHeater", 6)

    def send_action_to_hvac(self, action, ticks):
        """Function to send order to the hvac"""
        req = requests.get(f"{self.host}/api/hvac/{self.token}/{action}/{ticks}")
        details = json.loads(req.text)
        print(details)

if __name__ == '__main__':
    main = Main()
    main.start()
