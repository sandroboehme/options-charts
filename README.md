# Option Charts

This repo crunches some data to visualize the behavior of options in comparison to Bitcoin.
If you find bugs, I'd be happy to get to know them personally ;)!
It's certainly not perfect from reusability, naming consistency or other aspects.

The basic idea is, that you:
1. take the `instruments.ipynb` to set an expiration and copy the strikes, then
2. duplicate a notebook and insert the expiration and strikes.
3. After that you can check if the plots are overlaying too much.
   1. If they do, check the surface charts to see which strikes have the least data
   2. remove those strikes from the config and rerun the notebook.
   3. Refine the charts by repeating the process.
4. Make sure to understand which charts contain interpolated data and which don't.
5. Check if that all makes sense to you or not. I'd be happy if you share your thoughts!

For the charts I used Plotly which has some nice interactive features: 
1. if you drag the mouse horizontally, vertically or in a rectangle, you can drill down into some areas.
2. you can click on legend entries to hide the corresponding plots
3. you can double click on legend entries to show exclusively those corresponding plots

The Bitcoin price / value is always in gold / black.

If you neeed newer Bitcoin data, just run the 'readBitstampBTCdata.ipynb` notebook.
The options data will be downloaded automagically from Deribit if you have choosen an expiration or strike that isn't there yet.

I'm happy to accept PRs for using colors with a better contrast ;-)

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

## Exit virtualenv
``` 
deactivate
```
