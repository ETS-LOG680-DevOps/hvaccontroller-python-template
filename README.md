
# HvacController-Python

## How to use PipEnv to create a virtual environment
### Install required packages from requirements.txt
At root level in terminal, enter command : ```pipenv install```

Select the python interpreter of this virtual environment
### To install new package
```pipenv install <package>```

### To generate requirements.txt
```pipenv lock -r > requirements.txt```


## To run project
In terminal: ```python3 main.py```

## Unit Test

### To run unit test
At the root folder: run ```python -m unittest discover -v```

## SignalR & API
The client use SignalR to receive data and get request to activate the hvac unit
Server: http://178.128.234.252:32775/

### SignalR
To receive continuous data from the server, we use SignalR. SignalR allow us to mimic real-time data sent to the client. https://github.com/mandrewcito/signalrcore

To receive data from the server, start a connection with SignalR and connect to this hub: *{serverurl}/SensorHub?token={token}*.

### Endpoints
To control the Hvac, we use GET HTTP requests. The nbTicks represent for how long the AC or Heater will be activated.

- To turn off the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOffHvac*
- To start the AC of the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOnAc/{nbTicks}*
- To start the Heater of the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOnHeater/{nbTicks}*

The server also has a Healthcheck endpoint to test if the server is running properly:
- Healtcheck : *GET {serverUrl}/api/health*

