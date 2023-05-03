# Option Charts

This repo crunshes some data to visualize the behavior of options in comparison to Bitcoin.
If you find bugs, I'd be happy to get to know them ;)!
It's certainly not perfect from reusability, naming consistency or other aspects.

The basic idea is, that you:
1. take the `instruments.ipynb` to select an instrument, then
2. find some strikes that have enough trades before the selected expiry (data might be downloaded automagically if they aren't there yet)
3. copy one of the notebooks if you want
4. enter/change the expiry and strikes in the config obj, run the Notebook and check out the charts.
For the charts I used Plotly. This means, if you drag the mouse horizontally, vertically or in a rectangle, you can drill into some areas.
You can also hide some plots by clicking on the corresponding legend entry.

If you neeed newer Bitcoin data, just run the 'readBitstampBTCdata.ipynb` notebook

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
c
```

## Run
``` 
jupyter lab
```

## Exit virtualenv
``` 
deactivate
```
