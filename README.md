
## Requirements
Python 3

## Installation
```
# Uses system's default Python version to create the virtual environment
virtualenv --python python3 env
# If you want to use a specific path you can pass it like this:
virtualenv --python=/usr/local/bin/python3.9 env
source env/bin/activate
pip3 install -r requirements.txt
```

## Run
``` 
jupyter lab
```

## Open the Notebook
```
option_prices.ipynb
```

## Exit virtualenv
``` 
deactivate
```
