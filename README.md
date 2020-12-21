
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

if using virtual environnment, in terminal: ```<path>/python.exe main.py```
## Unit Test

### To run unit test
At the root folder: run ```python -m unittest discover -v```