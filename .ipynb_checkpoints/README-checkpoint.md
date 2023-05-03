# Option Charts

This repo crunshes some data to visualize the behavior of options in comparison to Bitcoin.
If you find bugs, I'd be happy to get to know them ;)!
It's certainly not perfect form reusability, naming consistency or other aspects.

The basic idea is, that you:
1. take the `instruments.ipynb` to select an instrument, then
2. choose some strikes that have enough trades before the selected expiry
3. copy one of the notebooks
4. enter the expiry and strikes to the config obj, run the Notebook and check out the charts.
For the charts I used Plotly. This means, if you drag the mouse horizontally, vertically or in a rectangle, you can drill into some areas.
You can also hide some plots by clickin on the corresponding legend entry.

## Requirements
Python 3
Virtualenv

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
