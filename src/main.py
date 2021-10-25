from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import sys
import requests
import json
import time
import os
# import mysql.connector as mysql

class Main:
    def __init__(self):
        self._hub_connection = None
        self.HOST = os.environ["HVAC_HOST"]

        if (os.getenv("HVAC_TOKEN") == None):
            self.TOKEN = "NOT_FOUND"
        else:
            self.TOKEN = os.environ["HVAC_TOKEN"]

        if (os.getenv("HVAC_COLD_LIMIT") == None):
            self.COLD_LIMIT = 20
        else :
            self.COLD_LIMIT = os.environ["HVAC_COLD_LIMIT"]

        if (os.getenv("HVAC_HOT_LIMIT") == None):
            self.HOT_LIMIT = 80
        else :
            self.HOT_LIMIT = os.environ["HVAC_HOT_LIMIT"]

        if (os.getenv("HVAC_TICKS") == None):
            self.TICKS = 6
        else :
            self.TICKS = os.environ["HVAC_TICKS"]
       
    
    def __del__(self):
        if (self._hub_connection != None):
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()        

    def start(self):
        if (self.TOKEN == "NOT_FOUND"):
            print("No token found ! The program cannot be executed !")
            sys.exit(0)

        self.setup()
        self._hub_connection.start()
        
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

        self._hub_connection.stop()
        sys.exit(0)

    def setSensorHub(self):
        self._hub_connection = HubConnectionBuilder()\
        .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")\
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
        if (data >= float(self.HOT_LIMIT)):                
            self.sendActionToHvac(date, "TurnOnAc", self.TICKS)
        elif (data <= float(self.COLD_LIMIT)):                
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKS)

    def sendActionToHvac(self, date, action):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKS}") 
        details = json.loads(r.text)
        print(details)

if __name__ == '__main__':
    main = Main()
    main.start()