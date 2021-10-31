"""This sript is the main program for Oxygène HVAC"""

import logging
import sys
import json
import time
import os
import requests # pylint: disable=import-error
from signalrcore.hub_connection_builder import HubConnectionBuilder # pylint: disable=import-error
# import mysql.connector as mysql


class Main:
    """Main Class"""
    def __init__(self):
        self._hub_connection = None
        self.host = os.environ["HVAC_HOST"]

        if os.getenv("HVAC_TOKEN") is None:
            self.token = "NOT_FOUND"
        else:
            self.token = os.environ["HVAC_TOKEN"]

        if os.getenv("HVAC_COLD_LIMIT") is None:
            self.cold_limit = 20
        else :
            self.cold_limit = os.environ["HVAC_COLD_LIMIT"]

        if os.getenv("HVAC_HOT_LIMIT") is None:
            self.hot_limit = 80
        else :
            self.hot_limit = os.environ["HVAC_HOT_LIMIT"]

        if os.getenv("HVAC_TICKS") is None:
            self.ticks = 6
        else :
            self.ticks = os.environ["HVAC_TICKS"]

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        """Setup function"""
        self.set_sensor_hub()

    def start(self):
        """Start function"""
        if self.token == "NOT_FOUND":
            print("No token found ! The program cannot be executed !")
            sys.exit(0)

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
        if data >= float(self.hot_limit):
            self.send_action_to_hvac("TurnOnAc", self.ticks)
        elif data <= float(self.cold_limit):
            self.send_action_to_hvac("TurnOnHeater", self.ticks)

    def send_action_to_hvac(self, action, ticks):
        """Function to send order to the hvac"""
        request = requests.get(f"{self.host}/api/hvac/{self.token}/{action}/{ticks}")
        details = json.loads(request.text)
        print(details)

if __name__ == '__main__':
    main = Main()
    main.start()
