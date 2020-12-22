from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import sys
import requests
import json
import time
import os
import mysql.connector as mysql

# https://github.com/mandrewcito/signalrcore

class Main:
    def __init__(self):
        self._hub_connection = None
        self.TOKEN = "<insert token here>" 
    
    def __del__(self):
        if (self._hub_connection != None):
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()        

    def start(self):
        self.setup()
        self._hub_connection.start()
        
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

        self._hub_connection.stop()
        sys.exit(0)

    def setSensorHub(self):
        self._hub_connection = HubConnectionBuilder()\
        .with_url(f"http://ec2-52-7-99-159.compute-1.amazonaws.com:32775/SensorHub?token={self.TOKEN}")\
        .configure_logging(logging.INFO)\
        .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 999
        }).build()

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(f"||| An exception was thrown closed: {data.error}"))

    def onSensorDataReceived(self, data):
        try:        
            print(data[0]["date"]  + " --> " + data[0]["data"])
            date = data[0]["date"]
            dp = float(data[0]["data"])

            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)
    
    def analyzeDatapoint(self, date, data):
        if (data >= 80.0):                
            self.sendActionToHvac(date, "TurnOnAc", 6)
        elif (data <= 20.0):                
            self.sendActionToHvac(date, "TurnOnHeater", 6)

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"http://ec2-52-7-99-159.compute-1.amazonaws.com:32775/api/hvac/{self.TOKEN}/{action}/{nbTick}") 
        details = json.loads(r.text)
        print(details)

if __name__ == '__main__':
    main = Main()
    main.start()



